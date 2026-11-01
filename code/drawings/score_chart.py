"""#132 のモデル別の点数を、記事用の棒グラフにする。

図面ごとに1枚の小さな図を並べ、モデルごとに DXF と画像の点数を横棒で比べる。
点数は results/2026-11-01/grades-*-medium.json から計算する（正答・適切な保留 1点、部分正答 0.5点）。

使い方: uv run --with matplotlib python score_chart.py 出力.png
"""
import collections
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる/results/2026-11-01"
MODELS = [
    ("claude-haiku-5-5", "Claude Haiku 5.5"), ("claude-sonnet-5-5", "Claude Sonnet 5.5"),
    ("claude-opus-5-5", "Claude Opus 5.5"), ("claude-fable-5-1", "Claude Fable 5.1"),
    ("gpt-6-luna", "GPT-6 Luna"), ("gpt-6.1-terra", "GPT-6.1 Terra"),
    ("gpt-6.1-sol", "GPT-6.1 Sol"), ("gpt-6-astra", "GPT-6 Astra"),
    ("gemini-3.8-flash", "Gemini 3.8 Flash"), ("gemini-4-argon", "Gemini 4 Argon"),
]
PANELS = [("L", "易しい図面（4-01 建具：形状寸法）"), ("H", "難しい図面（9-32 門：引き戸）")]
SERIES = [("dxf", "DXF", "#2a78d6"), ("png", "画像", "#eb6834")]
TEXT, MUTED, SURFACE = "#0b0b0b", "#52514e", "#fcfcfb"
OK = {"正答", "適切な保留"}


def scores(drawing):
    d = collections.defaultdict(float)
    for x in json.load(open(RESULTS / f"grades-{drawing}-medium.json")):
        d[(x["model"], x["format"])] += 1 if x["grade"] in OK else 0.5 if x["grade"] == "部分正答" else 0
    return d


def main(out):
    for f in font_manager.findSystemFonts():
        if "NotoSansJP" in f:
            font_manager.fontManager.addfont(f)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name()
    fig, axes = plt.subplots(1, 2, figsize=(12, 7), sharey=True, facecolor=SURFACE)
    h = 0.36
    for ax, (drawing, title) in zip(axes, PANELS):
        s = scores(drawing)
        ax.set_facecolor(SURFACE)
        for i, (key, _) in enumerate(MODELS):
            y = len(MODELS) - 1 - i
            for j, (fmt, _, color) in enumerate(SERIES):
                v = s[(key, fmt)]
                yy = y + (h / 2 + 0.02) * (1 if j == 0 else -1)
                ax.barh(yy, v, height=h, color=color)
                ax.text(v + 0.15, yy, f"{v:g}", va="center", fontsize=9, color=MUTED)
        ax.set_title(title, fontsize=13, color=TEXT, loc="left")
        ax.set_xlim(0, 15)
        ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14])
        ax.xaxis.grid(True, color="#e6e5e0", linewidth=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#c9c8c2")
        ax.tick_params(colors=MUTED, length=0)
        ax.set_xlabel("点数（14点満点）", color=MUTED)
    axes[0].set_yticks(range(len(MODELS)))
    axes[0].set_yticklabels([n for _, n in reversed(MODELS)], color=TEXT, fontsize=11)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in SERIES]
    fig.legend(handles, [l for _, l, _ in SERIES], loc="upper right", ncol=2, frameon=False,
               fontsize=11, labelcolor=TEXT)
    fig.suptitle("モデル別の点数（推論 medium、各1回）", x=0.02, ha="left", fontsize=15, color=TEXT)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out, dpi=150, facecolor=SURFACE)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
