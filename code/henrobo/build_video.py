"""へんロボの解説動画を組み立てる(#132 で作り、#138 でどの回にも使えるようにした)。図とカードに、へんロボの声・字幕・口パク・眼鏡のキラリを重ねる。

#106 の build_video.py（2026/10-26-...-04-.../assets/scripts/）を、へんロボ1人・静止画だけ用に直した。
- 映像は、記事の図（assets/）と、文字のカードだけ。録画は使わない
- へんロボは右下に1人だけ置く。口は声の大きさで4段階、台本の「(キラリ)」の行の後に眼鏡を光らせる
- 場面の長さは、声の長さで決める（台詞の間 0.5秒、「(間)」は 1.5秒）
- 字幕は1行で出す。台本の台詞は30字までにしてある
- 先頭に、サムネイルと同じタイトル画面（thumbnail.py）を音なしで TITLE_SEC 秒だけ置く

場面の図とカード、タイトル画面の文言は、その日のフォルダの henrobo_scenes.py に書く(SCENES と THUMB)。
作業フォルダ（~/henrobo-video/<Issue番号>/）に途中の映像を置く。動画はリポジトリに置かない（.gitignore）。

使い方: ~/.venvs/tried-audio/bin/python build_video.py <その日のフォルダ> [場面の番号 ...]
  番号を渡すと、その場面だけの試し版（preview-<番号>.mp4）を作る
"""
import json
import os
import re
import runpy
import subprocess
import sys

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import face  # noqa: E402
import thumbnail  # noqa: E402

# へんロボの立ち絵は #132 で作ったものを、どの回でも使う
CHAR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる/assets/charactor/henrobo-front.png"))
DAY = A = VOICE = WORK = ISSUE = None
SCENES, THUMB = {}, {}
FF = "ffmpeg"

FPS = 30
SR = 24000
W, H = 1920, 1080
CW, CH = 1500, 926          # 図を置く枠
CX, CY = 24, 14             # 枠の左上
BAND_Y = 954                # 字幕の帯の上端
BG = (30, 36, 48)
FONT = "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
MONO = "/System/Library/Fonts/Menlo.ttc"
SUB_COLOR = (255, 236, 200)
TITLE_SEC = 3.0
CHAR_H = 400                # へんロボの高さ
GAP_LINE, GAP_PAUSE = 0.5, 1.5
HEAD, TAIL = 0.6, 0.8
GLINT_DELAY, GLINT_SEC = 0.15, 0.6


def still(*names):
    return {"kind": "still", "paths": [n if n.startswith("/") else f"{A}/{n}" for n in names]}


def card(text, sub=""):
    return {"kind": "card", "text": text, "sub": sub}


def code(title, text):
    return {"kind": "code", "title": title, "text": text}


def configure(day):
    """その日のフォルダを読み込む。場面とタイトルは <day>/henrobo_scenes.py に書く。"""
    global DAY, A, VOICE, WORK, ISSUE, SCENES, THUMB
    DAY = os.path.abspath(day)
    A = f"{DAY}/assets"
    VOICE = f"{A}/voice"
    ISSUE = re.search(r"^issue: *(\d+)", open(f"{DAY}/log.md", encoding="utf-8").read(), re.M).group(1)
    WORK = os.path.expanduser(f"~/henrobo-video/{ISSUE}")
    ns = runpy.run_path(f"{DAY}/henrobo_scenes.py", init_globals={"A": A, "still": still, "card": card, "code": code})
    SCENES, THUMB = ns["SCENES"], ns["THUMB"]


def run(cmd):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y"] + cmd, check=True)


def load(path):
    x, sr = sf.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    assert sr == SR, path
    return x


# ---- 1. 台詞を並べる ----

