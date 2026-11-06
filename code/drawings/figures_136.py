"""#136 の課題1(矩計図)の記事に使う図を作る。

ルールの採点(check_k1.py)は、値があるかしか見ない。読みやすさや描き込みの量は、画像で人が見る。
図面は白い背景に黒の線で描き、指摘したい所を赤い枠で囲む。

- kanabakari-opus-mcp.png: 録画した Opus の矩計図(記事の図と、へんロボの動画のタイトル画面の背景)
- compare-K-1-mcp.jpg、compare-K-1-dxf.jpg: モデルごとの矩計図を並べる
- fig-conditions.png: 元の図面のどこを参考に、どこへ描き足させたか
- fig-behavior.png: モデルごとに、描いたか、確認したいことを書いたか
- fig-wall.png: 外壁の厚みの食い違い(既存の平面図 150 と、仕様の積み上げ 158.5)
- fig-floor.png: 土台と大引の高さの関係(Opus が DXF で描いた図)
- fig-insulation.png: 同じ Opus の、MCP と DXF の描き込みの差
- fig-dims-viewer.png: 同じファイル(Opus の DXF)の寸法を、ezdxf と LibreCAD で開いたときの違い
  (LibreCAD の画面写真は code/librecad-mcp/shoot_136.py で撮る)
- fig-dimpoints.jpg: 高さの寸法を、どこの点で測ったか(赤い丸)。部材の面か、図の端か、建物の外か
- fig-dimpoints-eave.png: 軒の出 600 を、垂木のどこまで測ったか
- video-dimpoints.png: 動画用。高さの寸法の測り方の3つの型を、横に並べる
- video-dimpoints-eave.png: 動画用。軒の出の測り方を2つだけ並べ、大きく見せる
- fig-extras-flash.png、fig-extras-argon.png: 頼んでいないもの(Flash の捨てコンクリートと砕石、Argon の高さの名前)

使い方: uv run --with ezdxf --with matplotlib --with pillow python code/drawings/figures_136.py
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import ezdxf
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from matplotlib.patches import Circle, Rectangle
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
DAY = REPO / "2026/11-05-AIと図面のコラボレーション-05-AIに矩計図と平面詳細図を描かせる"
RES = DAY / "results/2026-11-05"
OUT = DAY / "assets"
GL = -10500
VIEW = (45400, -12800, 53000, -5200)   # 一覧で切り出す範囲。どのモデルの図形も入る
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_R = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
RED = "#d03b3b"
INK = (30, 30, 30)
MUTED = (110, 110, 110)
NAMES = {"claude-haiku-5-5": "Claude Haiku 5.5", "claude-sonnet-5-5": "Claude Sonnet 5.5",
         "claude-opus-5-5": "Claude Opus 5.5", "claude-fable-5-1": "Claude Fable 5.1",
         "gpt-6.1-sol": "GPT-6.1 Sol", "gemini-3.8-flash": "Gemini 3.8 Flash",
         "gemini-4-argon": "Gemini 4 Argon"}
_docs = {}


def dxf_path(mode, model):
    return RES / f"K-1-{mode}/{model}__medium/drawing-changed.dxf"


def render(dxf, view, px, boxes=(), labels=(), dots=()):
    """DXF の view の範囲を、幅 px の画像にする。boxes は赤い枠 (x0, y0, x1, y1)、labels は赤い文字 (x, y, 文字)。"""
    doc = _docs.setdefault(str(dxf), ezdxf.readfile(dxf))
    x0, y0, x1, y1 = view
    size = (px / 100, px / 100 * (y1 - y0) / (x1 - x0))
    fig = plt.figure(figsize=size, dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK)
    Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(doc.modelspace())
    for bx0, by0, bx1, by1 in boxes:
        ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, fill=False, ec=RED, lw=3, zorder=10))
    for x, y in dots:
        ax.add_patch(Circle((x, y), (x1 - x0) / 110, fill=False, ec=RED, lw=3, zorder=12))
    from matplotlib import font_manager
    for x, y, t in labels:
        ax.text(x, y, t, color=RED, fontsize=22, zorder=11, fontproperties=font_manager.FontProperties(fname=FONT, size=22))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_axis_off()
    fig.set_size_inches(*size)  # ezdxf の描画が図の大きさを変えるので、戻す
    tmp = OUT / "_tmp.png"
    fig.savefig(tmp, dpi=100, facecolor="white")
    plt.close(fig)
    im = Image.open(tmp).convert("RGB")
    tmp.unlink()
    return im


def panels(cells, out, cols=2, band=80, note=None):
    """(見出し, 補足, 画像) を cols 列に並べる。"""
    w = max(im.width for _, _, im in cells)
    h = max(im.height for _, _, im in cells)
    rows = (len(cells) + cols - 1) // cols
    foot = 60 if note else 0
    sheet = Image.new("RGB", (w * cols, (h + band) * rows + foot), "white")
    d = ImageDraw.Draw(sheet)
    f1, f2 = ImageFont.truetype(FONT, 32), ImageFont.truetype(FONT_R, 24)
    for i, (title, sub, im) in enumerate(cells):
        x, y = (i % cols) * w, (i // cols) * (h + band)
        d.text((x + 20, y + 10), title, font=f1, fill=INK)
        if sub:
            d.text((x + 22, y + 50), sub, font=f2, fill=MUTED)
        sheet.paste(im, (x, y + band))
        d.rectangle([x, y, x + w - 1, y + h + band - 1], outline=(205, 205, 205), width=2)
    if note:
        d.text((20, sheet.height - foot + 14), note, font=f2, fill=MUTED)
    sheet.save(out, quality=88)
    print(out)


def compare():
    order = ["claude-sonnet-5-5", "claude-opus-5-5", "claude-fable-5-1", "gemini-3.8-flash", "gemini-4-argon"]
    for mode in ("mcp", "dxf"):
        cells = [(NAMES[m], "", render(dxf_path(mode, m), VIEW, 760)) for m in order if dxf_path(mode, m).exists()]
        panels(cells, OUT / f"compare-K-1-{mode}.jpg", cols=3, band=70)


def conditions():
    base = DAY / "base/house.dxf"
    view = (-3500, -26000, 56500, 11000)
    aa = (29300, -14500, 39200, -5200)
    target = (45500, -12500, 53000, -5200)
    im = render(base, view, 1800, boxes=[aa, target],
                labels=[(26500, -4400, "断面図 A-A（同じ位置で切る）"), (44500, -4400, "ここに矩計図を描く")])
    im.save(OUT / "fig-conditions.png")
    print(OUT / "fig-conditions.png")


def behavior():
    """モデル × 方法で、何をしたかを並べる。色は補助で、文字で読めるようにする。"""
    kinds = {
        "ask": ("描かずに質問", (232, 232, 232)),
        "list": ("描いて、確認を書き出す", (214, 230, 245)),
        "none": ("描いて、確認は「なし」", (250, 222, 200)),
        "timeout": ("時間切れ", (245, 245, 245)),
    }
    rows = []
    for model in NAMES:
        cells = []
        for mode in ("mcp", "dxf"):
            r = json.loads((RES / f"K-1-{mode}/{model}__medium/run.json").read_text())
            ans = r.get("answer") or ""
            if model == "claude-opus-5-5" and mode == "mcp":
                kind, n, sec = "list", 6, 429
            elif r["exit"] != 0 and not r.get("saved"):
                kind, n, sec = "timeout", 0, r["seconds"]
            elif not r.get("saved"):
                kind, n, sec = "ask", None, r["seconds"]
            else:
                tail = ans[ans.find("確認したいこと"):]
                kind = "none" if "なし" in tail[:40] else "list"
                n, sec = None, r["seconds"]
            cells.append((kind, sec))
        rows.append((NAMES[model], cells))
    W, rh, c0, cw = 1500, 74, 330, 585
    im = Image.new("RGB", (W, 130 + rh * len(rows) + 90), "white")
    d = ImageDraw.Draw(im)
    f1, f2, f3 = ImageFont.truetype(FONT, 30), ImageFont.truetype(FONT, 26), ImageFont.truetype(FONT_R, 22)
    d.text((c0 + 20, 40), "MCP（LibreCAD を操作）", font=f1, fill=INK)
    d.text((c0 + cw + 20, 40), "DXF を直接書く", font=f1, fill=INK)
    for i, (name, cells) in enumerate(rows):
        y = 110 + i * rh
        d.text((20, y + 20), name, font=f2, fill=INK)
        for j, (kind, sec) in enumerate(cells):
            x = c0 + j * cw
            label, color = kinds[kind]
            d.rounded_rectangle([x + 6, y + 6, x + cw - 6, y + rh - 6], radius=8, fill=color)
            d.text((x + 24, y + 20), label, font=f2, fill=INK)
            t = f"{int(sec // 60)}分{int(sec % 60):02d}秒"
            d.text((x + cw - 24 - d.textlength(t, font=f3), y + 24), t, font=f3, fill=MUTED)
    d.text((20, im.height - 60), "どのモデルにも「仕様と既存の図面が食い違うときは、描く前に聞いて」と指示した。"
           "Gemini 3.8 Flash の MCP は 20分の上限で止まった", font=f3, fill=MUTED)
    im.save(OUT / "fig-behavior.png")
    print(OUT / "fig-behavior.png")


def wall():
    """外壁の厚み。通り芯を 0 に、室内側を左、屋外側を右に描く。"""
    fig, axes = plt.subplots(2, 1, figsize=(12, 5.2), dpi=100)
    from matplotlib import font_manager
    fp = font_manager.FontProperties(fname=FONT_R)
    fpb = font_manager.FontProperties(fname=FONT)
    rows = [
        ("既存の平面図: 150（通り芯から ±75）", [(-75, 75, "壁 150", "#d9d9d9")]),
        ("仕様の積み上げ: 158.5（室内側 65、屋外側 93.5）",
         [(-65, -52.5, "石膏ボード\n12.5", "#eeeeee"), (-52.5, 52.5, "柱 105", "#e3cfa8"),
          (52.5, 61.5, "合板\n9", "#c9b48a"), (61.5, 79.5, "胴縁\n18", "#b8d0e6"),
          (79.5, 93.5, "サイディング\n14", "#9fb3c8")]),
    ]
    for ax, (title, parts) in zip(axes, rows):
        for x0, x1, lab, col in parts:
            ax.add_patch(Rectangle((x0, 0), x1 - x0, 1, fc=col, ec="#333333", lw=1))
            ax.text((x0 + x1) / 2, -0.12, lab, ha="center", va="top", fontproperties=fp, fontsize=11)
        ax.axvline(0, color=RED, lw=1.5, ls="--")
        ax.text(0, 1.08, "通り芯 Y1", color=RED, ha="center", fontproperties=fp, fontsize=11)
        ax.text(-100, 1.35, title, fontproperties=fpb, fontsize=14)
        ax.text(-98, 0.5, "室内", va="center", fontproperties=fp, fontsize=12, color="#666666")
        ax.text(103, 0.5, "屋外", va="center", fontproperties=fp, fontsize=12, color="#666666")
        ax.set_xlim(-100, 115)
        ax.set_ylim(-0.75, 1.55)
        ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(OUT / "fig-wall.png", facecolor="white")
    plt.close(fig)
    print(OUT / "fig-wall.png")


def floor():
    p = dxf_path("dxf", "claude-opus-5-5")
    dodai = (49947.5 - 15, GL + 420 - 15, 50052.5 + 15, GL + 525 + 15)
    obiki = (49090 - 45 - 15, GL + 525 - 90 - 15, 49090 + 45 + 15, GL + 525 + 15)
    im = render(p, (48150, -10700, 51200, -9800), 1500, boxes=[dodai, obiki])
    panels([("土台と大引（Claude Opus 5.5 が DXF で描いた図）",
             "赤い枠: 左が大引 90角、右が土台 105角。上の面をそろえ、その上に合板とフローリングが載る", im)],
           OUT / "fig-floor.png", cols=1, band=96)


def insulation():
    view = (48500, -8000, 50800, -6850)
    cells = [("Claude Opus 5.5 ／ MCP", "断熱材は外形の四角だけ", render(dxf_path("mcp", "claude-opus-5-5"), view, 900)),
             ("Claude Opus 5.5 ／ DXF を直接書く", "断熱材にジグザグの模様", render(dxf_path("dxf", "claude-opus-5-5"), view, 900))]
    panels(cells, OUT / "fig-insulation.png", cols=2, band=96, note="天井と外壁の上の部分を、同じ範囲で切り出した")


def extras():
    flash = render(dxf_path("dxf", "gemini-3.8-flash"), (46500, -10900, 50700, -9750), 1500,
                   boxes=[(48130, -10780, 50240, -10585), (46650, -10255, 48010, -10080)])
    panels([("Gemini 3.8 Flash ／ DXF を直接書く",
             "下の赤い枠: 底盤の下に、仕様にない捨てコンクリート 50 と砕石 100 を描き足した。左の赤い枠はその名前", flash)],
           OUT / "fig-extras-flash.png", cols=1, band=96)
    argon = render(dxf_path("dxf", "gemini-4-argon"), (45300, -10700, 49200, -7000), 1100,
                   boxes=[(45400, -10560, 47080, -7120)])
    panels([("Gemini 4 Argon ／ DXF を直接書く", "赤い枠: 頼んでいない高さの名前と数字を、図の左に並べた", argon)],
           OUT / "fig-extras-argon.png", cols=1, band=96)


# LibreCAD の画面写真(shoot_136.py)の、図面の座標と画素の対応。窓 46,600〜52,900 × -11,300〜-5,300 を高さに合わせて映す
LC_WIN = (46600, -11300, 52900, -5300)
LC_SCALE, LC_X0 = 0.2267, 388
OVERLAP = {  # 400 と 161 の寸法線の x(文字はその左に立つ)
    ("dxf", "claude-opus-5-5"): 47750, ("dxf", "claude-fable-5-1"): 51400, ("dxf", "gemini-4-argon"): 47650,
    ("dxf", "claude-sonnet-5-5"): 47880, ("mcp", "claude-sonnet-5-5"): 51100}


def lc_px(x, y):
    return LC_X0 + (x - LC_WIN[0]) * LC_SCALE, (LC_WIN[3] - y) * LC_SCALE


def lc_image(mode, model, view=None, mark=True):
    im = Image.open(RES / f"librecad/{mode}-{model}.png").convert("RGB")
    d = ImageDraw.Draw(im)
    x = OVERLAP.get((mode, model))
    if mark and x:
        (a, b), (c, e) = lc_px(x - 260, -9600), lc_px(x + 120, -10560)
        d.ellipse([a, b, c, e], outline=(230, 60, 60), width=6)
    if view:
        (a, b), (c, e) = lc_px(view[0], view[3]), lc_px(view[2], view[1])
        im = im.crop((int(a), int(b), int(c), int(e)))
    else:
        (a, _), (c, _) = lc_px(46620, 0), lc_px(52700, 0)
        im = im.crop((int(a), 0, int(c), im.height - 40))
    return im


def dims_viewer():
    view = (47000, -10750, 50300, -7000)
    left = render(dxf_path("dxf", "claude-opus-5-5"), view, 800)
    right = lc_image("dxf", "claude-opus-5-5", view).resize((800, left.height))
    panels([("ezdxf で開いた画面", "ファイルに入った寸法の絵をそのまま描く。文字 60、端は斜線", left),
            ("LibreCAD で開いた画面", "図面の設定から描き直す。文字 200、端は矢印。400 と 161 が重なる", right)],
           OUT / "fig-dims-viewer.png", cols=2, band=96, note="どちらも、Claude Opus 5.5 が DXF を直接書いて保存した同じファイル")


def dim_points(mode, model):
    """寸法が測っている2点。Flash は寸法の部品を使わず線で描いたので、寸法補助線の始まりの点を使う。"""
    if model == "gemini-3.8-flash":
        return [(50075, GL), (50075, GL + 400), (50075, GL + 561), (49935, GL + 2961), (50052, GL + 3311),
                (50000, GL + 3311), (50600, GL + 3184)]
    doc = _docs.setdefault(str(dxf_path(mode, model)), ezdxf.readfile(dxf_path(mode, model)))
    pts = set()
    for e in doc.modelspace().query("DIMENSION"):
        x, y = e.dxf.defpoint.x, e.dxf.defpoint.y
        if 44000 <= x <= 56000 and -15000 <= y <= -3000:
            for q in (e.dxf.defpoint2, e.dxf.defpoint3):
                pts.add((round(q.x), round(q.y)))
    return sorted(pts)


def dimpoints():
    view = (47300, -10750, 52000, -6950)
    rows = [
        ("mcp", "claude-opus-5-5", "基礎と軒桁の面で測る。基礎上端は立ち上がり、軒高は Y1 の軒桁の上"),
        ("dxf", "gemini-3.8-flash", "寸法補助線を、基礎の外面・壁の内面・軒桁から引き出す"),
        ("mcp", "claude-sonnet-5-5", "400 と 161 は基礎の外面。2,400 と 2,750 は図の北の端"),
        ("dxf", "gemini-4-argon", "図の北の端でそろえる。軒高の線を、軒桁から北の端まで引いた"),
        ("dxf", "claude-opus-5-5", "図の北の端の、少し外でそろえる。そこに基礎上端と軒桁はない"),
        ("dxf", "claude-fable-5-1", "建物の外（軒先より外）でそろえ、▽の印を並べる"),
    ]
    label = {"mcp": "MCP", "dxf": "DXF を直接書く"}
    cells = [(f"{NAMES[m]} ／ {label[mode]}", sub, render(dxf_path(mode, m), view, 820, dots=dim_points(mode, m)))
             for mode, m, sub in rows]
    pick = {0: "部材の面で測る", 4: "図の北の端でそろえる", 5: "建物の外でそろえ、▽の印"}
    panels([(t, pick[i], im) for i, (t, _, im) in enumerate(cells) if i in pick], OUT / "video-dimpoints.png",
           cols=3, band=96, note="赤い丸: 高さの寸法が測っている点")
    panels(cells, OUT / "fig-dimpoints.jpg", cols=2, band=96,
           note="赤い丸: 高さの寸法が測っている点。基礎上端（GL+400）の面は基礎の立ち上がりに、軒高（GL+3,311）の面は Y1 の軒桁の上にしかない")


def dimpoints_eave():
    view = (49750, -7520, 50850, -6950)
    rows = [("mcp", "claude-opus-5-5", "垂木の下面どうし（Y1 の軒高 → 垂木の先の下端）"),
            ("dxf", "claude-sonnet-5-5", "下面から上面へ（Y1 の軒高 → 垂木の先の上端）"),
            ("mcp", "claude-sonnet-5-5", "屋根の上面どうし（Y1 の屋根の上 → 垂木の先の上端）")]
    cells = [(f"{NAMES[m]} ／ {'MCP' if mode == 'mcp' else 'DXF を直接書く'}", sub,
              render(dxf_path(mode, m), view, 800, dots=[p for p in dim_points(mode, m) if p[1] > GL + 3000]))
             for mode, m, sub in rows]
    panels(cells, OUT / "fig-dimpoints-eave.png", cols=3, band=96, note="赤い丸: 軒の出 600 が測っている2点。数字はどれも 600")
    panels(cells[:2], OUT / "video-dimpoints-eave.png", cols=2, band=96, note="赤い丸: 軒の出 600 が測っている2点")


def opus():
    render(dxf_path("mcp", "claude-opus-5-5"), (46900, -11300, 51700, -5600), 2000).save(OUT / "kanabakari-opus-mcp.png")
    print(OUT / "kanabakari-opus-mcp.png")


def main():
    OUT.mkdir(exist_ok=True)
    opus()
    compare()
    conditions()
    behavior()
    wall()
    floor()
    insulation()
    dims_viewer()
    dimpoints()
    dimpoints_eave()
    extras()


if __name__ == "__main__":
    main()
