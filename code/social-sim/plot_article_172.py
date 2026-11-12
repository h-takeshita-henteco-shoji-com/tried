"""#172 の記事(note)用の説明図を作る。note では表が使えないため、ルールと比較を図にする。

使い方: uv run --with matplotlib python plot_article_172.py <出力フォルダ>
作る図:
- rules-flow.png      公共財ゲームの1回の流れ(受け取る → 入れる → 配られる)
- rules-payoff.png    全員が入れる / 1人だけ入れない / 全員が入れない ときの稼ぎ
- punish-rule.png     減点の仕組み(付ける人が払い、付けられた人の稼ぎが減る)
- dist-lottery-answer.png / dist-lottery-position.png  確率で答えさせる方法と、くじの位置
- people-lines.png    一人の中のゆらぎ(毎回くじ)と、人ごとの違い(固定0.7)
- criteria-grid.png   方法ごとの5つの物差しの判定
"""
import json
import os
import sys
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

plt.rcParams["font.family"] = ["Hiragino Sans", "sans-serif"]
HERE = os.path.dirname(os.path.abspath(__file__))
SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
GOOD, CRITICAL = "#0ca30c", "#d03b3b"
PEOPLE = ["Aさん", "Bさん", "Cさん", "Dさん"]


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def person(ax, x, y, name, color=BLUE, r=0.55, fs=10):
    ax.add_patch(Circle((x, y), r, facecolor=color, edgecolor=SURFACE, lw=2))
    ax.text(x, y, name[0], ha="center", va="center", color="white", fontsize=fs + 2, weight="bold")


def arrow(ax, p, q, color=MUTED, lw=1.6, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def box(ax, x, y, w, h, text, fc="#f0efec", ec=GRID, fs=11, color=INK):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.08,rounding_size=0.25",
                                facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color, linespacing=1.5)


