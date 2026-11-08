"""GraphRAG の土台: 用語と参照のグラフを、同じ SQLite に表として作る。LLM は使わない。

- 用語(entity): 見出し(「(22) 生活機能向上連携加算について」→「生活機能向上連携加算」)と、
  Q&A の項目名と、本文中の「〜加算」「〜減算」「〜介助」などから集める
- mention: チャンクが用語を含む(文字列の一致)
- ref: Q&A や通知の本文にある参照(「運営基準第25条」「留意事項通知第2の2(4)」「法第8条」)を、参照先のチャンクにつなぐ
表: entity(id, name, df), mention(entity, chunk), ref(src, dst, kind)
使い方: uv run python src/build_graph.py
"""
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rag

KAN = "〇一二三四五六七八九"
TERM = re.compile(r"[ァ-ヶー一-龠・]{2,24}(?:加算|減算|介助|援助|責任者|計画|基準|要件|体制|研修|サービス費)")
STRIP_HEAD = re.compile(r"^[\(（]?[0-9０-９一二三四五六七八九十]+[\)）]?[　 ]*|^[①-⑳][　 ]*|^[イロハニホヘトチリヌ][　 ]+")
STRIP_TAIL = re.compile(r"(について|の取扱い|に関する事項|の算定|に係る.*|等)$")
STOP = {"当該加算", "各加算", "本加算", "同加算", "上記加算", "居宅サービス計画", "サービス計画", "基準", "要件"}
MAX_DF = 400  # これより多くのチャンクに出る用語は、つながりとして意味が薄い


def kanji(n: int) -> str:
    """1〜999 を漢数字に(百二十三)。"""
    out = ""
    for v, u in ((100, "百"), (10, "十")):
        d, n = divmod(n, v)
        if d:
            out += ("" if d == 1 else KAN[d]) + u
    return out + (KAN[n] if n else "")


def norm(s):
    return unicodedata.normalize("NFKC", s)


def collect_terms(rows):
    terms = set()
    for cid, kind, doc, path, text in rows:
        for seg in (path or "").split(" > "):
            t = STRIP_TAIL.sub("", STRIP_HEAD.sub("", seg.split("　")[-1] if kind == "doc" else seg)).strip()
            if 3 <= len(t) <= 24 and not re.search(r"[0-9０-９、。()（）]", t):
                terms.add(t)
        terms.update(TERM.findall(text))
    return {t for t in terms if t not in STOP and not t.startswith(("の", "当該", "「", "人の", "新"))}


def build_refs(con, rows):
    """本文中の参照を、参照先のチャンクにつなぐ。見つからないものは捨てる。"""
    by_doc = defaultdict(list)
    for cid, kind, doc, path, text in rows:
        if kind == "doc":
            by_doc[doc].append((cid, norm(path or "")))

    def first(doc, *needles):
        for cid, p in by_doc[doc]:
            if all(n in p for n in needles):
                return cid
        return None

    out = []
    for cid, kind, doc, path, text in rows:
        t = norm(text)
        for m in re.finditer(r"(?:居宅サービス)?(?:運営基準|居宅基準)第(\d+)条", t):
            dst = first("省令37号", f"第{kanji(int(m.group(1)))}条")
            if dst:
                out.append((cid, dst, "運営基準"))
        for m in re.finditer(r"(?:介護保険)?法第(\d+)条", t):
            if "運営基準" in t[max(0, m.start() - 6) : m.start()]:
                continue
            dst = first("介護保険法", f"第{kanji(int(m.group(1)))}条")
            if dst:
                out.append((cid, dst, "法"))
        for m in re.finditer(r"(?:留意事項通知|老企第?36号)第(\d+)\s*の\s*(\d+)\s*[\(（]\s*(\d+)\s*[\)）]", t):
            a, b, c = (int(x) for x in m.groups())
            dst = first("老企36号", f"第{kanji(a)}", f"> {b} ", f"({c})")
            if dst:
                out.append((cid, dst, "留意事項通知"))
    return sorted(set(o for o in out if o[0] != o[1]))


def main():
    con = rag.connect()
    rows = con.execute("SELECT id, kind, doc, path, text FROM chunks").fetchall()
    terms = collect_terms(rows)
    print("候補の用語", len(terms))
    mention = defaultdict(set)
    for cid, kind, doc, path, text in rows:
        body = (path or "") + "\n" + text
        for t in terms:
            if t in body:
                mention[t].add(cid)
    keep = {t: ids for t, ids in mention.items() if 2 <= len(ids) <= MAX_DF}
    # 長い用語に含まれる短い用語は、同じチャンクでは長い方だけ数える(「処遇改善加算」と「介護職員処遇改善加算」)
    con.executescript("""
        DROP TABLE IF EXISTS entity; DROP TABLE IF EXISTS mention; DROP TABLE IF EXISTS ref;
        CREATE TABLE entity(id INTEGER PRIMARY KEY, name TEXT UNIQUE, df INTEGER);
        CREATE TABLE mention(entity INTEGER, chunk INTEGER, PRIMARY KEY(entity, chunk));
        CREATE INDEX mention_chunk ON mention(chunk);
        CREATE TABLE ref(src INTEGER, dst INTEGER, kind TEXT);
        CREATE INDEX ref_src ON ref(src); CREATE INDEX ref_dst ON ref(dst);
    """)
    for i, (t, ids) in enumerate(sorted(keep.items()), 1):
        con.execute("INSERT INTO entity VALUES(?,?,?)", (i, t, len(ids)))
        con.executemany("INSERT INTO mention VALUES(?,?)", [(i, c) for c in ids])
    refs = build_refs(con, rows)
    con.executemany("INSERT INTO ref VALUES(?,?,?)", refs)
    con.commit()
    n_m = con.execute("SELECT count(*) FROM mention").fetchone()[0]
    print("用語", len(keep), "mention", n_m, "ref", len(refs),
          {k: sum(1 for r in refs if r[2] == k) for k in ("運営基準", "法", "留意事項通知")})


if __name__ == "__main__":
    main()
