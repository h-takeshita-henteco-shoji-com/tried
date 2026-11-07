"""作図の録画を早送りにし、AI の発言と操作を字幕で重ねる(#136)。

建設業の人に、AI が何を考えて何を描いているかを、見て分かる形にする。
record_run.py が残した録画(OBS)と events.jsonl(AI の出力に、録画の開始からの秒数を付けたもの)を使う。

- 早送りの倍率は2段。描き始める前(図面を読む間)は画面が動かないので高い倍率、描く間は一定の倍率。
  右上に、実際の経過時間といまの倍率を出す
- 下の字幕は、AI が書いた文。長い文は、始めの1〜2文だけ出す
- 左上の札は、いま AI が使っている道具を、日本語の動詞で出す(線を描く、寸法を入れる など)
- 先頭に題を、最後に描き終えた図面を数秒止めて出す
- この ffmpeg は字幕の機能(libass)を持たない。文字は PIL で透明な画像にし、0.5秒ごとに並べて重ねる

使い方:
  ~/.venvs/tried-audio/bin/python code/librecad-mcp/make_timelapse.py <記録のフォルダ> <出力.mp4> \\
    --title "AIに矩計図を描かせる" --length 180
"""
import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
STEP = 0.5          # 字幕の画像を切り替える間隔(出力の秒)
THUMB_CROP = (30, 140, 1390, 985)  # 1920x1080 のコマの中の、LibreCAD の図面の部分
HOLD = 4.0          # 最後に図面を止めて見せる秒数
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"

TOOL_JA = {
    "ping": "つながりを確かめる", "doc_info": "図面の情報を読む", "operation_log": "操作の記録を読む",
    "set_vars": "図面の設定を変える", "open_drawing": "図面を開く", "new_drawing": "新しい図面を開く",
    "save": "保存する", "save_as": "名前を付けて保存する",
    "list_entities": "図面を読む", "get_entity": "図形を1つ読む", "list_blocks": "部品の一覧を読む",
    "list_fonts": "書体を調べる",
    "add_line": "線を描く", "add_polyline": "線をつなげて描く", "add_circle": "円を描く", "add_arc": "円弧を描く",
    "add_text": "文字を書く", "add_dim_linear": "寸法を入れる", "add_dim_aligned": "寸法を入れる",
    "add_hatch": "模様を塗る", "define_block": "部品を作る", "add_insert": "部品を置く",
    "set_props": "線の属性を変える", "move": "動かす", "copy": "写す", "rotate": "回す", "scale": "大きさを変える",
    "mirror": "反転して写す", "delete": "消す", "stretch": "伸び縮みさせる", "undo": "元に戻す", "redo": "やり直す",
    "layers": "レイヤーを調べる", "set_layer": "レイヤーを作る・選ぶ",
    "zoom": "表示を合わせる", "screenshot": "画面を撮って見直す", "measure": "長さを測る",
    "find_near": "近くの図形を探す", "check_connectivity": "線のつながりを確かめる", "validate": "図面を検査する",
    "snapshot": "今の状態を控える", "diff": "変わったところを比べる",
    "ToolSearch": "使える道具を調べる", "Read": "撮った画像を見る", "Workflow": "(使わない道具を誤って呼んだ)",
}


def font(size):
    return ImageFont.truetype(FONT, size)


def load_events(run_dir):
    """(秒, 種類, 中身) の列。種類は text(AIの文)と tool(道具の名前)。"""
    out = []
    for line in (run_dir / "events.jsonl").read_text().splitlines():
        e = json.loads(line)
        try:
            m = json.loads(e["line"])
        except ValueError:
            continue
        if m.get("type") != "assistant":
            continue
        for c in m["message"].get("content", []):
            # 字幕は日本語の説明だけにする。AI が途中で英語の短い見出しを書くことがあるため(#146)
            if c.get("type") == "text" and re.search(r"[ぁ-んァ-ン一-龥]", c["text"]):
                out.append((e["t"], "text", c["text"].strip()))
            elif c.get("type") == "tool_use":
                out.append((e["t"], "tool", c["name"].split("__")[-1]))
    return out


def short(text, limit=60):
    """字幕に出す分。Markdown の記号を外し、始めの文から limit 字まで。"""
    t = re.sub(r"[#*`|>]+", "", text)
    t = re.sub(r"\s*\n\s*", " ", t).strip()
    s = re.split(r"(?<=[。！？])", t)
    cap = ""
    for x in s:
        if len(cap) + len(x) > limit and cap:
            break
        cap += x
    return cap[:limit] + ("…" if len(cap) > limit else "")


