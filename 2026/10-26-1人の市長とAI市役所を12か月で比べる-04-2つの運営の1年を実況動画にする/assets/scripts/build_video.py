"""1人の市長とAI市役所の録画と静止画に、ぬめとどんの声・字幕・口の動きを重ねて1本の動画にする(#106)。

#98 の build_video.py を流用した。変えたところ:
- 録画は月ごと・前後半ごとのファイル。場面の映像は、ファイルと秒で指す(spans.json から選んだ)
- 録画の上36画素は Mac の窓の枠なので、下の 1920x1170 を切り出す(映像の枠と同じ比)
- 2つの運営を左右に並べる場面(end2、fixed2)
- 1つの場面に、録画と静止画を混ぜて並べられる(長さは重みの比で分ける)
- 字幕は1行だけで出す(人の指示)。台本の台詞は30字までにしてある

組み方:
1. 台本の場面ごとに、台詞を間をあけて並べ、場面の長さを声の長さで決める
2. 場面の映像を作る。録画の区間は、場面の長さに合うよう倍速を直す。足りないときは区間を広げる
3. 映像をつなぎ、1920x1080 の画面の上に置く。下の帯に字幕、左下にぬめ、右下にどんを重ねる

場面の映像は作業フォルダ(~/ai-mayor-recordings/numedon2/)に置き、作り直さない。消すと作り直す。

使い方: ~/.venvs/tried-audio/bin/python build_video.py [場面の番号 ...]
  番号を渡すと、その場面だけの試し版(preview-<番号>.mp4)を作る
"""
import glob
import json
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DAY = os.path.abspath(f"{HERE}/../..")
Y2026 = os.path.abspath(f"{DAY}/..")
REC = os.path.expanduser("~/ai-mayor-recordings")
WORK = f"{REC}/numedon2"
VOICE = f"{WORK}/voice"
FF = "ffmpeg"

FPS = 30
SR = 24000
W, H = 1920, 1080
CW, CH = 1520, 926          # 映像を置く枠
CX, CY = 200, 14            # 枠の左上
BAND_Y = 954                # 字幕の帯の上端
BG = (30, 36, 48)
CROP = "crop=1920:1170:0:36"  # 録画の中のゲームの画面(上36画素は窓の枠)
GAP_LINE, GAP_TURN, GAP_PAUSE = 0.5, 0.8, 1.5  # overlay.py と同じ
HEAD, TAIL = 0.6, 0.8       # 場面の最初の台詞の前と、最後の台詞の後
FONT = "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
NAMES = {"base": "基準の市長", "council": "AI市役所"}
RUN = {"base": "10-25-1人の市長とAI市役所を12か月で比べる-02-基準の市長に12か月任せて録画する",
       "council": "10-25-1人の市長とAI市役所を12か月で比べる-03-AI市役所に12か月任せて録画する"}
B1, B2 = "base/2026-10-25 17-59-06.mp4", "base/2026-10-25 19-07-19.mp4"
C = {m: f"council/2026-10-26 {t}.mp4" for m, t in enumerate(
    ["13-32-37", "13-55-44", "14-14-35", "14-41-59", "14-59-59", "15-20-32", "15-43-21", "16-10-12", "16-26-34",
     "16-47-06", "17-06-51", "17-25-18"], start=1)}
PANEL = "crop=780:470:20:150"  # パネル(道具の記録の窓)を拡大する

ART = f"{Y2026}/10-08-かわいいキャラのショート動画をAIで作る-09-絵コンテの静止画を作る/assets/work"
# 話し手: (絵, 口の中心, 口の線を消す枠, 口の半幅, 動画での高さ, 置く隅)  lipsync.py と同じ絵と口の位置
CHARS = {
    "ぬめ": (f"{ART}/nume-front.png", (341, 611), (315, 600, 368, 622), 21, 290, "left"),
    "どん": (f"{ART}/don-left.png", (122, 359), (92, 351, 150, 366), 24, 250, "right"),
}
OPEN = [0, 6, 13, 20]
SUB_COLOR = {"ぬめ": (255, 210, 225), "どん": (255, 232, 180)}


def P(rel):
    return f"{Y2026}/{rel}"


def clip(run, file, a, b, speed, crop=None):
    """録画の区間。a, b は秒。run は名前を添えるため(base / council)。"""
    return {"kind": "clip", "run": run, "file": f"{REC}/{file}", "a": float(a), "b": float(b), "speed": speed,
            "crop": crop or CROP}


