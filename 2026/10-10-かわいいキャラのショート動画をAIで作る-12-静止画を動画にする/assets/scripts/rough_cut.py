"""全カットを絵コンテの秒数どおりにつなぎ、#20 の仮組みの音を付ける(仮組み)。本番の編集は #23 で行う。

- 秒数は #20 の rough_mix_4 に合わせる。カット6を4秒に延ばした版で、全部で36秒。
- どのカットも 768×1376・24コマ/秒にそろえる。Wan の2本(480×864)は拡大する。
- 秒数より短いカットは最後のコマを止めて延ばし、長いカットは切る。
- カット9は夜の静止画を5秒置くだけ。夕方から夜へ変わる重ね方は #23 で作る。
"""
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DAY = HERE.parents[1]
S19 = DAY / "10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets/generated"
S20 = DAY / "10-09-かわいいキャラのショート動画をAIで作る-10-声と音を付ける/assets/generated"
G = HERE / "generated"
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")

CUTS = [  # (ファイル, 秒数)
    (G / "py-cut01.mp4", 4),
    (G / "py-cut02.mp4", 3),
    (G / "wan-cut03-2.mp4", 3),
    (G / "py-cut04.mp4", 4),
    (G / "py-cut05.mp4", 3),
    (G / "py-cut06.mp4", 4),
    (G / "py-cut07.mp4", 3),
    (G / "py-cut08.mp4", 4),
    (S19 / "py-cut09.png", 5),
    (G / "wan-cut10-2.mp4", 3),
]

args, chains = [FFMPEG, "-v", "error", "-y"], []
for i, (f, sec) in enumerate(CUTS):
    if f.suffix == ".png":
        args += ["-loop", "1", "-t", str(sec), "-i", str(f)]
    else:
        args += ["-i", str(f)]
    chains.append(f"[{i}:v]scale=768:1376:flags=lanczos,fps=24,setsar=1,"
                  f"tpad=stop_mode=clone:stop_duration={sec},trim=duration={sec},setpts=PTS-STARTPTS[v{i}]")
args += ["-i", str(S20 / "rough_mix_4.wav")]
n = len(CUTS)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1[v]"
args += ["-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest",
         str(G / "rough-cut-1.mp4")]
subprocess.run(args, check=True)
print(G / "rough-cut-1.mp4")
