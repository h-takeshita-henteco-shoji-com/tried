# 平均の高さは保ったまま、抑揚(高さの上下の幅)だけを変える。PSOLA(Praat)を使う。
import sys, math, statistics, parselmouth
from parselmouth.praat import call
src = sys.argv[1]
snd = parselmouth.Sound(src)
ks = [float(a) for a in sys.argv[2:]] or [0.7, 1.3]
for k in ks:
    m = call(snd, "To Manipulation", 0.01, 60, 400)
    tier = call(m, "Extract pitch tier")
    n = call(tier, "Get number of points")
    pts = [(call(tier, "Get time from index", i), call(tier, "Get value at index", i)) for i in range(1, n + 1)]
    center = statistics.median(math.log(f) for _, f in pts)
    call(tier, "Remove points between", snd.xmin, snd.xmax)
    for t, f in pts:
        # 対数(音程)の上で、中心からのずれを k 倍する
        call(tier, "Add point", t, math.exp(center + (math.log(f) - center) * k))
    call([tier, m], "Replace pitch tier")
    out = src.replace(".wav", f"_into{k:.1f}.wav")
    call(m, "Get resynthesis (overlap-add)").save(out, "WAV")
    print(out.split("/")[-1])
