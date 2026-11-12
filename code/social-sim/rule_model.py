"""AIを使わず、決まった式で各人の拠出を決める「規則型」の比較相手(#172)。

使い方: python rule_model.py [--seeds 1-20] [--out runs/rule]
4条件(partner/stranger × 罰あり/なし)を seed ごとに回し、run.py と同じ形の記録を残す。
記録は compare.py と robustness.py でそのまま判定できる。

式は次の3つだけ。係数は回す前に決め、人間の推移に合わせて動かしていない。
1. 見込み: 次の見込み = 0.4 × 今の見込み + 0.6 × 今回ほかの人が入れた平均
   (Fischbacher & Gächter 2010 の、見込みは観察した値に寄っていくという結果を単純にしたもの)
2. 拠出: 型ごとの式(見込み) + 罰で積み上がった上乗せ + ゆらぎ(正規分布、標準偏差2)
   型の割合は Fischbacher, Gächter & Fehr 2001: 条件付き協力50%、ただ乗り30%、山型14%、その他6%
3. 罰: 平均より少なく入れた人に、差1ポイントにつき0.2点を、全員が付ける
   受けた罰1点につき、次の回から拠出を1ポイント上乗せする
注意: 罰の係数0.2は、Fehr & Gächter 2000 の図5(受けた罰の量)を見て決めた。
そのため、物差し5(罰の向き)は、この比較相手にとっては検証にならない。
"""
import argparse
import os
import random
import sys
from dataclasses import asdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.games.public_goods import Config, apply_punishment, payoffs  # noqa: E402
from sim.record import Run  # noqa: E402

TYPES = [("cc", 0.50), ("fr", 0.30), ("hump", 0.14), ("other", 0.06)]
PARAMS = {
    "belief_first_mean": 10, "belief_first_sd": 4,   # 1回目の見込み(仮置き。人間の分布は手元にない)
    "belief_keep": 0.4,                              # 見込みのうち、前の見込みを残す割合
    "cc_slope": 0.9,                                 # 条件付き協力: 見込みの9割を入れる
    "noise_sd": 2.0,                                 # 1回ごとのゆらぎ
    "punish_rate": 0.2,                              # 平均との差1ポイントにつき付ける罰
    "punish_deadzone": 1.0,                          # 差がこれ以下なら罰しない
    "deter": 1.0,                                    # 受けた罰1点あたりの上乗せ
}


class RuleBackend:
    """Run に渡すための名札。AIは呼ばない。"""
    name = "rule:fg2010"

    def version(self):
        return "rule_model.py"


def assign_types(n, rng):
    k = [round(n * p) for _, p in TYPES]
    k[0] += n - sum(k)
    types = [t for (t, _), m in zip(TYPES, k) for _ in range(m)]
    rng.shuffle(types)
    return types


class Person:
    """kind が "llm" のときは、LLMが答えた表(table)・見込み・罰への反応(deter)を使う。"""

    def __init__(self, pid, kind, rng, endowment, llm=None):
        self.id = pid
        self.kind = kind
        self.e = endowment
        b = rng.gauss(PARAMS["belief_first_mean"], PARAMS["belief_first_sd"])
        self.belief = min(max(b, 0), endowment)
        self.extra = 0.0                       # 罰で積み上がった上乗せ
        self.fixed = rng.uniform(0, endowment)  # 「その他」の型が毎回入れる量の中心
        self.deter = PARAMS["deter"]
        self.llm = llm
        if llm:
            self.belief = float(llm["belief0"])
            self.deter = llm["deter"]

    def base(self):
        b = self.belief
        if self.kind == "llm":
            xs, ys = self.llm["xs"], self.llm["table"]
            for k in range(len(xs) - 1):
                if b <= xs[k + 1]:
                    t = (b - xs[k]) / (xs[k + 1] - xs[k])
                    return ys[k] + t * (ys[k + 1] - ys[k])
            return ys[-1]
        if self.kind == "cc":
            return PARAMS["cc_slope"] * b
        if self.kind == "fr":
            return 0.0
        if self.kind == "hump":
            return b if b <= self.e / 2 else self.e - b
        return self.fixed

    def contribute(self, rng):
        x = self.base() + self.extra + rng.gauss(0, PARAMS["noise_sd"])
        return int(min(max(round(x), 0), self.e))


def punish_points(contribs, cfg):
    k = len(contribs)
    pts = [[0] * k for _ in range(k)]
    for j in range(k):
        others = sum(contribs[q] for q in range(k) if q != j) / (k - 1)
        gap = others - contribs[j]
        if gap <= PARAMS["punish_deadzone"]:
            continue
        p = min(round(PARAMS["punish_rate"] * gap), cfg.punish_max)
        for i in range(k):
            if i != j:
                pts[i][j] = p
    return pts


def play(cfg, seed, out_root, llm_params=None, label="rule"):
    """llm_params を渡すと、型の割り振りの代わりに、LLMが答えた性質で各人を作る。"""
    rng = random.Random(f"{label}-{seed}")
    n = 24
    types = assign_types(n, rng)
    if llm_params:
        people = [Person(q["id"], "llm", rng, cfg.endowment, q) for q in llm_params]
    else:
        people = [Person(f"r{i:02d}", types[i], rng, cfg.endowment) for i in range(n)]
    name = f"{label}-s{seed}-game-{cfg.matching}-{'p' if cfg.punishment else 'n'}"
    run = Run(out_root, name, {"game": asdict(cfg), "groups": n // cfg.group_size, "seed": seed,
                               "personas": label, "variant": label, "params": PARAMS},
              RuleBackend(), [])
    run.manifest["people"] = [{"id": p.id, "kind": p.kind, "belief0": round(p.belief, 2),
                               "deter": p.deter} for p in people]
    match_rng = random.Random(seed)
    fixed = [list(range(g, g + cfg.group_size)) for g in range(0, n, cfg.group_size)]
    for r in range(1, cfg.rounds + 1):
        if cfg.matching == "partner":
            groups = fixed
        else:
            idx = list(range(n))
            match_rng.shuffle(idx)
            groups = [idx[g:g + cfg.group_size] for g in range(0, n, cfg.group_size)]
        for g, mem in enumerate(groups):
            c = [people[i].contribute(rng) for i in mem]
            base = payoffs(c, cfg)
            pts = punish_points(c, cfg) if cfg.punishment else [[0] * len(mem) for _ in mem]
            final = apply_punishment(base, pts, cfg)
            run.event({"group": g, "round": r, "members": [people[i].id for i in mem],
                       "contribs": c, "base": base, "points": pts, "final": final,
                       "kinds": [people[i].kind for i in mem]})
            for pos, i in enumerate(mem):
                p = people[i]
                others = sum(c[q] for q in range(len(mem)) if q != pos) / (len(mem) - 1)
                keep = PARAMS["belief_keep"]
                p.belief = keep * p.belief + (1 - keep) * others
                recv = sum(pts[q][pos] for q in range(len(mem)) if q != pos)
                p.extra = min(max(p.extra + p.deter * min(recv, 10), -cfg.endowment), cfg.endowment)
    run.finish({})
    return run.dir


def parse_seeds(s):
    lo, _, hi = s.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="1-20")
    ap.add_argument("--out", default=os.path.join(HERE, "runs", "rule"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for seed in parse_seeds(a.seeds):
        for matching in ("partner", "stranger"):
            for punishment in (False, True):
                print(play(Config(matching=matching, punishment=punishment), seed, a.out))


if __name__ == "__main__":
    main()
