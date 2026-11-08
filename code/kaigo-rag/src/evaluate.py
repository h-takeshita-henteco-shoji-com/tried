"""同じ問題集で、検索の方式を並べて採点する。

A: 正解の Q&A を上位に引けたか(recall@1/5/10, MRR@10)
B: 根拠(判定2)を上位10件に引けたか(hit@10, recall@10, nDCG@10)
出力: results/day1.json と標準出力の表
"""
import json
import math
import sys
import time

import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rag
from embed import embed_queries

ROOT = Path(__file__).resolve().parent.parent
K = 10


def vec_ann_norerank(con, qv, k=K):
    b = qv.tobytes()
    return con.execute(f"SELECT rowid, 0 FROM vec_ann(?, '{{K:{k}, nprobe:0.1}}')", (b,)).fetchall()


# HyDE の仮の答えのベクトル(問いの文 -> ベクトル)。main で用意する
HYDE: dict = {}


def hyde_vec(q, qv, mix: bool):
    h = HYDE[q]
    if not mix:
        return h
    v = qv + h
    return (v / np.linalg.norm(v)).astype(np.float32)


SMART = {
    "基準: ベクトル(ANN・nprobe0.4)": lambda con, q, qv, k=K: rag.vector(con, qv, k, table="vec_ann", nprobe=0.4),
    "基準: ハイブリッド": lambda con, q, qv, k=K: rag.hybrid(con, q, qv, k),
    "ハイブリッド+リランカー(上位30)": lambda con, q, qv, k=K: rag.rerank(con, q, rag.hybrid(con, q, qv, 30), k),
    "HyDE(仮の答えでベクトル)": lambda con, q, qv, k=K: rag.vector(con, hyde_vec(q, qv, False), k, table="vec_ann", nprobe=0.4),
    "HyDE(問いと仮の答えの平均)": lambda con, q, qv, k=K: rag.vector(con, hyde_vec(q, qv, True), k, table="vec_ann", nprobe=0.4),
    "HyDE+BM25(ハイブリッド)": lambda con, q, qv, k=K: rag.rrf(rag.bm25(con, q, 100), rag.vector(con, hyde_vec(q, qv, True), 100, nprobe=0.4), k=k),
    "見出しパス(ベクトル)": lambda con, q, qv, k=K: rag.vector(con, qv, k, table="vec_path"),
    "見出しパス(ハイブリッド)": lambda con, q, qv, k=K: rag.hybrid(con, q, qv, k, fts="fts_path", vec="vec_path"),
    "Contextual(ベクトル)": lambda con, q, qv, k=K: rag.vector(con, qv, k, table="vec_ctx"),
    "Contextual(ハイブリッド)": lambda con, q, qv, k=K: rag.hybrid(con, q, qv, k, fts="fts_ctx", vec="vec_ctx"),
    "Contextual(ハイブリッド)+リランカー": lambda con, q, qv, k=K: rag.rerank(con, q, rag.hybrid(con, q, qv, 30, fts="fts_ctx", vec="vec_ctx"), k),
}

METHODS = {
    "BM25(FTS5)": lambda con, q, qv, k=K: rag.bm25(con, q, k),
    "ベクトル(vec1 flat・厳密)": lambda con, q, qv, k=K: rag.vector(con, qv, k, table="vec_flat"),
    "ベクトル(vec1 ANN・rerankなし・nprobe0.1)": lambda con, q, qv, k=K: vec_ann_norerank(con, qv, k),
    "ベクトル(vec1 ANN・rerankあり・nprobe0.1)": lambda con, q, qv, k=K: rag.vector(con, qv, k, table="vec_ann"),
    "ベクトル(vec1 ANN・rerankあり・nprobe0.4)": lambda con, q, qv, k=K: rag.vector(con, qv, k, table="vec_ann", nprobe=0.4),
    "ハイブリッド(RRF)": lambda con, q, qv, k=K: rag.hybrid(con, q, qv, k),
}


def ndcg(ranked, grades, k=K):
    dcg = sum((2 ** grades.get(c, 0) - 1) / math.log2(i + 2) for i, c in enumerate(ranked[:k]))
    ideal = sorted(grades.values(), reverse=True)[:k]
    idcg = sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg else 0.0


