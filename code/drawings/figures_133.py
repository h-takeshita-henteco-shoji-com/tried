"""#133 の記事の図を作る。

- plan: 平面図に、扉(赤)と窓(青)の位置を番号で重ねる
- hall: ホールの正しい範囲と、モデルごとの拾い違い
- results: モデルごとの、合計金額の正解との差
- wall: 外壁の室内側の面。平面図は通り芯から 75、平面詳細図は 65
- opus: Opus が作った内訳書(results の 内訳書.md)の表を、そのまま画像にする(note は表を使えないため)

使い方: uv run --with ezdxf --with shapely --with matplotlib --with pillow python code/drawings/figures_133.py
"""
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import ezdxf  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from ezdxf.addons.drawing import Frontend, RenderContext  # noqa: E402
from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration  # noqa: E402
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Polygon as MPoly  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
import estimate_133 as E  # noqa: E402
import make_house as H  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DAY = REPO / "2026/11-07-AIと図面のコラボレーション-07-AIに建具を数えさせて建具表を作る"
OUT = DAY / "assets"
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_R = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
FP = font_manager.FontProperties(fname=FONT)
FPR = font_manager.FontProperties(fname=FONT_R)
RED, BLUE, GREEN, GRAY = "#d03b3b", "#2a6fb0", "#3a8f4f", "#555555"


def draw_dxf(ax, path):
    doc = ezdxf.readfile(path)
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK)
    Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(doc.modelspace())


