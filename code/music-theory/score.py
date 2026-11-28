"""music21 の譜を MusicXML・MIDI・PNG に書き出す共通の道具(#189)。

使い方:
    from score import export
    export(stream, "assets/ex01")  # ex01.musicxml / ex01.mid / ex01.png ができる

PNG は MuseScore 4 のコマンド(mscore)で作る。
MIDI は平均律の12音しか持てないため、微分音は tone.py で WAV にして確かめる。
"""
from __future__ import annotations

import glob
import os
import shutil
import subprocess

MSCORE = shutil.which("mscore") or "/Applications/MuseScore 4.app/Contents/MacOS/mscore"


def export(s, base: str, title: str = "", png: bool = True) -> list[str]:
    """譜 s を base.musicxml / base.mid / base.png に書き出し、作ったパスを返す。"""
    from music21 import metadata
    # 題を入れないと music21 が「Music21 Fragment」と書くので、明示して上書きする
    s.metadata = metadata.Metadata(title=title, composer="")
    os.makedirs(os.path.dirname(base) or ".", exist_ok=True)
    xml = s.write("musicxml", fp=base + ".musicxml")
    mid = s.write("midi", fp=base + ".mid")
    out = [str(xml), str(mid)]
    if png:
        # -T で余白を切り詰め、-r で解像度を下げる。
        # mscore は複数ページのとき base-1.png, base-2.png … を作る
        subprocess.run([MSCORE, "-T", "20", "-r", "200", "-o", base + ".png", str(xml)],
                       check=True, capture_output=True)
        out += sorted(glob.glob(base + "*.png"))
    return out
