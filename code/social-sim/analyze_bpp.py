"""話し合いと減点の公共財ゲーム(#173)の記録を、Bochet ほか(2006)の人間の結果と比べる。AIは呼ばない。

使い方: python analyze_bpp.py runs/c173
- 条件は記録の設定から決める: 減点の有無 × 話し合いなし・チャット・数字だけ
- 条件ごとに、seed をまたいだ回ごとの平均・10回の平均・最初と最後を出し、人間の値と並べる
- 最後に、10回の平均の順番を人間と比べる(Spearman の順位相関)
"""
import glob
import json
import os
import sys
from statistics import mean

HERE = os.path.dirname(os.path.abspath(__file__))
REF = json.load(open(os.path.join(HERE, "reference", "bpp2006.json"), encoding="utf-8"))
ORDER = ["B", "R", "CR", "CRwR", "NCT", "NCTwR"]
NAMES = {"B": "何もなし", "R": "減点だけ", "CR": "チャット", "CRwR": "チャット+減点",
         "NCT": "数字だけ", "NCTwR": "数字だけ+減点"}


def cond(game):
    talk = "CR" if game.get("chat_rounds") else ("NCT" if game.get("cheap_talk") else "")
    if not talk:
        return "R" if game["punishment"] else "B"
    return talk + ("wR" if game["punishment"] else "")


def rank(xs):
    s = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and xs[s[j + 1]] == xs[s[i]]:
            j += 1
        for k in range(i, j + 1):
            r[s[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = rank(a), rank(b)
    ma, mb = mean(ra), mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else float("nan")


def main(root):
    data = {}
    cost = 0.0
    for d in sorted(glob.glob(os.path.join(root, "*"))):
        mf = os.path.join(d, "manifest.json")
        if not os.path.exists(mf):
            continue
        m = json.load(open(mf, encoding="utf-8"))
        if "summary" not in m:
            continue
        c = cond(m["config"]["game"])
        ev = [json.loads(line) for line in open(os.path.join(d, "events.jsonl"), encoding="utf-8")]
        by = {}
        pts = 0
        for e in ev:
            by.setdefault(e["round"], []).extend(e["contribs"])
            pts += sum(map(sum, e["points"]))
        data.setdefault(c, []).append({"seed": m["config"]["seed"], "by": [mean(by[r]) for r in sorted(by)],
                                       "points": pts / len({p for e in ev for p in e["members"]}) if pts else 0})
        cost += m.get("cost_usd", 0)
    ai, hu = [], []
    print(f"{'条件':14s} {'本数':>3s} {'1回目':>6s} {'10回目':>6s} {'10回の平均':>8s}  人間(1回目/10回目/平均)  seedごとの平均")
    for c in ORDER:
        if c not in data:
            continue
        runs = data[c]
        by = [mean(r["by"][k] for r in runs) for k in range(10)]
        avg = mean(by)
        h = REF["by_period"][c]
        ai.append(avg)
        hu.append(REF["average"][c])
        seeds = " ".join(f"{mean(r['by']):.2f}" for r in sorted(runs, key=lambda r: r["seed"]))
        print(f"{NAMES[c]:14s} {len(runs):3d} {by[0]:6.2f} {by[-1]:6.2f} {avg:8.2f}  {h[0]:5.2f}/{h[-1]:5.2f}/{REF['average'][c]:5.2f}  {seeds}")
    if len(ai) >= 3:
        print(f"順位相関(10回の平均、AIと人間): {spearman(ai, hu):.2f}  条件数 {len(ai)}")
    print(f"費用 {cost:.2f}ドル")
    print("回ごとの平均:")
    for c in ORDER:
        if c in data:
            by = [mean(r["by"][k] for r in data[c]) for k in range(10)]
            print(f"  {NAMES[c]:12s} AI   " + " ".join(f"{x:5.2f}" for x in by))
            print(f"  {'':12s} 人間 " + " ".join(f"{x:5.2f}" for x in REF["by_period"][c]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "runs", "c173"))
