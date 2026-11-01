"""声の候補を音声認識で文字に戻し、元の文との読みの近さで聞き取りやすさを比べる(#132)。

使い方: ~/.venvs/tried-asr/bin/python clarity.py <wavのフォルダ> <元の文>
"""
import difflib
import glob
import re
import sys

import mlx_whisper
import pyopenjtalk
import wave

MODEL = "mlx-community/whisper-large-v3-turbo"


def kana(t):
    t = re.sub(r"[、。,.!?！？…「」『』()（）\s]", "", t)
    return re.sub(r"[’、。？！]", "", pyopenjtalk.g2p(t, kana=True))


def main(folder, text):
    ref = kana(text)
    for f in sorted(glob.glob(f"{folder}/*.wav")):
        heard = mlx_whisper.transcribe(f, path_or_hf_repo=MODEL, language="ja")["text"].strip()
        sim = difflib.SequenceMatcher(None, ref, kana(heard)).ratio()
        with wave.open(f) as w:
            sec = w.getnframes() / w.getframerate()
        print(f"{f.split('/')[-1]}\t{sim:.3f}\t{sec:.1f}s\t{len(text)/sec:.1f}字/秒\t{heard}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
