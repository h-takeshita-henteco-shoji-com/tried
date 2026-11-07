"""図面について、同じ会話の中で続けて質問し、答えを記録する(#137)。

条件は run_eval.py にそろえる(空の作業フォルダ、個人の指示を読ませない、ネットとライブラリの導入を禁じる)。
違いは、1問ごとに新しい会話にせず、前の問いの会話を続けること。
- Claude: 1問目に --session-id を付け、2問目から --resume で続ける
- Codex: 1問目の出力から session id を拾い、2問目から codex exec resume で続ける
- Gemini(agy): 2問目から --continue で続ける(直近の会話を続けるので、agy は1つずつ流す)

問いは、その日のフォルダの answer-key/<会話>.md の「### Qnn 質問」の行。「期待:」の行は渡さない。

使い方: uv run python run_dialog.py --dialog dialog-1 --models claude-opus-5-5
"""
import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

import run_eval as R

DAY = R.REPO / "2026/11-07-AIと図面のコラボレーション-08-AIに図面から室内ツアーを作らせる"
DRAWING = DAY / "base/house-t.dxf"
SHEET = DAY / "tasks/tategu-hyo.md"
TIMEOUT = 900

FIRST = """作業フォルダに、2LDKの平屋の図面ファイル（drawing.dxf、単位はmm）と、建具表（建具表.md）があります。
図面には、平面図、立面図（南・北・東・西）、断面図（A-A、B-B）、矩計図、平面詳細図が入っています。
これから、この図面について続けて質問します。毎回、次の形で短く答えてください。
- 答え:
- 根拠: どの図・どの資料のどこを見たか（座標、レイヤー、表の記号など）

図面と建具表以外は見ないでください。インターネットで調べないでください。
ライブラリを新しく入れないでください。図面は書き換えないでください。

質問: {q}"""
NEXT = "質問: {q}"


def load(dialog):
    text = (DAY / "answer-key" / f"{dialog}.md").read_text()
    return re.findall(r"^### (Q\d+) (.+)$", text, re.M)


def command(model, effort, prompt, turn, state):
    cli = R.MODELS[model]
    env = dict(R.os.environ)
    if cli == "claude":
        sid = state.setdefault("sid", str(uuid.uuid4()))
        cmd = ["claude", "-p", prompt, "--safe-mode", "--model", model, "--effort", effort,
               "--permission-mode", "bypassPermissions", "--disallowedTools=WebFetch,WebSearch",
               "--output-format", "stream-json", "--verbose"]
        cmd += ["--session-id", sid] if turn == 0 else ["--resume", sid]
        return cmd, None, env
    if cli == "codex":
        env["CODEX_HOME"] = str(R.CODEX_HOME)
        opts = ["--skip-git-repo-check", "-m", model, "-c", f"model_reasoning_effort={effort}"]
        if turn == 0:
            return ["codex", "exec", *opts, "-s", "workspace-write", "-"], prompt, env
        return ["codex", "exec", "resume", *opts, state["sid"], "-"], prompt, env
    cmd = ["agy", "-p", prompt, "--model", f"{model}-{effort}", "--dangerously-skip-permissions",
           "--disable-slash-commands", "--print-timeout", f"{TIMEOUT}s", "--output-format", "stream-json"]
    if turn > 0:
        cmd.append("--continue")
    return cmd, None, env


def run(dialog, model, effort, out_root):
    dest = out_root / dialog / f"{model}__{effort}.json"
    if dest.exists():
        return None
    qs = load(dialog)
    work = Path(tempfile.mkdtemp(prefix="drawing-dialog-"))
    shutil.copy(DRAWING, work / "drawing.dxf")
    shutil.copy(SHEET, work / "建具表.md")
    cli = R.MODELS[model]
    state, turns = {}, []
    for i, (qid, q) in enumerate(qs):
        prompt = (FIRST if i == 0 else NEXT).format(q=q)
        cmd, stdin, env = command(model, effort, prompt, i, state)
        t0 = time.monotonic()
        try:
            p = subprocess.run(cmd, cwd=work, input=stdin, capture_output=True, text=True, env=env, timeout=TIMEOUT)
            code, out, err = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            code, out, err = "timeout", e.stdout or "", e.stderr or ""
            out = out if isinstance(out, str) else out.decode(errors="replace")
            err = err if isinstance(err, str) else err.decode(errors="replace")
        if cli == "codex" and i == 0:
            m = re.search(r"session id:\s*([0-9a-f-]{36})", err + out)
            state["sid"] = m.group(1) if m else None
        answer = R.final_answer(cli, out)
        turns.append({"qid": qid, "question": q, "prompt": prompt, "seconds": round(time.monotonic() - t0, 1),
                      "exit": code, "answer": answer, "stdout": out, "stderr": err,
                      "suspect_web_or_install": sorted(set(x.group(0) for x in R.SUSPECT.finditer(
                          R.without_init(out) + err)))})
        print(f"  {qid} {model}: exit={code} {turns[-1]['seconds']}s")
        if code != 0:
            break
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({
        "dialog": dialog, "model": model, "effort": effort, "cli": cli, "cli_version": R.cli_version(cli),
        "started": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "files_created": sorted(str(f.relative_to(work)) for f in work.rglob("*")
                                if f.name not in ("drawing.dxf", "建具表.md")),
        "turns": turns}, ensure_ascii=False, indent=2))
    shutil.rmtree(work, ignore_errors=True)
    return turns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dialog", default="dialog-1")
    ap.add_argument("--models", required=True)
    ap.add_argument("--efforts", default="medium")
    a = ap.parse_args()
    out_root = DAY / "results" / dt.date.today().isoformat()
    R.prepare_codex_home()
    for model in a.models.split(","):
        for effort in a.efforts.split(","):
            print(model, effort)
            run(a.dialog, model, effort, out_root)


if __name__ == "__main__":
    main()
