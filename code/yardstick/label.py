"""AI(Claude Opus 5.5)に、文の役割、関連、特徴を見分けさせる。

claude -p を空のフォルダから呼び、ツールを使わせない。リポジトリの CLAUDE.md を読ませないためである。
使い方: python label.py <texts_dir> <out_dir> <run番号>
出力: <out_dir>/run<番号>/<文書>.{roles,relations,features}.tsv と raw.txt
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
from segment import load  # noqa: E402

MODEL = "claude-opus-5-5"
PROMPT = open(os.path.join(os.path.dirname(__file__), "prompts", "label.md"), encoding="utf-8").read()
EMPTY = tempfile.mkdtemp(prefix="yardstick-")


def numbered(doc):
    lines = [f"t00\t{doc['title']}"]
    prev = None
    for s in doc["sents"]:
        if s["par"] != prev:
            lines.append(f"[p{s['par']:02d}]")
            prev = s["par"]
        lines.append(f"{s['id']}\t{s['text']}")
    return "\n".join(lines)


def claude(prompt, model, system=None, session=None, resume=False):
    cmd = ["claude", "-p", "--model", model, "--tools", "", "--strict-mcp-config",
           "--setting-sources", "", "--output-format", "json"]
    if system:
        cmd += ["--system-prompt", system]
    if session:
        cmd += ["--resume", session] if resume else ["--session-id", session]
    for _ in range(3):
        try:
            # 応答が返らず止まる呼び出しがあったため、5分で打ち切ってやり直す
            r = subprocess.run(cmd + [prompt], capture_output=True, text=True, cwd=EMPTY, timeout=300)
        except subprocess.TimeoutExpired as e:
            r = subprocess.CompletedProcess(e.cmd, 1, "", "timeout")
            continue
        if r.returncode == 0:
            d = json.loads(r.stdout)
            if not d.get("is_error"):
                return d["result"]
    raise RuntimeError(r.stderr or r.stdout)


def block(text, name):
    m = re.search(rf"```{name}\n(.*?)```", text, re.S)
    return m.group(1).strip() + "\n" if m else ""


def run(path, out):
    doc_id = os.path.basename(path)[:-4]
    res = claude(PROMPT + "\n" + numbered(load(path)), MODEL)
    with open(f"{out}/{doc_id}.raw.txt", "w") as f:
        f.write(res)
    for name in ("roles", "relations", "features"):
        with open(f"{out}/{doc_id}.{name}.tsv", "w") as f:
            f.write(block(res, name))
    return doc_id


if __name__ == "__main__":
    texts, out_dir, n = sys.argv[1:4]
    out = f"{out_dir}/run{n}"
    os.makedirs(out, exist_ok=True)
    with ThreadPoolExecutor(4) as ex:
        for d in ex.map(lambda p: run(p, out), sorted(glob.glob(f"{texts}/*.txt"))):
            print("labeled", d, file=sys.stderr)
