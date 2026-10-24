#!/usr/bin/env python3
"""市役所と議会のハーネスの hooks(#100)。設計は council-design.md の6.5、呼び方は council-interfaces.md の10。

標準入力に Claude Code の hook の JSON を受ける。引数で場面を分ける。

    guard.py pre   PreToolUse。決まりに外れたら permissionDecision: deny を返す
    guard.py post  PostToolUse。hooks の記録に1行足す。advance の後は状態のファイルの advanced を true にする
    guard.py stop  Stop(定義のフロントマターでは SubagentStop になる)。局の案のファイルが足りなければ exit 2

状態のファイル(既定 ~/.cache/ai-mayor/council-current.json)は、環境変数 COUNCIL_STATE で差し替えられる。
状態のファイルがない、または読めないときは何もしない(ハーネスの外で呼ばれたとき)。
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

STATE = Path(os.environ.get("COUNCIL_STATE", "~/.cache/ai-mayor/council-current.json")).expanduser()
BASE = os.environ.get("AIMAYOR_URL", "http://127.0.0.1:8781")
MCP_PREFIX = "mcp__cities-skylines__"

BUREAUS = ["urban", "roads", "port", "economy", "health", "education", "fire"]
VOTE_TOOLS = {
    "set_tax": "税",
    "set_budget": "予算", "set_transport_line_budget": "予算",
    "take_loan": "融資",
    "bulldoze": "取り壊し", "remove_line": "取り壊し", "remove_transport_line": "取り壊し",
}
TAX_RANGE = 2      # 税は今の値から±2まで
BUDGET_RANGE = 20  # 予算は今の値から±20まで

# 局の案の7点(council-design.md の5.2)と、どの役も書く3つ(interfaces の9)
PROPOSAL_LABELS = ["施策", "実行計画", "期待する効果", "費用", "戻せるか", "前の月の答え合わせ", "市の計画"]
THREE = ["見たもの", "判断の根拠", "捨てたもの"]
STOP_LIMIT = 3  # 書き直させるのは3回まで。それより多いと終わらなくなるおそれがあるため


def load_state():
    try:
        s = json.loads(STATE.read_text(encoding="utf-8"))
        return s if s.get("runDir") and s.get("month") else None
    except (OSError, ValueError, AttributeError):
        return None


def read_text_safe(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return None


def read_json(path):
    try:
        return json.loads(read_text_safe(path) or "")
    except ValueError:
        return None


def council_file(state, suffix):
    return Path(state["runDir"]) / "council" / f"m{int(state['month']):02d}-{suffix}"


def scrub(s):
    # hooks の記録は公開のリポジトリに入る。ホームのパスを ~ にし、タブと改行を消す
    s = str(s).replace(str(Path.home()), "~")
    s = " ".join(s.split())
    return s if len(s) <= 200 else s[:197] + "..."


def log(state, agent, tool, result, detail):
    path = council_file(state, "hooks.log")
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    line = "\t".join([now, agent or "?", tool, result, scrub(detail)]) + "\n"
    # 7つの局が同時に書くので、1行ずつ追記する
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)


def short_tool(name):
    return (name or "").replace(MCP_PREFIX, "")


def role(agent):
    """agent_type から役を返す。bureau / finance / assembly / mayor-desk / mayor-field / None"""
    a = (agent or "").replace("council-", "", 1) if (agent or "").startswith("council-") else None
    if a in BUREAUS:
        return "bureau"
    return a if a in ("finance", "assembly", "mayor-desk", "mayor-field") else None


def allowed_writes(state, agent):
    # 2の表で、その役に許したファイル
    r, name = role(agent), (agent or "").replace("council-", "", 1)
    if r == "bureau":
        names = [f"{name}.md"]
    elif r == "finance":
        names = ["guide.md", "finance.md"]
    elif r == "assembly":
        names = ["assembly.md", "assembly-2.md", "assembly.json"]
    else:
        return None  # 市長は Write を絞らない
    return {council_file(state, n).resolve() for n in names}


def economy():
    # MOD の窓口から今の税と予算を読む。届かなければ None
    try:
        with urllib.request.urlopen(f"{BASE}/economy", timeout=3) as r:
            d = json.loads(r.read().decode("utf-8"))
        return d if d.get("ok") else None
    except Exception:
        return None


def check_limits(tool, args):
    """税±2、予算±20 を超えたら理由を返す。超えなければ ""。MOD に届かなければ None。"""
    eco = economy()
    if eco is None:
        return None
    target = args.get("target")
    if tool == "set_tax":
        cur = (eco.get("tax") or {}).get(target)
        new = args.get("rate")
        if cur is not None and new is not None and abs(int(new) - int(cur)) > TAX_RANGE:
            return f"税 {target} を {cur} から {new} にする変更は、±{TAX_RANGE} の幅を超える"
        return ""
    cur = (eco.get("budget") or {}).get(target)
    if not cur:
        return ""
    for key, side in (("percent", "day"), ("percent", "night"), ("day", "day"), ("night", "night")):
        new = args.get(key)
        if new is not None and abs(int(new) - int(cur.get(side, new))) > BUDGET_RANGE:
            return f"予算 {target} の{'昼' if side == 'day' else '夜'}を {cur.get(side)} から {new} にする変更は、±{BUDGET_RANGE} の幅を超える"
    return ""


def deny(state, agent, tool, reason):
    log(state, agent, tool, "deny", reason)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=False))
    sys.exit(0)


def pre(state, data):
    agent = data.get("agent_type")
    tool = short_tool(data.get("tool_name"))
    args = data.get("tool_input") or {}

    # すべての定義: 費用なしの建設を止める
    if str(args.get("pay", "")).lower() == "false":
        deny(state, agent, tool, "pay=false(費用なしの建設)は使えない。pay を省くか true にする")

    # 局、財政局、議会: 許したファイルのほかへの Write を止める
    if tool == "Write":
        ok = allowed_writes(state, agent)
        target = args.get("file_path")
        if ok is not None and (not target or Path(target).expanduser().resolve() not in ok):
            names = ", ".join(sorted(p.name for p in ok))
            deny(state, agent, tool, f"この役が書いてよいのは {names} だけ。書こうとした先: {scrub(target)}")
        return

    kind = VOTE_TOOLS.get(tool)
    if kind:
        if role(agent) != "mayor-field":
            deny(state, agent, tool, f"議決が要る道具({kind})は、実行する市長のほかは使えない")
        if state.get("advanced"):
            deny(state, agent, tool, f"advance の後(臨時)は、議決が要る手({kind})を打たない")
        ruling = read_json(council_file(state, "assembly.json")) or {}
        if kind not in (ruling.get("approvedKinds") or []):
            deny(state, agent, tool, f"今月の議会は「{kind}」の議案を可決していない")
        if tool in ("set_tax", "set_budget"):
            why = check_limits(tool, args)
            if why is None:
                # 止めずに通す。確かめられなかったことだけ残す(結果の欄は warn)
                log(state, agent, tool, "warn", "MOD に届かず、税と予算の幅を確かめずに通した")
            elif why:
                deny(state, agent, tool, why)


def response_error(resp):
    """道具の返り値が ok:false なら、その error を返す。そうでなければ None。"""
    texts = []
    if isinstance(resp, dict):
        if resp.get("ok") is False:
            return str(resp.get("error") or "ok:false")
        texts = [resp.get("text") or ""] + [c.get("text", "") for c in resp.get("content") or [] if isinstance(c, dict)]
    elif isinstance(resp, list):
        texts = [c.get("text", "") for c in resp if isinstance(c, dict)]
    elif isinstance(resp, str):
        texts = [resp]
    for t in texts:
        try:
            d = json.loads(t)
        except (ValueError, TypeError):
            continue
        if isinstance(d, dict) and d.get("ok") is False:
            return str(d.get("error") or "ok:false")
    return None


def post(state, data):
    agent = data.get("agent_type")
    tool = short_tool(data.get("tool_name"))
    args = data.get("tool_input") or {}
    err = response_error(data.get("tool_response"))
    shown = " ".join(f"{k}={v}" for k, v in args.items())
    log(state, agent, tool, "ng" if err else "ok", err or shown)
    if tool == "advance" and not err and not state.get("advanced"):
        state["advanced"] = True
        tmp = STATE.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        tmp.replace(STATE)


def has_label(md, label):
    # 見出し、箇条書き、太字、「欄: 中身」のどれでもよい。行の頭にあれば書いたとみなす
    return re.search(r"^\s*(?:#+\s*|[-*]\s*)?(?:\*\*)?" + re.escape(label), md, re.M) is not None


def stop(state, data):
    agent = data.get("agent_type")
    if role(agent) != "bureau":
        return
    bureau = agent.replace("council-", "", 1)
    path = council_file(state, f"{bureau}.md")
    md = read_text_safe(path)
    if md is None:
        missing = [f"案のファイル {path.name} がない"]
    else:
        heads = [h for h in THREE if not re.search(r"^##\s*" + h, md, re.M)]
        # 案を出さない月は、7点は要らない。3つの見出しだけ見る
        none = re.search(r"案(は|を)?\s*(なし|出さない)|^\s*[-*]?\s*(\*\*)?施策(\*\*)?\s*[:：]\s*なし", md, re.M)
        labels = [] if none else [x for x in PROPOSAL_LABELS if not has_label(md, x)]
        missing = [f"案の欄「{x}」" for x in labels] + [f"見出し「## {h}」" for h in heads]
    if not missing:
        return
    denied = sum(1 for line in (read_text_safe(council_file(state, "hooks.log")) or "").splitlines()
                 if line.split("\t")[1:4] == [agent, "Stop", "deny"])
    if denied >= STOP_LIMIT:
        log(state, agent, "Stop", "ng", f"{STOP_LIMIT}回書き直させても足りないまま終えた: " + "、".join(missing))
        return
    reason = f"{path.name} に足りないものがある: " + "、".join(missing) + "。書き足してから終える"
    log(state, agent, "Stop", "deny", reason)
    print(reason, file=sys.stderr)
    sys.exit(2)


def main():
    scene = sys.argv[1] if len(sys.argv) > 1 else ""
    state = load_state()
    if state is None:
        return  # ハーネスの外。止めない
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    {"pre": pre, "post": post, "stop": stop}.get(scene, lambda s, d: None)(state, data)


if __name__ == "__main__":
    main()
