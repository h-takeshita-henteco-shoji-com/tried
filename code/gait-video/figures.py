"""記事用の図を作る。results.csv と動画1コマを使う。"""
import sys
from pathlib import Path

import cv2
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
plt.rcParams.update({"font.family": "Hiragino Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8a8984", "axes.labelcolor": "#0b0b0b",
                     "xtick.color": "#52514e", "ytick.color": "#52514e"})
BLUE, ORANGE, GRID, INK2 = "#2a78d6", "#eb6834", "#e6e5e0", "#52514e"

r = pd.read_csv(ROOT / "results.csv", dtype={"pid": str})
r["pid"] = r.pid.str.zfill(2)
b = r[r.cam == "bottom"]
t = r[r.cam == "top"]


def ident(ax, lo, hi):
    ax.plot([lo, hi], [lo, hi], color="#8a8984", lw=1, ls="--", zorder=0)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_aspect("equal")
    ax.grid(color=GRID, lw=0.8)


# 図1 速さ
fig, ax = plt.subplots(figsize=(5.6, 5.4))
ident(ax, 0.3, 1.4)
ax.axvline(1.0, color=GRID, lw=2, zorder=0)
ax.axhline(1.0, color=GRID, lw=2, zorder=0)
ax.scatter(b.speed_xsens, b.speed_assume, s=70, color=BLUE,
           edgecolor="white", lw=2, label="目の高さのカメラ(校正なし)", zorder=3)
ax.scatter(t.speed_xsens, t.speed_loo, s=70, color=ORANGE, marker="s",
           edgecolor="white", lw=2, label="天井近くのカメラ(他の10人で校正)",
           zorder=3)
for df, col in [(b, "speed_assume")]:
    for _, row in df.iterrows():
        if row.pid in ("13", "14"):
            ax.annotate(f"参加者{int(row.pid)}", (row.speed_xsens, row[col]),
                        xytext=(10, -14), textcoords="offset points",
                        color=INK2, fontsize=10)
ax.set_xlabel("センサーで測った速さ(m/秒)")
ax.set_ylabel("動画から求めた速さ(m/秒)")
ax.set_title("歩く速さ:動画とセンサー(11人)", loc="left", fontsize=13)
ax.text(1.01, 0.33, "秒速1.0m", color=INK2, fontsize=9)
ax.legend(frameon=False, loc="upper left", fontsize=9.5)
fig.tight_layout()
fig.savefig(OUT / "1-歩く速さ.png", dpi=200)

# 図2 歩調(数え方の比較)
fig, axs = plt.subplots(1, 2, figsize=(9, 4.8), sharey=True)
for ax, col, title in [(axs[0], "cad_video", "山と谷の間隔で数える"),
                       (axs[1], "cad_acf", "繰り返しの周期で数える")]:
    ident(ax, 80, 140)
    ax.scatter(b.cad_xsens, b[col], s=60, color=BLUE, edgecolor="white",
               lw=2, label="目の高さのカメラ", zorder=3)
    ax.scatter(t.cad_xsens, t[col], s=60, color=ORANGE, marker="s",
               edgecolor="white", lw=2, label="天井近くのカメラ", zorder=3)
    mae = np.mean(np.abs(pd.concat([b[col] - b.cad_xsens,
                                    t[col] - t.cad_xsens])))
    ax.set_title(f"{title}\n平均の誤差 {mae:.1f}歩/分", loc="left",
                 fontsize=12)
    ax.set_xlabel("センサーの歩調(歩/分)")
axs[0].set_ylabel("動画の歩調(歩/分)")
axs[1].legend(frameon=False, loc="lower right", fontsize=9.5)
fig.tight_layout()
fig.savefig(OUT / "2-歩調の数え方.png", dpi=200)

# 図3 骨格を重ねた1コマ(参加者10、顔はデータ提供元でぼかし済み)
d = pd.read_csv(ROOT / "pose/OAW10-bottom.csv")
cap = cv2.VideoCapture(str(ROOT / "videos/Videos/OAW10-bottom.mp4"))
fr = int(sys.argv[3]) if len(sys.argv) > 3 else 1150
cap.set(cv2.CAP_PROP_POS_FRAMES, fr)
ok, img = cap.read()
row = d.iloc[fr]
pts = {i: (int(row[f"x{i}"]), int(row[f"y{i}"])) for i in range(33)
       if row[f"x{i}"] == row[f"x{i}"]}
bones = [(11, 12), (11, 23), (12, 24), (23, 24), (23, 25), (25, 27),
         (24, 26), (26, 28), (11, 13), (13, 15), (12, 14), (14, 16),
         (27, 31), (28, 32), (27, 29), (28, 30)]
for a, c in bones:
    if a in pts and c in pts:
        cv2.line(img, pts[a], pts[c], (214, 120, 42), 6, cv2.LINE_AA)
for i in [0, 27, 28]:
    if i in pts:
        cv2.circle(img, pts[i], 14, (52, 104, 235), -1, cv2.LINE_AA)
ys = [p[1] for p in pts.values()]
xs = [p[0] for p in pts.values()]
y0, y1 = max(min(ys) - 250, 0), min(max(ys) + 150, img.shape[0])
cx = int(np.median(xs))
x0, x1 = max(cx - 190, 0), min(cx + 190, img.shape[1])
img = img[y0:y1, x0:x1]
cv2.imwrite(str(OUT / "3-骨格の推定.jpg"),
            img,
            [cv2.IMWRITE_JPEG_QUALITY, 85])
print("frame", fr, "hpx", round(row.y27 / 2 + row.y28 / 2 - row.y0))
