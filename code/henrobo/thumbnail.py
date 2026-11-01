"""#132 の動画のタイトル画面を作る。同じ絵を、動画の先頭と YouTube のサムネイルに使う。

#106 の thumbnail.py にならい、太い文字の題と、キャラクター（へんロボ）を重ねる。
背景は、1枚目の図面（扉や窓の形の一覧）を暗くしたもの。へんロボは眼鏡を光らせる。

使い方: ~/.venvs/tried-audio/bin/python thumbnail.py
出力: assets/thumbnail.jpg（1280x720）
"""
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import face  # noqa: E402

DAY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる"))
A = f"{DAY}/assets"
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"
TAG = "【AIと図面】"
TITLE = ("10のAIに", "建築の図面を読ませた")
SUB = "単純な図面ほど、つまずいた"


def title_image(w=1920, h=1080):
    s = w / 1920
    bg = Image.open(f"{A}/drawings/建築工事標準詳細図/001126048-p09.png").convert("RGB")
    # 図面の左上寄りを、画面の比に合わせて切る
    bw = int(bg.width * 0.62)
    bh = int(bw * h / w)
    bg = bg.crop((int(bg.width * 0.04), int(bg.height * 0.06), int(bg.width * 0.04) + bw, int(bg.height * 0.06) + bh))
    bg = ImageEnhance.Brightness(bg.resize((w, h), Image.LANCZOS)).enhance(0.55)
    im = bg.copy()
    shade = Image.new("RGBA", (w, h), (20, 24, 32, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(w):  # 左ほど暗くして、題を読みやすくする
        sd.line((x, 0, x, h), fill=(20, 24, 32, int(235 - 120 * x / w)))
    im.paste(shade, (0, 0), shade)
    d = ImageDraw.Draw(im)
    x, y = int(90 * s), int(150 * s)
    for text, size, color, gap in ((TAG, 64, (170, 210, 255), 40), (TITLE[0], 150, (255, 255, 255), 30),
                                   (TITLE[1], 128, (255, 255, 255), 70), (SUB, 92, (255, 214, 80), 0)):
        f = ImageFont.truetype(FONT, int(size * s))
        d.text((x, y), text, font=f, fill=color, stroke_width=int(8 * s), stroke_fill=(0, 0, 0))
        y += int((size + gap) * s * 1.15)
    base = Image.open(f"{A}/charactor/henrobo-front.png").convert("RGBA")
    ch = face.glint(base, 0.5)
    ch_h = int(h * 0.62)
    ch = ch.resize((int(ch.width * ch_h / ch.height), ch_h), Image.LANCZOS)
    im.paste(ch, (w - ch.width - int(40 * s), h - ch_h - int(10 * s)), ch)
    return im


def main():
    out = f"{A}/thumbnail.jpg"
    title_image(1280, 720).save(out, quality=92)
    print(out, os.path.getsize(out))


if __name__ == "__main__":
    main()
