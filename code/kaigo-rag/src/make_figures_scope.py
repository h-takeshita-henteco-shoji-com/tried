"""#155(介護保険でできることを説明させる)の note 記事の図を作る。数字は results/scope_summary.json と log.md から写した。
使い方: uv run --with matplotlib python src/make_figures_scope.py <出力フォルダ>
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "Hiragino Sans", "font.size": 13, "axes.edgecolor": "#c3c2b7",
    "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#0b0b0b",
    "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
})
BLUE, ORANGE, GRAY, LIGHT, INK, SUB = "#2a78d6", "#eb6834", "#b9b8b2", "#a9c7ee", "#0b0b0b", "#52514e"
MODES = ["AI だけ", "AI が自分で検索"]


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def title(ax, t, sub=None):
    ax.set_title(t, loc="left", fontsize=16, fontweight="bold", color=INK, pad=28 if sub else 12)
    if sub:
        ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=11, color=SUB, va="bottom")


def grouped(name, groups, values, t, sub, fmt, xmax, note=None):
    """グループごとに2方式の横棒。AI だけは灰、検索は青。"""
    fig, ax = plt.subplots(figsize=(8.5, 1.25 * len(groups) + 1.6))
    h = 0.34
    for gi, (g, vs) in enumerate(zip(groups, values)):
        y0 = len(groups) - 1 - gi
        for mi, v in enumerate(vs):
            y = y0 + (0.2 if mi == 0 else -0.2)
            ax.barh(y, v, height=h, color=GRAY if mi == 0 else BLUE)
            ax.text(v + xmax * 0.01, y, fmt(v), va="center", fontsize=12, color=INK)
            ax.text(-xmax * 0.01, y, MODES[mi], va="center", ha="right", fontsize=11, color=SUB)
        ax.text(-xmax * 0.30, y0, g, va="center", ha="right", fontsize=13, color=INK, fontweight="bold")
    ax.set_yticks([])
    ax.set_xlim(0, xmax)
    ax.grid(axis="x", color="#e6e5e0", linewidth=0.8)
    ax.set_axisbelow(True)
    title(ax, t, sub)
    if note:
        fig.text(0.01, -0.02, note, fontsize=9, color=SUB, ha="left", va="top")
    save(fig, name)


# 1. 可否が合った割合(判定役 Sonnet 3回の多数決、答え3回の平均)
grouped("fig01-verdict.png", ["自作の20問", "自治体の事例13問"],
        [[100, 100], [9.7 / 13 * 100, 8.7 / 13 * 100]],
        "自治体の事例では、可否を外した", "可否が合った割合(答え3回の平均)",
        lambda v: f"{v:.0f}%", 115,
        note="判定は Sonnet が3回行い、多数決を取った。自作の問いは、通知の別紙の事例を言い換えたもの")

# 2. 正解ごとの答えの内訳(延べ。問いの数×3回)
rows = [("正解が「可」\n(11問×3回)", [(8, 0, 25), (1, 0, 32)]),
        ("正解が「不可」\n(17問×3回)", [(0, 38, 13), (0, 38, 13)]),
        ("正解が「条件付き」\n(5問×3回)", [(0, 0, 15), (0, 0, 15)])]
fig, ax = plt.subplots(figsize=(9, 6.2))
cols = {"可": BLUE, "不可": ORANGE, "条件付き": GRAY}
yt, yl = [], []
for gi, (g, pair) in enumerate(rows):
    y0 = (len(rows) - 1 - gi) * 1.3
    for mi, (a, b, c) in enumerate(pair):
        y = y0 + (0.22 if mi == 0 else -0.22)
        left = 0
        for k, v in zip(["可", "不可", "条件付き"], (a, b, c)):
            if v:
                ax.barh(y, max(v - 0.3, 0.6), left=left, height=0.38, color=cols[k])
            if v >= 2:
                ax.text(left + v / 2, y, str(v), ha="center", va="center", fontsize=11,
                        color="#ffffff" if k != "条件付き" else INK)
            left += v
        ax.text(-0.6, y, MODES[mi], va="center", ha="right", fontsize=11, color=SUB)
    ax.text(-14, y0, g, va="center", ha="right", fontsize=12, color=INK, fontweight="bold", linespacing=1.4)
ax.set_yticks([])
ax.set_xlim(0, 53)
ax.set_xlabel("答えの数")
ax.grid(axis="x", color="#e6e5e0", linewidth=0.8)
ax.set_axisbelow(True)
handles = [plt.Rectangle((0, 0), 1, 1, color=cols[k]) for k in cols]
ax.legend(handles, [f"AI が「{k}」と答えた" for k in cols], loc="upper center", bbox_to_anchor=(0.5, -0.12),
          ncol=3, frameon=False, fontsize=11)
title(ax, "AI は「可」と言わず、「条件付き」に寄せた", "正解ごとに、AI が何と答えたか(33問×3回の延べ)")
save(fig, "fig02-labels.png")

# 3. 根拠を機械で照らし合わせた結果
grouped("fig03-basis.png", ["正しい通知の名前を\n挙げた", "引用した文が\n資料どおり"],
        [[84, 100], [76, 90]],
        "根拠は、検索させると資料どおりになった", "判定役の AI を使わず、機械で数えた(33問×3回)",
        lambda v: f"{v:.0f}%", 115,
        note="通知の名前は、問いごとに正しいとみなす通知の一覧と突き合わせた。引用は「」内の8字以上の文を、送り仮名などのゆれをならして資料と比べた")


# ---------- 表の画像(note は表を表示できないため) ----------
import json
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parent.parent


def wrap(t, n):
    """字数で折り返す。句読点と閉じカッコは行頭に来ないよう、前の行に付ける。"""
    out = []
    for line in str(t).split("\n"):
        cur = ""
        for ch in line:
            if len(cur) >= n and ch not in "、。」』)":
                out.append(cur)
                cur = ""
            cur += ch
        out.append(cur)
    return "\n".join(out)


def table(name, t, sub, cols, widths, rows, cell_color=None, note=None, fs=11.5):
    """widths は列ごとの1行の字数。cell_color(ri, ci, text) が色を返せば、その色で塗る。"""
    lh = 0.30  # 1行の高さ(インチ)
    cw = [w * 0.185 + 0.25 for w in widths]  # 列の幅(インチ)
    W = sum(cw)
    wrapped = [[wrap(c, w) for c, w in zip(r, widths)] for r in rows]
    heights = [max(c.count("\n") + 1 for c in r) * lh + 0.22 for r in wrapped]
    hh = 0.5
    H = hh + sum(heights)
    fig = plt.figure(figsize=(W, H + 0.9))
    ax = fig.add_axes([0, 0, 1, H / (H + 0.9)])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    x = 0
    for c, w in zip(cols, cw):
        ax.add_patch(Rectangle((x, 0), w, hh, fc="#eeede8", ec="none"))
        ax.text(x + 0.12, hh / 2, c, va="center", fontsize=fs, fontweight="bold", color=INK)
        x += w
    y = hh
    for ri, (r, h) in enumerate(zip(wrapped, heights)):
        x = 0
        for ci, (c, w) in enumerate(zip(r, cw)):
            col = cell_color(ri, ci, rows[ri][ci]) if cell_color else None
            if col:
                ax.add_patch(Rectangle((x + 0.04, y + 0.05), w - 0.08, h - 0.1, fc=col, ec="none"))
            ax.text(x + 0.12, y + h / 2, c, va="center", fontsize=fs, color=INK, linespacing=1.45)
            x += w
        ax.plot([0, W], [y + h, y + h], color="#e0dfda", lw=0.8)
        y += h
    fig.text(0.0, 1 - 0.25 / (H + 0.9), t, fontsize=16, fontweight="bold", color=INK, va="top")
    if sub:
        fig.text(0.0, 1 - 0.62 / (H + 0.9), sub, fontsize=11, color=SUB, va="top")
    if note:
        fig.text(0.0, -0.04, note, fontsize=9.5, color=SUB, va="top")
    save(fig, name)


VCOL = {"可": "#dbe8f8", "不可": "#fbe1d6", "条件付き": "#ecebe6"}


def vcolor(ci):
    return lambda ri, c, txt: VCOL.get(txt) if c == ci else None


# 問いの一覧(自作20問)
SELF = [
    ("同居している息子の分も、一緒に夕飯を作ってもらえませんか", "不可", "利用者以外の分の調理(老振76号)"),
    ("息子夫婦と同居。昼間は2人とも仕事でいない。私の部屋の掃除をお願いできる?", "条件付き", "同居家族の状況を見て個別に判断(Q&A)"),
    ("庭の草むしりをしてもらえない?", "不可", "草むしり(老振76号)"),
    ("ベランダの鉢植えに水をやっておいてほしい", "不可", "花木の水やり(老振76号)"),
    ("足が悪くて犬の散歩に行けない。代わりに連れて行ってもらえる?", "不可", "ペットの世話(老振76号)"),
    ("年末だから、大掃除と窓拭きをお願いしたい", "不可", "大掃除・窓のガラス拭き(老振76号)"),
    ("お正月のおせち料理を作ってくれないかしら", "不可", "正月などの特別な手間の調理(老振76号)"),
    ("今日はお客さんが来るから、お茶を出してもらえる?", "不可", "来客の応接(老振76号)"),
    ("タンスの場所を変えて、部屋の模様替えを手伝ってほしい", "不可", "家具の移動・模様替え(老振76号)"),
    ("私の分の食料品の買い物をしてきてもらえますか", "可", "本人の買い物(老計10号)"),
    ("薬局で、私の薬を受け取ってきてほしい", "可", "薬の受け取り(老計10号)"),
    ("私が寝ている布団を干してもらえる?", "可", "本人の布団干し(老計10号)"),
    ("病院に付き添ってほしい。診察を待っている間も、そばにいてくれる?", "条件付き", "待ち時間は対象外、院内の見守りは可(Q&A)"),
    ("来てもらったついでに、髪を切ってもらえない?", "不可", "理美容は含まれない(Q&A)"),
    ("台所に一緒に立って、私が料理するのを見守りながら手伝ってもらえますか", "可", "一緒に行う家事の見守り(老計10号)"),
    ("車を洗っておいてもらえる?", "不可", "自家用車の洗車(老振76号)"),
    ("お風呂に入るのを手伝ってほしい", "可", "入浴介助(老計10号)"),
    ("家族みんなで使っている居間と台所を掃除してほしい", "不可", "主に本人が使う部屋以外の掃除(老振76号)"),
    ("ゴミ出しをお願いできますか", "可", "ゴミ出し(老計10号)"),
    ("ベッドのシーツを替えてもらえる?", "可", "シーツ交換(老計10号)"),
]
table("fig00a-questions-self.png", "自作の20問", "利用者や家族が言いそうな言い方で書いた。正解は通知と Q&A の本文から付けた",
      ["#", "頼みごと", "正解", "正解の根拠"], [3, 34, 6, 22],
      [[f"S{i+1:02d}", a, b, c] for i, (a, b, c) in enumerate(SELF)], cell_color=vcolor(2))

MUNI = [
    ("夫婦とも痛みや息切れがある。子どもの帰省に備えて、草取り、ガラス拭き、布団の入れ替えを頼みたい", "不可", "日常生活の援助に当たらない", "郡上市"),
    ("夫、長男、孫2人と同居。家族全員の分の家事と、孫の犬の散歩を毎日頼みたい", "不可", "家族の分の家事とペットの世話は対象外", "郡上市"),
    ("二世帯住宅で2階に長男家族。家事をしていた妻が骨折した。妻の代わりの家事を頼みたい", "不可", "長男家族も同居とみなす。休日に担える", "郡上市"),
    ("糖尿病と食物アレルギーがあり、市販の糖尿病食が食べられない。本人の昼食を作ってほしい", "可", "特段の専門的配慮をもって行う調理(身体介護)", "郡上市"),
    ("同居の長男が癌で入院、長男の妻は疲れ切っている。掃除、買い物、食事の用意を頼みたい", "条件付き", "期間を限り、食事の用意などに絞る", "郡上市・時津町"),
    ("夫婦とも要介護。同居の孫は家事をせず、祖父への暴力歴もある。重い物の買い物と、高い所や屈む掃除を頼みたい", "可", "孫の事情は「やむを得ない事情」に当たる", "郡上市・時津町"),
    ("介護をしていた夫が入院。同居の三男は障害で家事が難しい。ゴミ出しを頼みたい", "可", "同居家族が家事をできない", "郡上市"),
    ("一人暮らし。冬は薪ストーブ。薪運びと整理を一緒にやりたい", "可", "一緒に行う見守り的援助(身体介護)", "郡上市"),
    ("閉じこもりがちで足腰も弱ってきた。近所の散歩に付き添ってほしい", "条件付き", "まずデイサービスなどを検討。特別な理由があれば個別に判断", "郡上市"),
    ("夫婦とも息切れがある。書棚の大量の古本を整理し、宅配に出す準備を頼みたい", "不可", "日常生活の援助に当たらない", "時津町"),
    ("看護師の長男と2人暮らし。夜勤はあるが休日は月8回ほど。掃除と買い物を頼みたい", "不可", "日中独居だけでは、やむを得ない事情に当たらない", "時津町"),
    ("二世帯住宅で2階に長男家族。息子や孫には頼みにくい。1階のトイレと浴室の掃除を頼みたい", "不可", "頼みにくい、慣れていないは事情に当たらない", "時津町"),
    ("夫も要支援で、骨折のため掃除ができない。本人の寝室と、家の中の掃除を頼みたい", "条件付き", "本人の寝室は可。共用部分は不可", "時津町"),
]
table("fig00b-questions-muni.png", "自治体の事例から作った13問", "正解は自治体自身の判断。自治体の資料は、AI が検索する資料には入れていない",
      ["#", "事例と頼みごと", "正解", "自治体の判断の要点", "出典"], [3, 34, 6, 22, 8],
      [[f"M{i+1:02d}", a, b, c, d] for i, (a, b, c, d) in enumerate(MUNI)], cell_color=vcolor(2))

# 検証の流れ
fig, ax = plt.subplots(figsize=(11, 4.6))
ax.set_xlim(0, 11)
ax.set_ylim(0, 4.6)
ax.axis("off")


def bx(x, y, w, h, txt, fc="#ffffff", ec=GRAY, bold=False, size=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=size, color=INK,
            fontweight="bold" if bold else "normal", linespacing=1.5)


def ar(a, b):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", color=SUB, lw=1.2))


bx(0.1, 1.6, 2.0, 1.4, "問い 33問\n自作 20問\n自治体の事例 13問", bold=True)
bx(2.8, 2.55, 2.4, 0.9, "AI だけ\n(資料を見ない)×3回")
bx(2.8, 1.15, 2.4, 0.9, "AI が自分で検索\n(7,049件の資料)×3回", fc="#eaf2fc", ec=BLUE)
bx(5.9, 1.6, 1.9, 1.4, "答え\n可否・説明・根拠")
bx(8.5, 3.05, 2.4, 0.95, "AI の採点\nSonnet 3回の多数決\n+ Opus 1回", size=11)
bx(8.5, 1.85, 2.4, 0.85, "通知の名前の照合\n(機械)", size=11)
bx(8.5, 0.6, 2.4, 0.85, "引用の照合\n(機械)", size=11)
ar((2.1, 2.5), (2.8, 3.0)); ar((2.1, 2.1), (2.8, 1.6))
ar((5.2, 3.0), (5.9, 2.5)); ar((5.2, 1.6), (5.9, 2.1))
ar((7.8, 2.5), (8.5, 3.5)); ar((7.8, 2.3), (8.5, 2.3)); ar((7.8, 2.1), (8.5, 1.0))
ax.text(0.1, 4.3, "検証の流れ", fontsize=16, fontweight="bold", color=INK)
ax.text(0.1, 3.95, "答える AI は、どちらも Claude の Sonnet。採点では、どちらの方式の答えかを伏せた", fontsize=11, color=SUB)
save(fig, "fig00c-method.png")

# 自治体の事例ごとの当たり外れ(Sonnet 3回の多数決)
ids = [f"M{i:02d}" for i in range(1, 14)]
SHORT = ["帰省前の草取り・ガラス拭き", "家族全員の家事と犬の散歩", "二世帯住宅、妻が骨折", "糖尿病食の昼食づくり",
         "同居の長男が入院", "孫が家事をせず暴力歴", "夫が入院、三男は障害", "薪運びを一緒に", "散歩の付き添い",
         "古本の整理と梱包", "看護師の長男と同居", "二世帯住宅、頼みにくい", "夫も要支援、家の中の掃除"]
keys = [f"{m}_r{r}" for m in ["llm", "agentic"] for r in [1, 2, 3]]
votes = {}
for k in [1, 2, 3]:
    for l in open(ROOT / f"results/scope_grades_sonnet{k}.jsonl"):
        g = json.loads(l)
        for key, v in g["grades"].items():
            votes.setdefault((g["id"], key), []).append(v["verdict_ok"])
labels = {}
for m in ["llm", "agentic"]:
    for r in [1, 2, 3]:
        for l in open(ROOT / f"results/scope_{m}_r{r}.jsonl"):
            a = json.loads(l)
            labels[(a["id"], f"{m}_r{r}")] = a["verdict"]
fig, ax = plt.subplots(figsize=(11, 8.2))
ax.set_xlim(-5.7, 6.6)
ax.set_ylim(len(ids) + 0.2, -1.6)
ax.axis("off")
for j, key in enumerate(keys):
    ax.text(j + 0.5 + (0.3 if j >= 3 else 0), -0.35, f"{j % 3 + 1}回目", ha="center", fontsize=10, color=SUB)
ax.text(1.5, -1.0, "AI だけ", ha="center", fontsize=12, fontweight="bold")
ax.text(4.8, -1.0, "AI が自分で検索", ha="center", fontsize=12, fontweight="bold")
for i, q in enumerate(ids):
    m = MUNI[i]
    ax.text(-5.6, i + 0.5, f"{q}  {SHORT[i]}", va="center", fontsize=11, color=INK)
    ax.text(-0.15, i + 0.5, m[1], va="center", ha="right", fontsize=10.5, color=INK, fontweight="bold")
    for j, key in enumerate(keys):
        ok = sum(votes[(q, key)]) >= 2
        x = j + (0.3 if j >= 3 else 0)
        ax.add_patch(Rectangle((x + 0.05, i + 0.08), 0.9, 0.84, fc=LIGHT if ok else ORANGE, ec="none"))
        lab = labels[(q, key)].replace("条件付き", "条件")
        ax.text(x + 0.5, i + 0.5, lab, ha="center", va="center", fontsize=10, color=INK if ok else "#ffffff")
ax.text(-0.15, -0.35, "正解", ha="right", fontsize=10, color=SUB)
ax.add_patch(Rectangle((0.05, len(ids) + 0.0), 0.4, 0.0, fc="none"))
fig.text(0.03, 0.97, "外したのは、同居家族の事例に集まった", fontsize=16, fontweight="bold", color=INK, va="top")
fig.text(0.03, 0.935, "自治体の事例13問。マスの字は AI の答え。青は採点で「合う」、オレンジは「外れ」(Sonnet 3回の多数決)",
         fontsize=11, color=SUB, va="top")
save(fig, "fig05-muni-grid.png")

# 同居家族の3事例
table("fig06-cohabit.png", "同居家族の事例で、AI は「やむを得ない事情」を広く取った", "自治体の判断と、AI の答え(3回分)",
      ["事例", "自治体の判断", "AI だけ", "AI が自分で検索"], [25, 20, 20, 20],
      [["M03 二世帯住宅。家事をしていた妻が骨折", "不可。2階の長男家族も同居とみなす。休日に家事を担える",
        "3回とも条件付き。「二世帯住宅の扱いは市町村で違う」", "3回とも条件付き。「同居のご家族がいても、一律に断られるわけではありません」"],
       ["M11 看護師の長男と2人暮らし。休日は月8回", "不可。日中独居というだけでは、やむを得ない事情に当たらない",
        "3回とも条件付き。「長男の夜勤で家事が難しければ、使える場合があります」", "3回とも条件付き。「同居家族がいるだけで断られることはありません」"],
       ["M12 二世帯住宅。息子や孫には頼みにくい", "不可。頼みにくい、家事をしたことがない、は事情に当たらない",
        "3回とも条件付き。ただし「『頼みにくい』だけでは認められにくい」(採点は合う)", "3回とも条件付き。「ご家族の事情だけで断られることはありません」(採点は外れ)"]],
      cell_color=lambda ri, ci, t: ("#fbe1d6" if ci >= 2 and not (ri == 2 and ci == 2) else ("#dbe8f8" if ri == 2 and ci == 2 else None)))

# 根拠の外し方
table("fig07-basis-examples.png", "AI だけの根拠は、もっともらしく外れた", "実在する通知の名前で、似た文を作る",
      ["問い", "AI だけの答え", "AI が自分で検索した答え", "資料の実際"], [10, 26, 22, 22],
      [["S03 草むしり", "老計10号の「訪問介護の範囲に含まれないもの」", "老振76号 別紙 2①(草むしりが例示されている)",
        "例が載っているのは、老振76号の別紙"],
       ["S07 おせち", "「正月などの年中行事等のために特別に手間をかけて行われる調理」", "「正月、節句等のために特別な手間をかけて行う調理」(老振76号 別紙)",
        "「正月、節句等のために特別な手間をかけて行う調理」"],
       ["M04 糖尿病食", "普通の調理(生活援助)。「疾病に応じた調理を直接定めた条文は原文未確認のため、要確認」",
        "「特段の専門的配慮をもって行う調理」(身体介護)。糖尿病食が特別食に当たることを告示から引いた",
        "自治体も「特段の専門的配慮をもって行う調理」として認めた"]],
      cell_color=lambda ri, ci, t: "#fbe1d6" if ci == 1 else ("#dbe8f8" if ci == 2 else None))

# 分かりやすさと採点の一致
table("fig08-stability.png", "説明の分かりやすさと、採点の安定", None,
      ["見たこと", "AI だけ", "AI が自分で検索"], [34, 12, 14],
      [["説明の分かりやすさ(1〜3点、Sonnet の多数決)", "2.75", "2.82"],
       ["断るときに、保険外(全額自己負担)でなら頼めると案内した", "29/51件", "33/51件"],
       ["3回の答えで、可否のラベルが変わった問い", "2問", "2問"]],
      note="採点の一致(両方式あわせて): Sonnet 3回がすべて同じだった割合は、可否97%・根拠78%・分かりやすさ60%。"
           "Opus と多数決が同じだった割合は、92%・83%・77%")

print("ok")
