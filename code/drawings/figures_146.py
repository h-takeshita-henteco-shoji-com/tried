"""#146 の記事に使う図を作る。

- compare-P-1-librecad.jpg: 課題1で各モデルが描いた平面詳細図を、LibreCAD で開いた画面で並べる
- fig-conditions-p1.png: 元の図面のどこを、どこに描かせたか
- fig-behavior-p1.png: 課題1で、モデルごとに描いたか、外壁の厚みの食い違いにどう応じたか
- fig-try1.png: 直す前の指示文で Opus が描いた図(範囲が窓の途中で切れている)
- fig-p2-cut.png: 課題2で Opus が描いた切断線 K1(MCP と DXF)

画面写真は code/librecad-mcp/shoot_136.py --day <その日のフォルダ> --task P-1 --window 54800,-11300,62000,-4600 で撮る。
寸法は LibreCAD が図面の設定から描き直すので、人が CAD で見る姿で比べる(#136 の学び)。

使い方: ~/.venvs/tried-audio/bin/python code/drawings/figures_146.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
DAY = REPO / "2026/11-06-AIと図面のコラボレーション-06-AIに平面詳細図を描かせる"
SHOT = DAY / "results/2026-11-06/librecad"
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
NAMES = {"claude-haiku-5-5": "Haiku 5.5", "claude-sonnet-5-5": "Sonnet 5.5", "claude-opus-5-5": "Opus 5.5",
         "claude-fable-5-1": "Fable 5.1", "gemini-3.8-flash": "Gemini 3.8 Flash", "gemini-4-argon": "Gemini 4 Argon"}


def label_cells(cells, out, cols, band=60, note=None):
    w = max(im.width for _, im in cells)
    h = max(im.height for _, im in cells)
    foot = 50 if note else 0
    sheet = Image.new("RGB", (w * cols, (h + band) * ((len(cells) + cols - 1) // cols) + foot), "white")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 28)
    for i, (t, im) in enumerate(cells):
        x, y = (i % cols) * w, (i // cols) * (h + band)
        d.text((x + 12, y + 14), t, font=f, fill=(30, 30, 30))
        sheet.paste(im, (x, y + band))
    if note:
        d.text((12, sheet.height - foot + 10), note, font=ImageFont.truetype(FONT_R, 22), fill=(110, 110, 110))
    sheet.save(out, quality=88)
    print(out)


FONT_R = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"


def conditions():
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    import figures_136 as f136
    view = (-3500, -26000, 64000, 11000)
    plan = (-300, -300, 4850, 4850)          # 元の平面図の、描かせた範囲
    kana = (46600, -11600, 52300, -5300)     # 矩計図
    target = (54600, -11200, 61200, -4800)   # 平面詳細図を描かせた場所
    im = f136.render(DAY / "base/house-k1.dxf", view, 1900, boxes=[plan, kana, target],
                     labels=[(5200, 1800, "← この範囲を"), (46600, -4700, "前回の矩計図"),
                             (54600, -4200, "1/50 で描く")])
    im.save(DAY / "assets/fig-conditions-p1.png")
    print(DAY / "assets/fig-conditions-p1.png")


def behavior():
    kinds = {"ask": ("描かずに、厚みの違いを質問", (232, 232, 232)),
             "confirm": ("描いて、厚みの違いの確認を求める", (214, 230, 245)),
             "note": ("描いて、厚みの違いを書き出す", (226, 238, 220)),
             "none": ("描いて、厚みの違いに触れない", (250, 222, 200))}
    table = {  # 答えを読んで分けた(log.md の結果 8)
        "claude-haiku-5-5": ("confirm", "ask"), "claude-sonnet-5-5": ("note", "note"),
        "claude-opus-5-5": ("confirm", "note"), "claude-fable-5-1": ("note", "note"),
        "gpt-6.1-sol": ("ask", "ask"), "gemini-3.8-flash": ("none", "none"), "gemini-4-argon": ("none", "none")}
    names = dict(NAMES, **{"gpt-6.1-sol": "GPT-6.1 Sol"})
    W, rh, c0, cw = 1500, 74, 300, 600
    im = Image.new("RGB", (W, 130 + rh * len(table) + 80), "white")
    d = ImageDraw.Draw(im)
    f1, f2, f3 = ImageFont.truetype(FONT, 30), ImageFont.truetype(FONT, 25), ImageFont.truetype(FONT_R, 22)
    d.text((c0 + 20, 40), "MCP（LibreCAD を操作）", font=f1, fill=(30, 30, 30))
    d.text((c0 + cw + 20, 40), "DXF を直接書く", font=f1, fill=(30, 30, 30))
    order = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5", "claude-fable-5-1", "gpt-6.1-sol",
             "gemini-3.8-flash", "gemini-4-argon"]
    for i, m in enumerate(order):
        y = 110 + i * rh
        d.text((20, y + 20), names[m], font=f2, fill=(30, 30, 30))
        for j, k in enumerate(table[m]):
            x = c0 + j * cw
            label, color = kinds[k]
            d.rounded_rectangle([x + 6, y + 6, x + cw - 6, y + rh - 6], radius=8, fill=color)
            d.text((x + 24, y + 22), label, font=f2, fill=(30, 30, 30))
    d.text((20, im.height - 56), "外壁の厚み: 仕様の材料を積み上げると 158.5、元の 1/100 の平面図は 150。指示文には書かなかった",
           font=f3, fill=(110, 110, 110))
    im.save(DAY / "assets/fig-behavior-p1.png")
    print(DAY / "assets/fig-behavior-p1.png")


def try1():
    im = Image.open(SHOT / "try1-opus-zoom.png").convert("RGB")
    im = im.crop((0, 0, im.width, im.height - 40))
    label_cells([("直す前の指示文で描いた図（範囲 X1〜X3、Y1〜Y3）", im)], DAY / "assets/fig-try1.jpg", 1,
                note="南と西の窓が、範囲の端（X3・Y3）で途中から切れている")


def p2():
    cells = [(f"Claude Opus 5.5 ／ {t}", Image.open(SHOT / f).convert("RGB").crop((0, 0, 2234, 1352)).resize((960, 581)))
             for t, f in (("MCP", "p2-mcp-opus.png"), ("DXF を直接書く", "p2-dxf-opus.png"))]
    label_cells(cells, DAY / "assets/fig-p2-cut.jpg", 2, note="平面詳細図に描いた、矩計図の切断位置。両端の矢印が見る向き（東）、記号は K1")


def main():
    compare()
    conditions()
    behavior()
    try1()
    p2()


def compare():
    cells = []
    for mode in ("mcp", "dxf"):
        for m, name in NAMES.items():
            p = SHOT / f"{mode}-{m}.png"
            if not p.exists():
                continue
            im = Image.open(p).convert("RGB")
            im = im.crop((120, 0, 1700, im.height - 40))
            im = im.resize((620, int(620 * im.height / im.width)))
            cells.append((f"{name} ／ {'MCP' if mode == 'mcp' else 'DXF を直接書く'}", im))
    w, h = cells[0][1].size
    cols, band = 4, 50
    sheet = Image.new("RGB", (w * cols, (h + band) * ((len(cells) + cols - 1) // cols)), "white")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 28)
    for i, (t, im) in enumerate(cells):
        x, y = (i % cols) * w, (i // cols) * (h + band)
        d.text((x + 12, y + 10), t, font=f, fill=(30, 30, 30))
        sheet.paste(im, (x, y + band))
    out = DAY / "assets/compare-P-1-librecad.jpg"
    sheet.save(out, quality=85)
    print(out)


if __name__ == "__main__":
    main()
