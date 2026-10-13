"""記事の図を作る。

- summary-7.png: 7つの頼み方(#58 の4つと #59 の3つ)を、4つの値で並べた小さなグラフ4枚
  値の出どころ: ../measure/summary-7.json
  - 足し: 素材メモにない足しの数(check_memo.py の added。P1 は抜けの側なので含まない)
  - 結びの火: 最後の段落に「火」が出た本数
  - 先に明かす: AI(Opus 5.5)が見分けた「先に明かす」関連の数
  - 驚き: AIの読者(Haiku 4.5、1本5回)が転の文で驚いた割合。転が複数ある本は最大値
  棒は3本の平均(足しと結びの火は3本の合計)、点は1本ずつの値
書体と色は #58 の図に合わせた。今回の3つを青、前回の4つを灰色にする。頼み方は軸の文字で示す
"""
import json
import os

import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["font.family"] = "Hiragino Sans"
INK, SUB, GRID = "#0b0b0b", "#52514e", "#e4e3df"
NOW, PREV = "#2a78d6", "#8f8d87"
HERE = os.path.dirname(os.path.abspath(__file__))

CONDS = [("0-none", "指示なし"), ("1-naive", "素朴に頼む"), ("2-role", "役割を与える"), ("3-technique", "起承転結と頼む"),
         ("4-forbid", "禁止する"), ("5-definition", "定義を渡す"), ("6-model", "手本を渡す")]
PANELS = [("add", "素材メモにない足し", "3本の合計(件)", sum),
          ("fire", "結びの比喩", "最後の段落に「火」が出た本数(3本中)", sum),
          ("reveal", "先に明かす", "題などが答えを先に言うつながり(平均)", lambda v: sum(v) / 3),
          ("surprise", "転での驚き", "AIの読者が転で驚いた割合(平均)", lambda v: sum(v) / 3)]


def main():
    data = json.load(open(os.path.join(HERE, "..", "measure", "summary-7.json"), encoding="utf-8"))
    fig, axes = plt.subplots(1, 4, figsize=(16, 6), dpi=150, sharey=True)
    names = [n for _, n in CONDS]
    for ax, (key, title, note, agg) in zip(axes, PANELS):
        vals = [data[c][key] for c, _ in CONDS]
        bars = [agg(v) for v in vals]
        xmax = max(max(bars), max(max(v) for v in vals)) * 1.3 + (0.15 if key == "surprise" else 0.6)
        for i, (b, v) in enumerate(zip(bars, vals)):
            ax.barh(i, b, height=0.62, color=NOW if i >= 4 else PREV, zorder=2)
            if key in ("reveal", "surprise"):
                ax.scatter(v, [i] * 3, s=20, color=INK, zorder=3, linewidths=0, clip_on=False)
            label = f"{b:.2f}" if key == "surprise" else (f"{b:.1f}" if key == "reveal" else f"{b:.0f}")
            right = max(b, max(v)) if key in ("reveal", "surprise") else b
            ax.text(right + xmax * 0.04, i, label, va="center", fontsize=11, color=INK)
        ax.set_xlim(0, xmax)
        ax.set_yticks(range(len(names)), names, fontsize=11.5, color=INK)
        ax.axhline(3.5, color=SUB, lw=0.8, ls=(0, (3, 3)), zorder=1)
        ax.set_title(title, loc="left", fontsize=14, fontweight="bold", color=INK, pad=22)
        ax.text(0, 1.02, note, transform=ax.transAxes, fontsize=9.5, color=SUB, va="bottom")
        ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(axis="x", colors=SUB, labelsize=9.5)
        ax.tick_params(axis="y", length=0)
    # sharey なので1回だけ反転する。指示なしを一番上に置く
    axes[0].invert_yaxis()
    fig.suptitle("7つの頼み方で、同じ素材メモから3本ずつ書かせた結果", x=0.02, ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.02, 0.015, "灰色が前回の4つ、青が今回の3つ。黒い点は1本ずつの値。書き手は Sonnet 5.5、照合と役割は Opus 5.5、読者は Haiku 4.5(1本5回)",
             fontsize=9.5, color=SUB)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.8, bottom=0.1, wspace=0.12)
    fig.savefig(os.path.join(HERE, "summary-7.png"), facecolor="white")


if __name__ == "__main__":
    main()
