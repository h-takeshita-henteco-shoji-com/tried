"""背景に切り抜いたキャラを置く。大きさは「どんの頭の高さ = ぬめの体の幅 x 1.5」で決める。

10-08 に3倍から1.5倍へ変えた。3倍では、カット4の引きでぬめが小さすぎた。
"""
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import sys
sys.path.insert(0, "work")
from antenna import tilt
from cutout import cutout

W, H = 768, 1376
NUME_BODY_W = 787  # nume-side.png の体の幅(px)
NUME_LINE_W = 12   # nume-side.png の輪郭線の太さ(px)
OUT_LINE_W = 3.1   # 仕上がりで揃えたい線の太さ(px)。どんの線に合わせる
RATIO = 1.5

def bg_crop(path, box):
    """背景の一部を切り出して 9:16 に拡大する(中くらいの引き用)。"""
    return Image.open(path).convert("RGBA").crop(box).resize((W, H), Image.LANCZOS)

def scaled(im, h=None, w=None):
    r = h / im.height if h else w / im.width
    return im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS), r

def night(layer):
    """夜の背景に合わせて、キャラの層を暗く青寄りにする。"""
    r, g, b, a = layer.split()
    r = r.point(lambda v: v * 0.50)
    g = g.point(lambda v: v * 0.58)
    b = b.point(lambda v: v * 0.85)
    return Image.merge("RGBA", (r, g, b, a))

def put_don(canvas, don, head_h, cx, water_y):
    """どんの頭を、水面 water_y に首から上だけ出して置く。"""
    d, _ = scaled(don, h=head_h)
    x = round(cx - d.width / 2)
    canvas.alpha_composite(d, (x, water_y - d.height))
    # 首のまわりの波紋。手前側だけ、弧を3本
    dr = ImageDraw.Draw(canvas)
    cx_ = x + d.width / 2
    for i, (k, hh) in enumerate([(1.05, 24), (1.3, 40), (1.55, 58)]):
        w2 = d.width * k / 2
        dr.arc([cx_ - w2, water_y - hh / 2, cx_ + w2, water_y + hh / 2], 10, 170,
               fill=(225, 240, 248, 255 - i * 60), width=max(2, round(d.width / 120)))

def thicken(im, size):
    """縮小で細くなる黒線を、先に太らせておく。外の輪郭も同じだけ広げる。"""
    rgb = im.convert("RGB").filter(ImageFilter.MinFilter(size))
    a = im.getchannel("A").filter(ImageFilter.MaxFilter(size))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(rgb, (0, 0), a)
    # 広げた外側は黒の輪郭にする
    edge = Image.new("RGBA", im.size, (0, 0, 0, 255))
    edge.putalpha(a)
    edge.alpha_composite(Image.composite(out, Image.new("RGBA", im.size), im.getchannel("A")))
    return edge

