"""文書チャンクと Q&A をまとめて、検索の対象(コーパス)にする。B の40問はここで外す。

出力: data/corpus.jsonl(id は 1 から振る)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    split = json.load(open(ROOT / "data/split.json"))
    held = set(split["set_b_heldout"])
    docs = [json.loads(l) for l in open(ROOT / "data/chunks_docs.jsonl")]
    qa = [json.loads(l) for l in open(ROOT / "data/qa_all.jsonl")]

    rows = []
    for c in docs:
        rows.append({**c, "kind": "doc", "qa_id": None, "year": None})
    for x in qa:
        if x["qa_id"] in held:
            continue
        text = f"【Q&A】{x['item']}\n問: {x['question']}\n答: {x['answer']}"
        rows.append(
            {
                "kind": "qa", "doc_type": "QA", "doc": "Q&A集", "doc_name": "介護サービス関係Q&A集",
                "version": "R8.9", "current": 1, "path": f"{x['service']} > {x['item']}", "part": 0,
                "text": text, "qa_id": x["qa_id"], "year": x["year"], "source": x["source"],
            }
        )
    with open(ROOT / "data/corpus.jsonl", "w") as f:
        for i, r in enumerate(rows, 1):
            f.write(json.dumps({"id": i, **r}, ensure_ascii=False) + "\n")
    print(len(rows), "rows;", sum(r["kind"] == "doc" for r in rows), "doc,", sum(r["kind"] == "qa" for r in rows), "qa")


if __name__ == "__main__":
    main()
