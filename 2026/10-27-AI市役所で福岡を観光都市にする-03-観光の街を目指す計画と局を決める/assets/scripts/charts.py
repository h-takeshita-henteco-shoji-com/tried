"""記事の図を作る(#124)。表は note で崩れるので、画像にする。

数は mayor-note.md の数字の表(月例の行)と council/m*-run.json から取った。
使い方: uv run --with matplotlib --with pillow python assets/scripts/charts.py
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

RUN = Path(__file__).resolve().parents[2]
OUT = RUN / "assets"
FONT_B = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_R = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
font_manager.fontManager.addfont(FONT_R)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT_R).get_name()

BG = "#fafaf8"
ORANGE = "#ea6a32"
GREEN = "#21aa78"
BLUE = "#3c78c8"
GRAY = "#8c8c8c"

# 月末の数字(0 は出発点)
TOURISTS = [1646, 1747, 1772, 1742, 1811, 1801, 1665, 1744, 1790, 1705, 1763, 1725, 1765,
            1847, 1851, 1937, 1875, 1783, 1795, 1852, 1837, 2020, 2020, 2011, 2048]
POP = [178872, 178859, 178639, 178486, 178380, 178150, 179174, 180138, 180168, 180117, 179848, 179547, 179020,
       178202, 177176, 176528, 175864, 175384, 174778, 174330, 174078, 173537, 172759, 172273, 171949]


def monthly():
    fig, axes = plt.subplots(2, 1, figsize=(12, 8.4), facecolor=BG, sharex=True)
    xs = list(range(25))
    for ax in axes:
        ax.set_facecolor(BG)
        ax.axvspan(12, 24, color="#eeeeea", zorder=0)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#dddddd")
    a = axes[0]
    a.plot(xs, TOURISTS, color=ORANGE, lw=3, marker="o")
    a.axhline(3000, color=GRAY, ls="--")
    a.text(0.2, 2930, "目標 3,000人", color=GRAY, fontsize=13, va="top")
    a.set_ylim(1500, 3100)
    a.set_title("観光客の数(月末)", fontsize=17, loc="left")
    a.annotate("名所に電気が通る(17か月目)", xy=(17, 1783), xytext=(13.3, 1580), fontsize=12,
               arrowprops=dict(arrowstyle="->", color=GRAY))
    a.annotate("2,000人を超える(21か月目)", xy=(21, 2020), xytext=(16.2, 2350), fontsize=12,
               arrowprops=dict(arrowstyle="->", color=GRAY))
    a.text(6, 3050, "1年目", ha="center", fontsize=14, color=GRAY)
    a.text(18, 3050, "2年目", ha="center", fontsize=14, color=GRAY)
    b = axes[1]
    b.plot(xs, [p / 10000 for p in POP], color=BLUE, lw=3, marker="o")
    b.set_title("人口(万人、月末)", fontsize=17, loc="left")
    b.set_ylim(17.0, 18.2)
    b.set_xticks(xs)
    b.set_xticklabels(["始"] + [str(i) for i in range(1, 25)])
    b.set_xlabel("か月目", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT / "chart-monthly.png", dpi=110, facecolor=BG)


def measures():
    """年ごとに、採った施策を市の計画の分野で数える。"""
    names = {"5": "観光", "6": "交通", "4": "環境・景観", "3": "安全", "2": "教育", "8": "物流", "1": "医療など", "財": "医療など"}
    order = ["観光", "交通", "環境・景観", "安全", "教育", "物流", "医療など"]
    colors = [ORANGE, BLUE, GREEN, "#a05ac8", "#d2a032", "#5a5a5a", GRAY]
    years = []
    for a, b in [(1, 12), (13, 24)]:
        c = {k: 0 for k in order}
        for m in range(a, b + 1):
            r = json.loads((RUN / "council" / f"m{m:02d}-run.json").read_text())
            for x in r["bill"]["measures"]:
                items = " ".join(x.get("planItems") or [])
                key = "5" if "5-" in items else (items[:1] if items else "財")
                c[names.get(key, "医療など")] += 1
        years.append(c)
    fig, ax = plt.subplots(figsize=(12, 5.2), facecolor=BG)
    ax.set_facecolor(BG)
    for row, (label, c) in enumerate(zip(["1年目", "2年目"], years)):
        left = 0
        for k, col in zip(order, colors):
            v = c[k]
            if not v:
                continue
            ax.barh(row, v, left=left, color=col, edgecolor="white")
            if v >= 4:
                ax.text(left + v / 2, row, f"{k}\n{v}", ha="center", va="center", color="white", fontsize=12)
            else:
                ax.text(left + v / 2, row, str(v), ha="center", va="center", color="white", fontsize=12)
            left += v
        ax.text(left + 0.5, row, f"計{left}件", va="center", fontsize=13)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=k) for k, c in zip(order, colors)], ncol=7, loc="upper center",
              bbox_to_anchor=(0.5, -0.08), frameon=False, fontsize=12)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["1年目", "2年目"], fontsize=14)
    ax.invert_yaxis()
    ax.set_xlim(0, 64)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("採った施策の分野(市の計画のどの施策に向けた手か)", fontsize=16, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "chart-measures.png", dpi=110, facecolor=BG)
    return years


def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


KIND = {"新": ((33, 170, 120), "新しく足した"), "変": ((234, 106, 50), "変えた"),
        "同": ((150, 150, 150), "そのまま"), "廃": ((120, 90, 160), "やめた")}


def badge(d, x, y, kind):
    col, label = KIND[kind]
    d.rounded_rectangle((x, y, x + 150, y + 40), 20, fill=col)
    d.text((x + 75, y + 20), label, font=f(21, True), fill="white", anchor="mm")


def legend(d, y, kinds, W):
    x = W // 2 - len(kinds) * 95
    for k in kinds:
        badge(d, x, y, k)
        x += 190


def harness():
    """1か月の段ごとに、前回と今回を並べる。"""
    rows = [
        ("見る", "市長が街を見て、重点を決める", "同じ。地図に空き地と島の座標を書いて渡す", "新"),
        ("長期計画", "なし。毎月その場で案を考える", "各局が12か月の計画を作り、市長がレビュー。差し戻しは2回まで", "新"),
        ("案", "7局が1件ずつ。案の代わりに調査も出せる", "8局が5件まで。財政局も税・予算・政策の案を出す", "変"),
        ("査定", "財政局が、案ごとに可・減額・不可を付ける", "なくした。お金のチェックは議会へ", "廃"),
        ("まとめ", "市長が3件まで選ぶ", "件数の上限なし。局をまたぐ調整は市長が決める", "変"),
        ("差し戻し", "なし。外した案は翌月に出し直す", "条件付きで外した案を、局が1回だけ調べ直す", "新"),
        ("議会", "取り壊しなどの議案だけを確かめる", "議案に加えて、全部の施策をお金の目で確かめる", "変"),
        ("実行", "実行する市長だけが街を動かす", "同じ。10日ずつ3回進め、途中で2回見回る", "同"),
    ]
    W, RH = 1700, 118
    H = 230 + RH * len(rows) + 30
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    d.text((W // 2, 30), "AI市役所の1か月、前回と今回", font=f(40, True), fill=(30, 30, 30), anchor="mt")
    legend(d, 92, ["新", "変", "廃", "同"], W)
    cols = [(40, 230), (250, 720), (740, 1460), (1490, 1660)]
    d.text((cols[1][0] + 10, 175), "前回", font=f(26, True), fill=(95, 95, 95), anchor="lm")
    d.text((cols[2][0] + 10, 175), "今回", font=f(26, True), fill=(30, 30, 30), anchor="lm")
    y = 205
    for name, before, after, kind in rows:
        col = KIND[kind][0]
        d.rounded_rectangle((cols[0][0], y, cols[3][1], y + RH - 14), 12, fill=(240, 239, 236))
        d.rectangle((cols[0][0], y, cols[0][0] + 10, y + RH - 14), fill=col)
        cy = y + (RH - 14) // 2
        d.text((cols[0][0] + 30, cy), name, font=f(30, True), fill=(30, 30, 30), anchor="lm")
        wrap(d, cols[1][0] + 10, cy, before, 17, f(23), (95, 95, 95))
        wrap(d, cols[2][0] + 10, cy, after, 26, f(23, kind != "同"), (30, 30, 30))
        badge(d, cols[3][0], cy - 20, kind)
        y += RH
    img.save(OUT / "diagram-harness.png")


def wrap(d, x, cy, text, n, font, fill):
    lines = [text[i:i + n] for i in range(0, len(text), n)]
    lines = []
    cur = ""
    for part in text.replace("。", "。|").replace("、", "、|").split("|"):
        if len(cur) + len(part) > n and cur:
            lines.append(cur)
            cur = part
        else:
            cur += part
    if cur:
        lines.append(cur)
    lh = 32
    top = cy - lh * len(lines) / 2 + lh / 2
    for i, line in enumerate(lines):
        d.text((x, top + i * lh), line, font=font, fill=fill, anchor="lm")


def lessons():
    """前回の反省と、今回の直し方の対応。"""
    rows = [
        ("財政局がふるいにならず、税の案も出なかった", "財政局を案を出す局にし、お金のチェックは議会へ"),
        ("街全体を見る役がいない", "各局に長期計画を持たせ、市長がレビューして調整する"),
        ("渋滞に、小さな工事しか打てない", "道具を直し、壊してから建てる工事を試せるように(このテーマの1・2回目)"),
        ("市長は月3件、局は月1件しか出せない", "局は5件まで、市長は上限なし。外した案は1回だけ調べ直す"),
        ("幸福度も目標にしていた(ボツの12か月)", "幸福度は施策の結果として、目標から外す"),
    ]
    W, RH = 1700, 120
    H = 150 + RH * len(rows) + 20
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    d.text((W // 2, 30), "前回の反省と、今回の直し方", font=f(40, True), fill=(30, 30, 30), anchor="mt")
    y = 120
    for before, after in rows:
        d.rounded_rectangle((40, y, 760, y + RH - 20), 12, fill=(240, 239, 236), outline=(210, 70, 60), width=3)
        wrap(d, 70, y + (RH - 20) // 2, before, 24, f(25), (30, 30, 30))
        d.polygon([(785, y + 30), (785, y + 70), (835, y + 50)], fill=(160, 160, 160))
        d.rounded_rectangle((860, y, 1660, y + RH - 20), 12, fill=(240, 239, 236), outline=(33, 170, 120), width=3)
        wrap(d, 890, y + (RH - 20) // 2, after, 27, f(25, True), (30, 30, 30))
        y += RH
    img.save(OUT / "diagram-lessons.png")


def tourism_map():
    """観光の場所を、地形の図に書き込む。"""
    src = Image.open(RUN.parents[1] / "code/ai-mayor/mayor/city-map.png").convert("RGB")

    def px(x, z):
        return 432 + 0.0416 * x, 430 - 0.0416 * z

    x0, y0 = px(-6200, 3800)
    x1, y1 = px(6400, -4300)
    S = 1.9
    img = src.crop((int(x0), int(y0), int(x1), int(y1))).resize((int((x1 - x0) * S), int((y1 - y0) * S)))
    img = img.convert("RGBA")
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)

    def at(x, z):
        a, b = px(x, z)
        return (a - x0) * S, (b - y0) * S

    marks = [
        (-4862, 1731, "島B", "道・橋・風力(2・5か月目)\n水がなく、名所を置けない", (210, 70, 60), (-90, 80)),
        (700, 1565, "名所(空き地3)", "5か月目に置いた\n電気が来たのは17か月目", (234, 106, 50), (-420, -230)),
        (2290, 972, "名所A・B", "1か月目に2棟", (33, 170, 120), (60, -200)),
        (1580, -530, "名所(本土)", "11か月目に置き\n13か月目に道", (33, 170, 120), (200, 60)),
        (1862, 360, "峰の公園", "23か月目", (33, 170, 120), (240, -60)),
        (1477, -2950, "駅の候補(空き地1)", "24か月目に試す\n電気の線が通らない", (210, 70, 60), (80, 40)),
        (4545, 2382, "駅の候補(空き地5)", "一般道がない", (210, 70, 60), (-380, -170)),
    ]
    for x, z, name, note, col, (dx, dy) in marks:
        cx, cy = at(x, z)
        d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline=col + (255,), width=6)
        lines = [name] + note.split("\n")
        w = max(d.textlength(l, font=f(26)) for l in lines) + 30
        h = 40 + 34 * (len(lines) - 1) + 10
        tx = min(max(cx + dx, 8), img.width - w - 8)
        ty = min(max(cy + dy, 8), img.height - h - 8)
        d.line((cx, cy, tx + w / 2, ty + h / 2), fill=col + (255,), width=3)
        d.rounded_rectangle((tx, ty, tx + w, ty + h), 10, fill=(255, 255, 255, 235), outline=col + (255,), width=3)
        d.text((tx + 15, ty + 10), name, font=f(26, True), fill=(30, 30, 30))
        for i, l in enumerate(note.split("\n")):
            d.text((tx + 15, ty + 46 + 34 * i), l, font=f(23), fill=(70, 70, 70))
    img = Image.alpha_composite(img, over).convert("RGB")
    head = Image.new("RGB", (img.width, 90), (250, 250, 248))
    hd = ImageDraw.Draw(head)
    hd.text((img.width // 2, 20), "観光の場所と、24か月の結果(赤い点は道路)", font=f(36, True), fill=(30, 30, 30), anchor="mt")
    out = Image.new("RGB", (img.width, img.height + 90), (250, 250, 248))
    out.paste(head, (0, 0))
    out.paste(img, (0, 90))
    out.save(OUT / "map-tourism.jpg", quality=90)


BUREAU_JA = [("economy", "経済観光文化局"), ("port", "港湾空港局"), ("urban", "住宅都市みどり局"), ("roads", "道路下水道局"),
             ("health", "保健環境局"), ("education", "教育委員会"), ("fire", "消防局"), ("finance", "財政局")]


def bureaus():
    """局ごと・月ごとに、案が採られたか、外れたか、案なしか。"""
    import numpy as np
    from matplotlib.colors import ListedColormap
    grid = np.zeros((len(BUREAU_JA), 24))
    for m in range(1, 25):
        r = json.loads((RUN / "council" / f"m{m:02d}-run.json").read_text())
        took = {x["fromBureau"].split("-")[0] for x in r["bill"]["measures"]}
        for p in r["proposals"]:
            i = [b for b, _ in BUREAU_JA].index(p["bureau"])
            grid[i, m - 1] = 2 if p["bureau"] in took else (1 if p["hasProposal"] else 0)
    cmap = ListedColormap(["#e6e5e1", "#f2b48f", ORANGE])
    fig, ax = plt.subplots(figsize=(13, 5.4), facecolor=BG)
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=2, aspect="auto")
    ax.set_yticks(range(len(BUREAU_JA)))
    ax.set_yticklabels([j for _, j in BUREAU_JA], fontsize=13)
    ax.set_xticks(range(24))
    ax.set_xticklabels([str(i) for i in range(1, 25)], fontsize=11)
    ax.set_xlabel("か月目", fontsize=12)
    ax.set_xticks([x - 0.5 for x in range(25)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(len(BUREAU_JA) + 1)], minor=True)
    ax.grid(which="minor", color="white", lw=2)
    ax.tick_params(which="minor", length=0)
    ax.axvline(11.5, color="#555555", lw=3)
    for sp in ax.spines.values():
        sp.set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ORANGE, label="案が採られた"), Patch(color="#f2b48f", label="案を出したが外れた"),
                       Patch(color="#e6e5e1", label="案なし")], ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, -0.14), frameon=False, fontsize=12)
    ax.set_title("局ごとの案(太い線から右が2年目)", fontsize=16, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "chart-bureaus.png", dpi=110, facecolor=BG)


def budget():
    """13か月目に、市長が週の収支の余裕をどう分けたか(plan-review.md の調整8)。"""
    parts = [("教育の補助(EducationBoost)", 7940, "#d2a032"), ("駅", 960, BLUE), ("公園", 136, GREEN),
             ("道", 12, GRAY), ("残り(名所はこの中で1棟)", 356, ORANGE)]
    fig, ax = plt.subplots(figsize=(12, 3.4), facecolor=BG)
    ax.set_facecolor(BG)
    left = 0
    for name, v, col in parts:
        ax.barh(0, v, left=left, color=col, edgecolor="white", height=0.6)
        if v > 900:
            ax.text(left + v / 2, 0, f"{name}\n週{v:,}", ha="center", va="center", color="white", fontsize=13)
        left += v
    ax.annotate("残り 約356\n名所は週320以下の1棟まで", xy=(9404 - 178, 0.3), xytext=(7300, 0.75), fontsize=12,
                arrowprops=dict(arrowstyle="->", color=GRAY))
    ax.set_xlim(0, 9600)
    ax.set_ylim(-1, 1.1)
    ax.set_yticks([])
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.set_title("13か月目、週の収支の余裕 約9,400 の分け方", fontsize=16, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "chart-budget.png", dpi=110, facecolor=BG)


def goals():
    """観光の目標に、どこまで届いたか。"""
    rows = [("名所", 6, 10, 10, "棟"), ("観光客", 1646, 2048, 3000, "人"), ("訪問の数", None, 179, 250, ""),
            ("観光の週の収入", None, 93, 1000, ""), ("旅客の入口", 0, 0, 1, "つ")]
    fig, ax = plt.subplots(figsize=(12, 4.4), facecolor=BG)
    ax.set_facecolor(BG)
    for i, (name, start, end, goal, unit) in enumerate(rows):
        ratio = min(end / goal, 1.0)
        ax.barh(i, 1.0, color="#e6e5e1", height=0.6)
        ax.barh(i, ratio, color=GREEN if ratio >= 1 else ORANGE, height=0.6)
        head = f"{start:,} → " if start is not None else ""
        ax.text(1.02, i, f"{head}{end:,}{unit}(目標 {goal:,}{unit})", va="center", fontsize=13)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=13)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.6)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(["0%", "50%", "目標"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("2年後、観光の目標にどこまで届いたか(棒は目標に対する割合)", fontsize=16, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "chart-goals.png", dpi=110, facecolor=BG)


def plans():
    """観光に関わる長期計画の事業と、実際の結果。"""
    # (名前, 予定の月の範囲, 実際の月, 結果, できたか)
    rows = [
        ("1年目の計画(1か月目に作成)", None, None, "", None),
        ("名所A・B", (1, 1), [1], "1か月目に2棟", True),
        ("名所の2・3棟目", (2, 6), [5, 11], "5か月目と11か月目", True),
        ("旅客の駅", (1, 3), [], "置けず", False),
        ("島Bに橋と風力", (2, 5), [5], "5か月目に引けた", True),
        ("島Bの名所", (8, 8), [], "水がなく置けず", False),
        ("空き地3の道と電線", (4, 5), [5], "名所に電気が来ず", False),
        ("2年目の計画(13か月目に作り直し)", None, None, "", None),
        ("名所(本土)への道", (13, 15), [13], "13か月目に引けた", True),
        ("教育の補助(EducationBoost)", (13, 16), [13], "13か月目に入れた", True),
        ("名所に電線(17か月目に足す)", (17, 17), [17], "17か月目に電気が来た", True),
        ("名所の試し(1・2棟目)", (15, 21), [22], "22か月目に事業を閉じた", False),
        ("旅客の駅", (14, 18), [24], "24か月目に事業を閉じた", False),
    ]
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG)
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    for i, (name, span, done, note, ok) in enumerate(rows):
        if span is None:
            ax.text(0.4, i, name, fontsize=14, va="center", fontweight="bold", color="#333333")
            continue
        ax.barh(i, span[1] - span[0] + 1, left=span[0] - 0.5, color="#cfd8e8", height=0.55)
        for m in done:
            ax.plot(m, i, marker="o" if ok else "X", ms=13, color=GREEN if ok else "#d2463c")
        if not done:
            ax.plot(span[1] + 0.9, i, marker="X", ms=13, color="#d2463c")
        ax.text(25.3, i, note, fontsize=12, va="center", color=GREEN if ok else "#d2463c")
    ax.set_yticks([i for i, r in enumerate(rows) if r[1] is not None])
    ax.set_yticklabels([r[0] for r in rows if r[1] is not None], fontsize=12)
    ax.invert_yaxis()
    ax.set_xlim(0.3, 31)
    ax.set_xticks(range(1, 25))
    ax.axvline(12.5, color="#888888", lw=1.5, ls="--")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel("か月目", fontsize=12)
    ax.legend(handles=[Patch(color="#cfd8e8", label="計画の予定"),
                       Line2D([], [], marker="o", color=GREEN, ls="", ms=11, label="できた"),
                       Line2D([], [], marker="X", color="#d2463c", ls="", ms=11, label="できなかった・閉じた")],
              ncol=3, loc="upper center", bbox_to_anchor=(0.45, -0.09), frameon=False, fontsize=12)
    ax.set_title("観光に関わる長期計画の事業と、実際", fontsize=16, loc="left", pad=30)
    fig.tight_layout()
    fig.savefig(OUT / "chart-plans.png", dpi=110, facecolor=BG)


def island():
    """島Bの水をめぐる経緯。"""
    ev = [
        ("1か月目", "市長", "島Bの名所は StatueOfWealth(水と下水が要らない)。8か月目に置く計画", "plan"),
        ("5か月目", "道路下水道局", "「StatueOfWealth は水を要らない」。橋・風力・送電線だけ引き、水道管は引かない", "plan"),
        ("5か月目", "市長", "同じ月、空き地3に StatueOfWealth を置く案を採る。1種類1棟なので、島Bの水の要らない名所がなくなる", "bad"),
        ("6か月目", "港湾空港局", "島Bの港は、島の道と水道管が試し待ちなので、案にしない", "wait"),
        ("14か月目", "港湾空港局", "「島Bは水が届かない」。水源・水管・電線の試しを15か月目の予定に入れる", "plan"),
        ("15か月目", "港湾空港局", "水管(本土から35区間)と電線は、試しで通る。整地が未確認", "plan"),
        ("17か月目", "市長", "駅・整地・道・水管・電線の案(51,840)を、条件付きで外す。調べ直し1回では条件がそろわない", "bad"),
        ("24か月目", "港湾空港局", "候補を空き地1に替える。島Bは道の坂", "bad"),
    ]
    colors = {"plan": (60, 120, 200), "wait": (150, 150, 150), "bad": (210, 70, 60)}
    W, RH = 1700, 108
    H = 140 + RH * len(ev) + 30
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    d.text((W // 2, 30), "島Bに水が来なかった経緯", font=f(40, True), fill=(30, 30, 30), anchor="mt")
    d.text((W // 2, 84), "青=計画と試し、赤=前提が崩れた・止まった所", font=f(24), fill=(95, 95, 95), anchor="mt")
    y = 140
    d.line((230, y + 20, 230, y + RH * len(ev) - 40), fill=(190, 190, 190), width=6)
    for when, who, what, kind in ev:
        col = colors[kind]
        cy = y + (RH - 16) // 2
        d.text((190, cy), when, font=f(26, True), fill=(30, 30, 30), anchor="rm")
        d.ellipse((216, cy - 14, 244, cy + 14), fill=col)
        d.rounded_rectangle((270, y, W - 40, y + RH - 16), 12, fill=(240, 239, 236), outline=col, width=3)
        d.text((295, cy), who, font=f(24, True), fill=col, anchor="lm")
        wrap(d, 480, cy, what, 44, f(24), (30, 30, 30))
        y += RH
    img.save(OUT / "diagram-island.png")


def rootcause():
    """ハーネスに乗った手と、乗らなかった手。"""
    W, H = 1700, 1060
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    d.text((W // 2, 30), "ハーネスに乗った手、乗らなかった手", font=f(40, True), fill=(30, 30, 30), anchor="mt")
    cols = [(40, 820, "乗った手(ほぼ毎月、実行できた)", (33, 170, 120),
             "1つの局 × 1か月 × 1回の工事。試しの道具で、その場で確かめられる",
             ["公園を1つ置く(住宅都市みどり局)", "交差点に信号を付ける(道路下水道局)", "道を4車線に広げる(道路下水道局)",
              "埋立地を建て直す(保健環境局)"]),
            (880, 1660, "乗らなかった手(2年間、できなかった)", (210, 70, 60),
             "いくつもの局 × いくつもの月 × いくつもの工程。前の工程が済まないと、次を試せない",
             ["島Bを開く:橋・風力・水管・整地・名所(3局、1〜24か月目)", "旅客の駅:駅・整地・道・水管・電線の5工程",
              "名所に電気を引く:置いた建物の外形に、線が当たる", "名所を増やす:お金の枠と、置く場所の両方が要る"])]
    for x0, x1, head, col, sub, items in cols:
        d.rounded_rectangle((x0, 110, x1, 690), 16, fill=(240, 239, 236), outline=col, width=4)
        d.text(((x0 + x1) // 2, 150), head, font=f(30, True), fill=col, anchor="mm")
        wrap(d, x0 + 30, 230, sub, 30, f(23), (95, 95, 95))
        for i, it in enumerate(items):
            wrap(d, x0 + 50, 340 + i * 88, "・" + it, 30, f(25), (30, 30, 30))
    d.text((W // 2, 740), "乗らなかった手に要って、ハーネスになかったもの", font=f(30, True), fill=(30, 30, 30), anchor="mm")
    lacks = ["月と局をまたぐ「事業」の単位", "前の工程が済んだものとして試す道具", "計画の前提が崩れたら知らせる段",
             "方針の優先順位でお金を取っておく決まり"]
    for i, t in enumerate(lacks):
        x = 40 + (i % 2) * 830
        yy = 790 + (i // 2) * 120
        d.rounded_rectangle((x, yy, x + 790, yy + 96), 14, fill=(255, 255, 255), outline=(120, 90, 160), width=3)
        d.text((x + 395, yy + 48), t, font=f(27, True), fill=(30, 30, 30), anchor="mm")
    img.save(OUT / "diagram-rootcause.png")


if __name__ == "__main__":
    island()
    rootcause()
    plans()
    monthly()
    print(measures())
    harness()
    lessons()
    tourism_map()
    bureaus()
    budget()
    goals()
