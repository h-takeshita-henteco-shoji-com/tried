"""GraphRAG の候補で、上位10件に入った未判定のチャンクを集める。出力: data/unjudged_graph.json(judge_extra.py に渡す)"""
import json, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
import rag, evaluate as ev
from embed import embed_queries
con = rag.connect()
b = [json.loads(l) for l in open("data/set_b.jsonl")]
b = [x for x in b if x["query"].strip()]
qv = embed_queries([x["query"] for x in b])
out = {}
for x, v in zip(b, qv):
    ids = []
    for n in ["グラフだけ(問いの用語+上位3件の用語と参照)", "GraphRAG(ハイブリッド+グラフ)", "GraphRAG(ハイブリッド+グラフ)+リランカー"]:
        ids += [c for c, _ in ev.GRAPH[n](con, x["query"], v, 10)]
    c = [i for i in dict.fromkeys(ids) if str(i) not in x["judged"]]
    if c:
        out[x["qa_id"]] = c
json.dump(out, open("data/unjudged_graph.json", "w"))
print(len(out), sum(map(len, out.values())))
