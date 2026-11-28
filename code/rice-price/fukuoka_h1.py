"""#186 V6 の準備: 各月末までの価格から翌月を当てる(福岡12品目、#184 と同じ5つのモデルと2つの素朴な予想)。

予測の月: 2016年1月〜2026年10月。品目ごとに forecast/h1/<品目>.csv に書き、途中から再開できる。
使い方: HF_HUB_OFFLINE=1 .venv/bin/python fukuoka_h1.py
"""
import warnings
from pathlib import Path
import pandas as pd
import veg_models as vm
from fukuoka_models import ITEMS, series
warnings.filterwarnings("ignore")
HERE = Path(__file__).parent
OUT = HERE / "forecast/h1"; OUT.mkdir(exist_ok=True)


def main():
    df = series()
    targets = pd.date_range("2016-01-01", "2026-10-01", freq="MS")
    for it in ITEMS:
        f = OUT / f"{it}.csv"
        if f.exists():
            continue
        s = df[it]; rows = []
        for t in targets:
            hist = s.loc[:t - pd.offsets.MonthBegin()]; y, idx = hist.values, hist.index
            p = {"前の月のまま": y[-1], "前の年の同じ月": float(s.loc[t - pd.DateOffset(years=1)]),
                 "SARIMA": vm.sarima(y)[0], "指数平滑法": vm.ets(y)[0], "Prophet(Meta)": vm.prophet(y, idx)[0],
                 "TimesFM(Google)": vm.timesfm(y)[0], "Chronos(Amazon)": vm.chronos(y)[0]}
            rows += [{"年": t.year, "月": t.month, "品目": it, "モデル": k, "予測": round(float(v), 1), "実績": float(s.loc[t])} for k, v in p.items()]
        pd.DataFrame(rows).to_csv(f, index=False)
        print(it, flush=True)


if __name__ == "__main__":
    main()
