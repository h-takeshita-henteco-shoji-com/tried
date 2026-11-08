"""HippoRAG 2(OSU-NLP-Group/HippoRAG 2.0.0a3)で、訪問介護の範囲のグラフを作り、引く。

- LLM と埋め込みは、OpenAI と同じ形の中継サーバー(src/llm_shim.py)を通す。LLM は claude -p の Haiku、埋め込みは ruri-v3
  - HippoRAG は、埋め込みのモデル名に "text-embedding" を含むときだけ OpenAI 形式で呼ぶ。名前だけ合わせる
- 入力は data/msgraphrag/input/subset.jsonl(608件。Microsoft GraphRAG と同じ文面)。引いた文面をチャンク id に戻す
- HippoRAG 2: 問いに近い三つ組(fact)を引き、LLM で選び直し(recognition memory)、その用語から Personalized PageRank でたどる
- DPR: チャンクのベクトル検索だけ(グラフなし)。比べる基準
使い方(別の環境で動かす):
  /tmp/gr_hippo/.venv/bin/python src/graph_hipporag.py build [件数]
  /tmp/gr_hippo/.venv/bin/python src/graph_hipporag.py retrieve_all   -> results/lib_hipporag.json
"""
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAVE = ROOT / "data/hipporag"
BASE = "http://127.0.0.1:8766/v1"
os.environ.setdefault("OPENAI_API_KEY", "local")  # 中継サーバーはキーを確かめない


def docs(limit=None):
    rows = [json.loads(l) for l in open(ROOT / "data/msgraphrag/input/subset.jsonl")][:limit]
    return [r["text"] for r in rows], {r["text"]: int(r["id"][1:]) for r in rows}


def patch_text_processing():
    """HippoRAG は用語を正規化するとき、英数字以外を空白にする([^A-Za-z0-9 ])。日本語の用語が空や数字だけになり、
    グラフが1点につぶれる。Unicode の文字と数字を残す版に差し替える(ライブラリ本体は書き換えない)。"""
    import re
    import sys as _sys
    import hipporag  # noqa: F401  モジュールを読み込んでから差し替える

    def text_processing(text):
        if isinstance(text, list):
            return [text_processing(t) for t in text]
        if not isinstance(text, str):
            text = str(text)
        return re.sub(r"[^\w ]", " ", text.lower()).strip()

    for name, mod in list(_sys.modules.items()):
        if name.startswith("hipporag") and hasattr(mod, "text_processing"):
            mod.text_processing = text_processing


def make(save=SAVE):
    patch_text_processing()
    from hipporag import HippoRAG
    return HippoRAG(save_dir=str(save), llm_model_name="haiku", llm_base_url=BASE,
                    embedding_model_name="text-embedding-ruri", embedding_base_url=BASE)


def build(limit=None, save=SAVE):
    texts, _ = docs(limit)
    t0 = time.time()
    make(save).index(texts)
    print(f"indexed {len(texts)} in {time.time() - t0:.0f}s", flush=True)


def retrieve_all(save=SAVE, out_path=ROOT / "results/lib_hipporag.json", limit=None):
    _, ids = docs(limit)
    h = make(save)
    h.prepare_retrieval_objects()
    qs = [json.loads(l)["query"] for l in open(ROOT / "data/set_a.jsonl")]
    qs += [json.loads(l)["query"] for l in open(ROOT / "data/set_b.jsonl")]
    qs = [q for q in dict.fromkeys(qs) if q.strip()]
    h.get_query_embeddings(qs)

    def back(sol):
        return [ids[d] for d in sol.docs if d in ids][:20]

    t0 = time.time()
    # retrieve は問いを1つずつ回し、選び直しで LLM を呼ぶ。問いごとに並べる
    with ThreadPoolExecutor(8) as ex:
        hippo = list(ex.map(lambda q: back(h.retrieve([q], num_to_retrieve=20)[0]), qs))
    dpr = [back(s) for s in h.retrieve_dpr(qs, num_to_retrieve=20)]
    out = {"HippoRAG 2": dict(zip(qs, hippo)), "HippoRAG 2(DPR)": dict(zip(qs, dpr))}
    json.dump(out, open(out_path, "w"), ensure_ascii=False)
    print(f"done {len(qs)} in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else None
    if cmd == "build":
        build(n, Path(sys.argv[3]) if len(sys.argv) > 3 else SAVE)
    elif cmd == "retrieve_all":
        retrieve_all(Path(sys.argv[3]) if len(sys.argv) > 3 else SAVE,
                     Path(sys.argv[4]) if len(sys.argv) > 4 else ROOT / "results/lib_hipporag.json", n)
