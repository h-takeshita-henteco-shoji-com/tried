"""e-Stat「青果物卸売市場調査」の福岡市中央卸売市場の野菜の月別表から、品目別・月別の数量と価格を作る(#184)。

使い方: .venv/bin/python estat_fukuoka_parse.py
入力: data/raw_estat_fukuoka/<年>.xls(x)(URL は data/estat_fukuoka_ids.txt)。出力: data/fukuoka_monthly.csv(数量t、価格円/kg)
"""
import re
import unicodedata
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).parent
RAW = HERE / "data/raw_estat_fukuoka"


def norm(x):
    return re.sub(r"\s", "", unicodedata.normalize("NFKC", str(x))) if pd.notna(x) else ""


def parse(path):
    y = int(path.stem)
    d = pd.read_excel(path, header=None, engine="calamine")
    head = next(i for i in range(30) if norm(d.iat[i, 0]) == "品目")
    sub = next(i for i in range(head, head + 8) if any(norm(v) == "数量" for v in d.iloc[i]))
    labels = {c: norm(d.iat[head, c]) for c in d.columns}
    months = {c: int(m.group(1)) for c, t in labels.items() if (m := re.fullmatch(r"(\d+)月?", t)) and 1 <= int(m.group(1)) <= 12}
    subs = {c: norm(d.iat[sub, c]) for c in d.columns}
    cols = {}
    for c, m in months.items():
        price = next(k for k in range(c + 1, c + 4) if subs.get(k) == "価格")
        cols[m] = (c, price)
    first = min(months)
    recs = []
    for i in range(sub + 1, len(d)):
        name = "".join(norm(d.iat[i, c]) for c in range(0, 4) if not re.fullmatch(r"[\d.]+", norm(d.iat[i, c])))
        if not name or name.endswith("類") and pd.isna(pd.to_numeric(d.iat[i, first], errors="coerce")):
            continue
        for m, (cq, cp) in cols.items():
            q, p = pd.to_numeric(d.iat[i, cq], errors="coerce"), pd.to_numeric(d.iat[i, cp], errors="coerce")
            if pd.notna(q) and pd.notna(p):
                recs.append({"年": y, "月": m, "品目": name, "数量t": q, "価格": p})
    return recs


def main():
    recs = []
    for p in sorted(RAW.glob("*.xls*")):
        r = parse(p)
        recs += r
        print(p.name, len(r), len({x["品目"] for x in r}))
    df = pd.DataFrame(recs)
    df.to_csv(HERE / "data/fukuoka_monthly.csv", index=False)
    cnt = df.groupby("品目").size()
    print(df.shape, "192か月そろう品目:", (cnt == 192).sum())
    print(cnt.sort_values(ascending=False).head(60).to_string())


if __name__ == "__main__":
    main()
