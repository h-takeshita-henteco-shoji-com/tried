"""note 記事用の図。

使い方: python3 figures_article.py <出力フォルダ>
"""
import datetime as dt
import json
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

HERE = Path(__file__).parent
OUT = Path(sys.argv[1])
plt.rcParams.update({"font.family": "Hiragino Sans", "font.size": 12,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8a8984", "xtick.color": "#52514e", "ytick.color": "#52514e"})
BLUE, ORANGE, GRAY, GRID, INK, INK2 = "#2a78d6", "#eb6834", "#b9b8b2", "#e6e5e0", "#0b0b0b", "#52514e"
WD = "月火水木金"


def fig_calendar():
    """U09: 計画は月・水。9/14の週から水曜の訪問が木曜に移ったが、計画は月・水のまま。"""
    plan = {0, 2}
    visits = set()
    for line in (HERE / "data-v2/docs/U09.md").read_text().splitlines():
        if line.startswith("| 9/"):
            visits.add(int(line.split("|")[1].strip().split("/")[1]))
    weeks = []
    d = dt.date(2026, 8, 31)
    while d.month <= 9 and d <= dt.date(2026, 9, 30):
        weeks.append(d)
        d += dt.timedelta(days=7)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    for r, mon in enumerate(weeks):
        for c in range(5):
            day = mon + dt.timedelta(days=c)
            y = len(weeks) - 1 - r
            if day.month != 9:
                continue
            planned, visited = c in plan, day.day in visits
            if visited and not planned:
                fc, ec, txt, tc = ORANGE, ORANGE, "訪問\n(計画外)", "white"
            elif visited:
                fc, ec, txt, tc = BLUE, BLUE, "訪問", "white"
            elif planned:
                fc, ec, txt, tc = "white", BLUE, "予定\n(訪問なし)", BLUE
            else:
                fc, ec, txt, tc = "#f6f5f1", "#f6f5f1", "", INK2
            ax.add_patch(FancyBboxPatch((c + 0.06, y + 0.08), 0.88, 0.84, boxstyle="round,pad=0,rounding_size=0.08",
                                        fc=fc, ec=ec, lw=1.8, ls="--" if (planned and not visited) else "-"))
            ax.text(c + 0.12, y + 0.8, f"{day.day}", fontsize=10, color=tc, va="top")
            ax.text(c + 0.5, y + 0.42, txt, fontsize=10, color=tc, ha="center", va="center")
    for c in range(5):
        ax.text(c + 0.5, len(weeks) + 0.15, WD[c], ha="center", color=INK2, fontsize=12)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, len(weeks) + 0.5)
    ax.axis("off")
    ax.set_title("計画は「毎週 月・水曜日」のまま。14日の週から、水曜の訪問が木曜に移った", fontsize=12, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "1-計画と記録のずれ.png", dpi=200)
    plt.close(fig)


def fig_results():
    """1人ずつ渡したとき(観点あり)。仕込んだ不備と、ひっかけへの反応。"""
    models = ["小さいモデル\n(Haiku)", "中くらいのモデル\n(Sonnet)", "大きいモデル\n(Opus)"]
    found = [14, 14, 14]
    trap = [4, 0, 0]
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6), sharey=True)
    for ax, vals, total, color, title in [(axes[0], found, 14, BLUE, "仕込んだ不備を見つけた数(14件中)"),
                                          (axes[1], trap, 8, ORANGE, "ひっかけに反応した人数(8人中)")]:
        y = range(len(models))[::-1]
        ax.barh(list(y), [total] * 3, color="#f1f0eb", height=0.5)
        ax.barh(list(y), vals, color=color, height=0.5)
        for yy, v in zip(y, vals):
            ax.text(v + total * 0.03, yy, f"{v}", va="center", color=INK, fontsize=13)
        ax.set_xlim(0, total * 1.15)
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.tick_params(left=False)
        ax.set_title(title, fontsize=12, color=INK, loc="left")
    axes[0].set_yticks(list(range(3))[::-1])
    axes[0].set_yticklabels(models)
    fig.tight_layout()
    fig.savefig(OUT / "2-見つけた数と誤検知.png", dpi=200)
    plt.close(fig)


