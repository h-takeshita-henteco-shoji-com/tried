"""#132 の記事の「結果」に使う図を作る。

- question-chart.png: 問い別の点数（10のLLMの合計、DXFと画像）
- grade-breakdown.png: LLM別の判定の内訳（2枚の図面・2つの渡し方の合計56問）
- dxf-vs-image.png: 同じ扉を、人が見る絵と、LLMが受け取るDXFの中身で並べる
- crop-*.png: 図面の該当箇所の切り抜き（赤い枠付き）

使い方: uv run --with matplotlib --with ezdxf --with pillow python result_figures.py
"""
import collections
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import ezdxf
import matplotlib.pyplot as plt
from ezdxf import bbox
from matplotlib import font_manager
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
DAY = REPO / "2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる"
RESULTS = DAY / "results/2026-11-01"
DRAW = DAY / "assets/drawings/建築工事標準詳細図"
OUT = DAY / "assets"
TEXT, MUTED, SURFACE, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e0"
SERIES = [("dxf", "DXF", "#2a78d6"), ("png", "画像", "#eb6834")]
OK = {"正答", "適切な保留"}
MODELS = [
    ("claude-haiku-5-5", "Claude Haiku 5.5"), ("claude-sonnet-5-5", "Claude Sonnet 5.5"),
    ("claude-opus-5-5", "Claude Opus 5.5"), ("claude-fable-5-1", "Claude Fable 5.1"),
    ("gpt-6-luna", "GPT-6 Luna"), ("gpt-6.1-terra", "GPT-6.1 Terra"),
    ("gpt-6.1-sol", "GPT-6.1 Sol"), ("gpt-6-astra", "GPT-6 Astra"),
    ("gemini-3.8-flash", "Gemini 3.8 Flash"), ("gemini-4-argon", "Gemini 4 Argon"),
]
QUESTIONS = {
    "L": [("L-1-1", "何の図面か（易）"), ("L-1-2", "建具の区分（中）"), ("L-2-1", "ガラスなし両開き扉（易）"),
          ("L-2-2", "片上げ下げ窓（中）"), ("L-2-3", "がらり付き親子開き（難）"), ("L-3-1", "樹脂製で外倒し（中）"),
          ("L-3-2", "すべり出し＋らんま（難）"), ("L-3-3", "倉庫の扉のがらり（難）"), ("L-4-1", "車いすの扉の幅（易）"),
          ("L-4-2", "引き戸と標準寸法（中）"), ("L-4-3", "子扉の幅と高さ（難）"), ("L-5-1", "A-1の材質（易）"),
          ("L-5-2", "A-4のがらりの型（中）"), ("L-5-3", "A-3の扉の幅（難）")],
    "H": [("H-1-1", "何の図面か（易）"), ("H-1-2", "戸車はどの図か（中）"), ("H-2-1", "施錠の道具（易）"),
          ("H-2-2", "上部の支え（中）"), ("H-2-3", "縦格子の部材（易）"), ("H-3-1", "平面図のA・B・C（中）"),
          ("H-3-2", "幅4,500mmの戸車（難）"), ("H-3-3", "雨水の抜き方（難）"), ("H-4-1", "鉄部の塗装（易）"),
          ("H-4-2", "摺車の仕様（中）"), ("H-4-3", "門柱の仕上げ（難）"), ("H-5-1", "引き戸の幅（易）"),
          ("H-5-2", "めっきの有無（中）"), ("H-5-3", "戸が寄る部分の基礎（難）")],
}
GRADES = [("正答", "正答（適切な保留を含む）", "#0ca30c"), ("部分正答", "部分正答", "#fab219"),
          ("誤答", "誤答", "#d03b3b"), ("誤った断定", "誤った断定", "#ec835a"),
          ("不要な保留", "不要な保留", "#8f8d87")]


def setup_font():
    for f in font_manager.findSystemFonts():
        if "NotoSansJP" in f:
            font_manager.fontManager.addfont(f)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name()


