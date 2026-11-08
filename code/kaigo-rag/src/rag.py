"""SQLite 1つで、BM25(FTS5)、ベクトル検索(vec1)、ハイブリッド(RRF)を行う。"""
import json
import sqlite3
import unicodedata
from pathlib import Path

import numpy as np
from fugashi import Tagger

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data/kaigo.db"
VEC1 = str(ROOT / "ext/vec1")

KEEP_POS = {"名詞", "動詞", "形容詞", "副詞", "接頭辞"}
STOP = {"する", "ある", "いる", "なる", "できる", "れる", "られる", "こと", "もの", "よう", "ため", "場合",
        "とき", "の", "ん", "これ", "それ", "どう", "そう", "いう", "やる", "思う", "行う"}
_tagger = Tagger()


def tokenize(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text)
    out = []
    for w in _tagger(text):
        pos = w.feature.pos1
        if pos not in KEEP_POS:
            continue
        lemma = w.feature.lemma if pos in ("動詞", "形容詞") and w.feature.lemma else w.surface
        lemma = lemma.split("-")[0]
        if lemma in STOP or len(lemma) == 0:
            continue
        out.append(lemma)
    return out


def connect(path=DB) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.enable_load_extension(True)
    con.load_extension(VEC1)
    return con


def build(emb_path: Path, ann_params: dict):
    rows = [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]
    emb = np.load(emb_path)
    if DB.exists():
        DB.unlink()
    con = connect()
    con.executescript(
        """
        CREATE TABLE chunks(id INTEGER PRIMARY KEY, kind TEXT, doc_type TEXT, doc TEXT, version TEXT,
            current INTEGER, path TEXT, qa_id TEXT, year INTEGER, text TEXT);
        CREATE VIRTUAL TABLE fts USING fts5(tok, tokenize='unicode61');
        CREATE VIRTUAL TABLE vec_flat USING vec1(vector, kind, current);
        CREATE VIRTUAL TABLE vec_ann USING vec1(vector, kind, current);
        """
    )
    for r in rows:
        con.execute(
            "INSERT INTO chunks VALUES(?,?,?,?,?,?,?,?,?,?)",
            (r["id"], r["kind"], r["doc_type"], r["doc"], r["version"], r["current"], r["path"], r["qa_id"], r["year"], r["text"]),
        )
        con.execute("INSERT INTO fts(rowid, tok) VALUES(?,?)", (r["id"], " ".join(tokenize(r["text"]))))
        v = emb[r["id"] - 1].tobytes()
        for t in ("vec_flat", "vec_ann"):
            con.execute(f"INSERT INTO {t}(rowid, vector, kind, current) VALUES(?,?,?,?)", (r["id"], v, r["kind"], r["current"]))
    con.commit()
    con.execute("SELECT vec1_config('nthread', 8)")
    con.execute("INSERT INTO vec_flat(cmd, arg) VALUES('rebuild', ?)", (json.dumps({"index": "flat", "distance": "cos"}),))
    model = con.execute("SELECT vec1_train(vector, ?) FROM vec_ann", (json.dumps(ann_params),)).fetchone()[0]
    con.execute("INSERT INTO vec_ann(cmd, arg) VALUES('rebuild', ?)", (model,))
    con.commit()
    return con


# ---- 検索。どれも [(chunk_id, score)] を良い順に返す ----

def bm25(con, query: str, k: int = 10, table: str = "fts"):
    toks = list(dict.fromkeys(tokenize(query)))
    if not toks:
        return []
    m = " OR ".join('"' + t.replace('"', "") + '"' for t in toks)
    return con.execute(f"SELECT rowid, bm25({table}) FROM {table} WHERE {table} MATCH ? ORDER BY bm25({table}) LIMIT ?",
                       (m, k)).fetchall()


def vector(con, qv: np.ndarray, k: int = 10, table: str = "vec_ann", nprobe=0.1, rerank: int = 100):
    b = qv.astype(np.float32).tobytes()
    if table != "vec_ann":  # flat(厳密)の表
        sql = f"SELECT rowid, vec1_cos_distance(?, vector) d FROM {table}(?, '{{K:{k}}}') ORDER BY d LIMIT ?"
        return con.execute(sql, (b, b, k)).fetchall()
    # ANN は圧縮した値で候補を多めに取り、元のベクトルで並べ直す(rerank)
    kk = max(k, rerank)
    sql = (f"SELECT rowid, vec1_cos_distance(?, vector) d FROM {table}(?, '{{K:{kk}, nprobe:{nprobe}}}') "
           f"ORDER BY d LIMIT ?")
    return con.execute(sql, (b, b, k)).fetchall()


