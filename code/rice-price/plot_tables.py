"""記事に入れる表を画像にする(note は表が崩れるため)(#184)。使い方: .venv/bin/python plot_tables.py"""
import json
import statistics as st
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import fukuoka_models as fm

HERE = Path(__file__).parent
ASSETS = HERE.parent.parent / "2026/11-22-糸島の農業を社会学とAIで考える-09-米価を時系列データで予測する/assets"
plt.rcParams["font.family"] = "Hiragino Sans"


def table_png(df, title, note, out, col_w=None, highlight=None, fs=10.5, color_col=None):
    nrow, ncol = df.shape
    col_w = col_w or [2.6] + [1.3] * (ncol - 1)
    fig_w = max(sum(col_w) * 0.62 + 0.4, len(title) * 0.19)
    fig, ax = plt.subplots(figsize=(fig_w, 0.42 * (nrow + 1) + 1.0), dpi=160)
    ax.axis("off")
    tw = sum(col_w) * 0.62 / fig_w  # 表の幅は列の幅で決め、図が広いときは左に寄せる
    t = ax.table(cellText=df.values, colLabels=df.columns, loc="upper left", cellLoc="right", colLoc="center",
                 colWidths=[w / sum(col_w) * tw for w in col_w], bbox=[0, 0, tw, 1])
    t.auto_set_font_size(False)
    t.set_fontsize(fs)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#dddddd")
        cell.set_linewidth(0.6)
        if r == 0:
            cell.set_facecolor("#f0f0f0")
            cell.set_text_props(weight="bold")
        elif c == 0:
            cell.set_text_props(ha="left")
            cell._loc = "left"
        if color_col is not None and r > 0 and c == color_col:
            txt = cell.get_text().get_text()
            cell.get_text().set_color("#1F5FAD" if txt.startswith("(+)") else "#C0392B" if txt.startswith("(-)") else "#444444")
        if highlight and r > 0 and highlight(r - 1, c):
            cell.set_facecolor("#FFF3B0")
            if c == 0:
                cell.set_text_props(weight="bold")
    fig.suptitle(title, x=0.01, ha="left", fontsize=12.5)
    fig.text(0.01, 0.01, note, fontsize=7.5, color="#666666")
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    fig.savefig(out)
    plt.close(fig)


def rice():
    act = (21293 + 21434) / 2
    b = pd.read_csv(HERE / "forecast/baselines.csv").query("年産 == 2026").set_index("方法")["予測"]
    mm = pd.read_csv(HERE / "forecast/monthly_models.csv", index_col=0)
    def cl(c):
        return st.median(json.loads(f.read_text())["answer"]["sep_oct_point"] for f in (HERE / f"forecast/runs/{c}").glob("*.json"))
    rows = [("前の月のまま(2026年8月の値)", b["前の年産の8月の値"]), ("前の年産の平均のまま", b["前の年産の平均"])]
    rows += [(k, mm[k].iloc[:2].mean()) for k in ["TimesFM(Google)", "Chronos(Amazon)", "Prophet(Meta)", "SARIMA", "指数平滑法"]]
    rows += [("Claude 値段だけ・知識なし", cl("1a")), ("Claude 値段だけ・知識あり", cl("1b")),
             ("Claude 値段+需給・知識なし", cl("3a")), ("Claude 値段+需給・知識あり", cl("3b"))]
    df = pd.DataFrame(rows, columns=["方法", "予測(円)"])
    df["実績(円)"] = f"{act:,.0f}"
    df["差(円)"] = [diff_text(v - act) for v in df["予測(円)"]]
    df["誤差"] = [f"{v / act * 100 - 100:+.0f}%" for v in df["予測(円)"]]
    df["予測(円)"] = [f"{v:,.0f}" for v in df["予測(円)"]]
    best = min(range(len(df)), key=lambda i: abs(float(df["予測(円)"].iloc[i].replace(",", "")) - act))
    df.loc[len(df)] = ["参考: 堂島の先物(10月限、8月末ごろ)", "約21,360", f"{act:,.0f}", "約±0", "ほぼ一致"]
    table_png(df, "米の相対取引価格:2026年9・10月の平均の、実績と予測(2026年8月末の時点)",
              "円/玄米60kg、税込み。実績は9月21,293円・10月21,434円の平均。差は予測−実績(青は高く、赤は低く)。黄色は最も近かった方法。Claude は5回の中央値",
              ASSETS / "rice-table.png", col_w=[5.0, 1.6, 1.6, 1.6, 1.2], color_col=3,
              highlight=lambda r, c: r == best)


def mape(df):
    return df.assign(a=df["誤差%"].abs()).groupby("モデル")["a"].mean()


