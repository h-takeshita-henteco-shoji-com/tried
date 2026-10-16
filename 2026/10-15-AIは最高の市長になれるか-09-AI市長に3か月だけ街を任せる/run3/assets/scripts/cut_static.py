"""声の入った、短い動画を作る。台詞のない所と、AI市長が状況を確かめているだけの所を切る(#73)。

残すのは、台詞の区間(voice/plan.json)と、AI市長が手を動かした前後だけ。
手を動かした時刻は Mod のログ(command-log.txt)から取る。
- 手を動かす道具: 道を引く、区画を塗る、建物を置く、予算・税・政策を変える、時間を進める など(ACTION)
- パネルの DO と WHY の行も残す。手を動かす直前に、何をなぜするかが出るため
- 画面写真、カメラの移動、街の情報などの確かめる道具は残さない
残す区間の両端を区切りのコマ(キーフレーム)に合わせ、映像は元の録画から変換せずにつなぐ。
音は overlay.wav を同じ区間で切ってつなぎ直す。映像と音を一緒につなぐと、つなぎ目で音が削られたため。

先に overlay.py を、同じ冒頭を切る秒数で実行し、overlay.wav と plan.json を作っておく。
使い方: python3 cut_static.py <voice フォルダ> <command-log.txt> <元の録画.mov> <出力.mov> <ffmpeg> <冒頭を切った秒数>
"""
import datetime
import json
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

START = datetime.datetime(2026, 10, 16, 18, 23, 6)  # 録画の開始(overlay.py と同じ)
ACTION = {"build_line", "remove_line", "zone_area", "place_building", "bulldoze", "advance",
          "set_budget", "set_tax", "set_policy", "plant_forest"}
PRE, POST = 1.0, 3.0  # 手を動かした前後に残す秒数
PAD = 1.0             # 台詞の前後に残す秒数
MINGAP = 3.0          # これより短い切れ目は切らない


def keyframes(ff, video):
    r = subprocess.run([ff, "-hide_banner", "-skip_frame", "nokey", "-i", video, "-an", "-vf", "showinfo", "-f", "null", "-"],
                       capture_output=True, text=True)
    return np.array(sorted(float(s.split(":")[1]) for s in r.stderr.split() if s.startswith("pts_time:")))


def main():
    voice, log, video, out, ff, trim = sys.argv[1:7]
    trim = float(trim)
    x, sr = sf.read(f"{voice}/overlay.wav")
    total = len(x) / sr
    # 時刻はすべて、冒頭を切った後の動画の秒
    keep = [(p["start"] - PAD, p["end"] + PAD) for p in json.load(open(f"{voice}/plan.json"))]
    for line in open(log, encoding="utf-8-sig"):
        c = line.rstrip("\n").split("\t")
        if len(c) < 4 or not c[0][:4].isdigit():
            continue
        t = (datetime.datetime.fromisoformat(c[0]) - START).total_seconds() - trim
        m = re.search(r"-> ([\d.]+)s", c[3])
        if c[2] in ("DO", "WHY"):
            keep.append((t - PRE, t + POST))
        elif c[3].split(" ")[0] in ACTION:
            keep.append((t - PRE, t + 1 + (float(m.group(1)) if m else 0) + POST))
    merged = []
    for a, b in sorted(keep):
        a, b = max(a, 0), min(b, total)
        if merged and a - merged[-1][1] < MINGAP:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    keys = keyframes(ff, video) - trim
    segs = []
    for a, b in merged:
        ka = float(keys[keys <= a + 1e-6].max())
        nb = keys[keys >= b - 1e-6]
        kb = float(nb.min()) if len(nb) else total
        if segs and ka <= segs[-1][1] + 1e-6:
            segs[-1][1] = max(segs[-1][1], kb)
        else:
            segs.append([ka, kb])
    print(len(segs), "区間", f"{sum(b - a for a, b in segs) / 60:.1f}分")
    lst, wav, vonly = f"{voice}/cut_list.txt", f"{voice}/cut.wav", f"{voice}/cut_video_only.mov"
    with open(lst, "w") as f:
        for a, b in segs:
            f.write(f"file '{os.path.abspath(video)}'\ninpoint {a + trim:.6f}\noutpoint {b + trim:.6f}\n")
    parts = []
    for a, b in segs:
        i, j = int(round(a * sr)), int(round(b * sr))
        parts.append(np.pad(x[i:j], (0, j - i - len(x[i:j]))))
    sf.write(wav, np.concatenate(parts), sr)
    subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-an", "-c", "copy", vonly], check=True)
    subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", "-i", vonly, "-i", wav,
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out], check=True)
    os.remove(vonly)
    print("done", out)


if __name__ == "__main__":
    main()
