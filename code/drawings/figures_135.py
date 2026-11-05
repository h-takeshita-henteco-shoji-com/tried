"""#135 の記事に使う図を作る。

- task-map.png: C-1〜C-3 で変える場所を、平面図の上に色で示す
- table-must-move.png: 課題ごとに、一緒に直すべきもの
- table-scores.png: モデル別の判定
- table-c3-misses.png: C-3 の直し漏れの型
- librecad-c3-east.png、librecad-c3-plan.png: LibreCAD で開いた正解・Argon・Haiku を並べ、違う数字を赤で囲む

判定は results/2026-11-02/grades-C.json から読む。LibreCAD の画面は assets/librecad/ の、人が撮ったスクリーンショット。

使い方: uv run --with matplotlib --with ezdxf --with pillow python figures_135.py
"""
import json
from pathlib import Path

import ezdxf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.config import ColorPolicy, Configuration
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from matplotlib.patches import Rectangle
from PIL import Image, ImageDraw, ImageFont

from answer_tables import GRADE_COLOR, HEAD, LINE, MUTED, SURFACE, TEXT, wrap
from result_figures import setup_font

REPO = Path(__file__).resolve().parents[2]
DAY = REPO / "2026/11-02-AIと図面のコラボレーション-03-AIにDXFの寸法を変更させる"
OUT = DAY / "assets"
SHOT = OUT / "librecad"
RED = (208, 59, 59)
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
NAMES = {
    "claude-haiku-5-5": "Claude Haiku 5.5", "claude-sonnet-5-5": "Claude Sonnet 5.5",
    "claude-opus-5-5": "Claude Opus 5.5", "claude-fable-5-1": "Claude Fable 5.1",
    "gpt-6-luna": "GPT-6 Luna", "gpt-6.1-terra": "GPT-6.1 Terra", "gpt-6.1-sol": "GPT-6.1 Sol",
    "gpt-6-astra": "GPT-6 Astra", "gemini-3.8-flash": "Gemini 3.8 Flash", "gemini-4-argon": "Gemini 4 Argon",
}


def task_map():
    """元の平面図に、C-1〜C-3 で変える場所を色で重ねる。"""
    doc = ezdxf.readfile(OUT / "drawings/house-2ldk.dxf")
    panels = [
        ("C-1 窓を広げる", [((4150, -400, 4320, 400), "#eb6834")],
         "LDKの南の東側の窓を、右へ170mm広げる"),
        ("C-2 寝室1を広げる", [((10010, -400, 10920, 7680), "#eb6834")],
         "東の外壁を910mm東へ動かす。寝室2も広がる"),
        ("C-3 LDKを広げる", [((-400, 5460, 10410, 5915), "#eb6834")],
         "Y5より北を455mm北へ動かす。屋根も高くなる"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(18, 6.6), facecolor="white")
    for ax, (title, boxes, note) in zip(axes, panels):
        cfg = Configuration(color_policy=ColorPolicy.BLACK)  # 白い背景で、白い線(色 7)も見えるように
        Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(
            doc.modelspace(), finalize=False,
            filter_func=lambda e: e.dxf.layer in ("WALL", "DOOR", "WINDOW", "FIXTURE", "TEXT"))
        for (x0, y0, x1, y1), c in boxes:
            ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=c, alpha=0.35, edgecolor=c, lw=2))
        ax.set_xlim(-700, 11300)
        ax.set_ylim(-3300, 8200)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=15, loc="left", color=TEXT)
        ax.text(-600, -2800, note, fontsize=12, color=TEXT, va="top")
    fig.tight_layout()
    fig.savefig(OUT / "task-map.png", dpi=130, facecolor="white")
    plt.close(fig)


