"""note の記事(article.md)の図を作る。数字は log.md と、親テーマの下調べ(drafts/訪問介護の困りごとをAIで解く/assets/03)から写した。
使い方: uv run --with matplotlib python src/make_figures.py <出力フォルダ>
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "Hiragino Sans", "font.size": 13, "axes.edgecolor": "#c3c2b7",
    "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#0b0b0b",
    "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
})
BLUE, ORANGE, GRAY, LIGHT, INK, SUB = "#2a78d6", "#eb6834", "#b9b8b2", "#a9c7ee", "#0b0b0b", "#52514e"


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def title(ax, t, sub=None):
    ax.set_title(t, loc="left", fontsize=16, fontweight="bold", color=INK, pad=28 if sub else 12)
    if sub:
        ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=11, color=SUB, va="bottom")


def hbar(name, labels, values, t, sub=None, hi=(), fmt="{:.2f}", xmax=None, ref=None, width=8, note=None):
    """横棒。hi に入れた行だけ青、ほかは灰色。値は棒の右に書く。"""
    fig, ax = plt.subplots(figsize=(width, 0.55 * len(labels) + 1.6))
    y = range(len(labels))[::-1]
    ax.barh(list(y), values, color=[BLUE if l in hi else GRAY for l in labels], height=0.6)
    for yi, v in zip(y, values):
        ax.text(v + (xmax or max(values)) * 0.01, yi, fmt.format(v), va="center", fontsize=12, color=INK)
    ax.set_yticks(list(y), labels)
    ax.set_xlim(0, xmax or max(values) * 1.15)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e6e5e0", linewidth=0.8)
    ax.set_axisbelow(True)
    if ref:
        ax.axvline(ref[0], color=SUB, linestyle="--", linewidth=1)
        ax.text(ref[0], len(labels) - 0.4, ref[1], fontsize=10, color=SUB, ha="center")
    title(ax, t, sub)
    if note:
        fig.text(0.01, -0.02, note, fontsize=9, color=SUB, ha="left", va="top")
    save(fig, name)


def box(ax, x, y, w, h, text, fc="#ffffff", ec=GRAY, color=INK, size=12, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=color,
            fontweight="bold" if bold else "normal", linespacing=1.5)


def arrow(ax, a, b, color=SUB):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16, color=color, lw=1.4))


# 1. 訪問介護の仕事の流れと、つまずく場所
fig, ax = plt.subplots(figsize=(12, 4.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis("off")
steps = [("相談・契約", "ケアマネ、サ責\n利用者・家族", "できること・\nできないことが\n伝わらない"),
         ("計画", "サービス提供\n責任者(サ責)", "予定を変えても\n計画を直し忘れる"),
         ("訪問", "ヘルパー", "急な休みで\nシフトが崩れる\nハラスメント"),
         ("記録", "ヘルパー、サ責", "合間に急いで書き\n要件が欠ける"),
         ("請求", "請求事務\nケアマネ", "FAXと画面を\n見比べて\n誤りが残る")]
for i, (s, who, pain) in enumerate(steps):
    x = 0.1 + i * 2
    box(ax, x, 3.3, 1.75, 0.8, s, fc="#e8f0fb", ec=BLUE, size=14, bold=True)
    ax.text(x + 0.875, 2.85, who, ha="center", va="center", fontsize=10.5, color=SUB, linespacing=1.4)
    box(ax, x, 0.55, 1.75, 1.6, pain, fc="#fdf0ea", ec=ORANGE, size=11.5)
    if i < 4:
        arrow(ax, (x + 1.78, 3.7), (x + 2.07, 3.7))
ax.text(0.1, 0.12, "数年に1回の運営指導(行政の点検)で、書類どうしの食い違いが見つかると、さかのぼって報酬を返す", fontsize=11, color=INK)
ax.text(0.1, 4.45, "訪問介護の1か月の流れと、つまずく場所", fontsize=16, fontweight="bold", color=INK)
save(fig, "fig01-flow.png")

# 2. 有効求人倍率
hbar("fig02-jobs.png", ["訪問介護職員", "全職業の平均"], [15.53, 1.28],
     "訪問介護の求人倍率は15.53倍", "1人の求職者を、15社が取り合っている(2022年度、有効求人倍率)",
     hi=("訪問介護職員",), width=8, note="出典: 厚生労働省の統計をもとにした各社のまとめ。全職業は1.28倍")

# 3. ハラスメント
fig, ax = plt.subplots(figsize=(8.5, 3.4))
items = [("利用者本人からハラスメントを\n受けたことがある訪問介護職員", 50.0),
         ("ハラスメントの原因が「サービスの\n範囲が伝わっていない」だった割合", 43.0),
         ("相談窓口がない訪問介護員", 43.2)]
y = range(len(items))[::-1]
ax.barh(list(y), [100] * 3, color="#eeede8", height=0.55)
ax.barh(list(y), [v for _, v in items], color=BLUE, height=0.55)
for yi, (_, v) in zip(y, items):
    ax.text(v + 1.5, yi, f"{v:g}%", va="center", fontsize=13, color=INK, fontweight="bold")
ax.set_yticks(list(y), [l for l, _ in items], fontsize=11.5)
ax.set_xlim(0, 100); ax.set_xticks([]); ax.tick_params(axis="y", length=0)
ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
title(ax, "1人で家に入る仕事のリスク", "厚生労働省(平成30年度)、介護労働安定センター(令和4年度)の調査")
save(fig, "fig03-harassment.png")

# 4. 困りごとの連鎖
fig, ax = plt.subplots(figsize=(12, 5.2))
ax.set_xlim(0, 12); ax.set_ylim(0, 5.2); ax.axis("off")
ax.text(0.1, 5.15, "困りごとは、人手不足から書類の食い違いへ連なっている", fontsize=16, fontweight="bold", color=INK, va="top")
ax.text(0.1, 4.45, "現場の困りごと", fontsize=12, color=ORANGE, fontweight="bold")
ax.text(7.3, 4.45, "その結果、点検で見つかる困りごと", fontsize=12, color=BLUE, fontweight="bold")
box(ax, 0.1, 3.0, 2.0, 1.1, "人が採れない\n(求人倍率15倍)", fc="#fdf0ea", ec=ORANGE)
box(ax, 2.6, 3.0, 2.0, 1.1, "シフトが\n毎日崩れる", fc="#fdf0ea", ec=ORANGE)
box(ax, 5.1, 3.0, 1.8, 1.1, "予定を\n急に変える", fc="#fdf0ea", ec=ORANGE)
box(ax, 7.3, 3.4, 2.1, 0.8, "計画の直し忘れ", fc="#e8f0fb", ec=BLUE)
box(ax, 7.3, 2.45, 2.1, 0.8, "記録が雑になる", fc="#e8f0fb", ec=BLUE)
box(ax, 7.3, 1.5, 2.1, 0.8, "請求の誤り", fc="#e8f0fb", ec=BLUE)
box(ax, 9.9, 2.2, 2.0, 1.4, "運営指導で\n見つかり\n報酬を返す", fc=BLUE, ec=BLUE, color="#ffffff", bold=True)
arrow(ax, (2.12, 3.55), (2.58, 3.55)); arrow(ax, (4.62, 3.55), (5.08, 3.55))
for yy in (3.8, 2.85, 1.9):
    arrow(ax, (6.92, 3.55), (7.28, yy))
    arrow(ax, (9.42, yy), (9.88, 2.9))
box(ax, 0.1, 0.9, 2.0, 1.1, "移動・待機の時間に\n賃金が出ない", fc="#ffffff", ec=ORANGE, size=11)
box(ax, 2.6, 0.9, 2.0, 1.1, "利用者や家族からの\nハラスメント", fc="#ffffff", ec=ORANGE, size=11)
arrow(ax, (1.1, 2.02), (1.1, 2.98)); arrow(ax, (3.6, 2.02), (1.6, 2.98))
ax.text(3.05, 2.45, "辞める理由になる", fontsize=10, color=SUB)
ax.text(0.1, 0.3, "返還は過去にさかのぼるので、見つかるのが遅いほど額が大きくなる", fontsize=11, color=INK)
save(fig, "fig04-chain.png")

# 5. 立場ごとの困りごとの数
roles = ["サービス提供責任者", "ヘルパー", "経営者", "管理者", "請求事務", "経理", "総務・人事", "ケアマネジャー", "利用者", "家族"]
counts = [6, 6, 5, 5, 4, 3, 3, 3, 2, 2]
hbar("fig05-roles.png", roles, counts, "困りごとが集まるのは、サ責とヘルパー",
     "立場ごとに洗い出した困りごとの数(公開資料から整理)", hi=("サービス提供責任者", "ヘルパー"), fmt="{:d}", xmax=7.2)

# 6. 情報源
hbar("fig06-sources.png", ["厚労省 Q&A集", "告示・省令・通知(6本)", "介護保険法(3章)", "老計10号"],
     [3682, 2421, 917, 28], "AIに読ませた資料(7,048件に分けた)", "どれも無料で公開されている公的な文書",
     hi=("厚労省 Q&A集", "告示・省令・通知(6本)"), fmt="{:,}件", xmax=4400)

# 6b. ルールの階層
fig, ax = plt.subplots(figsize=(12, 6.2))
ax.set_xlim(0, 12); ax.set_ylim(0, 6.2); ax.axis("off")
ax.text(0.1, 6.05, "介護報酬のルールは、4つの段に分かれている", fontsize=16, fontweight="bold", color=INK, va="top")
rows = [("法律", "介護保険法", "制度の大枠。誰が、どんなサービスを使えるか", "国会"),
        ("告示・省令", "告示19号・94号・95号\n省令37号", "何が何単位か。加算の要件。事業所が守る運営基準", "大臣"),
        ("通知", "老企25号・36号\n老計10号", "告示と省令の読み方。算定の細かい決まり", "厚労省の担当課"),
        ("Q&A", "介護サービス関係Q&A集\n(3,722問)", "現場から寄せられた問いへの回答", "厚労省の担当課")]
for i, (lv, names, what, who) in enumerate(rows):
    y = 4.55 - i * 1.25
    indent = i * 0.35
    box(ax, 0.1 + indent, y, 1.7, 1.0, lv, fc="#e8f0fb", ec=BLUE, size=14, bold=True)
    box(ax, 2.0 + indent, y, 3.0, 1.0, names, fc="#ffffff", ec=GRAY, size=12)
    ax.text(5.25 + indent, y + 0.62, what, fontsize=12, color=INK, va="center")
    ax.text(5.25 + indent, y + 0.27, f"出すところ: {who}", fontsize=10.5, color=SUB, va="center")
ax.annotate("", xy=(11.6, 0.4), xytext=(11.6, 5.5), arrowprops=dict(arrowstyle="-|>", color=SUB, lw=1.4))
ax.text(11.45, 2.95, "下ほど細かく\n数も多い", fontsize=11, color=SUB, ha="right", va="center", linespacing=1.5)
save(fig, "fig06b-layers.png")

# 7. 検索のやり方ごとの点(B 根拠を探す問題、再現率)
hbar("fig07-search.png",
     ["キーワード(BM25)", "意味の近さ(ベクトル)", "両方を混ぜる", "見出しを足す", "AIに仮の答えを書かせる(HyDE)",
      "AIに説明を書き足させる(Contextual)", "混ぜる + 並べ直し(リランカー)"],
     [0.59, 0.66, 0.59, 0.74, 0.73, 0.65, 0.74], "効いたのは、地味な「並べ直し」と「見出し」",
     "根拠を探す問題で、正解の根拠を上位10件にどれだけ拾えたか(再現率)", hi=("混ぜる + 並べ直し(リランカー)", "見出しを足す"), xmax=0.9)

# 7b. 検索の具体例(言い換え問題 QA0741)。上位3件を方式ごとに並べる
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.set_xlim(0, 12); ax.set_ylim(0, 7.2); ax.axis("off")
ax.text(0.1, 7.1, "同じ問いでも、探し方で上位に来る資料が変わる", fontsize=16, fontweight="bold", color=INK, va="top")
ax.text(0.1, 6.55, "問い「1日2回入るとき、間は2時間くらい空ければいいと聞いた。その『くらい』はどの程度まで許される?」",
        fontsize=11.5, color=SUB, va="top")
OK = "正解(訪問介護)\n「概ね2時間」の幅は"
YA, TE = "夜間対応型\n一晩に複数回の訪問", "定期巡回\n一晩に複数回の訪問"
TK = "定期巡回\n2時間の間隔は要るか"
res = [("キーワード(BM25)", [YA, TE, TK], None, "正解は30位以内になし"),
       ("意味の近さ(ベクトル)", ["訪問介護\n2時間未満の間隔の数え方", "訪問介護\n看取り期の2時間ルール", OK], 2, "正解は3位"),
       ("混ぜる(ハイブリッド)", [TK, TE, YA], None, "正解は4位"),
       ("混ぜる + 並べ直し", [OK, "訪問介護\n複数の事業所が入るとき", TE], 0, "正解は1位")]
for i, (name, items, hit, note) in enumerate(res):
    y = 5.0 - i * 1.4
    ax.text(0.1, y + 0.66, name, fontsize=13, fontweight="bold", color=INK, va="center")
    ax.text(0.1, y + 0.26, note, fontsize=11, color=BLUE if hit == 0 else SUB, va="center")
    for j, it in enumerate(items):
        x = 3.5 + j * 2.85
        good = hit == j
        ax.text(x - 0.05, y + 0.48, f"{j + 1}", fontsize=11, color=SUB, ha="right", va="center")
        box(ax, x, y + 0.05, 2.6, 0.9, it, fc="#e8f0fb" if good else "#ffffff", ec=BLUE if good else GRAY, size=10.5, bold=good)
ax.text(0.1, 0.12, "Q&A の上の行はサービスの種類、下の行は問いの中身。並べ直しは、混ぜた結果の上位30件を小さな AI で読み直す", fontsize=10, color=SUB)
save(fig, "fig07b-search-example.png")

# 8. 答えの正しさ(39問、Sonnet 3回の多数決)
fig, ax = plt.subplots(figsize=(9, 3.6))
names = ["AIだけ(資料なし)", "検索して1回で答える", "AIが自分で何度も検索", "AIが目次をたどる"]
ok, part, ng = [11, 11, 16, 16], [9, 9, 11, 12], [19, 19, 12, 11]
y = list(range(len(names)))[::-1]
ax.barh(y, ok, color=BLUE, height=0.6, label="正しい")
ax.barh(y, part, left=ok, color=LIGHT, height=0.6, label="一部正しい", edgecolor="#fcfcfb", linewidth=2)
ax.barh(y, ng, left=[a + b for a, b in zip(ok, part)], color="#e1e0db", height=0.6, label="誤り", edgecolor="#fcfcfb", linewidth=2)
for yi, a in zip(y, ok):
    ax.text(a / 2, yi, f"{a}", ha="center", va="center", color="#ffffff", fontsize=12, fontweight="bold")
ax.set_yticks(y, names); ax.tick_params(axis="y", length=0); ax.set_xlim(0, 39)
ax.set_xlabel("問い(39問)")
ax.legend(ncol=3, frameon=False, loc="upper left", bbox_to_anchor=(0, -0.22), fontsize=11)
title(ax, "AIに自分で調べさせると、正しい答えが増えた", "根拠を探す39問の答えを、AIに3回判定させた多数決")
save(fig, "fig08-answers.png")

# 9. 外し方
fig, ax = plt.subplots(figsize=(9, 2.8))
names = ["AIだけ(資料なし)", "検索して1回で答える"]
rev, idk, other = [16, 0], [3, 18], [0, 1]
y = [1, 0]
ax.barh(y, rev, color=ORANGE, height=0.55, label="結論が逆")
ax.barh(y, idk, left=rev, color=GRAY, height=0.55, label="「資料では分からない」で止まる", edgecolor="#fcfcfb", linewidth=2)
ax.barh(y, other, left=[a + b for a, b in zip(rev, idk)], color="#e1e0db", height=0.55, label="その他", edgecolor="#fcfcfb", linewidth=2)
ax.text(8, 1, "16", ha="center", va="center", color="#ffffff", fontsize=13, fontweight="bold")
ax.text(9, 0, "18", ha="center", va="center", color=INK, fontsize=13, fontweight="bold")
ax.set_yticks(y, names); ax.tick_params(axis="y", length=0); ax.set_xlim(0, 19)
ax.set_xlabel("問い"); ax.set_xticks([0, 5, 10, 15])
ax.legend(ncol=3, frameon=False, loc="upper left", bbox_to_anchor=(0, -0.3), fontsize=10.5)
title(ax, "同じ点数でも、外し方が逆だった", "どちらも39問中19問が誤り。その19問の中身")
save(fig, "fig09-errors.png")

# 10. GraphRAG: グラフあり・なし
fig, ax = plt.subplots(figsize=(9, 3.8))
libs = ["LightRAG", "Microsoft GraphRAG", "HippoRAG 2"]
graph, plain = [0.70, 0.68, 0.87], [0.77, 0.77, 0.86]
y = [2, 1, 0]
ax.barh([v + 0.17 for v in y], plain, height=0.32, color=BLUE, label="グラフを使わない")
ax.barh([v - 0.17 for v in y], graph, height=0.32, color=ORANGE, label="グラフを使う")
for yi, a, b in zip(y, plain, graph):
    ax.text(a + 0.008, yi + 0.17, f"{a:.2f}", va="center", fontsize=11)
    ax.text(b + 0.008, yi - 0.17, f"{b:.2f}", va="center", fontsize=11)
ax.axvline(0.83, color=SUB, linestyle="--", linewidth=1)
ax.text(0.83, 2.62, "基準: 混ぜる+並べ直し 0.83", fontsize=10, color=SUB, ha="center")
ax.set_yticks(y, libs); ax.tick_params(axis="y", length=0); ax.set_xlim(0, 1.0)
ax.legend(ncol=2, frameon=False, loc="upper left", bbox_to_anchor=(0, -0.1), fontsize=11)
title(ax, "グラフで点が上がったライブラリはなかった", "訪問介護の範囲608件、根拠を探す問題の再現率")
save(fig, "fig10-graphrag.png")

# 11. グラフを作る手間
hbar("fig11-graph-cost.png", ["Microsoft GraphRAG", "LightRAG", "HippoRAG 2", "自前のグラフ(AIなし)"],
     [5900, 1796, 1230, 0], "グラフを作るのに、AIを何回呼んだか", "ライブラリは訪問介護の608件、自前は全7,048件で作った",
     hi=(), fmt="{:,}回", xmax=6800)

# 12. 改行
hbar("fig12-newline.png", ["改行を残して埋め込む", "改行を空白にして埋め込む"], [0.78, 0.87],
     "改行を空白にするだけで、点が上がった", "同じ埋め込みモデル(ruri-v3)、根拠を探す問題の再現率。基準の「混ぜる+並べ直し」は0.83",
     hi=("改行を空白にして埋め込む",), xmax=1.0)
print("done", sorted(p.name for p in OUT.glob("fig*.png")))