def save(fig, out):
    fig.savefig(out, dpi=150, facecolor=SURFACE, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print(out)


def rules_flow(out):
    """1回の流れ。例として 10・10・5・15 を入れた場合を、手元と配当の足し算まで見せる。"""
    put = [10, 10, 5, 15]
    total = sum(put)
    share = total * 0.4
    fig, ax = canvas(12, 4.8, 30, 12)
    heads = [(3.2, "① 全員が20ポイントを\n受け取る"), (13.5, "② 口座に入れる量を\nそれぞれが決める"),
             (24.5, "③ 口座の合計×0.4を\n全員に同じだけ配る")]
    for x, t in heads:
        ax.text(x, 11.3, t, ha="center", va="top", fontsize=12.5, color=INK, weight="bold", linespacing=1.4)
    ys = [8.2, 6.4, 4.6, 2.8]
    # ① 受け取る
    for y, n in zip(ys, PEOPLE):
        person(ax, 1.6, y, n)
        ax.text(2.5, y, "20ポイント", va="center", fontsize=11, color=INK)
    # ② 入れる
    for y, n, p in zip(ys, PEOPLE, put):
        person(ax, 8.6, y, n)
        ax.text(9.4, y + 0.25, f"入れる {p}", va="center", fontsize=10.5, color=BLUE)
        ax.text(9.4, y - 0.35, f"手元に残す {20 - p}", va="center", fontsize=10, color=MUTED)
        arrow(ax, (12.4, y), (15.2, 5.5), color=BLUE)
    box(ax, 17.0, 5.5, 4.0, 2.6, f"グループの\n口座\n合計 {total}", fc="#e8f1fb", ec=BLUE, fs=12)
    # ③ 配る
    ax.text(17.0, 3.2, f"{total} × 0.4 = {share:g}", ha="center", fontsize=11, color=INK)
    for y, n, p in zip(ys, PEOPLE, put):
        arrow(ax, (18.8, 5.5), (21.3, y), color=AQUA)
        person(ax, 22.0, y, n)
        ax.text(22.8, y, f"手元 {20 - p} + 配当 {share:g} = ", va="center", fontsize=10.5, color=INK)
        ax.text(28.6, y, f"{20 - p + share:g}", va="center", ha="right", fontsize=12, color=INK, weight="bold")
    ax.text(15.0, 0.9, "いちばん少なく入れたCさんが、いちばん多く稼ぐ。これを10回くり返す",
            ha="center", fontsize=11.5, color=INK)
    save(fig, out)


def rules_payoff(out):
    scen = [("全員が20を入れる", [20, 20, 20, 20]), ("Dさんだけ0、ほかは20", [20, 20, 20, 0]),
            ("全員が0", [0, 0, 0, 0])]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.4), sharey=True, facecolor=SURFACE)
    for ax, (title, put) in zip(axes, scen):
        ax.set_facecolor(SURFACE)
        share = sum(put) * 0.4
        earn = [20 - p + share for p in put]
        colors = [BLUE if p > 0 else ORANGE for p in put]
        bars = ax.bar(range(4), earn, color=colors, width=0.62, edgecolor=SURFACE, lw=2)
        for b, e in zip(bars, earn):
            ax.text(b.get_x() + b.get_width() / 2, e + 0.8, f"{e:g}", ha="center", fontsize=12, color=INK)
        ax.set_xticks(range(4))
        ax.set_xticklabels(PEOPLE, fontsize=10.5, color=INK)
        ax.set_title(title, fontsize=12.5, color=INK, loc="left")
        ax.set_ylim(0, 50)
        ax.axhline(20, color=MUTED, lw=1, ls=(0, (3, 2)))
        ax.grid(axis="y", color=GRID, lw=1)
        ax.set_axisbelow(True)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(colors=MUTED, length=0)
    axes[0].set_ylabel("その回の稼ぎ(ポイント)", color=MUTED)
    fig.text(0.5, -0.04, "点線は受け取った20。全員が入れれば、全員が32に増える。ただ、自分だけ入れないと44になる。"
             "全員がそう考えると、20のまま",
             ha="center", fontsize=11.5, color=INK)
    fig.tight_layout()
    save(fig, out)


def punish_rule(out):
    fig, ax = canvas(12, 4.0, 30, 10)
    ax.text(15, 9.5, "全員が入れた量を見たあとで、ほかの人に減点を付けられる", ha="center", va="top",
            fontsize=13, color=INK, weight="bold")
    person(ax, 4, 5, "Aさん", r=0.9, fs=14)
    ax.text(4, 3.4, "Aさん(20を入れた)", ha="center", fontsize=11, color=INK)
    person(ax, 26, 5, "Dさん", color=ORANGE, r=0.9, fs=14)
    ax.text(26, 3.4, "Dさん(0を入れた)", ha="center", fontsize=11, color=INK)
    arrow(ax, (5.3, 5.3), (24.6, 5.3), color=CRITICAL, lw=2.2)
    ax.text(15, 6.0, "減点を3点付ける", ha="center", fontsize=12.5, color=CRITICAL, weight="bold")
    box(ax, 9.5, 1.6, 10, 2.0, "付けたAさんも払う\n3点なら4ポイント(10点で30ポイント)", fs=10.5)
    box(ax, 20.5, 1.6, 10, 2.0, "付けられたDさんのその回の稼ぎが\n1点につき10%減る  44 → 30.8", fs=10.5)
    save(fig, out)


