"""カット3の始点の絵。ぬめが石の前の面のふもとにいて、登る前。

終点は #19 の py-cut03.png(登りきった姿、触角70°)。
始点は触角40°(前に倒す)にし、登る途中で下げる動きをAIに埋めさせる。
#19 の assets を作業場所にして実行する(compose.py の関数と素材を使うため)。
"""
import sys
from pathlib import Path
from PIL import Image

S19 = Path(__file__).resolve().parents[3] / "10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets"
OUT = Path(__file__).resolve().parents[1] / "generated"
sys.path.insert(0, str(S19 / "work"))
import os
os.chdir(S19)
from antenna import tilt
from compose import bg_crop, put_nume, H, W

nume_side = Image.open("work/nume-side.png")
nume_fwd = tilt(nume_side, pivot=(240, 430), y0=388, deg=40, x_max=328)
# 背景の切り出しは py-cut03 と同じ
box = (0, 665, 400, 665 + round(400 * H / W))
cx, foot_y = [int(v) for v in sys.argv[1:3]] if len(sys.argv) > 2 else (130, 800)
c = bg_crop("input/bg-c1-evening.jpeg", box)
put_nume(c, nume_fwd, 330, cx=cx, foot_y=foot_y, ratio=1.3, mirror=True)
c.convert("RGB").save(OUT / "py-cut03-start.png")
