"""PT の実務に近い2つの確認。

1. 秒速1.0mの線で分けたとき、動画とセンサーの判定が一致するか
2. 片道1本だけの動画で、速さと歩調がどこまで合うか
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import gait
from compare import H, K_ASSUME, PIDS, ROOT

r = pd.read_csv(ROOT / "results.csv", dtype={"pid": str})
r["pid"] = r.pid.str.zfill(2)

print("== 1. 秒速1.0m未満の判定")
for cam, g in r.groupby("cam"):
    for col in ["speed_assume", "speed_loo"]:
        a = g[col] < 1.0
        b = g.speed_xsens < 1.0
        print(cam, col, f"一致 {int((a == b).sum())}/{len(g)}",
              "食い違い:", list(g.pid[a != b]))

print("\n== 2. 片道1本だけ(最初のまっすぐな片道)")
rows = []
for p in PIDS:
    for cam in ["bottom", "top"]:
        d = pd.read_csv(ROOT / f"pose/OAW{p}-{cam}.csv")
        t, z, hpx, ok = gait.video_track(d, H[p])
        passes, _ = gait.video_passes(t, z, ok)
        xs = r[(r.pid == p) & (r.cam == cam)].iloc[0]
        for i, ps in enumerate(passes):
            v = gait.video_speed_k1([ps]) * K_ASSUME
            c = gait.video_cadence_acf(d, t, ok, [ps], hpx)
            direction = "近づく" if np.polyfit(*ps, 1)[0] < 0 else "離れる"
            rows.append(dict(pid=p, cam=cam, i=i, dir=direction,
                             dur=ps[0][-1] - ps[0][0],
                             speed_err=v - xs.speed_xsens,
                             cad_err=c - xs.cad_xsens))
s = pd.DataFrame(rows)
for cam, g in s.groupby("cam"):
    first = g[g.i == 0]
    print(cam, "片道の長さ(秒) 中央値", round(g.dur.median(), 1))
    print("  最初の片道だけ: 速さの誤差 平均絶対", round(first.speed_err.abs().mean(), 3),
          "最大", round(first.speed_err.abs().max(), 3),
          "| 歩調の誤差 平均絶対", round(first.cad_err.abs().mean(), 2),
          "最大", round(first.cad_err.abs().max(), 2))
    for dr, gg in g.groupby("dir"):
        print("  全片道", dr, len(gg), "本: 速さ 平均絶対", round(gg.speed_err.abs().mean(), 3),
              "| 歩調 平均絶対", round(gg.cad_err.abs().mean(), 2))
s.to_csv(ROOT / "per_pass.csv", index=False)
