"""#155: 利用者・家族の依頼が介護保険の範囲内かを、AI に根拠つきで分かる言葉で説明させ、採点する。

問題(33問)
- data/scope_questions.jsonl       自作20問(可7・不可11・条件付き2)
- data/scope_questions_muni.jsonl  自治体13問。郡上市・時津町の「生活援助の取扱い」の対応事例から。正解は自治体の判断
  自治体の資料はコーパスに入れない(答えが漏れるため)
- 各問に accept(正しいとみなす根拠の通知・Q&A の一覧)を持たせる

答え: llm(資料なし)と agentic(検索と全文読みの道具)。答える役は Sonnet。各方式3回(r1〜r3)
採点
- 判定役: Sonnet 3回(並びを変える)の中央値を多数決とする。別のモデルとして Opus 1回
  可否(1/0)、根拠(2/1/0)、分かりやすさ(3/2/1)。1問ごとに6つの答え(2方式×3回)を記号で伏せ、まとめて採点する
- 機械の採点(判定役を使わない)
  根拠: 答えの根拠に、accept の通知・Q&A の名前が1つでも出てくるか
  引用: 「」『』で囲んだ8字以上の文が、資料のどこかにほぼそのまま(表記ゆれを除いて90%以上一致)あるか
使い方:
  uv run python src/server.py &
  uv run python src/scope_explain.py answer llm 1   (agentic も。回は 1〜3。済んだ問いは飛ばす)
  uv run python src/scope_explain.py judge sonnet 1 (sonnet 1〜3、opus 1)
  uv run --with rapidfuzz python src/scope_explain.py score
"""
import json
import random
import re
import shutil
import statistics as st
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import answer as A

ROOT = Path(__file__).resolve().parent.parent
QS = [json.loads(l) for f in ("scope_questions.jsonl", "scope_questions_muni.jsonl") for l in open(ROOT / "data" / f)]
MODES = ["llm", "agentic"]
RUNS = [1, 2, 3]
KEYS = [f"{m}_r{r}" for m in MODES for r in RUNS]

RULES = """あなたは訪問介護の事業所のサービス提供責任者です。利用者や家族から、ヘルパーへの頼みごとについて聞かれました。
介護保険の訪問介護で、その頼みごとができるかを答えてください。答えは、国の告示・通知・Q&Aに基づかせてください。
説明は、利用者や家族が読んで分かる、やさしい言葉で書いてください。できない場合は、角が立たない言い方と、代わりの手段も添えてください。
最後に、次のJSONだけを出力してください。
{"verdict": "可" か "不可" か "条件付き", "explain": "利用者への説明(200字以内)", "basis": "根拠にした告示・通知・Q&Aの名前と箇所", "evidence": [根拠にしたチャンクの番号(整数。道具を使わない場合は空)]}"""

JUDGE = """あなたは介護保険の訪問介護に詳しい審査員です。利用者の頼みごとに対する、いくつかの答え(記号で伏せてある)を採点してください。
正解の可否と根拠を基準にします。

頼みごと: {ask}
正解の可否: {verdict}
正解の根拠: {basis}
正しいとみなす根拠の通知・Q&A(どれを挙げてもよい): {accept}

採点の基準:
- verdict_ok: 答えの可否が正解と合えば1、合わなければ0。正解が「条件付き」なら、答えが条件(何によって決まるか)を正しく述べていれば1。正解が「可」で、答えがケアプランへの位置付けなど妥当な前提を添えた「条件付き」なら1
- basis: 正しいとみなす根拠のどれかを挙げ、その中身の説明も合っていれば2。関係はあるが的を外している・中身の説明が誤っている・あいまいなら1。根拠が無い・誤りなら0。書き方の詳しさや長さでは点を変えない
- clarity: 利用者や家族が読んで分かるやさしさ。3=専門用語なしで分かりやすく、断る場合も配慮がある、2=おおむね分かる、1=専門用語が多い・冷たい

答え:
{answers}

次のJSONだけを出力してください。
{{"grades": {{"記号": {{"verdict_ok": 0か1, "basis": 0か1か2, "clarity": 1か2か3, "reason": "30字以内"}}}}}}"""


def ans_path(mode, run):
    return ROOT / f"results/scope_{mode}_r{run}.jsonl"


def load_answers():
    return {f"{m}_r{r}": {json.loads(l)["id"]: json.loads(l) for l in open(ans_path(m, r))} for m in MODES for r in RUNS}


