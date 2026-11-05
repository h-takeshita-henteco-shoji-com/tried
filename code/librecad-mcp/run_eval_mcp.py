"""#132・#138・#135 と同じ問いを、LibreCAD の MCP 経由で AI に解かせる(#134)。

DXF を直接読ませた回(code/drawings/run_eval.py)と、問い・正解・記録の形をそろえる。
違いは、図面を LibreCAD で開いておき、AI には MCP の道具で読み書きさせること。

- 毎回 LibreCAD を起動し直し(restart.sh)、図面の写しを開いてから AI を呼ぶ。前の回の状態を持ち越さないため
- Claude は --setting-sources "" で個人の設定と CLAUDE.md を読ませず(--safe-mode は MCP も止めるため使えない)、
  --strict-mcp-config で librecad だけをつなぐ。シェルと書き込みの道具は外す。画像を見るため Read は残す
- Codex は MCP 用の CODEX_HOME を使う。シェルは外せないので read-only にし、使ったかを記録する
- Gemini(agy)は、流す間だけ利用者の設定に librecad を登録し、終わったら外す
- MCP 以外の道具を使ったか(non_mcp_tools)と、LibreCAD が落ちたか(librecad_alive)も記録する

使い方(LibreCAD が入っていて、plugin を build.sh で入れてあること):
  uv run python code/librecad-mcp/run_eval_mcp.py --issue 135 --drawing C --models claude-haiku-5-5
"""
import argparse
import datetime as dt
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "drawings"))
import run_eval as base  # noqa: E402

REPO = HERE.parent.parent
DAY134 = REPO / "2026/11-05-AIと図面のコラボレーション-04-LibreCADにMCP機能を加える"
SERVER = HERE / "server.py"
CODEX_HOME_MCP = Path.home() / ".cache/drawing-eval/codex-home-mcp"
FMT = "mcp"

RULES = """図面は、librecad の MCP の道具で読んでください。図面ファイルを直接読んだり、シェルやプログラムで開いたりしないでください。
インターネットで調べないでください。"""

PROMPT = """LibreCAD に図面（{file}）が開いています。図面を読み、次の問いに日本語で答えてください。

問い: {question}

次の形で答えてください。
- 答え:
- 根拠: 図面のどこを見たか（図の名前、注記、表など）
- 確かさ: 図面に書かれている／図面から推測した／図面からは分からない

""" + RULES

PROMPT_138 = """LibreCAD に図面（{file}）が開いています。図面を読み、次の問いに日本語で答えてください。

問い: {question}

次の形で答えてください。
- 答え:
- 値の出どころ: 寸法に書かれた値／図形から測った・計算した値／図面からは分からない
- 根拠: 図面のどこを見たか（図の名前、寸法線、図形、注記など）。計算したときは式も書く
- 確かさ: 図面に書かれている／図面から推測した／図面からは分からない

""" + RULES

PROMPT_135 = """LibreCAD に図面（{file}）が開いています。2LDKの平屋の図面です。単位はmmです。
平面図、立面図（南・北・東・西）、断面図（A-A、B-B）が、1つの図面に入っています。
次の指示どおりに図面を変更し、平面図に合わせて、立面図と断面図もそろえて直してください。
変更後の図面を、librecad の save_as で {changed} に保存してください。
元のファイルは上書きしないでください（save は使わないでください）。

指示: {question}

指示どおりに変更できないときや、指示から決められないことがあるときは、図面を保存せずに、確認したいことを答えてください。

次の形で答えてください。
- 変更したこと:
- 一緒に動かしたもの: 壁、扉、窓、設備、寸法、通り芯、立面図、断面図など
- 確かめたこと:
- 確認したいこと: なければ「なし」

図面は、librecad の MCP の道具で読み書きしてください。図面ファイルを直接読んだり書いたり、シェルやプログラムで開いたりしないでください。
インターネットで調べないでください。"""


def lc_call(cmd, **args):
    with socket.create_connection(("127.0.0.1", 7471), timeout=60) as s:
        s.sendall((json.dumps({"id": 0, "cmd": cmd, "args": args}, ensure_ascii=False) + "\n").encode())
        buf = b""
        while not buf.endswith(b"\n"):
            c = s.recv(1 << 20)
            if not c:
                break
            buf += c
    return json.loads(buf) if buf else {"ok": False, "error": "no reply"}


def librecad_alive():
    try:
        return bool(lc_call("ping").get("ok"))
    except OSError:
        return False


