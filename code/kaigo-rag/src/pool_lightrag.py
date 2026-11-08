"""ライブラリの方式で、上位10件に入った未判定のチャンクを集める。judge_extra.py に渡す。
使い方: uv run python src/pool_lightrag.py [lightrag|msgraphrag]   results/lib_{名前}.json -> data/unjudged_{名前}.json
"""
import json
import sys
name = sys.argv[1] if len(sys.argv) > 1 else "lightrag"
d = json.load(open(f"results/lib_{name}.json"))
b = [json.loads(l) for l in open("data/set_b.jsonl")]
out = {}
for x in b:
    if not x["query"].strip():
        continue
    ids = [c for v in d.values() for c in v.get(x["query"], [])[:10]]
    c = [i for i in dict.fromkeys(ids) if str(i) not in x["judged"]]
    if c:
        out[x["qa_id"]] = c
json.dump(out, open(f"data/unjudged_{name}.json", "w"))
print(len(out), sum(map(len, out.values())))
