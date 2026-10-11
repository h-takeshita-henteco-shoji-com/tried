"""カット2(3秒): ぬめが口を管のように伸ばし、湯を3回飲んで、口を戻す。AIを使わない。

絵コンテの「葉の裏を3回なめる」を、10-11 に本人の指示で「口をストローのように伸ばして3回飲む」に変えた。
管の形は cut02_straw.py と同じ(通り道、根元ほど太い、顔の内側は縁なし)。長さと太さを時間で変える。
- 0〜0.6秒: 管が伸びる。伸び始めは根元も細く、口の横線からふくらんで見せる。先が湯に付くと波紋。
- 0.6〜2.4秒: 3回飲む。1回ごとに、ふくらみが先から根元へ上り、先の波紋が広がる。
- 2.4〜3.0秒: 管が縮み、口の横線に戻る。
"""
import math
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cut02_straw import BODY, LINE, P0, P1, P2, RIPPLE, S19, SS, TUBE_ROOT, TUBE_TIP, bezier, face_mask  # noqa: E402

OUT = Path(__file__).resolve().parents[1]
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FPS, SEC = 24, 3
EXTEND, SIPS_END = 0.6, 2.4
SIP = (SIPS_END - EXTEND) / 3
REGION = (360, 980, 560, 1120)  # 管の描かれる範囲。ここだけ4倍で描いて速くする

def ease(t):
    t = min(max(t, 0), 1)
    return t * t * (3 - 2 * t)

def length(t):
    """管の長さ 0〜1。"""
    if t < EXTEND:
        return ease(t / EXTEND)
    if t < SIPS_END:
        return 1
    return 1 - ease((t - SIPS_END) / (SEC - SIPS_END))

def sip(t):
    """飲んでいる1回の中の進み 0〜1。飲んでいない時は None。"""
    if EXTEND <= t < SIPS_END:
        return ((t - EXTEND) % SIP) / SIP
    return None

def frame(base, inside, t):
    L = length(t)
    s = sip(t)
    if L <= 0.01:
        return base
    path = bezier(P0, P1, P2)
    n = len(path) - 1
    k = max(1, round(n * L))
    grow = min(1, L / 0.3)  # 伸び始めは根元も細い
    width = []
    for i in range(k + 1):
        u = i / n
        w = (TUBE_ROOT + (TUBE_TIP - TUBE_ROOT) * u ** 0.7) * grow
        if s is not None:  # ふくらみが先(u=1)から根元(u=0)へ上る
            w += 4 * math.exp(-((u - (1 - s)) / 0.07) ** 2)
        width.append(max(w, 1.5))
    x0, y0, x1, y1 = REGION
    crop = base.crop(REGION).convert("RGBA")
    big = crop.resize((crop.width * SS, crop.height * SS), Image.LANCZOS)
    layer = Image.new("RGBA", big.size)
    d = ImageDraw.Draw(layer)
    pts = [((x - x0) * SS, (y - y0) * SS) for x, y in path[:k + 1]]
    for (x, y), (px, py), w in zip(pts, path, width):
        if inside[round(py), round(px)]:
            continue
        r = (w + 2 * LINE) * SS / 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=(0, 0, 0, 255))
    for (x, y), w in zip(pts, width):
        r = w * SS / 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=BODY + (255,))
    # 先が湯に付いている間の波紋。飲むたびに広がる
    if L > 0.97:
        ex, ey = pts[-1]
        grow_r = 0 if s is None else s
        for i, (w, h) in enumerate([(14, 4), (24, 7)]):
            k2 = 1 + 0.5 * grow_r
            a = round((230 - i * 70) * (1 - 0.6 * grow_r))
            d.arc([ex - w * k2 * SS, ey - h * k2 * SS + 2 * SS, ex + w * k2 * SS, ey + h * k2 * SS + 2 * SS],
                  10, 170, fill=RIPPLE + (a,), width=round(1.8 * SS))
    big.alpha_composite(layer)
    out = base.copy()
    out.paste(big.resize(crop.size, Image.LANCZOS).convert("RGB"), (x0, y0))
    return out

if __name__ == "__main__":
    base = Image.open(S19 / "generated/py-cut02.png").convert("RGB")
    inside = face_mask(base)
    p = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{base.width}x{base.height}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", str(OUT / "generated/py-cut02.mp4")],
                         stdin=subprocess.PIPE)
    keep = {0: "00", 7: "07", 14: "14", 22: "22", 30: "30", 64: "64", 66: "66", 71: "71"}
    for n in range(FPS * SEC):
        f = frame(base, inside, n / FPS)
        p.stdin.write(f.tobytes())
        if n in keep:
            f.crop((330, 950, 530, 1110)).save(f"/tmp/c2d_{keep[n]}.png")
    p.stdin.close()
    p.wait()
    print(OUT / "generated/py-cut02.mp4")
