"""#146 の課題1(LDK の南西の角の平面詳細図)を、ルールで採点する。

#136 の check_k1.py と同じ考え方。正しい描き方は1つではないので、正解の図面と線を比べず、仕様と元の平面図から決まる値があるかを見る。
平面詳細図は、元の平面図の X1・Y1 の交点を (56,000, -10,000) に移して描かせた。その近くの図形だけを、描いた図形とみなす。
点は 11 項目の合計(各1点。数で見る項目は、満たした割合で部分点)。

座標は、元の平面図の値(X1・Y1 の交点からの距離)で書く。南の外壁は Y1、西の外壁は X1。屋外は南(-y)と西(-x)。

使い方: uv run --with ezdxf python code/drawings/check_p1.py <元の図面.dxf> <描いた図面.dxf> [--json]
"""
import json
import sys
from collections import Counter

import ezdxf

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_k1 import entity_points, segments, text_of  # noqa: E402

X0, Y0 = 56000.0, -10000.0
REGION = (53500, -14500, 63500, -3500)   # 題を図の下に離して置くモデルがあるので、下は -14,500 まで
GRID_X = (0, 910, 2730, 4550)
GRID_Y = (0, 1820, 3640, 4550)
SOUTH_WIN = ((400, 2050), (2500, 4150))     # 南の窓の開口(x)
WEST_WIN = ((1200, 2400), (2800, 4000))     # 西の窓の開口(y)
# 外壁の層の面の、通り芯からの距離。屋外がマイナス
LAYERS = (-93.5, -79.5, -61.5, -52.5, 52.5, 65.0)


def inside(pts):
    return all(REGION[0] <= x <= REGION[2] and REGION[1] <= y <= REGION[3] for x, y in pts)


def split(path):
    doc = ezdxf.readfile(path)
    new, old = [], []
    for e in doc.modelspace():
        pts = entity_points(e)
        (new if pts and inside(pts) else old).append(e)
    return new, old


