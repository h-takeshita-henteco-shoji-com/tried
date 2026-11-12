"""前もって聞いた答え(語り)と、実際のゲームでの行動を、1人ずつ照らし合わせる(#172)。AIは呼ばない。

使い方: python say_do.py [--out runs/say-do-172.json]
- 語り: hybrid.py で聞いた答え(runs/hybrid/*-hybrid-below-ask と *-hybrid-ask)
- 行動: #169 のゲーム(Haiku 5.5、students、neutral、seed 1〜3)。同じ seed の人物像は、問いの system が一字一句同じ
照らし合わせるのは3つ。
1. 1回目: 語った見込みを、語った合わせ方の表に入れた量 と 実際の1回目の拠出
2. 合わせ方: 罰なしの条件で、前の回のほかの人の平均を表に入れた量 と 実際の次の回の拠出
3. 罰への反応: 罰ありの条件で、減点を受けた次の回に増やしたか減らしたか と 語った向き
あわせて、同じ問いを2回聞いた答え(-ask と -below-ask)が、どれだけ一致するかも見る(語りの再現性)。
"""
import argparse
import glob
import json
import os
from statistics import mean

HERE = os.path.dirname(os.path.abspath(__file__))
GAMES = {1: "20261111-100331|20261111-101131", 2: "20261111-103913", 3: "20261111-104801"}
XS = [0, 5, 10, 15, 20]


def interp(table, b):
    for k in range(len(XS) - 1):
        if b <= XS[k + 1]:
            t = (b - XS[k]) / (XS[k + 1] - XS[k])
            return table[k] + t * (table[k + 1] - table[k])
    return table[-1]


def corr(xs, ys):
    mx, my = mean(xs), mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    den = (sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys)) ** 0.5
    return round(num / den, 3) if den else None


def load_said(pattern):
    m = json.load(open(glob.glob(os.path.join(HERE, "runs", "hybrid", pattern, "manifest.json"))[0],
                       encoding="utf-8"))
    return {(int(s), q["id"]): q for s, qs in m["summary"]["params"].items() for q in qs}


def game_dirs(seed):
    out = []
    for stamp in GAMES[seed].split("|"):
        out += sorted(glob.glob(os.path.join(HERE, "runs", f"{stamp}-game-*")))
    return out


def histories(d):
    """人ごとに、回の順で (自分の拠出, ほかの人の平均, 受けた減点) を返す。"""
    m = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
    g = m["config"]["game"]
    cond = f"{g['matching']}/{'punish' if g['punishment'] else 'no_punish'}"
    h = {}
    for line in open(os.path.join(d, "events.jsonl"), encoding="utf-8"):
        e = json.loads(line)
        c, p = e["contribs"], e["points"]
        k = len(c)
        for pos, pid in enumerate(e["members"]):
            others = sum(c[q] for q in range(k) if q != pos) / (k - 1)
            recv = sum(p[q][pos] for q in range(k) if q != pos)
            h.setdefault(pid, {})[e["round"]] = (c[pos], others, recv)
    return cond, {pid: [v[r] for r in sorted(v)] for pid, v in h.items()}


