"""罰あり・同じ相手の条件で、人間と各方法の回ごとの平均拠出を1枚に並べる(#172 の記事用)。

使い方: uv run --with matplotlib python plot_punish_paths.py out.png
- 人間: reference の値(runs/compare-fg2000.json)
- そのままのAI(#169)、確率で答えさせ人ごとの固定0.7(seed 1〜3 の平均)、
  罰する式の参加者がいる組のAI、Sonnet 5.5(固定0.7、seed 1)
"""
import glob
import json
import os
import sys
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from compare import analyze, load  # noqa: E402

plt.rcParams["font.family"] = ["Hiragino Sans", "sans-serif"]
SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"


def by_round(dirs):
    rs = [analyze(*load(d)[1:])["by_round"] for d in dirs]
    return [mean(r[i] for r in rs) for i in range(10)]


def bot_groups(d):
    """式の参加者がいる組の、AIだけの回ごとの平均。"""
    m = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
    bots = {f"p{k * 4:03d}" for k in range(m["config"]["game"]["bots"])}
    acc = {}
    for line in open(os.path.join(d, "events.jsonl"), encoding="utf-8"):
        e = json.loads(line)
        if not bots & set(e["members"]):
            continue
        for pid, c in zip(e["members"], e["contribs"]):
            if pid not in bots:
                acc.setdefault(e["round"], []).append(c)
    return [mean(acc[r]) for r in sorted(acc)]


def main(out):
    runs = os.path.join(HERE, "runs")
    ref = json.load(open(os.path.join(runs, "compare-fg2000.json"), encoding="utf-8"))
    rho = [d for d in glob.glob(os.path.join(runs, "rho", "*-partner-p-dist-rho0.7"))
           if "sonnet" not in open(os.path.join(d, "manifest.json")).read()]
    sonnet = [d for d in glob.glob(os.path.join(runs, "rho", "*-partner-p-dist-rho0.7"))
              if "sonnet" in open(os.path.join(d, "manifest.json")).read()]
    series = [  # (ラベル, 値, 色, 線)
        ("人間", ref["human"]["partner/punish"]["by_round"], INK, (0, (3, 2))),
        ("そのままのAI", ref["ai"]["partner/punish"]["by_round"], "#eb6834", "-"),
        ("確率で答え、くじの位置の固定0.7", by_round(rho), "#2a78d6", "-"),
        ("多く入れて減点も付ける人がいる組のAI", bot_groups(glob.glob(os.path.join(runs, "bots", "*-bots3p"))[0]),
         "#1baf7a", "-"),
        ("Sonnet(固定0.7)", by_round(sonnet), "#6250d6", "-"),
    ]
    fig, ax = plt.subplots(figsize=(10, 5.2), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    x = list(range(1, 11))
    ends = []
    for label, ys, c, ls in series:
        hollow = ls != "-"
        ax.plot(x, ys, color=c, lw=2, ls=ls, marker="o", ms=8,
                mfc=SURFACE if hollow else c, mec=c if hollow else SURFACE, mew=2, label=label)
        ends.append((ys[-1], label))
    ends.sort()
    placed = []
    for y, text in ends:
        y2 = max(y, placed[-1] + 1.15) if placed else y
        placed.append(y2)
        ax.annotate(text, (10, y), xytext=(10.35, y2), va="center", fontsize=10, color=INK)
    ax.set_title("減点あり・毎回同じ相手", fontsize=13, color=INK, loc="left")
    ax.set_xlim(0.5, 15.5)
    ax.set_xticks(x)
    ax.set_ylim(0, 20.5)
    ax.set_yticks(range(0, 21, 5))
    ax.set_xlabel("回", color=MUTED)
    ax.set_ylabel("口座に入れた量の平均(手元20のうち)", color=MUTED)
    ax.grid(axis="y", color=GRID, lw=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED)
    ax.legend(loc="lower left", frameon=False, fontsize=10, handlelength=4)
    fig.tight_layout()
    fig.savefig(out, dpi=150, facecolor=SURFACE)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
