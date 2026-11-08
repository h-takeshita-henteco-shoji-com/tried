"""SQLite に、FTS5(BM25)と vec1(flat と ANN)の索引を作る。"""
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import rag

ROOT = Path(__file__).resolve().parent.parent
# 約6,100件。nbucket は件数の平方根の目安、opq は codesize 32 が推奨値
ANN = {"distance": "cos", "nbucket": 80, "codesize": 32, "quantizer": "opq"}

if __name__ == "__main__":
    t0 = time.time()
    con = rag.build(ROOT / "data/emb_ruri310m.npy", ANN)
    n = con.execute("SELECT count(*) FROM chunks").fetchone()[0]
    print(n, "chunks", f"{time.time() - t0:.1f}s", "db", f"{rag.DB.stat().st_size / 1e6:.1f}MB")
