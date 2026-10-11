"""カット2の中間の絵。ぬめが後ろを地面に付けたまま、頭を上げて葉の裏に触れた所。

Wan に始点=終点で「3回なめる」を任せると、1回だけ、舌は地面の側へ出た(wan-cut02-1)。
触れる姿をこちらで決め、始点→中間→始点を1回分として生成し、編集で3回繰り返す。
引数: 回転角 中心x 足元y 出力名。始点(py-cut02)は cx=330, foot_y=1090, 回転なし。
#19 の assets を作業場所にして実行する。
"""
import os
import sys
from pathlib import Path

from PIL import Image

S19 = Path(__file__).resolve().parents[3] / "10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets"
OUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(S19 / "work"))
os.chdir(S19)
from antenna import tilt  # noqa: E402
from compose import put_nume  # noqa: E402

rot, cx, foot_y = [int(v) for v in sys.argv[1:4]]
name = sys.argv[4]
nume_fwd = tilt(Image.open("work/nume-side.png"), pivot=(240, 430), y0=388, deg=40, x_max=328)
c = Image.open("input/bg-c2-fuki.jpeg").convert("RGBA")
put_nume(c, nume_fwd, 330, cx=cx, foot_y=foot_y, ratio=1.3, mirror=True, rotate=rot, shadow=rot == 0)
c.convert("RGB").save(OUT / name)
