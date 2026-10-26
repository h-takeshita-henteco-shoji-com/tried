"""記事の図を作る(#105)。表は note で崩れるので、画像にする。

見た目は #100 の diagram-*.png と #93 の chart-4-final.png(明るい地、薄い灰色の箱、上に色の帯)にそろえる。
数は council/m*-run.json(Workflow の返り値)と、2人の市政ノートの数字の表から取る。

使い方: uv run --with pillow --with matplotlib python assets/scripts/charts.py
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RUN = Path(__file__).resolve().parents[2]
OUT = RUN / "assets"
BG = (250, 250, 248)
CARD = (240, 239, 236)
INK = (30, 30, 30)
SUB = (95, 95, 95)
LIGHT = (160, 160, 160)
GRAY = (110, 110, 110)
ORANGE = (234, 106, 50)
GREEN = (33, 170, 120)
PURPLE = (75, 60, 160)
BLUE = (60, 120, 200)
RED = (210, 70, 60)
FONT_B = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_R = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"

BUREAUS = [("urban", "住宅都市みどり局"), ("roads", "道路下水道局"), ("port", "港湾空港局"),
           ("economy", "経済観光文化局"), ("health", "保健環境局"), ("education", "教育委員会"), ("fire", "消防局")]


def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def runs():
    return [json.loads((RUN / "council" / f"m{m:02d}-run.json").read_text()) for m in range(1, 13)]


def title(d, w, text, sub=None):
    d.text((w // 2, 40), text, font=f(40, True), fill=INK, anchor="mt")
    if sub:
        d.text((w // 2, 96), sub, font=f(24), fill=SUB, anchor="mt")


# 1. 12か月の案の流れ
def funnel(rs):
    props = sum(1 for r in rs for p in r["proposals"] if p["hasProposal"])
    assessed = sum(len(r["assessed"]["assessments"]) for r in rs)
    ok = sum(1 for r in rs for a in r["assessed"]["assessments"] if a["verdict"] == "可")
    adopted = sum(len(r["bill"]["measures"]) for r in rs)
    votes = [x for r in rs for x in (r.get("ruling") or {}).get("rulings", [])]
    passed = sum(1 for x in votes if x["verdict"] == "可決")
    done = sum(len(r["done"]["executed"]) for r in rs)
    surveys_p = sum(1 for r in rs for p in r["proposals"] if p["survey"]["exists"])
    surveys_a = sum(len(r["bill"].get("surveys") or []) for r in rs)
    assert props == assessed == ok, (props, assessed, ok)

    W, H = 1520, 1100
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, W, "12か月で、局の案はどう絞られたか", "7つの局が出した案の行方。数は12か月の合計")
    steps = [
        (GREEN, "7つの局", f"案を出した {props}件", f"案なし {7 * 12 - props}回(教育委員会は12か月とも案なし)"),
        (ORANGE, "財政局", f"「可」 {ok}件 / {assessed}件", "減額・不可は0件。費用と型の上限だけを見るため"),
        (PURPLE, "見てまとめる市長", f"採った {adopted}件 / 外した {props - adopted}件", "月に3件まで。外した理由は右"),
        (BLUE, "議会", f"可決 {passed}件 / {len(votes)}件", "議決が要るのは、取り壊し・予算・税・融資だけ"),
        (PURPLE, "実行する市長", f"打てた {done}件 / {adopted}件", "打てなかった2件は、どちらも打つ前に止めた"),
    ]
    y = 150
    for i, (c, who, big, small) in enumerate(steps):
        x0, x1 = 80, 860
        d.rounded_rectangle([x0, y, x1, y + 150], 12, fill=CARD)
        d.rectangle([x0, y, x0 + 10, y + 150], fill=c)
        d.text((x0 + 34, y + 18), who, font=f(26, True), fill=c)
        d.text((x0 + 34, y + 54), big, font=f(36, True), fill=INK)
        d.text((x0 + 34, y + 124), small, font=f(20), fill=SUB, anchor="lm")
        if i < len(steps) - 1:
            d.polygon([(470, y + 158), (490, y + 158), (480, y + 174)], fill=GRAY)
        y += 182
    # 外した理由
    reasons = [
        ("同じ月の別の試しと、測る場所や数が重なる", 10),
        ("必須の条件が確かめられていない", 5),
        ("3件の枠の中で、効き目が小さい", 4),
        ("維持費の枠を超える", 2),
    ]
    x0 = 920
    d.text((x0, 320), "市長が外した理由", font=f(28, True), fill=PURPLE)
    d.text((x0, 362), "外した案1件ごとの、いちばんの理由", font=f(20), fill=SUB)
    yy = 420
    mx = max(n for _, n in reasons)
    for text, n in reasons:
        d.text((x0, yy), text, font=f(22), fill=INK)
        d.rounded_rectangle([x0, yy + 36, x0 + int(440 * n / mx), yy + 64], 6, fill=PURPLE)
        d.text((x0 + int(440 * n / mx) + 12, yy + 50), f"{n}件", font=f(22, True), fill=INK, anchor="lm")
        yy += 100
    d.text((x0, yy + 10), "外した案には、「どうすれば来月採るか」を", font=f(20), fill=SUB)
    d.text((x0, yy + 40), "書いて局に返す。調査は別に3件まで採る", font=f(20), fill=SUB)
    d.text((x0, yy + 70), f"(調査は {surveys_p}件出て {surveys_a}件採った)", font=f(20), fill=SUB)
    img.save(OUT / "chart-council-funnel.png")


# 2. 局ごと・月ごとの案の行方
def matrix(rs):
    W, H = 1520, 860
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, W, "どの局の案が、いつ採られたか", "1マスが、その月のその局の案1件")
    colors = {"done": GREEN, "stopped": ORANGE, "rejected": (205, 205, 200), "none": None}
    x0, y0, cw, ch = 330, 190, 92, 72
    for m in range(12):
        d.text((x0 + m * cw + cw // 2, y0 - 30), f"{m + 1}", font=f(22, True), fill=SUB, anchor="mm")
    d.text((x0 - 24, y0 - 30), "か月目", font=f(20), fill=SUB, anchor="rm")
    for i, (slug, name) in enumerate(BUREAUS):
        y = y0 + i * ch
        d.text((x0 - 24, y + ch // 2), name, font=f(24, True), fill=INK, anchor="rm")
        for m, r in enumerate(rs):
            p = next(p for p in r["proposals"] if p["bureau"] == slug)
            mid = next((x["id"] for x in r["bill"]["measures"] if x["fromBureau"] == slug), None)
            if not p["hasProposal"]:
                state = "none"
            elif mid is None:
                state = "rejected"
            elif mid in r["done"]["executed"]:
                state = "done"
            else:
                state = "stopped"
            bx, by = x0 + m * cw + 6, y + 6
            box = [bx, by, bx + cw - 12, by + ch - 12]
            if state == "none":
                d.rounded_rectangle(box, 8, outline=(215, 215, 210), width=2)
                d.text(((box[0] + box[2]) // 2, (box[1] + box[3]) // 2), "なし", font=f(18), fill=LIGHT, anchor="mm")
            else:
                d.rounded_rectangle(box, 8, fill=colors[state])
            survey = any(s["fromBureau"] == slug for s in r["bill"].get("surveys") or [])
            if survey:
                d.ellipse([box[2] - 22, box[1] + 6, box[2] - 8, box[1] + 20], fill=BLUE)
    ly = y0 + 7 * ch + 40
    items = [(GREEN, "採って、打てた"), (ORANGE, "採ったが、打つ前に止めた"), ((205, 205, 200), "外した"),
             (None, "案なし"), (BLUE, "調査を採った")]
    lx = 330
    for c, t in items:
        if c is None:
            d.rounded_rectangle([lx, ly, lx + 34, ly + 26], 6, outline=(215, 215, 210), width=2)
        elif c == BLUE:
            d.ellipse([lx + 10, ly + 6, lx + 24, ly + 20], fill=BLUE)
        else:
            d.rounded_rectangle([lx, ly, lx + 34, ly + 26], 6, fill=c)
        d.text((lx + 46, ly + 13), t, font=f(22), fill=INK, anchor="lm")
        lx += 60 + int(d.textlength(t, font=f(22)))
    img.save(OUT / "chart-council-months.png")


# 3. 6か月目の流れ(例)
def month6():
    rows = [
        ("住宅都市みどり局", "東に公園(日本庭園)を1つ置く", "可", "採った", "-", "置けた。公園などが91に"),
        ("道路下水道局", "南北の細い道4区間を4車線に", "可", "採った", "-", "差し替えた。費用0"),
        ("港湾空港局", "貨物駅の出口を延ばし、大通りにつなぐ", "可", "外した", "-", "つながるかを確かめられていない"),
        ("経済観光文化局", "放棄された建物89棟を取り壊す", "可", "採った", "可決", "品物が届かない店 178→116"),
        ("保健環境局", "満杯の埋立地を空にする", "可", "外した", "-", "取り壊しと、測る場所が重なる"),
        ("教育委員会", "案なし(学校の定員は足りている)", "-", "-", "-", "-"),
        ("消防局", "案なし(火事と犯罪の印は0)", "-", "-", "-", "-"),
    ]
    heads = [("局", 250), ("案", 470), ("財政局", 110), ("市長", 110), ("議会", 100), ("結果・外した理由", 430)]
    W = 40 + sum(w for _, w in heads) + 40
    H = 200 + 72 * len(rows) + 60
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, W, "6か月目の1か月", "編成方針の重点: 企業の立地、物流のゲートウェイ、脱炭素")
    colc = {"財政局": ORANGE, "市長": PURPLE, "議会": BLUE}
    x = 40
    for h, w in heads:
        d.text((x + 12, 170), h, font=f(22, True), fill=colc.get(h, SUB), anchor="lm")
        x += w
    y = 200
    for i, row in enumerate(rows):
        if i % 2 == 0:
            d.rectangle([40, y, W - 40, y + 72], fill=CARD)
        x = 40
        for (h, w), v in zip(heads, row):
            bold = h == "局" or v in ("採った", "可決")
            col = INK
            if v == "外した":
                col = RED
            elif v in ("-",) or v.startswith("案なし"):
                col = LIGHT
            d.text((x + 12, y + 36), v, font=f(21, bold), fill=col, anchor="lm")
            x += w
        y += 72
    img.save(OUT / "chart-council-month6.png")


# 4. 任期の終わりの比べ
def final():
    rows = [
        ("人口", "178,872", "179,240", "176,793", 1),
        ("所持金", "208万", "268万", "243万", 1),
        ("週の黒字", "+9,965", "+16,011", "+9,445", 1),
        ("幸福度", "85", "83", "85", 2),
        ("品物が届かない店", "228棟", "305棟", "88棟", 2),
        ("火事と犯罪の印", "7棟", "11棟", "3棟", 2),
        ("汚染の印", "32棟", "44棟", "38棟", 2),
        ("ごみの印", "15棟", "11棟", "20棟", 1),
        ("公園など", "81", "81", "101", 2),
        ("交通の流れ", "51%", "53%", "55%", 2),
        ("使ったLLMのトークン量", "-", "約150万", "約1,420万", 0),
    ]
    W, H = 1200, 170 + 66 * len(rows) + 50
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cols = [("出発点", GRAY, 560), ("基準の市長", PURPLE, 790), ("AI市役所", GREEN, 1030)]
    for name, c, cx in cols:
        d.text((cx, 50), name, font=f(28, True), fill=INK, anchor="mm")
        d.rectangle([cx - 105, 80, cx + 105, 90], fill=c)
    y = 110
    for i, (label, a, b, c, best) in enumerate(rows):
        if i % 2 == 0:
            d.rectangle([24, y, W - 24, y + 66], fill=CARD)
        d.text((40, y + 33), label, font=f(24), fill=INK, anchor="lm")
        for j, (v, (_, _, cx)) in enumerate(zip((a, b, c), cols)):
            bold = best and j == best
            d.text((cx, y + 33), v, font=f(30 if bold else 24, bold), fill=INK if bold else SUB, anchor="mm")
        y += 66
    d.text((40, y + 20), "2050年12月27日。太字は2人のうち、よい方", font=f(20), fill=SUB)
    img.save(OUT / "chart-final.png")


# 5. 月ごとの人口と、品物が届かない店
def lines():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    font_manager.fontManager.addfont(FONT_R)
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT_R).get_name()
    months = list(range(0, 13))
    base_pop = [178872, 178716, 178791, 179243, 179366, 179403, 179243, 179071, 179310, 178531, 178765, 178945, 179240]
    city_pop = [178872, 178760, 178341, 178413, 178559, 178138, 178004, 177883, 177850, 177490, 177060, 177159, 176793]
    base_ng = [228, 215, 217, 233, 240, 250, 251, 287, 300, 303, 303, 308, 305]
    city_ng = [228, 215, 178, 169, 183, 178, 116, 120, 151, 137, 137, 130, 88]
    p, g = tuple(c / 255 for c in PURPLE), tuple(c / 255 for c in GREEN)
    fig, axes = plt.subplots(1, 2, figsize=(15.2, 5.6), dpi=100, facecolor=tuple(c / 255 for c in BG))
    for ax, (bs, cs, t, unit) in zip(axes, [(base_pop, city_pop, "人口", "人"), (base_ng, city_ng, "品物が届かない店", "棟")]):
        ax.set_facecolor(tuple(c / 255 for c in BG))
        ax.plot(months, bs, color=p, lw=3, marker="o", label="基準の市長")
        ax.plot(months, cs, color=g, lw=3, marker="o", label="AI市役所")
        ax.set_title(t, fontsize=20, pad=12)
        ax.set_xticks(months)
        ax.set_xticklabels(["出発"] + [f"{m}" for m in months[1:]], fontsize=12)
        ax.set_xlabel("か月目", fontsize=13)
        ax.tick_params(axis="y", labelsize=12)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.grid(axis="y", color=(0.88, 0.88, 0.86))
        ax.legend(fontsize=13, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "chart-monthly.png", facecolor=fig.get_facecolor())


if __name__ == "__main__":
    rs = runs()
    funnel(rs)
    matrix(rs)
    month6()
    final()
    lines()
    print("ok")
