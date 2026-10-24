"""本物の福岡市の組織と、AI市役所の subagent の並びを対比する図を作る(#100)。

見た目は #98 の diagram-*.png(明るい地、薄い灰色の箱、上に色の帯)にそろえる。

使い方: ~/.venvs/tried-audio/bin/python diagrams.py
出力: assets/diagram-bureaus.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
W, H = 1520, 1280
BG = (250, 250, 248)
CARD = (240, 239, 236)
DROP = (232, 231, 228)
INK = (30, 30, 30)
SUB = (95, 95, 95)
GRAY = (110, 110, 110)
ORANGE = (234, 106, 50)
GREEN = (33, 170, 120)
PURPLE = (75, 60, 160)
FONT_B = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_R = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"

# 左(本物の福岡市)の局と、右(AI市役所)のどの局になるか。None は使わなかった局
REAL = [
    ("財政局", "finance"),
    ("住宅都市みどり局", "urban"),
    ("道路下水道局", "roads"),
    ("水道局", "roads"),
    ("港湾空港局", "port"),
    ("交通局", "port"),
    ("経済観光文化局", "economy"),
    ("農林水産局", "economy"),
    ("保健医療局", "health"),
    ("環境局", "health"),
    ("教育委員会", "education"),
    ("消防局", "fire"),
    ("総務企画局", None),
    ("市民局", None),
    ("こども未来局", None),
    ("福祉局", None),
    ("区役所(7つ)", None),
]

AI = [
    ("finance", "財政局", "査定する"),
    ("urban", "住宅都市みどり局", "区画、公園"),
    ("roads", "道路下水道局", "道路、上下水道、電気"),
    ("port", "港湾空港局", "港、空港、地下鉄、バス"),
    ("economy", "経済観光文化局", "工場、店、事務所、観光"),
    ("health", "保健環境局", "病院、墓地、ごみ、汚染"),
    ("education", "教育委員会", "学校"),
    ("fire", "消防局", "消防署、警察署"),
]


def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def center_text(d, cx, y, text, font, fill=INK):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)


def title(d, text, sub=""):
    center_text(d, W / 2, 40, text, f(46, True))
    if sub:
        center_text(d, W / 2, 104, sub, f(28), SUB)


def main():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    title(d, "本物の福岡市の局と、AI市役所の subagent",
          "ゲームで扱える局だけを残し、仕事の近い局をまとめた")

    LX, LW = 70, 430
    RX, RW = 1010, 440
    TOP = 200
    ROW, GAP = 46, 10

    center_text(d, LX + LW / 2, TOP - 56, "福岡市(2026年4月)", f(34, True))
    center_text(d, RX + RW / 2, TOP - 56, "AI市役所の subagent", f(34, True))

    # 左の局を並べ、slug ごとに y を控える
    left_y = {}
    y = TOP
    for name, slug in REAL:
        d.rounded_rectangle((LX, y, LX + LW, y + ROW), 10, fill=CARD if slug else DROP)
        d.text((LX + 22, y + 9), name, font=f(28, bool(slug)), fill=INK if slug else (155, 155, 155))
        if not slug:
            center_text(d, LX + LW - 78, y + 11, "使わない", f(22), (155, 155, 155))
        left_y.setdefault(slug, []).append(y + ROW / 2)
        y += ROW + GAP
    left_bottom = y

    # 右の箱は、元になった局の高さの真ん中に置く(線が交差しないように)
    RH = ROW
    for slug, name, work in AI:
        ys = left_y[slug]
        cy = sum(ys) / len(ys)
        top = cy - RH / 2
        d.rounded_rectangle((RX, top, RX + RW, top + RH), 10, fill=CARD)
        d.rectangle((RX, top, RX + RW, top + 7), fill=ORANGE if slug == "finance" else GREEN)
        d.text((RX + 22, top + 10), name, font=f(26, True), fill=INK)
        nw = d.textlength(name, font=f(26, True))
        d.text((RX + 22 + nw + 16, top + 15), work, font=f(20), fill=SUB)
        # つなぐ線。まとめた局は、2本が1つの箱に入る
        mid = LX + LW + 90
        for sy in ys:
            d.line((LX + LW + 8, sy, mid, sy), fill=GRAY, width=3)
            d.line((mid, sy, mid, cy), fill=GRAY, width=3)
        d.line((mid, cy, RX - 8, cy), fill=GRAY, width=3)
        if len(ys) > 1:
            center_text(d, mid + 108, cy - 32, "まとめた", f(22), GRAY)

    # 下の帯: 市長と議会
    by = left_bottom + 36
    d.rounded_rectangle((LX, by, LX + LW, by + 86), 10, fill=CARD)
    d.rectangle((LX, by, LX + LW, by + 8), fill=PURPLE)
    d.text((LX + 22, by + 20), "市長 / 市議会", font=f(26, True), fill=INK)
    d.text((LX + 22, by + 52), "常任委員会が5つ。議決が要るのは予算と条例", font=f(22), fill=SUB)

    d.rounded_rectangle((RX, by, RX + RW, by + 86), 10, fill=CARD)
    d.rectangle((RX, by, RX + RW, by + 8), fill=PURPLE)
    d.text((RX + 22, by + 20), "市長(2つ)+ 議会(1つ)", font=f(26, True), fill=INK)
    d.text((RX + 22, by + 52), "見てまとめる / 実行する / 確かめる", font=f(22), fill=SUB)

    path = os.path.join(OUT, "diagram-bureaus.png")
    im.save(path)
    print("wrote", path)




# 予算の決め方の流れ。左が本物の福岡市、右がAI市役所。スイムレーンで対比する
LANES = ["市長", "財政局", "各局", "議会"]

REAL_FLOW = [
    ("市長", "編成方針を\n決める"),
    ("財政局", "編成要領を\n作る"),
    ("各局", "見積書を\n出す"),
    ("財政局", "査定して\n市長に上げる"),
    ("市長", "査定して\n予算案にする"),
    ("議会", "審査して\n議決する"),
]

AI_FLOW = [
    ("市長", "街を見て\n重点を決める"),
    ("財政局", "今月の枠を\n書く"),
    ("各局", "案を1件ずつ\n出す"),
    ("財政局", "可・減額・\n不可を付ける"),
    ("市長", "3件まで\n選ぶ"),
    ("議会", "議案だけ\n確かめる"),
]


def flow_panel(d, x0, y0, w, h, heading, note, steps, accent):
    """スイムレーンを縦にした1枚。レーンは列、手順は上から下へ流れる"""
    d.text((x0, y0 - 74), heading, font=f(32, True), fill=INK)
    d.text((x0, y0 - 38), note, font=f(22), fill=SUB)
    lane_w = w / len(LANES)
    head_h = 46
    for i, lane in enumerate(LANES):
        lx = x0 + i * lane_w
        d.rectangle((lx, y0, lx + lane_w - 8, y0 + h), fill=CARD if i % 2 == 0 else (245, 244, 241))
        center_text(d, lx + (lane_w - 8) / 2, y0 + 10, lane, f(24, True), SUB)
        d.line((lx, y0 + head_h, lx + lane_w - 8, y0 + head_h), fill=(225, 224, 220), width=2)

    row_h = (h - head_h - 20) / len(steps)
    box_h = row_h - 26
    boxes = []
    for n, (lane, text) in enumerate(steps):
        i = LANES.index(lane)
        lx = x0 + i * lane_w
        top = y0 + head_h + 14 + n * row_h
        box = (lx + 6, top, lx + lane_w - 14, top + box_h)
        d.rounded_rectangle(box, 10, fill=(255, 255, 255), outline=accent, width=3)
        cx = (box[0] + box[2]) / 2
        center_text(d, cx, box[1] + 8, str(n + 1), f(20, True), accent)
        # 箱の幅に収まるよう、1文字ずつ詰めて折り返す
        fnt = f(20)
        limit = (box[2] - box[0]) - 14
        lines = []
        for part in text.split("\n"):
            cur = ""
            for ch in part:
                if d.textlength(cur + ch, font=fnt) <= limit:
                    cur += ch
                else:
                    lines.append(cur)
                    cur = ch
            if cur:
                lines.append(cur)
        ty = box[1] + 34 + (0 if len(lines) > 1 else 12)
        for ln in lines[:3]:
            center_text(d, cx, ty, ln, fnt)
            ty += 26
        boxes.append(box)

    # つなぎは折れ線(下へ → 横へ → 下へ)
    import math
    for b0, b1 in zip(boxes, boxes[1:]):
        cx0, cx1 = (b0[0] + b0[2]) / 2, (b1[0] + b1[2]) / 2
        y_from, y_to = b0[3], b1[1]
        my = (y_from + y_to) / 2
        d.line((cx0, y_from, cx0, my), fill=GRAY, width=4)
        if abs(cx1 - cx0) > 1:
            d.line((cx0, my, cx1, my), fill=GRAY, width=4)
        d.line((cx1, my, cx1, y_to - 6), fill=GRAY, width=4)
        s2 = 13
        d.polygon([(cx1, y_to), (cx1 - s2, y_to - s2 - 2), (cx1 + s2, y_to - s2 - 2)], fill=GRAY)


def flow():
    H2 = 1080
    im = Image.new("RGB", (W, H2), BG)
    d = ImageDraw.Draw(im)
    center_text(d, W / 2, 40, "予算の決め方をなぞる", f(46, True))
    center_text(d, W / 2, 104, "局の案は、財政局を通ってから市長に届く。この順番をそのままAIの手順にした", f(28), SUB)
    pw = (W - 140 - 70) / 2
    flow_panel(d, 70, 260, pw, 760, "本物の福岡市", "年に1回(福岡市予算及び決算規則)", REAL_FLOW, PURPLE)
    flow_panel(d, 70 + pw + 70, 260, pw, 760, "AI市役所", "ゲームの1か月ごとに1回", AI_FLOW, GREEN)
    path = os.path.join(OUT, "diagram-budget-flow.png")
    im.save(path)
    print("wrote", path)


# 市の計画: 第10次福岡市基本計画の施策のうち、ゲームに当てた14個と目標
PLAN = [
    ("暮らし", [
        ("1-2 健やかで心豊かに暮らせる社会", "健康の平均", "70", "75以上"),
        ("2-3 自ら学び続ける子どもの育成", "学校の定員", "小7,200 / 高13,000", "子ども・10代以上"),
        ("3-3 安全で快適な生活基盤", "電気・水・下水が来ない市民", "0", "0 を保つ"),
        ("3-4 日常生活の安全・安心", "火事と犯罪の印", "8", "4以下"),
    ]),
    ("まち", [
        ("4-1 都市と自然が調和したまち", "住宅の地価の平均", "45", "50以上"),
        ("4-2 花や緑による潤い", "公園などの数", "22", "40以上"),
        ("4-3 脱炭素社会", "汚染の印", "9", "4以下"),
        ("4-4 資源循環", "ごみの印", "11", "0"),
        ("6-1 都心部の機能強化", "事務所レベル3の棟数", "118", "300以上"),
        ("6-3 公共交通を主軸とした交通体系", "交通の流れ", "64%", "70%以上"),
    ]),
    ("産業", [
        ("5-1、5-2 観光", "今いる観光客", "928", "1,500以上"),
        ("6-4、7-1 企業の立地、地場企業", "働き口", "43,075", "46,000以上"),
        ("6-4、7-1(続き)", "品物がない店 / 原料がない工場", "107 / 126", "50以下 / 60以下"),
        ("8-1 物流・人流のゲートウェイ", "港の中で止まったトラック", "1,421", "300以下"),
    ]),
]


def plan():
    rows = sum(len(v) for _, v in PLAN)
    RH2, HEAD, GH = 54, 212, 58
    H3 = HEAD + rows * RH2 + len(PLAN) * GH + 70
    im = Image.new("RGB", (W, H3), BG)
    d = ImageDraw.Draw(im)
    center_text(d, W / 2, 34, "10年の計画を、ゲームの数字に置き換えた", f(44, True))
    center_text(d, W / 2, 96, "第10次福岡市基本計画の30の施策のうち、ゲームに当たる14個を残した", f(26), SUB)

    X = [70, 620, 1000, 1230]   # 施策 / 測り方 / 出発点 / 12か月後
    COLS = ["施策(第10次基本計画)", "ゲームでの測り方", "出発点", "12か月後の目標"]
    y = HEAD
    for i, c in enumerate(COLS):
        d.text((X[i], y - 36), c, font=f(24, True), fill=SUB)
    d.line((70, y - 4, W - 70, y - 4), fill=(210, 209, 205), width=3)

    for group, items in PLAN:
        d.rounded_rectangle((70, y + 8, 180, y + 44), 8, fill=GREEN)
        center_text(d, 125, y + 13, group, f(24, True), (255, 255, 255))
        y += GH
        for name, how, start, goal in items:
            d.rectangle((70, y, W - 70, y + RH2 - 6), fill=CARD)
            d.text((X[0] + 12, y + 14), name, font=f(23), fill=INK)
            d.text((X[1], y + 14), how, font=f(22), fill=SUB)
            d.text((X[2], y + 14), start, font=f(22), fill=SUB)
            d.text((X[3], y + 14), goal, font=f(22, True), fill=INK)
            y += RH2
    center_text(d, W / 2, H3 - 46, "財政は目標ではなく守る線にした(週の収支を黒字に保つ)", f(22), SUB)
    path = os.path.join(OUT, "diagram-city-plan.png")
    im.save(path)
    print("wrote", path)


# 1か月を回す手順。役ごとに色を分け、書くファイルを添える
MONTH = [
    ("市長", "街を見て\n重点を決める", "m01-policy.md", PURPLE),
    ("財政局", "今月の枠を書く", "m01-guide.md", ORANGE),
    ("7つの局", "案を1件ずつ出す\n(同時に呼ぶ)", "m01-urban.md ほか7つ", GREEN),
    ("財政局", "可・減額・不可\nを付ける", "m01-finance.md", ORANGE),
    ("市長", "3件まで選び\n議案を分ける", "m01-bill.md", PURPLE),
    ("議会", "議案だけ確かめる\n(なければ呼ばない)", "m01-assembly.md", (60, 120, 200)),
    ("実行する市長", "打つ → 10日×3回\n進めて様子を見る", "mayor-note.md", PURPLE),
]


def month():
    H4 = 1060
    im = Image.new("RGB", (W, H4), BG)
    d = ImageDraw.Draw(im)
    center_text(d, W / 2, 34, "ゲームの1か月を回す手順", f(44, True))
    center_text(d, W / 2, 96, "subagent は別の subagent を呼べない。呼ぶ順番はスクリプトが決める", f(26), SUB)

    BX, BW, BH = 300, 560, 92
    top = 170
    gap = 26
    for n, (who, what, fname, color) in enumerate(MONTH):
        y = top + n * (BH + gap)
        d.rounded_rectangle((BX, y, BX + BW, y + BH), 12, fill=CARD)
        d.rectangle((BX, y, BX + 10, y + BH), fill=color)
        center_text(d, BX - 44, y + BH / 2 - 16, str(n + 1), f(30, True), color)
        d.text((BX + 28, y + 12), who, font=f(24, True), fill=color)
        lines = what.split("\n")
        ty = y + 40 if len(lines) > 1 else y + 50
        for ln in lines:
            d.text((BX + 28, ty), ln, font=f(23), fill=INK)
            ty += 28
        # 書くファイル
        d.text((BX + BW + 40, y + BH / 2 - 14), fname, font=f(22), fill=SUB)
        if n < len(MONTH) - 1:
            cx = BX + BW / 2
            d.line((cx, y + BH, cx, y + BH + gap - 8), fill=GRAY, width=4)
            d.polygon([(cx, y + BH + gap), (cx - 11, y + BH + gap - 12), (cx + 11, y + BH + gap - 12)], fill=GRAY)

    d.text((BX + BW + 40, top - 34), "書くファイル(council/ の中)", font=f(22, True), fill=SUB)
    center_text(d, W / 2, H4 - 54,
                "局どうしは互いの案を読まない。立場がぶつかるのは、市長が7つを並べて読む5番目", f(24), SUB)
    path = os.path.join(OUT, "diagram-month.png")
    im.save(path)
    print("wrote", path)


if __name__ == "__main__":
    main()
    flow()
    plan()
    month()