def still(*paths, sec=8.0):
    return {"kind": "still", "paths": [P(p) for p in paths], "sec": sec}


A105 = RUN["council"] + "/assets"
A100 = "10-24-AIは最高の市長になれるか-21-市役所と議会のハーネスを設計する/assets"
A98 = "10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets"
A93 = "10-23-AIは最高の市長になれるか-19-住みやす市長に10万人の福岡を任せる/assets"
A89 = "10-21-AIは最高の市長になれるか-14-4人を市長として定義する/assets"
A106 = "10-26-1人の市長とAI市役所を12か月で比べる-04-2つの運営の1年を実況動画にする/assets"

# 台本の場面ごとの映像。録画の秒は spans.json(施策を打った所)から選んだ
SCENES = {
    1: [{"kind": "end2"}],
    2: [still(f"{A93}/chart-4-final.png", f"{A100}/diagram-bureaus.png")],
    3: [still(f"{A89}/map-overview.jpg", f"{A105}/map-start-overview.jpg")],
    4: [still(f"{A105}/map-start-overview.jpg")],
    5: [still(f"{A105}/map-start-problems.jpg")],
    6: [still(f"{A106}/diagram-two.png")],
    7: [still(f"{A106}/diagram-two.png", f"{A100}/diagram-month.png", f"{A100}/diagram-month.png",
              f"{A100}/diagram-month.png")],
    8: [clip("base", B1, 251, 381, 4), clip("council", C[1], 20, 350, 24), clip("council", C[1], 345, 365, 1)],
    9: [clip("council", C[1], 120, 240, 4, PANEL)],
    10: [still(f"{A105}/chart-council-funnel.png", sec=30)],
    11: [still(f"{A105}/chart-council-month6.png", sec=24), clip("council", C[6], 826, 840, 1)],
    12: [still(f"{A105}/chart-council-months.png")],
    13: [clip("base", B1, 975, 992, 2), clip("base", B1, 1998, 2008, 1), clip("council", C[6], 826, 840, 1),
         clip("council", C[9], 715, 733, 2), clip("council", C[12], 584, 592, 1)],
    14: [clip("council", C[7], 684, 694, 1), clip("council", C[8], 552, 562, 1)],
    15: [clip("base", B1, 2468, 2484, 2), clip("base", B1, 2984, 3005, 2), clip("base", B2, 766, 788, 2),
         clip("base", B2, 1960, 1993, 4), clip("base", B2, 800, 806, 1), clip("base", B2, 1995, 2001, 1)],
    16: [clip("council", C[3], 492, 500, 1), clip("council", C[4], 530, 540, 1), clip("council", C[5], 630, 637, 1),
         clip("council", C[6], 780, 790, 1), clip("council", C[9], 675, 680, 1)],
    17: [{"kind": "fixed2"}],
    18: [still(f"{A105}/chart-final.png", f"{A105}/chart-monthly.png")],
    19: [still(f"{A105}/chart-final.png", sec=24), {"kind": "card", "text": "次回\n交通渋滞の解決と、観光の街を目指すAI市役所"}],
}


def sec(t):
    h, m, s = (int(x) for x in t.split(":"))
    return h * 3600 + m * 60 + s


def run(cmd):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y"] + cmd, check=True)


def rec_len(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout)


def load(path):
    x, sr = sf.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    assert sr == SR, path
    return x


# ---- 1. 台詞を並べる ----

STARTS = {}  # 場面ごとの、台詞の始め(場面の頭からの秒)

def place():
    """台詞を並べる。場面ごとの (始め, 長さ) と、(位置, 波形, 話し手, 字幕) の並びを返す。"""
    scenes = json.load(open(f"{VOICE}/lines.json"))
    t, spans, clips = 0.0, {}, []
    for sc in scenes:
        pos, prev = t + HEAD, None
        for ln in sc["lines"]:
            if prev is not None:
                pos += GAP_PAUSE if ln["pauseBefore"] else GAP_LINE if prev == ln["speaker"] else GAP_TURN
            x = load(f"{VOICE}/{ln['file']}")
            clips.append((pos, x, ln["speaker"], ln["text"]))
            pos += len(x) / SR
            prev = ln["speaker"]
        end = pos + TAIL
        spans[sc["no"]] = (t, end - t)
        STARTS[sc["no"]] = [p - t for p, *_ in clips[len(clips) - len(sc["lines"]):]]
        t = end
    return spans, clips