def wrap(draw, text, f, width):
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=f) > width:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    return lines + ([cur] if cur else [])


def card(lines):
    """説明の札。1行目は見出し、2行目からは本文(「・」で始めると箇条書き)。"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fh, fb = font(56), font(40)
    body = []
    for ln in lines[1:]:
        body += wrap(d, ln, fb, W - 520) or [""]
    h = 130 + 66 * len(body) + 60
    top = (H - h) / 2
    d.rounded_rectangle((200, top, W - 200, top + h), 24, fill=(20, 30, 45, 235))
    d.text((260, top + 80), lines[0], font=fh, fill="white", anchor="lm")
    for i, ln in enumerate(body):
        d.text((260, top + 170 + 66 * i), ln, font=fb, fill=(215, 225, 235), anchor="lm")
    return im


def overlay(clock, op, count, caption, title, speed):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if isinstance(title, list):
        return card(title)
    if title:
        f1, f2 = font(64), font(34)
        d.rounded_rectangle((260, 380, W - 260, 660), 24, fill=(20, 30, 45, 230))
        d.text((W / 2, 470), title[0], font=f1, fill="white", anchor="mm")
        d.text((W / 2, 570), title[1], font=f2, fill=(200, 215, 230), anchor="mm")
        return im
    # 右上: 実際の経過時間と倍率
    f = font(34)
    txt = f"経過 {int(clock // 60)}:{int(clock % 60):02d}（{speed:g}倍速）"
    tw = d.textlength(txt, font=f)
    d.rounded_rectangle((W - tw - 60, 20, W - 20, 84), 14, fill=(0, 0, 0, 190))
    d.text((W - 40, 52), txt, font=f, fill="white", anchor="rm")
    # 左上: いまの操作
    if op:
        txt = f"AIの操作: {op}"
        sub = f"{count}回目"
        f2 = font(26)
        tw = max(d.textlength(txt, font=f), d.textlength(sub, font=f2))
        d.rounded_rectangle((20, 20, 60 + tw, 128), 14, fill=(0, 90, 160, 210))
        d.text((40, 52), txt, font=f, fill="white", anchor="lm")
        d.text((40, 104), sub, font=f2, fill=(210, 230, 250), anchor="lm")
    # 下: AI の発言
    if caption:
        f = font(42)
        lines = wrap(d, "AI「" + caption + "」", f, W - 240)[:2]
        h = 70 * len(lines) + 30
        d.rounded_rectangle((80, H - h - 40, W - 80, H - 40), 18, fill=(0, 0, 0, 200))
        for i, ln in enumerate(lines):
            d.text((120, H - h - 40 + 50 + 70 * i), ln, font=f, fill="white", anchor="lm")
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("out")
    ap.add_argument("--video", default=None, help="録画。なければ run.json の video")
    ap.add_argument("--title", default="AIに矩計図を描かせる")
    ap.add_argument("--subtitle", default=None, help="題の下の行。なければモデル名と倍率")
    ap.add_argument("--length", type=float, default=180, help="早送りした本編の長さ(秒)の目安")
    ap.add_argument("--title-sec", type=float, default=3.0)
    ap.add_argument("--intro", default=None, help="題のあとに出す説明の札(テキスト。1行目が見出し)")
    ap.add_argument("--intro-sec", type=float, default=7.0)
    ap.add_argument("--outro", default=None, help="最後に出す結果の札(テキスト。1行目が見出し)")
    ap.add_argument("--outro-sec", type=float, default=8.0)
    ap.add_argument("--thumb", default=None, help="サムネイル(1280x720 の jpg)の出力先")
    ap.add_argument("--read-sec", type=float, default=10.0, help="描き始める前の部分を縮めた長さ(秒)")
    a = ap.parse_args()

    run_dir = Path(a.run_dir)
    run = json.loads((run_dir / "run.json").read_text())
    video = Path(a.video or run["video"])
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(video)], capture_output=True, text=True).stdout)
    events = load_events(run_dir)
    # 描き始める前(図面を読んでいる間)は、画面が動かない。その間だけ倍率を上げ、READ_SEC 秒ほどに縮める
    draws = [e[0] for e in events if e[1] == "tool" and e[2].startswith(("add_", "set_layer"))]
    t_draw = max(0.0, (draws[0] if draws else 0) - 2)
    speed = max(1, round((dur - t_draw) / a.length))
    speed_read = max(speed, round(t_draw / a.read_sec)) if t_draw > 0 else speed
    seg_read = t_draw / speed_read
    body = seg_read + (dur - t_draw) / speed

    def clock_at(t):  # 出力の本編の秒 → 実際の経過秒
        return t * speed_read if t < seg_read else t_draw + (t - seg_read) * speed
    model = run["model"].replace("claude-", "Claude ").replace("-", " ").title().replace(" 5 5", " 5.5").replace(" 5 1", " 5.1")
    sub = a.subtitle or f"{model}・LibreCAD を MCP で操作・実際の {int(dur // 60)}分{int(dur % 60)}秒 を早送り"
    intro = Path(a.intro).read_text().strip().splitlines() if a.intro else None
    outro = Path(a.outro).read_text().strip().splitlines() if a.outro else None
    head = a.title_sec + (a.intro_sec if intro else 0)
    tail = HOLD + (a.outro_sec if outro else 0)

    work = Path(tempfile.mkdtemp(prefix="timelapse-"))
    total = head + body + tail
    n = int(total / STEP) + 1
    lst = []
    prev_key, prev_png = None, None
    for i in range(n):
        t_out = i * STEP
        title = (a.title, sub) if t_out < a.title_sec else intro if t_out < head else None
        if outro and t_out >= head + body + HOLD:
            title = outro
        clock = min(dur, clock_at(max(0.0, t_out - head)))
        cur_speed = speed_read if clock < t_draw else speed
        past = [e for e in events if e[0] <= clock]
        tools = [e for e in past if e[1] == "tool"]
        op = TOOL_JA.get(tools[-1][2], tools[-1][2]) if tools and clock < dur else ("描き終えた" if clock >= dur else "")
        texts = [e for e in past if e[1] == "text"]
        # 発言は、出てから実時間で 40 秒か、次の発言まで出す
        cap = short(texts[-1][2]) if texts and clock - texts[-1][0] < 40 else ""
        key = (str(title), int(clock), op, len(tools), cap, cur_speed)
        if key != prev_key:
            png = work / f"o{i:05d}.png"
            overlay(clock, op, len(tools), cap, title, cur_speed).save(png)
            prev_key, prev_png = key, png
        lst.append(prev_png)
    with (work / "list.txt").open("w") as f:
        for p in lst:
            f.write(f"file '{p}'\nduration {STEP}\n")
        f.write(f"file '{lst[-1]}'\n")
    # 本編: 題の間は最初のコマを止め、早送りし、最後のコマを止める
    vf = (f"[0:v]trim=0:{t_draw},setpts=(PTS-STARTPTS)/{speed_read}[r];"
          f"[0:v]trim=start={t_draw},setpts=(PTS-STARTPTS)/{speed}[d];[r][d]concat=n=2:v=1[c];"
          f"[c]fps=30,scale={W}:{H}:force_original_aspect_ratio=decrease,"
          f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,tpad=start_mode=clone:start_duration={head}:"
          f"stop_mode=clone:stop_duration={tail}[v];"
          f"[1:v]fps=30,format=rgba[o];[v][o]overlay=0:0:shortest=1,format=yuv420p[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-f", "concat", "-safe", "0",
                    "-i", str(work / "list.txt"), "-filter_complex", vf, "-map", "[out]", "-an",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", a.out],
                   check=True)
    if a.thumb:
        # 字幕のない元の録画の最後のコマから、図面の部分を切り出し、下に題を置く
        last = work / "last.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-1", "-i", str(video), "-frames:v", "1",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2",
                        str(last)], check=True)
        draw = Image.open(last).convert("RGB").crop(THUMB_CROP)
        im = Image.new("RGB", (1280, 720), (15, 25, 40))
        draw.thumbnail((1280, 500))
        im.paste(draw, ((1280 - draw.width) // 2, 0))
        d = ImageDraw.Draw(im)
        d.text((640, 570), a.title, font=font(84), fill="white", anchor="mm")
        d.text((640, 665), f"{model} が LibreCAD を操作", font=font(40), fill=(255, 210, 90), anchor="mm")
        im.save(a.thumb, quality=92)
    shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({"out": a.out, "speed_read": speed_read, "speed": speed, "seconds": round(total, 1)},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
