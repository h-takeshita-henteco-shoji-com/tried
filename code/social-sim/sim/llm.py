"""AIを動かす部品。人物像と状況を渡し、決まった形式(JSON)で答えを受け取る。

モデルは "claude:<モデル名>" や "dummy:<seed>" の文字列で差し替える。
claude は `claude -p` を空のフォルダから呼ぶ。リポジトリの CLAUDE.md を読ませないためと、
Claude Code の既定のシステムプロンプト(約6,600トークン)を外して費用を下げるため。
"""
import json
import random
import subprocess
import tempfile
import time
from dataclasses import dataclass, field

EMPTY = tempfile.mkdtemp(prefix="social-sim-")


@dataclass
class Reply:
    output: dict            # スキーマに沿った答え
    raw: str                # モデルが返した文字列
    cost_usd: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    seconds: float = 0.0
    meta: dict = field(default_factory=dict)


class Claude:
    def __init__(self, model, effort=None, timeout=300, retries=3):
        self.model = model
        self.effort = effort
        self.timeout = timeout
        self.retries = retries

    @property
    def name(self):
        return f"claude:{self.model}" + (f"@{self.effort}" if self.effort else "")

    def version(self):
        r = subprocess.run(["claude", "--version"], capture_output=True, text=True)
        return r.stdout.strip()

    def ask(self, system, prompt, schema):
        cmd = ["claude", "-p", "--model", self.model, "--tools", "", "--strict-mcp-config",
               "--setting-sources", "", "--no-session-persistence", "--output-format", "json",
               "--system-prompt", system, "--json-schema", json.dumps(schema, ensure_ascii=False)]
        if self.effort:
            cmd += ["--effort", self.effort]
        err = ""
        for _ in range(self.retries):
            t0 = time.time()
            try:
                r = subprocess.run(cmd + [prompt], capture_output=True, text=True,
                                   cwd=EMPTY, timeout=self.timeout)
            except subprocess.TimeoutExpired:
                err = "timeout"
                continue
            if r.returncode != 0:
                err = r.stderr or r.stdout
                continue
            d = json.loads(r.stdout)
            out = d.get("structured_output")
            if d.get("is_error") or not isinstance(out, dict):
                err = r.stdout
                continue
            u = d.get("usage", {})
            tin = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) \
                + u.get("cache_read_input_tokens", 0)
            return Reply(out, d.get("result", ""), d.get("total_cost_usd", 0.0), tin,
                         u.get("output_tokens", 0), time.time() - t0,
                         {"session_id": d.get("session_id"), "num_turns": d.get("num_turns")})
        raise RuntimeError(f"{self.name}: {err[:500]}")


class Dummy:
    """お金をかけずに配線を確かめるための、でたらめに答える相手。"""

    def __init__(self, seed="0"):
        self.rng = random.Random(seed)
        self.seed = seed

    @property
    def name(self):
        return f"dummy:{self.seed}"

    def version(self):
        return "dummy"

    def ask(self, system, prompt, schema):
        out = {k: self._fake(v) for k, v in schema["properties"].items()}
        return Reply(out, json.dumps(out, ensure_ascii=False))

    def _fake(self, s):
        t = s.get("type")
        if t == "integer":
            return self.rng.randint(s.get("minimum", 0), s.get("maximum", 10))
        if t == "array":
            return [self._fake(s["items"]) for _ in range(s.get("minItems", 0))]
        if "enum" in s:
            return self.rng.choice(s["enum"])
        return "(dummy)"


def backend(spec):
    kind, _, rest = spec.partition(":")
    if kind == "claude":
        model, _, effort = rest.partition("@")
        return Claude(model, effort or None)
    if kind == "dummy":
        return Dummy(rest or "0")
    raise ValueError(f"知らない相手: {spec}")