def mcp_json(work):
    p = work.parent / f"{work.name}-mcp.json"
    p.write_text(json.dumps({"mcpServers": {"librecad": {"command": "uv", "args": ["run", "-q", str(SERVER)]}}}))
    return p


def build_command(model, effort, prompt, work):
    cli = base.MODELS[model]
    env = dict(base.os.environ)
    if cli == "claude":
        # --safe-mode は MCP も読み込まなくなる。代わりに設定の読み込み元を空にして、個人の指示を読ませない
        cmd = ["claude", "-p", prompt, "--setting-sources", "", "--disable-slash-commands",
               "--model", model, "--effort", effort,
               "--permission-mode", "bypassPermissions", "--no-session-persistence",
               "--mcp-config", str(mcp_json(work)), "--strict-mcp-config",
               "--disallowedTools=WebFetch,WebSearch,Bash,Write,Edit,NotebookEdit,Glob,Grep",
               "--output-format", "stream-json", "--verbose"]
        return cmd, None, env
    if cli == "codex":
        env["CODEX_HOME"] = str(CODEX_HOME_MCP)
        cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only", "--json",
               "-m", model, "-c", f"model_reasoning_effort={effort}", "-"]
        return cmd, prompt, env
    cmd = ["agy", "-p", prompt, "--model", f"{model}-{effort}", "--dangerously-skip-permissions",
           "--disable-slash-commands", "--print-timeout", f"{base.TIMEOUT_SEC}s",
           "--output-format", "stream-json"]
    return cmd, None, env


def tool_uses(cli, out):
    """使った道具の名前を、出てきた順に返す。MCP の道具は mcp:名前 にする。"""
    names = []
    for line in out.splitlines():
        try:
            m = json.loads(line)
        except ValueError:
            continue
        if cli == "claude" and m.get("type") == "assistant":
            for c in m["message"].get("content", []):
                if c.get("type") == "tool_use":
                    n = c["name"]
                    names.append("mcp:" + n.split("__")[-1] if n.startswith("mcp__librecad__")
                                 else n + ":" + json.dumps(c.get("input", {}), ensure_ascii=False)[:160])
        elif cli == "codex" and m.get("type") == "item.completed":
            it = m.get("item", {})
            if it.get("type") == "mcp_tool_call":
                names.append("mcp:" + it.get("tool", "?"))
            elif it.get("type") in ("command_execution", "file_change", "web_search"):
                names.append(it["type"] + ":" + str(it.get("command", ""))[:120])
        elif cli == "agy" and m.get("event") == "step_update":
            st = m.get("step_update", {})
            # 同じ道具の呼び出しが、状態ごとに何度も出る。終わった(DONE)ときだけ数える
            if st.get("step_type") == "tool" and st.get("state") == "DONE":
                info = st.get("tool_info", {})
                if st.get("tool_name") == "call_mcp_tool":
                    names.append("mcp:" + str(info.get("parameters", {}).get("ToolName", "?")))
                else:
                    # 何を読んだかで、図面を直接読んだのか、道具の結果を読んだのかを見分ける
                    names.append(str(st.get("tool_name")) + ":" + json.dumps(info.get("parameters", {}), ensure_ascii=False)[:160])
    return names


def final_answer(cli, out):
    if cli == "codex":
        msgs = []
        for line in out.splitlines():
            try:
                m = json.loads(line)
            except ValueError:
                continue
            if m.get("type") == "item.completed" and m.get("item", {}).get("type") == "agent_message":
                msgs.append(m["item"].get("text", ""))
        return msgs[-1] if msgs else ""
    return base.final_answer(cli, out)


