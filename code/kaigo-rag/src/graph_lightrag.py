"""LightRAG(HKUDS/LightRAG)で、訪問介護の範囲(data/subset_houmon.json)のグラフを作り、引く。

- LLM: claude -p(索引づくりは Haiku)。LightRAG の LLM 関数として差し込む
- 埋め込み: ruri-v3-310m(手元)。LightRAG は用語・関係・チャンクの3種を埋め込む。文書の接頭辞で揃える
- チャンク: こちらのチャンクを1件ずつ文書として入れる(LightRAG の中で切り直されない長さ)。file_path にチャンク id を持たせ、引いた結果を id に戻す
使い方:
  uv run python src/graph_lightrag.py build [件数]     索引を作る(途中から再開できる)
  uv run python src/graph_lightrag.py query "問い" [mode]
  uv run python src/graph_lightrag.py retrieve_all      A と B の全問を5つの mode で引く
"""
import asyncio
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "data/lightrag"
INDEX_MODEL = os.environ.get("KAIGO_INDEX_MODEL", "haiku")
CALLS = {"n": 0, "sec": 0.0}


def run_claude(prompt, system_prompt, model):
    """claude -p を1回呼ぶ。引数は配列で渡す(シェルを通さない)。文面は標準入力で渡す(--- で始まる文面をオプションと取り違えるため)。system は --system-prompt で渡し、Claude Code の既定の指示を外す。"""
    cmd = ["claude", "-p", "--model", model, "--output-format", "text", "--tools", "",
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--system-prompt", system_prompt]
    for attempt in range(3):
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=600, cwd="/tmp")
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
        time.sleep(5 * (attempt + 1))
    return r.stdout


async def claude(prompt, system_prompt=None, history_messages=None, **kw):
    """LightRAG の LLM 関数。"""
    hist = "".join(f"[{m['role']}]\n{m['content']}\n\n" for m in (history_messages or []))
    t0 = time.time()
    out = await asyncio.to_thread(run_claude, hist + prompt, system_prompt or "You are a helpful assistant.", INDEX_MODEL)
    CALLS["n"] += 1
    CALLS["sec"] += time.time() - t0
    return out


async def embed(texts):
    from embed import DOC_PREFIX, model
    return np.asarray(model().encode([DOC_PREFIX + t for t in texts], batch_size=8, normalize_embeddings=True))


async def make_rag():
    from lightrag import LightRAG
    from lightrag.utils import EmbeddingFunc
    WORK.mkdir(parents=True, exist_ok=True)
    rag = LightRAG(
        working_dir=str(WORK),
        llm_model_func=claude,
        llm_model_max_async=12,
        max_parallel_insert=8,  # 既定は2。claude -p は1回が長い(約28秒)ので、文書を多めに並べる
        embedding_func=EmbeddingFunc(embedding_dim=768, max_token_size=1024, func=embed),
        addon_params={"language": "Japanese"},
    )
    await rag.initialize_storages()
    return rag


def subset_rows():
    import rag as base
    con = base.connect()
    ids = json.load(open(ROOT / "data/subset_houmon.json"))
    q = f"SELECT id, doc, path, text FROM chunks WHERE id IN ({','.join(map(str, ids))}) ORDER BY id"
    return con.execute(q).fetchall()


async def build(limit=None):
    rag = await make_rag()
    rows = subset_rows()[:limit]
    t0 = time.time()
    # 見出しのパスを頭に付ける(どの規定のどこかが、抜き出しの手がかりになる)
    texts = [f"{doc} > {path}\n{text}" for _, doc, path, text in rows]
    await rag.ainsert(texts, ids=[f"c{i}" for i, *_ in rows], file_paths=[f"c{i}" for i, *_ in rows])
    print(f"inserted {len(rows)} in {time.time() - t0:.0f}s; llm calls {CALLS['n']} ({CALLS['sec']:.0f}s total)", flush=True)
    await rag.finalize_storages()


async def retrieve(rag, query, mode="mix", k=10):
    """LightRAG が LLM に渡すはずのチャンクを、順番どおりにチャンク id で返す。"""
    from lightrag import QueryParam
    data = await rag.aquery_data(query, param=QueryParam(mode=mode, top_k=40, chunk_top_k=k))
    chunks = data.get("data", {}).get("chunks", [])
    ids = []
    for c in chunks:
        m = re.match(r"c(\d+)", c.get("file_path", "") or "")
        if m:
            ids.append(int(m.group(1)))
    return list(dict.fromkeys(ids))[:k], data


MODES = ["naive", "local", "global", "hybrid", "mix"]


async def retrieve_all():
    """A と B の問いを、LightRAG の5つの mode で引き、results/lib_lightrag.json に書く(evaluate.py subset が読む)。"""
    rag = await make_rag()
    qs = [json.loads(l)["query"] for l in open(ROOT / "data/set_a.jsonl")]
    qs += [json.loads(l)["query"] for l in open(ROOT / "data/set_b.jsonl")]
    qs = [q for q in dict.fromkeys(qs) if q.strip()]
    out_path = ROOT / "results/lib_lightrag.json"
    out = json.load(open(out_path)) if out_path.exists() else {}
    sem = asyncio.Semaphore(8)
    t0 = time.time()

    async def one(q, mode):
        name = f"LightRAG({mode})"
        if q in out.get(name, {}):
            return
        async with sem:
            ids, _ = await retrieve(rag, q, mode, 20)
        out.setdefault(name, {})[q] = ids

    # 問いのキーワード抜き出し(LLM)は mode をまたいでキャッシュされるので、まず mix で全問を回す
    for mode in ["mix"] + [m for m in MODES if m != "mix"]:
        await asyncio.gather(*(one(q, mode) for q in qs))
        json.dump(out, open(out_path, "w"), ensure_ascii=False)
        print(mode, "done", f"{time.time() - t0:.0f}s", "llm calls", CALLS["n"], flush=True)
    await rag.finalize_storages()


async def main():
    if sys.argv[1] == "retrieve_all":
        await retrieve_all()
    elif sys.argv[1] == "build":
        await build(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    elif sys.argv[1] == "query":
        rag = await make_rag()
        ids, data = await retrieve(rag, sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "mix")
        print(ids)
        print(json.dumps(data.get("data", {}).get("entities", [])[:5], ensure_ascii=False)[:800])
        await rag.finalize_storages()


if __name__ == "__main__":
    asyncio.run(main())
