"""`/council-month` の手順6〜10を、1か月の Workflow が終わった後にまとめて行う(#105)。

親が毎月呼ぶ。ハーネスの部品(council-design.md の12の「固めるもの」)ではなく、親の片づけの道具。

使い方:
  python3 code/ai-mayor/tools/council_after_month.py <運営のフォルダ> <月> <Workflow の出力ファイル> <Workflow の journal.jsonl>

すること:
  6. 返り値を council/mMM-run.json に書く
  7. check_council_month.py を回し、市政ノートの「## 型から外れたこと」に足す
  8. 役ごとの会話の記録を transcripts/mMM-<段>-<役>.md に抜き出す
  9. 台帳と議事録を作る
  10. 段ごと・局ごとのトークン数と時間を、市政ノートの「## 費用」に足す
"""
import json
import os
import re
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))

# Workflow の段の名前から、ファイル名に使う段の英字
STAGE = {"見る": "see", "要領": "guide", "案": "proposal", "査定": "assess", "まとめ": "bill",
         "議会": "assembly", "直す": "fix", "議会2": "assembly2", "実行": "field"}


def run(args: list[str]) -> str:
    r = subprocess.run(args, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def append_section(note: str, heading: str, body: str) -> None:
    s = open(note, encoding="utf-8").read()
    if heading not in s:
        s = s.rstrip("\n") + f"\n\n{heading}\n"
    # 見出しの直後(次の見出しの前)に足す
    i = s.index(heading) + len(heading)
    m = re.search(r"\n## ", s[i:])
    j = i + m.start() if m else len(s)
    s = s[:j].rstrip("\n") + "\n\n" + body.strip() + "\n" + s[j:]
    open(note, "w", encoding="utf-8").write(s)


def main() -> None:
    run_dir, month, out_file, journal = os.path.abspath(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    mm = f"{month:02d}"
    out = json.load(open(out_file, encoding="utf-8"))
    os.makedirs(os.path.join(run_dir, "council"), exist_ok=True)
    json.dump(out["result"], open(os.path.join(run_dir, "council", f"m{mm}-run.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"6. wrote council/m{mm}-run.json")

    note = os.path.join(run_dir, "mayor-note.md")
    check = run(["python3", os.path.join(TOOLS, "check_council_month.py"), run_dir, str(month)])
    append_section(note, "## 型から外れたこと", f"### {month}か月目(check_council_month.py)\n\n```\n{check or 'なし'}\n```")
    print("7. check:", check[:300] or "なし")

    agents = [a for a in out.get("workflowProgress", []) if a.get("type") == "workflow_agent"]
    os.makedirs(os.path.join(run_dir, "transcripts"), exist_ok=True)
    rows = []
    for a in agents:
        label = a.get("label", "")
        parts = label.split()
        stage = STAGE.get(parts[0], parts[0]) if parts else "agent"
        who = parts[1] if len(parts) > 1 and not parts[1].startswith("m") else a.get("agentType", "").replace("council-", "")
        dest = os.path.join(run_dir, "transcripts", f"m{mm}-{stage}-{who}.md")
        msg = run(["python3", os.path.join(TOOLS, "extract_transcript.py"), a["agentId"], dest,
                   "--raw-dir", os.path.expanduser("~/ai-mayor-transcripts/council")])
        ended = a.get("endedAt") or a.get("lastProgressAt") or a.get("startedAt")
        minutes = (ended - a["startedAt"]) / 60000 if a.get("startedAt") and ended else 0
        rows.append((label, a.get("agentType", ""), a.get("model", ""), a.get("tokens", 0), a.get("toolCalls", 0), minutes))
        print("8.", label, "->", os.path.basename(dest), "|", msg.splitlines()[0] if msg else "")

    print("9.", run(["python3", os.path.join(TOOLS, "make_council_ledger.py"), run_dir, str(month)])[:200])
    print("9.", run(["python3", os.path.join(TOOLS, "make_council_minutes.py"), run_dir, str(month)])[:200])

    lines = [f"### {month}か月目", "", f"- 合計: {out.get('totalTokens', 0):,} トークン、道具の呼び出し {out.get('totalToolCalls', 0)} 回",
             "", "| 役 | モデル | トークン | 道具 | 分 |", "|---|---|---|---|---|"]
    for label, typ, model, tok, calls, mins in rows:
        lines.append(f"| {label}({typ.replace('council-', '')}) | {model} | {tok:,} | {calls} | {mins:.1f} |")
    append_section(note, "## 費用", "\n".join(lines))
    print("10. cost written")


if __name__ == "__main__":
    main()