def leaf_front(bg):
    """左下のフキの葉(夜の色)を抜き出す。ぬめの上に葉を戻し、葉の下に入って見せる。"""
    import numpy as np
    from scipy import ndimage
    a = np.asarray(bg.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (g > r + 25) & (g > 70)
    m[:1100] = False
    m[:, 260:] = False
    m = ndimage.binary_dilation(m, iterations=4)
    return Image.fromarray((m * 255).astype(np.uint8))

def put_nume(canvas, nume, don_head_h, cx, foot_y, ratio=RATIO, mirror=False, rotate=0, shadow=True):
    """ぬめの体の幅を、どんの頭の高さの 1/ratio にして置く。mirror で右向き、rotate で鼻先を上げる。"""
    r = don_head_h / ratio / NUME_BODY_W
    # 縮めた後の線が OUT_LINE_W になるよう、先に太らせる(MinFilter は奇数のみ)
    grow = max(1, round(OUT_LINE_W / r - NUME_LINE_W))
    nume = thicken(nume, size=grow + 1 - grow % 2)
    n = nume.resize((round(nume.width * r), round(nume.height * r)), Image.LANCZOS)
    if mirror:
        n = ImageOps.mirror(n)
    if rotate:
        n = n.rotate(rotate, resample=Image.BICUBIC, expand=True)
    # 足元の影(石に置いた感じを出す)
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    bw = NUME_BODY_W * r
    ImageDraw.Draw(sh).ellipse([cx - bw * 0.55, foot_y - 6, cx + bw * 0.45, foot_y + 6], fill=(40, 35, 35, 90))
    if shadow:
        canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    # 体の中心が cx に来るように置く(前にはみ出た触角の分を足す)
    left = cx - n.width / 2 if rotate else (cx - bw / 2 if mirror else cx + bw / 2 - n.width)
    canvas.alpha_composite(n, (round(left), foot_y - n.height))

if __name__ == "__main__":
    don_front = Image.open("work/don-front.png")
    don_left = Image.open("work/don-left.png")
    nume_side = Image.open("work/nume-side.png")
    nume_fwd = tilt(nume_side, pivot=(240, 430), y0=388, deg=40, x_max=328)
    nume_fwd.save("work/nume-side-forward.png")

    # カット1: 夕方の引き。右下にどんの顔、石の上は空き。
    c = Image.open("input/bg-c1-evening.jpeg").convert("RGBA")
    put_don(c, don_front, head_h=230, cx=575, water_y=1160)
    c.convert("RGB").save("generated/py-cut01.png")

    # カット4: 中くらいの引き。左の石にぬめ(左向き、触角は前)、右の湯にどん。
    box = (130, 440, 630, 440 + round(500 * H / W))
    c = bg_crop("input/bg-c1-evening.jpeg", box)
    don_h = 330
    put_don(c, don_left, head_h=don_h, cx=560, water_y=1020)
    put_nume(c, nume_fwd, don_h, cx=263, foot_y=545)
    c.convert("RGB").save("generated/py-cut04.png")

    # カット2: フキの葉の端。ぬめが葉の下から手前へ出てくる。触角は前。
    # 葉と地面のすき間はぬめより狭く、葉の陰に入れると顔が隠れる。葉の手前に置く。
    c = Image.open("input/bg-c2-fuki.jpeg").convert("RGBA")
    put_nume(c, nume_fwd, 330, cx=330, foot_y=1090, ratio=1.3, mirror=True)
    c.convert("RGB").save("generated/py-cut02.png")

    # カット3: 縁の石に登りきった瞬間。触角をもう一段下げる。
    # 体を大きく傾けると跳んで見えたため、石の角に体を載せ、鼻先だけ少し上げる。
    nume_low = tilt(nume_side, pivot=(240, 430), y0=388, deg=70, x_max=328)
    box = (0, 665, 400, 665 + round(400 * H / W))
    c = bg_crop("input/bg-c1-evening.jpeg", box)
    put_nume(c, nume_low, 330, cx=260, foot_y=552, ratio=1.3, mirror=True, rotate=6, shadow=False)
    c.convert("RGB").save("generated/py-cut03.png")

    # カット5: どんの顔の寄り。湯気はもとの背景のまま。
    box = (330, 560, 768, 560 + round(438 * H / W))
    c = bg_crop("input/bg-c1-evening.jpeg", box)
    put_don(c, don_front, head_h=560, cx=384, water_y=1080)
    c.convert("RGB").save("generated/py-cut05.png")

    # カット6: 5と同じ絵。
    Image.open("generated/py-cut05.png").save("generated/py-cut06.png")

    # カット7: ぬめの寄り。真横で左(庭石の側)を向き、どんに背を向ける。触角は前に倒れたまま。
    # 背面で触角を縮める案は、横に開いた角に見えたため使わない。
    box = (0, 520, 330, 520 + round(330 * H / W))
    c = bg_crop("input/bg-c1-evening.jpeg", box)
    put_nume(c, nume_fwd, 330, cx=430, foot_y=1000, ratio=0.75)
    c.convert("RGB").save("generated/py-cut07.png")

    # カット8: どんの寄り。鼻を沈める直前。湯を口の高さまで上げ、鼻先だけ出す。
    don_sink = cutout(Image.open("input/don-bath-front.png"), crop_bottom=480)
    box = (330, 560, 768, 560 + round(438 * H / W))
    c = bg_crop("input/bg-c1-evening.jpeg", box)
    put_don(c, don_sink, head_h=round(don_sink.height * 560 / don_front.height), cx=384, water_y=1080)
    c.convert("RGB").save("generated/py-cut08.png")

    # カット9: 1と同じ引きの夜。2匹とも動かない。ぬめは石の上で庭石の側を向く。
    c = Image.open("input/bg-c9-night.jpeg").convert("RGBA")
    chars = Image.new("RGBA", c.size)
    put_don(chars, don_front, head_h=230, cx=575, water_y=1160)
    put_nume(chars, nume_fwd, 230, cx=250, foot_y=800)
    c.alpha_composite(night(chars))
    c.convert("RGB").save("generated/py-cut09.png")

    # カット10: ぬめは石を降り、フキの葉の下へ。どんは葉の方を向き、目は開けたまま。
    # ぬめは葉の手前(カメラ寄り)にいるため、比率より大きく 1.2 倍で描く。
    bg = Image.open("input/bg-c9-night.jpeg").convert("RGBA")
    c = bg.copy()
    chars = Image.new("RGBA", c.size)
    put_don(chars, don_left, head_h=230, cx=575, water_y=1160)
    put_nume(chars, nume_fwd, 230, cx=140, foot_y=1200, ratio=1.2, shadow=False)
    c.alpha_composite(night(chars))
    c.paste(bg, (0, 0), leaf_front(bg))
    c.convert("RGB").save("generated/py-cut10.png")
