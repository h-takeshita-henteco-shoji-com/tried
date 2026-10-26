"""YouTube のサムネイル(1280x720)を作る(#106。#98 の thumbnail.py を流用)。

2つの運営の任期の終わりの画面を左右に並べ、名前と、それぞれが勝った数字、題、ぬめとどんを重ねる。
画面は各録画の終わりから20秒前のコマを、ゲームの画面だけ切り出して使う。

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
# それぞれが勝った数字。基準の市長はお金、AI市役所は品物が届かない店(困りごと)
LINE1 = {"base": "AI 1人", "council": "AI 11人"}
NUM = {"base": "お金 268万", "council": "困りごと 3分の1"}
NUM_COLOR = {"base": (255, 225, 90), "council": (255, 225, 90)}
COLOR = {"base": (110, 110, 110), "council": (33, 170, 120)}
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"
FILES = {"base": B.B2, "council": B.C[12]}


def frame(m):
    p = f"{B.WORK}/thumb-{m}.png"
    path = f"{B.REC}/{FILES[m]}"
    t = B.rec_len(path) - 20
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.1f}", "-i", path,
                    "-frames:v", "1", "-vf", B.CROP, p], check=True)
    return Image.open(p).convert("RGB")


def main():
    im = Image.new("RGB", (W, H))
    cw, ch = W // 2, H
    d = ImageDraw.Draw(im)
    for i, m in enumerate(B.NAMES):
        f = frame(m)
        # 左上のパネルと下のツールバーを避けて、真ん中寄りの街を切る
        fw, fh = f.size
        bh = int(fh * 0.72)
        bw = int(bh * cw / ch)
        y1 = int(fh * 0.87)
        x0 = (fw - bw) // 2 + 320
        c = f.crop((x0, y1 - bh, x0 + bw, y1)).resize((cw, ch), Image.LANCZOS)
        c = ImageEnhance.Brightness(c).enhance(0.9)
        x = i * cw
        im.paste(c, (x, 0))
        tx, ty = x + 28, 26
        fnt = ImageFont.truetype(FONT, 40)
        name = f"{B.NAMES[m]}({LINE1[m]})"
        nw = d.textlength(name, font=fnt)
        d.rounded_rectangle((tx - 12, ty - 4, tx + nw + 12, ty + 54), 10, fill=COLOR[m])
        d.text((tx, ty), name, font=fnt, fill=(255, 255, 255))
        fnt = ImageFont.truetype(FONT, 58)
        d.text((tx, ty + 64), NUM[m], font=fnt, fill=NUM_COLOR[m], stroke_width=7, stroke_fill=(0, 0, 0))
    # 真ん中の帯に題
    band = Image.new("RGBA", (W, 230), (20, 24, 32, 225))
    im.paste(band, (0, H // 2 - 115), band)
    tag = "【Cities: Skylines】"
    title = "AI市長 vs AI市役所"
    sub = "同じ17.9万人の福岡を、1年ずつ任せたら"
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
