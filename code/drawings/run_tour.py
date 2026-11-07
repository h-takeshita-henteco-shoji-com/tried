"""#137 の室内ツアーのページを、同じ会話の中で直していく。

1回目は run_eval.py --issue 137 で作った index.html を置いて始める。2回目からは前の回の会話を続け(claude --resume)、
前の回の index.html を引き継ぐ。回ごとの index.html と答えを results/<日付>/tour-opus/round-<n>/ に残す。
作業フォルダは回をまたいで同じものを使う(会話の中のファイルの場所がずれないように)。

使い方: uv run python run_tour.py --round 2 --prompt <指示のファイル>
"""
import argparse
import datetime as dt
import json
import shutil
import subprocess
import time
import uuid
from pathlib import Path

import run_eval as R

DAY = R.DAY137
RES = DAY / "results/2026-11-07"
FIRST = RES / "T-dxf/claude-opus-5-5__medium/V-1-1-files/index.html"
WORK = Path.home() / ".cache/drawing-eval/tour-opus"
STATE = RES / "tour-opus/state.json"
MODEL, EFFORT, TIMEOUT = "claude-opus-5-5", "medium", 3600


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--prompt", required=True)
    a = ap.parse_args()
    prompt = Path(a.prompt).read_text()
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    if a.round == 2 and not state:
        shutil.rmtree(WORK, ignore_errors=True)
        WORK.mkdir(parents=True)
        shutil.copy(DAY / "base/house-t.dxf", WORK / "drawing.dxf")
        shutil.copy(DAY / "tasks/finish-schedule.md", WORK / "仕上表.md")
        shutil.copy(DAY / "tasks/tategu-hyo.md", WORK / "建具表.md")
        shutil.copy(FIRST, WORK / "index.html")
        state = {"sid": str(uuid.uuid4()), "rounds": []}
        resume = ["--session-id", state["sid"]]
    else:
        resume = ["--resume", state["sid"]]
    cmd = ["claude", "-p", prompt, "--safe-mode", "--model", MODEL, "--effort", EFFORT,
           "--permission-mode", "bypassPermissions", "--disallowedTools=WebFetch,WebSearch",
           "--output-format", "stream-json", "--verbose", *resume]
    t0 = time.monotonic()
    p = subprocess.run(cmd, cwd=WORK, capture_output=True, text=True, timeout=TIMEOUT)
    sec = round(time.monotonic() - t0, 1)
    dest = RES / f"tour-opus/round-{a.round}"
    dest.mkdir(parents=True, exist_ok=True)
    for f in WORK.iterdir():
        if f.is_file() and f.suffix in (".html", ".js", ".md") and f.name not in ("仕上表.md", "建具表.md"):
            shutil.copy(f, dest / f.name)
    answer = R.final_answer("claude", p.stdout)
    (dest / "answer.json").write_text(json.dumps({
        "round": a.round, "model": MODEL, "effort": EFFORT, "prompt": prompt, "seconds": sec, "exit": p.returncode,
        "answer": answer, "stdout": p.stdout, "stderr": p.stderr,
        "started": dt.datetime.now().astimezone().isoformat(timespec="seconds")}, ensure_ascii=False, indent=2))
    state["rounds"].append({"round": a.round, "seconds": sec, "exit": p.returncode})
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    print(f"round {a.round}: exit={p.returncode} {sec}s")
    print(answer)


if __name__ == "__main__":
    main()
