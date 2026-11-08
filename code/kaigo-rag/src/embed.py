"""コーパスを ruri-v3-310m で埋め込む。

出力: data/emb_ruri310m.npy(float32、正規化済み、行は corpus の id-1)
"""
import json
import time
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent
MODEL = "cl-nagoya/ruri-v3-310m"
DOC_PREFIX = "検索文書: "
QUERY_PREFIX = "検索クエリ: "

_model = None


def model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL, device="mps")
        _model.max_seq_length = 1024
    return _model


def embed_queries(qs: list[str]) -> np.ndarray:
    return model().encode([QUERY_PREFIX + q for q in qs], batch_size=32, normalize_embeddings=True).astype(np.float32)


def main():
    rows = [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]
    texts = [DOC_PREFIX + r["text"] for r in rows]
    # 長さ順に並べてから埋め込むと、詰め物が減って速い
    # 手元のメモリが少ないため、小さな束で進め、途中経過を保存する
    order = np.argsort([len(t) for t in texts])
    part = ROOT / "data/emb_partial.npy"
    out = np.load(part) if part.exists() else np.zeros((len(texts), 768), dtype=np.float32)
    done = np.abs(out).sum(axis=1) > 0
    todo = [i for i in order if not done[i]]
    t0 = time.time()
    STEP = 256
    for k in range(0, len(todo), STEP):
        idx = todo[k : k + STEP]
        out[idx] = model().encode([texts[i] for i in idx], batch_size=4, normalize_embeddings=True)
        np.save(part, out)
        print(f"{k + len(idx)}/{len(todo)} {time.time() - t0:.0f}s", flush=True)
    np.save(ROOT / "data/emb_ruri310m.npy", out.astype(np.float32))
    part.unlink()
    print(out.shape, f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
