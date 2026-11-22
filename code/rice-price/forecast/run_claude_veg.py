"""Claude に野菜(キャベツ・たまねぎ)の2026年7〜9月の価格を予測させる(#184、事前登録3)。

使い方: ../.venv/bin/python run_claude_veg.py <a|b|c|d> <回数>
  a: 入荷量+値段・知識なし  b: 入荷量+値段・知識あり  c: 値段だけ・知識なし  d: 値段だけ・知識あり(事前登録5)
"""
import json
import sys
from pathlib import Path

import run_claude as rc

HERE = Path(__file__).parent
KEYS = [f"{i}_{m}" for i in ("cabbage", "onion") for m in ("2026-07", "2026-08", "2026-09")]
SCHEMA = {"type": "object", "properties": {"knowledge": {"type": "string"}, "reason": {"type": "string"},
          **{k: {"type": "number"} for k in KEYS}}, "required": ["knowledge", "reason", *KEYS]}
HEAD = """今日は2026年6月30日です。

次の表は、東京都中央卸売市場(全市場の合計)のキャベツとたまねぎの、月ごとの入荷量(トン)と卸売価格(円/kg、消費税を含む。金額÷数量)です。

{csv}
"""
NO = "\n予測には、上の表から読み取れることだけを使ってください。2026年の野菜の作柄・天候・価格について、あなたが知っている出来事やニュースは使わないでください。knowledge には「使わない」と書いてください。\n"
YES = "\n予測には、上の表に加えて、2026年6月30日までに起きた出来事やニュースのうち、あなたが知っているものを使ってかまいません。予測の前に、2026年の野菜の作柄・天候・価格について知っていることを knowledge に書いてください。知らないことは知らないと書いてください。\n"
ASK = """
問い: 2026年7月・8月・9月の、キャベツとたまねぎの月ごとの卸売価格(円/kg)を予測してください。
キーは cabbage_2026-07 のように「品目_年月」とします。理由を reason に、根拠にしたデータや事実を挙げて書いてください。
"""


def main():
    cond, n = sys.argv[1], int(sys.argv[2])
    price_only = cond in ("c", "d")
    head = HEAD.replace("入荷量(トン)と卸売価格", "卸売価格") if price_only else HEAD
    src = "inputs/veg_price_to_202606.csv" if price_only else "inputs/veg_to_202606.csv"
    prompt = head.replace("{csv}", (HERE / src).read_text()) + (NO if cond in ("a", "c") else YES) + ASK
    d = HERE / "runs" / f"veg_{cond}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "prompt.txt").write_text(prompt)
    rc.SCHEMA = SCHEMA
    for i in range(n):
        f = d / f"{i}.json"
        if f.exists():
            continue
        ans, cost = rc.call(prompt)
        f.write_text(json.dumps({"answer": ans, "cost_usd": cost, "model": rc.MODEL}, ensure_ascii=False, indent=1))
        print(cond, i, [round(ans[k]) for k in KEYS], cost, flush=True)


if __name__ == "__main__":
    main()