def grades():
    out = []
    for d in ("L", "H"):
        out += json.load(open(RESULTS / f"grades-{d}-medium.json"))
    return out


def style(ax):
    ax.set_facecolor(SURFACE)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#c9c8c2")
    ax.tick_params(colors=MUTED, length=0)


def question_chart(g):
    s = collections.defaultdict(float)
    for x in g:
        s[(x["qid"], x["format"])] += 1 if x["grade"] in OK else 0.5 if x["grade"] == "部分正答" else 0
    fig, axes = plt.subplots(1, 2, figsize=(13, 8), facecolor=SURFACE)
    titles = {"L": "易しい図面（4-01 建具：形状寸法）", "H": "難しい図面（9-32 門：引き戸）"}
    h = 0.36
    for ax, d in zip(axes, ("L", "H")):
        qs = QUESTIONS[d]
        for i, (q, _) in enumerate(qs):
            y = len(qs) - 1 - i
            for j, (fmt, _, c) in enumerate(SERIES):
                v = s[(q, fmt)]
                yy = y + (h / 2 + 0.02) * (1 if j == 0 else -1)
                ax.barh(yy, v, height=h, color=c)
                ax.text(v + 0.12, yy, f"{v:g}", va="center", fontsize=8, color=MUTED)
        ax.set_yticks(range(len(qs)))
        ax.set_yticklabels([n for _, n in reversed(qs)], fontsize=10, color=TEXT)
        ax.set_xlim(0, 11)
        ax.set_xticks([0, 2, 4, 6, 8, 10])
        ax.set_xlabel("点数（10のLLMの合計、10点満点）", color=MUTED)
        ax.set_title(titles[d], loc="left", fontsize=12, color=TEXT)
        style(ax)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in SERIES]
    fig.legend(handles, [l for _, l, _ in SERIES], loc="upper right", ncol=2, frameon=False, fontsize=11)
    fig.suptitle("問い別の点数", x=0.02, ha="left", fontsize=15, color=TEXT)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(OUT / "question-chart.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def grade_breakdown(g):
    c = collections.defaultdict(collections.Counter)
    for x in g:
        k = "正答" if x["grade"] in OK else x["grade"]
        c[x["model"]][k] += 1
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=SURFACE)
    for i, (m, name) in enumerate(MODELS):
        y = len(MODELS) - 1 - i
        left = 0
        for k, _, col in GRADES:
            v = c[m][k]
            if v:
                ax.barh(y, v - 0.08, left=left, height=0.62, color=col)
                if v >= 2:
                    ax.text(left + v / 2, y, str(v), ha="center", va="center", fontsize=9,
                            color="#ffffff" if k in ("正答", "誤答") else TEXT)
            left += v
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels([n for _, n in reversed(MODELS)], fontsize=11, color=TEXT)
    ax.set_xlim(0, 56)
    ax.set_xticks([0, 14, 28, 42, 56])
    ax.set_xlabel("答えの件数（2枚の図面 × 14問 × DXF・画像 = 56件）", color=MUTED)
    style(ax)
    handles = [plt.Rectangle((0, 0), 1, 1, color=col) for _, _, col in GRADES]
    fig.legend(handles, [l for _, l, _ in GRADES], loc="upper center", ncol=5, frameon=False,
               fontsize=10, bbox_to_anchor=(0.55, 0.93))
    fig.suptitle("LLM別の判定の内訳", x=0.02, ha="left", fontsize=15, color=TEXT)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(OUT / "grade-breakdown.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def to_disp(ext, x, y, w=2000):
    """DXFの座標を、PNGと同じ「幅2000」の表示座標に変える。"""
    s = w / ext.size.x
    return (x - ext.extmin.x) * s, (ext.extmax.y - y) * s


def crop_boxes(png, region, boxes, out, width=1800):
    im = Image.open(png).convert("RGB")
    f = im.size[0] / 2000
    x0, y0, x1, y1 = region
    c = im.crop(tuple(int(v * f) for v in region))
    d = ImageDraw.Draw(c)
    for b in boxes:
        d.rectangle(((b[0] - x0) * f, (b[1] - y0) * f, (b[2] - x0) * f, (b[3] - y0) * f),
                    outline=(220, 0, 0), width=max(4, int(4 * f)))
    c.thumbnail((width, width))
    c.save(out)


def dxf_vs_image():
    """A-3 の扉を、絵（左）と DXF の中身（右）で並べる。"""
    dxf = DRAW / "001126048-p09.dxf"
    png = DRAW / "001126048-p09.png"
    doc = ezdxf.readfile(dxf)
    msp = doc.modelspace()
    ext = bbox.extents(msp, fast=True)
    # 範囲は DXF の中の「A-3」の文字の位置から決める（扉の図は、この文字の下にある）
    label = next(e for e in msp.query("TEXT") if e.dxf.text == "A-3")
    lb = bbox.extents([label])
    cx = (lb.extmin.x + lb.extmax.x) / 2
    x0, x1, y0, y1 = cx - 8.5, cx + 11, lb.extmin.y - 33, lb.extmin.y - 3
    lines = []
    for e in msp.query("LWPOLYLINE TEXT"):
        b = bbox.extents([e], fast=True)
        if not b.has_data:
            continue
        if b.extmin.x >= x0 and b.extmax.x <= x1 and b.extmin.y >= y0 and b.extmax.y <= y1:
            if e.dxftype() == "TEXT":
                lines.append((999, f'TEXT "{e.dxf.text}"'))
            else:
                pts = [f"({p[0]:.1f}, {p[1]:.1f})" for p in e.get_points("xy")][:3]
                size = max(b.size.x, b.size.y)
                lines.append((size, "LWPOLYLINE " + " → ".join(pts) + (" …" if len(e) > 3 else "")))
    lines = [t for _, t in sorted(lines, key=lambda x: -x[0])]  # 大きい図形から並べる
    im = Image.open(png).convert("RGB")
    f = im.size[0] / 2000
    pic = im.crop(tuple(int(v * f) for v in (436, 228, 530, 412)))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 6), facecolor=SURFACE,
                                  gridspec_kw={"width_ratios": [1, 2.2]})
    a1.imshow(pic)
    a1.axis("off")
    a1.set_title("人が見る図（A-3）", loc="left", fontsize=12, color=TEXT)
    a2.axis("off")
    a2.set_title(f"LLMが受け取るDXFの中身（同じ範囲の図形 {len(lines)} 個。大きいものから）", loc="left",
                 fontsize=12, color=TEXT)
    body = "\n".join(lines[:22]) + ("\n…" if len(lines) > 22 else "")
    a2.text(0, 1, body, va="top", ha="left", family="monospace", fontsize=8.5, color=TEXT,
            transform=a2.transAxes)
    fig.tight_layout()
    fig.savefig(OUT / "dxf-vs-image.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def crops():
    p09 = DRAW / "001126048-p09.png"
    p15 = DRAW / "001126051-p15.png"
    # すべり出しの名前は C-8 の下にあるが、DXF では上の C-2 と同じ縦の並びに入っている
    crop_boxes(p09, (200, 655, 810, 1150), [(340, 655, 435, 890), (340, 890, 435, 1125)],
               OUT / "crop-c2-c8.png")
    # 車いすの扉の幅の答えは、表の横の備考 1）にある
    crop_boxes(p09, (1440, 655, 1800, 1130), [(1615, 760, 1795, 820)], OUT / "crop-note-1.png")
    # 立面図。開いたときの戸と戸車が破線で描かれ、その下にもレールが続く
    crop_boxes(p15, (150, 130, 700, 500), [(230, 185, 380, 450)], OUT / "crop-open-door.png")


def main():
    setup_font()
    g = grades()
    question_chart(g)
    grade_breakdown(g)
    dxf_vs_image()
    crops()
    print("ok")


if __name__ == "__main__":
    main()
