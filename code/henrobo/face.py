"""へんロボの口パクと眼鏡のキラリを、立ち絵に描き足す(#132)。

- 口: 元の横線を顔の色で消し、楕円の口を4段階（0=元の線、1〜3=開いた口）で描く。
- キラリ: 右のレンズに、斜めの白い光の帯を通す。0〜1の進み具合で位置と濃さが変わる。

座標は henrobo-front.png（665x953）の上で測ったもの。
"""
from PIL import Image, ImageDraw, ImageFilter

FACE = (221, 108, 0, 255)       # 顔の橙色
LINE = (255, 250, 235, 255)     # 線の白
MOUTH_BOX = (262, 405, 368, 422)  # 元の口の線（少し広めに消す）
MOUTH_CENTER = (315, 414)
MOUTH_W = 100
MOUTH_H = [0, 14, 26, 38]        # 段階ごとの口の高さ（0は元の線のまま）
LENS_R = (362, 234, 500, 344)    # 右のレンズの内側
LENS_L = (148, 234, 286, 344)    # 左のレンズの内側


def mouth(base, level):
    if level == 0:
        return base.copy()
    im = base.copy()
    d = ImageDraw.Draw(im)
    d.rectangle(MOUTH_BOX, fill=FACE)
    cx, cy = MOUTH_CENTER
    h = MOUTH_H[level]
    w = MOUTH_W * (0.75 + 0.08 * level)
    d.ellipse((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=(90, 35, 10, 255), outline=LINE, width=5)
    return im


def glint(base, t, lens=LENS_R):
    """t は 0〜1。光の帯がレンズの左上から右下へ動き、中ほどでいちばん明るい。"""
    if t <= 0 or t >= 1:
        return base
    x0, y0, x1, y1 = lens
    w, h = x1 - x0, y1 - y0
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pos = -w + t * (2 * w + h)
    peak = 1 - abs(2 * t - 1)
    strength = int(255 * min(1, peak * 1.6))
    for off, width in ((0, 36), (52, 14)):
        p = pos + off
        d.polygon([(x0 + p, y0), (x0 + p + width, y0), (x0 + p + width - h, y1), (x0 + p - h, y1)],
                  fill=(255, 255, 255, strength))
    mask = Image.new("L", base.size, 0)
    ImageDraw.Draw(mask).rectangle(lens, fill=255)
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", base.size, 0), mask))
    layer = layer.filter(ImageFilter.GaussianBlur(1.2))
    out = base.copy()
    out.alpha_composite(layer)
    # いちばん明るいときに、レンズの右上に小さな星を光らせる
    if peak > 0.5:
        star = Image.new("RGBA", base.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(star)
        r = 34 * (peak - 0.5) * 2
        cx, cy = x1 - 6, y0 + 6
        sd.polygon([(cx, cy - r), (cx + r * 0.18, cy - r * 0.18), (cx + r, cy), (cx + r * 0.18, cy + r * 0.18),
                    (cx, cy + r), (cx - r * 0.18, cy + r * 0.18), (cx - r, cy), (cx - r * 0.18, cy - r * 0.18)],
                   fill=(255, 255, 240, 255))
        out.alpha_composite(star.filter(ImageFilter.GaussianBlur(0.8)))
    return out
