"""野菜(キャベツ・たまねぎ)の価格を、6月までのデータで7〜9月を当てる(#184、事前登録3)。

使い方: .venv/bin/python veg_models.py [--fast]   (--fast は TimesFM・Chronos・Prophet を過去の試験から外す)
出力: forecast/veg_models.csv(年・品目・モデルごとの予測と実績)
"""
import itertools
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
import logging
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
logging.getLogger("prophet").setLevel(logging.WARNING)

HERE = Path(__file__).parent
V = pd.read_csv(HERE / "data/veg_monthly.csv", index_col=0, parse_dates=True)
H = 3
_tfm = _chr = None


def sarima(y):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    best = None
    for p, q, P, Q in itertools.product([0, 1], [0, 1], [0, 1], [0, 1]):
        try:
            r = SARIMAX(np.log(y), order=(p, 1, q), seasonal_order=(P, 1, Q, 12)).fit(disp=False)
        except Exception:
            continue
        if best is None or r.aic < best[0]:
            best = (r.aic, r)
    return np.exp(best[1].forecast(H))


def ets(y):
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    return ExponentialSmoothing(y, trend="add", damped_trend=True, seasonal="mul", seasonal_periods=12).fit().forecast(H)


def prophet(y, idx):
    from prophet import Prophet
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(pd.DataFrame({"ds": idx, "y": y}))
    fut = pd.date_range(idx[-1] + pd.offsets.MonthBegin(), periods=H, freq="MS")
    return m.predict(pd.DataFrame({"ds": fut}))["yhat"].values


def timesfm(y):
    global _tfm
    import timesfm as tf
    if _tfm is None:
        _tfm = tf.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
        _tfm.compile(tf.ForecastConfig(max_context=1024, max_horizon=256, normalize_inputs=True,
                                       use_continuous_quantile_head=True, fix_quantile_crossing=True))
    point, _ = _tfm.forecast(horizon=H, inputs=[y])
    return np.asarray(point[0])


def chronos(y):
    global _chr
    import torch
    from chronos import BaseChronosPipeline
    if _chr is None:
        _chr = BaseChronosPipeline.from_pretrained("amazon/chronos-bolt-base", device_map="cpu", torch_dtype=torch.float32)
    q, _ = _chr.predict_quantiles(torch.tensor(y), prediction_length=H, quantile_levels=[0.5])
    return q[0, :, 0].numpy()


def run(item, year, heavy=True):
    s = V[f"{item}_price"]
    hist = s.loc[:f"{year}-06-01"]
    y, idx = hist.values.astype(float), hist.index
    act = s.loc[f"{year}-07-01":f"{year}-09-01"].values
    preds = {"前の月のまま": np.repeat(y[-1], H), "前の年の同じ月": s.loc[f"{year - 1}-07-01":f"{year - 1}-09-01"].values,
             "SARIMA": sarima(y), "指数平滑法": ets(y)}
    if heavy:
        preds.update({"Prophet(Meta)": prophet(y, idx), "TimesFM(Google)": timesfm(y), "Chronos(Amazon)": chronos(y)})
    rows = []
    for k, p in preds.items():
        for i, m in enumerate([7, 8, 9]):
            rows.append({"品目": item, "年": year, "月": m, "モデル": k, "予測": float(p[i]),
                         "実績": float(act[i]) if i < len(act) else np.nan})
    return rows


def main():
    fast = "--fast" in sys.argv
    rows = []
    for item in ["cabbage", "onion"]:
        for year in range(2016, 2027):
            rows += run(item, year, heavy=(year == 2026 or not fast))
            print(item, year, flush=True)
    df = pd.DataFrame(rows)
    df["誤差%"] = (df["予測"] / df["実績"] - 1) * 100
    df.round(1).to_csv(HERE / "forecast/veg_models.csv", index=False)
    mape = df.assign(a=df["誤差%"].abs()).groupby(["品目", "モデル", df["年"] == 2026])["a"].mean().unstack().round(1)
    mape.columns = ["過去10年(2016〜2025)", "2026年(試験V)"]
    print(mape.to_string())


if __name__ == "__main__":
    main()
