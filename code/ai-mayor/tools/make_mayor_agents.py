"""市長ごとのサブエージェントの定義を作る(#92)。

雛形 code/ai-mayor/mayor/agent-template.md に、市長の定義 code/ai-mayor/mayor/mayors/<slug>.md を
書き込み、.claude/agents/ai-mayor-<slug>.md に置く。市長ごとに違うのは「市長の定義」の節だけになる。

    python3 code/ai-mayor/tools/make_mayor_agents.py          # 作る
    python3 code/ai-mayor/tools/make_mayor_agents.py --check  # 作り直しが要るかを確かめる
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = ROOT / "code/ai-mayor/mayor/agent-template.md"
MAYORS = ROOT / "code/ai-mayor/mayor/mayors"
AGENTS = ROOT / ".claude/agents"

SLUGS = ["base", "money", "population", "livable"]
# 4人で同じモデルに固定する。inherit にすると、親の会話のモデルで変わるため
MODEL = "claude-opus-5-5"


def load_mayor(slug):
    text = (MAYORS / f"{slug}.md").read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    front, body = m.group(1), m.group(2).strip()
    name = re.search(r"^name:\s*(.+)$", front, re.M).group(1).strip()
    # 雛形の「## 市長の定義」の下に入るよう、見出しを2段下げる
    body = re.sub(r"^(#+) ", lambda h: "#" * (len(h.group(1)) + 2) + " ", body, flags=re.M)
    return name, body


def render(slug):
    name, body = load_mayor(slug)
    text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in {"slug": slug, "name": name, "model": MODEL, "mayor": body}.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main():
    check = "--check" in sys.argv
    stale = []
    for slug in SLUGS:
        path = AGENTS / f"ai-mayor-{slug}.md"
        text = render(slug)
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(path.name)
        else:
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    if check:
        print("作り直しが要る: " + ", ".join(stale) if stale else "4つとも最新")
        sys.exit(1 if stale else 0)


if __name__ == "__main__":
    main()