def dist_lottery(out):
    """追加検証Aの実際の答え(組み替え・罰なし、1回目、p020)を使う。"""
    p = [5, 0, 0, 3, 3, 8, 3, 5, 7, 5, 25, 3, 5, 2, 2, 7, 2, 1, 1, 1, 12]
    cum, acc = [], 0
    for v in p:
        acc += v
        cum.append(acc)

    def at(u):
        return next(i for i, c in enumerate(cum) if c >= u * 100)

    f1, a1 = plt.subplots(figsize=(8.5, 4.4), facecolor=SURFACE)
    f2, a2 = plt.subplots(figsize=(10, 3.6), facecolor=SURFACE)
    for ax in (a1, a2):
        ax.set_facecolor(SURFACE)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(colors=MUTED, length=0)
    a1.bar(range(21), p, color=BLUE, width=0.75, edgecolor=SURFACE, lw=1)
    a1.set_xticks([0, 5, 10, 15, 20])
    a1.set_xlabel("入れるポイント", color=MUTED)
    a1.set_ylabel("AIが答えた確率(%)", color=MUTED)
    a1.set_title("AIに「0〜20のそれぞれを入れる確率」を答えさせる", fontsize=12, color=INK, loc="left")
    a1.grid(axis="y", color=GRID, lw=1)
    a1.set_axisbelow(True)
    a1.annotate("1つで答えさせると、\nいつもここ(10)", (10, 25), xytext=(13.2, 22.5), fontsize=10.5,
                color=INK, arrowprops={"arrowstyle": "-|>", "color": MUTED})
    a1.annotate("20にも12%", (20, 12), xytext=(16.4, 16.5), fontsize=10.5, color=INK,
                arrowprops={"arrowstyle": "-|>", "color": MUTED})
    a1.annotate("0にも5%", (0, 5), xytext=(0.6, 12.5), fontsize=10.5, color=INK,
                arrowprops={"arrowstyle": "-|>", "color": MUTED})
    # 右: 積み上げた帯の上の、くじの位置
    a2.set_xlim(0, 100)
    a2.set_ylim(0, 10)
    a2.set_yticks([])
    left = 0
    shades = ["#d6e6f8", "#a9c9ef", "#7aaae4", "#4b8bd9", "#2a78d6"]
    for i, v in enumerate(p):
        if v:
            a2.barh(5, v, left=left, height=2.2, color=shades[min(i // 5, 4)], edgecolor=SURFACE, lw=1)
            if v >= 5:
                a2.text(left + v / 2, 5, str(i), ha="center", va="center", fontsize=9,
                        color=INK if i < 10 else "white")
            left += v
    a2.set_xticks([0, 20, 50, 85, 100])
    a2.set_xticklabels(["0%", "20%", "50%", "85%", "100%"])
    a2.set_xlabel("くじの位置(帯の左端からの割合)", color=MUTED)
    a2.set_title("確率を帯に並べ、くじの位置で量を決める", fontsize=12, color=INK, loc="left")
    for u, label, c, dy in [(0.2, "いつも低めの人", ORANGE, 2.6), (0.85, "いつも高めの人", VIOLET, 2.6)]:
        x = u * 100
        a2.plot([x, x], [3.6, 6.4], color=c, lw=2.5)
        a2.text(x, 6.4 + dy - 1.6, f"{label}\n位置{int(x)}% → {at(u)}", ha="center", fontsize=10, color=INK)
    a2.text(50, 1.2, "毎回くじ: 位置を毎回引き直す。固定: 位置を人ごとに決めておく",
            ha="center", fontsize=10, color=MUTED, linespacing=1.5)
    for f, suffix in ((f1, "answer"), (f2, "position")):
        f.tight_layout()
        save(f, out.replace(".png", f"-{suffix}.png"))


def person_series(d):
    s = {}
    for line in open(os.path.join(d, "events.jsonl"), encoding="utf-8"):
        e = json.loads(line)
        for pid, c in zip(e["members"], e["contribs"]):
            s.setdefault(pid, {})[e["round"]] = c
    return {k: [v[r] for r in sorted(v)] for k, v in s.items()}


def people_lines(out):
    """同じ人物像(seed 1)の、同じ相手・罰なしの10回。固定0.7で高い順・中ほど・低い順の4人を選び、
    毎回くじ(追加検証A)でも同じ4人を描く。"""
    a = person_series(os.path.join(HERE, "runs", "20261111-150726-game-partner-n-dist"))
    r = person_series(os.path.join(HERE, "runs", "rho", "20261112-083714-game-partner-n-dist-rho0.7"))
    order = sorted(r, key=lambda k: -mean(r[k]))
    pick = [order[0], order[7], order[16], order[-1]]
    colors = [BLUE, AQUA, ORANGE, VIOLET]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4), sharey=True, facecolor=SURFACE)
    for ax, (title, s) in zip(axes, [("毎回くじ", a), ("くじの位置の度合い0.7", r)]):
        ax.set_facecolor(SURFACE)
        for k, c, lab in zip(pick, colors, ["1人目", "2人目", "3人目", "4人目"]):
            ax.plot(range(1, 11), s[k], color=c, lw=2, marker="o", ms=6, mec=SURFACE, mew=1.5, label=lab)
        ax.set_title(title, fontsize=12.5, color=INK, loc="left")
        ax.set_xticks(range(1, 11))
        ax.set_ylim(-0.5, 20.5)
        ax.set_yticks(range(0, 21, 5))
        ax.set_xlabel("回", color=MUTED)
        ax.grid(axis="y", color=GRID, lw=1)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(GRID)
        ax.tick_params(colors=MUTED)
    axes[0].set_ylabel("入れたポイント", color=MUTED)
    fig.legend(*axes[1].get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(0.5, 1.06), frameon=False, fontsize=10, ncol=4)
    fig.text(0.5, -0.04, "同じ4人(同じ人物像)の、同じ相手・減点なしの10回。左は線が絡み合い、右は人ごとの量が分かれる",
             ha="center", fontsize=11.5, color=INK)
    fig.tight_layout()
    save(fig, out)


def criteria_grid(out):
    cols = ["1回目の\n平均", "全部入れる人も\n入れない人も", "減点なしで\n下がる", "減点ありが\n多い", "少ない人ほど\n減点される"]
    rows = [("そのまま1つで答える(#169)", [1, 0, 1, 1, 1]),
            ("確率で答え、毎回くじ", [0, 1, 1, 1, 1]),
            ("くじの位置を完全に固定", [1, 0, 0, 1, 1]),
            ("くじの位置の度合い0.7", [1, 1, 1, 1, 1])]
    fig, ax = canvas(12, 3.9, 13.6, len(rows) + 1.6)
    for j, c in enumerate(cols):
        ax.text(5.6 + j * 1.75, len(rows) + 0.75, c, ha="center", va="center", fontsize=10.5, color=INK,
                linespacing=1.3)
    for i, (name, ok) in enumerate(rows):
        y = len(rows) - i - 0.3
        bold = i == len(rows) - 1
        ax.text(0.1, y, name, va="center", fontsize=11.5, color=INK, weight="bold" if bold else "normal")
        for j, v in enumerate(ok):
            x = 5.6 + j * 1.75
            ax.add_patch(FancyBboxPatch((x - 0.72, y - 0.36), 1.44, 0.72, boxstyle="round,pad=0.02,rounding_size=0.12",
                                        facecolor="#e6f4e6" if v else "#fae6e6", edgecolor=SURFACE))
            ax.text(x, y, "✓ 合う" if v else "✗ 外れる", ha="center", va="center", fontsize=10.5,
                    color="#006300" if v else CRITICAL)
    save(fig, out)


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    rules_flow(os.path.join(outdir, "rules-flow.png"))
    rules_payoff(os.path.join(outdir, "rules-payoff.png"))
    punish_rule(os.path.join(outdir, "punish-rule.png"))
    dist_lottery(os.path.join(outdir, "dist-lottery.png"))
    people_lines(os.path.join(outdir, "people-lines.png"))
    criteria_grid(os.path.join(outdir, "criteria-grid.png"))


if __name__ == "__main__":
    main(sys.argv[1])
