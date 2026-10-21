"""全体図(map-base.jpg)に、地名と困りごとの印を描き込む。

- map-overview.jpg: 地名を入れた全体図
- map-problems.jpg: 困りごとの場所を丸で囲んだ図。座標は cargo の道具の値(2041-01-17)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from stitch_map import stitch, world_to_px

HERE = Path(__file__).resolve().parent.parent
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"


def font(size):
    return ImageFont.truetype(FONT, size)


def label(d, xy, text, size=30, fill="white", anchor="mm"):
    d.text(xy, text, font=font(size), fill=fill, anchor=anchor,
           stroke_width=max(2, size // 9), stroke_fill="black")


# 地名。川と道は画素で置く(座標の値を持たないため、全体図を見て決めた)
PLACES_WORLD = [
    ("天神", (-1500, 300), 40),
    ("博多", (300, 450), 40),
    ("天神の南", (-1500, -1950 + 70 / 0.2354), 26),
    ("御笠川の東", (2200, 280), 30),
    ("北の地区", (2350, 2050 - 112 / 0.2354), 26),
    ("博多湾", (-1900, 1450), 36),
]
PLACES_PX = [
    ("那珂川", (870, 770), 24),
    ("御笠川", (1070, 650), 24),
    ("九州自動車道", (1660, 330), 22),
]

HARBOR = (-400, 1555, 1421)
NO_RESOURCES = [(2993, -942, 57), (2300, 1298, 30), (-2384, -542, 30)]
NO_GOODS = [(-1233, -809, 60), (-2147, -1075, 21), (-1006, 86, 16)]


def overview(base):
    img = base.copy()
    d = ImageDraw.Draw(img)
    for text, (x, z), size in PLACES_WORLD:
        label(d, world_to_px(x, z), text, size)
    for text, xy, size in PLACES_PX:
        label(d, xy, text, size, fill="#cfe8ff")
    hx, hy = world_to_px(*HARBOR[:2])
    d.ellipse([hx - 14, hy - 14, hx + 14, hy + 14], outline="white", width=4)
    label(d, (hx + 22, hy - 4), "貨物港", 24, anchor="lm")
    stamp(d, img)
    return img


def ring(d, x, z, r, color, width=6):
    px, py = world_to_px(x, z)
    d.ellipse([px - r, py - r, px + r, py + r], outline="black", width=width + 4)
    d.ellipse([px - r, py - r, px + r, py + r], outline=color, width=width)
    return px, py


def problems(base):
    img = base.copy()
    # 印が見えやすいよう、地図を少し暗くする
    img = Image.blend(img, Image.new("RGB", img.size, "black"), 0.25)
    d = ImageDraw.Draw(img)
    red, orange, blue = "#ff4040", "#ffa020", "#40c0ff"

    px, py = ring(d, HARBOR[0], HARBOR[1], 34, red, 8)
    label(d, (px + 44, py - 14), "貨物港", 30, fill=red, anchor="lm")
    label(d, (px + 44, py + 20), "荷物の車1,421台が止まる", 22, anchor="lm")

    for x, z, n in NO_RESOURCES:
        ring(d, x, z, 22 + n * 0.6, orange)
    for x, z, n in NO_GOODS:
        ring(d, x, z, 22 + n * 0.6, blue)

    # 凡例
    lx, ly = 1270, 860
    d.rounded_rectangle([lx - 16, ly - 50, lx + 480, ly + 72], 10, fill=(0, 0, 0, 180))
    items = [(red, "港の詰まり"), (orange, "原料が届かない工場(126棟)"), (blue, "品物が届かない店(107棟)")]
    for i, (c, t) in enumerate(items):
        y = ly - 30 + i * 36
        d.ellipse([lx, y - 10, lx + 20, y + 10], outline=c, width=5)
        label(d, (lx + 34, y), t, 22, anchor="lm")
    stamp(d, img)
    return img


def stamp(d, img):
    label(d, (16, img.height - 18), "2041年1月17日 人口100,140人", 24, anchor="ls")


if __name__ == "__main__":
    base = stitch()
    overview(base).save(HERE / "map-overview.jpg", quality=92)
    problems(base).save(HERE / "map-problems.jpg", quality=92)