GRAPH = {
    "基準: ハイブリッド": lambda con, q, qv, k=K: rag.hybrid(con, q, qv, k),
    "基準: ハイブリッド+リランカー(上位30)": SMART["ハイブリッド+リランカー(上位30)"],
    "グラフだけ(問いの用語)": lambda con, q, qv, k=K: rag.graph(con, q, [], k, n_seed=0),
    "グラフだけ(問いの用語+上位3件の用語と参照)": lambda con, q, qv, k=K: rag.graph(con, q, rag.hybrid(con, q, qv, 100), k),
    "GraphRAG(ハイブリッド+グラフ)": lambda con, q, qv, k=K: rag.graph_hybrid(con, q, qv, k),
    "GraphRAG(ハイブリッド+グラフ)+リランカー": lambda con, q, qv, k=K: rag.rerank(con, q, rag.graph_hybrid(con, q, qv, 30), k),
    "GraphRAG(ハイブリッド30件にグラフ10件を足す)+リランカー": lambda con, q, qv, k=K: rag.rerank(con, q, graph_add(con, q, qv), k),
}


def graph_add(con, q, qv, n_hy=30, n_gr=10):
    """ハイブリッドの上位30件はそのまま残し、グラフで見つかった別の候補を10件足す。"""
    hy = rag.hybrid(con, q, qv, 100)
    have = {c for c, _ in hy[:n_hy]}
    extra = [(c, s) for c, s in rag.graph(con, q, hy, 100) if c not in have][:n_gr]
    return hy[:n_hy] + extra


# 訪問介護の範囲(data/subset_houmon.json)だけで比べる組。LLM で索引を作るグラフの方式は、全件では時間が収まらないため
SUBSET: set = set()
LIBRARY_IDS: dict = {}  # {方式: {問い: [チャンク id]}}。graph_lightrag.py などが先に作る


def in_subset(lst, k):
    return [x for x in lst if x[0] in SUBSET][:k]


def subset_methods():
    m = {
        "BM25": lambda con, q, qv, k=K: in_subset(rag.bm25(con, q, 2000), k),
        "ベクトル(flat)": lambda con, q, qv, k=K: in_subset(rag.vector(con, qv, 1500, table="vec_flat"), k),
        "ハイブリッド": lambda con, q, qv, k=K: rag.rrf(in_subset(rag.bm25(con, q, 2000), 100),
                                                   in_subset(rag.vector(con, qv, 1500, table="vec_flat"), 100), k=k),
    }
    m["ハイブリッド+リランカー(上位30)"] = lambda con, q, qv, k=K: rag.rerank(con, q, m["ハイブリッド"](con, q, qv, 30), k)
    for name, table in LIBRARY_IDS.items():
        m[name] = (lambda t: lambda con, q, qv, k=K: [(c, 0) for c in t.get(q, [])][:k])(table)
    return m


