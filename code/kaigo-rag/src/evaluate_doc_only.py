"""B のうち、告示・通知だけを対象にした採点。文脈を足す方式は告示・通知にしか効かないため、分けて測る。

- 正解: 判定2のうち、告示・省令・通知のチャンク
- 結果: 各方式の上位200件から、告示・省令・通知だけを残して上位10件
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import evaluate as ev
import rag
from embed import DOC_PREFIX, embed_queries, model

ROOT = Path(__file__).resolve().parent.parent
K, POOL = 10, 200


def main():
    con = rag.connect()
    is_doc = {i for (i,) in con.execute("SELECT id FROM chunks WHERE kind='doc'")}
    qa = {json.loads(l)["qa_id"]: json.loads(l) for l in open(ROOT / "data/qa_all.jsonl")}
    set_b = [json.loads(l) for l in open(ROOT / "data/set_b.jsonl")]
    set_b = [x for x in set_b if qa[x["qa_id"]]["question"].strip()
             and any(v == 2 and int(k) in is_doc for k, v in x["judged"].items())]
    qv = embed_queries([x["query"] for x in set_b])
    hy = {json.loads(l)["query"]: json.loads(l)["hyde"] for l in open(ROOT / "data/hyde.jsonl")}
    hv = model().encode([DOC_PREFIX + hy[x["query"]] for x in set_b], normalize_embeddings=True)
    ev.HYDE.update({x["query"]: v.astype(np.float32) for x, v in zip(set_b, hv)})

    names = [n for n in ev.SMART if "リランカー" not in n] + ["ハイブリッド+リランカー(上位30)", "Contextual(ハイブリッド)+リランカー"]
    print(f"B(告示・通知の根拠がある問い): {len(set_b)}問")
    print("| 方式 | hit@10 | recall@10 |")
    print("|---|---|---|")
    for n in names:
        hits, recs = [], []
        for x, v in zip(set_b, qv):
            gold = {int(k) for k, g in x["judged"].items() if g == 2 and int(k) in is_doc}
            if "リランカー" in n:
                # リランカーは、告示・通知だけの候補30件を並べ直す
                fts, vec = ("fts_ctx", "vec_ctx") if "Contextual" in n else ("fts", "vec_ann")
                cand = [c for c in rag.hybrid(con, x["query"], v, POOL, fts=fts, vec=vec) if c[0] in is_doc][:30]
                ids = [c for c, _ in rag.rerank(con, x["query"], cand, K)]
            else:
                ids = [c for c, _ in ev.SMART[n](con, x["query"], v, POOL) if c in is_doc][:K]
            got = gold & set(ids)
            hits.append(1 if got else 0)
            recs.append(len(got) / min(len(gold), K))
        print(f"| {n} | {sum(hits) / len(hits):.2f} | {sum(recs) / len(recs):.2f} |", flush=True)


if __name__ == "__main__":
    main()
