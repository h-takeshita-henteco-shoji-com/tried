"""ベクターのPDFを、ページごとにDXFへ変換する(#132)。

PDFの線・曲線・塗りと文字を、そのままDXFの図形と文字に移す。
画像を経由しない（画像からDXFは作らない）。文字は文字データのまま残す。
座標は用紙上のmm。図面の縮尺には合わせない。

使い方: uv run --with pymupdf --with ezdxf python pdf_to_dxf.py 入力.pdf [ページ番号(1始まり) ...]
"""
import math
import sys

import ezdxf
import pymupdf
from ezdxf.enums import TextEntityAlignment
from ezdxf.math import Bezier4P, Vec2

PT_TO_MM = 25.4 / 72
# LibreCAD は文字スタイルの名前でフォントを探す。同梱の日本語フォント kst32b に合わせる
# （同梱の kochigothic は英数字しか持たない）
JP_STYLE = "kst32b"
JP_FONT = "NotoSansJP-Variable.ttf"
TEXT_HEIGHT_RATIO = 0.8  # PDFの文字の大きさ（em）に対する、DXFの文字の高さ


def to_mm(p, mat, height):
    q = pymupdf.Point(p) * mat
    return (q.x * PT_TO_MM, (height - q.y) * PT_TO_MM)


def subpaths(items, mat, height):
    """PDFのパスの要素を、つながった点の列に分ける。"""
    paths, cur = [], []
    for it in items:
        kind = it[0]
        if kind == "l":
            pts = [it[1], it[2]]
        elif kind == "c":
            bez = Bezier4P([Vec2(p.x, p.y) for p in it[1:5]])
            pts = [pymupdf.Point(v.x, v.y) for v in bez.flattening(0.2)]
        elif kind == "re":
            r = it[1]
            pts = [r.tl, r.tr, r.br, r.bl, r.tl]
        elif kind == "qu":
            q = it[1]
            pts = [q.ul, q.ur, q.lr, q.ll, q.ul]
        else:
            continue
        mm = [to_mm(p, mat, height) for p in pts]
        if cur and math.dist(cur[-1], mm[0]) < 1e-3 and kind in ("l", "c"):
            cur.extend(mm[1:])
        else:
            if len(cur) > 1:
                paths.append(cur)
            cur = mm
    if len(cur) > 1:
        paths.append(cur)
    return paths


def convert_page(page, out):
    doc = ezdxf.new("R2018", setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    doc.styles.add(JP_STYLE, font=JP_FONT)
    msp = doc.modelspace()
    mat = page.rotation_matrix
    height = page.rect.height

    for d in page.get_drawings():
        polys = subpaths(d["items"], mat, height)
        if d.get("fill") is not None and d["type"] in ("f", "fs"):
            hatch = msp.add_hatch(color=7)
            for pts in polys:
                hatch.paths.add_polyline_path(pts, is_closed=True)
        if d.get("color") is not None and d["type"] in ("s", "fs"):
            lw = max(0, min(211, round((d.get("width") or 0) * PT_TO_MM * 100)))
            for pts in polys:
                closed = math.dist(pts[0], pts[-1]) < 1e-3 and len(pts) > 2
                msp.add_lwpolyline(pts[:-1] if closed else pts, close=closed,
                                   dxfattribs={"lineweight": lw})

    for b in page.get_text("rawdict")["blocks"]:
        for line in b.get("lines", []):
            dx, dy = line["dir"]
            # ページの回転に合わせて文字の向きも回す
            v = pymupdf.Point(dx, dy) * mat - pymupdf.Point(0, 0) * mat
            angle = math.degrees(math.atan2(-v.y, v.x))
            for s in line["spans"]:
                text = "".join(c["c"] for c in s["chars"]).strip()
                if not text:
                    continue
                chars = [c for c in s["chars"] if c["c"].strip()]
                start = to_mm(chars[0]["origin"], mat, height)
                # 文字の幅を元のPDFに合わせる（フォントの違いで文字が重ならないように）
                last = chars[-1]
                end_pt = pymupdf.Point(last["origin"]) + pymupdf.Point(dx, dy) * (last["bbox"][2] - last["bbox"][0] if dx else last["bbox"][3] - last["bbox"][1])
                end = to_mm(end_pt, mat, height)
                t = msp.add_text(text, height=s["size"] * PT_TO_MM * TEXT_HEIGHT_RATIO,
                                 dxfattribs={"style": JP_STYLE})
                if len(chars) > 1 and math.dist(start, end) > 1e-3:
                    t.set_placement(start, end, align=TextEntityAlignment.FIT)
                else:
                    t.dxf.rotation = angle
                    t.set_placement(start)
    doc.saveas(out)


def main(path, pages):
    pdf = pymupdf.open(path)
    targets = pages or range(1, len(pdf) + 1)
    stem = path.rsplit(".", 1)[0]
    for n in targets:
        out = f"{stem}-p{n:02d}.dxf"
        convert_page(pdf[n - 1], out)
        print(out)


if __name__ == "__main__":
    main(sys.argv[1], [int(a) for a in sys.argv[2:]])
