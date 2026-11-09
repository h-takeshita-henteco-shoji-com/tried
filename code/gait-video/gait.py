"""センサー(Xsens)と動画(MediaPipe)から、歩く速さと歩調を求める。

まっすぐ歩いている区間だけを使う。折り返しの前後は除く。
"""
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, find_peaks

XSENS_HZ = 100
NOSE, LANK, RANK = 0, 27, 28


def lowpass(v, hz, cut):
    b, a = butter(2, cut / (hz / 2))
    return filtfilt(b, a, v)


# ---------- センサー ----------
def xsens_passes(x, margin=2.0):
    """往復の各片道から、両端 margin m を除いた区間の添字を返す。"""
    px = lowpass(x.PelvisX.values, XSENS_HZ, 1.0)
    turns = np.sort(np.r_[find_peaks(px, prominence=3, distance=300)[0],
                          find_peaks(-px, prominence=3, distance=300)[0]])
    edges = np.r_[0, turns, len(px) - 1]
    lo, hi = px.min() + margin, px.max() - margin
    out = []
    for a, b in zip(edges[:-1], edges[1:]):
        idx = np.arange(a, b)
        idx = idx[(px[idx] > lo) & (px[idx] < hi)]
        # 片道を最後まで歩き切った区間だけ使う
        if len(idx) > XSENS_HZ and np.ptp(px[idx]) > (hi - lo) * 0.9:
            out.append(idx)
    return out


def xsens_measures(x):
    px = lowpass(x.PelvisX.values, XSENS_HZ, 1.0)
    py = lowpass(x.PelvisY.values, XSENS_HZ, 1.0)
    v = np.hypot(np.gradient(px), np.gradient(py)) * XSENS_HZ
    passes = xsens_passes(x)
    speed = np.mean([v[i].mean() for i in passes])
    # 足が一番高く上がった瞬間を、1歩と数える
    steps = []
    for s in ["LFootZ", "RFootZ"]:
        z = lowpass(x[s].values, XSENS_HZ, 6)
        steps += list(find_peaks(z, prominence=0.02, distance=30)[0])
    steps = np.sort(steps)
    st = []
    for i in passes:
        k = steps[(steps >= i[0]) & (steps <= i[-1])]
        st += list(np.diff(k) / XSENS_HZ)
    st = np.array(st)
    st = st[(st > 0.3) & (st < 1.2)]
    return dict(speed=speed, step_time=np.median(st),
                cadence=60 / np.median(st), n_pass=len(passes),
                n_steps=len(st))


# ---------- 動画 ----------
def video_track(d, height_m, img_h=1920, vis=0.5):
    """1コマごとの、画面上の体の高さ(px)と、カメラからの距離(K=1)を返す。"""
    t = d.t_ms.values / 1000
    ok = d.x0.notna().values.copy()
    for j in (NOSE, LANK, RANK):
        ok &= (d[f"v{j}"].fillna(0).values > vis)
    ank = (d[f"y{LANK}"] + d[f"y{RANK}"]).values / 2
    ok &= (ank < img_h - 20) & (d[f"y{NOSE}"].fillna(-1).values > 0)
    hpx = ank - d[f"y{NOSE}"].values
    ok &= hpx > 30
    z = height_m / hpx  # 距離 = K * 身長 / 画面上の高さ(Kは後で決める)
    return t, z, hpx, ok


def video_passes(t, z, ok, margin_frac=0.2, min_len=3.0):
    """距離がまっすぐ増える・減る区間を片道として切り出す。"""
    tt, zz = t[ok], z[ok]
    if len(tt) < 30:
        return [], None
    fs = 1 / np.median(np.diff(tt))
    zs = pd.Series(zz).rolling(int(fs), center=True, min_periods=1).median().values
    dz = np.gradient(zs, tt)
    sign = np.sign(pd.Series(dz).rolling(int(fs), center=True,
                                         min_periods=1).mean().values)
    out = []
    start = 0
    for i in range(1, len(tt) + 1):
        gap = i < len(tt) and tt[i] - tt[i - 1] > 1.0
        if i == len(tt) or sign[i] != sign[start] or gap:
            seg = np.arange(start, i)
            if len(seg) > 2 and tt[seg[-1]] - tt[seg[0]] > min_len:
                # 片道の両端(加速・減速)を除く
                lo, hi = np.quantile(zs[seg], [margin_frac, 1 - margin_frac])
                core = seg[(zs[seg] >= lo) & (zs[seg] <= hi)]
                if len(core) > fs:
                    out.append(core)
            start = i
    return [(tt[c], zz[c]) for c in out], (tt, zs)


def video_speed_k1(passes):
    """K=1 のときの速さ。片道ごとに距離を時間で回帰した傾き。"""
    sl, w = [], []
    for tt, zz in passes:
        sl.append(abs(np.polyfit(tt, zz, 1)[0]))
        w.append(tt[-1] - tt[0])
    return np.average(sl, weights=w)


def video_step_time(d, t, ok, passes, hpx):
    """左右の足首の上下差の山と谷を、1歩と数える。"""
    yl = d[f"y{LANK}"].values
    yr = d[f"y{RANK}"].values
    st = []
    for tt, _ in passes:
        m = (t >= tt[0]) & (t <= tt[-1]) & ok
        if m.sum() < 20:
            continue
        ts = t[m]
        fs = 1 / np.median(np.diff(ts))
        s = (yl[m] - yr[m]) / hpx[m]
        s = lowpass(s - s.mean(), fs, 3.0)
        ext = np.sort(np.r_[find_peaks(s, distance=int(fs * 0.3))[0],
                            find_peaks(-s, distance=int(fs * 0.3))[0]])
        st += list(np.diff(ts[ext]))
    st = np.array(st)
    st = st[(st > 0.3) & (st < 1.2)]
    return np.median(st) if len(st) else np.nan, len(st)


def video_cadence_acf(d, t, ok, passes, hpx):
    """左右の足首の上下差が、何秒ごとに繰り返すか(自己相関)から歩調を求める。

    1周期は2歩(左右1歩ずつ)。片道ごとの周期を、長さで重み付けして平均する。
    """
    yl = d[f"y{LANK}"].values
    yr = d[f"y{RANK}"].values
    per, w = [], []
    for tt, _ in passes:
        m = (t >= tt[0]) & (t <= tt[-1]) & ok
        if m.sum() < 40:
            continue
        ts = t[m]
        # 等間隔に並べ直す(検出できなかったコマを補う)
        fs = 30.0
        tu = np.arange(ts[0], ts[-1], 1 / fs)
        s = np.interp(tu, ts, (yl[m] - yr[m]) / hpx[m])
        s = lowpass(s - s.mean(), fs, 3.0)
        ac = np.correlate(s, s, "full")[len(s) - 1:]
        ac /= ac[0]
        lo, hi = int(0.7 * fs), int(1.8 * fs)  # 1周期 0.7〜1.8秒
        if hi >= len(ac) - 1:
            continue
        k = lo + np.argmax(ac[lo:hi])
        # 放物線で、コマの間を補間する
        a, b, c = ac[k - 1], ac[k], ac[k + 1]
        dk = 0.5 * (a - c) / (a - 2 * b + c) if (a - 2 * b + c) != 0 else 0
        per.append((k + dk) / fs)
        w.append(tu[-1] - tu[0])
    if not per:
        return np.nan
    return 120 / np.average(per, weights=w)
