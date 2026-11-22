"""農水省「米の相対取引価格」の年産別・月別一覧から、月ごとの価格の表を作る(#184)。

使い方: .venv/bin/python fetch_parse.py
入力: data/raw/<年産>.xls(x)(https://www.maff.go.jp/j/seisan/keikaku/soukatu/kakaku.html の
      「相対取引価格(速報)(9月～8月)」)。出力: data/monthly.csv(円/玄米60kg、消費税相当額を含む)。
"""
import re
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")
RAW = Path(__file__).parent / "data" / "raw"
# 年産 → 西暦。年産の価格は、その年の9月から翌年8月まで
ERA = {"H": 1988, "R": 2018}
TARGETS = {"全銘柄平均価格": "all", ("福岡", "ヒノヒカリ"): "fukuoka_hinohikari",
           ("福岡", "夢つくし"): "fukuoka_yumetsukushi", ("福岡", "元気つくし"): "fukuoka_genkitsukushi",
           ("新潟", "コシヒカリ"): "niigata_koshihikari"}


def parse(path):
    year = ERA[path.stem[0]] + int(path.stem[1:3])
    d = pd.read_excel(path, header=None)
    head = next(i for i in range(15) if d.iloc[i].astype(str).str.contains("品種銘柄").any())
    # 月の列は、見出しに「月」を含む列(12列)
    cols = [c for c in d.columns if re.search(r"\d+月", str(d.iloc[head, c]))]
    assert len(cols) == 12, (path, len(cols))
    months = pd.date_range(f"{year}-09-01", periods=12, freq="MS")
    rows = []
    for _, r in d.iloc[head + 1:].iterrows():
        a, b = str(r[1]).strip(), str(r[2]).strip()
        key = "全銘柄平均価格" if a.startswith("全銘柄平均") else (a, b)
        if key in TARGETS:
            for m, c in zip(months, cols):
                v = pd.to_numeric(r[c], errors="coerce")
                rows.append({"month": m, "series": TARGETS[key], "price": v, "crop_year": year})
    return rows


def main():
    rows = []
    for p in sorted(RAW.glob("*.xls*")):
        if p.stem.endswith("a"):  # 年産平均だけの表は使わない
            continue
        rows += parse(p)
    df = pd.DataFrame(rows).dropna(subset=["price"])
    wide = df.pivot_table(index="month", columns="series", values="price").sort_index()
    out = RAW.parent / "monthly.csv"
    wide.round(0).to_csv(out)
    print(out, wide.shape, wide.index.min().date(), wide.index.max().date())
    print(wide.notna().sum())


if __name__ == "__main__":
    main()
