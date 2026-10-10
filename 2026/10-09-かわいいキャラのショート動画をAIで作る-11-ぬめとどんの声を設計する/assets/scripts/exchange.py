# 2匹のやりとりを1本につなぐ。ぬめが聞き、どんが遅れて答え、ぬめが相づちを打つ。
import sys, numpy as np, soundfile as sf
g = sys.argv[1]
for cand in ["A", "C"]:
    for i in [1, 2, 3]:
        parts = [f"{g}/nume_clone{cand}_ask_{i}.wav", 1.0, f"{g}/don_clone_reply_{i}_final.wav", 0.6, f"{g}/nume_clone{cand}_sokka_{i}.wav"]
        out, sr = [], None
        for p in parts:
            if isinstance(p, float):
                out.append(np.zeros(int(p * sr)))
            else:
                x, s = sf.read(p)
                assert sr in (None, s), (p, s, sr)
                sr = s
                out.append(x if x.ndim == 1 else x.mean(axis=1))
        f = f"{g}/exchange_nume{cand}_{i}.wav"
        sf.write(f, np.concatenate(out), sr)
        print(f.split("/")[-1])
