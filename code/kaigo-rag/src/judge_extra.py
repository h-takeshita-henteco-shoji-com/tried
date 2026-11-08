"""pool を広げる: 新しい方式が上位に出した、まだ判定していない候補を判定して set_b.jsonl に足す。

入力: 判定していない候補 {qa_id: [chunk_id, ...]} の JSON ファイル
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rag
from make_set_b import judge

ROOT = Path(__file__).resolve().parent.parent


def main(path: str):
    extra = json.load(open(path))
    rows = [json.loads(l) for l in open(ROOT / "data/set_b.jsonl")]
    items = [{"qa_id": r["qa_id"], "query": r["query"], "answer": r["answer"],
              "pool": [c for c in extra.get(r["qa_id"], []) if str(c) not in r["judged"]]} for r in rows]
    items = [it for it in items if it["pool"]]

    with ThreadPoolExecutor(4) as ex:
        results = dict(zip([it["qa_id"] for it in items], ex.map(lambda it: judge(it, rag.DB), items)))
    n = 0
    for r in rows:
        for cid, g in results.get(r["qa_id"], {}).items():
            r["judged"][str(cid)] = g
            n += 1
    with open(ROOT / "data/set_b.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("added", n, "judgments; new grade2:", sum(1 for d in results.values() for g in d.values() if g == 2))


if __name__ == "__main__":
    main(sys.argv[1])
