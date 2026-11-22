"""価格だけを使う統計の比較用モデル(#184 の段0・段2)。年産ごとに1年ずつずらして当てる。

使い方: .venv/bin/python baselines.py
予測するのは「その年産の9・10月の平均」。各年産の予測には、前の年産の8月までの値だけを使う。
消費税を抜いて(2014年3月分まで5%、4月分から8%)計算し、最後に8%を足して税込みに戻す。
2006・2007・2009年産は月ごとの表がないので、農水省の年産平均を使う(月の単純平均ではなく数量の加重平均)。
"""
import numpy as np
import pandas as pd
from pathlib import Path

HERE = Path(__file__).parent
Z80 = 1.2816
ANNUAL_ONLY = {2006: 15203, 2007: 14164, 2009: 14470}  # 年産平均だけの表(H18a, H19a, H21a)


def tax_rate(month):
    return 0.05 if month < pd.Timestamp("2014-04-01") else 0.08


def load():
    m = pd.read_csv(HERE / "data/monthly.csv", index_col=0, parse_dates=True)["all"]
    ex = m / [1 + tax_rate(t) for t in m.index]                      # 税抜き
    crop = ex.index.year - (ex.index.month < 9)
    years = pd.DataFrame({"p": ex, "crop": crop, "mon": ex.index.month})
    ann = years.groupby("crop")["p"].mean()
    sepoct = years[years.mon.isin([9, 10])].groupby("crop")["p"].mean()
    aug = years[years.mon == 8].set_index("crop")["p"]
    for y, v in ANNUAL_ONLY.items():  # 2006・2007は5%、2009も5%
        ann.loc[y] = v / 1.05
    return ann.sort_index(), sepoct, aug, m


def forecast(ann, aug, t):
    """年産 t を、t-1 年産までの年平均と t-1 年産の8月の値で予測する。戻り値は {名前: (点, 下限, 上限)} (税抜き)。"""
    hist = np.log(ann.loc[:t - 1])
    d = hist.diff().dropna()
    out = {}
    sd = d.std(ddof=1)
    last = hist.iloc[-1]
    out["前の年産の平均"] = (last, sd)
    if (t - 1) in aug.index:
        out["前の年産の8月の値"] = (np.log(aug.loc[t - 1]), sd)
    out["ランダムウォーク(傾きあり)"] = (last + d.mean(), sd)
    y, x = hist.values[1:], hist.values[:-1]
    b, a = np.polyfit(x, y, 1)
    res = y - (a + b * x)
    out["AR(1)"] = (a + b * last, res.std(ddof=2))
    return {k: tuple(np.exp([mu, mu - Z80 * s, mu + Z80 * s])) for k, (mu, s) in out.items()}


def main():
    ann, sepoct, aug, raw = load()
    rows = []
    for t in range(2016, 2027):
        for name, (pt, lo, hi) in forecast(ann, aug, t).items():
            act = sepoct.get(t)
            rows.append({"年産": t, "方法": name, "予測": pt * 1.08, "下限80": lo * 1.08, "上限80": hi * 1.08,
                         "実績9_10月": act * 1.08 if act is not None else np.nan})
    df = pd.DataFrame(rows)
    df["誤差%"] = (df["予測"] / df["実績9_10月"] - 1) * 100
    df["区間に入った"] = (df["実績9_10月"] >= df["下限80"]) & (df["実績9_10月"] <= df["上限80"])
    out = HERE / "forecast/baselines.csv"
    df.round(1).to_csv(out, index=False)
    piv = df.pivot(index="年産", columns="方法", values="誤差%").round(1)
    print("誤差%(予測÷実績−1、実績は9・10月の平均、税込み)")
    print(piv.to_string())
    print("\n2026年産(試験A)")
    print(df[df["年産"] == 2026][["方法", "予測", "下限80", "上限80", "実績9_10月", "誤差%", "区間に入った"]].round(0).to_string(index=False))
    print("\n平年(2016〜2023年産)の誤差の絶対値の平均%")
    print(df[df["年産"] <= 2023].groupby("方法")["誤差%"].apply(lambda s: s.abs().mean()).round(1).to_string())


if __name__ == "__main__":
    main()
