"""開始時点(2041-01-17)の全体図に、エリアの特徴と育った順番を描き込む。

全体図は #14 の stitch_map.py で、真上から撮った写真をつないで作る。
座標と年は grow/grow-note.md の記録から取った。
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
SRC = HERE.parent.parent / "10-21-AIは最高の市長になれるか-14-4人を市長として定義する/assets/scripts"
sys.path.insert(0, str(SRC))
from stitch_map import stitch, world_to_px  # noqa: E402

FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
f = lambda s: ImageFont.truetype(FONT, s)


def label(d, xy, text, size, fill="white", anchor="mm"):
    d.text(xy, text, font=f(size), fill=fill, anchor=anchor,
           stroke_width=max(2, size // 9), stroke_fill="black")


# (番号, 名前, 特徴, 年と人口, 座標)
AREAS = [
    ("1", "最初の街", "住宅と工業", "2031年 9,334人", (3750, -250)),
    ("2", "北の地区", "オフィスと住宅", "2033年 約2万人", (2300, 700)),
    ("3", "博多", "店・オフィス・病院", "2033年 約3万人", (230, 200)),
    ("4", "御笠川の東", "オフィス街", "2034年 約3.7万人", (1240, 150)),
    ("5", "天神", "高層の住宅と店の通り", "2035年 約3.9万人", (-1500, 250)),
    ("6", "貨物港", "港は1つだけ", "2037年 約5.7万人", (-400, 1555)),
    ("7", "天神の南", "高層の住宅", "2040年 約9万人", (-1350, -1150)),
]
OTHERS = [
    ("大学と HighTech 地区", (2370, -420), "#cfe8ff"),
    ("工業", (2900, -950), "#ffc060"),
    ("工業", (2250, 1260), "#ffc060"),
    ("工業", (-2400, -560), "#ffc060"),
]

if __name__ == "__main__":
    img = stitch()
    img = Image.blend(img, Image.new("RGB", img.size, "black"), 0.2)
    d = ImageDraw.Draw(img)
    for text, (x, z), c in OTHERS:
        label(d, world_to_px(x, z), text, 24, fill=c)
    for n, name, feat, when, (x, z) in AREAS:
        px, py = world_to_px(x, z)
        r = 20
        d.ellipse([px - r, py - r - 34, px + r, py + r - 34], fill="#e04040", outline="white", width=3)
        label(d, (px, py - 34), n, 24)
        label(d, (px, py + 4), name, 32)
        label(d, (px, py + 38), feat, 22, fill="#ffe680")
        label(d, (px, py + 64), when, 18, fill="#dddddd")
    label(d, (16, img.height - 18), "2041年1月17日 人口100,140人。数字は街が広がった順", 24, anchor="ls")
    img.save(HERE / "map-areas.jpg", quality=92)
