"""問題集を分け、A(言い換え問題)を Claude に作らせる。

- 訪問介護の Q&A を乱数で分ける。B 用の40問はコーパスから外す。A 用の100問は残す。
- A: Q&A の問いを、現場の人がチャットで聞く口ぶりに書き換える。正解は元の Q&A。
出力: data/split.json, data/set_a.jsonl
"""
import json
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = "sonnet"
BATCH = 20

PROMPT = """あなたは訪問介護事業所で働く人(ヘルパー、サービス提供責任者、管理者、事務)です。
次の各Q&Aの「問い」を、あなたが同僚や詳しい人にチャットで尋ねるときの言い方に書き換えてください。

決まり:
- 1〜2文。話し言葉で、具体的な場面を入れてよい
- 元の問いにある特徴的な言い回しや用語(「〜如何」「算定できるか」、加算の正式名など)をそのまま写さない。現場でふだん使う言い方にする
- ただし、元のQ&Aの答えがそのまま当てはまる問いにする。論点を変えない、増やさない
- 答えの中身は書かない
- 出力はJSONの配列だけ。[{"qa_id": "...", "query": "..."}]

Q&A:
"""


def ask_claude(prompt: str) -> str:
    r = subprocess.run(
        ["claude", "-p", prompt, "--model", MODEL, "--output-format", "text"],
        capture_output=True, text=True, timeout=600,
    )
    r.check_returncode()
    return r.stdout


def parse_json_array(s: str):
    i, j = s.find("["), s.rfind("]")
    return json.loads(s[i : j + 1])


def main():
    qa = [json.loads(l) for l in open(ROOT / "data/qa_all.jsonl")]
    home = [x for x in qa if x["service"].startswith("11 訪問介護")]
    rnd = random.Random(20261108)
    rnd.shuffle(home)
    set_b = [x["qa_id"] for x in home[:40]]
    set_a = [x["qa_id"] for x in home[40:140]]
    json.dump({"set_a": set_a, "set_b_heldout": set_b}, open(ROOT / "data/split.json", "w"), ensure_ascii=False, indent=1)

    by_id = {x["qa_id"]: x for x in qa}
    out_path = ROOT / "data/set_a.jsonl"
    done = set()
    if out_path.exists():
        done = {json.loads(l)["qa_id"] for l in open(out_path)}
    todo = [i for i in set_a if i not in done]
    for k in range(0, len(todo), BATCH):
        ids = todo[k : k + BATCH]
        body = "\n\n".join(
            f"qa_id: {i}\n項目: {by_id[i]['item']}\n問い: {by_id[i]['question']}\n答え(参考): {by_id[i]['answer'][:400]}"
            for i in ids
        )
        res = parse_json_array(ask_claude(PROMPT + body))
        with open(out_path, "a") as f:
            for r in res:
                if r["qa_id"] in ids:
                    f.write(json.dumps({"qa_id": r["qa_id"], "query": r["query"], "gold_qa": [r["qa_id"]]}, ensure_ascii=False) + "\n")
        print(k + len(ids), "/", len(todo))


if __name__ == "__main__":
    main()