def plan():
    view = (-1200, -1300, 11300, 8500)
    w = 1600
    fig = plt.figure(figsize=(w / 100, w / 100 * (view[3] - view[1]) / (view[2] - view[0])), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    draw_dxf(ax, DAY / "base/house-t.dxf")
    ops = E.openings()
    nd = nw = 0
    for n, kind, o, at, a, b, h, _ in ops:
        if kind == "扉のない開口":
            continue
        m = (a + b) / 2
        x, y = (m, at) if o == "h" else (at, m)
        door = kind in ("開き戸", "引き戸", "折れ戸")
        if door:
            nd += 1
            label, color = f"D{nd}", RED
        else:
            nw += 1
            label, color = f"W{nw}", BLUE
        ax.text(x, y, label, color="white", fontsize=15, ha="center", va="center", zorder=20, fontproperties=FP,
                bbox=dict(boxstyle="round,pad=0.25", fc=color, ec="none"))
    ax.text(view[0] + 150, view[3] - 350, f"扉 {nd}（赤）  窓 {nw}（青）", fontsize=26, color="#222",
            fontproperties=FP, va="top", zorder=21, bbox=dict(fc="white", ec="none", alpha=0.9))
    ax.set_xlim(view[0], view[2])
    ax.set_ylim(view[1], view[3])
    ax.set_aspect("equal")
    ax.set_axis_off()
    fig.set_size_inches(w / 100, w / 100 * (view[3] - view[1]) / (view[2] - view[0]))
    fig.savefig(OUT / "fig-plan-fixtures.png", dpi=100, facecolor="white")
    plt.close(fig)


def poly_patch(ax, geom, **kw):
    """穴のある形(壁など)も、穴を抜いて描く。"""
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path as MPath
    for g in getattr(geom, "geoms", [geom]):
        verts, codes = [], []
        for ring in [g.exterior, *g.interiors]:
            cs = list(ring.coords)
            verts += cs
            codes += [MPath.MOVETO] + [MPath.LINETO] * (len(cs) - 2) + [MPath.CLOSEPOLY]
        ax.add_patch(PathPatch(MPath(verts, codes), **kw))


def hall():
    from shapely.geometry import box
    view = (4100, 1500, 7700, 5900)
    fig, ax = plt.subplots(figsize=(13, 13 * (view[3] - view[1]) / (view[2] - view[0])), dpi=100)
    fig.subplots_adjust(0, 0, 1, 1)
    poly_patch(ax, E.WALLS, fc="#bbbbbb", ec="none", zorder=1)
    hall_poly = E.inner("ホール")
    poly_patch(ax, hall_poly, fc="#dcefdc", ec=GREEN, lw=3, zorder=2)
    toilet = E.inner("トイレ")
    poly_patch(ax, toilet, fc="#f6d6d6", ec=RED, lw=3, ls="--", zorder=3)
    corridor = box(6310, 3700, 7220, 4490)
    poly_patch(ax, corridor, fc="none", ec=BLUE, lw=4, ls=":", zorder=4)
    strip = box(5520, 5400, 6310, 5520)
    poly_patch(ax, strip, fc=RED, ec=RED, lw=2, zorder=4, alpha=0.8)
    # 玄関との境(上がり框)
    ax.plot([4610, 6310], [1820, 1820], color=GREEN, lw=3, ls="--", zorder=5)
    kw = dict(fontproperties=FP, zorder=10)
    ax.text(5450, 2650, "ホール 5.15m²\n（正解）", ha="center", va="center", fontsize=24, color=GREEN, **kw)
    ax.text(5000, 4500, "トイレ\n1.34m²", ha="center", va="center", fontsize=20, color=RED, **kw)
    ax.text(4150, 3600, "Fable：\nトイレも\nホールに\n入れた", ha="left", va="center", fontsize=17, color=RED, **kw)
    ax.text(6765, 4095, "寝室2の前\nの通路", ha="center", va="center", fontsize=17, color=BLUE, **kw)
    ax.text(6765, 3250, "Argon の1つめの版：\nここを落とした", ha="center", va="center", fontsize=16, color=BLUE, **kw)
    ax.text(6400, 5720, "Flash：壁の厚み120も床に入れた", ha="left", va="center", fontsize=16, color=RED, **kw)
    ax.annotate("", xy=(6000, 5470), xytext=(6450, 5700), arrowprops=dict(arrowstyle="->", color=RED, lw=2), zorder=10)
    ax.text(5460, 1200, "玄関", ha="center", va="center", fontsize=20, color=GRAY, **kw)
    ax.text(6900, 2400, "寝室1", ha="center", va="center", fontsize=20, color=GRAY, **kw)
    ax.text(6900, 5300, "寝室2", ha="center", va="center", fontsize=20, color=GRAY, **kw)
    ax.text(5460, 1650, "上がり框（玄関との境。壁はない）", ha="center", va="top", fontsize=15, color=GREEN, **kw)
    ax.set_xlim(view[0], view[2])
    ax.set_ylim(view[1], view[3])
    ax.set_aspect("equal")
    ax.set_axis_off()
    fig.savefig(OUT / "fig-hall.png", dpi=100, facecolor="white")
    plt.close(fig)


def results():
    rows = [  # 答えを読んで確かめた値(log.md の結果 7)
        ("Claude Opus 5.5", 0, "全室が正解と同じ"),
        ("Claude Sonnet 5.5", 0, "全室が正解と同じ"),
        ("Gemini 4 Argon", 0, "最後の版は正解と同じ（途中に誤った版）"),
        ("GPT-6.1 Sol", -733, "壁の面を芯から65で拾った（判断の違い）"),
        ("Gemini 3.8 Flash", 1294, "ホール：壁の厚みを床に入れた"),
        ("Claude Fable 5.1", 14571, "ホール：トイレの床を二重に拾った"),
        ("Claude Haiku 5.5", -7301, "格子で測った約値、扉の幅の取り違え"),
    ]
    fig, ax = plt.subplots(figsize=(15, 6.2), dpi=100)
    fig.subplots_adjust(left=0.2, right=0.97, top=0.86, bottom=0.12)
    ys = list(range(len(rows)))[::-1]
    for y, (n, v, note) in zip(ys, rows):
        color = "#9aa5b1" if v == 0 else (RED if abs(v) > 5000 else "#e0a050")
        ax.barh(y, v if v else 0, height=0.55, color=color)
        if v == 0:
            ax.plot([0], [y], marker="o", ms=11, color=GREEN)
        sx = 300 if v >= 0 else -300
        txt = f"{v:+,} 円　{note}" if v else f"±0 円　{note}"
        ax.text(max(v, 0) + 300 if v >= 0 else 300, y, txt, va="center", ha="left", fontsize=15, fontproperties=FPR)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontproperties=FP, fontsize=16)
    ax.axvline(0, color="#333", lw=1.2)
    ax.set_xlim(-9000, 34000)
    ax.set_xlabel("正解（3,255,807 円）との差（円）", fontproperties=FPR, fontsize=15)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e5e5e5")
    ax.set_axisbelow(True)
    fig.text(0.02, 0.94, "内装と建具の見積の合計。正解との差", fontproperties=FP, fontsize=20)
    fig.savefig(OUT / "fig-results.png", dpi=100, facecolor="white")
    plt.close(fig)


