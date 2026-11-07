"""#136 の作図の課題を、MCP 経由と DXF を直接書く方法の両方で、モデルごとに1回ずつ流す。
#146 から、その日のフォルダと元の図面を引数で渡せるようにした(--day、--drawing)。

#135 の run_eval.py(DXF)と #134 の run_eval_mcp.py(MCP)の、コマンドの組み立てと記録の形をそのまま使う。
違いは、問いが「答える」ではなく「描き足して保存する」であることと、指示文をファイルから読むこと。

- DXF: 図面の写しだけを置いた空のフォルダで動かし、drawing-changed.dxf を保存させる
- MCP: 毎回 LibreCAD を起動し直し、図面の写しを開いてから AI を呼ぶ。LibreCAD は1つなので、1回ずつ順に流す
- 結果は <out>/<課題>-<方法>/<モデル>__<effort>/ に、run.json(記録)と drawing-changed.dxf(描いた図面)を置く

使い方:
  uv run python code/librecad-mcp/run_136.py --task K-1 --mode mcp --models claude-haiku-5-5,gemini-3.8-flash
"""
import argparse
import datetime as dt
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import run_eval_mcp as mcp
from run_eval_mcp import HERE, REPO, base

DAY = REPO / "2026/11-05-AIと図面のコラボレーション-05-AIに矩計図と平面詳細図を描かせる"
DRAWING = DAY / "base/house.dxf"
# 指示文は DAY/tasks/prompt-<課題>[-dxf].txt
TIMEOUT = 2400  # 40分。#135 の20分では、作図は終わらないモデルがあると見た


def run_one(task, mode, model, effort, out_root):
    dest = out_root / f"{task}-{mode}" / f"{model}__{effort}"
    if (dest / "run.json").exists():
        return None
    cli = base.MODELS[model]
    work = Path(tempfile.mkdtemp(prefix=f"run136-{mode}-"))
    drawing = work / "drawing.dxf"
    shutil.copy(DRAWING, drawing)
    changed = work / base.CHANGED
    suffix = "" if mode == "mcp" else "-dxf"
    tmpl = (DAY / f"tasks/prompt-{task}{suffix}.txt").read_text()
    if mode == "mcp":
        prompt = tmpl.format(file=str(drawing), changed=str(changed))
        for _ in range(3):
            if subprocess.run([str(HERE / "restart.sh")], capture_output=True).returncode == 0:
                break
        else:
            raise RuntimeError("LibreCAD を起動できません")
        if not mcp.lc_call("open", path=str(drawing)).get("ok"):
            raise RuntimeError("図面を開けません")
        cmd, stdin, env = mcp.build_command(model, effort, prompt, work)
    else:
        prompt = tmpl.format(file="drawing.dxf", changed=base.CHANGED)
        cmd, stdin, env = base.build_command(model, effort, "dxf", prompt)

    started = dt.datetime.now().astimezone()
    t0 = time.monotonic()
    try:
        p = subprocess.run(cmd, cwd=work, input=stdin if stdin is not None else "", capture_output=True,
                           text=True, env=env, timeout=TIMEOUT)
        code, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        code, out, err = "timeout", e.stdout or "", e.stderr or ""
    seconds = round(time.monotonic() - t0, 1)
    out = out if isinstance(out, str) else out.decode(errors="replace")
    err = err if isinstance(err, str) else err.decode(errors="replace")
    dest.mkdir(parents=True, exist_ok=True)
    if changed.exists():
        shutil.copy(changed, dest / "drawing-changed.dxf")
    tools = mcp.tool_uses(cli, out) if mode == "mcp" else []
    record = {
        "task": task, "mode": mode, "model": model, "effort": effort, "cli": cli,
        "cli_version": base.cli_version(cli), "command": cmd, "prompt": prompt,
        "started": started.isoformat(timespec="seconds"), "seconds": seconds, "exit": code,
        "stdout": out, "stderr": err,
        "files_created": sorted(str(f.relative_to(work)) for f in work.rglob("*") if f.name != "drawing.dxf"),
        "answer": mcp.final_answer(cli, out) if mode == "mcp" else base.final_answer(cli, out),
        "saved": changed.exists(),
    }
    if mode == "mcp":
        record.update(tools=tools, mcp_calls=sum(1 for t in tools if t.startswith("mcp:")),
                      non_mcp_tools=[t for t in tools if not t.startswith("mcp:")],
                      librecad_alive=mcp.librecad_alive())
    text = (base.without_init(out) + err).replace("https://errors.pydantic.dev", "")
    record["suspect_web_or_install"] = sorted(set(m.group(0) for m in base.SUSPECT.finditer(text)))
    (dest / "run.json").write_text(json.dumps(record, ensure_ascii=False, indent=2))
    shutil.rmtree(work, ignore_errors=True)
    work.parent.joinpath(f"{work.name}-mcp.json").unlink(missing_ok=True)
    return record


def run_list(task, mode, models, effort, out_root):
    for model in models:
        r = run_one(task, mode, model, effort, out_root)
        if r:
            print(f"{task} {mode} {model}: exit={r['exit']} {r['seconds']}s saved={r['saved']}", flush=True)


def run_both(task, models, effort, out_root):
    """DXF と MCP を並べて流す。agy の MCP の登録は利用者全体に効くので、
    DXF の側で agy を先に済ませ、それが終わってから MCP の側で agy を登録する。"""
    import threading
    agy = [m for m in models if base.MODELS[m] == "agy"]
    rest = [m for m in models if m not in agy]
    dxf_agy_done = threading.Event()

    def dxf():
        run_list(task, "dxf", agy, effort, out_root)
        dxf_agy_done.set()
        run_list(task, "dxf", rest, effort, out_root)

    def mcp_side():
        run_list(task, "mcp", rest, effort, out_root)
        if agy:
            dxf_agy_done.wait()
            mcp.agy_mcp(True)
            try:
                run_list(task, "mcp", agy, effort, out_root)
            finally:
                mcp.agy_mcp(False)

    ts = [threading.Thread(target=dxf), threading.Thread(target=mcp_side)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default="K-1")
    ap.add_argument("--mode", required=True, choices=["mcp", "dxf", "both"])
    ap.add_argument("--models", required=True)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--day", default=None, help="その日のフォルダ(既定は #136)")
    ap.add_argument("--drawing", default=None, help="元の図面(既定は <day>/base/house.dxf)")
    ap.add_argument("--out", default=None, help="既定は <day>/results/<今日>")
    a = ap.parse_args()
    global DAY, DRAWING
    if a.day:
        DAY = Path(a.day).resolve()
        DRAWING = DAY / "base/house.dxf"
    if a.drawing:
        DRAWING = Path(a.drawing).resolve()
    a.out = a.out or str(DAY / "results" / dt.date.today().isoformat())
    base.prepare_codex_home()
    models = a.models.split(",")
    if a.mode == "both":
        run_both(a.task, models, a.effort, Path(a.out))
        return
    uses_agy = a.mode == "mcp" and any(base.MODELS[m] == "agy" for m in models)
    if uses_agy:
        mcp.agy_mcp(True)
    try:
        run_list(a.task, a.mode, models, a.effort, Path(a.out))
    finally:
        if uses_agy:
            mcp.agy_mcp(False)


if __name__ == "__main__":
    main()
