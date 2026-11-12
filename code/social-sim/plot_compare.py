"""compare.py の結果から、回ごとの平均拠出を人間とAIで並べた図を作る。

使い方: uv run --with matplotlib python plot_compare.py compare.json out.png [減点]
- 左が「毎回同じ相手」、右が「毎回組み替え」
- 色は罰の有無(青=罰あり、橙=罰なし)、線の形は人間(点線・白抜き)とAI(実線・塗り)
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams["font.family"] = ["Hiragino Sans", "YuGothic", "sans-serif"]
SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
COLOR = {"punish": "#2a78d6", "no_punish": "#eb6834"}
LABEL = {"punish": "罰あり", "no_punish": "罰なし"}
PANELS = [("partner", "毎回同じ相手"), ("stranger", "毎回組み替え")]


def main(src, out, words="罰"):
    """words に「減点」を渡すと、凡例を「減点あり・減点なし」にする(#172 の記事と動画)。"""
    LABEL.update({"punish": f"{words}あり", "no_punish": f"{words}なし"})
    d = json.load(open(src, encoding="utf-8"))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True, facecolor=SURFACE)
    for ax, (match, title) in zip(axes, PANELS):
        ax.set_facecolor(SURFACE)
        ends = []
        for pun in ("punish", "no_punish"):
            cond = f"{match}/{pun}"
            if cond not in d["ai"]:
                continue
            c = COLOR[pun]
            h = d["human"][cond]["by_round"]
            a = d["ai"][cond]["by_round"]
            x = list(range(1, len(h) + 1))
            ax.plot(x, h, color=c, lw=2, ls=(0, (3, 2)), marker="o", ms=8,
                    mfc=SURFACE, mec=c, mew=2, label=f"人間・{LABEL[pun]}")
            ax.plot(x, a, color=c, lw=2, marker="o", ms=8, mec=SURFACE, mew=2,
                    label=f"AI・{LABEL[pun]}")
            ends.append((h[-1], f"人間・{LABEL[pun]}"))
            ends.append((a[-1], f"AI・{LABEL[pun]}"))
        # 終点のラベルを、下から順に最低 1.1 ずつ離して置く(重なり防止)
        ends.sort()
        placed = []
        for y, text in ends:
            y2 = max(y, placed[-1] + 1.1) if placed else y
            placed.append(y2)
            ax.annotate(text, (10, y), xytext=(10.35, y2), textcoords="data", va="center",
                        fontsize=10, color=INK)
        ax.set_title(title, fontsize=13, color=INK, loc="left")
        ax.set_xlim(0.5, 13.2)
        ax.set_xticks(range(1, 11))
        ax.set_ylim(0, 20)
        ax.set_yticks(range(0, 21, 5))
        ax.set_xlabel("回", color=MUTED)
        ax.grid(axis="y", color=GRID, lw=1)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(GRID)
        ax.tick_params(colors=MUTED)
    axes[0].set_ylabel(("口座に入れた量の平均(手元20のうち)" if words == "減点" else "平均の拠出(手元20のうち)"), color=MUTED)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, frameon=False, fontsize=10, handlelength=4, bbox_to_anchor=(0.5, 1.0))
    fig.suptitle("")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(out, dpi=150, facecolor=SURFACE)
    print(out)


if __name__ == "__main__":
    main(*sys.argv[1:4])
