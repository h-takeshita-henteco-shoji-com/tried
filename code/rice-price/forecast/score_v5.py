"""#186 V5 の採点。fukuoka_a(#184 知識なし)と同じ方法で比べる。"""
import json, statistics as st
from pathlib import Path
import numpy as np, pandas as pd
import run_claude_fukuoka as f
HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data/fukuoka_daily_monthly.csv"); d['品目'] = d['品目'].str.strip()
rows = []
import sys
CONDS = sys.argv[1:] or ["fukuoka_a", "v5"]
for cond in CONDS:
    A = [json.loads(p.read_text())["answer"] for p in sorted((HERE / "runs" / cond).glob("*.json"))]
    for it in f.ITEMS:
        for m in (7, 8, 9):
            pred = st.median(a[f"{f.CODE[it]}_2026-0{m}"] for a in A)
            act = d[(d["品目"] == it) & (d["月"] == m)]["価格"].iloc[0]
            rows.append({"条件": cond, "品目": it, "月": m, "予測": pred, "実績": act, "誤差%": (pred / act - 1) * 100})
r = pd.DataFrame(rows); r["絶対"] = r["誤差%"].abs()
r.round(1).to_csv(HERE / ("v5_scores.csv" if CONDS == ["fukuoka_a", "v5"] else "v7_scores.csv"), index=False)
print(r.groupby("条件")["絶対"].mean().round(2))
w = r.pivot_table(index=["品目", "月"], columns="条件", values="絶対")
rng = np.random.default_rng(0)
for x, ref in (("v5", "fukuoka_a"), ("v7", "v5"), ("v7n", "fukuoka_a")):
    if x not in w or ref not in w: continue
    diff = (w[x] - w[ref]).values; bs = [rng.choice(diff, len(diff)).mean() for _ in range(5000)]
    print(f"差({x}-{ref})", diff.mean().round(2), "95%", np.percentile(bs, [2.5, 97.5]).round(2), "良くなった箇所", (diff < 0).sum(), "/", len(diff))
for c in CONDS:
    E = []
    for p in sorted((HERE / "runs" / c).glob("*.json")):
        a = json.loads(p.read_text())["answer"]
        E.append(round(np.mean([abs(a[f"{f.CODE[it]}_2026-0{m}"] / d[(d["品目"] == it) & (d["月"] == m)]["価格"].iloc[0] - 1) * 100 for it in f.ITEMS for m in (7, 8, 9)]), 1))
    print("1回ごと", c, E)
print(r.pivot_table(index="品目", columns="条件", values="絶対").round(1))
print("偏り(平均誤差%)", r.groupby("条件")["誤差%"].mean().round(2).to_dict())
for c in CONDS[1:]: print("費用", c, round(sum(json.loads(p.read_text())["cost_usd"] for p in (HERE / "runs" / c).glob("*.json")), 2))
