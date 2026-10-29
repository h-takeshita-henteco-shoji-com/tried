"""市役所と議会のハーネスのサブエージェントの定義を作る(#100)。

雛形 code/ai-mayor/mayor/council-agents/*.md に、局の定義(bureaus/)、市長の定義(mayors/plan.md)、
市の計画(city-plan.md)を書き込み、.claude/agents/council-*.md に置く。作るのは11個。
設計は code/ai-mayor/mayor/council-design.md の6、受け渡しの形は council-interfaces.md の1。

    python3 code/ai-mayor/tools/make_council_agents.py          # 作る
    python3 code/ai-mayor/tools/make_council_agents.py --check  # 作り直しが要るかを確かめる
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAYOR = ROOT / "code/ai-mayor/mayor"
TEMPLATES = MAYOR / "council-agents"
BUREAUS = MAYOR / "bureaus"
AGENTS = ROOT / ".claude/agents"

# 案を出す7つの局。並びは council-interfaces.md の1のとおり
BUREAU_SLUGS = ["urban", "roads", "port", "economy", "health", "education", "fire", "finance"]

# モデルは定義ごとに固定する(council-design.md の6.4)。inherit だと親の会話のモデルで変わる
OPUS = "claude-opus-5-5"
SONNET = "claude-sonnet-5-5"

# 読むだけの道具(council-design.md の6.2)。list_* は展開して書く
READ_ONLY = [
    "city_info", "economy", "economy_breakdown", "services", "citizens_summary", "complaints",
    "citizen_voices", "events", "demand_breakdown", "cargo", "vehicles_stuck", "traffic", "trade", "building_stats",
    "land_value", "new_buildings", "zones_at", "zone_summary", "zone_map", "buildings_near", "net_near", "net_reach",
    "junction_info", "water_trace", "map_layer",
    "list_net_types", "list_building_types", "list_policies", "list_districts", "list_transport_lines", "transport_depots",
    "list_loans", "list_saves", "list_map_layers", "list_trees",
    "height_at", "latlon_to_game", "citizens_without_service", "sim_health", "preview_bulldoze",
    "transport_reach",
    # 試すだけの道具(#105)。街は変えない。ゲームの道具で、建てる前に赤く出るかを見るのと同じ
    "test_upgrade_road", "test_build_line", "test_place_building",
]

# 見てまとめる市長が足す道具(council-design.md の6.2)。街は動かさない
DESK_EXTRA = ["save_city", "set_time", "screenshot", "move_camera", "explain"]

MCP = "mcp__cities-skylines__"


def tools_line(file_tools, game_tools):
    return ", ".join(file_tools + [MCP + t for t in game_tools])


def field_tools():
    """実行する市長の道具。これまでの市長の雛形(agent-template.md)と同じ全部の道具にする。"""
    text = (MAYOR / "agent-template.md").read_text(encoding="utf-8")
    line = re.search(r"^tools:\s*(.+)$", text, re.M).group(1).strip()
    # 試すだけの道具も持たせる(#105)。打つ前に、同じ引数で試せるように
    tests = [MCP + t for t in ("test_upgrade_road", "test_build_line", "test_place_building") if MCP + t not in line]
    return ", ".join([line] + tests)


def load(path, shift=2):
    """front matter の name と、見出しを下げた本文を返す。"""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    front, body = m.group(1), m.group(2).strip()
    name = re.search(r"^name:\s*(.+)$", front, re.M).group(1).strip()
    body = re.sub(r"^(#+) ", lambda h: "#" * (len(h.group(1)) + shift) + " ", body, flags=re.M)
    return name, body


def render(template, values):
    text = (TEMPLATES / template).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{(\w+)\}\}", text)
    if left:
        raise SystemExit(f"{template} に埋めていない所がある: {', '.join(sorted(set(left)))}")
    return text


def definitions():
    """作る定義の一覧。(ファイル名, 中身)を返す。"""
    _, plan = load(MAYOR / "city-plan.md")
    _, cmap = load(MAYOR / "city-map.md")
    mayor_name, mayor = load(MAYOR / "mayors/plan.md")

    read_tools = tools_line(["Read", "Write"], READ_ONLY)
    desk_tools = tools_line(["Read", "Write", "Edit"], READ_ONLY + DESK_EXTRA)

    out = []
    for slug in BUREAU_SLUGS:
        name, bureau = load(BUREAUS / f"{slug}.md")
        out.append((f"council-{slug}.md", render("bureau.md", {
            "slug": slug, "name": name, "tools": read_tools, "bureau": bureau, "plan": plan, "map": cmap,
        })))

    out.append(("council-assembly.md", render("assembly.md", {
        "tools": read_tools, "plan": plan,
    })))

    out.append(("council-mayor-desk.md", render("mayor-desk.md", {
        "name": mayor_name, "tools": desk_tools, "mayor": mayor, "plan": plan, "map": cmap,
    })))

    out.append(("council-mayor-field.md", render("mayor-field.md", {
        "name": mayor_name, "tools": field_tools(), "mayor": mayor, "plan": plan,
    })))
    return out


def main():
    check = "--check" in sys.argv
    made = definitions()
    stale = []
    for filename, text in made:
        path = AGENTS / filename
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(filename)
        else:
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    if check:
        if stale:
            print("作り直しが要る: " + ", ".join(stale))
            sys.exit(1)
        print(f"{len(made)}個とも最新")


if __name__ == "__main__":
    main()
