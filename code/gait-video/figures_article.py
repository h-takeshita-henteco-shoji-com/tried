"""note 記事用の図(介護事業の関係者向け)。"""
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
plt.rcParams.update({"font.family": "Hiragino Sans", "font.size": 12,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8a8984",
                     "xtick.color": "#52514e", "ytick.color": "#52514e"})
BLUE, ORANGE, GRAY, GRID, INK, INK2 = ("#2a78d6", "#eb6834", "#b9b8b2",
                                       "#e6e5e0", "#0b0b0b", "#52514e")
r = pd.read_csv(ROOT / "results.csv", dtype={"pid": str})
r["pid"] = r.pid.str.zfill(2)
b = r[r.cam == "bottom"].sort_values("speed_xsens").reset_index(drop=True)

# 図1 一人ずつ: センサーと動画
fig, ax = plt.subplots(figsize=(7.2, 6))
ax.axvspan(0.3, 1.0, color="#fbf1ec", zorder=0)
ax.axvline(1.0, color=ORANGE, lw=1.5, ls="--", zorder=1)
ax.text(0.65, 9, "秒速1.0m未満\nサルコペニア・フレイルを\n疑う目安",
        ha="center", va="center", color=INK2, fontsize=11)
for i, row in b.iterrows():
    ax.plot([row.speed_xsens, row.speed_assume], [i, i], color=GRAY, lw=2,
            zorder=2)
    ax.scatter(row.speed_xsens, i, s=90, color=INK2, zorder=3,
               edgecolor="white", lw=2, label="センサー(正解)" if i == 0 else None)
    ax.scatter(row.speed_assume, i, s=90, color=BLUE, zorder=4,
               edgecolor="white", lw=2, label="スマホの動画" if i == 0 else None)
ax.set_yticks(range(len(b)))
ax.set_yticklabels([f"{chr(65 + i)}さん" for i in range(len(b))])
ax.set_xlim(0.3, 1.3)
ax.set_xlabel("歩く速さ(m/秒)")
ax.grid(axis="x", color=GRID)
ax.set_title("11人の歩く速さ:センサーとスマホの動画", loc="left", fontsize=14,
             pad=34)
ax.legend(frameon=False, ncol=2, loc="lower left", bbox_to_anchor=(0, 1.0),
          fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "1-一人ずつの速さ.png", dpi=200)

# 図4 撮り方と本数で、誤差が変わる
fig, axs = plt.subplots(1, 2, figsize=(9, 4.6))
ax = axs[0]
labels = ["目の高さ", "天井近く\n(見下ろす)"]
vals = [r[r.cam == "bottom"].eval("abs(speed_assume-speed_xsens)/speed_xsens").mean() * 100,
        r[r.cam == "top"].eval("abs(speed_assume-speed_xsens)/speed_xsens").mean() * 100]
bars = ax.bar(labels, vals, color=[BLUE, GRAY], width=0.55)
for bb, v in zip(bars, vals):
    ax.text(bb.get_x() + bb.get_width() / 2, v + 0.3, f"{v:.0f}%",
            ha="center", color=INK, fontsize=13)
ax.set_ylim(0, 15)
ax.set_ylabel("誤差の平均(%)")
ax.set_title("カメラの高さ", loc="left", fontsize=13)
ax.grid(axis="y", color=GRID)
ax.set_axisbelow(True)

ax = axs[1]
pp = pd.read_csv(ROOT / "per_pass.csv", dtype={"pid": str})
one = pp[(pp.cam == "bottom") & (pp.i == 0)].speed_err.abs().mean()
many = b.eval("abs(speed_assume-speed_xsens)").mean()
bars = ax.bar(["片道1本", "往復を数本"], [one, many], color=[GRAY, BLUE],
              width=0.55)
for bb, v in zip(bars, [one, many]):
    ax.text(bb.get_x() + bb.get_width() / 2, v - 0.012, f"秒速\n{v:.2f}m",
            ha="center", va="top", color="white", fontsize=12)
ax.axhline(0.1, color=ORANGE, lw=1.5, ls="--")
ax.text(1.45, 0.103, "意味のある変化\n(秒速0.1m)", ha="right", va="bottom",
        color=INK2, fontsize=10)
ax.set_ylim(0, 0.14)
ax.set_ylabel("誤差の平均(m/秒)")
ax.set_title("撮る本数(目の高さのカメラ)", loc="left", fontsize=13)
ax.grid(axis="y", color=GRID)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(OUT / "4-撮り方と誤差.png", dpi=200)
print("one", one, "many", many, vals)
