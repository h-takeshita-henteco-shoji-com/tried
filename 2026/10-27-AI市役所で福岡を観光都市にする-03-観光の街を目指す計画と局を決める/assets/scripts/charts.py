"""記事の図を作る(#124)。表は note で崩れるので、画像にする。

数は mayor-note.md の数字の表(月例の行)と council/m*-run.json から取った。
使い方: uv run --with matplotlib --with pillow python assets/scripts/charts.py
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

RUN = Path(__file__).resolve().parents[2]
OUT = RUN / "assets"
FONT_B = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_R = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
font_manager.fontManager.addfont(FONT_R)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT_R).get_name()

BG = "#fafaf8"
ORANGE = "#ea6a32"
GREEN = "#21aa78"
BLUE = "#3c78c8"
GRAY = "#8c8c8c"

# 月末の数字(0 は出発点)
TOURISTS = [1646, 1747, 1772, 1742, 1811, 1801, 1665, 1744, 1790, 1705, 1763, 1725, 1765,
            1847, 1851, 1937, 1875, 1783, 1795, 1852, 1837, 2020, 2020, 2011, 2048]
POP = [178872, 178859, 178639, 178486, 178380, 178150, 179174, 180138, 180168, 180117, 179848, 179547, 179020,
       178202, 177176, 176528, 175864, 175384, 174778, 174330, 174078, 173537, 172759, 172273, 171949]


def monthly():
    fig, axes = plt.subplots(2, 1, figsize=(12, 8.4), facecolor=BG, sharex=True)
    xs = list(range(25))
    for ax in axes:
        ax.set_facecolor(BG)
        ax.axvspan(12, 24, color="#eeeeea", zorder=0)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#dddddd")
    a = axes[0]
    a.plot(xs, TOURISTS, color=ORANGE, lw=3, marker="o")
    a.axhline(3000, color=GRAY, ls="--")
    a.text(0.2, 2930, "目標 3,000人", color=GRAY, fontsize=13, va="top")
    a.set_ylim(1500, 3100)
    a.set_title("観光客の数(月末)", fontsize=17, loc="left")
    a.annotate("名所に電気が通る(17か月目)", xy=(17, 1783), xytext=(13.3, 1580), fontsize=12,
               arrowprops=dict(arrowstyle="->", color=GRAY))
    a.annotate("2,000人を超える(21か月目)", xy=(21, 2020), xytext=(16.2, 2350), fontsize=12,
               arrowprops=dict(arrowstyle="->", color=GRAY))
    a.text(6, 3050, "1年目", ha="center", fontsize=14, color=GRAY)
    a.text(18, 3050, "2年目", ha="center", fontsize=14, color=GRAY)
    b = axes[1]
    b.plot(xs, [p / 10000 for p in POP], color=BLUE, lw=3, marker="o")
    b.set_title("人口(万人、月末)", fontsize=17, loc="left")
    b.set_ylim(17.0, 18.2)
    b.set_xticks(xs)
    b.set_xticklabels(["始"] + [str(i) for i in range(1, 25)])
    b.set_xlabel("か月目", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT / "chart-monthly.png", dpi=110, facecolor=BG)


def measures():
    """年ごとに、採った施策を市の計画の分野で数える。"""
    names = {"5": "観光", "6": "交通", "4": "環境・景観", "3": "安全", "2": "教育", "8": "物流", "1": "医療など", "財": "医療など"}
    order = ["観光", "交通", "環境・景観", "安全", "教育", "物流", "医療など"]
    colors = [ORANGE, BLUE, GREEN, "#a05ac8", "#d2a032", "#5a5a5a", GRAY]
    years = []
    for a, b in [(1, 12), (13, 24)]:
        c = {k: 0 for k in order}
        for m in range(a, b + 1):
            r = json.loads((RUN / "council" / f"m{m:02d}-run.json").read_text())
            for x in r["bill"]["measures"]:
                items = " ".join(x.get("planItems") or [])
                key = "5" if "5-" in items else (items[:1] if items else "財")
                c[names.get(key, "医療など")] += 1
        years.append(c)
    fig, ax = plt.subplots(figsize=(12, 5.2), facecolor=BG)
    ax.set_facecolor(BG)
    for row, (label, c) in enumerate(zip(["1年目", "2年目"], years)):
        left = 0
        for k, col in zip(order, colors):
            v = c[k]
            if not v:
                continue
            ax.barh(row, v, left=left, color=col, edgecolor="white")
            if v >= 4:
                ax.text(left + v / 2, row, f"{k}\n{v}", ha="center", va="center", color="white", fontsize=12)
            else:
                ax.text(left + v / 2, row, str(v), ha="center", va="center", color="white", fontsize=12)
            left += v
        ax.text(left + 0.5, row, f"計{left}件", va="center", fontsize=13)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=k) for k, c in zip(order, colors)], ncol=7, loc="upper center",
              bbox_to_anchor=(0.5, -0.08), frameon=False, fontsize=12)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["1年目", "2年目"], fontsize=14)
    ax.invert_yaxis()
    ax.set_xlim(0, 64)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("採った施策の分野(市の計画のどの施策に向けた手か)", fontsize=16, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "chart-measures.png", dpi=110, facecolor=BG)
    return years


def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def harness():
    """新しいハーネスの1か月。前回から変えた所に橙の印を付ける。"""
    W, H = 1500, 1080
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    d.text((W // 2, 36), "新しいAI市役所の1か月", font=f(40, True), fill=(30, 30, 30), anchor="mt")
    d.text((W // 2, 92), "橙の枠が、前回から変えた所", font=f(24), fill=(95, 95, 95), anchor="mt")
    steps = [
        ("見る", "市長が街を見て、今月の重点を決める", "地図と、空き地や島の座標を渡す", True),
        ("長期計画", "各局が12か月の計画を作り、市長がレビュー", "1か月目と13か月目だけ。差し戻しは2回まで", True),
        ("案", "8つの局が、計画に沿って案を出す", "1局5件まで(前回は1件)。財政局も案を出す局に", True),
        ("まとめ", "市長が案を選ぶ。局をまたぐ調整も市長が決める", "採る件数に上限なし(前回は3件)", True),
        ("差し戻し", "条件付きで外した案を、局が1回だけ調べ直す", "市長がまとめ直す", True),
        ("議会", "取り壊しなどの議案と、全部の施策のお金を確かめる", "週の収支 +3,000、所持金 187万4千を守る", True),
        ("実行", "実行する市長だけが街を動かす。10日ずつ3回進める", "途中で2回見回る", False),
    ]
    y = 140
    for i, (name, desc, note, changed) in enumerate(steps):
        box = (120, y, W - 120, y + 112)
        d.rounded_rectangle(box, 14, fill=(240, 239, 236), outline=(234, 106, 50) if changed else (200, 200, 200),
                            width=5 if changed else 2)
        d.text((170, y + 56), name, font=f(32, True), fill=(30, 30, 30), anchor="lm")
        d.text((420, y + 38), desc, font=f(26), fill=(30, 30, 30), anchor="lm")
        d.text((420, y + 80), note, font=f(22), fill=(95, 95, 95), anchor="lm")
        if i < len(steps) - 1:
            d.polygon([(W // 2 - 14, y + 116), (W // 2 + 14, y + 116), (W // 2, y + 134)], fill=(160, 160, 160))
        y += 134
    img.save(OUT / "diagram-harness.png")


if __name__ == "__main__":
    monthly()
    print(measures())
    harness()