def ask(q, mode):
    prompt = RULES + ("\n\n" + A.TOOLS["agentic"] if mode == "agentic" else "") + f"\n\n頼みごと: {q['ask']}"
    text, calls, turns = A.run_claude(prompt, mode, [])
    m = re.search(r"\{[^{}]*\"verdict\"[^{}]*\}", text, re.S)
    try:
        obj = json.loads(m.group(0))
    except Exception:
        obj = {"verdict": "", "explain": text.strip()[-400:], "basis": "", "evidence": []}
    return {"id": q["id"], **obj, "searches": [c for c in calls if "search" in c], "reads": [c for c in calls if "read" in c], "turns": turns}


def cmd_answer(mode, run):
    A.WORK.mkdir(exist_ok=True)
    shutil.copy(ROOT / "src/tool.py", A.WORK / "tool.py")
    p = ans_path(mode, run)
    done = {json.loads(l)["id"]: json.loads(l) for l in open(p)} if p.exists() else {}
    todo = [q for q in QS if q["id"] not in done or not done[q["id"]].get("verdict")]
    with ThreadPoolExecutor(5) as ex:
        for o in ex.map(lambda q: ask(q, mode), todo):
            done[o["id"]] = o
    with open(p, "w") as f:
        for q in QS:
            f.write(json.dumps(done[q["id"]], ensure_ascii=False) + "\n")
    print(mode, run, "answered", len(todo), "total", len(done))


def run_judge(prompt, model):
    for _ in range(3):
        r = subprocess.run(["claude", "-p", "--model", model, "--output-format", "text", "--tools", "",
                            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}'],
                           input=prompt, capture_output=True, text=True, timeout=900, cwd="/tmp")
        m = re.search(r"\{.*\}", r.stdout, re.S)
        try:
            return json.loads(m.group(0))["grades"]
        except Exception:
            continue
    raise RuntimeError(r.stdout[-300:])


def cmd_judge(model, k):
    ans = load_answers()
    rnd = random.Random(f"{model}{k}")

    def one(q):
        keys = KEYS[:]
        rnd.shuffle(keys)
        labels = dict(zip("ABCDEF", keys))
        body = "\n\n".join(f"[{c}] 可否: {ans[key][q['id']].get('verdict')}\n説明: {ans[key][q['id']].get('explain')}\n根拠: {ans[key][q['id']].get('basis')}"
                           for c, key in labels.items())
        g = run_judge(JUDGE.format(answers=body, accept="、".join(q["accept"]), **{k2: q[k2] for k2 in ("ask", "verdict", "basis")}), model)
        return {"id": q["id"], "grades": {labels[c]: v for c, v in g.items() if c in labels}}

    with ThreadPoolExecutor(5) as ex:
        out = list(ex.map(one, QS))
    with open(ROOT / f"results/scope_grades_{model}{k}.jsonl", "w") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print("judged", model, k, len(out))


# --- 機械の採点 ---
NAME_PAT = {
    "老振76号": r"老振(第)?\s*[7７][6６]\s*号|事業運営の取扱等について",
    "老計10号": r"老計(第)?\s*[1１][0０]\s*号|サービス行為ごとの区分",
    "老企36号": r"老企(第)?\s*[3３][6６]\s*号|留意事項(通知)?",
    "告示19号": r"告示(第)?\s*[1１][9９]\s*号|費用の額の算定に関する基準",
    "Q&A": r"Q\s*[&＆]\s*A|Ｑ\s*[&＆]\s*Ａ|Q&A|Ｑ＆Ａ|疑義解釈|事務連絡",
}


def basis_hit(q, a):
    text = (a.get("basis") or "") + " " + (a.get("explain") or "")
    return int(any(re.search(NAME_PAT[n], text) for n in q["accept"]))


def norm(s):
    s = re.sub(r"[\s、。,，・()（）「」『』　:：;；/／\-－―‐〜~]", "", s)
    s = re.sub(r"[0-9０-９①-⑳一二三四五六七八九十]+", "", s)  # 項番号の書き方の違いを吸収
    return s.replace("え", "").replace("り", "")  # 送り仮名のゆれ(模様替え/模様替、取扱い/取扱)を吸収


def quotes(a):
    return [x for x in re.findall(r"[「『]([^」』]{8,})[」』]", (a.get("basis") or "") + (a.get("explain") or ""))]


