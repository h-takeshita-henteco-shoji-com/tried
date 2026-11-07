"""#133 の積算(内装と建具)の正解を、図面のもとの間取りのデータ(make_house.py)から計算する。

積算の条件は、その日のフォルダの tasks/estimate-spec.md。AI には渡さない。
- 部屋の内法の形は、通り芯で囲んだ範囲から、壁の帯(開口を抜かない)を引いて作る。扉の下の床は拾わない
- 壁の長さは、内法の周長から、壁のない境(玄関とホールの上がり框)を除いたもの
- 壁の面積は、壁の長さ × 天井高 2,400 から、0.5m² を超える開口を引く
- 巾木は、壁の長さから、床まである開口(扉、扉のない開口、掃き出し窓)の幅を引く

使い方: uv run --with ezdxf --with shapely python code/drawings/estimate_133.py [--json]
"""
import json
import sys
from collections import defaultdict

from shapely.geometry import LineString, Point, box
from shapely.ops import unary_union

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import make_house as H  # noqa: E402

CH = 2400
WALLS = unary_union([LineString([(x1, y1), (x2, y2)]).buffer(t / 2, cap_style=3, join_style=2)
                     for x1, y1, x2, y2, t in H.WALLS])

# 部屋: 名前 → (通り芯で囲んだ範囲, 床, 巾木)。ホールは寝室2の前の通路を含み、トイレを除く
ROOMS = {
    "LDK": (box(0, 0, 4550, 5460), "フローリング", "木製巾木"),
    "玄関": (box(4550, 0, 6370, 1820), "磁器質タイル", None),
    "ホール": (unary_union([box(4550, 1820, 6370, 5460), box(6370, 3640, 7280, 4550)])
             .difference(box(4550, 3640, 5460, 5460)), "フローリング", "木製巾木"),
    "寝室1": (box(6370, 0, 10010, 3640), "フローリング", "木製巾木"),
    "寝室1のクローゼット": (box(7280, 3640, 10010, 4550), "フローリング", "木製巾木"),
    "寝室2": (box(6370, 4550, 10010, 7280), "フローリング", "木製巾木"),
    "トイレ": (box(4550, 3640, 5460, 5460), "クッションフロア", "ソフト巾木"),
    "洗面脱衣": (box(2730, 5460, 4550, 7280), "クッションフロア", "ソフト巾木"),
    "ファミクロ": (box(4550, 5460, 6370, 7280), "フローリング", "木製巾木"),
    "パントリー": (box(0, 5460, 910, 7280), "フローリング", "木製巾木"),
}
BATH = box(910, 5460, 2730, 7280)

PRICE = {"フローリング": 8500, "磁器質タイル": 12000, "クッションフロア": 4000, "ビニルクロス(壁)": 1300,
         "ビニルクロス(天井)": 1500, "木製巾木": 1200, "ソフト巾木": 800, "ユニットバス 1616": 750000}
# 建具: (種類, 幅, 高さ) → (単価の項目, 単価)
SASH = {("掃き出し窓", 1650, 2000): 120000, ("腰窓", 1650, 1100): 75000, ("腰窓", 1200, 1100): 60000,
        ("腰窓", 600, 1100): 38000, ("高窓", 700, 500): 30000}


def inner(name):
    return ROOMS[name][0].difference(WALLS)


def room_of(x, y):
    p = Point(x, y)
    for n in ROOMS:
        if inner(n).buffer(1).contains(p):
            return n
    return "浴室" if BATH.contains(p) else "屋外"


def openings():
    """開口: (名前, 種類, 向き, 壁の座標, 始まり, 終わり, 高さ, 床まであるか)。"""
    out = []
    for n, o, at, a, b, *_ in H.DOORS:
        h = H.OPENING_H.get(n)
        out.append((n, "開き戸", o, at, a, b, (h[1] - h[0]) if h else 2000, True))
    for n, o, at, a, b, *_ in H.SLIDES:
        out.append((n, "引き戸", o, at, a, b, 2000, True))
    for n, o, at, a, b, *_ in H.FOLDS:
        out.append((n, "折れ戸", o, at, a, b, 2000, True))
    for i, (o, at, a, b) in enumerate(H.OPENINGS):
        out.append((["パントリーの入口", "寝室1のクローゼットの入口"][i], "扉のない開口", o, at, a, b, 2000, True))
    for n, o, at, a, b in H.WINDOWS:
        lo, hi = H.OPENING_H[n]
        kind = "掃き出し窓" if lo == 0 else "高窓" if lo >= 1400 else "腰窓"
        out.append((n, kind, o, at, a, b, hi - lo, lo == 0))
    return out


