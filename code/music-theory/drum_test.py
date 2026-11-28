"""ドラムの譜を作れるかを確かめる(#189)。

General MIDI の決まりでは、10番チャンネルの音の高さが打楽器の種類を表す。
36=バスドラム、38=スネア、42=ハイハット(閉)。
8ビートを2小節書き、MusicXML・MIDI・PNG にする。
"""
import sys

from music21 import clef, instrument, meter, note, percussion, stream

from score import export

out = sys.argv[1] if len(sys.argv) > 1 else "out"

KICK, SNARE, HAT = 36, 38, 42
# 8分音符ごとに鳴らす楽器。1小節は8つ
BAR = [
    (HAT, KICK), (HAT,), (HAT, SNARE), (HAT,),
    (HAT, KICK), (HAT, KICK), (HAT, SNARE), (HAT,),
]

part = stream.Part()
part.insert(0, instrument.Percussion())  # 10番チャンネルに割り当てる
part.append(clef.PercussionClef())
part.append(meter.TimeSignature("4/4"))
for _ in range(2):
    for hits in BAR:
        if len(hits) == 1:
            n = note.Unpitched(quarterLength=0.5)
        else:
            n = percussion.PercussionChord(
                [note.Unpitched() for _ in hits], quarterLength=0.5)
        # 譜の上の位置(displayStep)と、鳴らす楽器(storedInstrument の MIDI 番号)を決める
        targets = [n] if len(hits) == 1 else n.notes
        for u, h in zip(targets, hits):
            u.displayStep, u.displayOctave = {KICK: ("F", 4), SNARE: ("C", 5), HAT: ("G", 5)}[h]
            inst = instrument.UnpitchedPercussion()
            inst.percMapPitch = h
            u.storedInstrument = inst
            if h == HAT:
                u.notehead = "x"
        part.append(n)

s = stream.Score([part])
for path in export(s, f"{out}/drum_8beat", title="8ビート"):
    print(path)
