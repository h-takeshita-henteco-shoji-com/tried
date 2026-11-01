"""#132 の動画を組み立てる。図とカードに、へんロボの声・字幕・口パク・眼鏡のキラリを重ねる。

#106 の build_video.py（2026/10-26-...-04-.../assets/scripts/）を、へんロボ1人・静止画だけ用に直した。
- 映像は、記事の図（assets/）と、文字のカードだけ。録画は使わない
- へんロボは右下に1人だけ置く。口は声の大きさで4段階、台本の「(キラリ)」の行の後に眼鏡を光らせる
- 場面の長さは、声の長さで決める（台詞の間 0.5秒、「(間)」は 1.5秒）
- 字幕は1行で出す。台本の台詞は30字までにしてある

作業フォルダ（~/henrobo-video/132/）に途中の映像を置く。動画はリポジトリに置かない（.gitignore）。

使い方: ~/.venvs/tried-audio/bin/python build_video.py [場面の番号 ...]
  番号を渡すと、その場面だけの試し版（preview-<番号>.mp4）を作る
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import face  # noqa: E402

DAY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる"))
A = f"{DAY}/assets"
VOICE = f"{A}/voice"
WORK = os.path.expanduser("~/henrobo-video/132")
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
CHAR_H = 400                # へんロボの高さ
GAP_LINE, GAP_PAUSE = 0.5, 1.5
HEAD, TAIL = 0.6, 0.8
GLINT_DELAY, GLINT_SEC = 0.15, 0.6
DRAW = f"{A}/drawings/建築工事標準詳細図"

CODE = """for p in polys:
    pts=[q for q in p['p'] if q[1] is not None]
    if not all(x0<=a<=x1 and y0<=b<=y1 for a,b in pts):continue
    d=' '.join('%.2f,%.2f'%(a,-b) for a,b in pts)
    s.append('<polyline points="%s" fill="none" stroke="black" stroke-width="0.12"/>'%d)
s.append('</svg>')
open('/tmp/o/a.svg','w').write('\\n'.join(s))"""


def still(*names):
    return {"kind": "still", "paths": [n if n.startswith("/") else f"{A}/{n}" for n in names]}


def card(text, sub=""):
    return {"kind": "card", "text": text, "sub": sub}


TOC = ("1つ目　どうやってAIに図面を読ませたのか\n"
       "2つ目　AIはどう答えたのか\n"
       "3つ目　図面の仕事にとって、何を意味するのか")
SCENES = {
    1: [still(f"{DRAW}/001126048-p09.png"), still("crop-open-door.png")],
    2: [{"kind": "hero"}, card("AIに建築の図面を読ませて、\n3社10のモデルで比べた", "#132 AIと図面のコラボレーション")],
    3: [card(TOC, "今日のお話")],
    4: [card("1つ目\nどうやってAIに図面を読ませたのか"), still(f"{DRAW}/001126048-p09.png"),
        still(f"{DRAW}/001126051-p15.png")],
    5: [card("会議室の入口に、ガラスのない両開きの扉を付けたい。\nどの形状番号を選べばよいか\n\n"
             "すべり出し窓の上に、FIXのらんまを付けたい。\nこの図の形状で表せるか", "問いの例"),
        card("2枚の図面 × 14問\nDXF（CADのデータ）と画像\n10のAI × 1問ずつ = 560回", "比べ方")],
    6: [card("2つ目\nAIはどう答えたのか"), still("score-chart.png"), still("question-chart.png")],
    7: [still("table-L-2-1.png"), still("dxf-vs-image.png"), still("dxf-miss-map.png")],
    8: [{"kind": "code"}, still("door-symbols.png")],
    9: [still("table-L-3-2.png"), still("crop-c2-c8.png"), still("table-L-5-3.png")],
    10: [still("crop-open-door.png"), still("table-H-5-3.png")],
    11: [card("3つ目\n図面の仕事にとって、何を意味するのか"),
         card("試したのは、2枚の図面と28問だけ\n採点にもAIを使った", "注意点")],
    12: [{"kind": "hero"}, card("文字で書いてあることは、どのAIも読める\n記号や形は、DXFで差がつく\n"
                                "答えがない問いで、言い切るAIと止まるAIが出る", "へんロボの見立て")],
    13: [card("どうやってAIに図面を読ませたのか → 実務の問いを、10のAIに解かせた\n"
              "AIはどう答えたのか → 文字は読めても、記号と答えがない問いで差\n"
              "何を意味するのか → 任せられる範囲は、何を聞くかで決まる", "まとめ"),
         card("次回\n図面の寸法を読む力を試す")],
}


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
    size = 64 if len(lines) <= 2 else 46
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


def code_image():
    im = Image.new("RGB", (CW, CH), BG)
    d = ImageDraw.Draw(im)
    d.text((60, 60), "AIが書いたプログラムの一部（DXFの線を、絵に描き直す）", font=font(40), fill=(255, 200, 120))
    d.rounded_rectangle((40, 140, CW - 40, CH - 60), 20, fill=(16, 20, 28))
    d.multiline_text((80, 190), CODE, font=font(26, mono=True), fill=(220, 230, 240), spacing=18)
    return im


def hero_image():
    im = Image.new("RGB", (CW, CH), BG)
    ch = Image.open(f"{A}/charactor/henrobo-front.png").convert("RGBA")
    h = CH - 120
    ch = ch.resize((round(ch.width * h / ch.height), h), Image.LANCZOS)
    im.paste(ch, ((CW - ch.width) // 2, 60), ch)
    d = ImageDraw.Draw(im)
    for i, t in enumerate(("へんロボ", "中小企業のAI導入の現場から")):
        s = 56 if i == 0 else 34
        w = d.textlength(t, font=font(s))
        d.text((CW - w - 60, 80 + i * 80), t, font=font(s), fill=(255, 255, 255))
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
        return [code_image()]
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
    ch = Image.open(f"{A}/charactor/henrobo-front.png")
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
    base = Image.open(f"{A}/charactor/henrobo-front.png").convert("RGBA")
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


def main():
    only = [int(a) for a in sys.argv[1:]]
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
        out = f"{WORK}/henrobo-132.mp4"
    layers(clips, total)
    compose(video, total, out)
    print("done", out, f"{total / 60:.1f}分")


if __name__ == "__main__":
    main()
