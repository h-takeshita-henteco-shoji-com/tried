"""AI が寸法を変更した DXF を、正解の図面と比べる(#135)。

AI が壁を線で描き直すなど、部品の作り方を変えても比べられるよう、部品の数ではなく線の長さで比べる。
- 図形: レイヤー(平面図の WALL、DOOR、WINDOW、FIXTURE、GRID、立面図の ELEV、ELEV_WINDOW、ELEV_DETAIL、断面図の SECT、SECT_VIEW)ごとに、線と円弧を線分に直して重ね、
  正解にない線(余分)と、正解にあって無い線(不足)の長さを mm で出す。1mm までのずれは同じとみなす
- 寸法: DIMENSION ごとに、書かれた値、測る2点の間の長さ、画面に描かれる文字(寸法のブロックの中の文字)を出す。
  3つが食い違う寸法と、正解と値が違う寸法を挙げる

立面図と断面図は、図の中で建物をどこに置くかに意味がない(東の端をそろえても西の端をそろえても正しい)。
そのため図ごとに切り出し、正解と左右の端のどちらかをそろえる位置へずらして、差の小さい方で比べる(2026-11-03 に追加)。

使い方:
  uv run --with ezdxf --with shapely python check_change.py <変更後.dxf> <正解.dxf> [--json 出力.json]
"""
import argparse
import json
import math
import re

import ezdxf
from shapely.geometry import LineString, MultiLineString
from shapely.ops import unary_union

LAYERS = ["WALL", "DOOR", "WINDOW", "FIXTURE", "GRID", "ELEV", "ELEV_WINDOW", "ELEV_DETAIL", "SECT", "SECT_VIEW"]
TOL = 1.0


