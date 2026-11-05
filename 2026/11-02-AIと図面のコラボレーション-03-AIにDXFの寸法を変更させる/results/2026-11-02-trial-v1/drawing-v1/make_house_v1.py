"""2LDK の平屋の平面図を DXF で作る(#135)。

#135 で、AI に寸法を変更させる元の図面にする。座標は実物の mm。寸法は DIMENSION の部品で入れる。
土地は 60坪(間口 13m × 奥行 15.2m、南道路)を想定し、建物は南に LDK と寝室1を置く。平面図だけを描く。

- 格子は 910mm(半間)。建物は 11P × 7P = 10,010 × 6,370(約63.8m²、約19.3坪)
- 通り芯は壁の中心。外壁 150、間仕切り 120
- 壁は、中心線に厚みを付けた帯を合わせ、開口を抜いた形(shapely で作る)
- 扉は開く向きの線と円弧、窓は壁の中の3本の線
- 設備(便器、洗面化粧台、浴槽、洗濯機置き場、キッチン、冷蔵庫置き場、クローゼット)は FIXTURE レイヤーに描く

#135 の課題ごとに、正しく直した図面(正解の図面)も作る。VARIANTS に、元の図面からの変更を書く。

使い方: uv run --with ezdxf --with shapely python code/drawings/make_house.py <出力.dxf> [課題の ID]
"""
import sys

import ezdxf
from shapely.geometry import LineString, box
from shapely.ops import unary_union

JP_STYLE = "kst32b"
EXT, PART = 150, 120

# 通り芯
XS = {"X1": 0, "X2": 1820, "X3": 2730, "X4": 4550, "X5": 6370, "X6": 10010}
YS = {"Y1": 0, "Y2": 3640, "Y3": 4550, "Y4": 6370}
W, D = XS["X6"], YS["Y4"]

# 壁の中心線 (x1, y1, x2, y2, 厚さ)
WALLS = [
    (0, 0, W, 0, EXT), (W, 0, W, D, EXT), (W, D, 0, D, EXT), (0, D, 0, 0, EXT),
    (6370, 0, 6370, D, PART),        # LDK・寝室1 | 浴室・寝室2
    (0, 3640, W, 3640, PART),        # LDK | 玄関・廊下、寝室1 | 寝室2
    (1820, 3640, 1820, D, PART),     # 玄関 | 廊下・トイレ
    (1820, 4550, 6370, 4550, PART),  # 廊下 | トイレ・洗面・浴室
    (2730, 4550, 2730, D, PART),     # トイレ | 洗面
    (4550, 4550, 4550, D, PART),     # 洗面 | 浴室
]

# 扉: (名前, 壁の向き, 壁の座標, 開口の始まり, 終わり, 吊元の側, 開く側)
#   壁の向き "h" は水平の壁(y が一定)、"v" は垂直の壁(x が一定)
#   吊元の側 "a" は始まり側、"b" は終わり側。開く側 +1 は座標が増える向き
DOORS = [
    ("玄関ドア", "v", 0, 4550, 5450, "a", +1),
    ("LDK", "h", 3640, 2000, 2800, "a", -1),
    ("寝室1", "v", 6370, 1800, 2600, "b", +1),  # 冷蔵庫置き場(y=2,930〜)より南に置く
    ("寝室2", "v", 6370, 3720, 4470, "a", +1),
    ("トイレ", "h", 4550, 1920, 2620, "b", +1),
    ("洗面", "h", 4550, 2830, 3630, "a", +1),
    ("浴室", "v", 4550, 4900, 5600, "a", -1),
]
# 扉のない開口(玄関から廊下へ)
OPENINGS = [("v", 1820, 3720, 4470)]
# 窓: (名前, 壁の向き, 壁の座標, 始まり, 終わり)
WINDOWS = [
    ("LDK南1", "h", 0, 600, 2250), ("LDK南2", "h", 0, 3300, 4950), ("LDK西", "v", 0, 1200, 2400),
    ("寝室1南", "h", 0, 7450, 9100), ("寝室1東", "v", W, 1200, 2400),
    ("寝室2北", "h", D, 7550, 8750), ("寝室2東", "v", W, 4800, 5700),
    ("浴室北", "h", D, 5110, 5810), ("洗面北", "h", D, 3290, 3990), ("トイレ北", "h", D, 2000, 2550),
]
# 設備: (種類, 座標...)。rect は (x0, y0, x1, y1)、ellipse は (cx, cy, 横の半径, 縦の半径)、circle は (cx, cy, r)
FIXTURES = [
    ("rect", 2050, 6095, 2500, 6295), ("ellipse", 2275, 5820, 190, 275),            # 便器(タンクと便座)
    ("rect", 2850, 5795, 3600, 6295), ("ellipse", 3225, 6020, 220, 150),            # 洗面化粧台
    ("rect", 3800, 5655, 4440, 6295), ("circle", 4120, 5975, 250),                  # 洗濯機置き場
    ("rect", 4700, 5545, 6260, 6295), ("rect", 4780, 5625, 6180, 6215),             # 浴槽
    ("rect", 3000, 2930, 5550, 3580), ("rect", 3500, 3080, 4300, 3480),             # キッチン(流し)
    ("circle", 4800, 3255, 150), ("circle", 5200, 3255, 150),                       # キッチン(コンロ)
    ("rect", 5600, 2930, 6250, 3580),                                               # 冷蔵庫置き場
    ("rect", 7300, 3010, 9925, 3580), ("line", 7300, 3295, 9925, 3295),             # 寝室1 クローゼット
    ("rect", 7300, 3700, 9100, 4300), ("line", 7300, 4000, 9100, 4000),             # 寝室2 クローゼット
]
FIXTURE_TEXT = [("冷蔵庫", 5925, 3255)]

