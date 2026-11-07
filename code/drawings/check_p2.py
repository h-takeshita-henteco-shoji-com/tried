"""#146 の課題2(矩計図と平面詳細図の切断位置をそろえる)を、ルールで採点する。

元の図面は、課題1で Opus が描いた図面(矩計図と平面詳細図が入っている)。2枚はもともとそろっているので、
切断線と記号を描き足し、矩計図の題を直すほかは、何も動かさないのが正解。
照らし合わせた結果(答えの文章)は、人が読む。

点は 8 項目の合計(各1点。数で見る項目は、満たした割合で部分点)。

使い方: uv run --with ezdxf python code/drawings/check_p2.py <元の図面.dxf> <描いた図面.dxf> [--json]
"""
import json
import sys
from collections import Counter

import ezdxf

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_k1 import entity_points, segments, text_of  # noqa: E402

CUT_X = 56000 + 1800          # 平面詳細図の上での、矩計図の切断位置
WALL_Y = (-10000 - 93.5, -10000 + 65)   # 南の外壁の外の面と内の面
KANA = (44000, -15000, 53500, -3000)   # 矩計図の範囲
PLAN = (53500, -14500, 63500, -3500)   # 平面詳細図の範囲


def region(pts, r):
    return pts and all(r[0] <= x <= r[2] and r[1] <= y <= r[3] for x, y in pts)


def sig(e):
    """図形の形の目印。種類、レイヤー、点の座標(0.1 単位)、文字。"""
    pts = entity_points(e) or []
    return (e.dxftype(), e.dxf.layer, tuple((round(x, 1), round(y, 1)) for x, y in pts), text_of(e))


def norm(t):
    return t.replace(" ", "").replace("　", "")


def check(base_path, path):
    base = list(ezdxf.readfile(base_path).modelspace())
    new = list(ezdxf.readfile(path).modelspace())
    bs, ns = Counter(sig(e) for e in base), Counter(sig(e) for e in new)
    added = [e for e in new if ns[sig(e)] > bs.get(sig(e), 0)]
    removed = {s: c - ns.get(s, 0) for s, c in bs.items() if c > ns.get(s, 0)}

    items = {}
    # 1. 切断線: x=57,800 で、南の外壁をまたぐ縦の線
    segs = [(s, e) for e in added for s in segments(e)]
    cut = [(a, b, e) for (a, b), e in segs if abs(a[0] - CUT_X) <= 5 and abs(b[0] - CUT_X) <= 5
           and min(a[1], b[1]) < WALL_Y[0] and max(a[1], b[1]) > WALL_Y[1]]
    items["切断線(x=1,800 で南の外壁をまたぐ)"] = float(bool(cut))
    items["切断線のレイヤー PD_VIEW"] = float(any(e.dxf.layer == "PD_VIEW" for _, _, e in cut))
    # 2. 矢印: 切断線の両端の近くに、東へ伸びる図形
    ends = []
    if cut:
        a, b, _ = cut[0]
        ends = [min(a, b, key=lambda p: p[1]), max(a, b, key=lambda p: p[1])]
    def east_mark(p):
        for e in added:
            pts = entity_points(e) or []
            if e.dxftype() in ("TEXT", "MTEXT", "DIMENSION") or not pts:
                continue
            xs = [q[0] for q in pts] + [q[0] for s in segments(e) for q in s]
            ys = [q[1] for q in pts] + [q[1] for s in segments(e) for q in s]
            if min(xs) >= CUT_X - 50 and max(xs) > CUT_X + 100 and min(abs(y - p[1]) for y in ys) < 700:
                return True
        return False
    items["見る向きの矢印(両端、東)"] = sum(east_mark(p) for p in ends) / 2 if ends else 0.0
    # 3. 記号 K1: 切断線の両端の近く
    k1 = [e for e in added if e.dxftype() in ("TEXT", "MTEXT") and "K1" in norm(text_of(e))
          and region(entity_points(e), PLAN)]
    near = [any(abs(e.dxf.insert.x - p[0]) < 1000 and abs(e.dxf.insert.y - p[1]) < 1000 for e in k1) for p in ends]
    items["記号 K1(両端)"] = (sum(near) / 2) if ends else min(1.0, len(k1) / 2)
    hs = [e.dxf.char_height if e.dxftype() == "MTEXT" else e.dxf.height for e in k1]
    items["記号の文字の高さ 150"] = (sum(1 for h in hs if abs(h - 150) <= 5) / len(hs)) if hs else 0.0
    # 4. 矩計図の題
    titles = [norm(text_of(e)) for e in new if e.dxftype() in ("TEXT", "MTEXT") and region(entity_points(e), KANA)]
    items["矩計図の題「矩計図 K1 S=1/20」"] = float(any(t == "矩計図K1S=1/20" for t in titles)
                                              and not any(t == "矩計図S=1/20" for t in titles))
    # 5. 矩計図のほかの図形を動かしていない(題を除く)
    kana_removed = [s for s in removed if region([p for p in s[2]], KANA) and not s[3].startswith("矩計図")]
    items["矩計図のほかの図形を動かしていない"] = float(not kana_removed)
    # 6. 平面詳細図と、そのほかの図形を動かしていない
    other_removed = [s for s in removed if not region([p for p in s[2]], KANA)]
    items["平面詳細図とほかの図形を動かしていない"] = float(not other_removed)

    return {
        "score": round(sum(items.values()), 2), "max": len(items), "items": items,
        "detail": {"added": len(added), "added_layers": dict(Counter(e.dxf.layer for e in added)),
                   "removed_kana": [list(map(str, s[:2])) + [s[3]] for s in kana_removed][:20],
                   "removed_other": [list(map(str, s[:2])) + [s[3]] for s in other_removed][:20],
                   "k1_heights": hs, "kana_titles": titles},
    }


if __name__ == "__main__":
    r = check(sys.argv[1], sys.argv[2])
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2, default=float))
    else:
        print(f"{r['score']} / {r['max']}")
        for k, v in r["items"].items():
            print(f"  {v:.2f}  {k}")
