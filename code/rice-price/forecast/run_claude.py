"""Claude に米価を予測させる(#184 の段1a・1b・3a・3b)。

使い方: ../.venv/bin/python run_claude.py <条件> <回数>   条件: 1a 1b 3a 3b
Claude は空のフォルダから `claude -p` で呼ぶ。道具を持たせず、リポジトリも読めない。
入力は inputs/ の2026年8月までのデータだけ。出力は runs/<条件>/<n>.json。
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
P = HERE / "prompts"
MODEL = "claude-opus-5-5"
CONDS = {  # (需給の表を渡すか, 知識を使ってよいか)
    "1a": (False, False), "1b": (False, True), "3a": (True, False), "3b": (True, True),
}
MONTHS = ["2026-11", "2026-12", "2027-01", "2027-02", "2027-03", "2027-04",
          "2027-05", "2027-06", "2027-07", "2027-08"]
SCHEMA = {
    "type": "object",
    "properties": {
        "knowledge": {"type": "string"},
        "sep_oct_point": {"type": "number"},
        "sep_oct_low80": {"type": "number"},
        "sep_oct_high80": {"type": "number"},
        "monthly": {"type": "object", "properties": {m: {"type": "number"} for m in MONTHS},
                    "required": MONTHS},
        "reason": {"type": "string"},
    },
    "required": ["knowledge", "sep_oct_point", "sep_oct_low80", "sep_oct_high80", "monthly", "reason"],
}


def build(cond):
    supply, know = CONDS[cond]
    text = (P / "common.md").read_text().replace("{price_csv}", (HERE / "inputs/price_to_202608.csv").read_text())
    if supply:
        text += (P / "supply.md").read_text().replace("{supply_table}", (HERE / "inputs/supply_202608.md").read_text())
    text += (P / ("with_knowledge.md" if know else "no_knowledge.md")).read_text()
    if not know:
        text += "knowledge には「使わない」と書いてください。\n"
    return text + (P / "ask.md").read_text()


def call(prompt):
    cmd = ["claude", "-p", "--model", MODEL, "--tools", "", "--strict-mcp-config", "--setting-sources", "",
           "--no-session-persistence", "--output-format", "json",
           "--system-prompt", (P / "system.md").read_text(), "--json-schema", json.dumps(SCHEMA, ensure_ascii=False)]
    with tempfile.TemporaryDirectory() as empty:
        r = subprocess.run(cmd + [prompt], capture_output=True, text=True, cwd=empty, timeout=600)
    out = json.loads(r.stdout)
    return out.get("structured_output") or json.loads(out["result"]), out.get("total_cost_usd")


def main():
    cond, n = sys.argv[1], int(sys.argv[2])
    d = HERE / "runs" / cond
    d.mkdir(parents=True, exist_ok=True)
    prompt = build(cond)
    (d / "prompt.txt").write_text(prompt)
    for i in range(n):
        f = d / f"{i}.json"
        if f.exists():
            continue
        ans, cost = call(prompt)
        f.write_text(json.dumps({"answer": ans, "cost_usd": cost, "model": MODEL}, ensure_ascii=False, indent=1))
        print(cond, i, ans["sep_oct_point"], ans["sep_oct_low80"], ans["sep_oct_high80"], cost, flush=True)


if __name__ == "__main__":
    main()
