"""小さい動き(カット1、4、5、6、7)。AIを使わず、#19 の静止画の作り方に動きを足す。

- 湯気: 背景に描き込まれているので、湯気のある範囲だけを横に波打たせる。
  波は下から上へ進むので、立ちのぼって見える。空と湯は横方向に色が一様なので、横にずらしても湯気以外はほぼ変わらない。
  範囲は、どんと石の縦の線に掛からないように、カットごとに決めた。縁はぼかして混ぜる。
- 触角: #19 の tilt の角度を、前に倒した40°のまわりで少しずつ変える。
#19 の assets を作業場所にして実行する(compose.py と素材を使うため)。
使い方: python3 small_moves.py [カット番号 ...]   (省略時は全部)
"""
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

S19 = Path(__file__).resolve().parents[3] / "10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets"
OUT = Path(__file__).resolve().parents[1] / "generated"
WORK = Path(__file__).resolve().parents[1] / "work"
sys.path.insert(0, str(S19 / "work"))
os.chdir(S19)
from antenna import tilt  # noqa: E402
from compose import H, W, bg_crop, put_don, put_nume  # noqa: E402

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FPS = 24
EVENING = "input/bg-c1-evening.jpeg"

def write(name, frames, sec):
    p = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", str(OUT / name)], stdin=subprocess.PIPE)
    for n in range(FPS * sec):
        f = frames(n / FPS)
        p.stdin.write(f.convert("RGB").tobytes())
        if n == FPS:  # 1秒目のコマを確認用に残す
            f.convert("RGB").save(WORK / name.replace(".mp4", "-f24.png"))
    p.stdin.close()
    p.wait()
    print(OUT / name)

class Steam:
    """box の中だけを横に波打たせる。amp(t) で揺れの大きさを時間で変える。"""

    def __init__(self, box, feather=40, wave=220, period=2.0, amp=6.0):
        x0, y0, x1, y1 = box
        m = np.zeros((H, W), float)
        m[y0:y1, x0:x1] = 1
        self.mask = ndimage.gaussian_filter(m, feather / 2)
        self.yy, self.xx = np.mgrid[0:H, 0:W].astype(float)
        self.wave, self.period, self.amp = wave, period, amp

    def __call__(self, im, t, k=1.0):
        a = np.asarray(im.convert("RGB")).astype(float)
        dx = self.amp * k * self.mask * np.sin(2 * math.pi * (self.yy / self.wave + t / self.period))
        out = np.stack([ndimage.map_coordinates(a[..., c], [self.yy, self.xx + dx], order=1, mode="nearest")
                        for c in range(3)], -1)
        return Image.fromarray(out.clip(0, 255).astype(np.uint8))

_nume_cache = {}
NUME_BOARD = (1300, 1300)  # 触角を倒した絵が収まる大きさ

def nume_at(deg):
    """触角の角度ごとの絵。0.5°刻みでまとめて、作り直しを減らす。
    tilt は絵を余白なしで切り抜くため、角度で大きさが変わる。そのまま縮めると端数で体が1pxほどぶれた。
    体のある右下をそろえて一定の台紙に貼り、大きさを固定する。
    """
    key = round(deg * 2) / 2
    if key not in _nume_cache:
        n = tilt(Image.open("work/nume-side.png"), pivot=(240, 430), y0=388, deg=key, x_max=328)
        board = Image.new("RGBA", NUME_BOARD)
        board.alpha_composite(n, (NUME_BOARD[0] - n.width, NUME_BOARD[1] - n.height))
        _nume_cache[key] = board
    return _nume_cache[key]

def sway(t, base=40, amp=3, period=1.6):
    """前に倒した40°のまわりで、ゆっくり揺らす。"""
    return base + amp * math.sin(2 * math.pi * t / period)

def cut01():
    """カット1(4秒): 夕方の引き。湯気が立ちのぼる。どんは動かない。"""
    still = Image.open("generated/py-cut01.png")
    steam = Steam((490, 500, 768, 870))  # 縁のぼかしが石の右端とタオルに掛からないよう、内側に寄せた
    write("py-cut01.mp4", lambda t: steam(still, t), 4)

def cut04():
    """カット4(4秒): 2匹が並ぶ。触角が倒れたまま揺れる。湯気も揺らす。"""
    box = (130, 440, 630, 440 + round(500 * H / W))
    bg = bg_crop(EVENING, box)
    don = Image.open("work/don-left.png")
    steam = Steam((570, 200, 768, 640))

    def f(t):
        c = bg.copy()
        put_don(c, don, head_h=330, cx=560, water_y=1020)
        put_nume(c, nume_at(sway(t)), 330, cx=263, foot_y=545)
        return steam(c, t)
    write("py-cut04.mp4", f, 4)

def cut05_06():
    """カット5(3秒): 湯気が1度だけ流れる。カット6(4秒): 同じ絵で、湯気はごく弱く揺れ続ける。"""
    still = Image.open("generated/py-cut05.png")
    steam = Steam((270, 0, 768, 490), amp=8)
    once = lambda t: math.sin(math.pi * min(max((t - 0.4) / 2.2, 0), 1)) ** 2  # 0.4〜2.6秒に1回だけ
    write("py-cut05.mp4", lambda t: steam(still, t, once(t)), 3)
    write("py-cut06.mp4", lambda t: steam(still, t, 0.35), 4)

def cut07():
    """カット7(3秒): ぬめの寄り。触角が倒れたまま揺れる。湯気は映らない。"""
    box = (0, 520, 330, 520 + round(330 * H / W))
    bg = bg_crop(EVENING, box)

    def f(t):
        c = bg.copy()
        # 寄りなので揺れは小さめ。周期も少し長くして、元気なく見せる
        put_nume(c, nume_at(sway(t, amp=2, period=2.0)), 330, cx=430, foot_y=1000, ratio=0.75)
        return c
    write("py-cut07.mp4", f, 3)

if __name__ == "__main__":
    cuts = {"1": cut01, "4": cut04, "5": cut05_06, "6": cut05_06, "7": cut07}
    done = set()
    for k in sys.argv[1:] or ["1", "4", "5", "7"]:
        if cuts[k] not in done:
            cuts[k]()
            done.add(cuts[k])
