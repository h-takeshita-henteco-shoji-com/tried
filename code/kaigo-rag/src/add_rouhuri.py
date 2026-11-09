"""老振76号(指定訪問介護事業所の事業運営の取扱等について)の別紙「一般的に介護保険の生活援助の範囲に含まれない
と考えられる事例」を、コーパスの末尾に1件として足す。#155(介護保険でできることを説明させる)の根拠の本命。

- 厚労省の元の PDF は見つからなかった。さいたま市が転載した別紙から取った
  https://www.city.saitama.lg.jp/005/001/018/005/p041941_d/fil/03_houmongai_02_bessi.pdf
- 本文の要点(保険外のサービスとして提供するのは可能、市町村に連絡、ほかの支援を助言)を頭に足す
使い方: uv run python src/add_rouhuri.py   (2回走らせても重複しない)
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import rag
from embed import DOC_PREFIX, model

ROOT = Path(__file__).resolve().parent.parent
TEXT = """一般的に介護保険の生活援助の範囲に含まれないと考えられる事例
1.「直接本人の援助」に該当しない行為
主として家族の利便に供する行為又は家族が行うことが適当であると判断される行為
・利用者以外のものに係る洗濯、調理、買い物、布団干し
・主として利用者が使用する居室等以外の掃除
・来客の応接(お茶・食事の手配等)
・自家用車の洗車、清掃 等
2.「日常生活の援助」に該当しない行為
① 訪問介護員が行わなくとも日常生活を営むのに支障が生じないと判断される行為
・草むしり
・花木の水やり
・犬の散歩等ペットの世話 等
② 日常的に行われる家事の範囲を超える行為
・家具・電気器具等の移動、修繕、模様替え
・大掃除、窓のガラス拭き、床のワックスがけ
・室内外家屋の修理、ペンキ塗り
・植木の剪定等の園芸
・正月、節句等のために特別な手間をかけて行う調理 等
(本文の要点)保険給付の範囲外のサービスについて、利用者と事業者との間の契約に基づき、保険外のサービスとして、保険給付対象サービスと明確に区分し、利用者の自己負担によってサービスを提供することは、当然、可能である。"""


def main():
    rows = [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]
    rows = [r for r in rows if r["doc"] != "老振76号"]
    cid = max(r["id"] for r in rows) + 1
    r = {"id": cid, "doc_type": "通知", "doc": "老振76号", "doc_name": "指定訪問介護事業所の事業運営の取扱等について",
         "version": "H15.3", "current": 1, "path": "別紙 一般的に介護保険の生活援助の範囲に含まれないと考えられる事例",
         "part": 0, "text": TEXT, "kind": "doc", "qa_id": None, "year": None}
    with open(ROOT / "data/corpus.jsonl", "w") as f:
        for x in rows + [r]:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    v = model().encode([DOC_PREFIX + TEXT], normalize_embeddings=True)[0].astype(np.float32)
    con = rag.connect()
    old = [i for (i,) in con.execute("SELECT id FROM chunks WHERE doc='老振76号'")]
    for i in old + [cid]:
        con.execute("DELETE FROM chunks WHERE id=?", (i,))
        for t in ("fts", "vec_flat", "vec_ann"):
            con.execute(f"DELETE FROM {t} WHERE rowid=?", (i,))
    con.execute("INSERT INTO chunks VALUES(?,?,?,?,?,?,?,?,?,?)",
                (cid, "doc", r["doc_type"], r["doc"], r["version"], 1, r["path"], None, None, TEXT))
    con.execute("INSERT INTO fts(rowid, tok) VALUES(?,?)", (cid, " ".join(rag.tokenize(TEXT))))
    for t in ("vec_flat", "vec_ann"):
        con.execute(f"INSERT INTO {t}(rowid, vector, kind, current) VALUES(?,?,?,?)", (cid, v.tobytes(), "doc", 1))
    con.commit()
    print("added", cid, "rows", con.execute("SELECT count(*) FROM chunks").fetchone()[0])


if __name__ == "__main__":
    main()
