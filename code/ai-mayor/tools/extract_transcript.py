"""市長のサブエージェントの会話の記録から、要点だけを Markdown に抜き出す(#92)。

生の記録(~/.claude/projects/<プロジェクト>/<セッション>/subagents/agent-<id>.jsonl)は、
1か月で約2MBあり、手元の絶対パスを含む。リポジトリは公開なので、生の記録は入れない。
代わりに、時刻・道具・引数・結果の要約・市長の発言を抜き出し、運営のフォルダに置く。
生の記録は --raw-dir に写して、リポジトリの外に残す。

    python3 code/ai-mayor/tools/extract_transcript.py <agent id> <出力の .md> [--raw-dir ~/ai-mayor-transcripts/<運営>]

thinking の中身は記録に残らない(欄はあるが空)。判断の理由は、市政ノートと explain で追う。
"""

import argparse
import json
import re
import shutil
from pathlib import Path

HOME = str(Path.home())
REPO = str(Path(__file__).resolve().parents[3])
PROJECTS = Path.home() / ".claude/projects"
ARG_LIMIT = 300
RESULT_LIMIT = 300


def find(agent_id):
    hits = list(PROJECTS.glob(f"*/*/subagents/agent-{agent_id}.jsonl"))
    if len(hits) != 1:
        raise SystemExit(f"agent-{agent_id}.jsonl が {len(hits)} 件見つかった")
    return hits[0]


ROOTS = {REPO}


def scrub(s):
    # 手元のパスを公開してよい形に直す。リポジトリの中は相対パスに、それ以外はホームを ~ にする
    for root in sorted(ROOTS, key=len, reverse=True):
        s = s.replace(root + "/", "").replace(root, ".")
    s = s.replace(HOME, "~")
    # 道具の結果の画像は ~/.claude/projects/ の下に置かれる。場所はユーザー名を含むので消す
    return re.sub(r"~/\.claude/projects/[^\s\]\)\"']+", "[手元の一時ファイル]", s)


def short(s, limit):
    s = " ".join(s.split())
    return s if len(s) <= limit else s[:limit - 3] + "..."


def result_text(content):
    if isinstance(content, str):
        return content
    parts = []
    for c in content or []:
        if c.get("type") == "text":
            parts.append(c.get("text", ""))
        elif c.get("type") == "image":
            parts.append("[画像]")
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("agent_id")
    ap.add_argument("out")
    ap.add_argument("--raw-dir")
    a = ap.parse_args()

    src = find(a.agent_id)
    meta_path = src.with_suffix(".meta.json")
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}

    rows, calls, model = [], {}, None
    for line in src.read_text(encoding="utf-8").splitlines():
        o = json.loads(line)
        if o.get("cwd"):
            ROOTS.add(o["cwd"])  # 別の worktree で走らせた記録も、その根を相対パスに直す
        msg = o.get("message") or {}
        model = model or msg.get("model")
        t = (o.get("timestamp") or "")[11:19]
        content = msg.get("content")
        if isinstance(content, str):
            rows.append(f"### {t} 依頼\n\n{scrub(content)}\n")
            continue
        for c in content or []:
            kind = c.get("type")
            if kind == "text" and c.get("text", "").strip():
                who = "市長" if o.get("type") == "assistant" else "依頼"
                rows.append(f"### {t} {who}\n\n{scrub(c['text'].strip())}\n")
            elif kind == "tool_use":
                name = c.get("name", "").replace("mcp__cities-skylines__", "")
                args = short(scrub(json.dumps(c.get("input", {}), ensure_ascii=False)), ARG_LIMIT)
                calls[c.get("id")] = len(rows)
                rows.append(f"- {t} `{name}` {args}")
            elif kind == "tool_result":
                i = calls.get(c.get("tool_use_id"))
                mark = "NG" if c.get("is_error") else "OK"
                res = short(scrub(result_text(c.get("content"))), RESULT_LIMIT)
                if i is not None:
                    rows[i] += f"\n  - {mark} {res}"

    head = [
        "# 会話の記録(要点)",
        "",
        f"- サブエージェント: {meta.get('agentType', '?')}",
        f"- モデル: {model or '?'}",
        f"- 道具の呼び出し: {len(calls)} 回",
        f"- 引数と結果は {ARG_LIMIT} 字で切った。手元のパスは相対パスか ~ に直した",
        "",
    ]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(head + rows) + "\n", encoding="utf-8")
    print(f"wrote {out}({len(calls)} calls)")

    if a.raw_dir:
        raw = Path(a.raw_dir).expanduser()
        raw.mkdir(parents=True, exist_ok=True)
        for p in (src, meta_path):
            if p.exists():
                shutil.copy2(p, raw / p.name)
        print(f"copied raw to {raw}")


if __name__ == "__main__":
    main()
