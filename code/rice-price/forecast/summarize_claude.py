"""Claude の予測(runs/<条件>/*.json)をまとめる(#184)。使い方: ../.venv/bin/python summarize_claude.py"""
import json
import statistics as st
from pathlib import Path

HERE = Path(__file__).parent
ACTUAL = (21293 + 21434) / 2  # 2026年9月・10月の全銘柄平均の平均(税込み)
NAMES = {"1a": "価格だけ・知識なし", "1b": "価格だけ・知識あり", "3a": "価格+需給・知識なし", "3b": "価格+需給・知識あり"}

for c, name in NAMES.items():
    fs = sorted((HERE / "runs" / c).glob("*.json"), key=lambda p: int(p.stem))
    a = [json.loads(f.read_text())["answer"] for f in fs]
    if not a:
        continue
    pts = [x["sep_oct_point"] for x in a]
    hit = sum(x["sep_oct_low80"] <= ACTUAL <= x["sep_oct_high80"] for x in a)
    cost = sum(json.loads(f.read_text())["cost_usd"] or 0 for f in fs)
    print(f"{c} {name}: n={len(a)} 点予測 {[round(p) for p in pts]} 中央値 {st.median(pts):.0f} "
          f"誤差 {st.median(pts) / ACTUAL * 100 - 100:+.1f}% 区間に入った {hit}/{len(a)} "
          f"区間の例 {a[0]['sep_oct_low80']:.0f}〜{a[0]['sep_oct_high80']:.0f} 費用 ${cost:.2f}")
    print("   2027年8月の予測:", [round(x["monthly"]["2027-08"]) for x in a])
