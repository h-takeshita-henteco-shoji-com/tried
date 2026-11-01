"""台本(henrobo-script.md)の台詞を、へんロボの声で1行ずつ読ませる(#132)。

#106 の voice_lines.py を、へんロボ1人用に直したもの。
- 声: assets/voice-design/B_en_calm_1.wav を、Qwen3-TTS の Base モデルで複製する。加工はしない
- 「(間)」「(キラリ)」は読ませない。間は pauseBefore、キラリは glint として lines.json に残す
- 声を作るときだけ、読みの表(tts-readings.tsv)で誤りやすい語をかなに置き換える。text は台本のまま(字幕用)

使い方: ~/.venvs/tried-audio/bin/python voice_lines.py <台本.md> <出力フォルダ> [読みの表.tsv]
出力: <出力フォルダ>/lines.json と、1行ずつの wav
"""
import json
import os
import re
import sys
import time

import numpy as np
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

DAY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる"))
REF = (f"{DAY}/assets/voice-design/B_en_calm_1.wav",
       "こんにちは、へんロボです。今日は、AIに建築の図面を読ませて、三社十のモデルで比べた結果をお話しします。単純な図面ほど、意外な所でつまずきました。")
SEED = 1


def parse(path):
    scenes, cur = [], None
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^## (\d+)\. (.+)", line)
        if m:
            cur = {"no": int(m.group(1)), "title": m.group(2).strip(), "lines": []}
            scenes.append(cur)
            continue
        m = re.match(r"^> ((?:\((?:間|キラリ)\) )*)へんロボ: (.+)", line)
        if m and cur:
            cur["lines"].append({"speaker": "へんロボ", "text": m.group(2).strip(),
                                 "pauseBefore": "(間)" in m.group(1), "glint": "(キラリ)" in m.group(1)})
    return scenes


def load_readings(path):
    if not path or not os.path.exists(path):
        return []
    rows = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8")]
    return [(r[0], r[1]) for r in rows if len(r) == 2 and not r[0].startswith("#")]


def apply_readings(text, readings):
    for a, b in readings:
        text = text.replace(a, b)
    return text


def main():
    script, out = sys.argv[1], sys.argv[2]
    readings = load_readings(sys.argv[3] if len(sys.argv) > 3 else None)
    os.makedirs(out, exist_ok=True)
    scenes = parse(script)
    model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="mps", dtype=torch.float32)
    prompt = model.create_voice_clone_prompt(ref_audio=REF[0], ref_text=REF[1])
    for sc in scenes:
        for i, ln in enumerate(sc["lines"]):
            name = f"s{sc['no']:02d}_{i:02d}.wav"
            path = f"{out}/{name}"
            ln["file"] = name
            ln["ttsText"] = apply_readings(ln["text"], readings)
            if os.path.exists(path):
                continue
            torch.manual_seed(SEED)
            t0 = time.time()
            wavs, sr = model.generate_voice_clone(text=ln["ttsText"], language="Japanese", voice_clone_prompt=prompt)
            x = np.asarray(wavs[0], dtype=np.float64)
            sf.write(path, np.clip(x, -1, 1), sr)
            torch.mps.empty_cache()  # 行ごとに GPU のメモリを返す（#98 で、返さないと遅くなった）
            print(name, f"{len(x) / sr:.1f}s", f"{time.time() - t0:.0f}s gen", ln["ttsText"], flush=True)
    json.dump(scenes, open(f"{out}/lines.json", "w"), ensure_ascii=False, indent=1)
    print("lines", sum(len(s["lines"]) for s in scenes))


if __name__ == "__main__":
    main()
