"""Claude に福岡市中央卸売市場の野菜12品目の2026年7〜9月の価格を予測させる(#184、事前登録4)。

使い方: ../.venv/bin/python run_claude_fukuoka.py <a|b> <回数>   a: 知識を使わせない  b: 知識を使ってよい
"""
import json
import sys
from pathlib import Path

import run_claude as rc

HERE = Path(__file__).parent
ITEMS = ["キャベツ", "はくさい", "レタス", "こまつな", "トマト", "きゅうり", "なす", "ブロッコリー", "にんじん", "ばれいしょ", "たまねぎ", "ねぎ"]
CODE = dict(zip(ITEMS, ["cabbage", "hakusai", "lettuce", "komatsuna", "tomato", "cucumber", "eggplant", "broccoli",
                        "carrot", "potato", "onion", "negi"]))
KEYS = [f"{CODE[i]}_2026-0{m}" for i in ITEMS for m in (7, 8, 9)]
SCHEMA = {"type": "object", "properties": {"knowledge": {"type": "string"}, "reason": {"type": "string"},
          **{k: {"type": "number"} for k in KEYS}}, "required": ["knowledge", "reason", *KEYS]}
HEAD = """今日は2026年6月30日です。

次の表は、福岡市中央卸売市場の野菜12品目の、月ごとの卸売価格(円/kg)です。
2010年1月〜2025年12月は農林水産省「青果物卸売市場調査」の月別の確報、2026年1〜6月は同じ調査の日別の速報を月ごとに平均した値です。

{csv}
"""
NO = "\n予測には、上の表から読み取れることだけを使ってください。2026年の野菜の作柄・天候・価格について、あなたが知っている出来事やニュースは使わないでください。knowledge には「使わない」と書いてください。\n"
YES = "\n予測には、上の表に加えて、2026年6月30日までに起きた出来事やニュースのうち、あなたが知っているものを使ってかまいません。予測の前に、2026年の野菜の作柄・天候・価格について知っていることを knowledge に書いてください。知らないことは知らないと書いてください。\n"
ASK = ("\n問い: 2026年7月・8月・9月の、12品目それぞれの月ごとの卸売価格(円/kg)を予測してください。\n"
       "キーは cabbage_2026-07 のように「品目のコード_年月」とします。品目のコード: "
       + "、".join(f"{k}={v}" for k, v in CODE.items())
       + "。\n理由を reason に、品目ごとに短く書いてください。\n")



def main():
    cond, n = sys.argv[1], int(sys.argv[2])
    prompt = HEAD.replace("{csv}", (HERE / "inputs/fukuoka_to_202606.csv").read_text()) + (NO if cond == "a" else YES) + ASK
    d = HERE / "runs" / f"fukuoka_{cond}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "prompt.txt").write_text(prompt)
    rc.SCHEMA = SCHEMA
    for i in range(n):
        f = d / f"{i}.json"
        if f.exists():
            continue
        ans, cost = rc.call(prompt)
        f.write_text(json.dumps({"answer": ans, "cost_usd": cost, "model": rc.MODEL}, ensure_ascii=False, indent=1))
        print(cond, i, cost, flush=True)


if __name__ == "__main__":
    main()
