"""#136 の課題1(南の外壁の矩計図)を、ルールで採点する。

正しい描き方は1つではないので、正解の図面と線を比べず、仕様から決まる値があるかを見る。
矩計図は x=50,000 付近の、元の図面に何もない場所に描かせた。その範囲の図形だけを、描いた図形とみなす。
点は 15 項目の合計(各1点。寸法と層は、満たした割合で部分点)。項目は tasks/K-1.md の採点のルールに沿う。

座標は、通り芯 Y1 が x=50,000、GL が y=-10,500。高さは GL からの値で書く。

使い方: uv run --with ezdxf python code/drawings/check_k1.py <元の図面.dxf> <描いた図面.dxf> [--json]
"""
import json
import sys
from collections import Counter

import ezdxf

X0, GL = 50000.0, -10500.0
REGION = (44000, -15000, 56000, -3000)   # 描いた図形を探す範囲(元の図面には何もない)。題を他の図の題と同じ y=-14,100 に置くモデルがあるので、下は -15,000 まで


def inside(pts):
    return all(REGION[0] <= x <= REGION[2] and REGION[1] <= y <= REGION[3] for x, y in pts)


def entity_points(e):
    t = e.dxftype()
    try:
        if t == "LINE":
            return [tuple(e.dxf.start)[:2], tuple(e.dxf.end)[:2]]
        if t == "LWPOLYLINE":
            return [tuple(p[:2]) for p in e.get_points("xy")]
        if t == "POLYLINE":
            return [tuple(v.dxf.location)[:2] for v in e.vertices]
        if t in ("TEXT", "MTEXT", "INSERT"):
            return [tuple(e.dxf.insert)[:2]]
        if t in ("CIRCLE", "ARC"):
            return [tuple(e.dxf.center)[:2]]
        if t == "DIMENSION":
            return [tuple(e.dxf.defpoint)[:2]]
        if t == "HATCH":
            return [tuple(v)[:2] for p in e.paths for v in getattr(p, "vertices", [])] or None
    except Exception:
        return None
    return None


def segments(e):
    """線分の列。ポリラインは辺に分ける(ふくらみは無視)。部品(INSERT)は展開する。"""
    t = e.dxftype()
    if t == "LINE":
        return [(tuple(e.dxf.start)[:2], tuple(e.dxf.end)[:2])]
    if t in ("LWPOLYLINE", "POLYLINE"):
        pts = entity_points(e)
        closed = e.closed if t == "LWPOLYLINE" else e.is_closed
        if closed:
            pts = pts + pts[:1]
        return list(zip(pts, pts[1:]))
    if t == "INSERT":
        out = []
        for v in e.virtual_entities():
            out += segments(v)
        return out
    return []


