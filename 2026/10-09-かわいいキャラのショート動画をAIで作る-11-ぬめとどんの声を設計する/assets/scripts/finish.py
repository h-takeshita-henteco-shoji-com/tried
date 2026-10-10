# 採用した加工をまとめてかける。角を丸くし(soft1)、抑揚を3倍に広げる。
# 中身は soften.py の soft1 と intonation.py の 3.0 と同じ。
import sys, math, statistics, numpy as np, soundfile as sf, parselmouth
from scipy.signal import butter, sosfilt
from parselmouth.praat import call
for src in sys.argv[1:]:
    x, sr = sf.read(src)
    lo = sosfilt(butter(2, 4000, "low", fs=sr, output="sos"), x)
    y = lo + (x - lo) * 10 ** (-4 / 20)
    y *= np.sqrt(np.mean(x**2) / np.mean(y**2))
    snd = parselmouth.Sound(np.clip(y, -1, 1), sampling_frequency=sr)
    m = call(snd, "To Manipulation", 0.01, 60, 400)
    tier = call(m, "Extract pitch tier")
    n = call(tier, "Get number of points")
    pts = [(call(tier, "Get time from index", i), call(tier, "Get value at index", i)) for i in range(1, n + 1)]
    center = statistics.median(math.log(f) for _, f in pts)
    call(tier, "Remove points between", snd.xmin, snd.xmax)
    for t, f in pts:
        call(tier, "Add point", t, math.exp(center + (math.log(f) - center) * 3.0))
    call([tier, m], "Replace pitch tier")
    out = src.replace(".wav", "_final.wav")
    call(m, "Get resynthesis (overlap-add)").save(out, "WAV")
    print(out.split("/")[-1])
