"""真上から撮った6枚(tiles/)を、ゲームの座標でつないで全体図を作る。

撮り方: move_camera(x, z, size=4000, pitch=90, yaw=0) のあと screenshot(max_width=1920)。
画像は 1512x921。カメラの見る点は画素 (756, 410)、縮尺は 0.2354 画素/m(2,000mずらして471画素動いた)。
左上の道具の記録の窓と、下の操作の帯は使わない。重なる所は、写真の中心に近いものを使う。
"""
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
K = 0.2354          # 画素/m
CX, CY = 756, 410   # カメラの見る点の画素
X0, X1 = -2950, 4550  # 全体図に入れる範囲(m)
Z0, Z1 = -1950, 2050


def world_to_px(x, z):
    """ゲームの座標(m)を、全体図の画素に直す。"""
    return (x - X0) * K, (Z1 - z) * K


def valid_mask(h, w):
    m = np.ones((h, w), bool)
    m[815:, :] = False          # 下の操作の帯
    m[:435, :640] = False       # 道具の記録の窓
    m[:75, 700:800] = False     # 上の鳥の印
    m[:60, 1400:] = False       # 右上の印
    m[:, :4] = m[:, -4:] = False
    return m


def stitch():
    W = int((X1 - X0) * K)
    H = int((Z1 - Z0) * K)
    out = np.zeros((H, W, 3), np.uint8)
    best = np.full((H, W), np.inf)
    for f in sorted((HERE / "tiles").glob("tile_*.jpg")):
        _, sx, sz = f.stem.split("_")
        tx, tz = float(sx), float(sz)
        img = np.asarray(Image.open(f).convert("RGB"))
        h, w, _ = img.shape
        mask = valid_mask(h, w)
        # タイルの左上が全体図のどこに来るか
        ox, oy = world_to_px(tx, tz)
        ox, oy = int(round(ox - CX)), int(round(oy - CY))
        ys, xs = np.nonzero(mask)
        cy, cx = ys + oy, xs + ox
        ok = (cy >= 0) & (cy < H) & (cx >= 0) & (cx < W)
        ys, xs, cy, cx = ys[ok], xs[ok], cy[ok], cx[ok]
        d = (xs - CX) ** 2 + (ys - CY) ** 2
        better = d < best[cy, cx]
        out[cy[better], cx[better]] = img[ys[better], xs[better]]
        best[cy[better], cx[better]] = d[better]
    return Image.fromarray(out)


if __name__ == "__main__":
    stitch().save(HERE / "map-base.jpg", quality=92)  # 確かめる用。リポジトリには置かない
