"""ぬめとどんの声をカット版の動画に並べ、二人の絵を重ねて口を動かす(#81)。

#73 の overlay.py と lipsync.py を1つにまとめた。違いは次のとおり。
- 置く時刻は、台本(numedon-script.md)の見出しと「画面(分:秒)」に書いたカット版の時刻を使う
- 冒頭は場面1の声の長さだけ、最初の画面を止めて延ばす。カット版の最初の2分は施策が詰まっていて、そのままだと場面1〜3が重なる
- 前の場面の声が終わっていなければ、終わってから GAP_SCENE 秒あけて置く
- 絵は下の操作バー(日付・所持金・人口)を隠さないよう、バーの上に置く

使い方: ~/.venvs/tried-audio/bin/python overlay.py <台本.md> <voice フォルダ> <カット版.mp4> <出力.mp4> [試しに書き出す秒数]
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 4))
ART = f"{ROOT}/2026/10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets/work"
SR = 24000
FPS = 30
W, H = 1920, 1198
BAR = 80              # 下の操作バーの高さ(画素)。絵はこの上に置く
MARGIN = 12
GAP_LINE = 0.5        # 同じ話し手が続くとき
GAP_TURN = 0.8        # 話し手が替わるとき
GAP_SCENE = 1.0
# 話し手: (絵, 口の中心, 口の線を消す枠, 口の半幅, 動画での高さ, 置く隅)。数字は #73 の lipsync.py と同じ
CHARS = {
    "ぬめ": (f"{ART}/nume-front.png", (341, 611), (315, 600, 368, 622), 21, 300, "left"),
    "どん": (f"{ART}/don-left.png", (122, 359), (92, 351, 150, 366), 24, 280, "right"),
}
OPEN = [0, 6, 13, 20]  # 段階ごとの口の半分の高さ(元の絵の画素)


def secs(mmss):
    m, s = mmss.split(":")
    return int(m) * 60 + int(s)


def anchors(script):
    """台詞ごとに、置きたいカット版の時刻を返す。場面の見出しの時刻か、途中の「画面(分:秒)」の時刻"""
    out, want = [], None
    for line in open(script, encoding="utf-8"):
        m = re.match(r"^## \d+\. .+\((\d+:\d+)〜", line)
        if m:
            want = secs(m.group(1))
            continue
        m = re.match(r"^画面\((\d+:\d+)\)", line)
        if m:
            want = secs(m.group(1))
            continue
        if re.match(r"^> (ぬめ|どん): ", line):
            out.append(want)
            want = None
    return out


def load(path):
    x, sr = sf.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    if sr != SR:
        idx = np.arange(0, len(x), sr / SR)
        x = np.interp(idx, np.arange(len(x)), x)
    return x


def place(script, voice):
    """(位置の秒, 波形, 話し手) の並び、場面ごとの予定、冒頭に足す秒数を返す"""
    scenes = json.load(open(f"{voice}/lines.json"))
    wants = anchors(script)
    lines = [(sc, ln) for sc in scenes for ln in sc["lines"]]
    assert len(wants) == len(lines), (len(wants), len(lines))
    waves = [load(f"{voice}/{ln['file']}") for _, ln in lines]
    first = [i for i, (sc, _) in enumerate(lines) if sc["no"] == 1]
    lead = sum(len(waves[i]) / SR for i in first) + GAP_TURN * (len(first) - 1) + GAP_SCENE
    clips, plan, pos, prev = [], [], 0.0, None
    for (sc, ln), want, x in zip(lines, wants, waves):
        if want is not None:
            want = want + lead if sc["no"] > 1 else 0.0
            at = max(want, pos + (GAP_SCENE if prev else 0))
            plan.append({"scene": sc["no"], "title": sc["title"], "want": round(want, 1), "start": round(at, 1)})
            pos = at
        elif prev is not None:
            pos += GAP_LINE if prev == ln["speaker"] else GAP_TURN
        clips.append((pos, x, ln["speaker"]))
        pos += len(x) / SR
        prev = ln["speaker"]
        plan[-1]["end"] = round(pos, 1)
    return clips, plan, lead


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


def levels(track):
    n = SR // FPS
    frames = track[:len(track) // n * n].reshape(-1, n)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    voiced = rms[rms > 1e-3]
    ref = np.percentile(voiced, 95) if len(voiced) else 1
    lv = np.digitize(rms / ref, [0.12, 0.35, 0.65])
    # 1コマだけの開閉はちらつくので、前後と合わせてならす
    return np.array([int(np.median(lv[max(i - 1, 0):i + 2])) for i in range(len(lv))])


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def main():
    script, voice, video, out = sys.argv[1:5]
    limit = float(sys.argv[5]) if len(sys.argv) > 5 else None
    clips, plan, lead = place(script, voice)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True).stdout) + lead
    total = max(dur, max(p + len(x) / SR for p, x, _ in clips) + 1)

    mix = np.zeros(int(total * SR))
    for p, x, _ in clips:
        i = int(p * SR)
        mix[i:i + len(x)] += x
    mix = mix / (np.max(np.abs(mix)) or 1) * 0.9
    work = f"{voice}/overlay"
    os.makedirs(work, exist_ok=True)
    wav = f"{work}/voice.wav"
    sf.write(wav, mix, SR)
    json.dump(plan, open(f"{voice}/plan.json", "w"), ensure_ascii=False, indent=1)
    for p in plan:
        late = p["start"] - p["want"]
        print(f"場面{p['scene']:2d} {p['title']}: {mmss(p['start'])} - {mmss(p['end'])}" + (f"(予定より {late:.0f}秒あと)" if late > 0.5 else ""))

    inputs, filters = [], [f"[0:v]tpad=start_duration={lead:.3f}:start_mode=clone,fps={FPS}[base]"]
    last = "[base]"
    for k, (sp, (path, center, erase, hw, height, side)) in enumerate(CHARS.items()):
        track = np.zeros(int(total * SR))
        for p, x, who in clips:
            if who == sp:
                i = int(p * SR)
                track[i:i + len(x)] += x
        lv = levels(track)
        name = "nume" if sp == "ぬめ" else "don"
        files = []
        for level in range(4):
            im = mouth(path, center, erase, hw, level)
            im = im.resize((int(im.width * height / im.height), height), Image.LANCZOS)
            f = f"{work}/{name}_{level}.png"
            im.save(f)
            files.append((f, im.width))
        lst = f"{work}/{name}.txt"
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
        x = MARGIN if side == "left" else W - files[0][1] - MARGIN
        y = H - BAR - height
        nxt = f"[v{k}]"
        filters.append(f"{last}[{k + 1}:v]overlay={x}:{y}:eof_action=repeat{nxt}")
        last = nxt
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", video] + inputs + ["-i", wav,
           "-filter_complex", ";".join(filters), "-map", last, "-map", f"{len(CHARS) + 1}:a",
           "-c:v", "h264_videotoolbox", "-b:v", "8M", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]
    cmd += ["-t", str(limit)] if limit else ["-t", f"{total:.2f}"]
    subprocess.run(cmd + [out], check=True)
    print("done", out, f"冒頭に {lead:.1f}秒 足した")


if __name__ == "__main__":
    main()
