"""11人について、動画とセンサーの歩く速さ・歩調を比べる。

K(カメラの焦点距離と体の比率をまとめた定数)は、2通りで決める。
- 仮定: スマホの画角と体の比率を、一般的な値で置く
- 校正: 本人以外の10人で K を決め、本人に当てはめる(leave-one-out)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import gait

ROOT = Path("/tmp/toaga")
PIDS = ["01", "02", "03", "05", "06", "09", "10", "11", "12", "13", "14"]

# 仮定の K: 縦1920pxの長辺の画角を約65度とおく。鼻から足首は身長の約0.89
F_PX = (1920 / 2) / np.tan(np.radians(65 / 2))
K_ASSUME = F_PX * 0.89

meta = pd.read_excel(ROOT / "meta/table1.xlsx", nrows=14)
meta = meta.rename(columns=lambda c: str(c).strip())
H = {f"{int(r['Participant No.']):02d}": r["Height (cm)"] / 100
     for _, r in meta.iterrows()}
TUG = {f"{int(r['Participant No.']):02d}": r["TUG (s)"]
       for _, r in meta.iterrows()}


def main():
    global ROOT
    ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
    rows = []
    for p in PIDS:
        x = pd.read_csv(ROOT / f"meta/Xsens/OAW{p}.csv")
        xs = gait.xsens_measures(x)
        for cam in ["bottom", "top"]:
            f = ROOT / f"pose/OAW{p}-{cam}.csv"
            if not f.exists():
                continue
            d = pd.read_csv(f)
            t, z, hpx, ok = gait.video_track(d, H[p])
            passes, _ = gait.video_passes(t, z, ok)
            if not passes:
                continue
            v1 = gait.video_speed_k1(passes)
            st, n = gait.video_step_time(d, t, ok, passes, hpx)
            cad_acf = gait.video_cadence_acf(d, t, ok, passes, hpx)
            rows.append(dict(pid=p, cam=cam, tug=TUG[p], height=H[p],
                             detect=round(d.x0.notna().mean(), 3),
                             n_pass_video=len(passes), n_steps_video=n,
                             speed_xsens=xs["speed"], v_k1=v1,
                             cad_xsens=xs["cadence"],
                             cad_video=60 / st if st == st else np.nan,
                             cad_acf=cad_acf))

    r = pd.DataFrame(rows)
    r["speed_assume"] = r.v_k1 * K_ASSUME
    # leave-one-out で K を決める(カメラごと)
    r["speed_loo"] = np.nan
    for cam, g in r.groupby("cam"):
        for i in g.index:
            others = g.drop(i)
            k = np.median(others.speed_xsens / others.v_k1)
            r.loc[i, "speed_loo"] = r.loc[i, "v_k1"] * k


    def summary(a, b):
        e = a - b
        return dict(MAE=np.mean(np.abs(e)), bias=np.mean(e),
                    MAPE=np.mean(np.abs(e) / b) * 100,
                    r=np.corrcoef(a, b)[0, 1])


    print(f"K_ASSUME={K_ASSUME:.0f}")
    pd.set_option("display.width", 200)
    print(r.round(3).to_string())
    for cam, g in r.groupby("cam"):
        print(f"\n== {cam} (n={len(g)})")
        for col, ref in [("speed_assume", "speed_xsens"),
                         ("speed_loo", "speed_xsens"),
                         ("cad_video", "cad_xsens"),
                         ("cad_acf", "cad_xsens")]:
            s = summary(g[col].values, g[ref].values)
            print(col, {k: round(v, 3) for k, v in s.items()})
    r.to_csv(OUT / "results.csv", index=False)


if __name__ == "__main__":
    main()
