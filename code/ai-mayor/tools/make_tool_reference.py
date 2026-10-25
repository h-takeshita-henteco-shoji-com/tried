"""街を作る・変える道具の説明と引数を、局が読める1枚にまとめる(#105 の作り直し)。

局と、見てまとめる市長は、見る道具だけを持つ。街を変える道具の引数を確かめられず、建設の案が
「実行可」にならなかった(#105 の1回目)。そこで、道具の説明と引数の一覧を文書にして渡す。
道具そのものは渡さない(局は街を変えない)。

使い方:
  python3 code/ai-mayor/tools/make_tool_reference.py
書くファイル: code/ai-mayor/mayor/tool-reference.md
"""
import ast
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER = os.path.join(ROOT, "mcp", "server.py")
OUT = os.path.join(ROOT, "mayor", "tool-reference.md")

# 実行する市長が持つ、街を変える道具(.claude/agents/council-mayor-field.md の道具のうち、見る道具でないもの)
GROUPS = [
    ("道路・線・路線", ["build_line", "remove_line", "upgrade_road", "reverse_road", "create_transport_line",
                    "remove_transport_line", "set_transport_line_budget", "set_traffic_lights", "set_yield_sign"]),
    ("建物", ["place_building", "relocate_building", "bulldoze", "set_building_active", "empty_building", "set_historical"]),
    ("区画と地区", ["zone_area", "zone_rect", "zone_polygon", "paint_district", "set_district_policy", "rename_district"]),
    ("税・予算・政策・融資", ["set_tax", "set_budget", "set_policy", "take_loan", "repay_loan"]),
    ("木と地形", ["plant_trees", "remove_trees", "level_terrain", "raise_terrain", "lower_terrain", "terrain_dirt"]),
]


def main() -> None:
    tree = ast.parse(open(SERVER, encoding="utf-8").read())
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    lines = [
        "# 街を作る・変える道具の説明と引数",
        "",
        "<!-- code/ai-mayor/tools/make_tool_reference.py が mcp/server.py から作る。手で編集しない -->",
        "",
        "局と見てまとめる市長は、これらの道具を持っていません。案の実行計画に、使う道具の名前と引数の値を書くために読みます。",
        "道具を呼べるのは、実行する市長だけです。",
        "",
    ]
    for title, names in GROUPS:
        lines += [f"## {title}", ""]
        for name in names:
            f = funcs.get(name)
            if f is None:
                continue
            args = []
            defaults = [None] * (len(f.args.args) - len(f.args.defaults)) + list(f.args.defaults)
            for a, d in zip(f.args.args, defaults):
                ann = ast.unparse(a.annotation) if a.annotation else ""
                s = f"{a.arg}: {ann}" if ann else a.arg
                if d is not None:
                    s += f" = {ast.unparse(d)}"
                args.append(s)
            doc = (ast.get_docstring(f) or "").strip()
            lines += [f"### `{name}({', '.join(args)})`", "", doc, ""]
    open(OUT, "w", encoding="utf-8").write("\n".join(lines).rstrip() + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
