"""答えの正しさを、元の Q&A の答えと照らして Claude(Sonnet)に判定させる。

1問ごとに、全方式の答えを記号に置き換え、順番を混ぜてまとめて判定する(どの方式か伏せる)。
- 2: 結論が元の答えと同じで、要点もそろっている
- 1: 結論は同じだが、要点が欠けるか、一部に誤りがある
- 0: 結論が違う、答えていない、または「資料では分からない」で止まっている
出力: results/answer_grades.jsonl {qa_id, grades: {方式: 0/1/2}, reasons}
使い方: uv run python src/judge_answers.py llm rag agentic pageindex
      方式の名前は results/answers_<名前>.jsonl の <名前>。出力先は環境変数 KAIGO_GRADES、判定役のモデルは KAIGO_JUDGE で変えられる
"""
import json
import os
import random
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / os.environ.get("KAIGO_GRADES", "results/answer_grades.jsonl")

PROMPT = """介護保険の質問に対する、いくつかの答えを採点してください。正解は厚生労働省のQ&Aの答えです。

質問: {q}

正解(厚労省のQ&A): {gold}

採点する答え:
{answers}

基準:
- 2: 結論が正解と同じで、正解の要点もそろっている
- 1: 結論は正解と同じだが、要点が欠けている、または一部に誤りがある
- 0: 結論が正解と違う、質問に答えていない、または「資料では分からない」で止まっている
正解に無い補足は、正解と矛盾しなければ減点しない。

出力はJSONだけ: {{"記号": {{"grade": 0か1か2, "reason": "30字以内"}}, ...}}
"""


def ask(prompt):
    for _ in range(3):
        r = subprocess.run(["claude", "-p", prompt, "--model", os.environ.get("KAIGO_JUDGE", "sonnet"), "--output-format", "text",
                            "--tools", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}'],
                           capture_output=True, text=True, timeout=600)
        got = {k: (int(g), why) for k, g, why in
               re.findall(r'"([A-Z])"\s*:\s*\{\s*"grade"\s*:\s*([012])\s*,\s*"reason"\s*:\s*"([^"]*)"', r.stdout)}
        if got:
            return got
    return {}


def main(modes):
    qa = {json.loads(l)["qa_id"]: json.loads(l) for l in open(ROOT / "data/qa_all.jsonl")}
    ans = {m: {json.loads(l)["qa_id"]: json.loads(l) for l in open(ROOT / f"results/answers_{m}.jsonl")} for m in modes}
    ids = sorted(set.intersection(*[set(a) for a in ans.values()]))
    done = {json.loads(l)["qa_id"] for l in open(OUT)} if OUT.exists() else set()

    def one(qid):
        rnd = random.Random(qid + os.environ.get("KAIGO_SEED", ""))  # 回ごとに並び順を変えられる
        order = modes[:]
        rnd.shuffle(order)
        label = {chr(65 + i): m for i, m in enumerate(order)}
        body = "\n\n".join(f"{k}: {ans[m][qid]['answer']}" for k, m in label.items())
        set_b_query = next(json.loads(l)["query"] for l in open(ROOT / "data/set_b.jsonl") if json.loads(l)["qa_id"] == qid)
        got = ask(PROMPT.format(q=set_b_query, gold=qa[qid]["answer"], answers=body))
        rec = {"qa_id": qid, "grades": {label[k]: g for k, (g, _) in got.items() if k in label},
               "reasons": {label[k]: w for k, (_, w) in got.items() if k in label}}
        with open(OUT, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(qid, rec["grades"], flush=True)

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(one, [i for i in ids if i not in done]))


if __name__ == "__main__":
    main(sys.argv[1:])
