# 本番の音を組む。#20 の rough_mix.py を写し、次の2点だけ変えた。
# - どんの台詞を「……んー。今日は、なんだかぬるめだなぁ。」(don_clone_cut6b_2_final.wav)に替えた。
# - カット7に、ぬめの空返事「……ん、そっかぁ……。」を足した。どんより約7dB 小さくし、高い音を丸めてつぶやきに寄せる。
# - 新しい台詞は4.2秒あり、カット6(4秒)に収まらない。カット6を5秒に延ばした。
# - どんの台詞と空返事の間を約2秒あけるため、カット7を3秒から4秒に延ばした。
# - 2つ延ばした分、#20 で21秒より後に置いた音を2秒ずらした。全部で38秒。
# 使い方: python mix_final.py <出力ファイル> [<BGM のファイル>]
# BGM は OpenTracks の曲。規約で再配布が禁止なので、BGM も BGM 入りの出力もリポジトリに置かない。
import sys, numpy as np, soundfile as sf, librosa
from pathlib import Path
from scipy.signal import butter, sosfiltfilt

HERE = Path(__file__).resolve().parents[1]
DAY = HERE.parents[1]
S20 = DAY / "10-09-かわいいキャラのショート動画をAIで作る-10-声と音を付ける/assets/generated"
S28 = DAY / "10-09-かわいいキャラのショート動画をAIで作る-11-ぬめとどんの声を設計する/assets/generated"
out = sys.argv[1]
bgm_file = sys.argv[2] if len(sys.argv) > 2 else None
SR, LENGTH = 44100, 38.0
SHIFT = 2.0  # #20 の21秒より後をずらす量(カット6と7を1秒ずつ延ばした)
REPLY = "nume_clone_cut7b_2.wav"  # ぬめの空返事

def later(t):
    return t + SHIFT if t >= 21.0 else t

def load(path, gain_db=0.0, peak_db=None):
    y, sr = sf.read(path, always_2d=True)
    y = y.T.astype(np.float32)
    if sr != SR:
        y = librosa.resample(y, orig_sr=sr, target_sr=SR)
    if y.shape[0] == 1:
        y = np.repeat(y, 2, axis=0)
    if peak_db is not None:
        y *= 10 ** (peak_db / 20) / np.abs(y).max()
    return y * 10 ** (gain_db / 20)

mix = np.zeros((2, int(SR * LENGTH)), dtype=np.float32)
def place(y, start):
    i = int(SR * start)
    n = min(y.shape[1], mix.shape[1] - i)
    mix[:, i:i + n] += y[:, :n]

# 湯の音: #20 と同じ。2kHz より上を削り、1秒ごとの中央を -55dB に合わせる。37秒に足りなければ頭からつなぐ。
yu = load(S20 / "yu_flow_anime_stableaudio_2.wav")
yu = sosfiltfilt(butter(4, 2000, "low", fs=SR, output="sos"), yu, axis=1).astype(np.float32)
sec = [np.sqrt(np.mean(yu[:, i:i + SR] ** 2)) for i in range(0, yu.shape[1] - SR + 1, SR)]
yu *= 10 ** (-55 / 20) / np.median(sec)
if yu.shape[1] < mix.shape[1]:
    f = int(SR * 0.5)
    a, b = yu.copy(), yu.copy()
    a[:, -f:] *= np.linspace(1, 0, f); b[:, :f] *= np.linspace(0, 1, f)
    yu = np.concatenate([a[:, :-f], a[:, -f:] + b[:, :f], b[:, f:]], axis=1)
place(yu, 0.0)
place(load(S20 / "door_anime_stableaudio_2.wav", gain_db=-12), 1.5 - 0.05)              # 戸: カット1
place(load(S28 / "nume_cloneC_cut3_1.wav", peak_db=-3), 8.0 - 0.16)                     # ぬめ: カット3
place(load(HERE / "generated/voice/don_clone_cut6b_2_final.wav", peak_db=-3), 17.2 - 0.34)  # どん: カット6(17〜22秒)
# ぬめの空返事: カット7(22〜26秒)の頭から1.5秒。どんの声の終わり(約21.4秒)から約2秒あける。peak -10dB(どんは -3dB)。4kHz より上を -6dB。
reply = load(HERE / "generated/voice" / REPLY, peak_db=-10)
lo = sosfiltfilt(butter(2, 4000, "low", fs=SR, output="sos"), reply, axis=1)
reply = (lo + (reply - lo) * 10 ** (-6 / 20)).astype(np.float32)
place(reply, 23.5)
place(load(S20 / "light_anime_stableaudio_1.wav", gain_db=-8), later(31.0) - 0.01)     # 灯り: カット9

step = load(S20 / "nume_step_anime_stableaudio_2.wav", peak_db=-9)
def pop(t, length=0.15):
    a = int(SR * (t - 0.01)); b = a + int(SR * length)
    y = step[:, a:b].copy()
    f = int(SR * 0.03)
    y[:, -f:] *= np.linspace(1, 0, f)
    return y
pops = [pop(t) for t in (0.09, 0.86, 2.65, 3.29)]
moves = [4.5, 4.9, 7.1, 7.45, 8.6, 33.2, 33.55, 33.9]
for k, t in enumerate(moves):
    place(pops[k % len(pops)], later(t))

# BGM: #20 と同じ。台詞の間だけ6dB 下げる。どんの台詞は1秒長くなった。
if bgm_file:
    bgm = load(bgm_file)[:, :mix.shape[1]]
    bgm *= 10 ** (-32 / 20) / np.sqrt(np.mean(bgm ** 2))
    duck = np.ones(bgm.shape[1], dtype=np.float32)
    for a, b in [(7.8, 9.2), (16.8, 21.6), (23.4, 25.5)]:
        i, j, r = int(SR * a), int(SR * b), int(SR * 0.3)
        duck[i - r:i] = np.minimum(duck[i - r:i], np.linspace(1, 0.5, r))
        duck[i:j] = 0.5
        duck[j:j + r] = np.minimum(duck[j:j + r], np.linspace(0.5, 1, r))
    bgm *= duck
    f = int(SR * 1.0)
    bgm[:, :f] *= np.linspace(0, 1, f)
    place(bgm, 0.0)

fi, fo = int(SR * 0.3), int(SR * 1.5)
mix[:, :fi] *= np.linspace(0, 1, fi)
mix[:, -fo:] *= np.linspace(1, 0, fo)
peak = np.abs(mix).max()
if peak > 0.98:
    mix *= 0.98 / peak
sf.write(out, mix.T, SR)
print(out, f"{LENGTH:.0f}s, peak {20*np.log10(np.abs(mix).max()):.1f} dBFS")
