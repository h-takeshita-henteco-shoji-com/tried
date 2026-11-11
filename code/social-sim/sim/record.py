"""記録と再現の部品。1回の実行を1つのフォルダに残す。

- manifest.json: モデル名と版、プロンプトのファイルとハッシュ、設定値、seed、git の版
- calls.jsonl: AIへの問いと答えを1行ずつ(費用・トークン・時間つき)
- events.jsonl: ルールの計算結果(ラウンドごとの拠出や利得など)
"""
import datetime
import hashlib
import json
import os
import subprocess
import threading


def prompt_version(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def git_rev():
    r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    dirty = subprocess.run(["git", "status", "--porcelain", "--", os.path.dirname(__file__)],
                           capture_output=True, text=True).stdout.strip()
    return r.stdout.strip() + ("+dirty" if dirty else "")


class Run:
    def __init__(self, root, name, config, llm, prompts):
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.dir = os.path.join(root, f"{stamp}-{name}")
        os.makedirs(self.dir)
        self._lock = threading.Lock()
        self.cost = 0.0
        self.calls = 0
        self.manifest = {
            "name": name,
            "started": stamp,
            "llm": llm.name,
            "llm_version": llm.version(),
            "git": git_rev(),
            "prompts": {os.path.relpath(p): prompt_version(p) for p in prompts},
            "config": config,
        }
        self._write_manifest()

    def _write_manifest(self):
        with open(os.path.join(self.dir, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(self.manifest, f, ensure_ascii=False, indent=2)

    def _append(self, fname, row):
        with self._lock, open(os.path.join(self.dir, fname), "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    def call(self, who, system, prompt, reply, tag=None):
        with self._lock:
            self.cost += reply.cost_usd
            self.calls += 1
        self._append("calls.jsonl", {
            "who": who, "tag": tag, "system": system, "prompt": prompt,
            "output": reply.output, "raw": reply.raw, "cost_usd": reply.cost_usd,
            "tokens_in": reply.tokens_in, "tokens_out": reply.tokens_out,
            "seconds": round(reply.seconds, 2), "meta": reply.meta})

    def event(self, row):
        self._append("events.jsonl", row)

    def finish(self, summary):
        self.manifest["summary"] = summary
        self.manifest["calls"] = self.calls
        self.manifest["cost_usd"] = round(self.cost, 6)
        self._write_manifest()
