"""出発点の街(fukuoka-grow-179k、2050-01-01)の地図を作る。

- 真上から撮った写真(tiles/、take_tiles.py で撮る)を、実際に見ている点(centers.json)でつなぐ
- map-start-overview.jpg: エリアの名前を入れた全体図
- map-start-problems.jpg: 困りごとの場所に丸を付けた図。座標は cargo と complaints の値(2050-01-01)
つなぎ方と縮尺は #89 の地図(10-21 の assets/scripts/stitch_map.py)と同じ。
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
K = 0.2354          # 画素/m(size 4000、pitch 90 のとき)
CX, CY = 756, 410   # カメラの見る点の画素
X0, X1 = -3200, 4800
Z0, Z1 = -2400, 2300
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"


def world_to_px(x, z):
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
    centers = json.loads((HERE / "tiles" / "centers.json").read_text())
    W, H = int((X1 - X0) * K), int((Z1 - Z0) * K)
    out = np.zeros((H, W, 3), np.uint8)
    best = np.full((H, W), np.inf)
    for name, (tx, tz) in centers.items():
        img = np.asarray(Image.open(HERE / "tiles" / name).convert("RGB"))
        h, w, _ = img.shape
        mask = valid_mask(h, w)
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




def font(size):
    return ImageFont.truetype(FONT, size)


def label(d, xy, text, size=30, fill="white", anchor="mm"):
    d.text(xy, text, font=font(size), fill=fill, anchor=anchor,
           stroke_width=max(2, size // 9), stroke_fill="black")


# エリアの名前。#89 の地図と同じ呼び方。10万人の後に広がった所は、近い地名に「南」などを付けた
PLACES = [
    ("天神", (-1500, 300), 42),
    ("博多", (300, 380), 42),
    ("天神の南", (-1500, -1650), 28),
    ("博多の南", (200, -1740), 28),
    ("御笠川の東", (2300, 280), 32),
    ("北の地区", (2350, 1620), 28),
    ("東の工業地", (3200, -1150), 26),
    ("博多湾", (-1900, 1550), 40),
]
WATER = [
    ("那珂川", (746, -1221), 24),
    ("御笠川", (1595, -760), 24),
    ("九州自動車道", (4250, 950), 22),
]
CARGO_STATION = (3449, -1555, 492)
HARBOR = (-2000, 605)
NO_GOODS = [(-1069, -770, 74), (2206, 729, 46), (1004, 300, 33)]
GARBAGE = (-459, -1468, 9)
POLLUTION = (3882, -296, 16)
DEATH = (2240, 186, 27)
STAMP = "2050年1月1日 人口178,872人"


def crop(img):
    # 左上の、写真のない角を切る
    return img.crop((60, int((2300 - 2030) * K), img.width, img.height))


def overview(base):
    img = base.copy()
    d = ImageDraw.Draw(img)
    for text, (x, z), size in PLACES:
        label(d, world_to_px(x, z), text, size)
    for text, (x, z), size in WATER:
        label(d, world_to_px(x, z), text, size, fill="#cfe8ff")
    for text, (x, z) in [("東の貨物駅", CARGO_STATION[:2]), ("貨物港", HARBOR)]:
        px, py = world_to_px(x, z)
        d.ellipse([px - 14, py - 14, px + 14, py + 14], outline="white", width=4)
        label(d, (px + 22, py - 4), text, 24, anchor="lm")
    img = crop(img)
    stamp(ImageDraw.Draw(img), img)
    return img


def ring(d, x, z, r, color, width=6):
    px, py = world_to_px(x, z)
    d.ellipse([px - r, py - r, px + r, py + r], outline="black", width=width + 4)
    d.ellipse([px - r, py - r, px + r, py + r], outline=color, width=width)
    return px, py


def problems(base):
    img = Image.blend(base.copy(), Image.new("RGB", base.size, "black"), 0.25)
    d = ImageDraw.Draw(img)
    red, blue, yellow, purple, white = "#ff4040", "#40c0ff", "#ffd020", "#d070ff", "#f0f0f0"

    px, py = ring(d, CARGO_STATION[0], CARGO_STATION[1], 34, red, 8)
    label(d, (px - 44, py - 14), "東の貨物駅", 30, fill=red, anchor="rm")
    label(d, (px - 44, py + 20), "トラック492台が止まる", 22, anchor="rm")
    for x, z, n in NO_GOODS:
        ring(d, x, z, 24 + n * 0.6, blue)
    ring(d, GARBAGE[0], GARBAGE[1], 24 + GARBAGE[2] * 2, yellow)
    ring(d, POLLUTION[0], POLLUTION[1], 24 + POLLUTION[2] * 2, purple)
    ring(d, DEATH[0], DEATH[1], 24 + DEATH[2] * 1.2, white)

    lx, ly = 100, img.height - 250
    d.rounded_rectangle([lx - 14, ly - 34, lx + 470, ly + 160], 10, fill=(0, 0, 0))
    items = [(red, "貨物駅の詰まり"), (blue, "品物が届かない店(228棟)"), (white, "死者の印(52棟)"),
             (purple, "汚染の印(32棟)"), (yellow, "ごみの印(15棟)")]
    for i, (c, t) in enumerate(items):
        y = ly - 14 + i * 36
        d.ellipse([lx, y - 10, lx + 20, y + 10], outline=c, width=5)
        label(d, (lx + 34, y), t, 22, anchor="lm")
    img = crop(img)
    stamp(ImageDraw.Draw(img), img, right=True)
    return img


def stamp(d, img, right=False):
    if right:
        label(d, (img.width - 16, img.height - 18), STAMP, 24, anchor="rs")
    else:
        label(d, (16, img.height - 18), STAMP, 24, anchor="ls")


if __name__ == "__main__":
    base = stitch()
    overview(base).save(HERE / "map-start-overview.jpg", quality=90)
    problems(base).save(HERE / "map-start-problems.jpg", quality=90)
