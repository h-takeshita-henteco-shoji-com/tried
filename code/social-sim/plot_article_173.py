"""#173 の記事の図: 動機の文ごとの、回ごとの入れた量(チャットなし、各3組)と人間の「減点だけ」。

使い方: uv run --with matplotlib python plot_article_173.py
"""
import glob, json, os, statistics as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "2026", "11-17-糸島の農業を社会学とAIで考える-06-利用停止・評判・規約を再現する", "assets")
plt.rcParams["font.family"] = ["Hiragino Sans"]
INK, SUB, SURF = "#0b0b0b", "#52514e", "#fcfcfb"


def series(pat):
    d = glob.glob(os.path.join(HERE, "runs", "c173abl", pat))[0]
    ev = [json.loads(line) for line in open(os.path.join(d, "events.jsonl"))]
    return [st.mean(c for e in ev if e["round"] == r for c in e["contribs"]) for r in range(1, 11)]


human = json.load(open(os.path.join(HERE, "reference", "bpp2006.json")))["by_period"]["R"]
lines = [("人間(減点だけ)", human, INK, (0, (5, 3))),
         ("動機なし", series("*-id-plan-traits"), "#2a78d6", "-"),
         ("勝ち(win)", series("*-id-plan-traits-mwin"), "#eb6834", "-"),
         ("順位(rank)", series("*-id-plan-traits-mrank_plain"), "#1baf7a", "-")]
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=160)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
x = list(range(1, 11))
for name, ys, col, ls in lines:
    ax.plot(x, ys, color=col, lw=2, ls=ls, marker="o", ms=5, label=name)
    ax.annotate(name, (10, ys[-1]), xytext=(10, 0), textcoords="offset points", va="center", fontsize=12, color=INK)
ax.set_xlim(0.6, 12.4); ax.set_ylim(0, 10)
ax.set_xticks(x, [f"{r}回" for r in x])
ax.set_ylabel("4人が入れた量の平均(持ち点10)", color=SUB)
ax.set_title("全員に足した動機の一文ごとの、AIが入れた量の平均", loc="left", fontsize=15, color=INK)
ax.grid(axis="y", color="#e4e3df", lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color("#c9c8c3")
ax.tick_params(colors=SUB)
ax.legend(loc="lower left", frameon=False, fontsize=11)
fig.text(0.01, 0.01, "AIは各3組、チャットなし・くじなし・名前つき・作戦あり。人間は Bochet ほか(2006)", fontsize=9, color=SUB)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(os.path.join(OUT, "motive-by-round.png"), facecolor=SURF)
print("ok")


def people(pat, g):
    d = glob.glob(os.path.join(HERE, "runs", "c173abl", pat))[0]
    ev = [json.loads(line) for line in open(os.path.join(d, "events.jsonl"))]
    rows = sorted((e for e in ev if e["group"] == g), key=lambda e: e["round"])
    return [[e["contribs"][i] for e in rows] for i in range(4)]


traits = ["A 慎重", "B 人づきあいが好き", "C 負けず嫌い", "D 疑い深い"]
cols = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=160, sharey=True)
fig.patch.set_facecolor(SURF)
for ax, (title, pat) in zip(axes, [("動機なし(組0)", "*-id-plan-traits"), ("順位(rank、組0)", "*-id-plan-traits-mrank_plain")]):
    ax.set_facecolor(SURF)
    for k, ys in enumerate(people(pat, 0)):
        off = (k - 1.5) * 0.06          # 重なった線が見えるように、少しだけ上下にずらす
        ax.plot(x, [y + off for y in ys], color=cols[k], lw=2, marker="o", ms=5, label=traits[k])
    ax.set_title(title, loc="left", fontsize=14, color=INK)
    ax.set_ylim(-0.5, 10); ax.set_xticks(x, [str(r) for r in x])
    ax.set_xlabel("回", color=SUB)
    ax.grid(axis="y", color="#e4e3df", lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color("#c9c8c3")
    ax.tick_params(colors=SUB)
axes[0].set_ylabel("入れた量(持ち点10)", color=SUB)
axes[1].legend(loc="upper right", frameon=False, fontsize=11)
fig.text(0.01, 0.01, "同じ4つの性格、チャットなし・くじなし・名前つき・作戦あり。重なる線は少しずらして描いた", fontsize=9, color=SUB)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(os.path.join(OUT, "people-none-vs-rank.png"), facecolor=SURF)
print("ok2")
