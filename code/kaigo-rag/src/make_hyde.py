"""HyDE: 問いから、仮の答え(制度の文書の口ぶり)を Claude に書かせる。

仮の答えは正しくなくてよい。検索で、本物の規定や Q&A に近い位置へ問いを運ぶために使う。
出力: data/hyde.jsonl  {query, hyde}
"""
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = "sonnet"
BATCH = 15
OUT = ROOT / "data/hyde.jsonl"

PROMPT = """あなたは介護保険制度に詳しい人です。次の各問いについて、厚労省の通知やQ&Aの答えのような文体で、仮の答えを書いてください。

決まり:
- 2〜4文、200字以内。制度の用語(訪問介護費、算定、加算、指定居宅サービス等基準 など)を使う
- 確信がなくても、ありそうな答えを書く。検索に使うための下書きで、正しさは問わない
- 出力はJSONの配列だけ。[{{"n": 番号, "hyde": "..."}}]

{body}
"""


def ask(prompt: str) -> str:
    r = subprocess.run(["claude", "-p", prompt, "--model", MODEL, "--output-format", "text"],
                       capture_output=True, text=True, timeout=900)
    r.check_returncode()
    return r.stdout


def main():
    qa = {json.loads(l)["qa_id"]: json.loads(l) for l in open(ROOT / "data/qa_all.jsonl")}
    queries = [json.loads(l)["query"] for l in open(ROOT / "data/set_a.jsonl")]
    queries += [json.loads(l)["query"] for l in open(ROOT / "data/set_b.jsonl")]
    queries = [q for q in dict.fromkeys(queries) if q.strip()]
    done = {json.loads(l)["query"] for l in open(OUT)} if OUT.exists() else set()
    todo = [q for q in queries if q not in done]

    def run(qs):
        body = "\n".join(f"{n}. {q}" for n, q in enumerate(qs, 1))
        s = ask(PROMPT.format(body=body))
        try:
            arr = json.loads(s[s.find("[") : s.rfind("]") + 1])
            got = {int(x["n"]): x["hyde"] for x in arr}
        except Exception:
            got = {int(n): h for n, h in re.findall(r'"n"\s*:\s*(\d+)\s*,\s*"hyde"\s*:\s*"((?:[^"\\]|\\.)*)"', s)}
        with open(OUT, "a") as f:
            for n, q in enumerate(qs, 1):
                if n in got:
                    f.write(json.dumps({"query": q, "hyde": got[n]}, ensure_ascii=False) + "\n")
        print("hyde", len(got), "/", len(qs), flush=True)

    with ThreadPoolExecutor(3) as ex:
        list(ex.map(run, [todo[k : k + BATCH] for k in range(0, len(todo), BATCH)]))


if __name__ == "__main__":
    main()