def main(group: str, only: str = ""):
    con = rag.connect()
    if group == "subset":
        SUBSET.update(json.load(open(ROOT / "data/subset_houmon.json")))
        for f in sorted((ROOT / "results").glob("lib_*.json")):
            LIBRARY_IDS.update(json.load(open(f)))
        methods = subset_methods()
    else:
        methods = {"basic": METHODS, "smart": SMART, "graph": GRAPH}[group]
    methods = {n: f for n, f in methods.items() if only in n}
    tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master")}
    methods = {n: f for n, f in methods.items()
               if not (("見出しパス" in n and "vec_path" not in tables) or ("Contextual" in n and "vec_ctx" not in tables))}
    qa2cid = dict(con.execute("SELECT qa_id, id FROM chunks WHERE kind='qa'").fetchall())
    # Q&A集には、同じ問いと答えが種別ごとに重ねて載っている。中身が同じ Q&A は同じものとして扱う
    equiv = json.load(open(ROOT / "data/qa_equiv.json"))
    same = lambda qa_id: {qa2cid[e] for e in equiv[qa_id] if e in qa2cid}
    set_a = [json.loads(l) for l in open(ROOT / "data/set_a.jsonl")]
    set_b = [json.loads(l) for l in open(ROOT / "data/set_b.jsonl")] if (ROOT / "data/set_b.jsonl").exists() else []
    set_b = [b for b in set_b if any(v == 2 for v in b["judged"].values())]
    # Excel の行が崩れて、元の問いが空の Q&A は外す
    qa = {json.loads(l)["qa_id"]: json.loads(l) for l in open(ROOT / "data/qa_all.jsonl")}
    set_a = [x for x in set_a if qa[x["qa_id"]]["question"].strip()]
    set_b = [x for x in set_b if qa[x["qa_id"]]["question"].strip()]
    qa_vec = embed_queries([x["query"] for x in set_a])
    qb_vec = embed_queries([x["query"] for x in set_b]) if set_b else []
    hyde_path = ROOT / "data/hyde.jsonl"
    if group == "smart" and hyde_path.exists():
        from embed import DOC_PREFIX, model
        hy = {json.loads(l)["query"]: json.loads(l)["hyde"] for l in open(hyde_path)}
        qs = list(hy)
        vs = model().encode([DOC_PREFIX + hy[q] for q in qs], batch_size=8, normalize_embeddings=True)
        HYDE.update({q: v.astype(np.float32) for q, v in zip(qs, vs)})
        missing = [x["query"] for x in set_a + set_b if x["query"] not in HYDE]
        if missing:
            print("HyDE なしの問い:", len(missing))
            methods = {n: f for n, f in methods.items() if "HyDE" not in n}

    res = {}
    for name, fn in methods.items():
        print("…", name, flush=True)
        r = {"A": {}, "B": {}}
        ranks, t0 = [], time.perf_counter()
        for x, qv in zip(set_a, qa_vec):
            ids = [c for c, _ in fn(con, x["query"], qv)]
            gold = same(x["gold_qa"][0])
            ranks.append(next((i + 1 for i, c in enumerate(ids) if c in gold), None))
        ms = (time.perf_counter() - t0) / len(set_a) * 1000
        n = len(ranks)
        r["A"] = {
            "recall@1": sum(1 for x in ranks if x and x <= 1) / n,
            "recall@5": sum(1 for x in ranks if x and x <= 5) / n,
            "recall@10": sum(1 for x in ranks if x) / n,
            "MRR@10": sum(1 / x for x in ranks if x) / n,
            "ms/問": ms,
        }
        if set_b:
            hits, recs, nd = [], [], []
            for x, qv in zip(set_b, qb_vec):
                # 外した Q&A の写しがコーパスに残っていれば、結果からも正解からも除く
                leak = same(x["qa_id"])
                grades = {int(k): v for k, v in x["judged"].items() if int(k) not in leak
                          and (not SUBSET or int(k) in SUBSET)}
                gold = {c for c, v in grades.items() if v == 2}
                if not gold:
                    continue
                ids = [c for c, _ in fn(con, x["query"], qv, K + len(leak)) if c not in leak][:K]
                got = gold & set(ids)
                hits.append(1 if got else 0)
                recs.append(len(got) / min(len(gold), K))
                nd.append(ndcg(ids, grades))
            nb = len(hits)
            r["B"] = {"hit@10": sum(hits) / nb, "recall@10": sum(recs) / nb, "nDCG@10": sum(nd) / nb, "n": nb}
        res[name] = r

    (ROOT / "results").mkdir(exist_ok=True)
    out = ROOT / f"results/{group}.json"
    prev = json.load(open(out)) if out.exists() else {}
    res = {**prev, **res}
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"A: {len(set_a)}問 / B: {nb}問")
    print("| 方式 | A recall@1 | A recall@10 | A MRR@10 | B hit@10 | B recall@10 | B nDCG@10 | ms/問 |")
    print("|---|---|---|---|---|---|---|---|")
    for name, r in res.items():
        a, b = r["A"], r.get("B") or {}
        print(f"| {name} | {a['recall@1']:.2f} | {a['recall@10']:.2f} | {a['MRR@10']:.3f} | "
              f"{b.get('hit@10', float('nan')):.2f} | {b.get('recall@10', float('nan')):.2f} | {b.get('nDCG@10', float('nan')):.3f} | {a['ms/問']:.1f} |")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "basic", sys.argv[2] if len(sys.argv) > 2 else "")
