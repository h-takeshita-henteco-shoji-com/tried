"""Claude の福岡12品目の予測を採点し、fukuoka_models.csv に Claude の行を足した表を作る(#184)。"""
import json
import statistics as st
from pathlib import Path

import pandas as pd

import run_claude_fukuoka as f

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data/fukuoka_daily_monthly.csv")
rows = []
for cond, name in (("a", "Claude 知識なし"), ("b", "Claude 知識あり")):
    A = [json.loads(p.read_text())["answer"] for p in (HERE / f"runs/fukuoka_{cond}").glob("*.json")]
    for it in f.ITEMS:
        for m in (7, 8, 9):
            pred = st.median(a[f"{f.CODE[it]}_2026-0{m}"] for a in A)
            act = d[(d["品目"] == it) & (d["月"] == m)]["価格"].iloc[0]
            rows.append({"年": 2026, "月": m, "モデル": name, "予測": pred, "実績": act, "品目": it, "誤差%": (pred / act - 1) * 100})
pd.DataFrame(rows).round(1).to_csv(HERE / "fukuoka_claude.csv", index=False)
print("Claude の費用:", round(sum(json.loads(p.read_text())["cost_usd"] for c in "ab" for p in (HERE / f"runs/fukuoka_{c}").glob("*.json")), 2))
