"""性格を足した回を、回ごとの平均・多く入れて減点も付ける人・性格ごとの振る舞いで比べる(#172, #175)。AIは呼ばない。

使い方: python analyze_traits.py <名前>=<runs のパターン> [<名前>=<パターン> ...]
例:     python analyze_traits.py base='runs/rho/*-partner-p-dist-rho0.7' recip='runs/c175/*'
- パターンはカンマで区切って複数書ける。当てはまる記録のうち、Haiku の回だけを使う(Sonnet の回は除く)
- 多く入れる人: 10回の平均が14以上。多く入れて減点も付ける人: そのうち、自分より少ない人に合わせて10点以上の減点を付けた人
- 組の効果: 毎回同じ相手の組で、多く入れて減点も付ける人の人数ごとに、6〜9回目の平均を出す
"""
import glob
import json
import os
import sys
from statistics import mean

HIGH, PUNISH = 14, 10


def runs(pattern):
    out = []
    for d in sorted(x for pat in pattern.split(",") for x in glob.glob(pat)):
        m = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
        if "haiku" in m["llm"]:
            out.append((d, m))
    return out


def analyze(items):
    by_round, people, groups, traits = [], [], [], {}
    for d, m in items:
        trait = {p["id"]: p.get("trait", "") for p in m["people"]}
        ev = [json.loads(line) for line in open(os.path.join(d, "events.jsonl"), encoding="utf-8")]
        rounds = {}
        P = {}
        G = {}
        for e in ev:
            c, pts = e["contribs"], e["points"]
            rounds.setdefault(e["round"], []).extend(c)
            G.setdefault(e["group"], {})[e["round"]] = (e["members"], mean(c))
            for i, pid in enumerate(e["members"]):
                s = P.setdefault(pid, {"c": [], "low": 0, "other": 0})
                s["c"].append(c[i])
                for j in range(len(c)):
                    if j != i:
                        s["low" if c[j] < c[i] else "other"] += pts[i][j]
        by_round.append([mean(rounds[r]) for r in sorted(rounds)])
        for pid, s in P.items():
            row = (mean(s["c"]), s["low"], s["other"])
            people.append(row)
            traits.setdefault(trait[pid], []).append(row)
        for g, rr in G.items():
            mem = rr[1][0]
            n = sum(1 for pid in mem if mean(P[pid]["c"]) >= HIGH and P[pid]["low"] >= PUNISH)
            groups.append((n, mean(rr[r][1] for r in (6, 7, 8, 9))))
    return by_round, people, groups, traits


def main(args):
    for spec in args:
        name, _, pattern = spec.partition("=")
        items = runs(pattern)
        br, people, groups, traits = analyze(items)
        avg = [round(mean(x[i] for x in br), 1) for i in range(10)]
        hi = [r for r in people if r[0] >= HIGH]
        hp = [r for r in hi if r[1] >= PUNISH]
        print(f"== {name}  記録{len(items)}本  人数{len(people)}")
        print(f"  回ごとの平均 {avg}")
        print(f"  多く入れる人 {len(hi)}  多く入れて減点も付ける人 {len(hp)}  1人あたりの減点 "
              f"{mean(r[1] + r[2] for r in people):.1f}  多い人への減点が15点以上の人 {sum(r[2] >= 15 for r in people)}")
        for k in (0, 1, 2):
            gs = [v for n, v in groups if (n >= 2 if k == 2 else n == k)]
            if gs:
                print(f"  組の中の人数 {k}{'人以上' if k == 2 else '人'}: {len(gs)}組 6〜9回目 {mean(gs):.1f}")
        for t, rows in sorted(traits.items(), key=lambda kv: -mean(r[1] for r in kv[1])):
            print(f"    {t:24s} {len(rows):3d}人 入れた量 {mean(r[0] for r in rows):5.1f}  "
                  f"少ない人へ {mean(r[1] for r in rows):5.1f}  多い人へ {mean(r[2] for r in rows):5.1f}")


if __name__ == "__main__":
    main(sys.argv[1:])
