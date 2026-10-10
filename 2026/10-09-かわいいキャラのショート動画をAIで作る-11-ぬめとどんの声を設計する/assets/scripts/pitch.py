# 話す速さは変えずに、声の高さだけを少し上げる。
# 位相ボコーダ(librosa)はエコーが出たため、話し声向けの PSOLA(Praat)に替えた。
import sys, parselmouth
from parselmouth.praat import call
src = sys.argv[1]
snd = parselmouth.Sound(src)
for steps in [0.5, 1.0]:
    m = call(snd, "To Manipulation", 0.01, 60, 400)
    tier = call(m, "Extract pitch tier")
    call(tier, "Multiply frequencies", snd.xmin, snd.xmax, 2 ** (steps / 12))
    call([tier, m], "Replace pitch tier")
    out = src.replace(".wav", f"_up{steps:.1f}.wav")
    call(m, "Get resynthesis (overlap-add)").save(out, "WAV")
    print(out.split("/")[-1])
