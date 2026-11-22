"""福岡12品目: モデルごとの誤差(#184)。使い方: .venv/bin/python plot_fukuoka.py"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "2026/11-22-糸島の農業を社会学とAIで考える-09-米価を時系列データで予測する/assets/fukuoka-errors.png"
plt.rcParams["font.family"] = "Hiragino Sans"
r = pd.concat([pd.read_csv(HERE / "forecast/fukuoka_models.csv"), pd.read_csv(HERE / "forecast/fukuoka_claude.csv")])
r["a"] = r["誤差%"].abs()
past = r[r["年"] < 2026].groupby("モデル")["a"].mean()
now = r[r["年"] == 2026].groupby("モデル")["a"].mean()
order = now.sort_values(ascending=False).index
fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
y = range(len(order))
ax.hlines(y, [min(past.get(m, now[m]), now[m]) for m in order], [max(past.get(m, now[m]), now[m]) for m in order], color="#dddddd", lw=2)
ax.plot([past.get(m) for m in order], y, "o", color="#999999", ms=8, label="過去10年(2016〜2025年)の平均")
ax.plot([now[m] for m in order], y, "o", color="#0072B2", ms=9, label="2026年7〜9月(Claude も知らない期間)")
for i, m in enumerate(order):
    ax.text(now[m] + 0.3, i + 0.18, f"{now[m]:.1f}%", fontsize=8, color="#0072B2")
ax.set_yticks(list(y), order)
ax.set_xlabel("誤差の絶対値の平均(%、12品目×3か月)")
ax.set_xlim(10, 26)
ax.grid(axis="x", color="#eeeeee")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc="upper right")
ax.set_title("福岡市中央卸売市場の野菜12品目:6月までの価格で7〜9月を当てた誤差", loc="left", fontsize=12)
fig.text(0.01, 0.01, "出典: 農林水産省「青果物卸売市場調査」(確報・日別調査)。Claude は過去10年の試験をしていない(答えを知っているため)", fontsize=7.5, color="#666666")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(OUT)
print(OUT)
