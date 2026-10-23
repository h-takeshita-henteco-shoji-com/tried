"""4人の市長の録画と静止画に、ぬめとどんの声・字幕・口の動きを重ねて1本の動画にする(#98)。

#73 の overlay.py(台詞を並べる間の取り方)と lipsync.py(口の絵の4段階)を流用した。
#73 は1本の録画に声を重ねたが、今回は4本の録画と静止画から場面ごとに映像を組む。

組み方:
1. 台本の場面ごとに、台詞を間をあけて並べ、場面の長さを声の長さで決める
2. 場面の映像を作る。録画の区間は、場面の長さに合うよう倍速を直す。足りないときは区間を広げる
3. 映像をつなぎ、1920x1080 の画面の上に置く。下の帯に字幕、左下にぬめ、右下にどんを重ねる

録画はゲームの窓の外に余白があるので、窓の中(1788x1088)だけを切り出す。
場面の映像は作業フォルダ(既定 ~/ai-mayor-recordings/numedon/)に置き、作り直さない。消すと作り直す。

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
VOICE = f"{DAY}/assets/voice"
REC = os.path.expanduser("~/ai-mayor-recordings")
WORK = f"{REC}/numedon"
FF = "ffmpeg"

FPS = 30
SR = 24000
W, H = 1920, 1080
CW, CH = 1520, 926          # 映像を置く枠
CX, CY = 200, 14            # 枠の左上
BAND_Y = 954                # 字幕の帯の上端
BG = (30, 36, 48)
CROP = "crop=1788:1088:66:78"  # 録画の中のゲームの窓
# 窓の大きさが違う区間。(市長, 動画の中の始め, 終わり, 切り出し)。区間ごとに4点を見て確かめた
CROP_EXCEPT = [("money", 4372.133, 7085.2, "crop=1838:1118:41:74")]
GAP_LINE, GAP_TURN, GAP_PAUSE = 0.5, 0.8, 1.5  # overlay.py と同じ
HEAD, TAIL = 0.6, 0.8       # 場面の最初の台詞の前と、最後の台詞の後
FONT = "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
MAYORS = ["base", "money", "population", "livable"]
NAMES = {"base": "基準の市長", "money": "お金市長", "population": "人口市長", "livable": "住みやす市長"}
FIXED = {"base": "16-基準", "money": "17-お金", "population": "18-人口", "livable": "19-住みやす"}

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


def clip(mayor, a, b, speed):
    return {"kind": "clip", "mayor": mayor, "a": a, "b": b, "speed": speed}


def still(*paths):
    return {"kind": "still", "paths": [P(p) for p in paths]}


# 台本の場面ごとの映像。時刻は <市長>-full.mp4 の中の位置(scenes.md)
SCENES = {
    1: [{"kind": "end4"}],
    2: [still("10-14-AIは最高の市長になれるか-02-福岡の再現範囲と公開条件を決める/assets/range-map-half.png",
              "10-14-AIは最高の市長になれるか-04-地形を読み込み海と川を整える/assets/terrain-imported.png")],
    # 場面3は台詞に合わせて切り替える。(何行目の台詞から, 映像)。行は0から数える
    3: [{"kind": "timed", "parts": [
        (0, {"kind": "grow", "slice": (0, 5)}),
        (1, still("10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets/diagram-mcp-1.png")),
        (4, still("10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets/diagram-mcp-2.png")),
        (8, still("10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets/diagram-mcp-3.png")),
        (9, {"kind": "grow", "slice": (5, 24)}),
        (12, still("10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets/diagram-subagent-1.png")),
        (15, still("10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets/diagram-subagent-2.png")),
        (18, {"kind": "grow", "slice": (24, 99)}),
    ]}],
    4: [still("10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets/map-areas.jpg",
              "10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets/map-areas.jpg",
              "10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets/map-areas.jpg",
              "10-21-AIは最高の市長になれるか-14-4人を市長として定義する/assets/tenjin.jpg")],
    5: [still("10-21-AIは最高の市長になれるか-14-4人を市長として定義する/assets/map-problems.jpg",
              "10-22-AIは最高の市長になれるか-17-お金市長に10万人の福岡を任せる/assets/chart-problem-chain.png",
              "10-22-AIは最高の市長になれるか-17-お金市長に10万人の福岡を任せる/assets/chart-problem-chain.png",
              "10-21-AIは最高の市長になれるか-14-4人を市長として定義する/assets/harbor.jpg")],
    6: [still("10-23-AIは最高の市長になれるか-20-4人の市長の1年を実況動画にする/assets/diagram-mayors.png")],
    7: [clip("base", "0:02:40", "0:03:25", 4), clip("money", "0:02:30", "0:02:55", 2),
        clip("population", "0:09:40", "0:12:55", 8), clip("livable", "0:03:40", "0:04:10", 2)],
    8: [clip("base", "0:43:20", "0:44:10", 4), clip("base", "0:53:40", "0:54:05", 2),
        clip("base", "1:02:20", "1:02:50", 2)],
    9: [clip("base", "1:22:20", "1:23:15", 4)],
    10: [clip("money", "0:21:55", "0:22:10", 2)],
    11: [clip("money", "1:34:05", "1:37:45", 16), clip("money", "1:49:30", "1:53:44", 16),
         clip("money", "1:58:56", "2:04:06", 16), clip("money", "2:13:42", "2:19:03", 16)],
    12: [clip("money", "1:54:05", "1:54:12", 1)],
    13: [clip("money", "2:22:16", "2:23:36", 4), clip("money", "2:24:30", "2:24:40", 1)],
    14: [clip("money", "2:31:54", "2:34:21", 8)],
    15: [clip("population", "1:22:19", "1:25:33", 12), clip("population", "2:02:54", "2:07:10", 16)],
    16: [clip("population", "1:07:10", "1:07:20", 1), clip("population", "1:46:03", "1:46:10", 1),
         clip("population", "2:02:48", "2:02:55", 1)],
    17: [clip("population", "3:48:21", "3:50:14", 12)],
    18: [clip("livable", "0:27:05", "0:28:30", 4), clip("livable", "0:38:04", "0:41:40", 12)],
    19: [clip("livable", "0:41:54", "0:42:00", 1), clip("livable", "0:52:37", "0:52:45", 1),
         clip("livable", "1:38:10", "1:38:45", 2), clip("livable", "2:01:05", "2:01:40", 2)],
    20: [clip("livable", "2:24:33", "2:24:40", 1)],
    21: [{"kind": "fixed4"}],
    22: [still("10-23-AIは最高の市長になれるか-19-住みやす市長に10万人の福岡を任せる/assets/chart-4-final.png",
               "10-23-AIは最高の市長になれるか-19-住みやす市長に10万人の福岡を任せる/assets/chart-4-population.png",
               "10-23-AIは最高の市長になれるか-19-住みやす市長に10万人の福岡を任せる/assets/chart-4-happiness.png")],
    23: [still("10-23-AIは最高の市長になれるか-19-住みやす市長に10万人の福岡を任せる/assets/chart-4-final.png"),
         {"kind": "card", "text": "次回\n4人を1つの市役所として働かせる"}],
}


def sec(t):
    h, m, s = (int(x) for x in t.split(":"))
    return h * 3600 + m * 60 + s


def run(cmd):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y"] + cmd, check=True)


def rec_len(mayor):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                        f"{REC}/{mayor}/{mayor}-full.mp4"], capture_output=True, text=True)
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


def crop_for(mayor, a, b):
    for m, x0, x1, crop in CROP_EXCEPT:
        if m == mayor and a < x1 and b > x0:
            assert x0 <= a and b <= x1, f"{mayor} {a}〜{b} が窓の大きさの変わり目をまたぐ"
            return crop
    return CROP


def render_clip(c, dur, out, rec_end):
    a, b = sec(c["a"]), sec(c["b"])
    speed = c["speed"]
    need = dur * speed  # この長さの録画が要る
    if need > b - a:    # 足りない分は区間を広げる(前に1/4、後ろに3/4)
        extra = need - (b - a)
        a = max(0, a - extra / 4)
        b = min(rec_end, a + need)
        a = max(0, b - need)
    else:               # 余るときは倍速を上げて区間全部を見せる
        speed = (b - a) / dur
    n = round(dur * FPS)
    run(["-hwaccel", "videotoolbox", "-ss", f"{a:.3f}", "-t", f"{b - a + 1:.3f}",
         "-i", f"{REC}/{c['mayor']}/{c['mayor']}-full.mp4", "-an",
         "-vf", f"{crop_for(c['mayor'], a, b)},scale={CW}:{CH},setpts=PTS/{speed:.4f},fps={FPS},format=yuv420p",
         "-frames:v", str(n), "-c:v", "h264_videotoolbox", "-b:v", "12M", out])
    return speed


def render_grid4(inputs, dur, out, tag):
    """4本の映像を2x2に並べ、市長の名前を添える。inputs は ffmpeg の入力の引数の並び。"""
    cw, ch = CW // 2, CH // 2
    lab = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    for i, m in enumerate(MAYORS):
        label(lab, NAMES[m], ((i % 2) * cw + 16, (i // 2) * ch + 10), 30)
    lp = f"{WORK}/label-{tag}.png"
    lab.save(lp)
    f = "".join(f"[{i}:v]{CROP},scale={cw}:{ch},setsar=1[c{i}];" for i in range(4))
    f += "[c0][c1][c2][c3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[g];[g][4:v]overlay=0:0,fps=30,format=yuv420p"
    n = round(dur * FPS)
    run(inputs + ["-i", lp, "-filter_complex", f, "-frames:v", str(n), "-c:v", "h264_videotoolbox", "-b:v", "12M", out])


def grow_images():
    gdir = P("10-20-AIは最高の市長になれるか-13-MODを直して基準の市長にもう一度任せる/grow")
    rows = {}
    for line in open(f"{gdir}/grow-note.md", encoding="utf-8"):
        m = re.match(r"^\| (\d{4})-(\d\d)-\d\d \| (g\d+) \| ([\d,]+) \|", line)
        if m:
            rows[m.group(3)] = (f"{m.group(1)}年{int(m.group(2))}月", m.group(4))
    ims = []
    for p in sorted(glob.glob(f"{gdir}/assets/g*-town.jpg")):
        g = re.match(r"(g\d+)", os.path.basename(p)).group(1)
        im = fit_box(Image.open(p), CW, CH)
        if g in rows:
            label(im, f"{rows[g][0]}  人口 {rows[g][1]}人", (24, 18), 40)
        ims.append(im)
    return ims


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


def render_scene(no, dur, rec_ends):
    items = SCENES[no]
    out = f"{WORK}/scene-{no:02d}.mp4"
    if os.path.exists(out):
        return out
    parts = []
    clips = [c for c in items if c["kind"] == "clip"]
    if clips:
        # 倍速を保ったときの長さの比で、場面の長さを分ける
        base = [(sec(c["b"]) - sec(c["a"])) / c["speed"] for c in clips]
        tot = sum(base)
        edges = np.round(np.cumsum([0] + base) / tot * dur * FPS).astype(int)
        for i, c in enumerate(clips):
            d = (edges[i + 1] - edges[i]) / FPS
            p = f"{WORK}/scene-{no:02d}-{i}.mp4"
            sp = render_clip(c, d, p, rec_ends[c["mayor"]])
            print(f"  場面{no} {NAMES[c['mayor']]} {c['a']}〜{c['b']} {d:.1f}秒 {sp:.1f}倍", flush=True)
            parts.append(p)
    else:
        kind = items[0]["kind"]
        p = f"{WORK}/scene-{no:02d}-0.mp4"
        if kind == "still" or kind == "card":
            ims = []
            for it in items:
                ims += [fit_box(Image.open(x), CW, CH) for x in it["paths"]] if it["kind"] == "still" else [card(it["text"])]
            frames_video(ims, [dur / len(ims)] * len(ims), p)
        elif kind == "grow":
            ims = grow_images()
            frames_video(ims, [dur / len(ims)] * len(ims), p)
        elif kind == "timed":
            # 切り替えは台詞の0.3秒前。静止画の並びとして1本にする
            tl = items[0]["parts"]
            edges = [0.0] + [max(0.0, STARTS[no][i] - 0.3) for i, _ in tl[1:]] + [dur]
            ims, durs = [], []
            for (_, it), a, b in zip(tl, edges, edges[1:]):
                if it["kind"] == "grow":
                    g = grow_images()[slice(*it["slice"])]
                    ims += g
                    durs += [(b - a) / len(g)] * len(g)
                else:
                    ims += [fit_box(Image.open(x), CW, CH) for x in it["paths"]]
                    durs += [(b - a) / len(it["paths"])] * len(it["paths"])
            frames_video(ims, durs, p)
        elif kind == "fixed4":
            cw, ch = CW // 2, CH // 2
            ims = []
            for k in range(1, 13):
                im = Image.new("RGB", (CW, CH), BG)
                for i, m in enumerate(MAYORS):
                    f = glob.glob(f"{Y2026}/*{FIXED[m]}*/assets/fixed/m{k:02d}-west.jpg")[0]
                    im.paste(fit_box(Image.open(f), cw, ch), ((i % 2) * cw, (i // 2) * ch))
                    label(im, NAMES[m], ((i % 2) * cw + 16, (i // 2) * ch + 10), 30)
                d = ImageDraw.Draw(im)
                t = f"{k}か月目"
                tw = d.textlength(t, font=font(44))
                # 市長の名前は各枠の左上にあるので、月は右上の角に置く
                d.rounded_rectangle((CW - tw - 56, 8, CW - 8, 80), 16, fill=BG)
                d.text((CW - tw - 32, 16), t, font=font(44), fill=(255, 255, 255))
                ims.append(im)
            frames_video(ims, [dur / 12] * 12, p)
        elif kind == "end4":
            inputs = []
            for m in MAYORS:
                inputs += ["-hwaccel", "videotoolbox", "-ss", f"{rec_ends[m] - dur - 2:.3f}",
                           "-i", f"{REC}/{m}/{m}-full.mp4"]
            render_grid4(inputs, dur, p, "end4")
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
    im = Image.new("RGBA", (W, H - BAND_Y), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    size = 40
    while True:
        f = font(size)
        lines = wrap(text, f, 1280)
        if len(lines) <= 2 or size <= 30:
            break
        size -= 2
    y = (H - BAND_Y - len(lines) * size * 1.25) / 2
    for t in lines:
        w = d.textlength(t, font=f)
        d.text(((W - w) / 2, y), t, font=f, fill=SUB_COLOR[speaker], stroke_width=4, stroke_fill=(0, 0, 0))
        y += size * 1.25
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
    rec_ends = {m: rec_len(m) for m in MAYORS}
    nos = only or sorted(spans)
    json.dump({n: [round(a, 2), round(d, 2)] for n, (a, d) in spans.items()},
              open(f"{WORK}/spans.json", "w"), indent=1)
    parts = []
    for no in nos:
        print(f"場面{no} {spans[no][1]:.1f}秒", flush=True)
        parts.append(render_scene(no, spans[no][1], rec_ends))
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
        out = f"{WORK}/numedon-4mayors.mp4"
    layers(clips, total)
    compose(video, total, out)
    print("done", out, f"{total / 60:.1f}分")


if __name__ == "__main__":
    main()
