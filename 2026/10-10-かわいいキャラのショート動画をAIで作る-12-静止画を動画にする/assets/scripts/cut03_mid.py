"""カット3の中間の絵。ぬめが石の前の面を半分登った所。

Wan に任せると、登る所でぬめが縦に立ち上がり、ウサギに見えた(wan-cut03-1)。
登る途中の形をこちらで決め、始点→中間、中間→終点の2本に分けて生成する。
引数: 回転角 中心x 足元y 触角の角度。触角は始点40°と終点70°の間にする。
"""
import sys, os
from pathlib import Path
from PIL import Image

S19 = Path(__file__).resolve().parents[3] / "10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets"
OUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(S19 / "work"))
os.chdir(S19)
from antenna import tilt
from compose import bg_crop, put_nume, H, W

rot, cx, foot_y, ant = [int(v) for v in sys.argv[1:5]]
name = sys.argv[5] if len(sys.argv) > 5 else "py-cut03-mid.png"
nume = tilt(Image.open("work/nume-side.png"), pivot=(240, 430), y0=388, deg=ant, x_max=328)
box = (0, 665, 400, 665 + round(400 * H / W))
c = bg_crop("input/bg-c1-evening.jpeg", box)
put_nume(c, nume, 330, cx=cx, foot_y=foot_y, ratio=1.3, mirror=True, rotate=rot, shadow=False)
c.convert("RGB").save(OUT / name)