def table(fname, title, cols, rows, widths, colors=None, size=(13, None)):
    """簡単な表を画像にする。colors は、行ごとに色の印を付ける列の番号と、値から色を返す辞書。"""
    cell = [[wrap(str(v), n) for v, n in zip(r, [w[1] for w in widths])] for r in rows]
    heights = [max(c.count("\n") + 1 for c in row) for row in cell]
    unit = 0.34
    total = 0.9 + unit * (1 + sum(h + 0.5 for h in heights))
    fig = plt.figure(figsize=(size[0], total), facecolor=SURFACE)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(0, 1)
    ax.set_ylim(total, 0)
    ax.axis("off")
    ax.text(0, 0.2, title, fontsize=13, color=TEXT, va="top", weight="bold")
    y = 0.85
    xs = [0]
    for w, _ in widths:
        xs.append(xs[-1] + w)
    ax.add_patch(Rectangle((0, y), 1, unit, facecolor=HEAD, edgecolor="none"))
    for name, x0 in zip(cols, xs):
        ax.text(x0 + 0.008, y + unit / 2, name, fontsize=10.5, color=TEXT, va="center")
    y += unit
    for row, h in zip(cell, heights):
        rh = unit * (h + 0.5)
        ax.plot([0, 1], [y + rh, y + rh], color=LINE, linewidth=1)
        for i, (v, x0) in enumerate(zip(row, xs)):
            dx = 0.008
            if colors and i in colors and v in colors[i]:
                ax.add_patch(Rectangle((x0 + 0.006, y + rh / 2 - 0.13), 0.008, 0.26, facecolor=colors[i][v],
                                       edgecolor="none"))
                dx = 0.02
            ax.text(x0 + dx, y + rh / 2, v, fontsize=10, color=TEXT, va="center", linespacing=1.5)
        y += rh
    fig.savefig(OUT / fname, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def tables():
    table("table-must-move.png", "課題ごとに、一緒に直すべきもの",
          ["課題", "平面図", "立面図", "断面図"],
          [["C-1 窓を広げる", "窓の線、壁の開口", "南立面図の窓", "なし"],
           ["C-2 寝室1を広げる", "東の外壁、通り芯X8、東の窓2つ、寝室2のクローゼット、寝室1のクローゼットを伸ばす、寸法",
            "南・北立面図の幅と屋根の長さ、東立面図の位置", "B-B断面図の寝室1の幅"],
           ["C-3 LDKを広げる", "Y5より北の壁・扉・窓・設備、通り芯Y5・Y6、キッチンの背面と冷蔵庫、寸法",
            "東・西立面図の幅、棟の高さ（4,856→4,947）、北立面図", "A-A断面図の奥行と棟の高さ、B-B断面図の奥の屋根"],
           ["C-4 両立しない指示", "直さない（確認を求める）", "直さない", "直さない"]],
          [(0.17, 12), (0.38, 26), (0.27, 18), (0.18, 12)])
    g = json.load(open(DAY / "results/2026-11-02/grades-C.json"))
    by = {}
    for r in g:
        by.setdefault(r["model"], {})[r["qid"]] = r["grade"]
    pts = {"正答": 1, "適切な保留": 1, "部分正答": 0.5}
    rows = [[NAMES[m], *(d[q] for q in ("C-1-1", "C-2-1", "C-3-1", "C-4-1")),
             f"{sum(pts.get(v, 0) for v in d.values()):g}"] for m, d in by.items()]
    table("table-scores.png", "モデル別の判定（4点満点。正答と適切な保留は1点、部分正答は0.5点）",
          ["モデル", "C-1 窓", "C-2 寝室1", "C-3 LDK", "C-4 衝突", "点"], rows,
          [(0.24, 20), (0.15, 8), (0.15, 8), (0.15, 8), (0.15, 8), (0.16, 6)],
          colors={i: GRADE_COLOR for i in (1, 2, 3, 4)})
    table("table-c3-misses.png", "C-3（LDKを広げる）で、AIが残したもの",
          ["モデル", "判定", "残したもの"],
          [["Claude Sonnet 5.5、Opus 5.5", "正答", "なし。棟の高さまで直した"],
           ["Claude Fable 5.1", "部分正答", "壁と屋根は正しい。通り芯Y5の線と、それを測る寸法を動かさなかった"],
           ["Gemini 3.8 Flash", "部分正答", "立面図と断面図は正しい。トイレの引き戸の横の壁が455mm欠け、開口が広がった"],
           ["Gemini 4 Argon", "部分正答", "形は正しい。寸法の部品に古い値が残り、CADで開くと910、7,280、4,856と出る"],
           ["Claude Haiku 5.5", "誤答", "奥行は7,735にしたが、広げたのはLDKではなく浴室の列。畳数だけを約17畳に書き換えた"],
           ["GPT 4つ", "適切な保留", "保存せず、屋根の扱い（棟が北へ227.5mm、上へ91mm動く）を確認した"]],
          [(0.25, 18), (0.15, 8), (0.60, 44)], colors={1: GRADE_COLOR})


def circled(path, marks, label, width=1400):
    """スクリーンショットに赤い丸を付け、上に見出しを足す。marks は、幅 2000 に縮めたときの座標と半径。"""
    im = Image.open(path).convert("RGB")
    s = im.width / 2000
    d = ImageDraw.Draw(im)
    for x, y, r in marks:
        d.ellipse(((x - r) * s, (y - r * 0.6) * s, (x + r) * s, (y + r * 0.6) * s), outline=RED, width=int(7 * s))
    im = im.resize((width, round(im.height * width / im.width)))
    head = Image.new("RGB", (width, 70), "white")
    ImageDraw.Draw(head).text((20, 16), label, font=ImageFont.truetype(FONT, 30), fill=(20, 20, 20))
    out = Image.new("RGB", (width, im.height + 70), "white")
    out.paste(head, (0, 0))
    out.paste(im, (0, 70))
    return out


def stack(images, fname):
    w = max(i.width for i in images)
    out = Image.new("RGB", (w, sum(i.height for i in images) + 20 * (len(images) - 1)), "white")
    y = 0
    for i in images:
        out.paste(i, (0, y))
        y += i.height + 20
    out.save(OUT / fname)


def librecad():
    # 動画用に、1枚ずつの画像も書き出す(縦に並べた図は、横長の画面では小さすぎるため)
    singles = {
        "video-expected-east.png": ("expected-C-3-east.png", [(405, 290, 55), (340, 475, 55), (1180, 993, 70), (1025, 1048, 70)],
                                    "正解: 屋根 1,697・4,947、Y4〜Y5 1,365、奥行 7,735"),
        "video-argon-east.png": ("argon-C-3-east.png", [(465, 355, 55), (405, 512, 55), (1133, 962, 60), (1000, 1010, 70)],
                                 "Gemini 4 Argon: 形は広がったのに、数字は元のまま"),
        "video-haiku-east.png": ("haiku-C-3-east.png", [(350, 238, 55), (275, 432, 55), (1152, 985, 60), (1345, 985, 70)],
                                 "Claude Haiku 5.5: 広げたのは Y5〜Y6（2,275）。屋根の高さは元のまま"),
        "video-expected-plan.png": ("expected-C-3-plan.png", [(405, 545, 60), (365, 660, 60)],
                                    "正解: Y4〜Y5（LDKの北の端）1,365、奥行 7,735"),
        "video-haiku-plan.png": ("haiku-C-3-plan.png", [(522, 452, 60), (522, 572, 55), (790, 818, 70)],
                                 "Claude Haiku 5.5: Y5〜Y6 が 2,275、Y4〜Y5 は 910。LDKは約17畳"),
    }
    for out, (src, marks, label) in singles.items():
        circled(SHOT / src, marks, label, width=1800).save(OUT / out)
    stack([circled(SHOT / "expected-C-3-east.png", [(405, 290, 55), (340, 475, 55), (1180, 993, 70), (1025, 1048, 70)],
                   "正解: 屋根 1,697・4,947、Y4〜Y5 1,365、奥行 7,735"),
           circled(SHOT / "argon-C-3-east.png", [(465, 355, 55), (405, 512, 55), (1133, 962, 60), (1000, 1010, 70)],
                   "Gemini 4 Argon: 形は広がったのに、数字は元のまま"),
           circled(SHOT / "haiku-C-3-east.png", [(350, 238, 55), (275, 432, 55), (1152, 985, 60), (1345, 985, 70)],
                   "Claude Haiku 5.5: 広げたのは Y5〜Y6（2,275）。屋根の高さは元のまま")],
          "librecad-c3-east.png")
    stack([circled(SHOT / "expected-C-3-plan.png", [(405, 545, 60), (365, 660, 60)],
                   "正解: Y4〜Y5（LDKの北の端）1,365、奥行 7,735"),
           circled(SHOT / "argon-C-3-plan.png", [(605, 515, 55), (567, 618, 60)],
                   "Gemini 4 Argon: Y4〜Y5 が 910、奥行 7,280 と出る"),
           circled(SHOT / "haiku-C-3-plan.png", [(522, 452, 60), (522, 572, 55), (790, 818, 70)],
                   "Claude Haiku 5.5: Y5〜Y6 が 2,275、Y4〜Y5 は 910。LDKは約17畳")],
          "librecad-c3-plan.png")


if __name__ == "__main__":
    setup_font()
    task_map()
    tables()
    librecad()
    print("ok")