def sides(o, at, a, b):
    m = (a + b) / 2
    pts = [(m, at - 100), (m, at + 100)] if o == "h" else [(at - 100, m), (at + 100, m)]
    return [room_of(*p) for p in pts]


def wall_length(poly):
    """内法の周長のうち、外側に壁があるところの長さ。"""
    total = 0.0
    cs = list(poly.exterior.coords)
    for (x1, y1), (x2, y2) in zip(cs, cs[1:]):
        seg = LineString([(x1, y1), (x2, y2)])
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = seg.length
        nx, ny = dy / L, -dx / L       # 右の法線。どちらが外側でも、壁のある側を探す
        if any(WALLS.contains(Point(mx + s * nx * 5, my + s * ny * 5)) for s in (1, -1)):
            total += L
    return total


def compute():
    ops = openings()
    rooms = {}
    for n, (_, floor, base) in ROOMS.items():
        poly = inner(n)
        wl = wall_length(poly)
        mine = [op for op in ops if n in sides(*op[2:6])]
        ded = [(op[0], (op[5] - op[4]) * op[6] / 1e6) for op in mine]
        ded_area = sum(a for _, a in ded if a > 0.5)
        base_cut = sum(op[5] - op[4] for op in mine if op[7])
        rooms[n] = {
            "床": round(poly.area / 1e6, 2), "床の材料": floor, "天井": round(poly.area / 1e6, 2),
            "壁の長さ": round(wl / 1000, 2), "壁": round((wl * CH / 1e6) - ded_area, 2),
            "差し引いた開口": [f"{k} {a:.2f}" for k, a in ded if a > 0.5],
            "差し引かない開口": [f"{k} {a:.2f}" for k, a in ded if a <= 0.5],
            "巾木": round((wl - base_cut) / 1000, 2) if base else 0.0, "巾木の材料": base,
        }
    totals = defaultdict(float)
    for r in rooms.values():
        totals[r["床の材料"]] += r["床"]
        totals["ビニルクロス(壁)"] += r["壁"]
        totals["ビニルクロス(天井)"] += r["天井"]
        if r["巾木の材料"]:
            totals[r["巾木の材料"]] += r["巾木"]
    totals = {k: round(v, 2) for k, v in totals.items()}
    lines = [(k, v, PRICE[k], round(v * PRICE[k])) for k, v in totals.items()]
    lines.append(("ユニットバス 1616", 1, 750000, 750000))
    # 建具(浴室の折れ戸はユニットバスに含むので除く)
    sash = defaultdict(int)
    for n, kind, o, at, a, b, h, _ in ops:
        if kind in ("掃き出し窓", "腰窓", "高窓"):
            sash[(kind, b - a, h)] += 1
    for k, c in sash.items():
        lines.append((f"{k[0]} {k[1]}×{k[2]}", c, SASH[k], c * SASH[k]))
    doors = {"玄関ドア": 1, "勝手口ドア": 1, "室内片開き戸": 2, "室内引き戸": len(H.SLIDES)}
    dp = {"玄関ドア": 350000, "勝手口ドア": 120000, "室内片開き戸": 55000, "室内引き戸": 65000}
    for k, c in doors.items():
        lines.append((k, c, dp[k], c * dp[k]))
    return {"rooms": rooms, "totals": totals, "lines": lines, "total": sum(l[3] for l in lines)}


if __name__ == "__main__":
    r = compute()
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        sys.exit()
    for n, v in r["rooms"].items():
        print(f"{n}: 床 {v['床']}m²({v['床の材料']}) 壁の長さ {v['壁の長さ']}m 壁 {v['壁']}m² 巾木 {v['巾木']}m")
        print(f"    差し引いた: {v['差し引いた開口']}  差し引かない: {v['差し引かない開口']}")
    print()
    for k, q, p, amt in r["lines"]:
        print(f"{k}: {q} × {p:,} = {amt:,}")
    print(f"合計 {r['total']:,} 円")
