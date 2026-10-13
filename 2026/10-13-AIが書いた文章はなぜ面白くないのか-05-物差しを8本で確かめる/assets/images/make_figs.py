"""記事の図2枚を作る。

値の出どころ:
- 答えの先出し率: ../labeling/graph-metrics.md の run1(AI Opus 5.5 の1回目の見分け)
- 転で驚いた割合、跳ね比、面白さの点: ../reader-metrics.md(AIの読者 Haiku 4.5、既読で外した回を除く8〜10回)
  転が2つある湯だまりの書き直しは、大きいほうの値
- 読みやすさの点、予想が外れた割合、納得の点: ../reader-metrics.md の「文書ごとの読後と読みやすさ」
- 役割と関連の数: ../labeling/role-counts.md(AI Opus 5.5 の1回目と2回目)。起承転結、問い、答え、先に明かすの8つ。棒は2回の平均、数字は「1回目/2回目」
配色は dataviz スキルの参照パレットの1番(青)と2番(橙)。validate_palette.js で検証済み
"""
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator

rcParams["font.family"] = "Hiragino Sans"
ORIG, REW = "#2a78d6", "#eb6834"
INK, SUB, GRID = "#0b0b0b", "#52514e", "#e4e3df"
PAIRS = ["コードは設計である", "科学者とあたま", "湯だまり", "竜巻(面白くない)"]


def panel(ax, title, note, orig, rew, xmax, fmt="{:.2f}", labels=PAIRS, notes=None, line=None):
    n = len(labels)
    y = range(n)
    h = 0.36
    for i in y:
        for v, dy, c in ((orig[i], -h / 2, ORIG), (rew[i], h / 2, REW)):
            ax.barh(i + dy, v, height=h - 0.06, color=c, zorder=2)
            txt = (notes or {}).get((i, c)) or fmt.format(v)
            ax.text(v + xmax * 0.015, i + dy, txt, va="center", fontsize=11, color=INK)
    if line:
        ax.axvline(line[0], color=SUB, lw=1.2, ls=(0, (4, 3)), zorder=3)
        ax.text(line[0] + xmax * 0.015, n - 0.55, line[1], fontsize=10, color=SUB, va="center")
    ax.set_yticks(list(y), labels, fontsize=12, color=INK)
    # y 軸は共有しているので、上から並べる反転は最初のパネルだけで行う
    if not ax.yaxis_inverted():
        ax.invert_yaxis()
    ax.set_xlim(0, xmax)
    ax.set_title(title, loc="left", fontsize=14, fontweight="bold", color=INK, pad=24)
    ax.text(0, 1.02, note, transform=ax.transAxes, fontsize=10.5, color=SUB, va="bottom")
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="x", colors=SUB, labelsize=10)
    ax.tick_params(axis="y", length=0)


def legend(fig):
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color=ORIG, label="人が書いた原文"), Patch(color=REW, label="AIの書き直し")],
               loc="upper right", ncol=2, frameon=False, fontsize=12, bbox_to_anchor=(0.98, 0.985))


# 図1: 2つの軸
fig, axes = plt.subplots(1, 2, figsize=(12, 5.6), dpi=150, sharey=True)
panel(axes[0], "構成の軸: 答えの先出し率", "答えや明かしを、問いや転より先に渡した割合。小さいほど答えを待たせる",
      [0.33, 0.00, 0.44, 0.00], [0.36, 0.83, 0.58, 0.50], 1.0)
panel(axes[1], "文の軸: 転で「驚いた」と答えた割合", "AIの読者が、転の文を「驚いた文」に挙げた回の割合",
      [0.80, 0.88, 1.00, 0.00], [0.20, 0.00, 0.90, 0.30], 1.0,
      notes={(3, ORIG): "転なし"})
fig.suptitle("2つの軸で見た4つの文章", x=0.02, ha="left", fontsize=17, fontweight="bold", color=INK)
legend(fig)
fig.text(0.02, 0.01, "答えの先出し率は AI(Opus 5.5)が見分けた文の役割から。驚いた割合は AIの読者(Haiku 4.5)各8〜10回",
         fontsize=9.5, color=SUB)
fig.tight_layout(rect=(0, 0.04, 1, 0.93))
fig.savefig("two-axes-result.png", facecolor="white")

# 図2: 文の軸の測り方3つ
P3 = PAIRS[:3]
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), dpi=150, sharey=True)
panel(axes[0], "跳ね比(予想の動き)", "転の段落の動き ÷ ふつうの段落の動き",
      [1.04, 0.46, 0.97], [0.22, 0.92, 0.78], 2.6, labels=P3, line=(2.0, "目安 2"))
panel(axes[1], "転で驚いた割合", "転を「驚いた文」に挙げた回の割合",
      [0.80, 0.88, 1.00], [0.20, 0.00, 0.90], 1.2, labels=P3)
panel(axes[2], "面白さの点(5段階)", "読み終えてAIが付けた点の平均",
      [4.40, 5.00, 4.56], [4.50, 4.60, 4.30], 5.6, fmt="{:.1f}", labels=P3)
axes[2].set_xticks(range(6))
fig.suptitle("文の軸の測り方3つ。3つの文章すべてで原文が上に出たのは、驚いた割合だけ", x=0.02, ha="left",
             fontsize=16, fontweight="bold", color=INK)
legend(fig)
fig.text(0.02, 0.01, "AIの読者(Haiku 4.5)各8〜10回。跳ね比は、どの転も目安の2に届かなかった", fontsize=9.5, color=SUB)
fig.tight_layout(rect=(0, 0.05, 1, 0.9))
fig.savefig("measures-compare.png", facecolor="white")


