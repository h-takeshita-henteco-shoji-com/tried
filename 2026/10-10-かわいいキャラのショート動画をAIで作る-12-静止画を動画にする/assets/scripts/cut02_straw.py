"""カット2: ぬめの口(目の下の横線)が、ストローのように伸びて湯を飲む絵。

Wan で舌が体の下から出て、地面の側をなめた(wan-cut02-1)。本人の指示で、口を管のように伸ばす形に変えた。
- 管は口の前の端から出て、顔の外へ伸び、右下へ曲がって湯に届く。
- 黒い縁と体の色で描く。縁の太さは #19 の仕上がり(約3px)にそろえる。
- 先が湯に入る所に、薄い波紋の弧を2本描く。
4倍の大きさで描いてから縮め、線のぎざぎざを消す。
太い線を引くと管の中に切れ目が出たため、通り道に沿って円を細かく並べて描く。
根元ほど太くする(管の中 12px → 先 5px)。
顔の内側(輪郭線を含む)では管の縁を描かない。管の中の色が顔の輪郭線も覆い、顔から枝分かれして生えた形になる。
元の口の線は、太い根元で隠れる。
10-11 本人の指示: もっと太く、根元ほど太く、顔との境目の線は消す。
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

S19 = Path(__file__).resolve().parents[3] / "10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets"
OUT = Path(__file__).resolve().parents[1] / "generated"
SS = 4                      # 描くときの倍率
BODY = (200, 191, 178)      # ぬめの体の色(py-cut02 から取った)
LINE = 3.1                  # 縁の太さ(px)
TUBE_ROOT, TUBE_TIP = 12.0, 5.0  # 管の中の太さ(px)。根元ほど太い
RIPPLE = (225, 240, 248)
# 管の通り道(2次ベジェ)。口の前の端 → 顔の外 → 湯の面
P0, P1, P2 = (410, 1022), (470, 1018), (494, 1076)

def bezier(p0, p1, p2, n=400):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in (i / n for i in range(n + 1))]

def face_mask(im, seed=(400, 1022), tol=30, line=4):
    """顔の内側。体の色の塗りを seed からたどり、輪郭線の分だけ広げる。"""
    a = np.asarray(im.convert("RGB")).astype(int)
    near = np.abs(a - np.array(BODY)).sum(axis=2) < tol
    lab, _ = ndimage.label(near)
    m = lab == lab[seed[1], seed[0]]
    return ndimage.binary_dilation(m, iterations=line)

def draw_straw(im):
    inside = face_mask(im)
    big = im.convert("RGBA").resize((im.width * SS, im.height * SS), Image.LANCZOS)
    layer = Image.new("RGBA", big.size)
    d = ImageDraw.Draw(layer)
    path = bezier(P0, P1, P2)
    n = len(path) - 1
    width = [TUBE_ROOT + (TUBE_TIP - TUBE_ROOT) * (i / n) ** 0.7 for i in range(n + 1)]
    pts = [(x * SS, y * SS) for x, y in path]
    # 縁: 顔の外だけ
    for (x, y), (px, py), w in zip(pts, path, width):
        if inside[round(py), round(px)]:
            continue
        r = (w + 2 * LINE) * SS / 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=(0, 0, 0, 255))
    # 管の中: 全部。顔の輪郭線も覆う
    for (x, y), w in zip(pts, width):
        r = w * SS / 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=BODY + (255,))
    ex, ey = pts[-1]
    # 湯に入る所の波紋
    for i, (w, h) in enumerate([(14, 4), (24, 7)]):
        d.arc([ex - w * SS, ey - h * SS + 2 * SS, ex + w * SS, ey + h * SS + 2 * SS], 10, 170,
              fill=RIPPLE + (230 - i * 70,), width=round(1.8 * SS))
    big.alpha_composite(layer)
    return big.resize(im.size, Image.LANCZOS).convert("RGB")

if __name__ == "__main__":
    src = Image.open(S19 / "generated/py-cut02.png")
    out = draw_straw(src)
    out.save(OUT / "py-cut02-straw.png")
    out.crop((330, 950, 530, 1110)).resize((800, 640), Image.LANCZOS).save(OUT.parent / "work/py-cut02-straw-zoom.png")
