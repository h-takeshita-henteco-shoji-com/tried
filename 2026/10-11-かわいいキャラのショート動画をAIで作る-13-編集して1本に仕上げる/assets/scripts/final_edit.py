"""仮組み(#21)を土台に、ショート動画の本番を書き出す。

- 映像: #21 の採用カットをつなぐ。カット9は今日作った夕方から夜への版(py-cut09-dusk.mp4)に替える。
  カット6は台詞を替えて長くなったため5秒、カット7は空返事の前に間をあけるため4秒に延ばす。全部で38秒。
- 大きさ: 1080×1920(9:16)。768×1376 を横幅に合わせて拡大し、上下の数pxを切る。
- 字幕: 台詞2つだけ。顔に被らないよう、空の側(画面の上)に置く。字はヒラギノ丸ゴ。
- 音: mix_final.py で組んだ音を使い、約 -16 LUFS まで上げてリミッターで頭を抑える。
- 最後の1秒で暗転する(絵コンテのカット10)。
- BGM は再配布が禁止のため、BGM 入りの出力はリポジトリの外に書き出す。
  リポジトリには BGM なしの版を置く。

使い方: python final_edit.py [bgm]   bgm を付けると BGM 入りを ~/Music/tried-bgm/final/ に書き出す
"""
import os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DAY = HERE.parents[1]
S19 = DAY / "10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets/generated"
S20 = DAY / "10-09-かわいいキャラのショート動画をAIで作る-10-声と音を付ける/assets/generated"
S21 = DAY / "10-10-かわいいキャラのショート動画をAIで作る-12-静止画を動画にする/assets/generated"
G = HERE / "generated"
W_ = HERE / "work"
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FONT = "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
W, H, FPS = 1080, 1920, 24

CUTS = [  # (ファイル, 秒数)。秒数は mix_final.py の音に合わせた
    (S21 / "py-cut01.mp4", 4),
    (S21 / "py-cut02.mp4", 3),
    (S21 / "wan-cut03-2.mp4", 3),
    (S21 / "py-cut04.mp4", 4),
    (S21 / "py-cut05.mp4", 3),
    (S21 / "py-cut06.mp4", 5),  # 台詞を替えて4.2秒になったため、4秒から延ばした
    (S21 / "py-cut07.mp4", 4),  # 台詞と空返事の間をあけるため、3秒から延ばした
    (S21 / "py-cut08.mp4", 4),
    (G / "py-cut09-dusk.mp4", 5),
    (S21 / "wan-cut10-2.mp4", 3),
]
TOTAL = sum(s for _, s in CUTS)

SUBS = [  # (文字, 出す秒, 消す秒)。声の位置は mix_final.py の置き方から測った
    ("……んしょ", 7.9, 9.6),
    ("……んー。", 17.1, 18.8),
    ("今日は、", 18.85, 19.95),
    ("なんだかぬるめだなぁ", 19.95, 21.9),
    ("……ん、そっかぁ……", 23.4, 25.6),  # ぬめの空返事(カット7)
]

bgm = len(sys.argv) > 1 and sys.argv[1] == "bgm"
audio = Path.home() / "Music/tried-bgm/mix/final_mix_haru_no_kitchen.wav" if bgm else G / "mix-nobgm.wav"
gain = 11 if bgm else 5  # BGM 入りは -23.9 LUFS、なしは -19.3 LUFS。BGM 入りは声の頭がリミッターで削れる分、多めに上げる
if bgm:
    out = Path.home() / "Music/tried-bgm/final/nurui-yuugata-final.mp4"
else:
    out = G / "nurui-yuugata-nobgm.mp4"
out.parent.mkdir(parents=True, exist_ok=True)

args, chains = [FFMPEG, "-v", "error", "-y"], []
for i, (f, sec) in enumerate(CUTS):
    args += ["-i", str(f)]
    chains.append(f"[{i}:v]scale={W}:-2:flags=lanczos,crop={W}:{H},fps={FPS},setsar=1,"
                  f"tpad=stop_mode=clone:stop_duration={sec},trim=duration={sec},setpts=PTS-STARTPTS[v{i}]")
args += ["-i", str(audio)]
n = len(CUTS)

texts = []
for k, (t, a, b) in enumerate(SUBS):
    p = W_ / f"sub{k}.txt"
    p.write_text(t, encoding="utf-8")
    texts.append(f"drawtext=fontfile='{FONT}':textfile='{p}':fontsize=84:fontcolor=white:"
                 f"borderw=8:bordercolor=0x3a2f2a:x=(w-text_w)/2:y=h*0.17:"
                 f"alpha='min(1,min((t-{a})/0.15,({b}-t)/0.15))':enable='between(t,{a},{b})'")
fc = (";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1[cat];"
      f"[cat]{','.join(texts)},fade=t=out:st={TOTAL - 1}:d=1[v];"
      f"[{n}:a]volume={gain}dB,alimiter=limit=0.6:level=false,atrim=duration={TOTAL}[a]")
args += ["-filter_complex", fc, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-r", str(FPS), "-video_track_timescale", "24000", "-movflags", "+faststart", str(out)]
subprocess.run(args, check=True)
print(out)
