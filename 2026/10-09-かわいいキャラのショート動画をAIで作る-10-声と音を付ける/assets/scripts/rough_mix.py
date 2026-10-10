# 声と音を、絵コンテ(#12)の秒数どおりに並べた仮組みを作る。カット6だけ4秒に延ばした。BGM の要否を聞いて決めるため。
# 使い方: python rough_mix.py <#28 の generated フォルダ> <出力ファイル> [<湯の音のファイル>] [<BGM のファイル>]
# BGM は OpenTracks(旧DOVA-SYNDROME)の曲。規約で音源の再配布が禁止なので、BGM も BGM 入りの出力もリポジトリに置かない。
import sys, numpy as np, soundfile as sf, librosa
from scipy.signal import butter, sosfiltfilt

voice_dir, out = sys.argv[1], sys.argv[2]
yu_file = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else "generated/yu_flow_anime_stableaudio_2.wav"
bgm_file = sys.argv[4] if len(sys.argv) > 4 else None
SR, LENGTH = 44100, 36.0  # カット1〜10の合計。カット6を3秒から4秒に延ばした(どんの台詞が3.4秒あるため)

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

# (ファイル, 置く秒, 音量)。置く秒は、ファイルの頭の無音を差し引いた値。
# 湯の音: 全カット。泡の「ぽこっ」が、ぬめの「ぷに」と被ったため、粒のない流れの音に替えた。
# 指示文の「低く」が効かず高い音になったので、2kHz より上を削って低くする。
# 音量は、1秒ごとの中央が -55dB になるよう合わせる。
yu = load(yu_file)
yu = sosfiltfilt(butter(4, 2000, "low", fs=SR, output="sos"), yu, axis=1).astype(np.float32)
sec = [np.sqrt(np.mean(yu[:, i:i + SR] ** 2)) for i in range(0, yu.shape[1] - SR + 1, SR)]
yu *= 10 ** (-55 / 20) / np.median(sec)
place(yu, 0.0)
place(load("generated/door_anime_stableaudio_2.wav", gain_db=-12), 1.5 - 0.05)      # 戸: カット1(0〜4秒)、遠く
place(load(f"{voice_dir}/nume_cloneC_cut3_1.wav", peak_db=-3), 8.0 - 0.16)          # ぬめ: カット3(7〜10秒)
place(load(f"{voice_dir}/don_clone_cut6_1_final.wav", peak_db=-3), 17.2 - 0.33)     # どん: カット6(17〜21秒)
place(load("generated/light_anime_stableaudio_1.wav", gain_db=-8), 31.0 - 0.01)     # 灯り: カット9(28〜33秒)、戸の向こう

# ぬめが動くときの「ぷに」。1本から、ほかと重ならない4音を切り出し、順に替えて置く。
step = load("generated/nume_step_anime_stableaudio_2.wav", peak_db=-9)
def pop(t, length=0.15):
    a = int(SR * (t - 0.01)); b = a + int(SR * length)
    y = step[:, a:b].copy()
    f = int(SR * 0.03)
    y[:, -f:] *= np.linspace(1, 0, f)
    return y
pops = [pop(t) for t in (0.09, 0.86, 2.65, 3.29)]
moves = [
    4.5, 4.9,          # カット2(4〜7秒): 葉から顔を出す
    7.1, 7.45,         # カット3(7〜10秒): 石に登る。8秒の「……んしょ」の前
    8.6,               # カット3: 登りきる
    33.2, 33.55, 33.9, # カット10(33〜36秒): 石を降り、葉の下へ入る
]
for k, t in enumerate(moves):
    place(pops[k % len(pops)], t)

# BGM: 曲の頭から使う。声より平均で約15dB 小さくし、台詞の間はさらに6dB 下げる。
if bgm_file:
    bgm = load(bgm_file)[:, :mix.shape[1]]
    bgm *= 10 ** (-32 / 20) / np.sqrt(np.mean(bgm ** 2))
    duck = np.ones(bgm.shape[1], dtype=np.float32)
    for a, b in [(7.8, 9.2), (16.8, 20.8)]:  # ぬめ「……んしょ」、どんの台詞
        i, j, r = int(SR * a), int(SR * b), int(SR * 0.3)
        duck[i - r:i] = np.minimum(duck[i - r:i], np.linspace(1, 0.5, r))
        duck[i:j] = 0.5
        duck[j:j + r] = np.minimum(duck[j:j + r], np.linspace(0.5, 1, r))
    bgm *= duck
    f = int(SR * 1.0)
    bgm[:, :f] *= np.linspace(0, 1, f)
    place(bgm, 0.0)

# 頭は0.3秒で立ち上げ、カット10の暗転に合わせて最後の1.5秒で消す。
fi, fo = int(SR * 0.3), int(SR * 1.5)
mix[:, :fi] *= np.linspace(0, 1, fi)
mix[:, -fo:] *= np.linspace(1, 0, fo)

peak = np.abs(mix).max()
if peak > 0.98:
    mix *= 0.98 / peak
sf.write(out, mix.T, SR)
print(out, f"{LENGTH:.0f}s, peak {20*np.log10(np.abs(mix).max()):.1f} dBFS")
