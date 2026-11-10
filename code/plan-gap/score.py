"""AI の指摘を、混ぜた不備の一覧と突き合わせて採点する。

指摘が混ぜた不備と同じものを指すかは、AI(opus)に判定させる(観点の記号に頼らないため、list と free で同じ物差しにする)。
判定の結果は data/judge/<条件>.json に残し、2回目からは読み直す。
使い方: python3 score.py <条件のフォルダ名> ...   例: python3 score.py sonnet-list-1 opus-free-1
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
import os
DATA = HERE / os.environ.get("DATA", "data")
ANS = json.loads((DATA / "answers.json").read_text())

JUDGE = """あなたは採点者です。訪問介護の書類点検で、AI が挙げた指摘が、こちらで仕込んだ不備と同じものを指しているかを判定します。
仕込んだ不備(正解): {truth}
AI の指摘(番号つき):
{findings}

各指摘について、次のどれかを付けてください。
- hit: 仕込んだ不備と同じ問題を指している(言い方や細部が違ってもよい)
- other: 仕込んだ不備とは別のことを指している
JSON だけを返してください。形: {{"labels": ["hit" または "other", ...]}}  (指摘と同じ数、同じ順)"""


def judge(truth, findings):
    if not findings:
        return []
    fs = "\n".join(f"{i + 1}. [{f.get('category', '')}] {f.get('where', '')} / {f.get('what', '')}" for i, f in enumerate(findings))
    cmd = ["claude", "-p", "--model", "opus", "--output-format", "text", "--tools", "",
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
    for _ in range(3):
        r = subprocess.run(cmd, input=JUDGE.format(truth=truth, findings=fs), capture_output=True, text=True, timeout=600, cwd="/tmp")
        t = r.stdout
        try:
            labels = json.loads(t[t.find("{"): t.rfind("}") + 1])["labels"]
            if len(labels) == len(findings):
                return labels
        except Exception:
            pass
    return ["other"] * len(findings)


def score(cond):
    out = DATA / "out" / cond
    jpath = DATA / "judge" / f"{cond}.json"
    jpath.parent.mkdir(exist_ok=True)
    cache = json.loads(jpath.read_text()) if jpath.exists() else {}

    def one(uid):
        a = ANS[uid]
        res = json.loads((out / f"{uid}.json").read_text())
        fs = res.get("findings", [])
        if uid not in cache:
            if a["type"] in ("trap", "clean"):
                cache[uid] = ["other"] * len(fs)
            else:
                cache[uid] = judge(f"{a['label']}。{a['detail']}", fs)
        return uid

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(one, sorted(ANS)))
    jpath.write_text(json.dumps(cache, ensure_ascii=False, indent=1))

    rows = []
    for uid, a in sorted(ANS.items()):
        res = json.loads((out / f"{uid}.json").read_text())
        fs = res.get("findings", [])
        labels = cache[uid]
        rows.append({"uid": uid, "type": a["type"], "n": len(fs), "hit": "hit" in labels,
                     "other": labels.count("other"),
                     "cat_hit": any(f.get("category") == a["type"] for f in fs), "error": "error" in res})
    d = [r for r in rows if r["type"] not in ("trap", "clean")]
    t = [r for r in rows if r["type"] == "trap"]
    c = [r for r in rows if r["type"] == "clean"]
    summary = {
        "cond": cond,
        "recall": f"{sum(r['hit'] for r in d)}/{len(d)}",
        "trap_flagged": f"{sum(r['n'] > 0 for r in t)}/{len(t)}",
        "clean_flagged": f"{sum(r['n'] > 0 for r in c)}/{len(c)}",
        "extra_on_defect": sum(r["other"] for r in d),
        "errors": sum(r["error"] for r in rows),
        "by_type": {k: f"{sum(r['hit'] for r in d if r['type'] == k)}/{sum(1 for r in d if r['type'] == k)}" for k in "ABCDEF"},
        "missed": [r["uid"] for r in d if not r["hit"]],
        "trap_flagged_ids": [r["uid"] for r in t if r["n"] > 0],
    }
    return summary, rows


def main():
    allsum = []
    for cond in sys.argv[1:]:
        s, rows = score(cond)
        allsum.append(s)
        print(json.dumps(s, ensure_ascii=False))
    (DATA / "summary.json").write_text(json.dumps(allsum, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
