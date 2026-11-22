"""福岡市中央卸売市場の野菜12品目で、6月までの価格から7〜9月を当てる(#184、事前登録4)。

使い方: .venv/bin/python fukuoka_models.py
出力: forecast/fukuoka_models.csv、forecast/inputs/fukuoka_to_202606.csv(Claude に渡す表)
"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

import veg_models as vm

warnings.filterwarnings("ignore")
HERE = Path(__file__).parent
ITEMS = ["キャベツ", "はくさい", "レタス", "こまつな", "トマト", "きゅうり", "なす", "ブロッコリー", "にんじん", "ばれいしょ", "たまねぎ", "ねぎ"]


def series():
    m = pd.read_csv(HERE / "data/fukuoka_monthly.csv")
    d = pd.read_csv(HERE / "data/fukuoka_daily_monthly.csv")
    out = {}
    for it in ITEMS:
        a = pd.concat([m[m["品目"] == it], d[d["品目"] == it]])
        idx = pd.to_datetime(dict(year=a["年"], month=a["月"], day=1))
        out[it] = pd.Series(a["価格"].values.astype(float), index=idx).sort_index()
    return pd.DataFrame(out)


def run(s, year, heavy):
    hist = s.loc[:f"{year}-06-01"]
    y, idx = hist.values, hist.index
    act = s.loc[f"{year}-07-01":f"{year}-09-01"].values
    preds = {"前の月のまま": np.repeat(y[-1], 3), "前の年の同じ月": s.loc[f"{year - 1}-07-01":f"{year - 1}-09-01"].values,
             "SARIMA": vm.sarima(y), "指数平滑法": vm.ets(y)}
    if heavy:
        preds.update({"Prophet(Meta)": vm.prophet(y, idx), "TimesFM(Google)": vm.timesfm(y), "Chronos(Amazon)": vm.chronos(y)})
    return [{"年": year, "月": 7 + i, "モデル": k, "予測": float(p[i]), "実績": float(act[i])} for k, p in preds.items() for i in range(3)]


def main():
    df = series()
    assert df.loc[:"2026-09-01"].notna().all().all(), df.isna().sum()
    t = df.loc[:"2026-06-01"].copy()
    t.insert(0, "年月", t.index.strftime("%Y-%m"))
    t.round(0).astype({c: int for c in ITEMS}).to_csv(HERE / "forecast/inputs/fukuoka_to_202606.csv", index=False)
    rows = []
    for it in ITEMS:
        for year in range(2016, 2027):
            rows += [dict(r, 品目=it) for r in run(df[it], year, heavy=True)]
        print(it, flush=True)
    r = pd.DataFrame(rows)
    r["誤差%"] = (r["予測"] / r["実績"] - 1) * 100
    r.round(1).to_csv(HERE / "forecast/fukuoka_models.csv", index=False)
    a = r.assign(a=r["誤差%"].abs())
    tab = a.groupby(["モデル", a["年"] == 2026])["a"].mean().unstack().round(1)
    tab.columns = ["過去10年(2016〜2025)", "2026年(試験F)"]
    print(tab.sort_values("過去10年(2016〜2025)").to_string())


if __name__ == "__main__":
    main()
