"""図面の問いを、3社のCLIに1問ずつ解かせて記録する(#132、#138)。

条件をそろえるため、次のようにする。
- 1問ごとに新しい会話。図面だけを置いた空のフォルダで動かす。
- ファイル名は drawing.dxf / drawing.png にし、名前を答えの手掛かりにしない。
- 個人の指示を読ませない。Claude は --safe-mode、Codex は専用の CODEX_HOME。
- ライブラリは入れさせず、標準のPythonだけで読ませる。インターネットは使わせない。
  ネットを止められるのは Codex だけなので、ほかは指示で禁じ、記録をあとで確かめる。

使い方:
  uv run python run_eval.py --drawing L --format dxf --models claude-haiku-5-5,gpt-6-luna \
      --efforts low --questions L-2-1
  uv run python run_eval.py --issue 138 --drawing P --format dxf --models claude-haiku-5-5
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DAY132 = REPO / "2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる"
DAY138 = REPO / "2026/11-02-AIと図面のコラボレーション-02-AIに図面の寸法を正確に読ませる"
STD = DAY132 / "assets/drawings/建築工事標準詳細図"

# Issue ごとの、記録の置き場所と、図面(拡張子なし)と、正解の記録
ISSUES = {
    "132": {"day": DAY132, "drawings": {"L": STD / "001126048-p09", "M": STD / "001126048-p13",
                                        "H": STD / "001126051-p15"},
            "keys": {"L": "L-4-01.md", "M": "M-4-21.md", "H": "H-9-32.md"}},
    "138": {"day": DAY138, "drawings": {"P": DAY138 / "assets/drawings/plan-office", "H": STD / "001126051-p15"},
            "keys": {"P": "P-office.md", "H": "H-9-32.md"}},
}

# 個人の AGENTS.md を読ませないための Codex の置き場所。ログインのファイルだけをリンクする
CODEX_HOME = Path.home() / ".cache/drawing-eval/codex-home"

TIMEOUT_SEC = 1200

PROMPT = """作業フォルダにある図面ファイル（{file}）を読み、次の問いに日本語で答えてください。

問い: {question}

次の形で答えてください。
- 答え:
- 根拠: 図面のどこを見たか（図の名前、注記、表など）
- 確かさ: 図面に書かれている／図面から推測した／図面からは分からない

作業フォルダの図面ファイル以外は見ないでください。インターネットで調べないでください。
ライブラリを新しく入れないでください。"""

# #138 は寸法を問うので、値の出どころと、対象の寸法線や図形も書かせる
PROMPT_138 = """作業フォルダにある図面ファイル（{file}）を読み、次の問いに日本語で答えてください。

問い: {question}

次の形で答えてください。
- 答え:
- 値の出どころ: 寸法に書かれた値／図形から測った・計算した値／図面からは分からない
- 根拠: 図面のどこを見たか（図の名前、寸法線、図形、注記など）。計算したときは式も書く
- 確かさ: 図面に書かれている／図面から推測した／図面からは分からない