def cmd_score():
    from rapidfuzz import fuzz
    import rag
    con = rag.connect()
    chunks = [norm(t) for (t,) in con.execute("SELECT text FROM chunks")]
    big = "".join(chunks)

    def quote_ok(qt):
        n = norm(qt)
        if len(n) < 6:
            return None  # 番号だけの引用などは数えない
        if n in big:
            return True
        return max(fuzz.partial_ratio(n, c) for c in chunks if len(c) >= len(n) * 0.5) >= 90

    ans = load_answers()
    J = {}
    for name in ["sonnet1", "sonnet2", "sonnet3", "opus1"]:
        p = ROOT / f"results/scope_grades_{name}.jsonl"
        if p.exists():
            J[name] = {json.loads(l)["id"]: json.loads(l)["grades"] for l in open(p)}
    son = [J[n] for n in ("sonnet1", "sonnet2", "sonnet3") if n in J]
    vote = {q["id"]: {k: {f: int(st.median(s[q["id"]][k][f] for s in son)) for f in ("verdict_ok", "basis", "clarity")}
                      for k in KEYS} for q in QS}
    sets = {"全33問": QS, "自作20問": [q for q in QS if q["id"].startswith("S")], "自治体13問": [q for q in QS if q["id"].startswith("M")]}

    qcache = {}
    print("| 方式 | 問題 | 可否が合う(3回の平均) | 根拠 判定(0-2) | 根拠 機械(一覧の通知を挙げた割合) | 分かりやすさ(1-3) | 引用が資料にある | 3回で可否が揺れた問い |")
    print("|---|---|---|---|---|---|---|---|")
    for m in MODES:
        for sname, qs in sets.items():
            ks = [f"{m}_r{r}" for r in RUNS]
            vo = st.mean(vote[q["id"]][k]["verdict_ok"] for q in qs for k in ks) * len(qs)
            bj = st.mean(vote[q["id"]][k]["basis"] for q in qs for k in ks)
            bm = st.mean(basis_hit(q, ans[k][q["id"]]) for q in qs for k in ks)
            cl = st.mean(vote[q["id"]][k]["clarity"] for q in qs for k in ks)
            tot = ok = 0
            for q in qs:
                for k in ks:
                    for qt in quotes(ans[k][q["id"]]):
                        if qt not in qcache:
                            qcache[qt] = quote_ok(qt)
                        if qcache[qt] is not None:
                            tot += 1
                            ok += qcache[qt]
            sway = sum(len({ans[k][q["id"]].get("verdict") for k in ks}) > 1 for q in qs)
            print(f"| {m} | {sname} | {vo:.1f}/{len(qs)} | {bj:.2f} | {bm:.0%} | {cl:.2f} | {ok}/{tot} ({ok / max(tot, 1):.0%}) | {sway} |")

    cells = [(q["id"], k) for q in QS for k in KEYS]
    for f in ("verdict_ok", "basis", "clarity"):
        same3 = sum(len({s[i][k][f] for s in son}) == 1 for i, k in cells) / len(cells)
        line = f"{f}: Sonnet 3回とも同じ {same3:.0%}"
        if "opus1" in J:
            agree = sum(J["opus1"][i][k][f] == vote[i][k][f] for i, k in cells) / len(cells)
            om = {m: st.mean(J["opus1"][q["id"]][f"{m}_r{r}"][f] for q in QS for r in RUNS) for m in MODES}
            line += f"、Opus と多数決が同じ {agree:.0%}、Opus の平均 llm {om['llm']:.2f} / agentic {om['agentic']:.2f}"
        print(line)

    print("\n可否を外した答え(多数決で verdict_ok=0)")
    for q in QS:
        bad = [k for k in KEYS if vote[q["id"]][k]["verdict_ok"] == 0]
        if bad:
            print(f"- {q['id']}({q['verdict']}): " + ", ".join(f"{k}={ans[k][q['id']].get('verdict')}" for k in bad))
    print("\n検索の回数(平均)", {m: round(st.mean(len(ans[f'{m}_r{r}'][q['id']].get('searches', [])) for q in QS for r in RUNS), 1) for m in MODES})
    json.dump({"vote": vote, "quotes": qcache}, open(ROOT / "results/scope_summary.json", "w"), ensure_ascii=False)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "answer":
        cmd_answer(sys.argv[2], int(sys.argv[3]))
    elif c == "judge":
        cmd_judge(sys.argv[2], int(sys.argv[3]))
    elif c == "score":
        cmd_score()