def check(base_path, path):
    new, old = split(path)
    _, base_old = split(base_path)
    segs = [s for e in new if e.dxftype() != "DIMENSION" for s in segments(e)]
    horiz = [(min(a[0], b[0]) - X0, max(a[0], b[0]) - X0, a[1] - Y0) for a, b in segs
             if abs(a[1] - b[1]) < 0.01 and abs(a[0] - b[0]) > 1]
    vert = [(min(a[1], b[1]) - Y0, max(a[1], b[1]) - Y0, a[0] - X0) for a, b in segs
            if abs(a[0] - b[0]) < 0.01 and abs(a[1] - b[1]) > 1]
    texts = [e for e in new if e.dxftype() in ("TEXT", "MTEXT")]

    def h_at(y, xa, xb, tol=1.0):   # 高さ y に、x の範囲 [xa, xb] を通る水平線があるか
        return any(abs(yy - y) <= tol and x1 <= xa and x2 >= xb for x1, x2, yy in horiz)

    def v_at(x, ya, yb, tol=1.0):
        return any(abs(xx - x) <= tol and y1 <= ya and y2 >= yb for y1, y2, xx in vert)

    items = {}
    # 1. 置く場所: X1 と Y1 の通り芯
    items["置く場所(X1・Y1 の通り芯)"] = float(any(abs(xx) <= 2 and y2 - y1 > 2000 for y1, y2, xx in vert)
                                         and any(abs(y) <= 2 and x2 - x1 > 2000 for x1, x2, y in horiz))
    # 2. ほかの通り芯
    others = [any(abs(xx - g) <= 2 and y2 - y1 > 2000 for y1, y2, xx in vert) for g in GRID_X[1:]]
    others += [any(abs(y - g) <= 2 and x2 - x1 > 2000 for x1, x2, y in horiz) for g in GRID_Y[1:]]
    items["通り芯 X2〜X4・Y2〜Y4"] = sum(others) / len(others)
    # 3〜4. 外壁の層: 窓と窓の間の壁で見る(南は x=2,050〜2,500、西は y=2,400〜2,800)
    south = [h_at(d, 2100, 2450) for d in LAYERS]
    west = [v_at(d, 2450, 2750) for d in LAYERS]
    items["南の外壁の層(柱 105・合板 9・胴縁 18・サイディング 14・石膏ボード 12.5)"] = min(1.0, sum(south) / 5)
    items["西の外壁の層"] = min(1.0, sum(west) / 5)
    # 5. 柱: 105 角の四角。角(X1-Y1、X4-Y1)と、窓の開口の両わき
    want = [(0, 0), (4550, 0)]
    want += [(x, 0) for a, b in SOUTH_WIN for x in (a - 52.5, b + 52.5)]
    want += [(0, y) for a, b in WEST_WIN for y in (a - 52.5, b + 52.5)]
    cols = []
    for e in new:
        if e.dxftype() != "LWPOLYLINE":
            continue
        pts = e.get_points("xy")
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        if len(pts) >= 4 and abs(max(xs) - min(xs) - 105) < 3 and abs(max(ys) - min(ys) - 105) < 3:
            cols.append(((max(xs) + min(xs)) / 2 - X0, (max(ys) + min(ys)) / 2 - Y0))
    found_cols = [w for w in want if any(abs(c[0] - w[0]) <= 60 and abs(c[1] - w[1]) <= 60 for c in cols)]
    items["柱(角と窓の両わき、10本)"] = len(found_cols) / len(want)
    # 6. 開口の中の交点には柱がない(X2-Y1、X3-Y1、X1-Y2、X1-Y3)
    bad = [(910, 0), (2730, 0), (0, 1820), (0, 3640)]
    items["開口の中に柱を置いていない"] = float(not any(abs(c[0] - b[0]) <= 30 and abs(c[1] - b[1]) <= 30
                                              for c in cols for b in bad))
    # 7〜8. 寸法: 通り芯の間と、窓の開口。測った2点を、元の平面図の値で見る
    dims = []
    for e in new:
        if e.dxftype() != "DIMENSION":
            continue
        try:
            m = round(e.get_measurement(), 1)
        except Exception:
            continue
        p1, p2 = e.dxf.defpoint2, e.dxf.defpoint3
        horiz_dim = abs(p1.x - p2.x) >= abs(p1.y - p2.y)
        a, b = sorted((p1.x - X0, p2.x - X0) if horiz_dim else (p1.y - Y0, p2.y - Y0))
        dims.append(("x" if horiz_dim else "y", round(a), round(b), m))

    def has_dim(ax, a, b):
        return any(d[0] == ax and abs(d[1] - a) <= 2 and abs(d[2] - b) <= 2 for d in dims)
    grid_want = [("x", a, b) for a, b in zip(GRID_X, GRID_X[1:])] + [("y", a, b) for a, b in zip(GRID_Y, GRID_Y[1:])]
    items["寸法: 通り芯の間(6つ)"] = sum(has_dim(*w) for w in grid_want) / len(grid_want)
    win_want = [("x", a, b) for a, b in SOUTH_WIN] + [("y", a, b) for a, b in WEST_WIN]
    win_want += [("x", 0, 400), ("y", 0, 1200)]   # 窓の位置(通り芯から)
    items["寸法: 窓の幅と位置(通り芯から)"] = sum(has_dim(*w) for w in win_want) / len(win_want)
    # 9. 文字の高さ 150(題を含む)
    heights = [e.dxf.char_height if e.dxftype() == "MTEXT" else e.dxf.height for e in texts]
    items["文字の高さ 150"] = (sum(1 for h in heights if abs(h - 150) <= 5) / len(heights)) if heights else 0.0
    # 10. 題
    items["題「平面詳細図 S=1/50」"] = float(any("平面詳細図" in text_of(e) and "1/50" in text_of(e) for e in texts))
    # 11. レイヤー
    layers = Counter(e.dxf.layer for e in new)
    need = ("PD_CUT", "PD_VIEW", "PD_INS", "DIM", "TEXT")
    items["レイヤー(PD_CUT・PD_VIEW・PD_INS・DIM・TEXT)"] = sum(1 for n in need if layers[n]) / len(need)
    # 12. 元の図形(矩計図を含む)を壊していない
    a, b = Counter(e.dxf.layer for e in base_old), Counter(e.dxf.layer for e in old)
    lost = {k: a[k] - b.get(k, 0) for k in a if a[k] > b.get(k, 0)}
    items["元の図形を壊していない"] = float(not lost)

    return {
        "score": round(sum(items.values()), 2), "max": len(items), "items": items,
        "detail": {"new_entities": len(new), "layers": dict(layers), "dims": dims, "columns": cols,
                   "south_layers": dict(zip(LAYERS, south)), "west_layers": dict(zip(LAYERS, west)),
                   "text_heights": sorted(Counter(round(h) for h in heights).items()), "lost_outside": lost},
    }


if __name__ == "__main__":
    r = check(sys.argv[1], sys.argv[2])
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2, default=float))
    else:
        print(f"{r['score']} / {r['max']}")
        for k, v in r["items"].items():
            print(f"  {v:.2f}  {k}")
