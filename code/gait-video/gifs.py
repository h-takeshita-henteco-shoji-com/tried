"""記事用の GIF を作る。骨格と、カメラまでの距離・歩く速さを重ねる。

1枚の動画、または2本を横に並べた動画を作れる。
使い方: python gifs.py <ROOT> <出力フォルダ>
"""
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

import gait
from compare import H, K_ASSUME

FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FPS = 8
BONES = [(11, 12), (11, 23), (12, 24), (23, 24), (23, 25), (25, 27),
         (24, 26), (26, 28), (11, 13), (13, 15), (12, 14), (14, 16),
         (27, 31), (28, 32)]
INK, INK2, BLUE = (11, 11, 11), (82, 81, 78), (42, 120, 214)


def font(n):
    return ImageFont.truetype(FONT, n)


def live_values(d, h):
    t, z, hpx, ok = gait.video_track(d, h)
    dist = pd.Series(np.where(ok, z * K_ASSUME, np.nan)).interpolate(limit=10)
    dist = dist.rolling(9, center=True, min_periods=3).median().values
    spd = np.full(len(t), np.nan)
    for i in range(len(t)):
        m = (t > t[i] - 1.5) & (t <= t[i]) & ~np.isnan(dist)
        if m.sum() > 10:
            spd[i] = abs(np.polyfit(t[m], dist[m], 1)[0])
    return t, dist, spd


def panel(root, p, cam, t0, dur, width, title, sub=None, half=200):
    """1本分のコマ(PIL画像)のリストを返す。"""
    d = pd.read_csv(root / f"pose/OAW{p}-{cam}.csv")
    t, dist, spd = live_values(d, H[p])
    sel = np.where((t >= t0) & (t <= t0 + dur))[0]
    xs = d.loc[sel, [f"x{j}" for j in range(11, 29)]].values.ravel()
    cx = int(np.nanmedian(xs))
    x0, x1 = max(cx - half, 0), min(cx + half, 1080)
    ys = d.loc[sel, ["y0", "y27", "y28"]].values
    y0 = int(max(np.nanmin(ys[:, 0]) - 140, 0))
    y1 = int(min(np.nanmax(ys[:, 1:]) + 60, 1920))
    cap = cv2.VideoCapture(str(root / f"videos/Videos/OAW{p}-{cam}.mp4"))
    # 速さは、片道の始めからその時点までの距離を、時間で回帰した傾き
    # (時間がたつほど安定し、最後は片道全体の推定値になる)
    spd = np.full(len(t), np.nan)
    for i in sel:
        m = (t >= t0) & (t <= t[i]) & ~np.isnan(dist)
        if t[i] - t0 >= 1.5 and m.sum() > 10:
            spd[i] = abs(np.polyfit(t[m], dist[m], 1)[0])
    out = []
    for k in range(int(dur * FPS)):
        tk = t0 + k / FPS
        i = int(np.argmin(np.abs(t - tk)))
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, img = cap.read()
        if not ok:
            break
        row = d.iloc[i]
        pts = {j: (int(row[f"x{j}"]), int(row[f"y{j}"])) for j in range(33)
               if row[f"x{j}"] == row[f"x{j}"]}
        for a, b in BONES:
            if a in pts and b in pts:
                cv2.line(img, pts[a], pts[b], (214, 120, 42), 7, cv2.LINE_AA)
        for j in (0, 27, 28):
            if j in pts:
                cv2.circle(img, pts[j], 13, (52, 104, 235), -1, cv2.LINE_AA)
        img = img[y0:y1, x0:x1]
        im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        im = im.resize((width, int(im.height * width / im.width)))
        out.append((im, dist[i], spd[i]))
    return out, title, sub


def decorate(frames_info, height, width):
    """見出しと、距離・速さの帯を付ける。高さをそろえる。"""
    frames, title, sub = frames_info
    res = []
    top = 64 if sub else 40
    for im, dv, sv in frames:
        im = im.resize((width, height)) if im.height != height else im
        c = Image.new("RGB", (width, height + top + 84), "white")
        c.paste(im, (0, top))
        dr = ImageDraw.Draw(c)
        dr.text((10, 6), title, font=font(22), fill=INK)
        if sub:
            dr.text((10, 36), sub, font=font(17), fill=INK2)
        y = top + height + 6
        dr.text((10, y), "カメラまで", font=font(15), fill=INK2)
        dr.text((10, y + 24), f"{dv:4.1f} m" if dv == dv else "  -",
                font=font(24), fill=INK)
        dr.text((width // 2 - 14, y), "歩く速さ(動画)", font=font(15), fill=INK2)
        dr.text((width // 2 - 14, y + 24), f"秒速 {sv:4.2f} m" if sv == sv else "測っています",
                font=font(22), fill=BLUE)
        res.append(c)
    return res


def save(frames_list, out, gap=12):
    n = min(len(f) for f in frames_list)
    w = sum(f[0].width for f in frames_list) + gap * (len(frames_list) - 1)
    h = max(f[0].height for f in frames_list)
    seq = []
    for k in range(n):
        c = Image.new("RGB", (w, h), "white")
        x = 0
        for f in frames_list:
            c.paste(f[k], (x, 0))
            x += f[k].width + gap
        seq.append(c.convert("P", palette=Image.ADAPTIVE, colors=96))
    seq[0].save(out, save_all=True, append_images=seq[1:],
                duration=int(1000 / FPS), loop=0, optimize=True)
    print(out.name, n, "frames", out.stat().st_size // 1024, "KB")


def pair(root, out, specs, width=300, height=520):
    fl = [decorate(panel(root, *s[:4], width, s[4], s[5],
                         half=s[6] if len(s) > 6 else 200),
                   height, width) for s in specs]
    save(fl, out)


if __name__ == "__main__":
    ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
    # 0. ハイライト(1人)
    pair(ROOT, OUT / "0-歩く速さを測る.gif", [
        ("12", "bottom", 35.5, 7.5, "Dさん", "センサー 秒速0.92m")], width=330,
        height=560)
    # 1. 遅い人(Aさん)と速い人(Kさん)
    pair(ROOT, OUT / "6-遅い人と速い人.gif", [
        ("13", "bottom", 13.0, 6.0, "Aさん", "センサー 秒速0.47m", 140),
        ("03", "bottom", 10.4, 6.0, "Kさん", "センサー 秒速1.15m")])
    # 2. ずれた人(Fさん)
    pair(ROOT, OUT / "7-ずれた人.gif", [
        ("14", "bottom", 33.0, 7.0, "Fさん", "センサー 秒速1.03m")], width=330,
        height=560)
    # 3. 同じ人(Kさん)を、目の高さと天井近くで
    pair(ROOT, OUT / "8-カメラの高さ.gif", [
        ("03", "bottom", 10.4, 5.5, "目の高さのカメラ", "Kさん センサー 秒速1.15m"),
        ("03", "top", 8.6, 5.5, "天井近くのカメラ", "Kさん センサー 秒速1.15m")])
