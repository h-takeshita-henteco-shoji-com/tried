"""へんロボの動画のタイトル画面を作る(#132)。同じ絵を、動画の先頭と YouTube のサムネイルに使う。

#106 の thumbnail.py にならい、太い文字の題と、キャラクター（へんロボ）を重ねる。
背景は、図面を暗くしたもの。へんロボは眼鏡を光らせる。
題の文言と背景の図面は、その日のフォルダの henrobo_scenes.py の THUMB に書く。

使い方: ~/.venvs/tried-audio/bin/python thumbnail.py <その日のフォルダ>
出力: <その日のフォルダ>/assets/thumbnail.jpg（1280x720）
"""
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import face  # noqa: E402

CHAR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる/assets/charactor/henrobo-front.png"))

FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"


def title_image(thumb, w=1920, h=1080):
    s = w / 1920
    bg = Image.open(thumb["background"]).convert("RGB")
    # 図面の一部を、画面の比に合わせて切る。crop は図面の幅に対する (左, 上, 幅) の割合
    fx, fy, fw = thumb["crop"]
    bw = int(bg.width * fw)
    bh = int(bw * h / w)
    x0, y0 = int(bg.width * fx), int(bg.height * fy)
    bg = bg.crop((x0, y0, x0 + bw, y0 + bh))
    bg = ImageEnhance.Brightness(bg.resize((w, h), Image.LANCZOS)).enhance(0.55)
    im = bg.copy()
    shade = Image.new("RGBA", (w, h), (20, 24, 32, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(w):  # 左ほど暗くして、題を読みやすくする
        sd.line((x, 0, x, h), fill=(20, 24, 32, int(235 - 120 * x / w)))
    im.paste(shade, (0, 0), shade)
    d = ImageDraw.Draw(im)
    x, y = int(90 * s), int(150 * s)
    for text, size, color, gap in ((thumb["tag"], 64, (170, 210, 255), 40), (thumb["title"][0], 150, (255, 255, 255), 30),
                                   (thumb["title"][1], 128, (255, 255, 255), 70), (thumb["sub"], 92, (255, 214, 80), 0)):
        f = ImageFont.truetype(FONT, int(size * s))
        d.text((x, y), text, font=f, fill=color, stroke_width=int(8 * s), stroke_fill=(0, 0, 0))
        y += int((size + gap) * s * 1.15)
    base = Image.open(CHAR).convert("RGBA")
    ch = face.glint(base, 0.5)
    ch_h = int(h * 0.62)
    ch = ch.resize((int(ch.width * ch_h / ch.height), ch_h), Image.LANCZOS)
    im.paste(ch, (w - ch.width - int(40 * s), h - ch_h - int(10 * s)), ch)
    return im


def main():
    import build_video as B  # build_video が thumbnail を読むので、ここで読む
    B.configure(sys.argv[1])
    out = f"{B.A}/thumbnail.jpg"
    title_image(B.THUMB, 1280, 720).save(out, quality=92)
    print(out, os.path.getsize(out))


if __name__ == "__main__":
    main()
