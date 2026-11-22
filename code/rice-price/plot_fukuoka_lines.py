"""福岡12品目: 実績と、2026年6月末の時点の予測(7〜9月)の折れ線(#184)。使い方: .venv/bin/python plot_fukuoka_lines.py"""
import json
import statistics as st
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import fukuoka_models as fm

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "2026/11-22-糸島の農業を社会学とAIで考える-09-米価を時系列データで予測する/assets/fukuoka-lines.png"
plt.rcParams["font.family"] = "Hiragino Sans"
S = fm.series().loc["2026-01-01":"2026-09-01"]
M = pd.read_csv(HERE / "forecast/fukuoka_models.csv").query("年 == 2026")
C = pd.read_csv(HERE / "forecast/fukuoka_claude.csv").query("モデル == 'Claude 知識なし'")
months = pd.date_range("2026-07-01", periods=3, freq="MS")
LINES = {"前の月のまま": ("#999999", ":"), "指数平滑法": ("#D55E00", "-."), "TimesFM(Google)": ("#8C6D31", "-.")}

fig, axes = plt.subplots(3, 4, figsize=(15, 9.5), dpi=140)
for ax, it in zip(axes.flat, fm.ITEMS):
    ax.plot(S.index, S[it], color="#222222", lw=2.6, marker="o", ms=4, label="実績", zorder=5)
    for k, (col, ls) in LINES.items():
        p = M[(M["品目"] == it) & (M["モデル"] == k)].sort_values("月")["予測"].values
        ax.plot([pd.Timestamp("2026-06-01")] + list(months), [S.loc["2026-06-01", it]] + list(p), color=col, lw=2, ls=ls, label=k)
    p = C[C["品目"] == it].sort_values("月")["予測"].values
    ax.plot([pd.Timestamp("2026-06-01")] + list(months), [S.loc["2026-06-01", it]] + list(p), color="#0072B2", lw=2.4, marker="o", ms=5, label="Claude(知識なし)")
    ax.axvspan(pd.Timestamp("2026-06-15"), pd.Timestamp("2026-09-15"), color="#f3f6fa", zorder=0)
    ax.axvline(pd.Timestamp("2026-06-15"), color="#bbbbbb", lw=1, ls=":")
    ax.set_title(it, loc="left", fontsize=11)
    ax.tick_params(labelsize=8)
    ax.set_xticks(pd.date_range("2026-01-01", "2026-09-01", freq="MS"))
    ax.set_xticklabels([f"{m}月" for m in range(1, 10)])
    ax.grid(axis="y", color="#eeeeee")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
fig.legend(*axes.flat[0].get_legend_handles_labels(), loc="upper left", ncol=5, fontsize=10, frameon=False, bbox_to_anchor=(0.005, 0.955))
fig.suptitle("福岡市中央卸売市場の野菜12品目:2026年の実績と、6月末の時点の予測(色のついた部分が7〜9月、円/kg)", x=0.01, ha="left", fontsize=13)
fig.text(0.01, 0.005, "出典: 農林水産省「青果物卸売市場調査」(2025年までは確報、2026年は日別調査を月ごとに平均)。予測の線は、6月の実績から引いた", fontsize=8, color="#666666")
fig.tight_layout(rect=(0, 0.02, 1, 0.92))
fig.savefig(OUT)
print(OUT)
