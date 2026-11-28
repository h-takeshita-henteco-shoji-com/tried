"""#186 V7: Claude に農水省「野菜の生育状況及び価格見通し(令和8年7月)」(2026-06-30公表)の文章を渡す。

v7: V5(価格・入荷量・天候の表)に見通しを足す。v7n: #184 の知識なし(価格の表だけ)に見通しを足す。
使い方: ../.venv/bin/python run_claude_v7.py <v7|v7n> <回数>
"""
import json
import sys
from pathlib import Path

import run_claude as rc
import run_claude_fukuoka as f
import run_claude_v5 as v5

HERE = Path(__file__).parent
OUT = """
次の文章は、農林水産省が2026年6月30日に公表した「野菜の生育状況及び価格見通し(令和8年7月)」の、品目ごとの部分です。東京都中央卸売市場に出荷される野菜について、主産地や卸売会社から聞き取った見通しです。PDF から文字を取り出したもので、表の並びが崩れているところがあります。福岡市の市場の見通しではないことに注意してください。

{txt}
"""


def build(cond):
    txt = OUT.replace("{txt}", (HERE / "inputs/maff_outlook_202607.txt").read_text())
    if cond == "v7":
        base = v5.build()
        cut = base.index(f.NO.replace("上の表", "上の3つの表"))
        return base[:cut] + txt + f.NO.replace("上の表", "上の3つの表と見通しの文章") + f.ASK
    base = f.HEAD.replace("{csv}", (HERE / "inputs/fukuoka_to_202606.csv").read_text())
    return base + txt + f.NO.replace("上の表", "上の表と見通しの文章") + f.ASK


def main():
    cond, n = sys.argv[1], int(sys.argv[2])
    prompt = build(cond)
    d = HERE / "runs" / cond
    d.mkdir(parents=True, exist_ok=True)
    (d / "prompt.txt").write_text(prompt)
    rc.SCHEMA = f.SCHEMA
    for i in range(n):
        p = d / f"{i}.json"
        if p.exists():
            continue
        ans, cost = rc.call(prompt)
        p.write_text(json.dumps({"answer": ans, "cost_usd": cost, "model": rc.MODEL}, ensure_ascii=False, indent=1))
        print(cond, i, cost, flush=True)


if __name__ == "__main__":
    main()
