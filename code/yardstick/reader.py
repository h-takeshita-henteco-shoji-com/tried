"""AIの読者(Claude Haiku 4.5)に、題 → 冒頭 → 1段落ずつ → 読後 の順で読ませる。

measures.md の「2. AIの読者」の手順に従う。1回につき1つの会話で、毎回新しい会話にする。
使い方: python reader.py <texts_dir> <reader.md> <out_dir> <回数> [文書名...]
出力: <out_dir>/<文書>/run<NN>.jsonl(1行が1ターンの問いと答え)
"""
import glob
import json
import os
import re
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
from label import claude  # noqa: E402
from segment import load  # noqa: E402

MODEL = "claude-haiku-4-5-20251001"
REACT = '"反応": {"驚いた": [文番号], "納得した": [文番号], "問いが解けた": [文番号], "迷った": [文番号], "手が止まった": [文番号]}'
REACT_HELP = """反応の意味:
- 驚いた: 予想していなかった文
- 納得した: 前に驚いたことの理由が分かった文
- 問いが解けた: 抱いていた問いが解けた文
- 迷った: 意味が取れなかった文
- 手が止まった: 読む気が落ちた文
当てはまる文がなければ空の配列にしてください。"""


def opening_end(doc):
    """冒頭は、本文の20%を超えた最初の段落の終わりまで。"""
    acc = 0
    for s in doc["sents"]:
        acc += s["len"]
        if acc / doc["total"] > 0.2:
            return s["par"]
    return doc["sents"][-1]["par"]


def show(sents):
    return "\n".join(f"{s['id']} {s['text']}" for s in sents)


def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None


def turns(doc):
    p0 = opening_end(doc)
    yield "title", f"""これから1つの文章を、題、冒頭、続きの1段落ずつの順に渡します。先を推測して答えてください。
答えはすべて JSON だけで返してください。

まず題だけを渡します。
題: {doc['title']}

次の JSON で答えてください。
{{"題の感想": "この題について、あなたはどう思うか", "予想": "この文章の結論を1文で予想"}}"""
    yield "opening", f"""冒頭を渡します。各文の頭に文番号があります。

{show([s for s in doc['sents'] if s['par'] <= p0])}

次の JSON で答えてください。
{{"予想": "この文章の結論を1文で予想", "根拠": "予想の根拠を1〜2文", "自信": 1〜5, "読みたい": 1〜5, "読みたい理由": "...", "問い": ["いま抱いている問い"], "変化": "題だけのときの予想から、変わらない/少し変わった/逆になった", {REACT}}}
{REACT_HELP}"""
    pars = sorted({s["par"] for s in doc["sents"] if s["par"] > p0})
    for k, p in enumerate(pars, 1):
        yield f"p{p:02d}", f"""続きの1段落を渡します({k}/{len(pars)})。

{show([s for s in doc['sents'] if s['par'] == p])}

次の JSON で答えてください。
{{"予想": "いまの結論の予想を1文", "変化": "前の段落から、変わらない/少し変わった/逆になった", "自信": 1〜5, "問い": ["いま抱いている問い"], {REACT}}}"""
    yield "final", """文章はここで終わりです。次の JSON で答えてください。
{"実際の結論": "1文", "外れたか": "当たった/一部外れた/外れた", "納得": 1〜5(外れ方に納得したか), "要点": "要点を1文で", "書き手": "書き手はどんな経験をした人だと思うか", "面白さ": 1〜5, "面白さの理由": "...", "読みやすさ": 1〜5, "読みやすさの理由": "...", "既読": "この文章を前に読んだことがあるか(ある/ない)", "既読の題": "あれば題", "既読の書き手": "あれば書き手"}
面白さは、知的な面白さに限ります(笑える、感動する、美しいは含めません)。"""


def one_run(doc_id, doc, persona, out_path):
    if os.path.exists(out_path):
        return
    system = f"あなたは次の読者です。\n{persona}\n\n文章を読み、指示された JSON だけを返してください。"
    session = str(uuid.uuid4())
    rows = []
    for i, (step, prompt) in enumerate(turns(doc)):
        res = claude(prompt, MODEL, system=system, session=session, resume=i > 0)
        rows.append({"step": step, "answer": parse(res), "raw": res})
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    texts, persona_path, out_dir, n = sys.argv[1:5]
    only = set(sys.argv[5:])
    persona = open(persona_path, encoding="utf-8").read().split("## 渡す本文", 1)[1].strip()
    jobs = []
    for path in sorted(glob.glob(f"{texts}/*.txt")):
        doc_id = os.path.basename(path)[:-4]
        if only and doc_id not in only:
            continue
        os.makedirs(f"{out_dir}/{doc_id}", exist_ok=True)
        doc = load(path)
        for r in range(1, int(n) + 1):
            jobs.append((doc_id, doc, persona, f"{out_dir}/{doc_id}/run{r:02d}.jsonl"))
    with ThreadPoolExecutor(10) as ex:
        for _ in ex.map(lambda j: one_run(*j), jobs):
            pass
    print("done", len(jobs), file=sys.stderr)
