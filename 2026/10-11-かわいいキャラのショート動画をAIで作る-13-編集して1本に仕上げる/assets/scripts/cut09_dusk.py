"""カット9: 夕方から夜へ、空の色だけが変わる5秒を作る(仮組みでは夜の静止画を置いただけだった)。

- 背景は #19 の夕方(bg-c1-evening)と夜(bg-c9-night)を、コマごとに混ぜる。
- キャラは #19 の compose.py と同じ位置に置き、夜の色へ同じ割合で寄せる。
- 混ぜ方: 0.5秒止めてから、4秒かけてゆっくり変え、最後の0.5秒は夜で止める。
"""
import os, subprocess, sys
from pathlib import Path
from PIL import Image

DAY = Path(__file__).resolve().parents[3]
S19 = DAY / "10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets"
OUT = Path(__file__).resolve().parents[1] / "generated/py-cut09-dusk.mp4"
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FPS, SEC = 24, 5

os.chdir(S19)  # compose.py は assets からの相対パスで読む
sys.path.insert(0, str(S19 / "work"))
from compose import put_don, put_nume, night

don_front = Image.open("work/don-front.png")
nume_fwd = Image.open("work/nume-side-forward.png")
eve = Image.open("input/bg-c1-evening.jpeg").convert("RGBA")
ngt = Image.open("input/bg-c9-night.jpeg").convert("RGBA")
chars = Image.new("RGBA", eve.size)
put_don(chars, don_front, head_h=230, cx=575, water_y=1160)
put_nume(chars, nume_fwd, 230, cx=250, foot_y=800)
chars_n = night(chars)

def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)

p = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                      "-s", f"{eve.width}x{eve.height}", "-r", str(FPS), "-i", "-",
                      "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(OUT)],
                     stdin=subprocess.PIPE)
for i in range(FPS * SEC):
    k = ease((i / FPS - 0.5) / 4.0)
    c = Image.blend(eve, ngt, k)
    c.alpha_composite(Image.blend(chars, chars_n, k))
    p.stdin.write(c.convert("RGB").tobytes())
p.stdin.close()
p.wait()
print(OUT)
