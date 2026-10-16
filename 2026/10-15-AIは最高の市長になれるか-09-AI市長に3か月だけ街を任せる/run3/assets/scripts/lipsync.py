"""カットした動画の左下にぬめ、右下にどんを置き、声に合わせて口を動かす(#73)。

絵は「かわいいキャラのショート動画をAIで作る」で作った正面のぬめと、横顔のどん。
口の線を消して楕円の口を描き、開き具合を 0(閉じ)〜3(大) の4段階にする。
話し手ごとに声を並べ直し(overlay.place)、cut_static.py と同じ区間で切って、1/30秒ごとの音量で段階を決める。
口の絵の並びは concat の画像リストにし、ffmpeg の overlay で重ねる。映像は変換し直す(h264_videotoolbox)。

使い方: python3 lipsync.py <voice フォルダ> <カットした.mov> <出力.mov> <ffmpeg> <冒頭を切った秒数> [試しに書き出す秒数]
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import overlay  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 5))
ART = f"{ROOT}/2026/10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets/work"
FPS = 30
MARGIN = 20
# 話し手: (絵, 口の中心, 口の線を消す枠, 口の半幅, 動画での高さ, 置く隅)
CHARS = {
    "ぬめ": (f"{ART}/nume-front.png", (341, 611), (315, 600, 368, 622), 21, 520, "left"),
    "どん": (f"{ART}/don-left.png", (122, 359), (92, 351, 150, 366), 24, 480, "right"),
}
OPEN = [0, 6, 13, 20]  # 段階ごとの口の半分の高さ(元の絵の画素)


def mouth(path, center, erase, hw, level):
    im = Image.open(path).convert("RGBA")
    if level == 0:
        return im
    a = np.array(im)
    x0, y0, x1, y1 = erase
    skin = np.median(a[y0 - 12:y0 - 4, x0:x1, :3].reshape(-1, 3), axis=0).astype(int)
    d = ImageDraw.Draw(im)
    d.rectangle(erase, fill=tuple(skin) + (255,))
    cx, cy = center
    w, h = hw * (0.6 + 0.1 * level), OPEN[level]
    d.ellipse((cx - w, cy - h, cx + w, cy + h), fill=(150, 60, 60, 255), outline=(25, 25, 25, 255), width=5)
    return im


def segments(voice, trim):
    segs, a = [], None
    for line in open(f"{voice}/cut_list.txt"):
        if line.startswith("inpoint"):
            a = float(line.split()[1]) - trim
        elif line.startswith("outpoint"):
            segs.append((a, float(line.split()[1]) - trim))
    return segs


def levels(track, sr):
    n = sr // FPS
    frames = track[:len(track) // n * n].reshape(-1, n)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    voiced = rms[rms > 1e-3]
    ref = np.percentile(voiced, 95) if len(voiced) else 1
    r = rms / ref
    lv = np.digitize(r, [0.12, 0.35, 0.65])
    # 1コマだけの開閉はちらつくので、前後と合わせてならす
    return np.array([int(np.median(lv[max(i - 1, 0):i + 2])) for i in range(len(lv))])


def main():
    voice, video, out, ff, trim = sys.argv[1:6]
    trim = float(trim)
    limit = float(sys.argv[6]) if len(sys.argv) > 6 else None
    sr = overlay.SR
    clips, _ = overlay.place(voice, trim)
    segs = segments(voice, trim)
    total = max(p + len(x) / sr for p, x, _ in clips) + 1
    work = f"{voice}/lipsync"
    os.makedirs(work, exist_ok=True)
    W, H = 3248, 2122
    inputs, filters, last = [], [], "[0:v]"
    for k, (sp, (path, center, erase, hw, height, side)) in enumerate(CHARS.items()):
        track = np.zeros(int(total * sr))
        for p, x, who in clips:
            if who == sp:
                i = int(p * sr)
                track[i:i + len(x)] += x
        cut = np.concatenate([track[int(round(a * sr)):int(round(b * sr))] for a, b in segs])
        lv = levels(cut, sr)
        files = []
        for level in range(4):
            im = mouth(path, center, erase, hw, level)
            im = im.resize((int(im.width * height / im.height), height), Image.LANCZOS)
            f = f"{work}/{'nume' if sp == 'ぬめ' else 'don'}_{level}.png"
            im.save(f)
            files.append((f, im.width))
        lst = f"{work}/{'nume' if sp == 'ぬめ' else 'don'}.txt"
        with open(lst, "w") as f:
            i = 0
            while i < len(lv):
                j = i
                while j < len(lv) and lv[j] == lv[i]:
                    j += 1
                f.write(f"file '{os.path.abspath(files[lv[i]][0])}'\nduration {(j - i) / FPS:.6f}\n")
                i = j
            f.write(f"file '{os.path.abspath(files[0][0])}'\n")
        print(sp, "口を開けているコマ", int((lv > 0).sum()), "/", len(lv))
        inputs += ["-f", "concat", "-safe", "0", "-i", lst]
        x = MARGIN * 2 if side == "left" else W - files[0][1] - MARGIN
        y = H - height - MARGIN
        nxt = f"[v{k}]"
        filters.append(f"{last}[{k + 1}:v]overlay={x}:{y}:eof_action=repeat{nxt}")
        last = nxt
    cmd = [ff, "-hide_banner", "-loglevel", "error", "-y", "-i", video] + inputs + [
        "-filter_complex", ";".join(filters), "-map", last, "-map", "0:a",
        "-c:v", "h264_videotoolbox", "-b:v", "30M", "-video_track_timescale", "19200", "-c:a", "copy"]
    if limit:
        cmd += ["-t", str(limit)]
    subprocess.run(cmd + [out], check=True)
    print("done", out)


if __name__ == "__main__":
    main()