def wall():
    fig, ax = plt.subplots(figsize=(14, 5.4), dpi=100)
    fig.subplots_adjust(0.02, 0.05, 0.98, 0.9)
    kw = dict(fontproperties=FP)
    # 上: 平面図(壁厚 150 の帯)
    ax.add_patch(plt.Rectangle((-75, 2.2), 150, 0.9, fc="#cccccc", ec="#333"))
    ax.text(-260, 2.65, "平面図\n（1/100）", ha="right", va="center", fontsize=18, **kw)
    ax.annotate("", xy=(-75, 3.35), xytext=(0, 3.35), arrowprops=dict(arrowstyle="<->", lw=2))
    ax.text(-37, 3.5, "75", ha="center", fontsize=18, color=RED, **kw)
    # 下: 平面詳細図(柱 105 + 石膏ボード 12.5、外側は合板・胴縁・サイディング)
    layers = [(-65, 12.5, "#f2e6c9", ""), (-52.5, 105, "#d9b38c", "柱 105"),
              (52.5, 9, "#c9a77a", ""), (61.5, 18, "#a9c4e0", ""), (79.5, 14, "#8fa7c2", "")]
    for x, wdt, c, t in layers:
        ax.add_patch(plt.Rectangle((x, 0.4), wdt, 0.9, fc=c, ec="#333"))
        if t:
            ax.text(x + wdt / 2, 0.85, t, ha="center", va="center", fontsize=14, **kw)
    ax.annotate("石膏ボード 12.5", xy=(-58, 1.3), xytext=(-150, 1.75), fontsize=14, ha="center",
                arrowprops=dict(arrowstyle="->", lw=1.5), **kw)
    ax.text(-260, 0.85, "平面詳細図\n（1/50）", ha="right", va="center", fontsize=18, **kw)
    ax.annotate("", xy=(-65, 0.15), xytext=(0, 0.15), arrowprops=dict(arrowstyle="<->", lw=2))
    ax.text(-32, -0.15, "65", ha="center", va="top", fontsize=18, color=RED, **kw)
    ax.axvline(0, color=RED, lw=1.5, ls="-.")
    ax.text(0, 3.9, "通り芯", ha="center", fontsize=16, color=RED, **kw)
    ax.text(-300, 1.85, "← 室内", ha="center", fontsize=15, color=GRAY, **kw)
    ax.text(110, 1.85, "屋外 →", ha="center", fontsize=15, color=GRAY, **kw)
    ax.text(150, 1.7, "75で拾った:\n  Opus、Sonnet、Fable、Haiku、Flash、Argon\n"
            "65で拾った: GPT\n違いの確認を求めた: Opus、GPT、Argon",
            ha="left", va="center", fontsize=15, **dict(fontproperties=FPR))
    ax.set_xlim(-420, 700)
    ax.set_ylim(-0.6, 4.2)
    ax.set_axis_off()
    fig.text(0.02, 0.94, "外壁の室内側の面。通り芯からの距離が、図によって違う", fontsize=19, **kw)
    fig.savefig(OUT / "fig-wall-75-65.png", dpi=100, facecolor="white")
    plt.close(fig)


