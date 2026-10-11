"""カット3(3秒): ぬめが段差の前で触角を下げ、縁の石に登る。AIを使わない。

Wan では、垂直の面を登る所でぬめが縦に立ち上がり、ウサギに見えた(wan-cut03-1、wan-cut03-2a)。
後半(乗り越えかけ→登りきる)は Wan でうまくいったが、480×864 で前後のカットと解像度が合わない。全体を Python で作る。
- 0〜0.7秒: ふもとで触角を 40°→70° に下げる。
- 0.7〜2.2秒: 体は横向きのまま、石の前の面に沿って上へ滑る。角の近くで 8° 傾け、乗り越えかけの姿にする。
  これまで体を傾けると浮いて見えたため、登る間は傾けない。
- 2.2〜3.0秒: 石の上を右へ滑り、終点(#19 の py-cut03.png)の姿に収まる。
横向きのまま上へ滑らせると、石の前に浮いて見えた。次の2つを足した。
- 壁に落ちる影: 体の形の影を左下へずらしてぼかし、面に付いて見せる。ふもとでも同じ影を使う。
- 這うリズム: 登る間だけ、体を縦に縮めたり伸ばしたりする(2回)。
這った跡のぬめりは描かない。10-03 で「粘液・光沢を描かない」と決めたため。
位置は体の後ろの下端(尾の付け根)を基準にし、そこを中心に回す。触角の角度で絵の大きさが変わっても、体がぶれない。
"""
import os
import subprocess
import sys
from pathlib import Path

import math

from PIL import Image, ImageFilter, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from small_moves import EVENING, FFMPEG, FPS, H, W, bg_crop, nume_at  # noqa: E402  (#19 の assets に移る)
from compose import NUME_BODY_W, NUME_LINE_W, OUT_LINE_W, thicken  # noqa: E402

OUT = Path(__file__).resolve().parents[1]
SEC = 3
R = 330 / 1.3 / NUME_BODY_W  # #19 のカット3と同じ大きさ
BOX = (0, 665, 400, 665 + round(400 * H / W))

# (時刻, 後ろの下端x, 後ろの下端y, 体の傾き, 触角の角度)
KEYS = [
    (0.0, 3, 800, 0, 40),
    (0.7, 3, 800, 0, 70),
    (1.8, 30, 600, 0, 72),
    (2.2, 66, 574, 8, 75),
    (3.0, 118, 551, 6, 70),
]

def ease(t):
    return t * t * (3 - 2 * t)

def at(t):
    for (t0, *a), (t1, *b) in zip(KEYS, KEYS[1:]):
        if t <= t1:
            u = ease((t - t0) / (t1 - t0))
            return [x + (y - x) * u for x, y in zip(a, b)]
    return KEYS[-1][1:]

_scaled = {}

def scaled(deg):
    key = round(deg * 2) / 2
    if key not in _scaled:
        grow = max(1, round(OUT_LINE_W / R - NUME_LINE_W))
        n = thicken(nume_at(key), size=grow + 1 - grow % 2)
        n = n.resize((round(n.width * R), round(n.height * R)), Image.LANCZOS)
        _scaled[key] = ImageOps.mirror(n)  # 右向き。後ろの下端が左下の角になる
    return _scaled[key]

CLIMB = (0.7, 2.0)       # 這うリズムを付ける時間
SHADOW = (-8, 8, 4, 150)  # 影のずれx, ずれy, ぼかし, 濃さ。(-5, 5, 3, 80) では暗い石の面で見えなかった

def squash(t):
    """登る間だけ、縦の倍率を 1±0.05 で2回ゆらす。"""
    a, b = CLIMB
    if not a < t < b:
        return 1.0
    u = (t - a) / (b - a)
    return 1 + 0.05 * math.sin(2 * math.pi * 2 * u) * math.sin(math.pi * u)

def frame(bg, t):
    rx, ry, rot, deg = at(t)
    n = scaled(deg)
    k = squash(t)
    if k != 1.0:
        n = n.resize((n.width, round(n.height * k)), Image.LANCZOS)
    layer = Image.new("RGBA", (W, H))
    layer.alpha_composite(n, (round(rx), round(ry) - n.height))
    if abs(rot) > 0.01:
        layer = layer.rotate(rot, resample=Image.BICUBIC, center=(rx, ry))
    c = bg.copy()
    dx, dy, blur, alpha = SHADOW
    sh = Image.new("RGBA", (W, H), (30, 25, 25, 0))
    sh.putalpha(layer.getchannel("A").point(lambda v: v * alpha // 255))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (dx, dy))
    c.alpha_composite(layer)
    return c.convert("RGB")

if __name__ == "__main__":
    bg = bg_crop(EVENING, BOX)
    if len(sys.argv) > 1:  # 確認用: 指定した時刻のコマだけ書く
        for t in sys.argv[1:]:
            frame(bg, float(t)).save(f"/tmp/c3_{t}.png")
        sys.exit()
    p = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", str(OUT / "generated/py-cut03.mp4")],
                         stdin=subprocess.PIPE)
    for k in range(FPS * SEC):
        p.stdin.write(frame(bg, k / FPS).tobytes())
    p.stdin.close()
    p.wait()
    print(OUT / "generated/py-cut03.mp4")
