"""記事の図を作る。

- role-counts-chart.png: 文の役割の種類別の数を、頼み方ごとに並べたグラフ(役割ごとの小さなグラフ8枚)
  値の出どころ: ../measure/role-counts.md(AI Opus 5.5 の1回目の見分け。役割は読み終えた後の役割)
  棒は3本の平均、点は seed 1〜3 の値。書体と色は #52 の図に合わせた
"""
import os
import re

import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["font.family"] = "Hiragino Sans"
INK, SUB, GRID = "#0b0b0b", "#52514e", "#e4e3df"
# 頼んだ3つは参照パレットの1番(青)。指示なしは比べる相手なので灰色。頼み方は軸の文字で示し、色だけに頼らない
ASK, BASE = "#2a78d6", "#8f8d87"
HERE = os.path.dirname(os.path.abspath(__file__))

CONDS = [("0-none", "指示なし"), ("1-naive", "素朴に頼む"), ("2-role", "役割を与える"), ("3-technique", "起承転結と頼む")]
ROWS = [("文の数", "文の数", "本文の文の数"),
        ("起", "起", "予想を持たせ始める文"),
        ("承", "承", "転の前に予想を強める文"),
        ("転[全体]", "転(全体)", "文章全体の大きな転"),
        ("転[内側]", "転(内側)", "途中の小さな転"),
        ("結", "結", "転に納得できる理由を渡す文"),
        ("問い", "問い", "答えを求める問いの文"),
        ("答え", "答え", "問いへの答えが完結する文"),
        ("関連:先に明かす", "先に明かす", "題などが、後の転や答えを先に言う")]


def load():
    text = open(os.path.join(HERE, "..", "measure", "role-counts.md"), encoding="utf-8").read()
    lines = [l for l in text.split("\n") if l.startswith("|")]
    head = [c.strip() for c in lines[0].strip("|").split("|")]
    table = {}
    for l in lines[2:]:
        cells = [c.strip() for c in l.strip("|").split("|")]
        table[cells[0]] = dict(zip(head[1:], cells[1:]))
    return table


def main():
    t = load()
    roles = [r for r in ROWS if r[0] != "文の数"]
    fig, axes = plt.subplots(2, 4, figsize=(16, 9), dpi=150, sharey=True)
    names = [n for _, n in CONDS]
    for ax, (key, name, note) in zip(axes.flat, roles):
        vals = [[int(t[key][f"{c}-s{s}"]) for s in (1, 2, 3)] for c, _ in CONDS]
        means = [sum(v) / 3 for v in vals]
        xmax = max(max(v) for v in vals) * 1.35 + 1
        for i, (m, v) in enumerate(zip(means, vals)):
            ax.barh(i, m, height=0.62, color=BASE if i == 0 else ASK, zorder=2)
            ax.scatter(v, [i] * 3, s=22, color=INK, zorder=3, linewidths=0, clip_on=False)
            ax.text(max(max(v), m) + xmax * 0.04, i, f"{m:.1f}", va="center", fontsize=11, color=INK)
        ax.set_xlim(0, xmax)
        ax.set_yticks(range(len(names)), names, fontsize=11.5, color=INK)
        ax.set_title(name, loc="left", fontsize=14, fontweight="bold", color=INK, pad=22)
        ax.text(0, 1.02, note, transform=ax.transAxes, fontsize=10, color=SUB, va="bottom")
        ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(axis="x", colors=SUB, labelsize=9.5)
        ax.tick_params(axis="y", length=0)
    # sharey なので1回だけ反転する。指示なし(比べる相手)を一番上に置く
    axes[0, 0].invert_yaxis()
    fig.suptitle("AIが見分けた文の役割の数(頼み方ごと、3本ずつ)", x=0.02, ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.02, 0.012, "棒と数字は3本の平均、黒い点は1本ずつの値。灰色が指示なし(比べる相手)。AI(Opus 5.5)が1回見分けた。役割は読み終えた後の役割。「先に明かす」は役割ではなく、文どうしのつながりの数",
             fontsize=9.5, color=SUB)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.86, bottom=0.07, wspace=0.12, hspace=0.55)
    fig.savefig(os.path.join(HERE, "role-counts-chart.png"), facecolor="white")


if __name__ == "__main__":
    main()