def card(path, title, rows, foot=None, width=7.6):
    lines = []
    for k, v in rows:
        w = textwrap.wrap(v, 34)
        lines.append((k, w))
    h = 0.9 + sum(0.34 * len(w) + 0.25 for _, w in lines) + (0.4 if foot else 0)
    fig = plt.figure(figsize=(width, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.15, 0.15), width - 0.3, h - 0.3, boxstyle="round,pad=0,rounding_size=0.15",
                                fc="white", ec=GRAY, lw=1.2))
    ax.add_patch(FancyBboxPatch((0.15, h - 0.75), width - 0.3, 0.6, boxstyle="round,pad=0,rounding_size=0.15",
                                fc="#eef3fb", ec="none"))
    ax.text(0.45, h - 0.45, title, fontsize=13, color=INK, va="center", weight="bold")
    y = h - 1.05
    for k, w in lines:
        ax.text(0.45, y, k, fontsize=11, color=INK2, va="top")
        for j, s in enumerate(w):
            ax.text(1.75, y - j * 0.34, s, fontsize=11.5, color=INK, va="top")
        y -= 0.34 * len(w) + 0.25
    if foot:
        ax.text(0.45, 0.4, foot, fontsize=9.5, color=INK2, va="center")
    fig.savefig(path, dpi=200)
    plt.close(fig)


def fig_cards():
    f = json.loads((HERE / "data-v2/out/opus-list-1/U09.json").read_text())["findings"][0]
    card(OUT / "3-AIの指摘.png", "AIの指摘(利用者U09)",
         [("どこ", f["where"]), ("何が", f["what"]), ("根拠", f["evidence"])],
         foot="架空の書類を点検させた結果。AIの出力を、言い回しはそのままに図にした")
    b = [x for x in json.loads((HERE / "data-v2/out/opus-billrule-1/U15.json").read_text())["findings"]][0]
    card(OUT / "4-算定への影響の答え.png", "AIの答え: 計画にない介助を足した回",
         [("何が", b["what"]), ("影響", "算定はできるが、計画の見直しが必要"), ("理由", b["basis"])],
         foot="架空の書類を点検させた結果。AIの出力を、言い回しはそのままに図にした")


def fig_billing():
    """不備ごとの、請求への響き方。"""
    RED, AMB, VIO = "#d64545", "#e8a23a", "#6b5fc7"
    rows = [
        ("計画にない内容を提供した", RED, "その部分は算定の根拠がない", "返還を求められうる"),
        ("計画にない日に訪ねた", RED, "緊急時訪問介護加算に当たらなければ、", "算定の根拠がない"),
        ("曜日・時間を変えたのに、計画が古いまま", AMB, "計画と実際がずれている", "計画を直す必要がある"),
        ("計画の同意が、訪問より後", VIO, "説明と同意の手続き(運営基準)の不備", "返還までは自治体の判断による"),
    ]
    legend = [(RED, "算定の根拠がない"), (AMB, "計画の見直しが必要"), (VIO, "運営基準の不備")]
    fig = plt.figure(figsize=(8.6, 4.9))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 8.6)
    ax.set_ylim(0, 4.9)
    ax.axis("off")
    ax.text(0.3, 4.55, "不備", fontsize=11, color=INK2)
    ax.text(4.35, 4.55, "請求への響き方", fontsize=11, color=INK2)
    for i, (name, col, a, b) in enumerate(rows):
        y = 3.55 - i * 0.95
        ax.add_patch(FancyBboxPatch((0.3, y), 3.5, 0.75, boxstyle="round,pad=0,rounding_size=0.1", fc="#f6f5f1", ec="none"))
        ax.text(0.5, y + 0.375, name, fontsize=11.5, color=INK, va="center")
        ax.annotate("", xy=(4.25, y + 0.375), xytext=(3.85, y + 0.375), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5))
        ax.add_patch(FancyBboxPatch((4.3, y), 4.0, 0.75, boxstyle="round,pad=0,rounding_size=0.1", fc="white", ec=col, lw=1.8))
        ax.add_patch(FancyBboxPatch((4.3, y), 0.12, 0.75, boxstyle="round,pad=0,rounding_size=0.05", fc=col, ec="none"))
        ax.text(4.6, y + 0.5, a, fontsize=11, color=INK, va="center")
        ax.text(4.6, y + 0.22, b, fontsize=11, color=INK, va="center", weight="bold")
    x = 0.3
    for col, lab in legend:
        ax.add_patch(FancyBboxPatch((x, 0.2), 0.22, 0.22, boxstyle="round,pad=0,rounding_size=0.04", fc=col, ec="none"))
        ax.text(x + 0.32, 0.31, lab, fontsize=10.5, color=INK2, va="center")
        x += 2.4
    fig.savefig(OUT / "6-請求への響き方.png", dpi=200)
    plt.close(fig)


