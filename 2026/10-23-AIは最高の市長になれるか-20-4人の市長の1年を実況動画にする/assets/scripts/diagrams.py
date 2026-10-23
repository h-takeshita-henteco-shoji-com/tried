"""場面3で Mod、MCP、subagent を説明する図を作る(#98)。

図は台詞に合わせて少しずつ組み上がるよう、段階ごとに1枚ずつ書き出す。
見た目は #90 の chart-mayors.png(明るい地、薄い灰色の箱、上に色の帯)にそろえる。
大きさは動画の映像の枠(1520x926)と同じ。

使い方: ~/.venvs/tried-audio/bin/python diagrams.py
出力: assets/diagram-mcp-1〜3.png、assets/diagram-subagent-1〜2.png、assets/diagram-mayors.png

diagram-mayors.png は #90 の chart-mayors.png と同じ中身で、「追う」を「重視する」、「捨てる」を「軽視する」に言い換えた。
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
W, H = 1520, 926
BG = (250, 250, 248)
CARD = (240, 239, 236)
INK = (30, 30, 30)
SUB = (95, 95, 95)
GRAY = (110, 110, 110)
ORANGE = (234, 106, 50)
GREEN = (33, 170, 120)
PURPLE = (75, 60, 160)
FONT_B = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_R = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"


def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def center_text(d, cx, y, text, font, fill=INK):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)


def card(d, box, title, lines=(), color=GRAY, title_size=40):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 18, fill=CARD)
    d.rectangle((x0, y0, x1, y0 + 14), fill=color)
    cx = (x0 + x1) / 2
    center_text(d, cx, y0 + 40, title, f(title_size, True))
    y = y0 + 40 + title_size + 24
    for t in lines:
        center_text(d, cx, y, t, f(28), SUB)
        y += 44


def arrow(d, p, q, label="", color=INK, label_above=True):
    (x0, y0), (x1, y1) = p, q
    d.line((x0, y0, x1, y1), fill=color, width=6)
    # 矢じり
    import math
    a = math.atan2(y1 - y0, x1 - x0)
    s = 22
    pts = [(x1, y1), (x1 - s * math.cos(a - 0.45), y1 - s * math.sin(a - 0.45)),
           (x1 - s * math.cos(a + 0.45), y1 - s * math.sin(a + 0.45))]
    d.polygon(pts, fill=color)
    if label:
        fnt = f(26)
        w = d.textlength(label, font=fnt)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        if abs(y1 - y0) > abs(x1 - x0):  # 縦の矢印は右に添える
            d.text((mx + 20, my - 16), label, font=fnt, fill=color)
        else:
            d.text((mx - w / 2, my - 46 if label_above else my + 12), label, font=fnt, fill=color)


def title(d, text, sub=""):
    center_text(d, W / 2, 46, text, f(46, True))
    if sub:
        center_text(d, W / 2, 112, sub, f(30), SUB)


def chip(d, box, text, color):
    d.rounded_rectangle(box, 12, fill=(255, 255, 255), outline=color, width=3)
    x0, y0, x1, y1 = box
    center_text(d, (x0 + x1) / 2, y0 + (y1 - y0 - 28) / 2 - 4, text, f(28), INK)


def mcp(step):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    AI = (60, 240, 400, 700)
    MID = (590, 240, 930, 700)
    GAME = (1120, 240, 1460, 700)
    if step == 1:
        title(d, "AIは、そのままではゲームを操作できない")
    elif step == 2:
        title(d, "Mod:ゲームに足す改造部品", "ゲームの中に、外からの頼みごとを聞く窓口を作った")
    else:
        title(d, "MCP:AIに道具を使わせる決まった形", "AIが道具を呼ぶと、Modの窓口に頼みごとが届く")
    card(d, AI, "AI", ["Claude"], PURPLE, 48)
    card(d, GAME, "ゲーム", ["Cities: Skylines"], GREEN, 48)
    if step >= 2:
        mod = (GAME[0] + 30, 470, GAME[2] - 30, 660)
        d.rounded_rectangle(mod, 14, fill=(255, 255, 255), outline=ORANGE, width=5)
        center_text(d, (mod[0] + mod[2]) / 2, mod[1] + 30, "Modの窓口", f(36, True), ORANGE)
        center_text(d, (mod[0] + mod[2]) / 2, mod[1] + 92, "頼みごとを聞いて", f(26), SUB)
        center_text(d, (mod[0] + mod[2]) / 2, mod[1] + 130, "ゲームを動かす", f(26), SUB)
    if step < 3:
        center_text(d, (MID[0] + MID[2]) / 2, 340, "?", f(200, True), (200, 200, 196))
    else:
        card(d, MID, "MCP", [], ORANGE, 48)
        tools = ["街の数字を見る", "道を引く", "建物を置く", "税を変える"]
        for i, t in enumerate(tools):
            y = MID[1] + 140 + i * 74
            chip(d, (MID[0] + 40, y, MID[2] - 40, y + 58), t, ORANGE)
        arrow(d, (AI[2] + 10, 400), (MID[0] - 10, 400), "道具を呼ぶ")
        arrow(d, (MID[2] + 10, 540), (GAME[0] + 20, 540), "頼む")
        arrow(d, (GAME[0] + 20, 620), (MID[2] + 10, 620), "結果を返す", label_above=False)
        arrow(d, (MID[0] - 10, 620), (AI[2] + 10, 620), "結果", label_above=False)
    # 下の帯に、ここまでに出た言葉をまとめる
    y = 760
    if step >= 2:
        d.text((90, y), "Mod", font=f(34, True), fill=ORANGE)
        d.text((250, y), "ゲームに足す改造部品", font=f(34), fill=INK)
    if step >= 3:
        d.text((90, y + 64), "MCP", font=f(34, True), fill=ORANGE)
        d.text((250, y + 64), "AIに道具を使わせるための、決まった形", font=f(34), fill=INK)
    return im


def subagent(step):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    if step == 1:
        title(d, "subagent:親のAIから呼び出される、役割を持った別のAI")
        parent = (330, 170, 830, 330)
        card(d, parent, "親のAI", ["Claude Code"], PURPLE, 42)
        child = (330, 460, 830, 700)
        card(d, child, "subagent", ["役:市長", "MCPの道具で街を動かす"], ORANGE, 42)
        arrow(d, (580, 340), (580, 450), "呼び出す")
        memo = (1060, 470, 1380, 690)
        d.rounded_rectangle(memo, 10, fill=(255, 255, 255), outline=GRAY, width=3)
        center_text(d, (memo[0] + memo[2]) / 2, memo[1] + 24, "最初に読ませる", f(28, True))
        center_text(d, (memo[0] + memo[2]) / 2, memo[1] + 66, "指示の文", f(28, True))
        for i in range(3):
            y = memo[1] + 128 + i * 24
            d.line((memo[0] + 40, y, memo[2] - 40 - i * 40, y), fill=(190, 190, 186), width=6)
        arrow(d, (memo[0] - 10, 580), (child[2] + 10, 580), "役割を決める", GRAY)
        d.text((90, 790), "subagent", font=f(34, True), fill=ORANGE)
        d.text((290, 790), "親のAIから呼び出される、役割を持った別のAI", font=f(34), fill=INK)
    else:
        title(d, "毎回あたらしいsubagentを呼び、ノートで引き継ぐ",
              "subagentが覚えていられることの量には、限りがあるため")
        parent = (560, 180, 960, 300)
        card(d, parent, "親のAI", [], PURPLE, 42)
        xs = [70, 590, 1110]
        for i, x in enumerate(xs):
            box = (x, 470, x + 340, 650)
            card(d, box, f"subagent {i + 1}", [f"{i + 1}回目の市長"], ORANGE, 38)
            arrow(d, (760 + (x + 170 - 760) * 0.55, 310), (x + 170, 460), "呼び出す" if i == 1 else "")
        for i in range(2):
            nx = xs[i] + 340 + 20
            note = (nx + 20, 515, nx + 140, 605)
            d.rounded_rectangle(note, 8, fill=(255, 255, 255), outline=GREEN, width=4)
            center_text(d, (note[0] + note[2]) / 2, note[1] + 26, "ノート", f(28, True), GREEN)
            arrow(d, (nx - 16, 560), (note[0] - 4, 560), "", GREEN)
            arrow(d, (note[2] + 4, 560), (xs[i + 1] - 10, 560), "", GREEN)
        center_text(d, W / 2, 700, "前のsubagentが書いたノートを読んで、続きを運営する", f(32), GREEN)
        d.text((90, 800), "育てたときは半年ずつ、4人の市長は1か月ずつ任せた", font=f(32), fill=SUB)
    return im


MAYORS = [
    ("基準の市長", GRAY, "人口、電気・水・下水、赤字にしない", "なし", "決まりなし(性格なし)"),
    ("お金市長", ORANGE, "週の黒字4万、働き口5万5千、所持金", "幸福度と健康、公園・病院・学校", "週の収支が多く増えるほう"),
    ("人口市長", GREEN, "人口13万、住宅の需要、毎月の人口増", "黒字の幅、渋滞、汚染(借金も可)", "家が多く建つほう"),
    ("住みやす市長", PURPLE, "幸福度90、健康80、汚染・騒音・ごみ0", "人口と働き口、工場と貨物港", "困りごとが多く減るほう"),
]


def mayors():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    cw, ch, gap, top = 700, 400, 40, 40
    x0 = (W - cw * 2 - gap) // 2
    for i, (name, color, keep, drop, tie) in enumerate(MAYORS):
        x = x0 + (i % 2) * (cw + gap)
        y = top + (i // 2) * (ch + gap)
        d.rounded_rectangle((x, y, x + cw, y + ch), 18, fill=CARD)
        d.rectangle((x, y, x + cw, y + 16), fill=color)
        d.text((x + 40, y + 52), name, font=f(44, True), fill=INK)
        d.text((x + 40, y + 150), f"重視する: {keep}", font=f(28), fill=INK)
        d.text((x + 40, y + 228), f"軽視する: {drop}", font=f(28), fill=SUB)
        d.text((x + 40, y + 306), f"迷ったとき: {tie}", font=f(28), fill=SUB)
    return im


def main():
    mayors().save(f"{OUT}/diagram-mayors.png")
    for s in (1, 2, 3):
        mcp(s).save(f"{OUT}/diagram-mcp-{s}.png")
    for s in (1, 2):
        subagent(s).save(f"{OUT}/diagram-subagent-{s}.png")
    print("ok")


if __name__ == "__main__":
    main()
