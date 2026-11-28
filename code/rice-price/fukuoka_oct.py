"""#186: 9月末までの価格から10月を当てる(福岡12品目、#184 と同じ5つのモデル、2016〜2026年)。

使い方: HF_HUB_OFFLINE=1 .venv/bin/python fukuoka_oct.py [年 ...]   出力: forecast/fukuoka_oct.csv
"""
import warnings
from pathlib import Path
import numpy as np, pandas as pd
import veg_models as vm
from fukuoka_models import ITEMS, series
warnings.filterwarnings("ignore")
HERE = Path(__file__).parent


def run(s, year):
    hist = s.loc[:f"{year}-09-01"]; y, idx = hist.values, hist.index
    act = float(s.loc[f"{year}-10-01"])
    preds = {"前の月のまま": y[-1], "前の年の同じ月": float(s.loc[f"{year - 1}-10-01"]),
             "SARIMA": vm.sarima(y)[0], "指数平滑法": vm.ets(y)[0], "Prophet(Meta)": vm.prophet(y, idx)[0],
             "TimesFM(Google)": vm.timesfm(y)[0], "Chronos(Amazon)": vm.chronos(y)[0]}
    return [{"年": year, "月": 10, "モデル": k, "予測": float(p), "実績": act} for k, p in preds.items()]


def main():
    import sys
    df = series()
    years = [int(a) for a in sys.argv[1:]] or list(range(2016, 2027))
    out = HERE / "forecast/fukuoka_oct.csv"
    old = pd.read_csv(out) if out.exists() else pd.DataFrame(columns=["年"])
    old = old[~old["年"].isin(years)]
    assert df.loc[:f"{max(years)}-10-01"].notna().all().all(), df.isna().sum()
    rows = []
    for it in ITEMS:
        for year in years:
            rows += [dict(r, 品目=it) for r in run(df[it], year)]
        print(it, flush=True)
    r = pd.DataFrame(rows); r["誤差%"] = (r["予測"] / r["実績"] - 1) * 100
    pd.concat([old, r.round(1)]).sort_values(["品目", "年"]).to_csv(out, index=False)


if __name__ == "__main__":
    main()
