"""全体の推移の中に、直近の予測部分を拡大した小窓を入れたグラフ(#184)。

使い方: .venv/bin/python plot_inset.py
出力: assets/veg-forecast.png(東京2品目)、assets/fukuoka-lines.png(福岡12品目)、assets/forecast-vs-actual.png(米)
"""
import json
import statistics as st
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import fukuoka_models as fm

HERE = Path(__file__).parent
ASSETS = HERE.parent.parent / "2026/11-22-糸島の農業を社会学とAIで考える-09-米価を時系列データで予測する/assets"
plt.rcParams["font.family"] = "Hiragino Sans"
M7 = pd.date_range("2026-07-01", periods=3, freq="MS")
JUN = pd.Timestamp("2026-06-01")


def style(ax, fs=8):
    ax.grid(axis="y", color="#eeeeee")
    ax.tick_params(labelsize=fs)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def draw(ax, actual, preds, start, lw=1.0, ms=0):
    """actual: Series、preds: {名前: (月の並び, 値の並び, 色, 線種, 太さ)}。start は予測の線の起点の月。"""
    ax.plot(actual.index, actual.values, color="#222222", lw=2.2 * lw, marker="o" if ms else None, ms=ms, label="実績", zorder=5)
    for k, (xs, ys, col, ls, w) in preds.items():
        ax.plot([start] + list(xs), [actual.loc[start]] + list(ys), color=col, ls=ls, lw=w * lw,
                marker="o" if (ms and k.startswith("Claude")) else None, ms=ms, label=k)


def inset(ax, actual, preds, start, x0, x1, bounds, ticks, fmt):
    win = actual.loc[x0:x1]
    ins = ax.inset_axes(bounds)
    ins.set_facecolor("#f7f9fc")
    draw(ins, win, preds, start, lw=1.15, ms=3.5)
    vals = list(win.values) + [v for _, ys, *_ in preds.values() for v in ys]
    pad = (max(vals) - min(vals)) * 0.08
    ins.set_ylim(min(vals) - pad, max(vals) + pad)
    ins.set_xlim(pd.Timestamp(x0) - pd.Timedelta(days=12), pd.Timestamp(x1) + pd.Timedelta(days=12))
    ins.set_xticks(ticks)
    ins.set_xticklabels([fmt(t) for t in ticks])
    style(ins, 7)
    ins.yaxis.tick_right()
    for s in ins.spines.values():
        s.set_visible(True)
        s.set_color("#888888")
    ax.indicate_inset_zoom(ins, edgecolor="#888888", alpha=0.8)
    return ins


def veg_tokyo():
    V = pd.read_csv(HERE / "data/veg_monthly.csv", index_col=0, parse_dates=True).loc["2023-01":"2026-09"]
    M = pd.read_csv(HERE / "forecast/veg_models.csv").query("年 == 2026")
    A = [json.loads(f.read_text())["answer"] for f in (HERE / "forecast/runs/veg_c").glob("*.json")]
    COL = {"前の月のまま": ("#999999", ":", 1.6), "SARIMA": ("#CC79A7", "-.", 1.4), "指数平滑法": ("#D55E00", "-.", 1.4),
           "Prophet(Meta)": ("#E69F00", "-.", 1.4), "TimesFM(Google)": ("#8C6D31", "-.", 1.4), "Chronos(Amazon)": ("#7F7F7F", "-.", 1.4)}
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=150)
    for ax, (it, title, bounds) in zip(axes, [("cabbage", "キャベツ", [0.02, 0.56, 0.62, 0.42]),
                                              ("onion", "たまねぎ", [0.02, 0.56, 0.62, 0.42])]):
        s = V[f"{it}_price"]
        preds = {k: (M7, M[(M["品目"] == it) & (M["モデル"] == k)].sort_values("月")["予測"].values, *v) for k, v in COL.items()}
        preds["Claude(値段だけ・知識なし)"] = (M7, [st.median(a[f"{it}_{m:%Y-%m}"] for a in A) for m in M7], "#0072B2", "-", 2.2)
        draw(ax, s, preds, JUN)
        ax.set_title(f"{title}(東京都中央卸売市場)", loc="left", fontsize=12)
        ax.set_ylabel("円/kg(税込み)")
        style(ax, 9)
        lo, hi = s.min(), s.max()
        ax.set_ylim(lo - (hi - lo) * 0.05, hi + (hi - lo) * 0.8)  # 上に小窓の場所を空ける
        inset(ax, s, preds, JUN, "2026-04-01", "2026-09-01", bounds, pd.date_range("2026-04-01", "2026-09-01", freq="MS"),
              lambda t: f"{t.month}月")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper left", ncol=8, fontsize=9, frameon=False, bbox_to_anchor=(0.005, 0.95))
    fig.suptitle("野菜の卸売価格:実績と、2026年6月末の時点の7〜9月の予測(小窓は4〜9月を拡大)", x=0.01, ha="left", fontsize=13)
    fig.text(0.01, 0.01, "出典: 東京都中央卸売市場「市場統計情報明細データ」(全市場の合計、金額÷数量)。予測の線は6月の実績から引いた", fontsize=7.5, color="#666666")
    fig.tight_layout(rect=(0, 0.03, 1, 0.91))
    fig.savefig(ASSETS / "veg-forecast.png")


