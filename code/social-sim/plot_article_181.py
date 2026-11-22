"""#181 記事のルール説明図(rules.png, delay-cost.png)。使い方: uv run --with matplotlib python plot_article_181.py <出力フォルダ>"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import os
for w in ("W3", "W6"):
    font_manager.fontManager.addfont(f"/System/Library/Fonts/ヒラギノ角ゴシック {w}.ttc")
plt.rcParams["font.family"] = "Hiragino Sans"
INK, MUTED, LINE = "#1d1d1f", "#6b6b70", "#d9d6cc"
BUYER, SELLER, LAND, OK, NG, BG = "#2f6db5", "#b8732a", "#8fbf6a", "#1f7a4d", "#b3261e", "#f6f4ee"
out = sys.argv[1]

def person(ax, x, y, r, color, mark, name, sub=None):
    ax.add_patch(Circle((x, y), r, color=color))
    ax.text(x, y, mark, color="white", ha="center", va="center", fontsize=20, weight="bold")
    ax.text(x, y - r - 0.25, name, ha="center", va="top", fontsize=13, weight="bold", color=INK)
    if sub:
        ax.text(x, y - r - 0.62, sub, ha="center", va="top", fontsize=10.5, color=MUTED)

def rbox(ax, x, y, w, h, fc, ec="none", r=0.15):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=1))

def arrow(ax, a, b, color, both=False):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="<|-|>" if both else "-|>", mutation_scale=16, color=color, lw=2))

# ---- 図1: ルール ----
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=150)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(-0.2, 6.2); ax.axis("off")
ax.text(0.3, 5.85, "ゲームのルール", fontsize=17, weight="bold", color=INK, va="top")
person(ax, 1.6, 3.6, 0.65, BUYER, "買", "買い手", "土地をまとめたい")
for i, y in enumerate([4.6, 2.6]):
    rbox(ax, 6.0, y - 0.45, 0.9, 0.9, LAND, r=0.08)
    ax.text(6.45, y, f"土地{i+1}", color="white", ha="center", va="center", fontsize=12, weight="bold")
    person(ax, 7.75, y, 0.42, SELLER, "売", f"売り手{i+1}")
    arrow(ax, (2.35, 3.6 + (0.35 if i == 0 else -0.35)), (5.9, y), MUTED, both=True)
    ax.text(4.1, (3.6 + y) / 2 + (0.32 if i == 0 else -0.32), "値段を出す ⇄ 応じる・断る", ha="center", va="center", fontsize=10.5, color=MUTED,
            rotation=13 if i == 0 else -13)
ax.text(1.6, 1.75, "2つとも買えたら\n90ドルの価値\n(1つだけなら0)", ha="center", va="top", fontsize=11.5, color=BUYER, weight="bold")
ax.text(9.25, 3.6, "手放すと\n30ドルの費用", ha="center", va="center", fontsize=11.5, color=SELLER, weight="bold")
# 例
rbox(ax, 3.2, -0.15, 6.6, 1.6, "white", ec=LINE)
ax.text(3.4, 1.28, "例: 2人とも40ドルで売った場合の稼ぎ", fontsize=11.5, weight="bold", color=INK, va="top")
ax.text(3.4, 0.86, "買い手  90 − 40 − 40 = 10ドル", fontsize=11, color=BUYER, va="top")
ax.text(6.6, 0.86, "売り手  40 − 30 = 10ドルずつ", fontsize=11, color=SELLER, va="top")
ax.text(3.4, 0.5, "3人で分けられるのは、いつも合計30ドル(90ドル − 費用30ドル×2人)", fontsize=10, color=MUTED, va="top")
ax.text(3.4, 0.17, "10ターンのうちに2つともまとまらなければ、3人とも0ドル", fontsize=10, color=MUTED, va="top")
fig.savefig(f"{out}/rules.png", bbox_inches="tight", facecolor=BG); plt.close(fig)

# ---- 図2: 遅れの損 ----
fig, ax = plt.subplots(figsize=(10, 6.4), dpi=150)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 6.4); ax.axis("off")
ax.text(0.3, 6.15, "「遅れの損」: 誰かが1回断るたびに、3人全員の稼ぎが5%ずつ減る", fontsize=15, weight="bold", color=INK, va="top")
ax.text(0.3, 5.7, "例: 買い手が2人に40ドルずつ出し続けた場合", fontsize=11.5, color=MUTED, va="top")
rows = [
    ("1ターン目", [("売り手1", "断る", NG), ("売り手2", "断る", NG)], 2, 0.90),
    ("2ターン目", [("売り手1", "売る", OK), ("売り手2", "断る", NG)], 3, 0.85),
    ("3ターン目", [("売り手1", "売った後", MUTED), ("売り手2", "売る", OK)], 3, 0.85),
]
ax.text(6.2, 5.25, "断った回数の合計", fontsize=10.5, color=MUTED, ha="center")
ax.text(8.25, 5.25, "最後に受け取れる割合", fontsize=10.5, color=MUTED, ha="center")
for k, (turn, acts, rej, m) in enumerate(rows):
    y = 4.6 - k * 1.0
    rbox(ax, 0.3, y - 0.38, 9.4, 0.76, "white", ec=LINE)
    ax.text(0.55, y, turn, fontsize=12.5, weight="bold", color=INK, va="center")
    for j, (who, act, c) in enumerate(acts):
        x = 1.95 + j * 2.0
        ax.text(x, y, f"{who}:", fontsize=11, color=SELLER, va="center")
        ax.text(x + 0.82, y, act, fontsize=11.5, color=c, va="center", weight="bold")
    ax.text(6.2, y, f"{rej}回", fontsize=13, color=INK, ha="center", va="center", weight="bold")
    # 割合バー
    ax.add_patch(FancyBboxPatch((7.2, y - 0.1), 1.8, 0.2, boxstyle="round,pad=0,rounding_size=0.08", fc=LINE, ec="none"))
    ax.add_patch(FancyBboxPatch((7.2, y - 0.1), 1.8 * m, 0.2, boxstyle="round,pad=0,rounding_size=0.08", fc=NG, ec="none"))
    ax.text(9.5, y, f"{round(m*100)}%", fontsize=12, color=INK, ha="right", va="center", weight="bold") if False else None
    ax.text(9.55, y, f"{round(m*100)}%", fontsize=12.5, color=INK, ha="right", va="center", weight="bold")
rbox(ax, 0.3, 0.25, 9.4, 1.35, "white", ec=LINE)
ax.text(0.55, 1.42, "結果: まとまった値段は40ドルずつだが、3回断ったので、全員の稼ぎが15%減る", fontsize=11.5, weight="bold", color=INK, va="top")
ax.text(0.55, 1.0, "買い手  10ドル × 85% = 8.5ドル", fontsize=11, color=BUYER, va="top")
ax.text(4.0, 1.0, "売り手  10ドル × 85% = 8.5ドルずつ", fontsize=11, color=SELLER, va="top")
ax.text(0.55, 0.62, "断ったのが売り手でも、買い手を含む3人全員が減る。1ターン目で決まれば、3人とも10ドルのまま", fontsize=10, color=MUTED, va="top")
fig.savefig(f"{out}/delay-cost.png", bbox_inches="tight", facecolor=BG); plt.close(fig)
print("ok")


# ================= 結果の図(dataviz の手順: 色は役割で固定、値は直接書く) =================
import numpy as np
C_HUMAN, C_AI, C_RULE = "#e87ba4", "#eda100", "#1baf7a"   # 人間 / AIだけ / AI+プログラム(全図で固定)
GRID = "#e6e4dc"
CONDS = ["買い手が出す\n損なし", "買い手が出す\n損あり", "売り手が出す\n損なし", "売り手が出す\n損あり"]


def base_ax(fig, ax, title, sub=None):
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(colors=MUTED, length=0, labelsize=11)
    fig.text(0.04, 0.97, title, fontsize=15, weight="bold", color=INK, va="top")
    if sub:
        fig.text(0.04, 0.905, sub, fontsize=10.5, color=MUTED, va="top")


def legend(fig, items, y=0.84):
    x = 0.04
    for label, c in items:
        fig.patches.append(FancyBboxPatch((x, y - 0.012), 0.018, 0.03, boxstyle="round,pad=0,rounding_size=0.004",
                                          transform=fig.transFigure, fc=c, ec="none"))
        fig.text(x + 0.025, y + 0.003, label, fontsize=11, color=INK, va="center")
        x += 0.03 + 0.0145 * len(label) + 0.03


def grouped(ax, groups, series, vals, colors, fmt="{:.1f}", width=0.26):
    x = np.arange(len(groups))
    n = len(series)
    for k in range(n):
        xs = x + (k - (n - 1) / 2) * (width + 0.03)
        ax.bar(xs, vals[k], width, color=colors[k], zorder=3)
        for xi, v in zip(xs, vals[k]):
            ax.text(xi, v + max(max(r) for r in vals) * 0.015, fmt.format(v), ha="center", va="bottom", fontsize=10.5, color=INK)
    ax.set_xticks(x, groups)
    ax.yaxis.grid(True, color=GRID, zorder=0); ax.set_axisbelow(True)


# 図3: 断った回数
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=150)
base_ax(fig, ax, "1組あたりの断った回数(10ターンの交渉)", "AIだけ: 各10組。AI+プログラム: 各30組。人間: Cadigan ほか(2009)")
legend(fig, [("人間", C_HUMAN), ("AIだけ", C_AI), ("AI+プログラム(断る判断)", C_RULE)])
grouped(ax, CONDS, ["人間", "AIだけ", "AI+プログラム"],
        [[10.8, 2.9, 11.0, 3.3], [0.8, 1.1, 1.6, 1.4], [10.1, 4.4, 9.9, 4.1]], [C_HUMAN, C_AI, C_RULE])
ax.set_ylabel("回", color=MUTED, rotation=0, labelpad=12); ax.set_ylim(0, 13)
fig.subplots_adjust(top=0.78, bottom=0.14, left=0.07, right=0.98)
fig.savefig(f"{out}/rejections.png", facecolor=BG); plt.close(fig)

# 図4: プログラムの仕組み(具体例)
fig, ax = plt.subplots(figsize=(10, 3.9), dpi=150)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG); ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis("off")
ax.text(0.3, 4.4, "値段を示された側の判断を、AIの予想とプログラムに分けた", fontsize=15, weight="bold", color=INK, va="top")
ax.text(0.3, 3.95, "例: 遅れの損がある条件で、1ターン目に35ドルを示された売り手", fontsize=11, color=MUTED, va="top")
steps = [
    ("① AIが予想を書く", "「断れば、次のターンに\n買い手は40ドルを出す」", SELLER),
    ("② プログラムが計算する", "断ったときに増える稼ぎ\n(40−30)×95% − (35−30)\n= 4.5ドル", BUYER),
    ("③ しきい値と比べる", "4.5ドル > しきい値1ドル\n→ 断る", NG),
]
for i, (h, body, c) in enumerate(steps):
    x = 0.3 + i * 3.25
    rbox(ax, x, 0.75, 2.95, 2.6, "white", ec=LINE)
    ax.text(x + 0.2, 3.1, h, fontsize=12.5, weight="bold", color=c, va="top")
    ax.text(x + 0.2, 2.45, body, fontsize=12, color=INK, va="top", linespacing=1.6)
    if i < 2:
        arrow(ax, (x + 3.0, 2.05), (x + 3.22, 2.05), MUTED)
ax.text(0.3, 0.3, "しきい値は人ごとにくじで決める(平均1ドル)。最後の10ターン目は次がないので、AI自身の答えをそのまま使う", fontsize=10, color=MUTED, va="bottom")
fig.savefig(f"{out}/rule-mechanism.png", bbox_inches="tight", facecolor=BG); plt.close(fig)

# 図5: 30ドルの分け方(買い手 / 売り手1 / 売り手2)
rows = [  # (条件, [(見出し, 買い手, 売り手1, 売り手2)])
    ("買い手が出す・損なし", [("人間", 10.55, 9.72, 9.72), ("AI+プログラム(断る判断)", 1.1, 14.9, 14.0), ("AI+譲る幅も抑える", 9.4, 11.3, 9.3)]),
    ("買い手が出す・損あり", [("人間", 11.12, 7.24, 7.24), ("AI+プログラム(断る判断)", 3.3, 10.2, 9.8), ("AI+譲る幅も抑える", 12.2, 5.3, 5.1)]),
    ("売り手が出す・損なし", [("人間", 10.43, 9.28, 9.28), ("AI+プログラム(断る判断)", 22.7, 4.0, 3.3), ("AI+譲る幅も抑える", 6.4, 11.4, 12.2)]),
    ("売り手が出す・損あり", [("人間", 9.39, 7.80, 7.80), ("AI+プログラム(断る判断)", 15.0, 4.8, 4.2), ("AI+譲る幅も抑える", 4.1, 8.3, 8.6)]),
]
fig, ax = plt.subplots(figsize=(10, 8.2), dpi=150)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.text(0.04, 0.99, "3人の稼ぎの分け方(平均、ドル)", fontsize=15, weight="bold", color=INK, va="top")
fig.text(0.04, 0.955, "棒の長さの合計が、3人で分けた額。遅れの損があると30ドルより短くなる。人間の売り手は、論文の1人あたりの平均", fontsize=10, color=MUTED, va="top")
legend(fig, [("買い手", BUYER), ("売り手1", SELLER), ("売り手2", "#dcae7e")], y=0.918)
y = 0; yt, yl = [], []
for cond, items in rows:
    ax.text(-0.3, y - 0.15, cond, fontsize=12, weight="bold", color=INK, ha="left", va="bottom")
    y -= 0.55
    for name, b, s1, s2 in items:
        left = 0
        for v, c in ((b, BUYER), (s1, SELLER), (s2, "#dcae7e")):
            ax.barh(y, v - 0.15, left=left, height=0.5, color=c, zorder=3)
            if v >= 2.5:
                ax.text(left + (v - 0.15) / 2, y, f"{v:.1f}", ha="center", va="center", fontsize=10, color="white" if c != "#dcae7e" else INK)
            left += v
        yt.append(y); yl.append(name)
        y -= 0.62
    y -= 0.35
ax.set_yticks(yt, yl); ax.tick_params(axis="y", colors=INK, labelsize=10.5, length=0)
ax.set_xlim(-0.3, 31); ax.xaxis.grid(True, color=GRID, zorder=0); ax.set_axisbelow(True)
ax.axvline(30, color=MUTED, lw=1, ls=(0, (3, 3)), zorder=2)
ax.text(30, 0.25, "30ドル", ha="center", fontsize=9.5, color=MUTED)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(LINE); ax.tick_params(axis="x", colors=MUTED, length=0)
fig.subplots_adjust(top=0.875, bottom=0.05, left=0.22, right=0.97)
fig.savefig(f"{out}/payoffs.png", facecolor=BG); plt.close(fig)

# 図6: 粘った人の得と、断られた直後の譲り幅
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 5), dpi=150, gridspec_kw={"width_ratios": [2.2, 1]})
fig.patch.set_facecolor(BG)
for a in (a1, a2):
    a.set_facecolor(BG)
    for sp in ("top", "right", "left"):
        a.spines[sp].set_visible(False)
    a.spines["bottom"].set_color(LINE); a.tick_params(colors=MUTED, length=0, labelsize=10.5)
fig.text(0.04, 0.97, "AIどうしの交渉では、粘るほうが人間より大きく得をした", fontsize=15, weight="bold", color=INK, va="top")
legend(fig, [("人間", C_HUMAN), ("AI+プログラム(断る判断)", C_RULE)], y=0.875)
grouped(a1, CONDS, ["人間", "AI"], [[5.4, 1.4, 13.9, 7.7], [10.7, 4.9, 28.9, 12.0]], [C_HUMAN, C_RULE], width=0.34)
a1.set_title("値段を示された側が粘って増やした稼ぎ(ドル)\n最終の稼ぎ − 1ターン目の値段どおりの稼ぎ", fontsize=10.5, color=MUTED, loc="left")
a1.tick_params(axis="x", labelsize=9.5)
grouped(a2, ["買い手が出す\n損なし", "買い手が出す\n損あり"], ["人間", "AI"], [[2, 1.75], [5.8, 4.3]], [C_HUMAN, C_RULE], width=0.34)
a2.set_title("1回断られた直後に\n買い手が上げた額(ドル)", fontsize=10.5, color=MUTED, loc="left")
a2.tick_params(axis="x", labelsize=9.5)
fig.text(0.04, 0.02, "人間の右の値は、論文の図3を目で読んだおよその値", fontsize=9.5, color=MUTED)
fig.subplots_adjust(top=0.72, bottom=0.17, left=0.04, right=0.98, wspace=0.12)
for a in (a1, a2):
    a.set_yticks([])
fig.savefig(f"{out}/holdout-gain.png", facecolor=BG); plt.close(fig)

# 図7: 1回きり。AIが書いた不公平さと、断った割合
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.8), dpi=150, gridspec_kw={"width_ratios": [1.3, 1]})
fig.patch.set_facecolor(BG)
for a in (a1, a2):
    a.set_facecolor(BG)
    for sp in ("top", "right", "left"):
        a.spines[sp].set_visible(False)
    a.spines["bottom"].set_color(LINE); a.tick_params(colors=MUTED, length=0, labelsize=10.5); a.set_yticks([])
fig.text(0.04, 0.97, "1回きりの交渉: AIは不公平を感じても、それだけでは断らなかった", fontsize=15, weight="bold", color=INK, va="top")
xs = ["31ドル", "33ドル", "35ドル", "40ドル"]; uf = [70, 60, 50, 23]
a1.bar(xs, uf, 0.5, color=C_AI, zorder=3)
for i, v in enumerate(uf):
    a1.text(i, v + 1.5, str(v), ha="center", fontsize=11, color=INK)
a1.set_title("買い手が示した値段ごとの、売り手のAIが書いた\n不公平さ(0〜100、平均)", fontsize=10.5, color=MUTED, loc="left")
a1.set_ylim(0, 85)
legend(fig, [("人間", C_HUMAN), ("AIだけ", C_AI), ("AI+プログラム", C_RULE)], y=0.84)
grouped(a2, ["買い手が出す\n(合わせた)", "売り手が出す\n(確かめ)"], ["人間", "AIだけ", "AI+プログラム"],
        [[25.9, 15.4], [0, 0], [25.8, 5.0]], [C_HUMAN, C_AI, C_RULE], fmt="{:.1f}%", width=0.24)
a2.set_title("値段を断った割合", fontsize=10.5, color=MUTED, loc="left"); a2.set_yticks([]); a2.set_ylim(0, 32)
fig.subplots_adjust(top=0.66, bottom=0.13, left=0.04, right=0.98, wspace=0.1)
fig.savefig(f"{out}/one-shot.png", facecolor=BG); plt.close(fig)
print("ok2")
