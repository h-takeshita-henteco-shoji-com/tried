"""Contextual Retrieval: 文書チャンクに、文書の中での位置づけを Claude に書かせる。

本家(Anthropic)は文書全体を渡すが、今回の文書は1本15万字を超える。
そこで、見出しのパスと、同じ文書の前後のチャンクの抜粋だけを渡す。
Q&A は種別と項目で意味が通るため、AI は使わない(build_variants.py で機械的に足す)。
出力: data/context_doc.jsonl  {id, context}
"""
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = "haiku"
BATCH = 20
OUT = ROOT / "data/context_doc.jsonl"

PROMPT = """次は、介護報酬・運営基準の文書「{doc}({doc_name})」から切り出したチャンクです。
各チャンクについて、文書全体の中での位置づけを、1〜2文(80字以内)で書いてください。

決まり:
- 検索で見つけやすくするための文。どのサービスの、どの単位数・加算・減算・基準・手続の、何についての規定かを書く
- チャンクに書かれていない事実を足さない。見出しと前後から分かることだけを書く
- 出力はJSONのオブジェクトだけ。キーはid(文字列)、値は文

{body}
"""


def ask(prompt: str) -> str:
    r = subprocess.run(["claude", "-p", prompt, "--model", MODEL, "--output-format", "text"],
                       capture_output=True, text=True, timeout=900)
    r.check_returncode()
    return r.stdout


def parse(s: str, ids: set[int]) -> dict[int, str]:
    i, j = s.find("{"), s.rfind("}")
    try:
        obj = json.loads(s[i : j + 1])
        return {int(k): str(v) for k, v in obj.items() if int(k) in ids}
    except Exception:
        return {int(k): v for k, v in re.findall(r'"(\d+)"\s*:\s*"((?:[^"\\]|\\.)*)"', s) if int(k) in ids}


def main():
    rows = [json.loads(l) for l in open(ROOT / "data/corpus.jsonl")]
    docs = [r for r in rows if r["kind"] == "doc"]
    done = {json.loads(l)["id"] for l in open(OUT)} if OUT.exists() else set()

    # 1つの束には同じ文書のチャンクだけを入れる
    batches = []
    for d in dict.fromkeys(r["doc"] for r in docs):
        ds = [r for r in docs if r["doc"] == d]
        for k in range(0, len(ds), BATCH):
            b = [r for r in ds[k : k + BATCH] if r["id"] not in done]
            if b:
                batches.append(b)

    by_id = {r["id"]: r for r in rows}

    def run(b):
        parts = []
        for r in b:
            prev = by_id.get(r["id"] - 1)
            prev_txt = prev["text"][:150].replace("\n", " ") if prev and prev["doc"] == r["doc"] else ""
            parts.append(f"[id={r['id']}] 見出し: {r['path']}\n直前の抜粋: {prev_txt}\n本文: {r['text'][:900]}")
        prompt = PROMPT.format(doc=b[0]["doc"], doc_name=b[0]["doc_name"], body="\n\n".join(parts))
        got = {}
        for _ in range(3):
            got.update(parse(ask(prompt), {r["id"] for r in b} - set(got)))
            if len(got) >= len(b):
                break
        with open(OUT, "a") as f:
            for cid, ctx in got.items():
                f.write(json.dumps({"id": cid, "context": ctx}, ensure_ascii=False) + "\n")
        print("batch", b[0]["id"], len(got), "/", len(b), flush=True)

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(run, batches))


if __name__ == "__main__":
    main()