def sign(x, eps=0.0):
    return "増" if x > eps else ("減" if x < -eps else "同")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "runs", "say-do-172.json"))
    a = ap.parse_args()
    said = load_said("*-hybrid-below-ask")
    said_even = load_said("*-hybrid-ask")
    first_pred, first_act = [], []
    cond_rows = []          # (人, 予測, 実際, 前の自分の拠出)
    pun = {}                # 人 -> 受けた次の回の増減のリスト / 受けなかった次の回の増減のリスト
    for seed in GAMES:
        for d in game_dirs(seed):
            cond, hist = histories(d)
            for pid, rows in hist.items():
                q = said[(seed, pid)]
                first_pred.append(interp(q["table"], q["belief0"]))
                first_act.append(rows[0][0])
                for r in range(len(rows) - 1):
                    mine, others, recv = rows[r]
                    nxt = rows[r + 1][0]
                    if cond.endswith("no_punish"):
                        cond_rows.append(((seed, pid), interp(q["table"], others), nxt, mine))
                    else:
                        slot = pun.setdefault((seed, pid), {"hit": [], "hit_below": [], "none": []})
                        if recv > 0:
                            slot["hit"].append(nxt - mine)
                            if mine < others:
                                slot["hit_below"].append(nxt - mine)
                        else:
                            slot["none"].append(nxt - mine)
    out = {}
    out["1_first_round"] = {
        "n": len(first_act), "pred_mean": round(mean(first_pred), 2), "act_mean": round(mean(first_act), 2),
        "mean_abs_err": round(mean(abs(p - x) for p, x in zip(first_pred, first_act)), 2),
        "corr": corr(first_pred, first_act)}
    pred = [p for _, p, _, _ in cond_rows]
    act = [x for _, _, x, _ in cond_rows]
    prev = [m for _, _, _, m in cond_rows]
    out["2_conditional"] = {
        "n": len(cond_rows), "pred_mean": round(mean(pred), 2), "act_mean": round(mean(act), 2),
        "bias_act_minus_pred": round(mean(x - p for p, x in zip(pred, act)), 2),
        "mean_abs_err_said_table": round(mean(abs(p - x) for p, x in zip(pred, act)), 2),
        "mean_abs_err_same_as_last": round(mean(abs(m - x) for m, x in zip(prev, act)), 2),
        "corr_said_table": corr(pred, act), "corr_same_as_last": corr(prev, act)}
    cross = {}
    rows3 = []
    for key, s in pun.items():
        if not s["hit"]:
            continue
        stated = sign(said[key]["deter"])
        actual = sign(mean(s["hit"]))
        cross[f"語り{stated}/行動{actual}"] = cross.get(f"語り{stated}/行動{actual}", 0) + 1
        rows3.append({"who": f"s{key[0]}/{key[1]}", "said_deter": said[key]["deter"],
                      "act_delta_hit": round(mean(s["hit"]), 2),
                      "act_delta_none": round(mean(s["none"]), 2) if s["none"] else None,
                      "n_hit": len(s["hit"])})
    hits = [x for s in pun.values() for x in s["hit"]]
    hits_below = [x for s in pun.values() for x in s["hit_below"]]
    nones = [x for s in pun.values() for x in s["none"]]
    out["3_punishment"] = {
        "people_punished": len(rows3), "cross": cross,
        "said_decrease_share": round(sum(r["said_deter"] < 0 for r in rows3) / len(rows3), 3),
        "act_mean_delta_after_hit": round(mean(hits), 2), "n_hit": len(hits),
        "act_mean_delta_after_hit_when_below": round(mean(hits_below), 2), "n_hit_below": len(hits_below),
        "act_mean_delta_no_hit": round(mean(nones), 2), "n_no_hit": len(nones),
        "corr_said_vs_act": corr([r["said_deter"] for r in rows3], [r["act_delta_hit"] for r in rows3]),
        "people": rows3}
    keys = [k for k in said if k in said_even and k[0] in GAMES]
    out["4_said_twice"] = {
        "n": len(keys),
        "belief0_same": round(sum(said[k]["belief0"] == said_even[k]["belief0"] for k in keys) / len(keys), 3),
        "table_mean_abs_diff": round(mean(abs(x - y) for k in keys
                                          for x, y in zip(said[k]["table"], said_even[k]["table"])), 2),
        "deter_sign_same": round(sum(sign(said[k]["deter"]) == sign(said_even[k]["deter"])
                                     for k in keys) / len(keys), 3)}
    text = json.dumps(out, ensure_ascii=False, indent=1)
    open(a.out, "w", encoding="utf-8").write(text)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "people"} for k, v in out.items()},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