# ---- 2. 場面の映像 ----

def fit_box(im, w, h):
    im = im.convert("RGB")
    r = min(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    out = Image.new("RGB", (w, h), BG)
    out.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return out


def font(size):
    return ImageFont.truetype(FONT, size)


def label(im, text, xy, size=34):
    d = ImageDraw.Draw(im)
    d.text(xy, text, font=font(size), fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))


def frames_video(images, durations, out):
    """静止画の並びを、それぞれの秒数で動画にする。"""
    tmp = out + ".d"
    os.makedirs(tmp, exist_ok=True)
    lst = f"{tmp}/list.txt"
    with open(lst, "w") as f:
        for i, (im, d) in enumerate(zip(images, durations)):
            p = f"{tmp}/{i:03d}.png"
            im.save(p)
            f.write(f"file '{p}'\nduration {d:.4f}\n")
        f.write(f"file '{p}'\n")
    n = round(sum(durations) * FPS)
    run(["-f", "concat", "-safe", "0", "-i", lst, "-vf", f"fps={FPS},format=yuv420p", "-frames:v", str(n),
         "-c:v", "h264_videotoolbox", "-b:v", "12M", out])


def render_clip(c, dur, out):
    a, b = c["a"], c["b"]
    speed = c["speed"]
    rec_end = rec_len(c["file"])
    need = dur * speed  # この長さの録画が要る
    if need > b - a:    # 足りない分は区間を広げる(前に1/4、後ろに3/4)
        extra = need - (b - a)
        a = max(0, a - extra / 4)
        b = min(rec_end, a + need)
        a = max(0, b - need)
    else:               # 余るときは倍速を上げて区間全部を見せる
        speed = (b - a) / dur
    n = round(dur * FPS)
    run(["-hwaccel", "videotoolbox", "-ss", f"{a:.3f}", "-t", f"{b - a + 1:.3f}", "-i", c["file"], "-an",
         "-vf", f"{c['crop']},scale={CW}:{CH}:force_original_aspect_ratio=decrease,"
                f"pad={CW}:{CH}:(ow-iw)/2:(oh-ih)/2:color=0x{BG[0]:02x}{BG[1]:02x}{BG[2]:02x},"
                f"setpts=PTS/{speed:.4f},fps={FPS},format=yuv420p",
         "-frames:v", str(n), "-c:v", "h264_videotoolbox", "-b:v", "12M", out])
    return speed


def render_pair(inputs, dur, out, tag):
    """2本の映像を左右に並べ、運営の名前を添える。inputs は ffmpeg の入力の引数の並び。"""
    cw, ch = CW // 2, round(CW // 2 * 1170 / 1920)
    y = (CH - ch) // 2
    lab = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    for i, m in enumerate(NAMES):
        label(lab, NAMES[m], (i * cw + 16, y + 10), 32)
    lp = f"{WORK}/label-{tag}.png"
    lab.save(lp)
    f = "".join(f"[{i}:v]{CROP},scale={cw}:{ch},setsar=1[c{i}];" for i in range(2))
    f += (f"[c0][c1]hstack=inputs=2[g];[g]pad={CW}:{CH}:0:{y}:color=0x{BG[0]:02x}{BG[1]:02x}{BG[2]:02x}[p];"
          f"[p][2:v]overlay=0:0,fps=30,format=yuv420p")
    n = round(dur * FPS)
    run(inputs + ["-i", lp, "-filter_complex", f, "-frames:v", str(n), "-c:v", "h264_videotoolbox", "-b:v", "12M", out])


def card(text):
    im = Image.new("RGB", (CW, CH), BG)
    d = ImageDraw.Draw(im)
    lines = text.split("\n")
    sizes = [44] + [64] * (len(lines) - 1)
    y = CH // 2 - sum(s * 1.6 for s in sizes) / 2
    for s, t in zip(sizes, lines):
        w = d.textlength(t, font=font(s))
        d.text(((CW - w) / 2, y), t, font=font(s), fill=(255, 255, 255))
        y += s * 1.6
    return im


def weight(it):
    if it["kind"] == "clip":
        return (it["b"] - it["a"]) / it["speed"]
    if it["kind"] == "still":
        return it["sec"] * len(it["paths"])
    return 8.0