def rrf(*ranked_lists, k: int = 10, c: int = 60):
    score: dict[int, float] = {}
    for lst in ranked_lists:
        for rank, (cid, _) in enumerate(lst):
            score[cid] = score.get(cid, 0.0) + 1.0 / (c + rank + 1)
    return sorted(score.items(), key=lambda x: -x[1])[:k]


def hybrid(con, query: str, qv: np.ndarray, k: int = 10, pool: int = 100, fts: str = "fts", vec: str = "vec_ann"):
    return rrf(bm25(con, query, pool, table=fts), vector(con, qv, pool, table=vec, nprobe=0.4), k=k)


# ---- リランカー(cross-encoder) ----
RERANKER = "cl-nagoya/ruri-v3-reranker-310m"
_ce = None


def rerank(con, query: str, cands: list, k: int = 10):
    """候補 [(chunk_id, _)] を、問いと本文を一緒に読むモデルで並べ直す。"""
    global _ce
    if _ce is None:
        from sentence_transformers import CrossEncoder
        _ce = CrossEncoder(RERANKER, device="mps", max_length=1024)
    ids = [c for c, _ in cands]
    texts = [con.execute("SELECT text FROM chunks WHERE id=?", (i,)).fetchone()[0] for i in ids]
    scores = _ce.predict([(query, t) for t in texts], batch_size=4)
    return sorted(zip(ids, map(float, scores)), key=lambda x: -x[1])[:k]


# ---- GraphRAG: 用語と参照のグラフ(build_graph.py)をたどる ----

_ents = None


def query_entities(con, query: str):
    """問いの文字列に含まれる用語。長い用語に含まれる短い用語は除く。"""
    global _ents
    if _ents is None:
        _ents = con.execute("SELECT id, name, df FROM entity").fetchall()
    q = unicodedata.normalize("NFKC", query)
    hit = [(i, n, df) for i, n, df in _ents if unicodedata.normalize("NFKC", n) in q]
    return [h for h in hit if not any(h[1] != o[1] and h[1] in o[1] for o in hit)]


def graph(con, query: str, seeds: list, k: int = 50, n_seed: int = 3, seed_df: int = 50):
    """グラフで候補を広げる。
    - 問いに含まれる用語と、上位 n_seed 件のチャンクが含む珍しい用語(df<=seed_df)を起点にする
    - 起点の用語を含むチャンクに、用語の珍しさ(idf)を足し上げた点を付ける
    - 上位のチャンクから参照でつながるチャンク(両向き)にも点を足す
    """
    import math
    n = con.execute("SELECT count(*) FROM chunks").fetchone()[0]
    ents = {i: df for i, _, df in query_entities(con, query)}
    top = [c for c, _ in seeds[:n_seed]]
    for c in top:
        for i, df in con.execute("SELECT e.id, e.df FROM mention m JOIN entity e ON e.id=m.entity WHERE m.chunk=?", (c,)):
            if df <= seed_df:
                ents.setdefault(i, df)
    score: dict[int, float] = {}
    for i, df in ents.items():
        w = math.log(n / df)
        for (c,) in con.execute("SELECT chunk FROM mention WHERE entity=?", (i,)):
            score[c] = score.get(c, 0.0) + w
    for c in top:
        for (d,) in con.execute("SELECT dst FROM ref WHERE src=? UNION SELECT src FROM ref WHERE dst=?", (c, c)):
            score[d] = score.get(d, 0.0) + math.log(n)
    return sorted(score.items(), key=lambda x: -x[1])[:k]


def graph_hybrid(con, query: str, qv, k: int = 10, pool: int = 100):
    """ハイブリッドの結果と、グラフで広げた候補を RRF で混ぜる。"""
    hy = hybrid(con, query, qv, pool)
    return rrf(hy, graph(con, query, hy, pool), k=k)
