"""道具が一通り動くかを確かめる(#189)。

1. music21 でハ長調の音階と和音を書き、MusicXML・MIDI・PNG にする
2. 同じ「ド・ソ」の5度を、純正(3:2)と平均律(700セント)で WAV にして聴き比べる
"""
import sys

from music21 import chord, meter, note, stream

from score import export
from tone import cents_to_ratio, write_wav

out = sys.argv[1] if len(sys.argv) > 1 else "out"

s = stream.Stream()
s.append(meter.TimeSignature("4/4"))
for p in ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]:
    s.append(note.Note(p, quarterLength=1))
s.append(chord.Chord(["C4", "E4", "G4"], quarterLength=4))
for path in export(s, f"{out}/smoke_scale", title="ハ長調の音階と主和音"):
    print(path)

C4 = 261.63
print(write_wav(f"{out}/smoke_fifth.wav", [
    ([C4, C4 * 3 / 2], 2.0),              # 純正の5度。うなりがない
    ([], 0.5),
    ([C4, C4 * cents_to_ratio(700)], 2.0),  # 平均律の5度。わずかにうなる
]))
