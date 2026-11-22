"""東京都中央卸売市場の市場統計情報明細データから、野菜の月ごとの数量と価格を作る(#184)。

使い方: .venv/bin/python veg_parse.py
入力: data/raw_veg/(https://www.shijou.metro.tokyo.lg.jp/torihiki/geppo の「市場統計情報明細データ」。
      2002〜2025年は年ごとのファイル、2026年は月ごとのファイル。大きいのでリポジトリには入れず、URL を data/veg_urls.txt に残す)
出力: data/veg_monthly.csv。全市場の合計の数量(kg)と、金額÷数量の価格(円/kg、消費税を含む)。
"""
import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
RAW = HERE / "data/raw_veg"
ITEMS = {"キャベツ": "cabbage", "たまねぎ": "onion"}


def files():
    for p in sorted(RAW.glob("*.xlsx")):
        m = re.match(r"y(\d{4})(\d{2})?meisai", p.name)
        y, mo = int(m.group(1)), m.group(2)
        if y <= 2025 and mo is None:      # 年ごとのファイル
            yield p
        elif y == 2026 and mo is not None:  # 2026年は月ごと
            yield p


def main():
    parts = []
    for p in files():
        for _, d in pd.read_excel(p, sheet_name=None, engine="calamine").items():
            d.columns = [str(c).strip() for c in d.columns]
            name = d["品目名称"].astype(str).str.replace(r"\s", "", regex=True)
            d = d[name.isin(ITEMS)].assign(item=name[name.isin(ITEMS)].map(ITEMS))
            parts.append(d[["年", "月", "item", "産地", "数量(kg)", "金額(円)"]])
        print(p.name, flush=True)
    df = pd.concat(parts)
    df["month"] = pd.to_datetime(dict(year=df["年"], month=df["月"], day=1))
    g = df.groupby(["month", "item"])[["数量(kg)", "金額(円)"]].sum()
    g["price"] = g["金額(円)"] / g["数量(kg)"]
    wide = g.unstack("item")
    out = pd.DataFrame({f"{it}_{k}": wide[(col, it)] for it in ITEMS.values()
                        for k, col in (("kg", "数量(kg)"), ("price", "price"))})
    out.round(1).to_csv(HERE / "data/veg_monthly.csv")
    # 産地の内訳(品目・年・出荷地ごとの数量)も残す
    df.groupby(["item", "年", "産地"])["数量(kg)"].sum().to_csv(HERE / "data/veg_origin_yearly.csv")
    print(out.shape, out.index.min().date(), out.index.max().date())


if __name__ == "__main__":
    main()
