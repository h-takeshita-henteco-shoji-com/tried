"""答えの判定を複数回取ったものをまとめる。

- 多数決: Sonnet の3回の判定の中央値(3つの点の真ん中)
- ぶれ: 3回とも同じ点だった割合
- 別のモデル: Opus の判定と、Sonnet の多数決が一致した割合
- 方式の差: 2つの方式を問いごとに比べ、勝ち・負け・引き分けを数える。符号検定の p 値を付ける
使い方: uv run python src/vote_answers.py            (資料を足す前後の7方式、Opus つき)
      uv run python src/vote_answers.py graph      (GraphRAG と、比べる4方式。Opus なし)
"""
import sys
import json
import statistics as st
from itertools import combinations
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODES = ["llm", "rag", "agentic", "pageindex", "rag_v2", "agentic_v2", "pageindex_v2"]
NAMES = {"llm": "LLM だけ", "rag": "RAG 一発", "agentic": "エージェント検索", "pageindex": "PageIndex 方式",
         "graph_v2": "GraphRAG(エージェント+グラフ)", "rag_v2": "RAG 一発(足した後)", "agentic_v2": "エージェント検索(足した後)", "pageindex_v2": "PageIndex 方式(足した後)"}
SONNET = ["answer_grades_v2.jsonl", "answer_grades_v2_r2.jsonl", "answer_grades_v2_r3.jsonl"]
OPUS = "answer_grades_v2_opus.jsonl"


def load(name):
    return {json.loads(l)["qa_id"]: json.loads(l)["grades"] for l in open(ROOT / "results" / name)}


def sign_p(w, l):
    """両側の符号検定。引き分けは除く。"""
    n = w + l
    if n == 0:
        return 1.0
    k = min(w, l)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def main():
    global MODES, SONNET
    use_opus = True
    pairs = [("agentic", "rag"), ("pageindex", "rag"), ("agentic", "llm"), ("pageindex", "llm"), ("rag", "llm"),
             ("agentic", "pageindex"), ("agentic_v2", "agentic"), ("pageindex_v2", "pageindex"), ("rag_v2", "rag")]
    if sys.argv[1:] == ["graph"]:
        MODES = ["rag_v2", "agentic", "agentic_v2", "pageindex_v2", "graph_v2"]
        SONNET = [f"answer_grades_graph_r{i}.jsonl" for i in (1, 2, 3)]
        use_opus = False
        pairs = [("graph_v2", "rag_v2"), ("graph_v2", "agentic"), ("graph_v2", "agentic_v2"), ("graph_v2", "pageindex_v2"),
                 ("agentic", "rag_v2"), ("agentic_v2", "rag_v2")]
    runs = [load(n) for n in SONNET]
    opus = load(OPUS) if use_opus else runs[0]
    qids = sorted(set.intersection(*[set(r) for r in runs], set(opus)))
    qids = [q for q in qids if all(set(MODES) <= set(r[q]) for r in runs + [opus])]
    vote = {q: {m: int(st.median(r[q][m] for r in runs)) for m in MODES} for q in qids}

    print(f"問い: {len(qids)}")
    print("| 方式 | 多数決 正しい(2) | 一部(1) | 誤り(0) | 平均点 | Sonnet 3回の正答数 | Opus 正しい(2) | Opus 平均点 |")
    print("|---|---|---|---|---|---|---|---|")
    for m in MODES:
        g = [vote[q][m] for q in qids]
        each = "/".join(str(sum(r[q][m] == 2 for q in qids)) for r in runs)
        o = [opus[q][m] for q in qids]
        print(f"| {NAMES[m]} | {g.count(2)} | {g.count(1)} | {g.count(0)} | {st.mean(g):.2f} | {each} "
              f"| {o.count(2)} | {st.mean(o):.2f} |")

    cells = [(q, m) for q in qids for m in MODES]
    same3 = sum(len({r[q][m] for r in runs}) == 1 for q, m in cells)
    agree = sum(opus[q][m] == vote[q][m] for q, m in cells)
    near = sum(abs(opus[q][m] - vote[q][m]) <= 1 for q, m in cells)
    print(f"\nSonnet 3回とも同じ点: {same3}/{len(cells)} ({same3 / len(cells):.0%})")
    print(f"Opus と Sonnet 多数決が同じ点: {agree}/{len(cells)} ({agree / len(cells):.0%})、差1以内: {near / len(cells):.0%}")
    if not use_opus:
        print("(この組では Opus の判定を取っていない。Opus の列と一致の行は、Sonnet の1回目を写しただけ)")
    hi = sum(opus[q][m] > vote[q][m] for q, m in cells)
    lo = sum(opus[q][m] < vote[q][m] for q, m in cells)
    print(f"Opus のほうが高い: {hi}、低い: {lo}")

    print("\n方式の差(Sonnet 多数決。問いごとの勝ち-負け-引き分け、符号検定の p 値)")
    print("| 比べた2方式 | 勝ち | 負け | 引き分け | p |")
    print("|---|---|---|---|---|")
    for a, b in pairs:
        w = sum(vote[q][a] > vote[q][b] for q in qids)
        l = sum(vote[q][a] < vote[q][b] for q in qids)
        print(f"| {NAMES[a]} 対 {NAMES[b]} | {w} | {l} | {len(qids) - w - l} | {sign_p(w, l):.3f} |")


if __name__ == "__main__":
    main()