作業フォルダの図面ファイル以外は見ないでください。インターネットで調べないでください。
ライブラリを新しく入れないでください。"""

MODELS = {
    "claude-haiku-5-5": "claude",
    "claude-sonnet-5-5": "claude",
    "claude-opus-5-5": "claude",
    "claude-fable-5-1": "claude",
    "gpt-6-luna": "codex",
    "gpt-6.1-terra": "codex",
    "gpt-6.1-sol": "codex",
    "gpt-6-astra": "codex",
    "gemini-3.8-flash": "agy",
    "gemini-4-argon": "agy",
}


def load_questions(issue, drawing):
    cfg = ISSUES[issue]
    text = (cfg["day"] / "answer-key" / cfg["keys"][drawing]).read_text()
    return dict(re.findall(r"^### ([LMHP]-\d-\d) (.+)$", text, re.M))


def prepare_codex_home():
    CODEX_HOME.mkdir(parents=True, exist_ok=True)
    link = CODEX_HOME / "auth.json"
    if not link.exists():
        link.symlink_to(Path.home() / ".codex/auth.json")


def build_command(model, effort, fmt, prompt):
    """CLIごとのコマンドと、標準入力に渡す文、環境変数を返す。"""
    cli = MODELS[model]
    env = dict(os.environ)
    if cli == "claude":
        cmd = ["claude", "-p", prompt, "--safe-mode", "--model", model, "--effort", effort,
               "--permission-mode", "bypassPermissions", "--no-session-persistence",
               "--disallowedTools=WebFetch,WebSearch", "--output-format", "stream-json", "--verbose"]
        return cmd, None, env
    if cli == "codex":
        env["CODEX_HOME"] = str(CODEX_HOME)
        cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "workspace-write",
               "-m", model, "-c", f"model_reasoning_effort={effort}"]
        if fmt == "png":
            cmd += ["--image", "drawing.png"]
        return cmd + ["-"], prompt, env
    cmd = ["agy", "-p", prompt, "--model", f"{model}-{effort}", "--dangerously-skip-permissions",
           "--disable-slash-commands", "--print-timeout", f"{TIMEOUT_SEC}s",
           "--output-format", "stream-json"]
    return cmd, None, env


# 道具の使い方の記録から、通信やライブラリの導入の疑いを探す
SUSPECT = re.compile(r"search_web|read_url_content|open_browser_url|"
                     r"pip3? install|uv (pip|add)|curl |wget |https?://(?!www\.mlit|www\.w3\.org)", re.I)


def without_init(out):
    """最初の init の行は、使える道具の一覧を含むため、疑いの検索から外す。"""
    keep = []
    for line in out.splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            keep.append(line)
            continue
        if d.get("event") == "init" or (d.get("type") == "system" and d.get("subtype") == "init"):
            continue
        keep.append(line)
    return "\n".join(keep)


def final_answer(cli, out):
    """CLIの出力から、最後の答えの文だけを取り出す。"""
    if cli == "codex":
        return out.strip()
    key = {"claude": ("type", "result", "result"), "agy": ("event", "result", None)}[cli]
    answer = ""
    for line in out.splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get(key[0]) == key[1]:
            answer = d.get("result") if cli == "claude" else d["result"].get("response", "")
    return (answer or "").strip()


def cli_version(cli):
    args = {"claude": ["claude", "--version"], "codex": ["codex", "--version"],
            "agy": ["agy", "--version"]}[cli]
    return subprocess.run(args, capture_output=True, text=True).stdout.strip()


def run_one(issue, drawing, fmt, model, effort, qid, question, out_root):
    dest = out_root / f"{drawing}-{fmt}" / f"{model}__{effort}"
    if (dest / f"{qid}.json").exists():
        return None  # 中断のあとに流し直すとき、済んだ問いは飛ばす
    file = f"drawing.{fmt}"
    prompt = (PROMPT_138 if issue == "138" else PROMPT).format(file=file, question=question)
    work = Path(tempfile.mkdtemp(prefix="drawing-eval-"))
    src = ISSUES[issue]["drawings"][drawing]
    shutil.copy(f"{src}.{fmt}", work / file)
    cmd, stdin, env = build_command(model, effort, fmt, prompt)
    started = dt.datetime.now().astimezone()
    t0 = time.monotonic()
    try:
        p = subprocess.run(cmd, cwd=work, input=stdin, capture_output=True, text=True,
                           env=env, timeout=TIMEOUT_SEC)
        code, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        code, out, err = "timeout", e.stdout or "", e.stderr or ""
    seconds = round(time.monotonic() - t0, 1)
    created = sorted(str(f.relative_to(work)) for f in work.rglob("*") if f.name != file)
    record = {
        "qid": qid, "question": question, "drawing": drawing, "drawing_file": src.name,
        "format": fmt, "model": model, "effort": effort, "cli": MODELS[model],
        "cli_version": cli_version(MODELS[model]), "command": cmd, "prompt": prompt,
        "started": started.isoformat(timespec="seconds"), "seconds": seconds, "exit": code,
        "stdout": out if isinstance(out, str) else out.decode(errors="replace"),
        "stderr": err if isinstance(err, str) else err.decode(errors="replace"),
        "files_created": created,
        "answer": final_answer(MODELS[model], out if isinstance(out, str) else ""),
    }
    record["suspect_web_or_install"] = sorted(set(m.group(0) for m in SUSPECT.finditer(
        without_init(record["stdout"]) + record["stderr"])))
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{qid}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2))
    shutil.rmtree(work, ignore_errors=True)
    return record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", default="132", choices=ISSUES)
    ap.add_argument("--drawing", required=True, choices=["L", "M", "H", "P"])
    ap.add_argument("--format", required=True, choices=["dxf", "png"])
    ap.add_argument("--models", required=True)
    ap.add_argument("--efforts", default="medium")
    ap.add_argument("--questions", default="all")
    ap.add_argument("--out", default=None, help="結果の置き場所。既定は results/今日の日付")
    a = ap.parse_args()

    questions = load_questions(a.issue, a.drawing)
    qids = list(questions) if a.questions == "all" else a.questions.split(",")
    out_root = Path(a.out) if a.out else ISSUES[a.issue]["day"] / "results" / dt.date.today().isoformat()
    prepare_codex_home()
    for model in a.models.split(","):
        for effort in a.efforts.split(","):
            for qid in qids:
                r = run_one(a.issue, a.drawing, a.format, model, effort, qid, questions[qid], out_root)
                if r is None:
                    continue
                flag = f" 要確認:{r['suspect_web_or_install']}" if r["suspect_web_or_install"] else ""
                print(f"{qid} {a.format} {model} {effort}: exit={r['exit']} {r['seconds']}s{flag}")


if __name__ == "__main__":
    main()