def veg_fukuoka():
    S = fm.series().loc["2024-01-01":"2026-09-01"]
    M = pd.read_csv(HERE / "forecast/fukuoka_models.csv").query("年 == 2026")
    C = pd.read_csv(HERE / "forecast/fukuoka_claude.csv").query("モデル == 'Claude 知識なし'")
    COL = {"前の月のまま": ("#999999", ":", 1.6), "指数平滑法": ("#D55E00", "-.", 1.5), "TimesFM(Google)": ("#8C6D31", "-.", 1.5)}
    fig, axes = plt.subplots(3, 4, figsize=(17, 11), dpi=130)
    for ax, it in zip(axes.flat, fm.ITEMS):
        s = S[it]
        preds = {k: (M7, M[(M["品目"] == it) & (M["モデル"] == k)].sort_values("月")["予測"].values, *v) for k, v in COL.items()}
        preds["Claude(知識なし)"] = (M7, C[C["品目"] == it].sort_values("月")["予測"].values, "#0072B2", "-", 2.0)
        draw(ax, s, preds, JUN, lw=0.8)
        ax.set_title(it, loc="left", fontsize=12)
        ax.set_xticks(pd.to_datetime(["2024-01-01", "2025-01-01", "2026-01-01"]))
        ax.set_xticklabels(["2024", "2025", "2026"])
        style(ax, 8)
        lo, hi = s.min(), s.max()
        ax.set_ylim(lo - (hi - lo) * 0.05, hi + (hi - lo) * 0.75)  # 上に小窓の場所を空ける
        inset(ax, s, preds, JUN, "2026-05-01", "2026-09-01", [0.02, 0.58, 0.60, 0.40],
              pd.date_range("2026-05-01", "2026-09-01", freq="MS"), lambda t: f"{t.month}")
    h, l = axes.flat[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper left", ncol=5, fontsize=10, frameon=False, bbox_to_anchor=(0.005, 0.955))
    fig.suptitle("福岡市中央卸売市場の野菜12品目:実績と、2026年6月末の時点の7〜9月の予測(円/kg。小窓は2026年5〜9月を拡大)",
                 x=0.01, ha="left", fontsize=13)
    fig.text(0.01, 0.005, "出典: 農林水産省「青果物卸売市場調査」(2025年までは確報、2026年は日別調査を月ごとに平均)。予測の線は6月の実績から引いた", fontsize=8, color="#666666")
    fig.tight_layout(rect=(0, 0.02, 1, 0.93))
    fig.savefig(ASSETS / "fukuoka-lines.png")


if __name__ == "__main__":
    veg_tokyo()
    veg_fukuoka()
    print("ok")
