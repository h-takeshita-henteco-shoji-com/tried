"""YouTube のサムネイル(1280x720)を作る(#98)。

4人の任期の終わりの画面を2x2に並べ、市長の名前と人口、題、ぬめとどんを重ねる。
画面は各録画の終わりから20秒前のコマを、ゲームの窓だけ切り出して使う。

使い方: ~/.venvs/tried-audio/bin/python thumbnail.py
出力: assets/thumbnail.jpg
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_video as B  # noqa: E402

W, H = 1280, 720
POP = {"base": "10.7万人", "money": "5.7万人", "population": "11.6万人", "livable": "10.7万人"}
# 1人だけ人口が半分になったお金市長の数字を、赤で目立たせる(ポップアウト)
NUM_COLOR = {"base": (255, 225, 90), "money": (255, 80, 70), "population": (255, 225, 90), "livable": (255, 225, 90)}
COLOR = {"base": (110, 110, 110), "money": (234, 106, 50), "population": (33, 170, 120), "livable": (75, 60, 160)}
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"


def frame(m):
    p = f"{B.WORK}/thumb-{m}.png"
    t = B.rec_len(m) - 20
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.1f}", "-i", f"{B.REC}/{m}/{m}-full.mp4",
                    "-frames:v", "1", "-vf", B.CROP, p], check=True)
    return Image.open(p).convert("RGB")


def main():
    im = Image.new("RGB", (W, H))
    cw, ch = W // 2, H // 2
    d = ImageDraw.Draw(im)
    for i, m in enumerate(B.MAYORS):
        f = frame(m)
        # 左上のパネルと下のツールバーを避けて、真ん中寄りの街を切る
        fw, fh = f.size
        bh = int(fh * 0.40)
        bw = int(bh * cw / ch)
        y1 = int(fh * 0.89)
        x0 = (fw - bw) // 2 - 100
        box = (x0, y1 - bh, x0 + bw, y1)
        c = f.crop(box).resize((cw, ch), Image.LANCZOS)
        c = ImageEnhance.Brightness(c).enhance(0.9)
        x, y = (i % 2) * cw, (i // 2) * ch
        im.paste(c, (x, y))
        # 上の段は枠の上、下の段は枠の下に名前を置き、真ん中の題の帯と重ねない
        ty = y + 22 if i < 2 else y + ch - 136
        # 下の段は、隅のぬめとどんを避けて内側に寄せる
        if i < 2:
            tx = x + 20 if i % 2 == 0 else x + cw - 20 - 300
        else:
            tx = x + cw - 20 - 300 if i % 2 == 0 else x + 20
        # 名前は市長の色の札に白で書き、動画の中の図と色を結びつける
        fnt = ImageFont.truetype(FONT, 38)
        nw = d.textlength(B.NAMES[m], font=fnt)
        d.rounded_rectangle((tx - 12, ty - 4, tx + nw + 12, ty + 50), 10, fill=COLOR[m])
        d.text((tx, ty), B.NAMES[m], font=fnt, fill=(255, 255, 255))
        fnt = ImageFont.truetype(FONT, 58)
        d.text((tx, ty + 56), POP[m], font=fnt, fill=NUM_COLOR[m], stroke_width=7, stroke_fill=(0, 0, 0))
    # 真ん中の帯に題
    band = Image.new("RGBA", (W, 230), (20, 24, 32, 225))
    im.paste(band, (0, H // 2 - 115), band)
    tag = "【Cities: Skylines】"
    title = "AI市長4人に福岡を任せたら"
    sub = "同じ10万人の街が、1年でこう分かれた"
    for text, size, y, color in [(tag, 36, H // 2 - 106, (170, 210, 255)), (title, 84, H // 2 - 64, (255, 255, 255)),
                                 (sub, 38, H // 2 + 40, (235, 235, 235))]:
        fnt = ImageFont.truetype(FONT, size)
        tw = d.textlength(text, font=fnt)
        d.text(((W - tw) / 2, y), text, font=fnt, fill=color, stroke_width=4, stroke_fill=(0, 0, 0))
    for sp, (path, *_rest) in B.CHARS.items():
        c = Image.open(path).convert("RGBA")
        h = 210 if sp == "ぬめ" else 180
        c = c.resize((int(c.width * h / c.height), h), Image.LANCZOS)
        im.paste(c, (6 if sp == "ぬめ" else W - c.width - 6, H - h - 4), c)
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "thumbnail.jpg"))
    im.save(out, quality=92)
    print(out, os.path.getsize(out))


if __name__ == "__main__":
    main()