RED, BLUE = "#C0392B", "#1F5FAD"


def diff_text(v):
    return f"(+){v:,.0f}" if round(v) > 0 else (f"(-){-v:,.0f}" if round(v) < 0 else "±0")


def item_table(name, market, actual, preds, out, note):
    """1品目の表。月ごとに予測と、実績との差(予測−実績)を並べる。差は+を青、-を赤で書く。"""
    cols = [""] + [h for mo in (7, 8, 9) for h in (f"{mo}月", "差")]
    rows = [["実績"] + [x for v in actual for x in (f"{v:.0f}", "")]]
    signs = [[0] * 7]
    for k, vs in preds.items():
        rows.append([k] + [x for v, a in zip(vs, actual) for x in (f"{v:.0f}", diff_text(v - a))])
        signs.append([0] + [x for v, a in zip(vs, actual) for x in (0, (round(v - a) > 0) - (round(v - a) < 0))])
    fig, ax = plt.subplots(figsize=(7.6, 0.36 * (len(rows) + 1) + 0.9), dpi=160)
    ax.axis("off")
    t = ax.table(cellText=rows, colLabels=cols, cellLoc="right", colLoc="center",
                 colWidths=[0.31] + [0.115] * 6, bbox=[0, 0, 1, 1])
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
        if r > 0 and c > 0 and c % 2 == 0:
            sg = signs[r - 1][c]
            cell.get_text().set_color(BLUE if sg > 0 else RED if sg < 0 else "#444444")
            cell.set_fontsize(8.5)
    fig.suptitle(f"{name}({market}):2026年7〜9月の実績と予測(円/kg)", x=0.02, ha="left", fontsize=11.5)
    fig.text(0.02, 0.01, note + "。差は予測−実績で、青は高く、赤は低く予測した", fontsize=7, color="#666666")
    fig.tight_layout(rect=(0, 0.05, 1, 0.92))
    fig.savefig(out)
    plt.close(fig)


ORDER = ["前の月のまま", "前の年の同じ月", "指数平滑法", "SARIMA", "Prophet(Meta)", "TimesFM(Google)", "Chronos(Amazon)"]


def tokyo():
    m = pd.read_csv(HERE / "forecast/veg_models.csv").query("年 == 2026")
    V = pd.read_csv(HERE / "data/veg_monthly.csv", index_col=0, parse_dates=True)
    A = [json.loads(f.read_text())["answer"] for f in (HERE / "forecast/runs/veg_c").glob("*.json")]
    for it, name in (("cabbage", "キャベツ"), ("onion", "たまねぎ")):
        preds = {k: [m[(m["品目"] == it) & (m["モデル"] == k) & (m["月"] == mo)]["予測"].iloc[0] for mo in (7, 8, 9)] for k in ORDER}
        preds["Claude(値段だけ・知識なし)"] = [st.median(a[f"{it}_2026-0{mo}"] for a in A) for mo in (7, 8, 9)]
        item_table(name, "東京都中央卸売市場", [V.loc[f"2026-0{mo}-01", f"{it}_price"] for mo in (7, 8, 9)], preds,
                   ASSETS / f"table-tokyo-{it}.png", "税込み。予測は2026年6月までの値段だけから出した。Claude は3回の中央値")


CODE = {"キャベツ": "cabbage", "はくさい": "hakusai", "レタス": "lettuce", "こまつな": "komatsuna", "トマト": "tomato",
        "きゅうり": "cucumber", "なす": "eggplant", "ブロッコリー": "broccoli", "にんじん": "carrot", "ばれいしょ": "potato",
        "たまねぎ": "onion", "ねぎ": "negi"}


def fukuoka():
    S = fm.series()
    r = pd.concat([pd.read_csv(HERE / "forecast/fukuoka_models.csv"), pd.read_csv(HERE / "forecast/fukuoka_claude.csv")]).query("年 == 2026")
    for it in fm.ITEMS:
        preds = {k: [r[(r["品目"] == it) & (r["モデル"] == k) & (r["月"] == mo)]["予測"].iloc[0] for mo in (7, 8, 9)]
                 for k in ORDER + ["Claude 知識なし"]}
        preds["Claude(知識なし)"] = preds.pop("Claude 知識なし")
        item_table(it, "福岡市中央卸売市場", [S.loc[f"2026-0{mo}-01", it] for mo in (7, 8, 9)], preds,
                   ASSETS / f"table-fukuoka-{CODE[it]}.png", "実績は日別調査を月ごとに平均。予測は2026年6月までの値段だけから出した。Claude は3回の中央値")


if __name__ == "__main__":
    rice()
    tokyo()
    fukuoka()
    print("ok")
