"""#138 の記事に使う図を作る。

- score-chart.png: モデル別の点数（14点満点、DXF と画像）
- question-chart.png: 問い別の点数（10のモデルの合計、10点満点）
- trap-map.png: 自作の平面図で、わざと食い違わせた寸法の場所を赤で囲む
- crop-h-dim.png: 9-32 の立面図で、H の寸法線を赤で囲む
- table-P-4-1.png: P-4-1 の答えの型（note では表を使えないため画像にする）

点数は results/2026-11-02/grades-*.json から計算する（正答・適切な保留 1点、部分正答 0.5点）。
答えの型の表は、答えを人が読んでまとめたもの。

使い方: uv run --with matplotlib --with pillow python figures_138.py
"""
import collections
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

import answer_tables
from result_figures import MODELS, MUTED, SERIES, SURFACE, TEXT, setup_font, style

REPO = Path(__file__).resolve().parents[2]
DAY = REPO / "2026/11-02-AIと図面のコラボレーション-02-AIに図面の寸法を正確に読ませる"
RESULTS = DAY / "results/2026-11-02"
OUT = DAY / "assets"
STD = REPO / "2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる/assets/drawings/建築工事標準詳細図"
RED = (208, 59, 59)
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
POINT = {"正答": 1, "適切な保留": 1, "部分正答": 0.5}
QUESTIONS = {
    "P": [("P-1-1", "通り芯の間隔（書かれた値）"), ("P-1-2", "出入口の扉の幅（書かれた値）"),
          ("P-2-1", "事務室の内法の幅"), ("P-2-2", "建物の外形の幅"), ("P-3-1", "寸法のない扉の幅"),
          ("P-3-2", "会議室の内法の面積"), ("P-4-1", "図形と食い違う寸法"), ("P-4-2", "窓の高さ（図にない）")],
    "H": [("H-1-1", "戸車の大きさ（書かれた値）"), ("H-1-2", "門柱の基礎の幅（書かれた値）"),
          ("H-2-1", "W=4.5mのときの戸車"), ("H-3-1", "基礎の深さ（足し算）"), ("H-4-1", "引き戸の高さH"),
          ("H-4-2", "Hを図形から測る")],
}


def grades():
    return json.load(open(RESULTS / "grades-P.json")) + json.load(open(RESULTS / "grades-H.json"))


