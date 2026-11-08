"""資料を足す: 老計10号と介護保険法。既存の id を動かさないよう、コーパスの末尾に足す。

- 老計10号: 枚方市が載せている通知の全文(平成30年改正の溶け込み版、PDF)。厚労省は改正通知だけを PDF で出している
- 介護保険法: 全老健「法令・Q&A検索システム」(uid=1)
既存の DB(chunks、fts、vec_flat、vec_ann)に行を足す。vec1 の ANN は学習済みの区画にそのまま入る
注意: build_corpus.py を回し直したら、これも回し直す
使い方: uv run python src/add_docs.py
"""
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import chunk_docs
import fetch
import rag
from embed import DOC_PREFIX, model

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw"
ROKEI10_PDF = "https://www.city.hirakata.osaka.jp/cmsfiles/contents/0000046/46318/tsuuchi_houmon_10.pdf"
EXTRA = ROOT / "data/chunks_extra.jsonl"

# 老計10号の見出し: 「１ 身体介護」「１－０ サービス準備・記録等」「１－１－１ 排泄介助」など
Z = "０-９0-9"
R10_HEAD = re.compile(rf"^([{Z}]+([―－][{Z}]+)+[ 　]*|[{Z}]+[ 　]+)[^ 　{Z}―－]")
BULLET = re.compile(r"^(○|・|※|（|\(|[①-⑳])")


def rokei10_chunks():
    pdf = RAW / "rokei10/hirakata.pdf"
    if not pdf.exists():
        pdf.parent.mkdir(parents=True, exist_ok=True)
        pdf.write_bytes(fetch.get(ROKEI10_PDF))
    raw = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout
    # PDF の折り返しをつなぐ。見出しと箇条の頭では改行を残す
    lines, num = [], ""
    for l in (x.strip() for x in raw.splitlines()):
        if not l or re.fullmatch(r"[-‐ 0-9]+", l):  # ページ番号
            continue
        if re.fullmatch(rf"[{Z}]+([―－][{Z}]+)*", l):  # 見出しの番号だけの行は、次の行(見出しの名前)とつなぐ
            num = l
            continue
        if num:
            l, num = f"{num} {l}", ""
        if lines and not R10_HEAD.match(l) and not BULLET.match(l) and not R10_HEAD.match(lines[-1]) \
                and not lines[-1].endswith(("。", "）")):
            lines[-1] += l
        else:
            lines.append(l)
    # 見出しの深さ: 「１」=0、「１－１」=1、「１－１－１」=2
    stack, sections, cur, path = {}, [], [], []
    for l in lines:
        m = R10_HEAD.match(l)
        if m and len(l) < 40:
            if cur:
                sections.append((path, cur))
            lv = len(re.findall("[―－]", re.match(rf"[{Z}―－]+", l).group(0)))
            stack = {k: v for k, v in stack.items() if k < lv}
            stack[lv] = l
            path = [stack[k] for k in sorted(stack)]
            cur = [l]
        else:
            cur.append(l)
    if cur:
        sections.append((path, cur))
    # 見出しだけの小さな節は、次の節の頭に寄せる(chunk_docs.py と同じ)
    merged, carry = [], []
    for path, sec in sections:
        if sum(map(len, carry + sec)) < 80:
            carry += sec
            continue
        merged.append((path, carry + sec))
        carry = []
    if carry:
        merged.append((sections[-1][0], carry))
    out = []
    for path, sec in merged:
        pieces = chunk_docs.split_long(sec) if sum(map(len, sec)) > chunk_docs.MAX_CHARS else [sec]
        for j, p in enumerate(pieces):
            out.append({"doc_type": "通知", "doc": "老計10号", "doc_name": "訪問介護におけるサービス行為ごとの区分等について",
                        "version": "H30.3", "current": 1, "path": " > ".join(path), "part": j, "text": "\n".join(p)})
    return out


def law_chunks():
    f = RAW / "roken_1.txt"
    if not f.exists():
        t = fetch.get("https://hourei.roken.or.jp/detail.php?uid=1").decode("utf-8", "replace")
        f.write_text(fetch.to_text(t))
        time.sleep(1)
    chunk_docs.DOCS[1] = ("法律", "介護保険法", "介護保険法", "R7")
    # 訪問介護の請求に関わる章だけを使う(総則、保険給付、事業者及び施設)。附則と保険料・財政の章は外す
    keep = ("第一章", "第四章", "第五章")
    return [c for c in chunk_docs.chunk_doc(1) if c["path"].startswith(keep)]


def main():
    rows = [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]
    rows = [r for r in rows if r["doc"] not in ("老計10号", "介護保険法")]
    new = rokei10_chunks() + law_chunks()
    start = max(r["id"] for r in rows) + 1
    new = [{"id": start + i, **c, "kind": "doc", "qa_id": None, "year": None} for i, c in enumerate(new)]
    for d in ("老計10号", "介護保険法"):
        cs = [c for c in new if c["doc"] == d]
        print(d, len(cs), "chunks", "avg", sum(len(c["text"]) for c in cs) // len(cs))
    with open(ROOT / "data/corpus.jsonl", "w") as f:
        for r in rows + new:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(EXTRA, "w") as f:
        for r in new:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    t0 = time.time()
    emb = model().encode([DOC_PREFIX + r["text"] for r in new], batch_size=4, normalize_embeddings=True)
    print("embedded", len(new), f"{time.time() - t0:.0f}s")
    np.save(ROOT / "data/emb_extra.npy", emb)

    con = rag.connect()
    con.execute("DELETE FROM chunks WHERE id >= ?", (start,))
    for t in ("fts", "vec_flat", "vec_ann"):
        con.execute(f"DELETE FROM {t} WHERE rowid >= ?", (start,))
    for r, v in zip(new, emb):
        con.execute("INSERT INTO chunks VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (r["id"], r["kind"], r["doc_type"], r["doc"], r["version"], r["current"], r["path"], None, None, r["text"]))
        con.execute("INSERT INTO fts(rowid, tok) VALUES(?,?)", (r["id"], " ".join(rag.tokenize(r["text"]))))
        for t in ("vec_flat", "vec_ann"):
            con.execute(f"INSERT INTO {t}(rowid, vector, kind, current) VALUES(?,?,?,?)",
                        (r["id"], v.astype(np.float32).tobytes(), r["kind"], r["current"]))
    con.commit()
    print("db rows", con.execute("SELECT count(*) FROM chunks").fetchone()[0])


if __name__ == "__main__":
    main()
