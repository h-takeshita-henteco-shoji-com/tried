"""資料を足した後の pool: B の各問いで、基本3種と、ハイブリッド+リランカーの上位20件に入った新しい資料のチャンクを集める。

出力: data/unjudged_newdocs.json(judge_extra.py に渡す)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rag
from embed import embed_queries

ROOT = Path(__file__).resolve().parent.parent


def main():
    con = rag.connect()
    new = {i for (i,) in con.execute("SELECT id FROM chunks WHERE doc IN ('老計10号', '介護保険法')")}
    set_b = [json.loads(l) for l in open(ROOT / "data/set_b.jsonl")]
    set_b = [x for x in set_b if x["query"].strip()]
    qv = embed_queries([x["query"] for x in set_b])
    out = {}
    for x, v in zip(set_b, qv):
        ids = [c for c, _ in rag.bm25(con, x["query"], 20)] + [c for c, _ in rag.vector(con, v, 20, table="vec_flat")]
        hy = rag.hybrid(con, x["query"], v, 30)
        ids += [c for c, _ in hy[:20]] + [c for c, _ in rag.rerank(con, x["query"], hy, 20)]
        cand = [c for c in dict.fromkeys(ids) if c in new and str(c) not in x["judged"]]
        if cand:
            out[x["qa_id"]] = cand
    json.dump(out, open(ROOT / "data/unjudged_newdocs.json", "w"))
    print(len(out), "questions;", sum(map(len, out.values())), "candidates")


if __name__ == "__main__":
    main()
