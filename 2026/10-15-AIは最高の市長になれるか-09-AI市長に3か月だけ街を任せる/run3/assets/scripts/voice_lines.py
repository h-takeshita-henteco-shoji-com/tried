"""批評の台本(numedon-review-script.md)の台詞を、ぬめとどんの声で読ませる(#73)。

声は #28(ぬめとどんの声を設計する)で採用したもの。Qwen3-TTS の Base モデルで声をクローンする。
- どん: don_qwen_B_1.wav をクローンし、#28 の加工(角を丸くし、抑揚を3倍)をかける
- ぬめ: nume_qwen_C_1.wav をクローンする(加工なし)
「(間)」などのト書きは読ませない。

使い方: ~/.venvs/tried-audio/bin/python voice_lines.py <台本.md> <出力フォルダ>
出力: <出力フォルダ>/lines.json(場面・話し手・台詞・ファイル)と、1行ずつの wav
"""
import json
import math
import os
import re
import statistics
import sys
import time

import numpy as np
import parselmouth
import soundfile as sf
import torch
from parselmouth.praat import call
from qwen_tts import Qwen3TTSModel
from scipy.signal import butter, sosfilt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 5))
VOICE = f"{ROOT}/2026/10-09-かわいいキャラのショート動画をAIで作る-11-ぬめとどんの声を設計する/assets/generated"
REFS = {
    "どん": (f"{VOICE}/don_qwen_B_1.wav", "……んー。熱いっていうより、ぬるい寄りの熱い、だな。おれは、ここでいい。……行ったか。"),
    "ぬめ": (f"{VOICE}/nume_qwen_C_1.wav", "どん、あれ何。どん、まだ熱い？ぬめ、もう行く。そっか。……んしょ。"),
}
SEED = 1


def parse(path):
    scenes, cur = [], None
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^## (\d+)\. (.+)", line)
        if m:
            cur = {"no": int(m.group(1)), "title": m.group(2).strip(), "lines": []}
            scenes.append(cur)
            continue
        m = re.match(r"^> (ぬめ|どん): (.+)", line)
        if m and cur:
            text = re.sub(r"\((間|[^)]*向く[^)]*|[^)]*這う[^)]*)\)", "", m.group(2)).strip()
            pause = "(間)" in m.group(2)
            cur["lines"].append({"speaker": m.group(1), "text": text, "pauseBefore": pause})
    return scenes


def finish_don(x, sr):
    """#28 の finish.py と同じ加工。高い音を弱めて角を丸くし、抑揚を3倍に広げる。"""
    lo = sosfilt(butter(2, 4000, "low", fs=sr, output="sos"), x)
    y = lo + (x - lo) * 10 ** (-4 / 20)
    y *= np.sqrt(np.mean(x ** 2) / max(np.mean(y ** 2), 1e-12))
    snd = parselmouth.Sound(np.clip(y, -1, 1), sampling_frequency=sr)
    m = call(snd, "To Manipulation", 0.01, 60, 400)
    tier = call(m, "Extract pitch tier")
    n = call(tier, "Get number of points")
    if n < 2:
        return y
    pts = [(call(tier, "Get time from index", i), call(tier, "Get value at index", i)) for i in range(1, n + 1)]
    center = statistics.median(math.log(f) for _, f in pts)
    call(tier, "Remove points between", snd.xmin, snd.xmax)
    for t, f in pts:
        call(tier, "Add point", t, math.exp(center + (math.log(f) - center) * 3.0))
    call([tier, m], "Replace pitch tier")
    out = call(m, "Get resynthesis (overlap-add)")
    return np.array(out.values[0])


def main():
    script, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    scenes = parse(script)
    model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="mps", dtype=torch.float32)
    prompts = {sp: model.create_voice_clone_prompt(ref_audio=a, ref_text=t) for sp, (a, t) in REFS.items()}
    for sc in scenes:
        for i, ln in enumerate(sc["lines"]):
            name = f"s{sc['no']:02d}_{i:02d}_{'don' if ln['speaker'] == 'どん' else 'nume'}.wav"
            path = f"{out}/{name}"
            ln["file"] = name
            if os.path.exists(path):
                continue
            torch.manual_seed(SEED)
            t0 = time.time()
            wavs, sr = model.generate_voice_clone(text=ln["text"], language="Japanese", voice_clone_prompt=prompts[ln["speaker"]])
            x = np.asarray(wavs[0], dtype=np.float64)
            if ln["speaker"] == "どん":
                x = finish_don(x, sr)
            sf.write(path, np.clip(x, -1, 1), sr)
            print(name, f"{len(x) / sr:.1f}s", f"{time.time() - t0:.0f}s gen", ln["text"], flush=True)
    json.dump(scenes, open(f"{out}/lines.json", "w"), ensure_ascii=False, indent=1)
    print("lines", sum(len(s["lines"]) for s in scenes))


if __name__ == "__main__":
    main()