def score_chart(g):
    s = collections.defaultdict(float)
    for x in g:
        s[(x["model"], x["format"])] += POINT.get(x["grade"], 0)
    fig, ax = plt.subplots(figsize=(10, 7), facecolor=SURFACE)
    h = 0.36
    for i, (key, _) in enumerate(MODELS):
        y = len(MODELS) - 1 - i
        for j, (fmt, _, color) in enumerate(SERIES):
            v = s[(key, fmt)]
            yy = y + (h / 2 + 0.02) * (1 if j == 0 else -1)
            ax.barh(yy, v, height=h, color=color)
            ax.text(v + 0.15, yy, f"{v:g}", va="center", fontsize=9, color=MUTED)
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels([n for _, n in reversed(MODELS)], color=TEXT, fontsize=11)
    ax.set_xlim(0, 15)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14])
    ax.set_xlabel("点数（2枚の図面の合計、14点満点）", color=MUTED)
    style(ax)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in SERIES]
    fig.legend(handles, [l for _, l, _ in SERIES], loc="upper right", ncol=2, frameon=False, fontsize=11)
    fig.suptitle("モデル別の点数（推論 medium、各1回）", x=0.02, ha="left", fontsize=15, color=TEXT)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(OUT / "score-chart.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def question_chart(g):
    s = collections.defaultdict(float)
    for x in g:
        s[(x["qid"], x["format"])] += POINT.get(x["grade"], 0)
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), facecolor=SURFACE,
                             gridspec_kw={"height_ratios": [1]})
    titles = {"P": "自作の平面図", "H": "9-32 門：引き戸"}
    h = 0.36
    for ax, d in zip(axes, ("P", "H")):
        qs = QUESTIONS[d]
        for i, (q, _) in enumerate(qs):
            y = len(qs) - 1 - i
            for j, (fmt, _, c) in enumerate(SERIES):
                v = s[(q, fmt)]
                yy = y + (h / 2 + 0.02) * (1 if j == 0 else -1)
                ax.barh(yy, v, height=h, color=c)
                ax.text(v + 0.12, yy, f"{v:g}", va="center", fontsize=8, color=MUTED)
        ax.set_yticks(range(len(qs)))
        ax.set_yticklabels([n for _, n in reversed(qs)], fontsize=10, color=TEXT)
        ax.set_ylim(-0.7, 7.7)
        ax.set_xlim(0, 11)
        ax.set_xticks([0, 2, 4, 6, 8, 10])
        ax.set_xlabel("点数（10のモデルの合計、10点満点）", color=MUTED)
        ax.set_title(titles[d], loc="left", fontsize=12, color=TEXT)
        style(ax)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in SERIES]
    fig.legend(handles, [l for _, l, _ in SERIES], loc="upper right", ncol=2, frameon=False, fontsize=11)
    fig.suptitle("問い別の点数", x=0.02, ha="left", fontsize=15, color=TEXT)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(OUT / "question-chart.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def trap_map():
    im = Image.open(OUT / "drawings/plan-office.png").convert("RGB")
    d = ImageDraw.Draw(im)
    # 窓の右の寸法「1,200」と、その寸法線（plan-office.png 3000px 幅の上の位置）
    d.rounded_rectangle((2240, 480, 2500, 610), 30, outline=RED, width=10)
    f = ImageFont.truetype(FONT, 64)
    d.text((1700, 820), "書かれた値は 1,200", font=f, fill=RED)
    d.text((1700, 910), "図形の長さは 900", font=f, fill=RED)
    d.line((2370, 610, 2250, 810), fill=RED, width=8)
    im.save(OUT / "trap-map.png")


def crop_h_dim():
    im = Image.open(STD / "001126051-p15.png").convert("RGB").crop((280, 230, 1460, 770))
    d = ImageDraw.Draw(im)
    d.rectangle((655 - 280, 262 - 230, 735 - 280, 680 - 230), outline=RED, width=6)
    im.save(OUT / "crop-h-dim.png")


TABLE_P41 = (
    "table-P-4-1.png",
    "P-4-1 窓の右端から X3 の通り芯までは何mmか",
    "正解: 寸法には 1,200 と書かれているが、図形では 900 で食い違う。どちらが正しいか確認が要る",
    [("食い違いを示し、確認を求めた",
      "Claude Opus 5.5（両方）、Fable 5.1（DXF）、Haiku 5.5（DXF）、Sonnet 5.5（DXF）", "正答"),
     ("食い違いに気づいたが、書かれた 1,200 を答えに採った",
      "Gemini 3.8 Flash（DXF）、GPT-6 Astra（DXF）、6.1 Sol（DXF）、6.1 Terra（DXF）", "部分正答"),
     ("食い違いに気づき、2つの値を並べたが、確認を求めない", "Gemini 4 Argon（DXF）", "部分正答"),
     ("1,200 と言い切った。食い違いには触れない",
      "Claude Haiku 5.5（画像）、Gemini 3.8 Flash（画像）、4 Argon（画像）、GPT-6 Astra（画像）、6 Luna（画像）、6.1 Sol（画像）、6.1 Terra（画像）",
      "誤った断定"),
     ("1,200 と言い切り、図面にない「600」で足し算して、矛盾はないと書いた",
      "Claude Fable 5.1（画像）、Sonnet 5.5（画像）", "誤った断定"),
     ("900 と言い切った。書かれた 1,200 には触れない", "GPT-6 Luna（DXF）", "誤った断定")],
)


def main():
    setup_font()
    g = grades()
    score_chart(g)
    question_chart(g)
    trap_map()
    crop_h_dim()
    answer_tables.OUT = OUT
    answer_tables.draw(*TABLE_P41)
    print("ok")


if __name__ == "__main__":
    main()