# 図3: 役割と関連の数(1次データ)
def panel_counts(ax, title, note, orig, rew, xmax, labels):
    n = len(labels)
    h = 0.36
    for i in range(n):
        for (a, b), dy, c in ((orig[i], -h / 2, ORIG), (rew[i], h / 2, REW)):
            v = (a + b) / 2
            ax.barh(i + dy, v, height=h - 0.06, color=c, zorder=2)
            ax.text(v + xmax * 0.02, i + dy, f"{a}/{b}", va="center", fontsize=11, color=INK)
    ax.set_yticks(list(range(n)), labels, fontsize=12, color=INK)
    if not ax.yaxis_inverted():
        ax.invert_yaxis()
    ax.set_xlim(0, xmax)
    ax.set_title(title, loc="left", fontsize=14, fontweight="bold", color=INK, pad=24)
    ax.text(0, 1.02, note, transform=ax.transAxes, fontsize=10.5, color=SUB, va="bottom")
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="x", colors=SUB, labelsize=10)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))


LAB = ["コードは設計である\n(47文 / 80文)", "科学者とあたま\n(86文 / 118文)",
       "湯だまり\n(110文 / 94文)", "竜巻(面白くない)\n(10文 / 18文)"]
# (原文の1回目,2回目), (書き直しの1回目,2回目)。順は A, B, D, C
COUNTS = [
    ("起", "予想を持たせ始める文", [(2, 5), (1, 2), (6, 2), (1, 0)], [(4, 3), (11, 9), (4, 3), (0, 0)]),
    ("承", "転の前に予想を強める文", [(9, 11), (1, 2), (8, 10), (0, 0)], [(1, 1), (12, 9), (6, 9), (0, 0)]),
    ("転(全体)", "文章全体の大きな転", [(1, 1), (1, 1), (1, 2), (0, 1)], [(1, 1), (1, 1), (2, 2), (1, 1)]),
    ("転(内側)", "途中の小さな転", [(2, 2), (3, 1), (3, 2), (1, 0)], [(3, 2), (11, 12), (6, 4), (1, 1)]),
    ("結", "転に納得できる理由を渡す文", [(20, 13), (74, 64), (9, 7), (1, 1)], [(22, 24), (27, 27), (9, 11), (4, 5)]),
    ("問い", "答えを求める問いの文", [(4, 5), (6, 4), (8, 8), (0, 0)], [(7, 11), (2, 6), (7, 5), (1, 0)]),
    ("答え", "問いへの答えが完結する文", [(7, 6), (6, 4), (5, 4), (1, 1)], [(7, 10), (2, 5), (4, 4), (2, 0)]),
    ("先に明かす", "題や見出しが、後の転や答えを先に言う", [(2, 2), (0, 0), (4, 4), (0, 0)], [(4, 5), (10, 10), (7, 6), (2, 2)]),
]
fig, axes = plt.subplots(2, 4, figsize=(16, 9.6), dpi=150, sharey=True)
for ax, (name, note, o, r) in zip(axes.flat, COUNTS):
    xmax = max(max(a, b) for a, b in o + r) * 1.45 + 1
    panel_counts(ax, name, note, o, r, xmax, LAB)
fig.suptitle("AIが見分けた文の役割の数。全体の転は残り、承と「先に明かす」が大きく変わった", x=0.02, ha="left",
             fontsize=16, fontweight="bold", color=INK)
legend(fig)
fig.text(0.02, 0.01, "AI(Opus 5.5)が同じ指示で2回見分けた。棒は2回の平均、数字は「1回目/2回目」。役割は読み終えた後の役割。行の見出しの文の数は「原文 / 書き直し」",
         fontsize=9.5, color=SUB)
fig.tight_layout(rect=(0, 0.03, 1, 0.94), h_pad=3)
fig.savefig("role-counts.png", facecolor="white")


# 図4: 定義の部分ごとの比べ
fig, axes = plt.subplots(1, 4, figsize=(15, 5.2), dpi=150, sharey=True)
panel(axes[0], "読みやすさ", "読み終えてAIが付けた点(5段階)",
      [4.75, 3.12, 4.44, 4.11], [4.60, 4.50, 4.50, 4.70], 5.9, fmt="{:.1f}")
axes[0].set_xticks(range(6))
panel(axes[1], "面白さ: 予想が外れた", "予想が一部でも外れたと答えた割合",
      [0.70, 1.00, 0.67, 0.89], [0.40, 0.60, 0.70, 0.40], 1.25)
panel(axes[2], "面白さ: 転で驚いた", "転の文を「驚いた文」に挙げた割合",
      [0.80, 0.88, 1.00, 0.00], [0.20, 0.00, 0.90, 0.30], 1.25, notes={(3, ORIG): "転なし"})
panel(axes[3], "面白さ: 納得した", "外れ方に納得したかの点(5段階)",
      [4.10, 4.38, 4.56, 3.56], [4.40, 4.50, 4.20, 4.50], 5.9, fmt="{:.1f}")
axes[3].set_xticks(range(6))
axes[1].set_xticks([0, 0.5, 1])
axes[2].set_xticks([0, 0.5, 1])
for ax in axes:
    ax.set_yticks(range(4), ["コードは設計である", "科学者とあたま", "湯だまり", "竜巻(面白くない)"], fontsize=12)
fig.suptitle("書き直しは、読みやすさと納得を保ち、「予想が外れる」「驚く」で下がった", x=0.02, ha="left",
             fontsize=16, fontweight="bold", color=INK)
legend(fig)
fig.text(0.02, 0.01, "AIの読者(Haiku 4.5)各8〜10回の平均。湯だまりは、どの部分でも差が小さい",
         fontsize=9.5, color=SUB)
fig.tight_layout(rect=(0, 0.05, 1, 0.9))
fig.savefig("definition-parts.png", facecolor="white")
