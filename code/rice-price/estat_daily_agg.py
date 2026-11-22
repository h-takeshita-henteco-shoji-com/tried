"""e-Stat「青果物卸売市場調査(日別調査)」の福岡市の野菜(CSV)を、月ごとの数量と加重平均価格にまとめる(#184)。

使い方: .venv/bin/python estat_daily_agg.py
入力: data/raw_estat_daily/2026-MM-DD.csv(statInfId は data/estat_daily_ids.json)。出力: data/fukuoka_daily_monthly.csv
価格は、その月の日ごとの価格を数量で重み付けした平均(円/kg)。数量は t に直す。
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent


def main():
    fs = sorted((HERE / "data/raw_estat_daily").glob("*.csv"))
    d = pd.concat([pd.read_csv(f, encoding="cp932", dtype={"産地コード": str}) for f in fs])
    d = d[d["産地名"].isna()].copy()  # 品目の合計の行だけ
    for c in ("数量", "価格"):
        d[c] = pd.to_numeric(d[c].astype(str).str.replace(",", ""), errors="coerce")
    d["金額"] = d["数量"] * d["価格"]
    g = d.groupby(["年", "月", "品目名"]).agg(数量=("数量", "sum"), 金額=("金額", "sum"), 日数=("日", "nunique")).reset_index()
    g["価格"] = (g["金額"] / g["数量"]).round(0)
    g["数量t"] = (g["数量"] / 1000).round(0)
    g.rename(columns={"品目名": "品目"})[["年", "月", "品目", "数量t", "価格", "日数"]].to_csv(HERE / "data/fukuoka_daily_monthly.csv", index=False)
    print(len(fs), "日分", g.shape)


if __name__ == "__main__":
    main()
