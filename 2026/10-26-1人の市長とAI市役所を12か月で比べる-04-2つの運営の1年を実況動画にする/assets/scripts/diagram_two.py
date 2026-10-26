"""2つの運営を並べた図を作る(#106 の場面6・7)。見た目は #100 の diagram-*.png にそろえる。

使い方: uv run --with pillow python assets/scripts/diagram_two.py
出力: assets/diagram-two.png
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "diagram-two.png"
W, H = 1520, 926
BG = (250, 250, 248)
CARD = (240, 239, 236)
INK = (30, 30, 30)
SUB = (95, 95, 95)
GRAY = (110, 110, 110)
ORANGE = (234, 106, 50)
GREEN = (33, 170, 120)
PURPLE = (75, 60, 160)
BLUE = (60, 120, 200)
FB = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FR = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"


def f(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def box(d, x0, y0, x1, y1, color, who, lines):
    d.rounded_rectangle([x0, y0, x1, y1], 12, fill=CARD)
    d.rectangle([x0, y0, x0 + 8, y1], fill=color)
    d.text((x0 + 26, y0 + 14), who, font=f(26, True), fill=color)
    for i, t in enumerate(lines):
        d.text((x0 + 26, y0 + 54 + i * 32), t, font=f(22), fill=INK)


def main():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((W // 2, 34), "同じ街を、2つのやり方で12か月", font=f(40, True), fill=INK, anchor="mt")
    d.text((W // 2, 90), "約束(公約)は同じ3つ。人口を毎月増やす、電気・水・下水を切らさない、赤字を続けない",
           font=f(22), fill=SUB, anchor="mt")
    # 左: 基準の市長
    lx = 60
    d.text((lx + 300, 150), "基準の市長(AI 1人)", font=f(32, True), fill=GRAY, anchor="mt")
    box(d, lx, 210, lx + 600, 410, GRAY, "1人で全部やる",
        ["街を見る", "施策を3件まで選んで、打つ", "翌月に、予想が当たったかを確かめる"])
    d.text((lx + 300, 450), "性格は持たせず、決まった手順だけで動く", font=f(22), fill=SUB, anchor="mt")
    # 右: AI市役所
    rx = 760
    d.text((rx + 350, 150), "AI市役所(AI 11人)", font=f(32, True), fill=GREEN, anchor="mt")
    rows = [
        (PURPLE, "見てまとめる市長", "街を見て重点を決め、局の案から3件まで選ぶ"),
        (ORANGE, "財政局", "使えるお金の枠を書き、案の費用を確かめる"),
        (GREEN, "7つの局", "担当の数字のために、案を1件ずつ出す"),
        (BLUE, "議会", "取り壊し・予算・税の議案だけを確かめる"),
        (PURPLE, "実行する市長", "選ばれた案を打つ。街を動かすのはここだけ"),
    ]
    y = 205
    for c, who, what in rows:
        d.rounded_rectangle([rx, y, rx + 700, y + 92], 10, fill=CARD)
        d.rectangle([rx, y, rx + 8, y + 92], fill=c)
        d.text((rx + 26, y + 12), who, font=f(24, True), fill=c)
        d.text((rx + 26, y + 52), what, font=f(21), fill=INK)
        y += 104
    d.text((rx + 350, y + 10), "7つの局: 住宅都市みどり、道路下水道、港湾空港、", font=f(20), fill=SUB, anchor="mt")
    d.text((rx + 350, y + 40), "経済観光文化、保健環境、教育委員会、消防", font=f(20), fill=SUB, anchor="mt")
    d.text((rx + 350, y + 74), "どのAIも subagent。市の計画(福岡市の基本計画をまねた目標)も読む", font=f(20), fill=SUB,
           anchor="mt")
    im.save(OUT)


if __name__ == "__main__":
    main()