def place():
    scenes = json.load(open(f"{VOICE}/lines.json"))
    t, spans, clips = 0.0, {}, []
    for sc in scenes:
        pos, first = t + HEAD, True
        for ln in sc["lines"]:
            if not first:
                pos += GAP_PAUSE if ln["pauseBefore"] else GAP_LINE
            first = False
            x = load(f"{VOICE}/{ln['file']}")
            clips.append((pos, x, ln["text"], ln.get("glint", False)))
            pos += len(x) / SR
        end = pos + TAIL
        spans[sc["no"]] = (t, end - t)
        t = end
    return spans, clips


# ---- 2. 場面の映像 ----

def font(size, mono=False):
    return ImageFont.truetype(MONO if mono else FONT, size)


def fit_box(im, w, h):
    im = im.convert("RGBA")
    r = min(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    out = Image.new("RGB", (w, h), BG)
    # 透明な部分や白地の図は、白い台紙に載せて見やすくする
    pad = 12
    out.paste((250, 250, 248), ((w - im.width) // 2 - pad, (h - im.height) // 2 - pad,
                                (w + im.width) // 2 + pad, (h + im.height) // 2 + pad))
    out.paste(im, ((w - im.width) // 2, (h - im.height) // 2), im)
    return out


def card_image(text, sub=""):
    im = Image.new("RGB", (CW, CH), BG)
    d = ImageDraw.Draw(im)
    lines = text.split("\n")
    size = 64 if len(lines) <= 2 else 54
    while max(d.textlength(t, font=font(size)) for t in lines) > CW - 120 and size > 28:
        size -= 2
    y = CH / 2 - len(lines) * size * 1.7 / 2
    if sub:
        sw = d.textlength(sub, font=font(36))
        d.text(((CW - sw) / 2, y - 90), sub, font=font(36), fill=(255, 200, 120))
    for t in lines:
        w = d.textlength(t, font=font(size))
        d.text(((CW - w) / 2, y), t, font=font(size), fill=(255, 255, 255))
        y += size * 1.7
    return im


def code_image(title, text):
    """コードや、AIの答えの抜き出しを、暗い枠の中に等幅で出す。"""
    im = Image.new("RGB", (CW, CH), BG)
    d = ImageDraw.Draw(im)
    d.text((60, 60), title, font=font(40), fill=(255, 200, 120))
    d.rounded_rectangle((40, 140, CW - 40, CH - 60), 20, fill=(16, 20, 28))
    d.multiline_text((80, 190), text, font=font(26, mono=True), fill=(220, 230, 240), spacing=18)
    return im


def hero_image():
    """名前と決まり文句のカード。へんロボは右下に常にいるので、ここには大きく描かない（2人に見えるため）。"""
    im = Image.new("RGB", (CW, CH), BG)
    d = ImageDraw.Draw(im)
    for t, s, y, c in (("へんロボ", 120, CH / 2 - 140, (255, 200, 120)),
                       ("中小企業のAI導入の現場から、", 48, CH / 2 + 30, (255, 255, 255)),
                       ("試したことを、そのままお伝えします。", 48, CH / 2 + 110, (255, 255, 255))):
        w = d.textlength(t, font=font(s))
        d.text(((CW - w) / 2, y), t, font=font(s), fill=c)
    return im


def frames_video(images, durations, out):
    tmp = out + ".d"
    os.makedirs(tmp, exist_ok=True)
    lst = f"{tmp}/list.txt"
    with open(lst, "w") as f:
        for i, (im, dd) in enumerate(zip(images, durations)):
            p = f"{tmp}/{i:03d}.png"
            im.save(p)
            f.write(f"file '{p}'\nduration {dd:.4f}\n")
        f.write(f"file '{p}'\n")
    n = round(sum(durations) * FPS)
    run(["-f", "concat", "-safe", "0", "-i", lst, "-vf", f"fps={FPS},format=yuv420p", "-frames:v", str(n),
         "-c:v", "h264_videotoolbox", "-b:v", "12M", out])


def item_images(it):
    if it["kind"] == "still":
        return [fit_box(Image.open(p), CW, CH) for p in it["paths"]]
    if it["kind"] == "card":
        return [card_image(it["text"], it["sub"])]
    if it["kind"] == "code":
        return [code_image(it["title"], it["text"])]
    return [hero_image()]


def render_scene(no, dur):
    out = f"{WORK}/scene-{no:02d}.mp4"
    ims = [im for it in SCENES[no] for im in item_images(it)]
    frames_video(ims, [dur / len(ims)] * len(ims), out)
    return out


# ---- 3. 声・字幕・口・キラリ ----

def levels(track):
    n = SR // FPS
    frames = track[:len(track) // n * n].reshape(-1, n)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    voiced = rms[rms > 1e-3]
    ref = np.percentile(voiced, 95) if len(voiced) else 1
    lv = np.digitize(rms / ref, [0.12, 0.35, 0.65])
    return np.array([int(np.median(lv[max(i - 1, 0):i + 2])) for i in range(len(lv))])


def runs_list(path, seq, files):
    with open(path, "w") as f:
        i = 0
        while i < len(seq):
            j = i
            while j < len(seq) and seq[j] == seq[i]:
                j += 1
            f.write(f"file '{files[seq[i]]}'\nduration {(j - i) / FPS:.6f}\n")
            i = j
        f.write(f"file '{files[seq[-1]]}'\n")


def subtitle_png(text, path):
    im = Image.new("RGBA", (W, H - BAND_Y), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    size = 44
    while size > 30 and d.textlength(text, font=font(size)) > 1400:
        size -= 2
    f = font(size)
    w = d.textlength(text, font=f)
    d.text(((W - CHAR_W - w) / 2 + 20, (H - BAND_Y - size) / 2 - 4), text, font=f, fill=SUB_COLOR,
           stroke_width=4, stroke_fill=(0, 0, 0))
    im.save(path)


CHAR_W = 0


def layers(clips, total):
    global CHAR_W
    ch = Image.open(CHAR)
    CHAR_W = round(ch.width * CHAR_H / ch.height)  # 字幕を、へんロボと重ならない位置に置くため
    n = int(total * SR)
    mix = np.zeros(n)
    nf = round(total * FPS)
    subs = np.zeros(nf, dtype=int)
    sub_files = [f"{WORK}/sub-blank.png"]
    Image.new("RGBA", (W, H - BAND_Y), (0, 0, 0, 0)).save(sub_files[0])
    glint_at = []
    for k, (p, x, text, glint) in enumerate(clips, 1):
        if p < 0 or p >= total:
            continue
        i = int(p * SR)
        seg = x[:max(0, n - i)]
        mix[i:i + len(seg)] += seg
        f = f"{WORK}/sub-{k:03d}.png"
        subtitle_png(text, f)
        sub_files.append(f)
        end = p + len(x) / SR
        subs[int(p * FPS):min(nf, int((end + 0.25) * FPS))] = len(sub_files) - 1
        if glint:
            glint_at.append(end + GLINT_DELAY)
    mix = mix / (np.max(np.abs(mix)) or 1) * 0.9
    sf.write(f"{WORK}/voice.wav", mix, SR)
    runs_list(f"{WORK}/subs.txt", subs, sub_files)
    # へんロボの絵: 0〜3 は口の段階、4 から先はキラリの途中（口は閉じたまま）
    base = Image.open(CHAR).convert("RGBA")
    ng = round(GLINT_SEC * FPS)
    images = [face.mouth(base, lv) for lv in range(4)]
    images += [face.glint(base, (g + 1) / (ng + 1)) for g in range(ng)]
    files = []
    for i, im in enumerate(images):
        im = im.resize((round(im.width * CHAR_H / im.height), CHAR_H), Image.LANCZOS)
        f = f"{WORK}/henrobo_{i:02d}.png"
        im.save(f)
        files.append(f)
    lv = levels(mix)
    seq = np.concatenate([lv, np.zeros(max(0, nf - len(lv)), dtype=int)])[:nf]
    for t in glint_at:
        s = int(t * FPS)
        for g in range(ng):
            if s + g < nf and seq[s + g] == 0:
                seq[s + g] = 4 + g
    runs_list(f"{WORK}/henrobo.txt", seq, files)


def compose(video, total, out):
    f = (f"[0:v]pad={W}:{H}:{CX}:{CY}:color=0x{BG[0]:02x}{BG[1]:02x}{BG[2]:02x}[bg];"
         f"[bg][2:v]overlay=0:{BAND_Y}:eof_action=repeat[s];"
         f"[s][3:v]overlay={W - CHAR_W - 30}:{H - CHAR_H - 20}:eof_action=repeat,format=yuv420p[v]")
    run(["-i", video, "-i", f"{WORK}/voice.wav",
         "-f", "concat", "-safe", "0", "-i", f"{WORK}/subs.txt",
         "-f", "concat", "-safe", "0", "-i", f"{WORK}/henrobo.txt",
         "-filter_complex", f, "-map", "[v]", "-map", "1:a", "-t", f"{total:.3f}",
         "-c:v", "h264_videotoolbox", "-b:v", "16M", "-c:a", "aac", "-b:a", "192k", out])


def write_srt(clips, offset, out):
    """YouTube に登録する字幕ファイル(SRT)を書く。時刻は、先頭のタイトル画面の分(offset)だけずらす。"""
    def ts(t):
        ms = round(t * 1000)
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(out, "w", encoding="utf-8") as f:
        for i, (p, x, text, _) in enumerate(clips, 1):
            a = p + offset
            f.write(f"{i}\n{ts(a)} --> {ts(a + len(x) / SR + 0.25)}\n{text}\n\n")


def add_title(body, out):
    png = f"{WORK}/title.png"
    thumbnail.title_image(THUMB, W, H).save(png)
    run(["-loop", "1", "-t", f"{TITLE_SEC}", "-framerate", str(FPS), "-i", png,
         "-f", "lavfi", "-t", f"{TITLE_SEC}", "-i", f"anullsrc=r={SR}:cl=mono", "-i", body,
         "-filter_complex", "[0:v]format=yuv420p[t];[2:a]aformat=channel_layouts=mono[b];"
         "[t][1:a][2:v][b]concat=n=2:v=1:a=1[v][a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "h264_videotoolbox", "-b:v", "16M",
         "-c:a", "aac", "-b:a", "192k", out])


def main():
    configure(sys.argv[1])
    only = [int(a) for a in sys.argv[2:]]
    os.makedirs(WORK, exist_ok=True)
    spans, clips = place()
    nos = only or sorted(spans)
    parts = []
    for no in nos:
        print(f"場面{no} {spans[no][1]:.1f}秒", flush=True)
        parts.append(render_scene(no, spans[no][1]))
    lst = f"{WORK}/all.txt"
    open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
    video = f"{WORK}/content.mp4"
    run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video])
    if only:
        shifted, t = [], 0.0
        for no in nos:
            a, d = spans[no]
            shifted += [(p - a + t, x, tx, g) for p, x, tx, g in clips if a <= p < a + d]
            t += d
        clips, total = shifted, t
        out = f"{WORK}/preview-{'-'.join(map(str, nos))}.mp4"
    else:
        total = sum(d for _, d in spans.values())
        out = f"{WORK}/henrobo-{ISSUE}.mp4"
    layers(clips, total)
    if only:
        compose(video, total, out)
    else:
        body = f"{WORK}/body.mp4"
        compose(video, total, body)
        add_title(body, out)
        write_srt(clips, TITLE_SEC, f"{WORK}/henrobo-{ISSUE}.srt")
        total += TITLE_SEC
    print("done", out, f"{total / 60:.1f}分")


if __name__ == "__main__":
    main()