ROOMS = [("LDK", 3185, 1820, "約14畳"), ("寝室1", 8190, 1820, "約8畳"), ("寝室2", 8190, 5005, "約6畳"),
         ("玄関", 910, 5005, ""), ("廊下", 4095, 4095, ""), ("トイレ", 2275, 5380, ""),
         ("洗面脱衣", 3450, 5480, ""), ("浴室", 5460, 5150, "")]


def shift_north(dy):
    """Y3 より北のものを dy だけ北へ動かす(C-3: 廊下を広げる)。"""
    global WALLS, DOORS, WINDOWS, ROOMS, YS, D, FIXTURES, FIXTURE_TEXT
    mv = lambda v: v + dy if v >= YS["Y3"] else v  # noqa: E731
    y3 = YS["Y3"]

    def fx(f):  # 北側の部屋の設備だけ、まるごと北へ動かす
        k, *v = f
        ys = [v[1]] + ([v[3]] if k in ("rect", "line") else [])
        if min(ys) < y3:
            return f
        if k in ("rect", "line"):
            return (k, v[0], v[1] + dy, v[2], v[3] + dy)
        return (k, v[0], v[1] + dy, *v[2:])
    FIXTURES = [fx(f) for f in FIXTURES]
    FIXTURE_TEXT = [(t, x, y + dy if y >= y3 else y) for t, x, y in FIXTURE_TEXT]
    WALLS = [(x1, mv(y1), x2, mv(y2), t) for x1, y1, x2, y2, t in WALLS]
    DOORS = [(n, o, mv(at) if o == "h" else at, *((a, b) if o == "h" or a < YS["Y3"] else (a + dy, b + dy)), h, s)
             for n, o, at, a, b, h, s in DOORS]
    WINDOWS = [(n, o, mv(at) if o == "h" else at, *((a, b) if o == "h" or a < YS["Y3"] else (a + dy, b + dy)))
               for n, o, at, a, b in WINDOWS]
    ROOMS = [(n, x, mv(y), sz) for n, x, y, sz in ROOMS]
    YS = {k: mv(v) for k, v in YS.items()}
    D = YS["Y4"]


def widen_east(dx):
    """X6 の外壁を dx だけ東へ動かす(C-2: 寝室1を広げる)。"""
    global WALLS, WINDOWS, ROOMS, XS, W
    mv = lambda v: v + dx if v >= XS["X6"] else v  # noqa: E731
    WALLS = [(mv(x1), y1, mv(x2), y2, t) for x1, y1, x2, y2, t in WALLS]
    WINDOWS = [(n, o, mv(at) if o == "v" else at, a, b) for n, o, at, a, b in WINDOWS]
    ROOMS = [(n, x + dx / 2 if x > XS["X5"] else x, y, sz) for n, x, y, sz in ROOMS]
    XS = {k: mv(v) for k, v in XS.items()}
    W = XS["X6"]


def set_window(name, a, b):
    global WINDOWS
    WINDOWS = [(n, o, at, a, b) if n == name else (n, o, at, aa, bb) for n, o, at, aa, bb in WINDOWS]


# 課題ごとの正解の図面。C-4 は両立しない指示なので、図面は変えない(確認を求めるのが正解)
VARIANTS = {
    "C-1-1": lambda: set_window("LDK南2", 3300, 5120),
    "C-2-1": lambda: widen_east(910),
    "C-3-1": lambda: shift_north(455),
}


def thick(orient, at, a, b, t):
    """壁の中の開口を、壁の厚みより少し広い長方形にする。"""
    return box(a, at - t, b, at + t) if orient == "h" else box(at - t, a, at + t, b)


def wall_shape():
    bands = [LineString([(x1, y1), (x2, y2)]).buffer(t / 2, cap_style=3, join_style=2) for x1, y1, x2, y2, t in WALLS]
    walls = unary_union(bands)
    holes = [thick(o, at, a, b, EXT) for _, o, at, a, b, *_ in DOORS] + [thick(o, at, a, b, EXT) for o, at, a, b in OPENINGS]
    holes += [thick(o, at, a, b, EXT) for _, o, at, a, b in WINDOWS]
    return walls.difference(unary_union(holes))


