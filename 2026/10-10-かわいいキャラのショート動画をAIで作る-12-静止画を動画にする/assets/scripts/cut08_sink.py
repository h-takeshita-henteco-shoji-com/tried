"""カット8: どんが口を少し開きかけて閉じ、鼻を湯に沈める(4秒)。AIを使わず、層を動かして作る。

構図はカット5(#19 の py-cut05.png)と同じ寄りから始める。
- 口: もとの横線を鼻の色で消し、黒い縁の楕円を描く。高さを 0→最大→0 と変える。
- 沈む: どんの層を下へずらし、水面より下を透明にする。目は水面の上に残す。
- 波紋: カット5と同じ弧3本に、沈む間だけ外へ広がる弧を足す。
#19 の assets を作業場所にして実行する(compose.py と素材を使うため)。
"""
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

S19 = Path(__file__).resolve().parents[3] / "10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets"
OUT = Path(__file__).resolve().parents[1] / "generated"
sys.path.insert(0, str(S19 / "work"))
os.chdir(S19)
from compose import bg_crop, H, W  # noqa: E402

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FPS, SEC = 24, 4
HEAD_H, CX, WATER_Y = 560, 384, 1080  # カット5と同じ
MOUTH = (258, 359)        # don-front.png での口の中心
MOUTH_W, MOUTH_H = 46, 24  # 開いた口の大きさ(元の絵の px)。「少し」なので小さめ
MUZZLE = (142, 120, 96)    # 鼻(口の周り)の色
SINK = 215                 # 沈む量(画面の px)。鼻の穴が水面の下に入り、目は残る。170では鼻の穴が出たまま、230では目が水面に付いた

def ease(t):
    t = min(max(t, 0), 1)
    return t * t * (3 - 2 * t)

def mouth_open(t):
    """口の開き 0〜1。0.5秒で開き、0.5秒止め、0.4秒で閉じる。"""
    if t < 0.5:
        return 0
    if t < 1.0:
        return ease((t - 0.5) / 0.5)
    if t < 1.5:
        return 1
    return 1 - ease((t - 1.5) / 0.4)

def sink(t):
    """沈んだ量 0〜1。閉じてから少し間を置き、2.3〜3.3秒で沈む。"""
    return ease((t - 2.3) / 1.0)

def don_with_mouth(don, k):
    d = don.copy()
    if k <= 0:
        return d
    dr = ImageDraw.Draw(d)
    mx, my = MOUTH
    dr.rectangle([mx - 26, my - 6, mx + 26, my + 6], fill=MUZZLE + (255,))
    h = max(3, MOUTH_H * k)
    w = MOUTH_W * (0.7 + 0.3 * k)
    dr.ellipse([mx - w / 2, my - h / 2, mx + w / 2, my + h / 2],
               fill=(70, 45, 40, 255), outline=(0, 0, 0, 255), width=6)
    return d

def frame(bg, don, t):
    k, s = mouth_open(t), sink(t)
    d = don_with_mouth(don, k)
    r = HEAD_H / d.height
    d = d.resize((round(d.width * r), HEAD_H), Image.LANCZOS)
    layer = Image.new("RGBA", (W, H))
    x = round(CX - d.width / 2)
    layer.alpha_composite(d, (x, WATER_Y - HEAD_H + round(SINK * s)))
    # 水面より下は見せない
    a = layer.getchannel("A")
    ImageDraw.Draw(a).rectangle([0, WATER_Y, W, H], fill=0)
    layer.putalpha(a)
    c = bg.copy()
    c.alpha_composite(layer)
    dr = ImageDraw.Draw(c)
    cx = x + d.width / 2
    lw = max(2, round(d.width / 120))
    for i, (kk, hh) in enumerate([(1.05, 24), (1.3, 40), (1.55, 58)]):
        w2 = d.width * kk / 2
        dr.arc([cx - w2, WATER_Y - hh / 2, cx + w2, WATER_Y + hh / 2], 10, 170,
               fill=(225, 240, 248, 255 - i * 60), width=lw)
    # 沈む間だけ、外へ広がって消える弧
    if 0 < s < 1 or 3.3 <= t < 3.8:
        p = min(1, (t - 2.3) / 1.5)
        w2 = d.width * (1.6 + 0.6 * p) / 2
        hh = 60 + 40 * p
        dr.arc([cx - w2, WATER_Y - hh / 2, cx + w2, WATER_Y + hh / 2], 10, 170,
               fill=(225, 240, 248, round(200 * (1 - p))), width=lw)
    return c.convert("RGB")

if __name__ == "__main__":
    bg = bg_crop("input/bg-c1-evening.jpeg", (330, 560, 768, 560 + round(438 * H / W)))
    don = Image.open("work/don-front.png")
    out = OUT / "py-cut08.mp4"
    p = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    for n in range(FPS * SEC):
        f = frame(bg, don, n / FPS)
        p.stdin.write(f.tobytes())
        if n in (0, 24, 60, 96 - 1):
            f.save(OUT.parent / "work" / f"py-cut08-f{n:02d}.png")
    p.stdin.close()
    p.wait()
    print(out)