def render_scene(no, dur):
    items = SCENES[no]
    out = f"{WORK}/scene-{no:02d}.mp4"
    if os.path.exists(out):
        return out
    parts = []
    if items[0]["kind"] in ("end2", "fixed2"):
        p = f"{WORK}/scene-{no:02d}-0.mp4"
        if items[0]["kind"] == "end2":
            inputs = []
            for f in (f"{REC}/{B2}", f"{REC}/{C[12]}"):
                inputs += ["-hwaccel", "videotoolbox", "-ss", f"{rec_len(f) - dur - 2:.3f}", "-i", f]
            render_pair(inputs, dur, p, "end2")
        else:
            cw = CW // 2
            ims = []
            for k in range(1, 13):
                im = Image.new("RGB", (CW, CH), BG)
                for i, m in enumerate(NAMES):
                    ph = fit_box(Image.open(P(f"{RUN[m]}/assets/fixed/m{k:02d}-east.jpg")), cw, CH)
                    im.paste(ph, (i * cw, 0))
                    label(im, NAMES[m], (i * cw + 16, (CH - round(cw * 1170 / 1920)) // 2 + 10), 32)
                d = ImageDraw.Draw(im)
                t = f"{k}か月目"
                tw = d.textlength(t, font=font(44))
                d.rounded_rectangle(((CW - tw) / 2 - 24, 60, (CW + tw) / 2 + 24, 132), 16, fill=BG)
                d.text(((CW - tw) / 2, 68), t, font=font(44), fill=(255, 255, 255))
                ims.append(im)
            frames_video(ims, [dur / 12] * 12, p)
        parts.append(p)
    else:
        # 録画と静止画を並べる。長さは重みの比で分ける
        ws = [weight(it) for it in items]
        edges = np.round(np.cumsum([0] + ws) / sum(ws) * dur * FPS).astype(int)
        for i, it in enumerate(items):
            d = (edges[i + 1] - edges[i]) / FPS
            p = f"{WORK}/scene-{no:02d}-{i}.mp4"
            if it["kind"] == "clip":
                sp = render_clip(it, d, p)
                print(f"  場面{no} {NAMES[it['run']]} {os.path.basename(it['file'])} {it['a']:.0f}〜{it['b']:.0f} "
                      f"{d:.1f}秒 {sp:.1f}倍", flush=True)
            elif it["kind"] == "still":
                ims = [fit_box(Image.open(x), CW, CH) for x in it["paths"]]
                frames_video(ims, [d / len(ims)] * len(ims), p)
            elif it["kind"] == "card":
                frames_video([card(it["text"])], [d], p)
            parts.append(p)
    lst = f"{WORK}/scene-{no:02d}.txt"
    open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
    run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])
    return out


# ---- 3. 声・字幕・口 ----

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
    return np.array([int(np.median(lv[max(i - 1, 0):i + 2])) for i in range(len(lv))])


def runs_list(path, seq, files):
    """同じ絵が続く区間をまとめて、concat の画像リストにする。seq は1コマごとの絵の番号。"""
    with open(path, "w") as f:
        i = 0
        while i < len(seq):
            j = i
            while j < len(seq) and seq[j] == seq[i]:
                j += 1
            f.write(f"file '{files[seq[i]]}'\nduration {(j - i) / FPS:.6f}\n")
            i = j
        f.write(f"file '{files[seq[-1]]}'\n")


def wrap(text, fnt, width):
    lines, cur = [], ""
    for ch in text:
        if ImageDraw.Draw(Image.new("L", (1, 1))).textlength(cur + ch, font=fnt) > width:
            # 句読点で始まる行を作らない
            if ch in "、。!?」)…":
                cur += ch
                continue
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    return lines + [cur] if cur else lines


def subtitle_png(text, speaker, path):
    """字幕は1行だけ(人の指示)。入らないときは字を小さくする。"""
    im = Image.new("RGBA", (W, H - BAND_Y), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    size = 44
    while size > 30 and d.textlength(text, font=font(size)) > 1400:
        size -= 2
    f = font(size)
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, (H - BAND_Y - size) / 2 - 4), text, font=f, fill=SUB_COLOR[speaker], stroke_width=4,
           stroke_fill=(0, 0, 0))
    im.save(path)


