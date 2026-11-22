"""品目ごとに、左に折れ線、右に実績と予測の対比表を並べた図(#184)。

使い方: .venv/bin/python plot_combo.py
出力: assets/combo-tokyo-<品目>.png、assets/combo-fukuoka-<品目>.png
"""
import json
import statistics as st
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import fukuoka_models as fm
from plot_tables import CODE, ORDER, diff_text

HERE = Path(__file__).parent
ASSETS = HERE.parent.parent / "2026/11-22-糸島の農業を社会学とAIで考える-09-米価を時系列データで予測する/assets"
plt.rcParams["font.family"] = "Hiragino Sans"
RED, BLUE = "#C0392B", "#1F5FAD"
COLORS = {"前の月のまま": ("#999999", ":"), "前の年の同じ月": ("#BBBBBB", "--"), "指数平滑法": ("#D55E00", "-."),
          "SARIMA": ("#CC79A7", "-."), "Prophet(Meta)": ("#E69F00", "-."), "TimesFM(Google)": ("#8C6D31", "-."),
          "Chronos(Amazon)": ("#009E73", "-."), "Claude": ("#0072B2", "-.")}
MONTHS = pd.date_range("2026-07-01", periods=3, freq="MS")


def combo(name, market, series, preds, out, note):
    """series: 月ごとの実績(2026年9月まで)、preds: {方法: [7,8,9月の予測]}。"""
    actual = [series.loc[m] for m in MONTHS]
    fig = plt.figure(figsize=(15, 5.6), dpi=140)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.08)
    ax = fig.add_subplot(gs[0])
    s = series.loc["2025-07-01":"2026-09-01"]
    ax.axvspan(pd.Timestamp("2026-06-15"), pd.Timestamp("2026-09-15"), color="#f3f6fa", zorder=0)
    jun = series.loc["2026-06-01"]
    for k, vs in preds.items():
        col, ls = COLORS["Claude" if k.startswith("Claude") else k]
        ax.plot([pd.Timestamp("2026-06-01")] + list(MONTHS), [jun] + list(vs), color=col, ls=ls, lw=1.6, label=k)
    ax.plot(s.index, s.values, color="#222222", lw=2.6, marker="o", ms=4, label="実績", zorder=5)
    ax.set_xticks(pd.date_range("2025-07-01", "2026-09-01", freq="2MS"))
    ax.set_xticklabels([f"{t.year % 100}/{t.month}" for t in pd.date_range("2025-07-01", "2026-09-01", freq="2MS")], fontsize=8)
    ax.set_ylabel("円/kg(税込み)", fontsize=9)
    ax.tick_params(labelsize=8)
    ax.grid(axis="y", color="#eeeeee")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left", ncol=2)
    ax.text(pd.Timestamp("2026-07-28"), ax.get_ylim()[0], "予測した期間", ha="center", va="bottom", fontsize=8, color="#666666")

    tx = fig.add_subplot(gs[1])
    tx.axis("off")
    cols = [""] + [h for mo in (7, 8, 9) for h in (f"{mo}月", "差")]
    rows = [["実績"] + [x for v in actual for x in (f"{v:.0f}", "")]]
    signs = [[0] * 7]
    for k, vs in preds.items():
        rows.append([k] + [x for v, a in zip(vs, actual) for x in (f"{v:.0f}", diff_text(v - a))])
        signs.append([0] + [x for v, a in zip(vs, actual) for x in (0, (round(v - a) > 0) - (round(v - a) < 0))])
    err = {k: sum(abs(v / a - 1) for v, a in zip(vs, actual)) / 3 for k, vs in preds.items()}
    best = min(err, key=err.get)
    t = tx.table(cellText=rows, colLabels=cols, cellLoc="right", colLoc="center",
                 colWidths=[0.31] + [0.115] * 6, bbox=[0, 0.02, 1, 0.96])
    t.auto_set_font_size(False)
    t.set_fontsize(9.5)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#dddddd")
        cell.set_linewidth(0.6)
        if r == 0:
            cell.set_facecolor("#f0f0f0")
        if r == 1:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#f7f7f7")
        if c == 0 and r > 0:
            cell.get_text().set_ha("left")
            cell.PAD = 0.04
        if r > 1 and rows[r - 1][0] == best:
            cell.set_facecolor("#FFF3B0")
            if c == 0:
                cell.set_text_props(weight="bold")
        if r > 0 and c > 0 and c % 2 == 0:
            sg = signs[r - 1][c]
            cell.get_text().set_color(BLUE if sg > 0 else RED if sg < 0 else "#444444")
            cell.set_fontsize(8.5)
    fig.suptitle(f"{name}({market}):2026年7〜9月の実績と、6月末の時点の予測(円/kg)", x=0.01, ha="left", fontsize=13)
    fig.text(0.01, 0.01, note + f"。差は予測−実績で、青は高く、赤は低く予測した。黄色は3か月の誤差の平均が最も小さかった方法({best}、{err[best] * 100:.1f}%)",
             fontsize=7.5, color="#666666")
    fig.subplots_adjust(left=0.05, right=0.99, top=0.88, bottom=0.1)
    fig.savefig(out)
    plt.close(fig)


def tokyo():
    V = pd.read_csv(HERE / "data/veg_monthly.csv", index_col=0, parse_dates=True)
    m = pd.read_csv(HERE / "forecast/veg_models.csv").query("年 == 2026")
    A = [json.loads(f.read_text())["answer"] for f in (HERE / "forecast/runs/veg_c").glob("*.json")]
    for it, name in (("cabbage", "キャベツ"), ("onion", "たまねぎ")):
        preds = {k: [m[(m["品目"] == it) & (m["モデル"] == k) & (m["月"] == mo)]["予測"].iloc[0] for mo in (7, 8, 9)] for k in ORDER}
        preds["Claude(値段だけ・知識なし)"] = [st.median(a[f"{it}_2026-0{mo}"] for a in A) for mo in (7, 8, 9)]
        combo(name, "東京都中央卸売市場", V[f"{it}_price"], preds, ASSETS / f"combo-tokyo-{it}.png",
              "出典: 東京都中央卸売市場「市場統計情報明細データ」。予測は2026年6月までの値段だけから出した。Claude は3回の中央値")


def fukuoka():
    S = fm.series()
    r = pd.concat([pd.read_csv(HERE / "forecast/fukuoka_models.csv"), pd.read_csv(HERE / "forecast/fukuoka_claude.csv")]).query("年 == 2026")
    for it in fm.ITEMS:
        preds = {k: [r[(r["品目"] == it) & (r["モデル"] == k) & (r["月"] == mo)]["予測"].iloc[0] for mo in (7, 8, 9)] for k in ORDER}
        preds["Claude(知識なし)"] = [r[(r["品目"] == it) & (r["モデル"] == "Claude 知識なし") & (r["月"] == mo)]["予測"].iloc[0] for mo in (7, 8, 9)]
        combo(it, "福岡市中央卸売市場", S[it], preds, ASSETS / f"combo-fukuoka-{CODE[it]}.png",
              "出典: 農林水産省「青果物卸売市場調査」(2026年は日別調査を月ごとに平均)。予測は2026年6月までの値段だけから出した。Claude は3回の中央値")


if __name__ == "__main__":
    tokyo()
    fukuoka()
    print("ok")
