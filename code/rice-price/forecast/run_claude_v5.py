"""#186 V5: #184 の「Claude 知識なし」(fukuoka_a)に、入荷量と天候の表を足す(福岡12品目、2026年7〜9月)。

使い方: ../.venv/bin/python run_claude_v5.py <回数>
"""
import json
import sys
from pathlib import Path

import run_claude as rc
import run_claude_fukuoka as f

HERE = Path(__file__).parent
EXTRA = """
次の表は、同じ市場の同じ12品目の、月ごとの入荷量(トン)です。出どころと作り方は、価格の表と同じです。

{vol}
次の表は、気象庁の観測による、主な産地に近い7地点の月ごとの天候です。降水量は月の合計(mm)、気温は月の平均(℃)、日照は月の合計(時間)です。
品目と地点の対応の目安: キャベツ・はくさい・レタス=軽井沢、こまつな・なす=福岡、トマト=熊本、きゅうり=佐賀、ブロッコリー・にんじん・ばれいしょ=帯広、たまねぎ=網走、ねぎ=大分。

{wx}
"""


def build():
    return (f.HEAD.replace("{csv}", (HERE / "inputs/fukuoka_to_202606.csv").read_text())
            + EXTRA.replace("{vol}", (HERE / "inputs/fukuoka_volume_to_202606.csv").read_text())
                   .replace("{wx}", (HERE / "inputs/weather_to_202606.csv").read_text())
            + f.NO.replace("上の表", "上の3つの表") + f.ASK)


def main():
    n = int(sys.argv[1])
    prompt = build()
    d = HERE / "runs" / "v5"
    d.mkdir(parents=True, exist_ok=True)
    (d / "prompt.txt").write_text(prompt)
    rc.SCHEMA = f.SCHEMA
    for i in range(n):
        p = d / f"{i}.json"
        if p.exists():
            continue
        ans, cost = rc.call(prompt)
        p.write_text(json.dumps({"answer": ans, "cost_usd": cost, "model": rc.MODEL}, ensure_ascii=False, indent=1))
        print("v5", i, cost, flush=True)


if __name__ == "__main__":
    main()
