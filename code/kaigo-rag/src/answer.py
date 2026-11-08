"""B の問いに、方式ごとに Claude(Sonnet)で答えさせる。

- llm      : 検索なし。モデルの知識だけで答える(比較の下限)
- rag      : ハイブリッド+リランカーの上位5件を渡して、1回で答える
- agentic  : 検索の道具(search と read)を渡し、何度でも引かせてから答える
- pageindex: 目次の道具(tree と read)だけを渡す。PageIndex と同じく、検索語の照合も埋め込みも使わない
出力: results/answers_<方式>.jsonl {qa_id, answer, evidence, searches, reads, turns, sec}
前提: server.py を起動しておく
- graph    : GraphRAG。agentic の道具に、用語と参照のグラフをたどる related を足す
使い方: uv run python src/answer.py llm|rag|agentic|pageindex|graph
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import tool

ROOT = Path(__file__).resolve().parent.parent
WORK = Path("/tmp/kaigo-agent")  # データの無い場所で動かす(道具以外から答えを覗けないように)
MODEL = "sonnet"

RULES = """あなたは訪問介護の事業所から、介護報酬と運営基準の質問を受ける相談員です。
答えは、資料に書いてあることに基づかせてください。
最後に、次のJSONだけを出力してください。
{"answer": "答え(300字以内。結論を先に)", "evidence": [根拠にしたチャンクの番号(整数)]}"""

TOOLS = {
    "agentic": """資料を引く道具があります。Bash で次のように使います。
  python3 tool.py search "検索語"   告示・省令・通知とQ&A集から、関係しそうな8件を返す
  python3 tool.py read 1234 5678     チャンクの全文を読む
検索語を変えて何度でも引けます。根拠が見つかるまで調べてから答えてください。""",
    "pageindex": """資料の目次をたどる道具があります。Bash で次のように使います。
  python3 tool.py tree           資料の一覧
  python3 tool.py tree n123      その見出しの下の、見出しとチャンクの一覧
  python3 tool.py read 1234 5678 チャンクの全文を読む
検索の道具はありません。人が条文集を引くように、目次をたどって該当箇所を探してください。根拠が見つかるまで調べてから答えてください。""",
    "graph": """資料を引く道具があります。Bash で次のように使います。
  python3 tool.py search "検索語"   告示・省令・通知とQ&A集から、関係しそうな8件を返す
  python3 tool.py read 1234 5678     チャンクの全文を読む
  python3 tool.py related 1234       そのチャンクが含む用語と、参照している条文・通知(参照されている側も)
  python3 tool.py related 用語        その用語(加算名など)を含むチャンクの一覧
related で用語と参照をたどると、告示・省令・通知・Q&A のつながりを追えます。根拠が見つかるまで調べてから答えてください。""",
}
ALLOWED = {
    "agentic": ["Bash(python3 tool.py search:*)", "Bash(python3 tool.py read:*)"],
    "pageindex": ["Bash(python3 tool.py tree:*)", "Bash(python3 tool.py read:*)"],
    "graph": ["Bash(python3 tool.py search:*)", "Bash(python3 tool.py read:*)", "Bash(python3 tool.py related:*)"],
}


def leaks():
    """B の各問いについて、中身が同じ Q&A のチャンク id(コーパスに残っているもの)。"""
    import rag
    con = rag.connect()
    qa2cid = {q: i for i, q in con.execute("SELECT id, qa_id FROM chunks WHERE kind='qa'")}
    equiv = json.load(open(ROOT / "data/qa_equiv.json"))
    return lambda qa_id: sorted(qa2cid[e] for e in equiv[qa_id] if e in qa2cid)


def run_claude(prompt, mode, excl):
    cmd = ["claude", "-p", prompt, "--model", MODEL, "--output-format", "stream-json", "--verbose",
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
    if mode in ALLOWED:
        cmd += ["--tools", "Bash", "--allowedTools", *ALLOWED[mode], "--max-turns", "30"]
        if mode == "pageindex":  # 目次の文字列を grep で照合すると、検索になってしまう
            cmd += ["--disallowedTools", "Bash(grep:*)", "Bash(rg:*)", "Bash(awk:*)", "Bash(sed:*)"]
    else:
        cmd += ["--tools", ""]
    env = {**os.environ, "KAIGO_EXCLUDE": ",".join(map(str, excl))}
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1200, cwd=WORK, env=env)
    events = [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
    calls = [b["input"].get("command", "") for e in events if e.get("type") == "assistant"
             for b in e["message"]["content"] if b.get("type") == "tool_use"]
    final = next((e for e in reversed(events) if e.get("type") == "result"), {})
    return final.get("result", ""), calls, final.get("num_turns", 0)


def parse(text):
    m = re.search(r"\{[^{}]*\"answer\"[^{}]*\}", text, re.S)
    try:
        obj = json.loads(m.group(0))
        return obj.get("answer", ""), [int(x) for x in obj.get("evidence", []) if str(x).isdigit()]
    except Exception:
        return text.strip()[-600:], []


def main(mode):
    WORK.mkdir(exist_ok=True)
    shutil.copy(ROOT / "src/tool.py", WORK / "tool.py")
    qa = {json.loads(l)["qa_id"]: json.loads(l) for l in open(ROOT / "data/qa_all.jsonl")}
    set_b = [json.loads(l) for l in open(ROOT / "data/set_b.jsonl")]
    set_b = [x for x in set_b if qa[x["qa_id"]]["question"].strip()]
    same = leaks()
    tag = os.environ.get("KAIGO_TAG", "")  # 資料を足した後の版などを、別のファイルに分ける(例: _v2)
    out = ROOT / f"results/answers_{mode}{tag}.jsonl"
    done = {json.loads(l)["qa_id"] for l in open(out)} if out.exists() else set()
    todo = [x for x in set_b if x["qa_id"] not in done][: int(sys.argv[2]) if len(sys.argv) > 2 else None]

    def one(x):
        t0 = time.time()
        excl = same(x["qa_id"])
        q = f"質問: {x['query']}"
        if mode == "llm":
            prompt = f"{RULES}\n資料は渡しません。知っていることで答え、evidence は空にしてください。\n\n{q}"
        elif mode == "rag":
            hits = tool.get("/search", excl, q=x["query"])[:5]
            ctx = "\n\n".join(f"[{h['id']}] {h['doc']} > {h['path']}\n{tool.get('/read', excl, id=h['id'])['text']}" for h in hits)
            prompt = f"{RULES}\n\n資料:\n{ctx}\n\n{q}"
        else:
            prompt = f"{RULES}\n\n{TOOLS[mode]}\n\n{q}"
        text, calls, turns = run_claude(prompt, mode, excl)
        ans, ev = parse(text)
        rec = {"qa_id": x["qa_id"], "answer": ans, "evidence": ev,
               "searches": [c for c in calls if " search " in c or " tree" in c or " related " in c],
               "reads": [c for c in calls if " read " in c], "turns": turns, "sec": round(time.time() - t0)}
        with open(out, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(mode, x["qa_id"], rec["sec"], "s", len(rec["searches"]), "searches", len(ev), "evidence", flush=True)

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(one, todo))


if __name__ == "__main__":
    main(sys.argv[1])  # 2つ目の引数で、件数を絞って試せる
