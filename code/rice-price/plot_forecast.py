"""実績と予測の折れ線グラフ(#184)。使い方: .venv/bin/python plot_forecast.py"""
import json
import statistics as st
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "2026/11-22-糸島の農業を社会学とAIで考える-09-米価を時系列データで予測する/assets/forecast-vs-actual.png"
plt.rcParams["font.family"] = "Hiragino Sans"

act = pd.read_csv(HERE / "data/monthly.csv", index_col=0, parse_dates=True)["all"].loc["2023-01":]
base = pd.read_csv(HERE / "forecast/baselines.csv").query("年産 == 2026").set_index("方法")["予測"]
months = pd.date_range("2026-09-01", "2027-08-01", freq="MS")

def claude_path(cond):
    a = [json.loads(f.read_text())["answer"] for f in (HERE / f"forecast/runs/{cond}").glob("*.json")]
    so = st.median(x["sep_oct_point"] for x in a)
    rest = [st.median(x["monthly"][m.strftime("%Y-%m")] for x in a) for m in months[2:]]
    return [so, so] + rest

fig, ax = plt.subplots(figsize=(11, 5.6), dpi=150)
ax.plot(act.index, act.values, color="#222222", lw=2.4, label="実績(全銘柄平均)", zorder=5)
ax.axvline(pd.Timestamp("2026-08-31"), color="#999999", lw=1, ls=":")
ax.text(pd.Timestamp("2026-08-20"), 11000, "予測した時点\n(2026年8月31日)", ha="right", va="bottom", fontsize=9, color="#666666")

C = {"1a": ("Claude 価格だけ", "#0072B2", "-"), "3b": ("Claude 価格+需給+知識", "#56B4E9", "--")}
for k, (lab, col, ls) in C.items():
    ax.plot(months, claude_path(k), color=col, lw=2, ls=ls, marker="o", ms=3, label=lab)
S = {"前の年産の平均": ("前の年と同じ", "#000000")}
sep_oct = months[:2]
for k, (lab, col) in S.items():
    ax.plot(sep_oct, [base[k]] * 2, color=col, lw=3, ls=(0, (1, 1)), label=f"{lab}(9・10月)")
mm = pd.read_csv(HERE / "forecast/monthly_models.csv", index_col=0)
M = {"SARIMA": "#CC79A7", "指数平滑法": "#D55E00", "Prophet(Meta)": "#E69F00", "TimesFM(Google)": "#8C6D31", "Chronos(Amazon)": "#7F7F7F"}
for k, col in M.items():
    ax.plot(months, mm[k].values, color=col, lw=1.4, ls="-.", label=k)
ax.plot([pd.Timestamp("2026-10-01")], [21360], marker="D", ms=8, color="#009E73", ls="none",
        label="堂島の先物 10月限(8月末ごろ)", zorder=6)
ax.annotate("実績 21,364円\n(9・10月の平均)", (pd.Timestamp("2026-10-01"), 21434), (pd.Timestamp("2026-11-20"), 17500),
            fontsize=9, arrowprops=dict(arrowstyle="-", color="#444444"))

# 小窓: 2026年6月〜2027年1月を拡大
ins = ax.inset_axes([0.03, 0.36, 0.33, 0.42])
ins.set_facecolor("#f7f9fc")
w = act.loc["2026-06":]
ins.plot(w.index, w.values, color="#222222", lw=2.4, marker="o", ms=4, zorder=5)
for line in ax.get_lines()[1:]:
    xs, ys = line.get_xdata(), line.get_ydata()
    ins.plot(xs, ys, color=line.get_color(), ls=line.get_linestyle(), lw=line.get_linewidth(), marker=line.get_marker(), ms=line.get_markersize())
ins.set_xlim(pd.Timestamp("2026-05-20"), pd.Timestamp("2027-01-10"))
ins.set_ylim(19000, 44000)
ins.set_xticks(pd.date_range("2026-06-01", "2027-01-01", freq="MS"))
ins.set_xticklabels(["6月", "7月", "8月", "9月", "10月", "11月", "12月", "1月"], fontsize=7)
ins.tick_params(labelsize=7)
ins.yaxis.tick_right()
ins.grid(axis="y", color="#e5e5e5", lw=0.6)
ax.indicate_inset_zoom(ins, edgecolor="#888888", alpha=0.8)
ax.set_title("米の相対取引価格:実績と、2026年8月末の時点の予測(小窓は2026年6月〜2027年1月を拡大)", fontsize=13, loc="left")
ax.set_ylabel("円/玄米60kg(税込み)")
ax.set_ylim(10000, 47000)
ax.grid(axis="y", color="#e5e5e5", lw=0.8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(loc="upper left", fontsize=8.5, frameon=False, ncol=3)
fig.text(0.01, 0.01, "出典: 農林水産省「米の相対取引価格」、堂島取引所(株探の市況記事より推定)。Claude は各5回の中央値。先物は相対取引価格と指数の定義が違う",
         fontsize=7.5, color="#666666")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(OUT)
print(OUT)
