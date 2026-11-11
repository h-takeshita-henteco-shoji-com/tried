"""seed や言い回しを変えた複数の記録で、物差し1〜5の判定が毎回そろうかを数える。

使い方: python robustness.py runs/<日時>-game-* [--out runs/robustness.json]
同じ seed・言い回しの4条件(partner/stranger × 罰あり/なし)を1組として判定する。
"""
import argparse
import json
from collections import defaultdict
from statistics import mean

from compare import analyze, load

BELOW = ["[-20,-14)", "[-14,-8)", "[-8,-2)"]
ABOVE = ["(2,8]", "(8,14]", "(14,20]"]


def pooled(pbd, bins):
    pts = [(v["mean"], v["n"]) for b, v in pbd.items() if b in bins and v["n"]]
    n = sum(k for _, k in pts)
    return (round(sum(m * k for m, k in pts) / n, 2) if n else None), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--out")
    a = ap.parse_args()
    sets = defaultdict(dict)
    cost = 0
    for d in a.runs:
        cond, m, ev = load(d)
        c = m["config"]
        label = f"{c.get('personas', 'students')}/seed{c['seed']}/{c['variant']}"
        r = analyze(m, ev)
        r["max"] = max(x for e in ev for x in e["contribs"])
        r["min"] = min(x for e in ev for x in e["contribs"])
        sets[label][cond] = r
        cost += r["cost_usd"] or 0
    rows = {}
    for label, s in sorted(sets.items()):
        row = {}
        row["1_first_share"] = [s[k]["first_share"] for k in sorted(s)]
        row["1_ok"] = all(0.4 <= x <= 0.6 for x in row["1_first_share"])
        row["2_sd_all"] = [s[k]["sd_all"] for k in sorted(s)]
        row["2_range"] = [(s[k]["min"], s[k]["max"]) for k in sorted(s)]
        row["2_ok"] = all(s[k]["min"] == 0 and s[k]["max"] == 20 and s[k]["sd_all"] > 3 for k in s)
        row["3_final_over_first"] = {m: s[f"{m}/no_punish"]["final_over_first"] for m in ("partner", "stranger")}
        row["3_ok"] = all(v <= 0.5 for v in row["3_final_over_first"].values())
        row["4_final"] = {m: (s[f"{m}/punish"]["mean_final"], s[f"{m}/no_punish"]["mean_final"])
                          for m in ("partner", "stranger")}
        row["4_ok"] = all(p - n >= 3 for p, n in row["4_final"].values())
        row["4b_partner_minus_stranger_punish_all"] = round(
            s["partner/punish"]["mean_all"] - s["stranger/punish"]["mean_all"], 2)
        row["5"] = {}
        ok5 = True
        for m in ("partner", "stranger"):
            pbd = s[f"{m}/punish"]["punish_by_deviation"]
            below, nb = pooled(pbd, BELOW)
            above, na = pooled(pbd, ABOVE)
            row["5"][m] = {"below": below, "n_below": nb, "above": above, "n_above": na}
            ok5 &= below is not None and (above is None or below > above)
        row["5_ok"] = ok5
        rows[label] = row
    out = {"cost_usd": round(cost, 4), "sets": rows,
           "ok_count": {k: sum(r[k] for r in rows.values()) for k in ("1_ok", "2_ok", "3_ok", "4_ok", "5_ok")},
           "n_sets": len(rows)}
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