def fig_trap():
    """ひっかけの例と、AIの判定。"""
    fig = plt.figure(figsize=(8.6, 4.6))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 8.6)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    # 左: 書類
    ax.add_patch(FancyBboxPatch((0.2, 0.4), 4.0, 3.9, boxstyle="round,pad=0,rounding_size=0.15", fc="white", ec=GRAY, lw=1.2))
    ax.text(0.45, 3.95, "書類に書いてあること", fontsize=12, color=INK, weight="bold", va="center")
    ax.text(0.45, 3.45, "訪問介護計画", fontsize=10.5, color=INK2, va="center")
    ax.text(0.45, 3.1, "毎週 木・金曜日 10:00〜11:00", fontsize=11.5, color=INK, va="center")
    ax.text(0.45, 2.55, "9月17日(木)の記録", fontsize=10.5, color=INK2, va="center")
    ax.text(0.45, 2.2, "13:00〜14:00 に訪問", fontsize=11.5, color=INK, va="center")
    ax.add_patch(FancyBboxPatch((0.4, 0.55), 3.6, 1.3, boxstyle="round,pad=0,rounding_size=0.1", fc="#eef3fb", ec="none"))
    for j, t in enumerate(["特記事項: 本人の通院のため、", "本人とケアマネジャーの了承を得て、", "この日だけ時間を変更", "(提供票も変更済み)"]):
        ax.text(0.6, 1.6 - j * 0.3, t, fontsize=10.5, color=INK, va="center")
    # 右: AI の判定
    ax.text(4.6, 3.95, "AIの判定", fontsize=12, color=INK, weight="bold", va="center")
    ax.add_patch(FancyBboxPatch((4.5, 2.05), 3.9, 1.55, boxstyle="round,pad=0,rounding_size=0.12", fc="#fdeee6", ec=ORANGE, lw=1.5))
    ax.text(4.7, 3.3, "小さいAI(Haiku)", fontsize=10.5, color=INK2, va="center")
    for j, t in enumerate(["不備あり。「17日は時間を変えたが、", "訪問介護計画は10:00〜11:00の", "ままで、変更の記載がない」"]):
        ax.text(4.7, 2.95 - j * 0.3, t, fontsize=11, color=INK, va="center")
    ax.add_patch(FancyBboxPatch((4.5, 0.55), 3.9, 1.25, boxstyle="round,pad=0,rounding_size=0.12", fc="#eef3fb", ec=BLUE, lw=1.5))
    ax.text(4.7, 1.5, "中くらい(Sonnet)・大きい(Opus)", fontsize=10.5, color=INK2, va="center")
    ax.text(4.7, 1.1, "指摘なし", fontsize=11, color=INK, va="center")
    ax.text(0.2, 0.12, "架空の書類を点検させた結果。小さいAIの言葉は、要点を残して短くした", fontsize=9.5, color=INK2, va="center")
    fig.savefig(OUT / "7-ひっかけとAIの判定.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    fig_calendar()
    fig_results()
    fig_cards()
    fig_billing()
    fig_trap()
