"""エージェントに渡す道具の中身。モデルを読み込んだまま、localhost で検索と目次を返す。

- /search?q=      ハイブリッド(上位30)をリランカーで並べ直した上位8件
- /read?id=       チャンクの全文
- /docs           文書の一覧(PageIndex 方式の入口)
- /tree?node=     目次の1段(子の見出しと、葉のチャンク)
- /related?x=     GraphRAG: チャンク id なら用語と参照先、用語ならそれを含むチャンク(build_graph.py のグラフ)
ヘッダ X-Exclude: 隠すチャンク id(B の問いと中身が同じ Q&A。答えの写しを防ぐ)
使い方: uv run python src/server.py   (tool.py から呼ぶ)
"""
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).parent))
import rag
from embed import embed_queries

ROOT = Path(__file__).resolve().parent.parent
PORT = 8765
LOCK = threading.Lock()


def build_tree(con):
    """チャンクの見出しパスから、文書ごとの木を作る。Q&A集は 種別 > 項目 > 問い。"""
    nodes = {"root": {"title": "資料の一覧", "children": [], "leaves": []}}
    key2id = {}
    rows = con.execute("SELECT id, kind, doc, path, text FROM chunks ORDER BY id").fetchall()
    names = {r["doc"]: r["doc_name"] for r in map(json.loads, open(ROOT / "data/corpus.jsonl"))}

    def node(key, title, parent):
        if key not in key2id:
            nid = f"n{len(key2id) + 1}"
            key2id[key] = nid
            nodes[nid] = {"title": title, "children": [], "leaves": [], "parent": parent}
            nodes[parent]["children"].append(nid)
        return key2id[key]

    for cid, kind, doc, path, text in rows:
        cur = node((doc,), f"{doc}({names.get(doc, '')})", "root")
        parts = [p for p in path.split(" > ") if p] if path else []
        for i, p in enumerate(parts):
            cur = node((doc, *parts[: i + 1]), p, cur)
        if kind == "qa":
            q = text.split("\n問: ", 1)[-1].split("\n答: ")[0]
            label = "問: " + q[:60]
        else:
            body = text.split("\n", 1)[-1] if text.startswith("○") else text
            label = body.replace("\n", " ")[:60]
        nodes[cur]["leaves"].append((cid, label))
    return nodes


def count(nodes, nid, excl):
    n = nodes[nid]
    return sum(1 for c, _ in n["leaves"] if c not in excl) + sum(count(nodes, c, excl) for c in n["children"])


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def reply(self, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        excl = {int(x) for x in self.headers.get("X-Exclude", "").split(",") if x}
        with LOCK:
            if u.path == "/search":
                qv = embed_queries([q["q"]])[0]
                cand = [c for c in rag.hybrid(CON, q["q"], qv, 30 + len(excl)) if c[0] not in excl][:30]
                out = []
                for cid, s in rag.rerank(CON, q["q"], cand, 8):
                    doc, path, text = CON.execute("SELECT doc, path, text FROM chunks WHERE id=?", (cid,)).fetchone()
                    out.append({"id": cid, "doc": doc, "path": path, "text": text[:300]})
                self.reply(out)
            elif u.path == "/read":
                cid = int(q["id"])
                r = None if cid in excl else CON.execute("SELECT doc, path, text FROM chunks WHERE id=?", (cid,)).fetchone()
                self.reply({"id": cid, "doc": r[0], "path": r[1], "text": r[2]} if r else {"error": "not found"})
            elif u.path in ("/docs", "/tree"):
                nid = q.get("node", "root")
                if nid not in TREE:
                    return self.reply({"error": "no such node"})
                n = TREE[nid]
                self.reply({
                    "node": nid, "title": n["title"],
                    "children": [{"node": c, "title": TREE[c]["title"], "chunks": count(TREE, c, excl)}
                                 for c in n["children"] if count(TREE, c, excl)],
                    "chunks": [{"id": c, "head": l} for c, l in n["leaves"] if c not in excl],
                })
            elif u.path == "/related":
                # GraphRAG の道具: チャンクの用語と参照先、または用語を含むチャンク
                x = q["x"]
                if x.isdigit():
                    cid = int(x)
                    ents = CON.execute("SELECT e.name, e.df FROM mention m JOIN entity e ON e.id=m.entity "
                                       "WHERE m.chunk=? ORDER BY e.df", (cid,)).fetchall()
                    refs = CON.execute("SELECT r.dst, r.kind, c.doc, c.path FROM ref r JOIN chunks c ON c.id=r.dst WHERE r.src=? "
                                       "UNION SELECT r.src, '被参照', c.doc, c.path FROM ref r JOIN chunks c ON c.id=r.src WHERE r.dst=?",
                                       (cid, cid)).fetchall()
                    self.reply({"entities": [{"name": n, "chunks": df} for n, df in ents],
                                "refs": [{"id": d, "kind": k, "doc": doc, "path": p} for d, k, doc, p in refs if d not in excl][:20]})
                else:
                    rows = CON.execute("SELECT c.id, c.doc, c.path, c.text FROM entity e JOIN mention m ON m.entity=e.id "
                                       "JOIN chunks c ON c.id=m.chunk WHERE e.name=? ORDER BY c.kind DESC, c.id", (x,)).fetchall()
                    self.reply({"entity": x, "count": len(rows), "chunks": [
                        {"id": i, "doc": d, "path": p, "head": t.replace("\n", " ")[:80]} for i, d, p, t in rows if i not in excl][:30]})
            else:
                self.reply({"error": "unknown"})


if __name__ == "__main__":
    CON = rag.connect()
    CON.execute("SELECT 1")
    TREE = build_tree(CON)
    rag.rerank(CON, "準備", [(1, 0.0)], 1)  # リランカーを先に読み込む
    embed_queries(["準備"])
    print("ready", PORT, "nodes", len(TREE), flush=True)
    HTTPServer(("127.0.0.1", PORT), H).serve_forever()
