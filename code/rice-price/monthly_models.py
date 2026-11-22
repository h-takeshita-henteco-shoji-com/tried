"""月ごとの時系列モデルで米価を予測する(#184、事前登録2)。

使い方: .venv/bin/python monthly_models.py [モデル名 ...]   (省略時は全部)
入力: forecast/inputs/price_to_202608.csv の2010年9月以降。出力: forecast/monthly_models.csv(2026年9月〜2027年8月)。
"""
import itertools
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).parent
OUT = HERE / "forecast/monthly_models.csv"
H = 12

df = pd.read_csv(HERE / "forecast/inputs/price_to_202608.csv")
y = pd.Series(df.iloc[:, 1].values, index=pd.PeriodIndex(df.iloc[:, 0], freq="M")).loc["2010-09":].astype(float)
assert len(y) == 192 and y.index.is_monotonic_increasing
future = pd.period_range("2026-09", periods=H, freq="M")


def sarima():
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    best = None
    for p, q, P, Q, D in itertools.product([0, 1, 2], [0, 1, 2], [0, 1], [0, 1], [0, 1]):
        try:
            r = SARIMAX(np.log(y.values), order=(p, 1, q), seasonal_order=(P, D, Q, 12)).fit(disp=False)
        except Exception:
            continue
        if best is None or r.aic < best[0]:
            best = (r.aic, (p, 1, q, P, D, Q), r)
    print("SARIMA 次数", best[1])
    return np.exp(best[2].forecast(H))


def ets():
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    r = ExponentialSmoothing(y.values, trend="add", damped_trend=True, seasonal="mul", seasonal_periods=12).fit()
    return r.forecast(H)


def prophet():
    from prophet import Prophet
    d = pd.DataFrame({"ds": y.index.to_timestamp(), "y": y.values})
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False).fit(d)
    f = m.predict(pd.DataFrame({"ds": future.to_timestamp()}))
    return f["yhat"].values


def timesfm():
    import timesfm as tf
    import torch
    torch.set_float32_matmul_precision("high")
    m = tf.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
    m.compile(tf.ForecastConfig(max_context=1024, max_horizon=256, normalize_inputs=True,
                                use_continuous_quantile_head=True, fix_quantile_crossing=True))
    point, _ = m.forecast(horizon=H, inputs=[y.values])
    return np.asarray(point[0])


def chronos():
    import torch
    from chronos import BaseChronosPipeline
    p = BaseChronosPipeline.from_pretrained("amazon/chronos-bolt-base", device_map="cpu", torch_dtype=torch.float32)
    q, _ = p.predict_quantiles(torch.tensor(y.values), prediction_length=H, quantile_levels=[0.1, 0.5, 0.9])
    return q[0, :, 1].numpy()


MODELS = {"SARIMA": sarima, "指数平滑法": ets, "Prophet(Meta)": prophet, "TimesFM(Google)": timesfm, "Chronos(Amazon)": chronos}


def main():
    names = sys.argv[1:] or list(MODELS)
    res = pd.read_csv(OUT, index_col=0) if OUT.exists() else pd.DataFrame(index=[str(p) for p in future])
    for n in names:
        try:
            res[n] = np.round(MODELS[n](), 0)
        except Exception as e:
            print(n, "失敗:", repr(e)[:300])
            continue
        so = res[n].iloc[:2].mean()
        print(f"{n}: 9・10月 {so:.0f}円 誤差 {so / 21363.5 * 100 - 100:+.1f}%  2027年8月 {res[n].iloc[-1]:.0f}円", flush=True)
    res.to_csv(OUT)


if __name__ == "__main__":
    main()
