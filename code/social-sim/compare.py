"""再現の結果を、Fehr & Gächter(2000)の値と物差しごとに並べる。

使い方: python compare.py runs/<日時>-game-partner-n runs/<日時>-game-partner-p ... [--out compare.json]
条件名(partner/no_punish など)は、各記録の manifest から読む。
"""
import argparse
import json
import os
from statistics import mean, pstdev

HERE = os.path.dirname(os.path.abspath(__file__))
BINS = [(-20, -14, "[-20,-14)"), (-14, -8, "[-14,-8)"), (-8, -2, "[-8,-2)"), (-2, 2.0001, "[-2,2]"),
        (2.0001, 8.0001, "(2,8]"), (8.0001, 14.0001, "(8,14]"), (14.0001, 20.0001, "(14,20]")]


def load(run_dir):
    m = json.load(open(os.path.join(run_dir, "manifest.json"), encoding="utf-8"))
    ev = [json.loads(line) for line in open(os.path.join(run_dir, "events.jsonl"), encoding="utf-8")]
    g = m["config"]["game"]
    cond = f"{g.get('matching', 'partner')}/{'punish' if g['punishment'] else 'no_punish'}"
    return cond, m, ev


def bin_of(d):
    for lo, hi, name in BINS:
        if lo <= d < hi:
            return name
    raise ValueError(d)


def analyze(m, ev):
    rounds = sorted({e["round"] for e in ev})
    by_round = {r: [c for e in ev if e["round"] == r for c in e["contribs"]] for r in rounds}
    first, last = by_round[rounds[0]], by_round[rounds[-1]]
    allc = [c for v in by_round.values() for c in v]
    end = m["config"]["game"]["endowment"]
    out = {
        "n_people": len(first),
        "by_round": [round(mean(by_round[r]), 2) for r in rounds],
        "first_mean": round(mean(first), 2),
        "first_share": round(mean(first) / end, 3),
        "first_sd": round(pstdev(first), 2),
        "first_zero": round(sum(c == 0 for c in first) / len(first), 3),
        "first_full": round(sum(c == end for c in first) / len(first), 3),
        "mean_all": round(mean(allc), 2),
        "sd_all": round(pstdev(allc), 2),
        "mean_final": round(mean(last), 2),
        "final_zero": round(sum(c == 0 for c in last) / len(last), 3),
        "final_full": round(sum(c == end for c in last) / len(last), 3),
        "final_over_first": round(mean(last) / mean(first), 2) if mean(first) else None,
        "cost_usd": m.get("cost_usd"),
        "calls": m.get("calls"),
    }
    if m["config"]["game"]["punishment"]:
        recv = {name: [] for _, _, name in BINS}
        for e in ev:
            c, p = e["contribs"], e["points"]
            k = len(c)
            for j in range(k):
                others = mean(c[q] for q in range(k) if q != j)
                recv[bin_of(c[j] - others)].append(sum(p[i][j] for i in range(k) if i != j))
        out["punish_by_deviation"] = {b: {"mean": round(mean(v), 2) if v else None, "n": len(v)}
                                      for b, v in recv.items()}
        given = [sum(row) for e in ev for row in e["points"]]
        out["punish_any_share"] = round(sum(g > 0 for g in given) / len(given), 3)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    ref = json.load(open(os.path.join(HERE, "reference", "fg2000.json"), encoding="utf-8"))
    result = {"reference": "reference/fg2000.json", "runs": {}, "ai": {}}
    for d in a.runs:
        cond, m, ev = load(d)
        result["runs"][cond] = os.path.relpath(d, HERE)
        result["ai"][cond] = analyze(m, ev)
    result["human"] = {c: {"by_round": ref["by_period"][c]["values"], **ref["tables"][c]}
                       for c in result["ai"]}
    result["human_punish_by_deviation"] = ref["punishment_by_deviation"]
    text = json.dumps(result, ensure_ascii=False, indent=1)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