def layers(clips, total, t0=0.0):
    """声(wav)、字幕と口の画像リストを作る。t0 から total 秒ぶん。"""
    n = int(total * SR)
    mix = np.zeros(n)
    tracks = {sp: np.zeros(n) for sp in CHARS}
    nf = round(total * FPS)
    subs = np.zeros(nf, dtype=int)  # 0 は字幕なし
    sub_files = [f"{WORK}/sub-blank.png"]
    Image.new("RGBA", (W, H - BAND_Y), (0, 0, 0, 0)).save(sub_files[0])
    k = 0
    for pos, x, sp, text in clips:
        p = pos - t0
        if p < 0 or p >= total:
            continue
        i = int(p * SR)
        seg = x[:max(0, n - i)]
        mix[i:i + len(seg)] += seg
        tracks[sp][i:i + len(seg)] += seg
        k += 1
        f = f"{WORK}/sub-{k:03d}.png"
        subtitle_png(text, sp, f)
        sub_files.append(f)
        subs[int(p * FPS):min(nf, int((p + len(x) / SR + 0.25) * FPS))] = len(sub_files) - 1
    mix = mix / (np.max(np.abs(mix)) or 1) * 0.9
    sf.write(f"{WORK}/voice.wav", mix, SR)
    runs_list(f"{WORK}/subs.txt", subs, sub_files)
    for sp, (path, center, erase, hw, height, side) in CHARS.items():
        tag = "nume" if sp == "ぬめ" else "don"
        files = []
        for level in range(4):
            im = mouth(path, center, erase, hw, level)
            im = im.resize((int(im.width * height / im.height), height), Image.LANCZOS)
            f = f"{WORK}/{tag}_{level}.png"
            im.save(f)
            files.append(f)
        lv = levels(tracks[sp])
        lv = np.concatenate([lv, np.zeros(max(0, nf - len(lv)), dtype=int)])[:nf]
        runs_list(f"{WORK}/{tag}.txt", lv, files)


def compose(video, total, out):
    nume_w = int(Image.open(f"{WORK}/nume_0.png").width)
    don_w = int(Image.open(f"{WORK}/don_0.png").width)
    nh, dh = CHARS["ぬめ"][4], CHARS["どん"][4]
    f = (f"[0:v]pad={W}:{H}:{CX}:{CY}:color=0x{BG[0]:02x}{BG[1]:02x}{BG[2]:02x}[bg];"
         f"[bg][2:v]overlay=0:{BAND_Y}:eof_action=repeat[s];"
         f"[s][3:v]overlay=8:{H - nh - 6}:eof_action=repeat[n];"
         f"[n][4:v]overlay={W - don_w - 8}:{H - dh - 10}:eof_action=repeat,format=yuv420p[v]")
    run(["-i", video, "-i", f"{WORK}/voice.wav",
         "-f", "concat", "-safe", "0", "-i", f"{WORK}/subs.txt",
         "-f", "concat", "-safe", "0", "-i", f"{WORK}/nume.txt",
         "-f", "concat", "-safe", "0", "-i", f"{WORK}/don.txt",
         "-filter_complex", f, "-map", "[v]", "-map", "1:a", "-t", f"{total:.3f}",
         "-c:v", "h264_videotoolbox", "-b:v", "16M", "-c:a", "aac", "-b:a", "192k", out])


def main():
    only = [int(a) for a in sys.argv[1:]]
    os.makedirs(WORK, exist_ok=True)
    spans, clips = place()
    nos = only or sorted(spans)
    json.dump({n: [round(a, 2), round(d, 2)] for n, (a, d) in spans.items()},
              open(f"{WORK}/spans.json", "w"), indent=1)
    parts = []
    for no in nos:
        print(f"場面{no} {spans[no][1]:.1f}秒", flush=True)
        parts.append(render_scene(no, spans[no][1]))
    lst = f"{WORK}/all.txt"
    open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
    video = f"{WORK}/content.mp4"
    run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video])
    # 試し版は、渡した場面の台詞だけを、その場面の頭からの時刻に並べ直す
    if only:
        shifted, t = [], 0.0
        for no in nos:
            a, d = spans[no]
            shifted += [(p - a + t, x, sp, tx) for p, x, sp, tx in clips if a <= p < a + d]
            t += d
        clips, total = shifted, t
        out = f"{WORK}/preview-{'-'.join(map(str, nos))}.mp4"
    else:
        total = sum(d for _, d in spans.values())
        out = f"{WORK}/numedon-2runs.mp4"
    layers(clips, total)
    compose(video, total, out)
    print("done", out, f"{total / 60:.1f}分")


if __name__ == "__main__":
    main()