def main(out, variant=None):
    if variant:
        VARIANTS[variant]()
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4
    doc.styles.add(JP_STYLE, font="kst32b.lff")
    for name, color, lt in (("WALL", 7, "CONTINUOUS"), ("GRID", 1, "CENTER"), ("DOOR", 3, "CONTINUOUS"),
                            ("WINDOW", 4, "CONTINUOUS"), ("FIXTURE", 8, "CONTINUOUS"), ("DIM", 2, "CONTINUOUS"), ("TEXT", 7, "CONTINUOUS")):
        doc.layers.add(name, color=color, linetype=lt)
    m = doc.modelspace()

    shape = wall_shape()
    for poly in getattr(shape, "geoms", [shape]):
        for ring in [poly.exterior, *poly.interiors]:
            m.add_lwpolyline(list(ring.coords)[:-1], close=True, dxfattribs={"layer": "WALL"})

    # 扉: 吊元から、開口の幅の長さの線と、90度の円弧
    for _, o, at, a, b, hinge, side in DOORS:
        w = b - a
        h = a if hinge == "a" else b
        if o == "h":
            p, leaf = (h, at), (h, at + side * w)
            start = 0 if (hinge == "a") == (side > 0) else 90
            ang = (0, 90) if hinge == "a" and side > 0 else (90, 180) if hinge == "b" and side > 0 else \
                (270, 360) if hinge == "a" else (180, 270)
        else:
            p, leaf = (at, h), (at + side * w, h)
            ang = (0, 90) if hinge == "a" and side > 0 else (270, 360) if hinge == "b" and side > 0 else \
                (90, 180) if hinge == "a" else (180, 270)
        m.add_line(p, leaf, dxfattribs={"layer": "DOOR"})
        m.add_arc(p, w, ang[0], ang[1], dxfattribs={"layer": "DOOR"})
    for k, *v in FIXTURES:
        at = {"layer": "FIXTURE"}
        if k == "rect":
            x0, y0, x1, y1 = v
            m.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs=at)
        elif k == "line":
            m.add_line((v[0], v[1]), (v[2], v[3]), dxfattribs=at)
        elif k == "circle":
            m.add_circle((v[0], v[1]), v[2], dxfattribs=at)
        else:
            cx, cy, rx, ry = v
            major, ratio = ((rx, 0), ry / rx) if rx >= ry else ((0, ry), rx / ry)
            m.add_ellipse((cx, cy), major_axis=major, ratio=ratio, dxfattribs=at)
    for t, x, y in FIXTURE_TEXT:
        m.add_text(t, height=120, dxfattribs={"layer": "FIXTURE", "style": JP_STYLE}).set_placement(
            (x, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    for _, o, at, a, b in WINDOWS:
        for d in (-EXT / 2, 0, EXT / 2):
            pts = ((a, at + d), (b, at + d)) if o == "h" else ((at + d, a), (at + d, b))
            m.add_line(*pts, dxfattribs={"layer": "WINDOW"})

    # 通り芯と符号
    def label(s, at):
        m.add_circle(at, 300, dxfattribs={"layer": "GRID"})
        m.add_text(s, height=250, dxfattribs={"layer": "GRID", "style": JP_STYLE}).set_placement(
            at, align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    for n, x in XS.items():
        m.add_line((x, -1500), (x, D + 2300), dxfattribs={"layer": "GRID"})
        label(n, (x, D + 2600))
    for n, y in YS.items():
        m.add_line((-2300, y), (W + 1200, y), dxfattribs={"layer": "GRID"})
        label(n, (-2600, y))

    # 寸法。値は「3,640」の形で書く
    ov = {"dimtxt": 200, "dimasz": 120, "dimexo": 80, "dimgap": 60, "dimtxsty": JP_STYLE, "dimtad": 1, "dimdec": 0}

    def dim(a, b, base, angle=0):
        n = abs((b[1] - a[1]) if angle == 90 else (b[0] - a[0]))
        m.add_linear_dim(base=base, p1=a, p2=b, angle=angle, text=f"{n:,}", override=ov,
                         dxfattribs={"layer": "DIM"}).render()

    xs, ys = sorted(XS.values()), sorted(YS.values())
    for a, b in zip(xs, xs[1:]):
        dim((a, D), (b, D), (0, D + 1300))
    dim((0, D), (W, D), (0, D + 1800))
    for a, b in zip(ys, ys[1:]):
        dim((0, a), (0, b), (-1300, 0), angle=90)
    dim((0, 0), (0, D), (-1800, 0), angle=90)

    for name, x, y, size in ROOMS:
        h = 300 if size else 180
        m.add_text(name, height=h, dxfattribs={"layer": "TEXT", "style": JP_STYLE}).set_placement(
            (x, y + (180 if size else 0)), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        if size:
            m.add_text(size, height=220, dxfattribs={"layer": "TEXT", "style": JP_STYLE}).set_placement(
                (x, y - 250), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    m.add_text("2LDK 平屋 平面図   S=1/100   単位: mm", height=300, dxfattribs={"layer": "TEXT", "style": JP_STYLE}
               ).set_placement((W / 2, -2300), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    m.add_text("南（道路側）", height=220, dxfattribs={"layer": "TEXT", "style": JP_STYLE}).set_placement(
        (W / 2, -1300), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    doc.saveas(out)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
