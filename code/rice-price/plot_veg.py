"""野菜の実績と、2026年6月末の時点の予測(#184)。使い方: .venv/bin/python plot_veg.py"""
import json
import statistics as st
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "2026/11-22-糸島の農業を社会学とAIで考える-09-米価を時系列データで予測する/assets/veg-forecast.png"
plt.rcParams["font.family"] = "Hiragino Sans"
V = pd.read_csv(HERE / "data/veg_monthly.csv", index_col=0, parse_dates=True).loc["2026-01":"2026-09"]
M = pd.read_csv(HERE / "forecast/veg_models.csv").query("年 == 2026")
months = pd.date_range("2026-07-01", periods=3, freq="MS")
A = [json.loads(f.read_text())["answer"] for f in (HERE / "forecast/runs/veg_c").glob("*.json")]
COL = {"前の月のまま": "#999999", "SARIMA": "#CC79A7", "指数平滑法": "#D55E00", "Prophet(Meta)": "#E69F00",
       "TimesFM(Google)": "#8C6D31", "Chronos(Amazon)": "#7F7F7F"}

fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=150, sharey=False)
for ax, (it, title) in zip(axes, [("cabbage", "キャベツ"), ("onion", "たまねぎ")]):
    ax.plot(V.index, V[f"{it}_price"], color="#222222", lw=2.8, marker="o", ms=5, label="実績", zorder=5)
    j = V.loc["2026-06-01", f"{it}_price"]
    for k, col in COL.items():
        p = M[(M["品目"] == it) & (M["モデル"] == k)].sort_values("月")["予測"].values
        ax.plot([pd.Timestamp("2026-06-01")] + list(months), [j] + list(p), color=col, lw=1.8, ls="-.", label=k)
    ax.plot([pd.Timestamp("2026-06-01")] + list(months), [j] + [st.median(a[f"{it}_{m:%Y-%m}"] for a in A) for m in months], color="#0072B2", lw=2.6,
            marker="o", ms=5, label="Claude(値段だけ・知識なし、3回の中央値)")
    ax.axvspan(pd.Timestamp("2026-06-15"), pd.Timestamp("2026-09-15"), color="#f3f6fa", zorder=0)
    ax.axvline(pd.Timestamp("2026-06-15"), color="#999999", lw=1, ls=":")
    ax.set_title(f"{title}(東京都中央卸売市場)", loc="left", fontsize=12)
    ax.set_ylabel("円/kg(税込み)")
    ax.set_xticks(pd.date_range("2026-01-01", "2026-09-01", freq="MS"))
    ax.set_xticklabels([f"{m}月" for m in range(1, 10)])
    ax.grid(axis="y", color="#e5e5e5", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
axes[1].legend(fontsize=8.5, frameon=False, loc="upper right")
fig.suptitle("野菜の卸売価格:2026年の実績と、6月末の時点の予測(色のついた部分が7〜9月)", x=0.01, ha="left", fontsize=13)
fig.text(0.01, 0.01, "出典: 東京都中央卸売市場「市場統計情報明細データ」(全市場の合計、金額÷数量)。予測の線は、6月の実績から引いた", fontsize=7.5, color="#666666")
fig.tight_layout(rect=(0, 0.03, 1, 0.95))
fig.savefig(OUT)
print(OUT)