OPUS = DAY / "results/2026-11-07/T-dxf/claude-opus-5-5__medium/T-5-1-files/内訳書.md"


def md_tables(path):
    """見出し(## n.) ごとに、表の行(セルの並び)を返す。"""
    out, head, rows = {}, None, []
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            if head and rows:
                out[head] = rows
            head, rows = line[3:].strip(), []
        elif line.startswith("|") and not set(line) <= set("|-: "):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    if head and rows:
        out[head] = rows
    return out


def table_image(title, rows, width=1600, note=None):
    from PIL import Image, ImageDraw, ImageFont
    f_b, f_r, f_t = ImageFont.truetype(FONT, 24), ImageFont.truetype(FONT_R, 24), ImageFont.truetype(FONT, 30)
    clean = [[c.replace("**", "") for c in r] for r in rows]
    bold = [any("**" in c for c in r) for r in rows]
    num = [all(re.fullmatch(r"[\d,.—–\-]*", r[i].replace("**", "")) for r in rows[1:] if i < len(r))
           for i in range(len(rows[0]))]
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    pad = 18
    cw = [max(d0.textlength(r[i], font=f_b) for r in clean if i < len(r)) + pad * 2 for i in range(len(clean[0]))]
    scale = min(1.0, (width - 40) / sum(cw))
    if scale < 1:   # はみ出すときは、いちばん広い列(文字の列)を折り返さずに縮める代わりに、字を小さくする
        f_b, f_r = ImageFont.truetype(FONT, int(24 * scale)), ImageFont.truetype(FONT_R, int(24 * scale))
        cw = [max(d0.textlength(r[i], font=f_b) for r in clean if i < len(r)) + pad * 2 for i in range(len(clean[0]))]
    rh = int(f_b.size * 2.0)
    top = 70
    H = top + rh * len(clean) + (50 if note else 20)
    W = int(sum(cw)) + 40
    im = Image.new("RGB", (max(W, width), H), "white")
    d = ImageDraw.Draw(im)
    d.text((20, 18), title, font=f_t, fill="#222")
    y = top
    for k, (r, b) in enumerate(zip(clean, bold)):
        if k == 0:
            d.rectangle([20, y, 20 + sum(cw), y + rh], fill="#eef1f5")
        elif b:
            d.rectangle([20, y, 20 + sum(cw), y + rh], fill="#f7f3e8")
        x = 20
        for i, c in enumerate(r):
            f = f_b if (k == 0 or b) else f_r
            tw = d.textlength(c, font=f)
            tx = x + cw[i] - pad - tw if (num[i] and k > 0) else x + pad
            d.text((tx, y + (rh - f.size) / 2 - 2), c, font=f, fill="#222")
            x += cw[i]
        d.line([20, y + rh, 20 + sum(cw), y + rh], fill="#d0d4da", width=1)
        y += rh
    if note:
        d.text((20, y + 14), note, font=ImageFont.truetype(FONT_R, 20), fill="#666")
    return im


def opus():
    t = md_tables(OPUS)
    src = "Claude Opus 5.5 が作った内訳書（内訳書.md）の表を、そのまま画像にした"
    table_image("部屋ごとの数量", t["1. 部屋ごとの数量"], note=src).save(OUT / "fig-opus-rooms.png")
    table_image("材料ごとの合計と金額", t["2. 材料ごとの合計と金額"], note=src).save(OUT / "fig-opus-materials.png")
    table_image("建具表と金額", t["3. 建具表と金額"], note=src).save(OUT / "fig-opus-fixtures.png")


if __name__ == "__main__":
    for f in (sys.argv[1:] or ["plan", "hall", "results", "wall"]):
        globals()[f]()
        print(f)
