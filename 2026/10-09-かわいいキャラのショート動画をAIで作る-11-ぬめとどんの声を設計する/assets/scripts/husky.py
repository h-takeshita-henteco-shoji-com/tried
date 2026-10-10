# かすれだけを減らす。WORLD で声を「高さ・声色・雑音成分」に分け、雑音成分だけを減らす。
# 加工なしで組み立て直しただけの版(husky0)も作り、WORLD 自体の音の劣化と区別する。
import sys, numpy as np, soundfile as sf, pyworld as pw
from scipy.signal import medfilt
src = sys.argv[1]
x, sr = sf.read(src)
x = x.astype(np.float64)
f0, t = pw.harvest(x, sr)
sp = pw.cheaptrick(x, f0, t, sr)
ap = pw.d4c(x, f0, t, sr)
voiced = f0 > 0
# 名前: (雑音成分を何乗するか, 高さの細かい揺れをならすか)
for name, power, smooth in [("husky0", 1.0, False), ("husky-1", 1.5, True), ("husky-2", 2.5, True)]:
    a = ap.copy()
    a[voiced] = a[voiced] ** power  # 0〜1 の値を累乗すると、雑音成分が小さくなる
    f = f0.copy()
    if smooth:
        f[voiced] = medfilt(f0, 5)[voiced]  # 震えの不揃い(ざらつき)を少しならす
    y = pw.synthesize(f, sp, a, sr)
    y *= np.sqrt(np.mean(x**2) / np.mean(y**2))
    out = src.replace(".wav", f"_{name}.wav")
    sf.write(out, np.clip(y, -1, 1), sr)
    print(out.split("/")[-1])
