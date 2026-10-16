"""ぬめとどんの声を、場面ごとに録画の時刻へ並べ、動画に重ねる(#73)。

場面を置く時刻は、Mod のログ(command-log.txt)の実時間から決める。
録画の開始は 18:23:06(ファイルの creation_time。パネルの時刻と画面を照らし合わせて確かめた)。
前の場面の声が終わっていなければ、終わってから GAP_SCENE 秒あけて置く。
映像は作り直さず(-c:v copy)、声の音声だけを足す。録画には元の音声がない。
冒頭を切るときは、切る秒数を5つ目に渡す。映像をコピーで切るため、キーフレームの時刻を渡す。
(冒頭の初期化は約2分。パネルに最初の命令が出るキーフレームは 127.525 秒)

使い方: python3 overlay.py <voice フォルダ> <録画.mov> <出力.mov> <ffmpeg> [冒頭を切る秒数]
"""
import datetime
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

START = datetime.datetime(2026, 10, 16, 18, 23, 6)
SR = 24000
GAP_LINE = 0.5        # 同じ話し手が続くとき
GAP_TURN = 0.8        # 話し手が替わるとき
GAP_PAUSE = 1.5       # ト書きの「(間)」
GAP_SCENE = 1.0

# 場面の番号: (ログの実時間, 何の時刻か)
ANCHORS = {
    1: ("18:25:12", "最初の city_info(月例の始まり)"),
    2: ("18:28:59", "DO 高速道路への入口の道を試しに引く"),
    3: ("18:29:59", "DO 下水の出口を川に置けるか試す"),
    4: ("18:31:08", "DO 風力発電を1基置く(格子と区画の後)"),
    5: ("18:32:14", "1回目の advance が終わり、10-26 の見回り"),
    6: ("18:34:00", "11-15 の月例(工業の電気の困りごとを見る)"),
    7: ("18:36:27", "DO 工業に送電線を引く"),
    8: ("18:36:32", "DO 水道の予算を100→80に下げる"),
    9: ("18:40:32", "DO 風力の2基目を置く"),
    10: ("18:42:40", "最後の advance が終わり、任期の終わり"),
    11: ("18:42:47", "任期の終わりの確かめ"),
}


def load(path):
    x, sr = sf.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    if sr != SR:
        idx = np.arange(0, len(x), sr / SR)
        x = np.interp(idx, np.arange(len(x)), x)
    return x


def place(voice, trim=0.0):
    """台詞を録画の時刻に並べる。(位置の秒, 波形, 話し手) の並びと、場面ごとの予定を返す。lipsync.py も使う。"""
    scenes = json.load(open(f"{voice}/lines.json"))
    clips, cursor, plan = [], 0.0, []
    for sc in scenes:
        t = datetime.datetime.combine(START.date(), datetime.time.fromisoformat(ANCHORS[sc["no"]][0]))
        want = (t - START).total_seconds() - trim
        at = max(want, cursor + GAP_SCENE)
        pos, prev = at, None
        for ln in sc["lines"]:
            if prev is not None:
                pos += GAP_PAUSE if ln["pauseBefore"] else GAP_LINE if prev == ln["speaker"] else GAP_TURN
            x = load(f"{voice}/{ln['file']}")
            clips.append((pos, x, ln["speaker"]))
            pos += len(x) / SR
            prev = ln["speaker"]
        plan.append({"scene": sc["no"], "title": sc["title"], "want": round(want, 1), "start": round(at, 1), "end": round(pos, 1)})
        cursor = pos
    return clips, plan


def main():
    voice, video, out, ff = sys.argv[1:5]
    trim = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    clips, plan = place(voice, trim)
    total = max(p + len(x) / SR for p, x, _ in clips) + 1
    mix = np.zeros(int(total * SR))
    for p, x, _ in clips:
        i = int(p * SR)
        mix[i:i + len(x)] += x
    peak = np.max(np.abs(mix)) or 1
    mix = mix / peak * 0.9
    wav = f"{voice}/overlay.wav"
    sf.write(wav, mix, SR)
    json.dump(plan, open(f"{voice}/plan.json", "w"), ensure_ascii=False, indent=1)
    for p in plan:
        print(f"場面{p['scene']:2d} {p['title']}: {p['start'] // 60:.0f}:{p['start'] % 60:04.1f} - {p['end'] // 60:.0f}:{p['end'] % 60:04.1f}"
              + ("" if p["start"] == p["want"] else f"(予定 {p['want'] // 60:.0f}:{p['want'] % 60:04.1f} から後ろへずらした)"))
    subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(trim), "-i", video, "-i", wav,
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out], check=True)
    print("done", out, os.path.getsize(out))


if __name__ == "__main__":
    main()
