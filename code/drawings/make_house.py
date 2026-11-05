"""2LDK の平屋の平面図を DXF で作る(#135)。

#135 で、AI に寸法を変更させる元の図面にする。座標は実物の mm。寸法は DIMENSION の部品で入れる。
土地は 60坪(間口 13m × 奥行 15.2m、南道路)を想定し、建物は南に LDK と寝室1を置く。平面図だけを描く。

- 格子は 910mm(半間)。建物は 11P × 8P = 10,010 × 7,280(約72.9m²、約22坪)\n  最初の版(11P × 7P)は、廊下が長く、寝室1に LDK から入る間取りで、住みにくいと指摘を受けて描き直した
- 通り芯は壁の中心。外壁 150、間仕切り 120
- 壁は、中心線に厚みを付けた帯を合わせ、開口を抜いた形(shapely で作る)
- 扉は開く向きの線と円弧、窓は壁の中の3本の線
- 設備(便器、洗面化粧台、浴槽、洗濯機置き場、キッチン、冷蔵庫置き場、クローゼット)は FIXTURE レイヤーに描く
- 立面図(南・北・東・西)も同じ DXF に描く。窓と扉の横の位置は、平面図のデータから読む
  切妻屋根(棟は東西、勾配 4/10)、軒の出 600、けらば 300。GL±0、基礎上端 400、FL 500、天井 FL+2,400、軒の高さ 3,250
- 断面図(A-A 南北、B-B 東西)も同じ DXF に描く。切断線と交わる壁・窓・部屋を、平面図のデータから拾う。基礎はベタ基礎

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
XS = {"X1": 0, "X2": 910, "X3": 2730, "X4": 4550, "X5": 5460, "X6": 6370, "X7": 7280, "X8": 10010}
YS = {"Y1": 0, "Y2": 1820, "Y3": 3640, "Y4": 4550, "Y5": 5460, "Y6": 7280}
W, D = max(XS.values()), max(YS.values())

# 壁の中心線 (x1, y1, x2, y2, 厚さ)
WALLS = [
    (0, 0, W, 0, EXT), (W, 0, W, D, EXT), (W, D, 0, D, EXT), (0, D, 0, 0, EXT),
    (4550, 0, 4550, D, PART),        # LDK | 玄関・ホール・トイレ、洗面脱衣 | ファミリークローゼット
    (6370, 0, 6370, 3640, PART),     # 玄関・ホール | 寝室1
    (6370, 4550, 6370, D, PART),     # ファミリークローゼット | 寝室2
    (7280, 3640, 7280, 4550, PART),  # 廊下 | 寝室1のクローゼット
    (4550, 3640, 5460, 3640, PART),  # ホール | トイレ
    (6370, 3640, W, 3640, PART),     # 寝室1 | 廊下・クローゼット
    (6370, 4550, W, 4550, PART),     # 廊下・クローゼット | 寝室2
    (5460, 3640, 5460, 5460, PART),  # トイレ | ホール
    (0, 5460, 6370, 5460, PART),     # LDK・トイレ・ホール | パントリー・浴室・洗面脱衣・ファミリークローゼット
    (910, 5460, 910, D, PART),       # パントリー | 浴室
    (2730, 5460, 2730, D, PART),     # 浴室 | 洗面脱衣
]

# 扉: (名前, 壁の向き, 壁の座標, 開口の始まり, 終わり, 吊元の側, 開く側)
#   壁の向き "h" は水平の壁(y が一定)、"v" は垂直の壁(x が一定)
#   吊元の側 "a" は始まり側、"b" は終わり側。開く側 +1 は座標が増える向き
DOORS = [
    ("玄関ドア", "h", 0, 5000, 5900, "a", -1),           # 外開き(日本の住宅の玄関の基本)
    ("寝室1", "v", 6370, 2300, 3100, "b", +1),
    ("寝室2", "h", 4550, 6440, 7210, "a", +1),
    ("勝手口", "v", 0, 4450, 5200, "b", -1),             # キッチンの西の壁、外開き
]
# 引き戸: (名前, 壁の向き, 壁の座標, 開口の始まり, 終わり, 戸を置く面の側, 引き込む向き)
#   戸を置く面の側 +1 は座標が増える側の面。引き込む向き +1 は、開口の終わりの側へ引き込む
SLIDES = [
    ("LDK", "v", 4550, 2300, 3100, -1, +1),               # LDKの側の面、北へ引き込む(南の壁をリビングに使えるよう)
    ("トイレ", "v", 5460, 4620, 5320, +1, -1),            # ホールの側の面、南へ引き込む
    ("洗面", "h", 5460, 3700, 4400, +1, -1),              # 洗面脱衣の側の面、西へ引き込む
    ("ファミリークローゼット", "h", 5460, 5540, 6300, +1, -1),  # ファミクロの側の面、西へ引き込む
    ("洗面|ファミクロ", "v", 4550, 5560, 6260, +1, +1),   # ファミクロの側の面、北へ引き込む
]
# 折れ戸: (名前, 壁の向き, 壁の座標, 開口の始まり, 終わり, 折れる側)
FOLDS = [("浴室", "v", 2730, 5650, 6350, -1)]           # 浴室の側へ折れる
# 扉のない開口
OPENINGS = [("h", 5460, 100, 800),     # パントリー(オープン。引き込む壁が足りないため)
            ("h", 3640, 7400, 9900)]   # 寝室1のクローゼット(折れ戸)
# 窓: (名前, 壁の向き, 壁の座標, 始まり, 終わり)
WINDOWS = [
    ("LDK南1", "h", 0, 400, 2050), ("LDK南2", "h", 0, 2500, 4150),
    ("LDK西1", "v", 0, 1200, 2400), ("LDK西2", "v", 0, 2800, 4000),
    ("寝室1南", "h", 0, 7300, 8950), ("寝室1東", "v", W, 1200, 2400),
    ("寝室2北", "h", D, 7600, 8800), ("寝室2東", "v", W, 6500, 7100),
    ("浴室北", "h", D, 1500, 2200), ("洗面北", "h", D, 3300, 4000), ("ファミクロ北", "h", D, 5100, 5800),
]
# 設備: (種類, 座標...)。rect は (x0, y0, x1, y1)、ellipse は (cx, cy, 横の半径, 縦の半径)、circle は (cx, cy, r)
FIXTURES = [
    ("rect", 4780, 3700, 5230, 3900), ("ellipse", 5005, 4175, 190, 275),          # 便器(南の壁にタンク、北を向いて座る)
    ("rect", 3700, 6720, 4450, 7220), ("ellipse", 4075, 6945, 220, 150),          # 洗面化粧台
    ("rect", 2850, 6580, 3490, 7220), ("circle", 3170, 6900, 250),                # 洗濯機置き場
    ("rect", 1000, 6420, 2640, 7190), ("rect", 1080, 6500, 2560, 7110),           # 浴槽
    ("rect", 1000, 3200, 3550, 3850), ("rect", 1300, 3330, 2100, 3720),           # アイランドキッチン(流しと作業台)。背面と冷蔵庫の前は 900
    ("rect", 1000, 4750, 2700, 5400),                                             # 背面(コンロと収納。奥行 650)
    ("circle", 1600, 5075, 150), ("circle", 2050, 5075, 150),                     # コンロ(壁付けの換気扇の下)
    ("rect", 2850, 4750, 3500, 5400),                                             # 冷蔵庫置き場(背面収納の東隣)
    ("line", 4610, 1820, 6310, 1820),                                             # 玄関の上がり框
    ("rect", 4610, 60, 4960, 1760),                                               # 玄関の靴入れ
    ("line", 7280, 4095, 9935, 4095),                                             # 寝室1のクローゼット(ハンガーパイプ)
    ("rect", 9350, 4610, 9935, 6400), ("line", 9640, 4610, 9640, 6400),           # 寝室2のクローゼット
    ("line", 4610, 6370, 6310, 6370),                                             # ファミリークローゼット(ハンガーパイプ)
    ("line", 4700, 6950, 6250, 6950),                                             # ファミリークローゼット(室内干しのパイプ)
    ("line", 60, 6370, 850, 6370),                                                # パントリーの棚
]
FIXTURE_TEXT = [("冷蔵庫", 3175, 5075), ("室内干し", 5475, 7060), ("鍵付き", 4830, 5700), ("勝手口", 350, 4825)]

ROOMS = [("LDK", 2275, 2000, "約15畳"), ("寝室1", 8190, 1820, "約8畳"), ("寝室2", 7900, 5900, "約6畳"),
         ("玄関", 5600, 900, ""), ("ホール", 5460, 2730, ""), ("トイレ", 5000, 4950, ""),
         ("洗面脱衣", 3450, 6280, ""), ("浴室", 1600, 5900, ""), ("ファミクロ", 5650, 6150, ""),
         ("パントリー", 455, 6650, "small"), ("クローゼット", 8645, 3850, "")]


def shift_north(dy, y_from, fix_from):
    """y_from より北のものを dy だけ北へ動かす(C-3: LDK を南北に広げる)。
    設備は、いちばん南の端が fix_from より北にあるものを動かす(北の壁に付いた設備)。"""
    global WALLS, DOORS, SLIDES, FOLDS, OPENINGS, WINDOWS, ROOMS, YS, D, FIXTURES, FIXTURE_TEXT
    mv = lambda v: v + dy if v >= y_from else v  # noqa: E731

    def op(o, at, a, b):  # 壁の中の開口。水平の壁は壁ごと、垂直の壁は開口が y_from より北なら動かす
        if o == "h":
            return mv(at), a, b
        return (at, a + dy, b + dy) if a >= y_from else (at, a, b)

    def fx(f):
        k, *v = f
        ys = [v[1]] + ([v[3]] if k in ("rect", "line") else [])
        if min(ys) < fix_from:
            return f
        if k in ("rect", "line"):
            return (k, v[0], v[1] + dy, v[2], v[3] + dy)
        return (k, v[0], v[1] + dy, *v[2:])
    WALLS = [(x1, mv(y1), x2, mv(y2), t) for x1, y1, x2, y2, t in WALLS]
    DOORS = [(n, o, *op(o, at, a, b), *rest) for n, o, at, a, b, *rest in DOORS]
    SLIDES = [(n, o, *op(o, at, a, b), *rest) for n, o, at, a, b, *rest in SLIDES]
    FOLDS = [(n, o, *op(o, at, a, b), *rest) for n, o, at, a, b, *rest in FOLDS]
    OPENINGS = [(o, *op(o, at, a, b)) for o, at, a, b in OPENINGS]
    WINDOWS = [(n, o, *op(o, at, a, b)) for n, o, at, a, b in WINDOWS]
    FIXTURES = [fx(f) for f in FIXTURES]
    FIXTURE_TEXT = [(t, x, y + dy if y >= fix_from else y) for t, x, y in FIXTURE_TEXT]
    ROOMS = [(n, x, y + dy if y >= y_from else y, sz) for n, x, y, sz in ROOMS]
    YS = {k: mv(v) for k, v in YS.items()}
    D = max(YS.values())


def widen_east(dx):
    """東の外壁(X8)を dx だけ東へ動かす(C-2: 寝室1を広げる)。東の壁に付いた設備も一緒に動かす。"""
    global WALLS, WINDOWS, DOORS, OPENINGS, ROOMS, XS, W, FIXTURES
    w0 = W
    mv = lambda v: v + dx if v >= w0 else v  # noqa: E731
    near = lambda v: v + dx if v >= w0 - 700 else v  # noqa: E731

    def fx(f):
        k, *v = f
        if k in ("rect", "line"):
            if min(v[0], v[2]) >= w0 - 700:   # 東の壁際の設備は、まるごと動かす
                return (k, v[0] + dx, v[1], v[2] + dx, v[3])
            return (k, v[0], v[1], near(v[2]) if v[2] >= w0 - 100 else v[2], v[3])  # 東の壁まで伸びる線は伸ばす
        return (k, near(v[0]), *v[1:]) if v[0] >= w0 - 700 else f
    WALLS = [(mv(x1), y1, mv(x2), y2, t) for x1, y1, x2, y2, t in WALLS]
    WINDOWS = [(n, o, mv(at) if o == "v" else at, a, b) for n, o, at, a, b in WINDOWS]
    DOORS = [(n, o, mv(at) if o == "v" else at, *rest) for n, o, at, *rest in DOORS]
    # 東の壁際まで続く開口(寝室1のクローゼットの折れ戸)は、東の端を壁と一緒に動かす。
    # 本番で、保存した4つのモデルがそろってこう直し、クローゼットが伸びる以上この方が自然と判断した(2026-11-03)
    OPENINGS = [(o, at, a, b + dx if o == "h" and b >= w0 - 200 else b) for o, at, a, b in OPENINGS]
    FIXTURES = [fx(f) for f in FIXTURES]
    ROOMS = [(n, x + dx / 2 if x > XS["X6"] else x, y, sz) for n, x, y, sz in ROOMS]
    XS = {k: mv(v) for k, v in XS.items()}
    W = max(XS.values())


def set_window(name, a, b):
    global WINDOWS
    WINDOWS = [(n, o, at, a, b) if n == name else (n, o, at, aa, bb) for n, o, at, aa, bb in WINDOWS]


# 課題ごとの正解の図面。C-4 は両立しない指示なので、図面は変えない(確認を求めるのが正解)
VARIANTS = {
    "C-1-1": lambda: set_window("LDK南2", 2500, 4320),
    "C-2-1": lambda: widen_east(910),
    "C-3-1": lambda: shift_north(455, YS["Y5"], 4700),
}


# 立面図の高さ(GL からの mm)と屋根
BASE_TOP, FL, EAVE_H = 400, 500, 3250
PITCH, EAVE_OUT, VERGE_OUT, ROOF_T = 0.4, 600, 300, 150
# 窓と扉の、床からの下端と上端
OPENING_H = {
    "LDK南1": (0, 2000), "LDK南2": (0, 2000),                       # 掃き出し窓
    "LDK西1": (900, 2000), "LDK西2": (900, 2000),                   # 腰窓
    "寝室1南": (900, 2000), "寝室1東": (900, 2000), "寝室2北": (900, 2000), "寝室2東": (900, 2000),
    "浴室北": (1400, 1900), "洗面北": (1400, 1900), "ファミクロ北": (1400, 1900),  # 高窓(目隠し)
    "玄関ドア": (0, 2200), "勝手口": (0, 2000),
}
# 図の置き場所は、建物の大きさに関係なく固定する(寸法を変えても、図の位置は動かない)
VIEW_OX_RIGHT, VIEW_OX_SECTION = 16010, 30290
# 立面図の置き場所(平面図の下)。u は立面図の横の座標(見る人の左が 0)
ELEVATIONS = [("南立面図", "S", 0, -10500), ("北立面図", "N", 0, -21500),
              ("東立面図", "E", None, -10500), ("西立面図", "W", None, -21500)]


def facade_openings(face):
    """その面の外壁にある窓と扉を、(名前, u0, u1, 種類) で返す。u は立面図の横の座標。"""
    out = []
    for n, o, at, a, b, *_ in WINDOWS + DOORS:
        if n not in OPENING_H:
            continue
        hit = {"S": o == "h" and at == 0, "N": o == "h" and at == D, "W": o == "v" and at == 0,
               "E": o == "v" and at == W}[face]
        if hit:
            u0, u1 = to_u(face, a), to_u(face, b)
            out.append((n, min(u0, u1), max(u0, u1), "door" if any(n == d[0] for d in DOORS) else "window"))
    return out


def to_u(face, v):
    """平面図の座標(南北の面なら x、東西の面なら y)を、立面図の横の座標に直す。"""
    return {"S": v, "N": W - v, "E": v, "W": D - v}[face]


def draw_elevations(m, dim, text):
    from shapely.geometry import LineString as LS, Polygon
    W_EL = max(W, D)
    for title, face, ox, oy in ELEVATIONS:
        ox = VIEW_OX_RIGHT if ox is None else ox
        L = W if face in "SN" else D          # その面の壁の長さ
        P = lambda u, h: (ox + u, oy + h)      # noqa: E731
        lay = lambda n: {"layer": n}           # noqa: E731
        ridge = EAVE_H + D / 2 * PITCH         # 外壁の線の上での棟の高さ(屋根の下面)
        # 地面と基礎
        m.add_line(P(-1500, 0), P(L + 1500, 0), dxfattribs=lay("ELEV"))
        m.add_lwpolyline([P(0, 0), P(L, 0), P(L, BASE_TOP), P(0, BASE_TOP)], close=True, dxfattribs=lay("ELEV"))
        if face in "SN":
            # 軒側: 壁は軒裏まで。屋根は鼻先(破風)と、軒から棟までの屋根面
            soffit = EAVE_H - EAVE_OUT * PITCH
            wall = Polygon([(0, BASE_TOP), (L, BASE_TOP), (L, soffit), (0, soffit)])
            m.add_lwpolyline([P(-VERGE_OUT, soffit), P(L + VERGE_OUT, soffit), P(L + VERGE_OUT, soffit + ROOF_T),
                              P(-VERGE_OUT, soffit + ROOF_T)], close=True, dxfattribs=lay("ELEV"))
            top = ridge + ROOF_T
            m.add_lwpolyline([P(-VERGE_OUT, soffit + ROOF_T), P(L + VERGE_OUT, soffit + ROOF_T), P(L + VERGE_OUT, top),
                              P(-VERGE_OUT, top)], close=True, dxfattribs=lay("ELEV"))
            u = -VERGE_OUT + 455
            while u < L + VERGE_OUT:  # 屋根の縦の筋(ガルバリウム鋼板の立平葺き)
                m.add_line(P(u, soffit + ROOF_T), P(u, top), dxfattribs=lay("ELEV_DETAIL"))
                u += 455
        else:
            # 妻側: 壁は妻の三角形まで。屋根は両側へ流れる帯
            wall = Polygon([(0, BASE_TOP), (L, BASE_TOP), (L, EAVE_H), (L / 2, ridge), (0, EAVE_H)])
            lo = [(-EAVE_OUT, EAVE_H - EAVE_OUT * PITCH), (L / 2, ridge), (L + EAVE_OUT, EAVE_H - EAVE_OUT * PITCH)]
            hi = [(u, h + ROOF_T) for u, h in lo]
            m.add_lwpolyline([P(*q) for q in lo + hi[::-1]], close=True, dxfattribs=lay("ELEV"))
        m.add_lwpolyline([P(*q) for q in list(wall.exterior.coords)[:-1]], close=True, dxfattribs=lay("ELEV"))
        # 窓と扉
        holes = []
        for n, u0, u1, kind in facade_openings(face):
            h0, h1 = (FL + v for v in OPENING_H[n])
            holes.append(box(u0, h0, u1, h1))
            m.add_lwpolyline([P(u0, h0), P(u1, h0), P(u1, h1), P(u0, h1)], close=True, dxfattribs=lay("ELEV_WINDOW"))
            m.add_lwpolyline([P(u0 + 50, h0 + 50), P(u1 - 50, h0 + 50), P(u1 - 50, h1 - 50), P(u0 + 50, h1 - 50)],
                             close=True, dxfattribs=lay("ELEV_WINDOW"))
            if kind == "window" and u1 - u0 >= 1200:  # 引き違い窓の、2枚の境の線
                m.add_line(P((u0 + u1) / 2, h0 + 50), P((u0 + u1) / 2, h1 - 50), dxfattribs=lay("ELEV_WINDOW"))
            if kind == "door":  # 扉の取っ手
                m.add_circle(P(u1 - 150, h0 + 1000), 30, dxfattribs=lay("ELEV_WINDOW"))
        # 外壁の横の目地(サイディング 455 ごと)。窓と扉の所は抜く
        face_area = wall.difference(unary_union(holes)) if holes else wall
        h = BASE_TOP + 455
        while h < ridge:
            seg = LS([(-10, h), (L + 10, h)]).intersection(face_area)
            for g in getattr(seg, "geoms", [seg]):
                if g.length > 0 and g.geom_type == "LineString":
                    (a0, b0), (a1, b1) = g.coords[0], g.coords[-1]
                    m.add_line(P(a0, b0), P(a1, b1), dxfattribs=lay("ELEV_DETAIL"))
            h += 455
        # 通り芯
        grids = XS if face in "SN" else YS
        for name, v in grids.items():
            u = to_u(face, v)
            m.add_line(P(u, -1300), P(u, -300), dxfattribs=lay("GRID"))
            text(name, P(u, -1600), 200, "GRID")
        # 寸法: 横は通り芯の間隔と全体、縦は GL・FL・軒の高さ・最高の高さ
        us = sorted(to_u(face, v) for v in grids.values())
        for a, b in zip(us, us[1:]):
            dim(P(a, 0), P(b, 0), (0, oy - 2300))
        dim(P(0, 0), P(L, 0), (0, oy - 2800))
        top = ridge + ROOF_T
        hs = [0, FL, EAVE_H, round(top)]
        for a, b in zip(hs, hs[1:]):
            dim(P(0, a), P(0, b), (ox - 1500, 0), angle=90)
        dim(P(0, 0), P(0, hs[-1]), (ox - 2100, 0), angle=90)
        for t, h in (("GL", 0), ("FL", FL), ("軒高", EAVE_H)):
            text(t, P(-2700, h), 150, "TEXT")
        # 材料の名前と、図の名前
        text("屋根: ガルバリウム鋼板 立平葺き 4/10", P(L / 2, top + 500), 180, "TEXT")
        text("外壁: 窯業系サイディング", P(L + 1600, 1800), 160, "TEXT")
        text("基礎", P(L + 1000, 200), 160, "TEXT")
        text(title + "   S=1/100", P(L / 2, -3600), 300, "TEXT")


# 断面図: (名前, 切る向き, 切る座標, 見る向き)。"x" は x=一定の線で南北に切る、"y" は y=一定の線で東西に切る
SECTIONS = [("A-A断面図", "x", 1800, "東"), ("B-B断面図", "y", 2000, "北")]
CEIL = FL + 2400
SLAB_BOT, SLAB_TOP, FOOT_W = -100, 50, 150   # ベタ基礎の底板と、立ち上がりの幅


def sec_u(axis, v):
    """断面図の横の座標。A-A(東を見る)は左が北、B-B(北を見る)は左が西。"""
    return D - v if axis == "x" else v


def roof_under(y):
    """南の外壁から y の位置での、屋根の下面の高さ。"""
    return EAVE_H + min(y, D - y) * PITCH


def draw_sections(m, dim, text):
    from shapely.geometry import Polygon
    cut = {"layer": "SECT", "lineweight": 50}
    thin = {"layer": "SECT_VIEW"}
    ox0 = VIEW_OX_SECTION
    for (title, axis, c, look), oy in zip(SECTIONS, (-10500, -21500)):
        ox = ox0
        L = D if axis == "x" else W
        P = lambda u, h: (ox + u, oy + h)  # noqa: E731
        # 切断線と交わる壁: (平面での位置, 厚さ)
        walls = []
        for x1, y1, x2, y2, t in WALLS:
            if axis == "x" and y1 == y2 and min(x1, x2) <= c <= max(x1, x2):
                walls.append((y1, t))
            if axis == "y" and x1 == x2 and min(y1, y2) <= c <= max(y1, y2):
                walls.append((x1, t))
        walls = sorted(set(walls))
        # 切った壁にある窓・扉の、床からの高さ(なければ None)
        def opening_at(v):
            o_ = "h" if axis == "x" else "v"
            for n, o, at, a, b, *_ in WINDOWS + DOORS + SLIDES:
                if o == o_ and at == v and a <= c <= b:
                    return OPENING_H.get(n, (0, 2000))
            return None
        # 地面
        m.add_line(P(-1500, 0), P(L + 1500, 0), dxfattribs=thin)
        # ベタ基礎: 底板と、壁の下の立ち上がり
        found = [box(-FOOT_W / 2, SLAB_BOT, L + FOOT_W / 2, SLAB_TOP)]
        for v, t in walls:
            u = sec_u(axis, v)
            found.append(box(u - FOOT_W / 2, SLAB_BOT, u + FOOT_W / 2, BASE_TOP))
        for g in getattr(unary_union(found), "geoms", [unary_union(found)]):
            m.add_lwpolyline([P(*q) for q in list(g.exterior.coords)[:-1]], close=True, dxfattribs=cut)
        # 床と天井(壁と壁の間)
        us = sorted(sec_u(axis, v) for v, _ in walls)
        for (ua, ta), (ub, tb) in zip(sorted((sec_u(axis, v), t) for v, t in walls),
                                      sorted((sec_u(axis, v), t) for v, t in walls)[1:]):
            a_, b_ = ua + ta / 2, ub - tb / 2
            m.add_lwpolyline([P(a_, FL - 30), P(b_, FL - 30), P(b_, FL), P(a_, FL)], close=True, dxfattribs=cut)
            m.add_line(P(a_, CEIL), P(b_, CEIL), dxfattribs=cut)
        # 壁の切り口。外壁は屋根の下まで、間仕切りは天井まで。窓と扉の所は抜く
        for v, t in walls:
            u = sec_u(axis, v)
            outer = v in (0, D) if axis == "x" else v in (0, W)
            if outer:
                top = EAVE_H if axis == "x" else roof_under(c)
            else:
                top = CEIL
            body = box(u - t / 2, BASE_TOP, u + t / 2, top)
            op = opening_at(v)
            if op:
                body = body.difference(box(u - t, FL + op[0], u + t, FL + op[1]))
                h0, h1 = FL + op[0], FL + op[1]
                m.add_line(P(u, h0), P(u, h1), dxfattribs=thin)  # 窓や扉のガラス・戸の線
            for g in getattr(body, "geoms", [body]):
                if g.area > 0:
                    m.add_lwpolyline([P(*q) for q in list(g.exterior.coords)[:-1]], close=True, dxfattribs=cut)
        # 屋根
        if axis == "x":
            # 南北に切ると、屋根は三角形に切れる
            lo = [(-EAVE_OUT, EAVE_H - EAVE_OUT * PITCH), (L / 2, EAVE_H + L / 2 * PITCH),
                  (L + EAVE_OUT, EAVE_H - EAVE_OUT * PITCH)]
            hi = [(u, h + ROOF_T) for u, h in lo]
            m.add_lwpolyline([P(*q) for q in lo + hi[::-1]], close=True, dxfattribs=cut)
            m.add_lwpolyline([P(0, EAVE_H - 150), P(L, EAVE_H - 150), P(L, EAVE_H), P(0, EAVE_H)], close=True,
                             dxfattribs=thin)                                   # 小屋梁
            m.add_line(P(L / 2, EAVE_H), P(L / 2, EAVE_H + L / 2 * PITCH - 120), dxfattribs=thin)  # 小屋束
            m.add_lwpolyline([P(L / 2 - 60, EAVE_H + L / 2 * PITCH - 120), P(L / 2 + 60, EAVE_H + L / 2 * PITCH - 120),
                              P(L / 2 + 60, EAVE_H + L / 2 * PITCH), P(L / 2 - 60, EAVE_H + L / 2 * PITCH)],
                             close=True, dxfattribs=thin)                       # 棟木
            text("4/10", P(L * 0.25, EAVE_H + L * 0.25 * PITCH + 450), 180, "TEXT")
        else:
            # 東西に切ると、屋根は水平な帯に切れる。奥に棟までの屋根面が見える
            h = roof_under(c)
            m.add_lwpolyline([P(-VERGE_OUT, h), P(L + VERGE_OUT, h), P(L + VERGE_OUT, h + ROOF_T),
                              P(-VERGE_OUT, h + ROOF_T)], close=True, dxfattribs=cut)
            ridge_top = EAVE_H + D / 2 * PITCH + ROOF_T
            m.add_lwpolyline([P(-VERGE_OUT, h + ROOF_T), P(L + VERGE_OUT, h + ROOF_T), P(L + VERGE_OUT, ridge_top),
                              P(-VERGE_OUT, ridge_top)], close=True, dxfattribs=thin)
        # 部屋の名前と天井の高さ。壁と壁の間ごとに、いちばん近い部屋の名前を当てる
        ws = sorted(v for v, _ in walls)
        for a_, b_ in zip(ws, ws[1:]):
            # 切断線に沿う向きで壁と壁の間にあり、切断線にいちばん近い部屋
            cands = [(abs((x_ if axis == "x" else y_) - c), n) for n, x_, y_, _ in ROOMS
                     if a_ < (y_ if axis == "x" else x_) < b_]
            if cands:
                n = min(cands)[1]
                u = sec_u(axis, (a_ + b_) / 2)
                text(n, P(u, FL + 1300), 220, "TEXT")
                text("CH=2,400", P(u, FL + 900), 150, "TEXT")
        # 通り芯と寸法
        grids = YS if axis == "x" else XS
        for name, v in grids.items():
            u = sec_u(axis, v)
            m.add_line(P(u, -1300), P(u, -300), dxfattribs={"layer": "GRID"})
            text(name, P(u, -1600), 200, "GRID")
        gu = sorted(sec_u(axis, v) for v in grids.values())
        for a_, b_ in zip(gu, gu[1:]):
            dim(P(a_, 0), P(b_, 0), (0, oy - 2300))
        dim(P(0, 0), P(L, 0), (0, oy - 2800))
        top = round(EAVE_H + D / 2 * PITCH + ROOF_T)
        hs = [0, FL, CEIL, EAVE_H, top]
        for a_, b_ in zip(hs, hs[1:]):
            dim(P(0, a_), P(0, b_), (ox - 1500, 0), angle=90)
        dim(P(0, 0), P(0, top), (ox - 2100, 0), angle=90)
        for t_, h in (("GL", 0), ("FL", FL), ("天井", CEIL), ("軒高", EAVE_H)):
            text(t_, P(-2700, h), 150, "TEXT")
        text("ベタ基礎", P(L + 1000, 150), 160, "TEXT")
        text(f"{title}   S=1/100   （{look}を見る）", P(L / 2, -3600), 300, "TEXT")
        # 平面図に切断線を描く
        label = title[0]
        if axis == "x":
            m.add_line((c, -1800), (c, D + 1100), dxfattribs={"layer": "SECT_VIEW", "linetype": "DASHDOT", "ltscale": 20})
            for yy in (-1800, D + 1100):
                text(label, (c - 300, yy), 260, "TEXT")
                m.add_line((c, yy), (c + 500, yy), dxfattribs={"layer": "SECT_VIEW"})  # 東を見る矢印
                m.add_lwpolyline([(c + 500, yy - 80), (c + 650, yy), (c + 500, yy + 80)], close=True,
                                 dxfattribs={"layer": "SECT_VIEW"})
        else:
            m.add_line((-2100, c), (W + 900, c), dxfattribs={"layer": "SECT_VIEW", "linetype": "DASHDOT", "ltscale": 20})
            for xx in (-2100, W + 900):
                text(label, (xx, c - 300), 260, "TEXT")
                m.add_line((xx, c), (xx, c + 500), dxfattribs={"layer": "SECT_VIEW"})  # 北を見る矢印
                m.add_lwpolyline([(xx - 80, c + 500), (xx, c + 650), (xx + 80, c + 500)], close=True,
                                 dxfattribs={"layer": "SECT_VIEW"})


def thick(orient, at, a, b, t):
    """壁の中の開口を、壁の厚みより少し広い長方形にする。"""
    return box(a, at - t, b, at + t) if orient == "h" else box(at - t, a, at + t, b)


def wall_shape():
    bands = [LineString([(x1, y1), (x2, y2)]).buffer(t / 2, cap_style=3, join_style=2) for x1, y1, x2, y2, t in WALLS]
    walls = unary_union(bands)
    holes = [thick(o, at, a, b, EXT) for _, o, at, a, b, *_ in DOORS + SLIDES + FOLDS]
    holes += [thick(o, at, a, b, EXT) for o, at, a, b in OPENINGS]
    holes += [thick(o, at, a, b, EXT) for _, o, at, a, b in WINDOWS]
    return walls.difference(unary_union(holes))


def main(out, variant=None):
    if variant:
        VARIANTS[variant]()
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4
    doc.styles.add(JP_STYLE, font="kst32b.lff")
    for name, color, lt in (("WALL", 7, "CONTINUOUS"), ("GRID", 1, "CENTER"), ("DOOR", 3, "CONTINUOUS"),
                            ("WINDOW", 4, "CONTINUOUS"), ("FIXTURE", 8, "CONTINUOUS"), ("ELEV", 7, "CONTINUOUS"),
                            ("ELEV_WINDOW", 4, "CONTINUOUS"), ("ELEV_DETAIL", 8, "CONTINUOUS"), ("SECT", 7, "CONTINUOUS"),
                            ("SECT_VIEW", 8, "CONTINUOUS"), ("DIM", 2, "CONTINUOUS"), ("TEXT", 7, "CONTINUOUS")):
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
    # 引き戸: 閉じた位置の戸(実線の長方形)と、引き込んだときの戸(破線の長方形)
    for _, o, at, a, b, face, way in SLIDES:
        off = face * (PART / 2 + 25)  # 壁の面のすぐ外に置き、壁の線と重ならないようにする
        w = b - a

        def box_(u0, u1, ltype):
            pts = [(u0, off - 25), (u1, off - 25), (u1, off + 25), (u0, off + 25)]
            pts = [(u, at + d) if o == "h" else (at + d, u) for u, d in pts]
            m.add_lwpolyline(pts, close=True, dxfattribs={"layer": "DOOR", "linetype": ltype, "ltscale": 8})
        box_(a - 30, b + 30, "CONTINUOUS")
        box_(*((b, b + w) if way > 0 else (a - w, a)), "DASHED")
    # 折れ戸: 2枚の戸が、開口の内側へ「く」の字に折れる
    for _, o, at, a, b, side in FOLDS:
        mid, depth = (a + b) / 2, (b - a) / 2 * 0.6
        pts = [(a, 0), (mid, side * depth), (b, 0)]
        pts = [(u, at + d) if o == "h" else (at + d, u) for u, d in pts]
        m.add_lwpolyline(pts, dxfattribs={"layer": "DOOR"})
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
        if size == "small":  # 細い部屋は、文字を小さくして縦に書く
            for i, ch in enumerate(name):
                m.add_text(ch, height=130, dxfattribs={"layer": "TEXT", "style": JP_STYLE}).set_placement(
                    (x, y + (len(name) / 2 - i) * 160), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
            continue
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
    def text(s_, at, h, layer):
        m.add_text(s_, height=h, dxfattribs={"layer": layer, "style": JP_STYLE}).set_placement(
            at, align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    draw_elevations(m, dim, text)
    draw_sections(m, dim, text)
    doc.saveas(out)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