def segments(entity):
    t = entity.dxftype()
    if t == "LINE":
        return [((entity.dxf.start.x, entity.dxf.start.y), (entity.dxf.end.x, entity.dxf.end.y))]
    if t == "LWPOLYLINE":
        pts = [(p[0], p[1]) for p in entity.get_points("xy")]
        if entity.closed:
            pts.append(pts[0])
        return list(zip(pts, pts[1:]))
    if t == "POLYLINE":
        pts = [(v.dxf.location.x, v.dxf.location.y) for v in entity.vertices]
        if entity.is_closed:
            pts.append(pts[0])
        return list(zip(pts, pts[1:]))
    if t == "ELLIPSE":
        pts = [(p.x, p.y) for p in entity.flattening(1)]
        return list(zip(pts, pts[1:]))
    if t in ("ARC", "CIRCLE"):
        c, r = entity.dxf.center, entity.dxf.radius
        a0, a1 = (entity.dxf.start_angle, entity.dxf.end_angle) if t == "ARC" else (0, 360)
        if a1 < a0:
            a1 += 360
        n = max(8, int((a1 - a0) / 5))
        pts = [(c.x + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                c.y + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        return list(zip(pts, pts[1:]))
    return []


def layer_lines(doc):
    out = {l: [] for l in LAYERS}
    for e in doc.modelspace():
        layer = e.dxf.layer.upper()
        if layer in out:
            out[layer] += [s for s in segments(e) if s[0] != s[1]]
    return {l: unary_union([LineString(s) for s in segs]) if segs else MultiLineString() for l, segs in out.items()}


def dims(doc):
    out = []
    for d in doc.modelspace().query("DIMENSION"):
        try:
            meas = round(d.get_measurement())
        except Exception:  # noqa: BLE001  回転などで測れない寸法は飛ばす
            continue
        text = d.dxf.get("text", "<>")
        shown = None
        block = doc.blocks.get(d.dxf.get("geometry", "")) if d.dxf.hasattr("geometry") else None
        if block is not None:
            for e in block:
                if e.dxftype() in ("MTEXT", "TEXT"):
                    shown = e.plain_text() if e.dxftype() == "MTEXT" else e.dxf.text
        written = meas if text in ("", "<>") else text
        num = re.sub(r"[^\d.]", "", str(written))
        out.append({"measurement": meas, "text": text, "shown": shown,
                    "value": float(num) if num else None,
                    "p1": [round(d.dxf.defpoint2.x), round(d.dxf.defpoint2.y)],
                    "p2": [round(d.dxf.defpoint3.x), round(d.dxf.defpoint3.y)]})
    return out


# 図の範囲(#135 の図面一式。make_house.py の置き場所に合わせる)。平面図は動かさずに比べる
VIEWS = {
    "plan": (-6000, -5000, 15000, 13000),
    "elev_S": (-6000, -15500, 13000, -5000), "elev_N": (-6000, -27000, 13000, -15500),
    "elev_E": (13000, -15500, 27300, -5000), "elev_W": (13000, -27000, 27300, -15500),
    "sect_A": (27300, -15500, 45000, -5000), "sect_B": (27300, -27000, 45000, -15500),
}
ANCHOR = {"elev": "ELEV", "sect": "SECT"}


def clip(lines, rect):
    from shapely.geometry import box as _box
    return lines.intersection(_box(*rect))


def compare(changed, expected):
    from shapely import affinity
    a, b = ezdxf.readfile(changed), ezdxf.readfile(expected)
    la, lb = layer_lines(a), layer_lines(b)
    geom = {l: {"extra_mm": 0, "missing_mm": 0} for l in LAYERS}
    shifts = {}
    for view, rect in VIEWS.items():
        ca = {l: clip(la[l], rect) for l in LAYERS}
        cb = {l: clip(lb[l], rect) for l in LAYERS}
        cands = [0.0]
        anchor = ANCHOR.get(view.split("_")[0])
        if anchor and not ca[anchor].is_empty and not cb[anchor].is_empty:
            (ax0, _, ax1, _), (bx0, _, bx1, _) = ca[anchor].bounds, cb[anchor].bounds
            cands += [bx0 - ax0, bx1 - ax1]
        best = None
        for dx in cands:
            d = {}
            for l in LAYERS:
                g = affinity.translate(ca[l], xoff=dx) if dx else ca[l]
                d[l] = (g.difference(cb[l].buffer(TOL)).length, cb[l].difference(g.buffer(TOL)).length)
            tot = sum(x + y for x, y in d.values())
            if best is None or tot < best[0]:
                best = (tot, dx, d)
        shifts[view] = round(best[1])
        for l, (x, y) in best[2].items():
            geom[l]["extra_mm"] += round(x)
            geom[l]["missing_mm"] += round(y)
    da, db = dims(a), dims(b)
    inconsistent = [d for d in da if d["value"] is not None and
                    (abs(d["value"] - d["measurement"]) > 0.5 or
                     (d["shown"] is not None and re.sub(r"[^\d]", "", d["shown"]) != re.sub(r"[^\d]", "", str(d["text"] if d["text"] not in ("", "<>") else d["measurement"]))))]
    want = sorted(d["measurement"] for d in db)
    got = sorted(d["measurement"] for d in da)
    missing_dims = [v for v in want if v not in got or got.remove(v)]
    got = sorted(d["measurement"] for d in da)
    extra_dims = [v for v in got if v not in want or want.remove(v)]
    return {"geometry": geom, "view_shift_mm": shifts, "dims_inconsistent": inconsistent, "dims_missing": missing_dims, "dims_extra": extra_dims,
            "dims_count": [len(da), len(db)]}


def summary(r):
    lines = []
    for l, g in r["geometry"].items():
        lines.append(f"{l}: 余分 {g['extra_mm']}mm、不足 {g['missing_mm']}mm")
    moved = {k: v for k, v in r.get("view_shift_mm", {}).items() if v}
    if moved:
        lines.append(f"図の中で建物の置き方が違ったので、ずらして比べた図: {moved}")
    lines.append(f"寸法の数: {r['dims_count'][0]}（正解 {r['dims_count'][1]}）")
    lines.append(f"正解にない寸法の長さ: {r['dims_extra']}、正解にあって無い寸法の長さ: {r['dims_missing']}")
    for d in r["dims_inconsistent"]:
        lines.append(f"食い違う寸法: 書かれた値 {d['text']}、測った長さ {d['measurement']}、画面の文字 {d['shown']}")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("changed")
    ap.add_argument("expected")
    ap.add_argument("--json")
    x = ap.parse_args()
    r = compare(x.changed, x.expected)
    print(summary(r))
    if x.json:
        open(x.json, "w").write(json.dumps(r, ensure_ascii=False, indent=1))
