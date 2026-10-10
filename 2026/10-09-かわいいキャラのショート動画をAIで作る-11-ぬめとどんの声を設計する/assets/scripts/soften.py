# 高い音を弱めて、声の角を丸くする。強さ違いで3本作る。
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
src = sys.argv[1]
x, sr = sf.read(src)
def shelf(x, fc, gain_db):
    # 低い音はそのまま、fc より上だけを gain_db 下げる
    lo = sosfilt(butter(2, fc, "low", fs=sr, output="sos"), x)
    return lo + (x - lo) * 10 ** (gain_db / 20)
variants = {
    "soft1": lambda x: shelf(x, 4000, -4),
    "soft2": lambda x: shelf(x, 3000, -8),
    "soft3": lambda x: shelf(shelf(x, 2500, -8), 6000, -10),
}
for name, f in variants.items():
    y = f(x)
    y *= np.sqrt(np.mean(x**2) / np.mean(y**2))  # 音量を元に揃える
    y = np.clip(y, -1, 1)
    out = src.replace(".wav", f"_{name}.wav")
    sf.write(out, y, sr)
    print(out.split("/")[-1])
