"""B(根拠問題)の正解を、pooling と Claude の判定で付ける。

- 問いは、コーパスから外した Q&A の問いそのもの
- 候補(pool): BM25・ベクトル(flat)・ハイブリッドの上位20件ずつの和集合
- Claude が、公式の答えを見ながら各候補を 2/1/0 で判定する
出力: data/set_b.jsonl  {qa_id, query, answer, judged: {chunk_id: grade}}
"""
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rag
from embed import embed_queries

ROOT = Path(__file__).resolve().parent.parent
MODEL = "sonnet"
POOL = 20

PROMPT = """介護報酬のQ&Aについて、検索で集めた候補の文章が、公式の答えの「根拠」になるかを判定してください。

判定:
- 2: 公式の答えが拠っている規定・説明そのもの。この候補を読めば答えを導ける(別のQ&Aでも、同じ論点に同じ答えを出していれば2)
- 1: 同じ制度や加算の話で関連はあるが、これだけでは答えを導けない
- 0: 関係がない、または別の論点

出力はJSONのオブジェクトだけ。キーは候補のid(文字列)、値は 0/1/2。すべての候補を判定すること。

# 問い
{q}

# 公式の答え
{a}

# 候補
{cands}
"""


def ask(prompt: str) -> str:
    r = subprocess.run(["claude", "-p", prompt, "--model", MODEL, "--output-format", "text"],
                       capture_output=True, text=True, timeout=900)
    r.check_returncode()
    return r.stdout


def judge(item, con_path):
    con = rag.connect(con_path)
    q, a, ids = item["query"], item["answer"], item["pool"]
    cands = "\n\n".join(
        f"[id={cid}] ({doc} / {path})\n{text[:700]}"
        for cid, doc, path, text in (
            con.execute("SELECT id, doc, path, text FROM chunks WHERE id=?", (cid,)).fetchone() for cid in ids
        )
    )
    for _ in range(3):
        s = ask(PROMPT.format(q=q, a=a[:1500], cands=cands))
        got = {int(k): int(v) for k, v in re.findall(r'"(\d+)"\s*:\s*([012])', s) if int(k) in ids}
        if len(got) >= len(ids) * 0.9:
            return got
    return got


def main():
    split = json.load(open(ROOT / "data/split.json"))
    qa = {json.loads(l)["qa_id"]: json.loads(l) for l in open(ROOT / "data/qa_all.jsonl")}
    con = rag.connect()
    items = []
    qs = [qa[i]["question"] for i in split["set_b_heldout"]]
    qvs = embed_queries(qs)
    for i, q, qv in zip(split["set_b_heldout"], qs, qvs):
        pool = []
        for lst in (rag.bm25(con, q, POOL), rag.vector(con, qv, POOL, table="vec_flat"), rag.hybrid(con, q, qv, POOL)):
            pool += [cid for cid, _ in lst]
        items.append({"qa_id": i, "query": q, "answer": qa[i]["answer"], "pool": list(dict.fromkeys(pool))})
    print("pool avg", sum(len(x["pool"]) for x in items) / len(items))

    out = ROOT / "data/set_b.jsonl"
    done = {json.loads(l)["qa_id"] for l in open(out)} if out.exists() else set()
    todo = [it for it in items if it["qa_id"] not in done]

    def run(it):
        j = judge(it, rag.DB)
        with open(out, "a") as f:
            f.write(json.dumps({"qa_id": it["qa_id"], "query": it["query"], "answer": it["answer"],
                                "judged": {str(k): v for k, v in j.items()}}, ensure_ascii=False) + "\n")
        print("judged", it["qa_id"], len(j), "/", len(it["pool"]), flush=True)
        return j

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(run, todo))
    results = [json.loads(l)["judged"] for l in open(out)]
    n2 = [sum(v == 2 for v in j.values()) for j in results]
    print("grade2 per q:", n2, "zero:", sum(x == 0 for x in n2))


if __name__ == "__main__":
    main()
