"""DXF のモデル空間を PNG に書き出す(#132)。

変換は「DXF → 画像」の向きだけにする。画像から DXF は作らない。
条件をそろえるため、白い背景に黒の線（印刷した図面と同じ）で、長い辺のピクセル数を固定して書き出す。
CAD の色は黒い背景向けで、白い背景では黄色などが読みにくいため。
色で意味を分ける図面（設備図など）は --color を付ける。黒い背景に元の色で書き出す。

使い方: uv run --with ezdxf --with matplotlib python dxf_to_png.py 入力.dxf [長い辺のpx] [--color]
"""
import sys

from ezdxf import bbox, recover
from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration
from ezdxf.addons.drawing.matplotlib import qsave

DPI = 100


def main(path: str, long_side: int = 3000, color: bool = False) -> None:
    doc, _ = recover.readfile(path)
    msp = doc.modelspace()
    ext = bbox.extents(msp, fast=True)
    w, h = ext.size.x, ext.size.y
    scale = long_side / max(w, h) / DPI
    out = path.rsplit(".", 1)[0] + ".png"
    if color:
        cfg = Configuration(background_policy=BackgroundPolicy.BLACK)
        bg = "#000000"
    else:
        cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK)
        bg = "#FFFFFF"
    qsave(msp, out, bg=bg, dpi=DPI, size_inches=(w * scale, h * scale), config=cfg)
    print(out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--color"]
    main(args[0], *(int(a) for a in args[1:2]), color="--color" in sys.argv)
