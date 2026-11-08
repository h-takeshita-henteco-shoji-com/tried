"""vec1 ANN の nprobe と rerank の効き方を測る。厳密検索(flat)の上位10件をどれだけ再現できるか。"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import rag
from embed import embed_queries

ROOT = Path(__file__).resolve().parent.parent
con = rag.connect()
set_a = [json.loads(l) for l in open(ROOT / "data/set_a.jsonl")]
qv = embed_queries([x["query"] for x in set_a])
exact = [[c for c, _ in rag.vector(con, v, 10, table="vec_flat")] for v in qv]
print("| nprobe | rerank | flat上位10の再現率 | ms/問 |")
print("|---|---|---|---|")
for nprobe in (0.025, 0.05, 0.1, 0.2, 0.4, 1.0, 80):
    for rr in (10, 100):
        t0 = time.perf_counter(); got = []
        for v in qv:
            if rr == 10:
                b = v.tobytes()
                got.append([c for (c,) in con.execute(f"SELECT rowid FROM vec_ann(?, '{{K:10, nprobe:{nprobe}}}')", (b,))])
            else:
                got.append([c for c, _ in rag.vector(con, v, 10, nprobe=nprobe, rerank=rr)])
        ms = (time.perf_counter() - t0) / len(qv) * 1000
        rec = sum(len(set(g) & set(e)) for g, e in zip(got, exact)) / (10 * len(qv))
        print(f"| {nprobe} | {'なし' if rr == 10 else rr} | {rec:.3f} | {ms:.2f} |")
