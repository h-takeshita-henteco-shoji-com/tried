"""減点を受けた人と、その周りの人が、次の回にどう変えるかを集計する(#178)。AIは呼ばない。

使い方: python analyze_punished.py <名前>=<runs のパターン> [<名前>=<パターン> ...]
- パターンはカンマで区切って複数書ける。減点ありの、Haiku の記録だけを使う。固定の参加者(bots)は数えない
- 減点を受けた場面: t回目(1〜9回目)に、全額未満を入れて、減点を1点以上受けた。FG2000 本文 p.992 と同じ定義
  人間: 同じ相手 125件で89%が次の回に増やし、平均4.6増。毎回相手が変わる 368件で78%が増やし、平均3.8増
- 続くか: 減点を受けた回(t)から見た、t+1・t+2・t+3回目の量の差(t が7回目以下の場面だけ)
- 周りの人: t回目に減点を受けず、同じ組の誰かが減点を受けた人。比べる相手は、組の誰も減点を受けなかった回の人
"""
import glob
import json
import os
import sys
from statistics import mean

from compare import load


def runs(pattern):
    out = []
    for d in sorted(x for pat in pattern.split(",") for x in glob.glob(pat)):
        cond, m, ev = load(d)
        if cond.endswith("/punish") and "haiku" in m["llm"]:
            out.append((d, cond, m, ev))
    return out


def analyze(items):
    hit, persist, near, calm = [], {1: [], 2: [], 3: []}, [], []
    hit_below, hit_even = [], []
    for d, cond, m, ev in items:
        G = {}
        for e in ev:
            G.setdefault(e["group"], {})[e["round"]] = e
        for g, rr in G.items():
            for t in range(1, 10):
                if t not in rr or t + 1 not in rr:
                    continue
                e, nx = rr[t], rr[t + 1]
                n = len(e["members"])
                recv = [sum(e["points"][i][j] for i in range(n)) for j in range(n)]
                bot = [r.startswith("(固定の参加者") for r in e.get("reasons", [""] * n)]
                anyone = any(recv[j] > 0 for j in range(n) if not bot[j])
                for j in range(n):
                    if bot[j]:
                        continue
                    c = e["contribs"][j]
                    dc = nx["contribs"][j] - c
                    others = mean(e["contribs"][k] for k in range(n) if k != j)
                    if recv[j] > 0 and c < 20:
                        hit.append(dc)
                        (hit_below if c < others - 1 else hit_even).append(dc)
                        if t <= 7 and all(t + k in rr for k in (1, 2, 3)):
                            for k in (1, 2, 3):
                                persist[k].append(rr[t + k]["contribs"][j] - c)
                    elif recv[j] == 0 and c < 20 and c >= others - 1:
                        (near if anyone else calm).append(dc)
    return hit, hit_below, hit_even, persist, near, calm


def fmt(xs):
    if not xs:
        return "なし"
    up = [x for x in xs if x > 0]
    return (f"{len(xs)}件 増やした{len(up) / len(xs):.0%} 平均{mean(xs):+.2f}"
            f" 増やした場面だけの平均{mean(up) if up else 0:+.2f}")


def main(args):
    for spec in args:
        name, _, pattern = spec.partition("=")
        items = runs(pattern)
        hit, hb, he, persist, near, calm = analyze(items)
        print(f"== {name}  記録{len(items)}本")
        print(f"  減点を受けた次の回        {fmt(hit)}")
        print(f"    平均より少なく入れていた {fmt(hb)}")
        print(f"    平均以上を入れていた     {fmt(he)}")
        print("  受けた回から見た差        " + "  ".join(
            f"t+{k} {mean(v):+.2f}" for k, v in persist.items() if v) + f"  ({len(persist[1])}件)")
        print(f"  周り(組の誰かが受けた)    {fmt(near)}")
        print(f"  比べる相手(誰も受けない)  {fmt(calm)}")


if __name__ == "__main__":
    main(sys.argv[1:])
