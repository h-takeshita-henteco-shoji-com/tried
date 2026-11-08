"""Microsoft GraphRAG(microsoft/graphrag 3.3.0)の索引から、問いごとに LLM へ渡すはずのチャンクを取り出す。

- 索引は graphrag の CLI で作る(data/msgraphrag/settings.yaml。LLM と埋め込みは src/llm_shim.py 経由)
- 入力は、こちらのチャンクを1件ずつ文書にしたもの(id = "c{チャンク id}")。text unit の document_id からチャンク id に戻す
- local: 問いに近い用語から、用語・関係・community 要約・text unit を集める。集めた text unit(Sources)を、並んだ順に採点する
- basic: text unit のベクトル検索。似ている順に採点する
- global と drift は、チャンクではなく community 要約を LLM に渡すので、検索としては採点できない
答えは作らせない(LLM を呼ばない)。問いの埋め込みだけ中継サーバーに頼む
使い方: /tmp/gr_ms/.venv/bin/python src/graph_msgraphrag.py [root]   -> results/lib_msgraphrag.json
"""
import json
import re
import sys
from pathlib import Path

import pandas as pd
from graphrag.config.embeddings import entity_description_embedding, text_unit_text_embedding
from graphrag.config.load_config import load_config
from graphrag.query.factory import get_basic_search_engine, get_local_search_engine
from graphrag.query.indexer_adapters import (read_indexer_entities, read_indexer_relationships,
                                             read_indexer_reports, read_indexer_text_units)
from graphrag.utils.api import get_embedding_store

ROOT = Path(__file__).resolve().parent.parent
K = 20


def main(root):
    cfg = load_config(root)
    out_dir = Path(root) / "output"
    t = {n: pd.read_parquet(out_dir / f"{n}.parquet") for n in
         ["entities", "communities", "community_reports", "text_units", "relationships"]}
    doc = dict(zip(t["text_units"]["human_readable_id"].astype(str), t["text_units"]["document_id"]))
    doc_by_id = dict(zip(t["text_units"]["id"], t["text_units"]["document_id"]))
    level = 2
    local = get_local_search_engine(
        config=cfg,
        reports=read_indexer_reports(t["community_reports"], t["communities"], level),
        text_units=read_indexer_text_units(t["text_units"]),
        entities=read_indexer_entities(t["entities"], t["communities"], level),
        relationships=read_indexer_relationships(t["relationships"]),
        covariates={"claims": []},
        description_embedding_store=get_embedding_store(config=cfg.vector_store, embedding_name=entity_description_embedding),
        response_type="multiple paragraphs", system_prompt="",
    )
    basic = get_basic_search_engine(
        config=cfg, text_units=read_indexer_text_units(t["text_units"]),
        text_unit_embeddings=get_embedding_store(config=cfg.vector_store, embedding_name=text_unit_text_embedding),
        response_type="multiple paragraphs", system_prompt="",
    )

    def cid(d):
        m = re.match(r"c(\d+)", str(d))
        return int(m.group(1)) if m else None

    def run_local(q):
        r = local.context_builder.build_context(query=q, **local.context_builder_params)
        src = r.context_records.get("sources")
        if src is None or src.empty:
            return []
        ids = [cid(doc.get(str(x))) for x in src["id"]]
        return list(dict.fromkeys(i for i in ids if i is not None))[:K]

    def run_basic(q):
        cb = basic.context_builder
        hits = cb.text_unit_embeddings.similarity_search_by_text(
            text=q, text_embedder=lambda s: cb.text_embedder.embedding(input=[s]).first_embedding, k=K)
        ids = [cid(doc_by_id.get(h.document.id)) for h in hits]
        return list(dict.fromkeys(i for i in ids if i is not None))[:K]

    qs = [json.loads(l)["query"] for l in open(ROOT / "data/set_a.jsonl")]
    qs += [json.loads(l)["query"] for l in open(ROOT / "data/set_b.jsonl")]
    qs = [q for q in dict.fromkeys(qs) if q.strip()]
    out = {"MS GraphRAG(local)": {}, "MS GraphRAG(basic)": {}}
    for i, q in enumerate(qs):
        out["MS GraphRAG(local)"][q] = run_local(q)
        out["MS GraphRAG(basic)"][q] = run_basic(q)
        if i % 20 == 0:
            print(i, len(qs), out["MS GraphRAG(local)"][q][:5], out["MS GraphRAG(basic)"][q][:5], flush=True)
    json.dump(out, open(ROOT / "results/lib_msgraphrag.json", "w"), ensure_ascii=False)
    print("done", len(qs))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "data/msgraphrag"))
