"""周波数を直接指定して WAV を作る道具(#189)。

MIDI と MuseScore は平均律が前提なので、ピタゴラス音律、シュルティ、ガムランなど
平均律から外れた音の高さは、ここで正弦波を合成して聴き比べる。

使い方:
    from tone import write_wav, cents_to_ratio
    write_wav("assets/pyth.wav", [(261.63, 0.5), (261.63 * 9 / 8, 0.5)])
    write_wav("assets/chord.wav", [([261.63, 261.63 * 3 / 2], 2.0)])  # 同時に鳴らす
"""
from __future__ import annotations

import wave

import numpy as np

RATE = 44100


def cents_to_ratio(cents: float) -> float:
    """セント(半音=100)を周波数の比に直す。"""
    return 2 ** (cents / 1200)


def _note(freqs, sec: float) -> np.ndarray:
    t = np.arange(int(RATE * sec)) / RATE
    freqs = freqs if isinstance(freqs, (list, tuple)) else [freqs]
    # 倍音を少し足して、純正と平均律のうなりを聴き取りやすくする
    y = sum(sum(np.sin(2 * np.pi * f * k * t) / k ** 1.5 for k in (1, 2, 3)) for f in freqs)
    env = np.minimum(1, t / 0.02) * np.minimum(1, (sec - t) / 0.05)  # 立ち上がりと終わりのクリック音を消す
    return y * env / max(len(freqs), 1)


def write_wav(path: str, notes, gain: float = 0.3) -> str:
    """notes は (周波数 または 周波数のリスト, 秒) の並び。休符は周波数に [] を渡す。"""
    y = np.concatenate([_note(f, sec) for f, sec in notes])
    y = y / (np.abs(y).max() or 1) * gain
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes((y * 32767).astype(np.int16).tobytes())
    return path