def run_one(issue, drawing, model, effort, qid, question, out_root):
    dest = out_root / f"{drawing}-{FMT}" / f"{model}__{effort}"
    if (dest / f"{qid}.json").exists():
        return None
    cli = base.MODELS[model]
    work = Path(tempfile.mkdtemp(prefix="drawing-eval-mcp-"))
    src = base.ISSUES[issue]["drawings"][drawing]
    drawing_file = work / "drawing.dxf"
    shutil.copy(f"{src}.dxf", drawing_file)
    changed = work / base.CHANGED
    tmpl = {"138": PROMPT_138, "135": PROMPT_135}.get(issue, PROMPT)
    prompt = tmpl.format(file=str(drawing_file), question=question, changed=str(changed))

    for attempt in range(3):  # 再起動は、まれに失敗する。やり直す
        r = subprocess.run([str(HERE / "restart.sh")], capture_output=True, text=True)
        if r.returncode == 0:
            break
    else:
        raise RuntimeError(f"LibreCAD を起動できません: {r.stderr}")
    opened = lc_call("open", path=str(drawing_file))
    if not opened.get("ok"):
        raise RuntimeError(f"LibreCAD で図面を開けません: {opened}")

    cmd, stdin, env = build_command(model, effort, prompt, work)
    started = dt.datetime.now().astimezone()
    t0 = time.monotonic()
    try:
        p = subprocess.run(cmd, cwd=work, input=stdin if stdin is not None else "", capture_output=True, text=True,
                           env=env, timeout=base.TIMEOUT_SEC)
        code, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        code, out, err = "timeout", e.stdout or "", e.stderr or ""
    seconds = round(time.monotonic() - t0, 1)
    out = out if isinstance(out, str) else out.decode(errors="replace")
    err = err if isinstance(err, str) else err.decode(errors="replace")
    alive = librecad_alive()
    tools = tool_uses(cli, out)
    dest.mkdir(parents=True, exist_ok=True)
    if changed.exists():
        shutil.copy(changed, dest / f"{qid}.dxf")
    record = {
        "qid": qid, "question": question, "drawing": drawing, "drawing_file": src.name,
        "format": FMT, "model": model, "effort": effort, "cli": cli,
        "cli_version": base.cli_version(cli), "command": cmd, "prompt": prompt,
        "started": started.isoformat(timespec="seconds"), "seconds": seconds, "exit": code,
        "stdout": out, "stderr": err,
        "files_created": sorted(str(f.relative_to(work)) for f in work.rglob("*") if f.name != "drawing.dxf"),
        "answer": final_answer(cli, out),
        "tools": tools,
        "mcp_calls": sum(1 for t in tools if t.startswith("mcp:")),
        "non_mcp_tools": [t for t in tools if not t.startswith("mcp:")],
        "librecad_alive": alive,
    }
    # 道具の入力の誤りで出る pydantic のエラー文の URL は、通信ではないので外す
    text = (base.without_init(out) + err).replace("https://errors.pydantic.dev", "")
    record["suspect_web_or_install"] = sorted(set(m.group(0) for m in base.SUSPECT.finditer(text)))
    (dest / f"{qid}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2))
    shutil.rmtree(work, ignore_errors=True)
    work.parent.joinpath(f"{work.name}-mcp.json").unlink(missing_ok=True)
    return record


def agy_mcp(add):
    if add:
        subprocess.run(["agy", "mcp", "add", "librecad", "uv", "run", "-q", str(SERVER)], check=True,
                       capture_output=True)
    else:
        subprocess.run(["agy", "mcp", "remove", "librecad"], capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", default="135", choices=base.ISSUES)
    ap.add_argument("--drawing", required=True, choices=["L", "M", "H", "P", "C"])
    ap.add_argument("--models", required=True)
    ap.add_argument("--efforts", default="medium")
    ap.add_argument("--questions", default="all")
    ap.add_argument("--out", default=None, help="結果の置き場所。既定は #134 の results/今日の日付-issue番号")
    a = ap.parse_args()

    questions = base.load_questions(a.issue, a.drawing)
    qids = list(questions) if a.questions == "all" else a.questions.split(",")
    out_root = Path(a.out) if a.out else DAY134 / "results" / f"{dt.date.today().isoformat()}-{a.issue}"
    models = a.models.split(",")
    uses_agy = any(base.MODELS[m] == "agy" for m in models)
    if uses_agy:
        agy_mcp(True)
    try:
        for model in models:
            for effort in a.efforts.split(","):
                for qid in qids:
                    r = run_one(a.issue, a.drawing, model, effort, qid, questions[qid], out_root)
                    if r is None:
                        continue
                    flags = []
                    if r["non_mcp_tools"]:
                        flags.append(f"MCP以外:{len(r['non_mcp_tools'])}")
                    if not r["librecad_alive"]:
                        flags.append("LibreCADが落ちた")
                    if r["suspect_web_or_install"]:
                        flags.append(f"要確認:{r['suspect_web_or_install']}")
                    print(f"{qid} {model} {effort}: exit={r['exit']} {r['seconds']}s mcp={r['mcp_calls']} "
                          + " ".join(flags), flush=True)
    finally:
        if uses_agy:
            agy_mcp(False)


if __name__ == "__main__":
    main()
