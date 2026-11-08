"""チャンクの頭に文脈を足した版を作り、同じ DB に FTS5 と vec1(flat)の表を足す。

- path: 見出しのパスを機械的に足す(Q&A は種別と項目)
- ctx : Contextual Retrieval。文書チャンクは Claude が書いた位置づけの文を足す。Q&A は path と同じ
使い方: uv run python src/build_variants.py path|ctx
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import rag
from embed import DOC_PREFIX, model

ROOT = Path(__file__).resolve().parent.parent


def texts_for(variant: str, rows):
    ctx = {}
    if variant == "ctx":
        ctx = {json.loads(l)["id"]: json.loads(l)["context"] for l in open(ROOT / "data/context_doc.jsonl")}
    out = []
    for r in rows:
        if r["kind"] == "qa":
            head = f"{r['doc_name']} > {r['path']}"
        elif variant == "path":
            head = f"{r['doc']}({r['doc_name']}) > {r['path']}"
        else:
            head = f"{r['doc']}: {ctx.get(r['id'], '')}"
        out.append(head + "\n" + r["text"])
    return out


def embed_all(texts, cache: Path):
    order = np.argsort([len(t) for t in texts])
    out = np.load(cache) if cache.exists() else np.zeros((len(texts), 768), dtype=np.float32)
    todo = [i for i in order if not np.abs(out[i]).sum() > 0]
    t0 = time.time()
    for k in range(0, len(todo), 256):
        idx = todo[k : k + 256]
        out[idx] = model().encode([DOC_PREFIX + texts[i] for i in idx], batch_size=4, normalize_embeddings=True)
        np.save(cache, out)
        print(f"{k + len(idx)}/{len(todo)} {time.time() - t0:.0f}s", flush=True)
    return out


def main(variant: str):
    rows = [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]
    texts = texts_for(variant, rows)
    emb = embed_all(texts, ROOT / f"data/emb_{variant}.npy")
    con = rag.connect()
    con.executescript(f"""
        DROP TABLE IF EXISTS fts_{variant};
        DROP TABLE IF EXISTS vec_{variant};
        CREATE VIRTUAL TABLE fts_{variant} USING fts5(tok, tokenize='unicode61');
        CREATE VIRTUAL TABLE vec_{variant} USING vec1(vector, kind, current);
    """)
    for r, t in zip(rows, texts):
        con.execute(f"INSERT INTO fts_{variant}(rowid, tok) VALUES(?,?)", (r["id"], " ".join(rag.tokenize(t))))
        con.execute(f"INSERT INTO vec_{variant}(rowid, vector, kind, current) VALUES(?,?,?,?)",
                    (r["id"], emb[r["id"] - 1].tobytes(), r["kind"], r["current"]))
    con.execute(f"INSERT INTO vec_{variant}(cmd, arg) VALUES('rebuild', ?)", (json.dumps({"index": "flat", "distance": "cos"}),))
    con.commit()
    print("ok", variant)


if __name__ == "__main__":
    main(sys.argv[1])