def text_of(e):
    t = e.dxftype()
    if t == "TEXT":
        return e.dxf.text
    if t == "MTEXT":
        return e.plain_text()
    return ""


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
    segs = [s for e in new for s in segments(e)]
    horiz = [(min(a[0], b[0]), max(a[0], b[0]), a[1]) for a, b in segs if abs(a[1] - b[1]) < 0.01 and abs(a[0] - b[0]) > 1]
    vert = [(min(a[1], b[1]), max(a[1], b[1]), a[0]) for a, b in segs if abs(a[0] - b[0]) < 0.01 and abs(a[1] - b[1]) > 1]
    sloped = [(a, b) for a, b in segs if abs(b[0] - a[0]) > 100 and abs(abs((b[1] - a[1]) / (b[0] - a[0])) - 0.4) < 0.002]
    texts = [text_of(e) for e in new if e.dxftype() in ("TEXT", "MTEXT")]

    def h_at(h, xa, xb, tol=2):  # 高さ h(GL から)に、x の範囲 [xa, xb] にかかる水平線があるか
        return any(abs(y - (GL + h)) <= tol and x1 < xb and x2 > xa for x1, x2, y in horiz)

    def v_at(x, tol=1, ya=None, yb=None):
        return any(abs(xx - x) <= tol and (ya is None or (y1 < GL + yb and y2 > GL + ya)) for y1, y2, xx in vert)

    items = {}
    # 1. 置く場所: 通り芯 Y1 と GL の線
    items["置く場所(Y1 と GL)"] = float(any(abs(xx - X0) <= 2 and y2 - y1 > 1000 for y1, y2, xx in vert)
                                     and any(abs(y - GL) <= 2 and x2 - x1 > 500 for x1, x2, y in horiz))
    # 2〜5. 高さ
    items["基礎上端 GL+400"] = float(h_at(400, X0 - 75, X0 + 75))
    items["FL GL+561"] = float(h_at(561, X0 - 1700, X0 - 100))
    items["天井 GL+2,961"] = float(h_at(2961, X0 - 1700, X0 - 100))
    items["軒の高さ GL+3,311"] = float(h_at(3311, X0 - 60, X0 + 60))
    # 6. 床の層: 土台の下(420)、土台の上(525)、合板の上(549)
    floor = [h_at(h, X0 - 300, X0 + 50, tol=1) for h in (420, 525, 549)]
    items["床の層(土台・合板・フローリング)"] = sum(floor) / 3
    # 7. 外壁の層: 石膏ボード、柱の内外の面、合板、胴縁、サイディング(窓の上で見る)
    wall_x = (X0 - 52.5 - 12.5, X0 - 52.5, X0 + 52.5, X0 + 61.5, X0 + 79.5, X0 + 93.5)
    wall = [v_at(x, ya=2600, yb=3300) for x in wall_x]
    items["外壁の層(柱 105・合板 9・胴縁 18・サイディング 14・石膏ボード 12.5)"] = min(1.0, sum(wall) / 5)
    # 8. 勾配
    items["勾配 4/10 の線"] = float(any(abs(b[0] - a[0]) > 400 for a, b in sloped))

    # 9. 垂木の下面が Y1 の上で軒の高さを通る
    def y_on(a, b, x):
        return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])
    items["垂木の下面が Y1 で GL+3,311"] = float(any(min(a[0], b[0]) <= X0 <= max(a[0], b[0])
                                                 and abs(y_on(a, b, X0) - (GL + 3311)) <= 3 for a, b in sloped))
    # 10. 軒の出 600: 勾配の線の端か、縦の線が x=50,600 にある
    tip = [p for a, b in sloped for p in (a, b) if abs(p[0] - (X0 + 600)) <= 5]
    tip += [(xx, y1) for y1, y2, xx in vert if abs(xx - (X0 + 600)) <= 5 and y2 > GL + 3000]
    items["軒の出 600"] = float(bool(tip))
    # 11. 寸法: 指示した5つ(勾配の表示は 12 で見る)。書かれた値と測った長さが合うもの
    want = {400: "GL〜基礎上端", 161: "基礎上端〜FL", 2400: "FL〜天井", 2750: "FL〜軒の高さ", 600: "軒の出"}
    found = set()
    dim_detail = []
    for e in new:
        if e.dxftype() != "DIMENSION":
            continue
        try:
            m = round(e.get_measurement(), 1)
        except Exception:
            continue
        label = (e.dxf.get("text", "") or "").replace(",", "")
        ok_label = label in ("", "<>") or label.strip() == f"{m:g}"
        dim_detail.append({"measured": m, "label": e.dxf.get("text", ""), "label_ok": ok_label})
        for v in want:
            if abs(m - v) <= 1 and ok_label:
                found.add(v)
    items["寸法(400・161・2,400・2,750・600)"] = len(found) / len(want)
    # 12. 勾配の表示
    items["勾配の表示 4/10"] = float(any("4/10" in t.replace(" ", "").replace("／", "/") for t in texts))
    # 13. 題
    items["題「矩計図 S=1/20」"] = float(any("矩計図" in t and "1/20" in t for t in texts))
    # 14. レイヤー
    layers = Counter(e.dxf.layer for e in new)
    need = ("KANA_CUT", "KANA_VIEW", "KANA_INS", "DIM", "TEXT")
    items["レイヤー(KANA_CUT・KANA_VIEW・KANA_INS・DIM・TEXT)"] = sum(1 for n in need if layers[n]) / len(need)
    # 15. 元の図形を壊していない: 範囲の外の図形の数が、レイヤーごとに同じ
    a, b = Counter(e.dxf.layer for e in base_old), Counter(e.dxf.layer for e in old)
    lost = {k: a[k] - b.get(k, 0) for k in a if a[k] > b.get(k, 0)}
    items["元の図形を壊していない"] = float(not lost)

    return {
        "score": round(sum(items.values()), 2), "max": len(items), "items": items,
        "detail": {"new_entities": len(new), "layers": dict(layers), "dims": dim_detail,
                   "floor_lines": dict(zip((420, 525, 549), floor)), "wall_lines": dict(zip(wall_x, wall)),
                   "lost_outside": lost, "texts": len(texts)},
    }


if __name__ == "__main__":
    r = check(sys.argv[1], sys.argv[2])
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"{r['score']} / {r['max']}")
        for k, v in r["items"].items():
            print(f"  {v:.2f}  {k}")
