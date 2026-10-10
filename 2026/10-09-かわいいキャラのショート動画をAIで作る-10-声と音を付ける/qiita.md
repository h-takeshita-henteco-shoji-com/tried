---
title: Stable Audio Open を Mac で動かし、アニメ向けの効果音を作る(指示文・被り対策・仮組み)
tags: [StableAudioOpen, diffusers, Python, 効果音, AppleSilicon]
---

キャラクターのショート動画(36秒、台詞2つ)に付ける効果音を、Stable Audio Open 1.0 で作りました。経緯と試行錯誤はnoteに書いています。
https://note.com/tried_hs/n/n8b230afc8c98

この記事では、手元の Mac で Stable Audio Open を動かし、アニメ向けの効果音として使える形に仕上げるまでの手順と工夫を扱います。

## 結論

- Stable Audio Open 1.0 は、Apple M5・メモリ16GBの Mac で、diffusers から MPS で動いた。1本の生成は100段で約3分。ただし、そのままでは最後の段で止まるので、2か所の修正が要った。
- 指示文は、雰囲気の言葉より、鳴っている音そのものを書くほうが効いた。
  - `quiet`、`calm` を重ねると、静かな音ではなく、ほぼ無音(-62dB 前後)になった。
  - アニメ向けには `Cartoon sound effect, anime style.` と書き、擬音語(plip、tok、click)と `Dry, no reverb.` を添えると、1音ずつ立った乾いた音になった。
- 効果音どうしの被りは、音の「粒の形」と「高さ」を分けて避けた。
  - 粒のある湯の泡と、キャラの動く音(短く弾む音)が被った。湯を、粒のない流れの音に替えた。
  - 指示文の `low` は効かず、高さはローパスフィルター(2kHz)で下げた。
- 短い効果音は、1本に数回鳴らして作り、1音ずつ切り出して使い回した。
- 音は単独では選べなかった。絵コンテの秒数どおりに並べた仮組みを、Python で作って聞き比べた。数値は手がかりにとどまり、最後は耳で決めた。

## 環境

- MacBook(Apple M5、メモリ16GB)、macOS 26.6.2
- Python 3.12(uv の venv。Docker は使っていない)
- torch 2.14.1(MPS)、diffusers 0.39.0、transformers 4.57.3、torchsde 0.2.6、scipy 1.18.1、librosa
- モデル: `stabilityai/stable-audio-open-1.0`(float32)

```bash
uv venv --python 3.12 ~/.venvs/tried-audio
VIRTUAL_ENV=~/.venvs/tried-audio uv pip install diffusers transformers torchsde soundfile librosa scipy
```

Docker を使わなかったのは、Mac の Docker の中からは MPS(GPU)が使えないためです。CPU だけでは、1本の生成がかなり遅くなります。

モデルは gated(利用規約への同意が必要)です。Hugging Face のモデルページで同意し、読み取り用のトークンでログインしておきます。ライセンスは Stability AI Community License で、年間売上100万ドル未満なら商用でも無料です。

## 1. Mac で動かす

### 基本の呼び出し

```python
import torch, soundfile as sf
from diffusers import StableAudioPipeline

pipe = StableAudioPipeline.from_pretrained(
    "stabilityai/stable-audio-open-1.0", torch_dtype=torch.float32).to("mps")
audio = pipe(prompt, negative_prompt="Low quality, music, melody, speech, voices, singing.",
             num_inference_steps=100, audio_end_in_s=4.0,
             generator=torch.Generator("cpu").manual_seed(1)).audios[0]
sf.write("out.wav", audio.T.float().cpu().numpy(), pipe.vae.sampling_rate)  # 44.1kHz ステレオ
```

- 長さは `audio_end_in_s` で決める。最大47秒なので、36秒の湯の音を、つながずに1本で作れた。
- 生成時間は、長さにほとんどよらなかった。2秒の音も36秒の音も、1本150〜220秒。
- float16 は試していない。MPS の float16 は NaN が出やすいという報告が多いので、最初から float32 にした。メモリには収まった。
- `negative_prompt` には、音楽と人の声を入れた。効果音に旋律や声が混ざるのを避けるため。

### そのままでは最後の段で止まる

上のままだと、最後の段で `RecursionError` になりました。

```text
UserWarning: Should have ta>=t0 but got ta=... and t0=....
 90%|█████████ | 9/10 [00:14<00:01,  1.66s/it]
  File ".../scheduling_cosine_dpmsolver_multistep.py", line 662, in step
    noise = self.noise_sampler(self.sigmas[self.step_index], self.sigmas[self.step_index + 1]).to(
  ...
RecursionError: maximum recursion depth exceeded
```

スケジューラ `CosineDPMSolverMultistepScheduler` は、ノイズを足す部品 `BrownianTreeNoiseSampler` を `[sigma_min, sigma_max] = [0.3, 500]` の範囲で作ります。ところが10段のときの sigma は、両端で範囲の外に出ていました。

```text
[500.0001, 219.2738, 96.162, 42.1716, 18.4943, 8.1106, 3.5569, 1.5599, 0.6841, 0.3, 0.0]
```

2つの修正を、入れる・入れないで組み合わせた結果です(10段、2秒の音)。

| sigma を範囲内に収める | `final_sigmas_type` | 結果 |
|---|---|---|
| なし | `"zero"`(既定) | 最後の段で `RecursionError` |
| あり | `"zero"`(既定) | 出力が全部 NaN(最後の段で壊れる) |
| なし | `"sigma_min"` | 出力が全部 NaN |
| あり | `"sigma_min"` | 正常 |

両方を入れたコードです。ライブラリは書き換えず、スクリプトの中で差し替えています。

```python
import diffusers.schedulers.scheduling_dpmsolver_sde as sde
from diffusers import CosineDPMSolverMultistepScheduler

# 1. sampler に渡す sigma を、作成時の範囲に収める
_orig_init = sde.BrownianTreeNoiseSampler.__init__
def _init(self, x, sigma_min, sigma_max, seed=None, transform=lambda x: x):
    _orig_init(self, x, sigma_min, sigma_max, seed, transform)
    self._lo, self._hi, self._x = float(sigma_min), float(sigma_max), x
def _call(self, sigma, sigma_next):
    clamp = lambda s: min(max(float(s), self._lo), self._hi)
    a, b = clamp(sigma), clamp(sigma_next)
    if a == b:
        return torch.randn_like(self._x)
    t0, t1 = self.transform(torch.as_tensor(a)), self.transform(torch.as_tensor(b))
    return self.tree(t0, t1) / (t1 - t0).abs().sqrt()
sde.BrownianTreeNoiseSampler.__init__ = _init
sde.BrownianTreeNoiseSampler.__call__ = _call

# 2. 最後の sigma を 0 ではなく sigma_min(0.3)で止める
pipe.scheduler = CosineDPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config, final_sigmas_type="sigma_min")
```

最後の sigma が 0.3 で止まるので、理屈の上ではわずかにノイズが残ります。今回の効果音では、聞いて分かる差はありませんでした。CUDA 環境で同じことが起きるかは確かめていません。

## 2. 指示文: 写実からアニメへ

作った音は3つです。湯の音(全編)、遠くで戸の閉まる音、戸の向こうで灯りの消える音。

### 静かさを重ねると、無音になる

最初の湯の音の指示文です。

```text
A small, quiet outdoor hot spring pool at dusk. A thin trickle of warm water flowing in, soft continuous gurgling, an occasional tiny bubble. No wind, no music, no voices. Calm, steady, loopable.
```

2本作り、どちらも1秒ごとの音量が -61〜-68dB でした。ほぼ聞こえません。
`quiet`、`calm`、`No wind` と静かさを重ねたためと見て、水の音を具体的に書き直しました。

```text
Close-up field recording of warm water trickling and gurgling into a small stone hot spring pool. Gentle steady stream of water, soft splashing, small bubbles popping. Natural outdoor ambience at dusk. No music, no voices.
```

音量の中央が -49〜-51dB まで上がりました。

### アニメ向けの書き方

聞ける音にはなりましたが、どれも本物の録音のような音でした。アニメでは浮くうえに、小さく鳴ると何の音か分かりません。
そこで、次の4点を指示文に入れました。

- 頭に `Cartoon sound effect, anime style.` と書く。学習元の Freesound には、cartoon の札の付いた効果音が多い。
- 英語の擬音語で、音の形を伝える(`plip plop`、`swoosh` と `tok`、`click`)。
- `Dry, no reverb.` で響きを消す。
- `far away`、`muffled` は外す。遠さは、あとで音量で作る。

戸の音の例です。

```text
Cartoon sound effect, anime style. A Japanese wooden sliding door: a quick exaggerated swoosh slide, then one clear hollow wooden tok at the end. Punchy, crisp, easy to recognize. Dry, no reverb. No music, no voices.
```

測った結果です(各2本)。

| 音 | 写実の版 | アニメの版 |
|---|---|---|
| 湯 | 最大 -15dB、泡が下地に埋もれる | 最大 -4dB 前後。下地はほぼ同じで、泡が1秒に5〜6回立つ |
| 戸・灯り | 遠く、こもった音 | 短く大きく鳴ったあと、-70〜-98dB の無音。響きが残らない |

## 3. 効果音どうしの被りを避ける

### 被りに気づいたのは、並べたとき

キャラ(ナメクジ)が動くときの音を足しました。足がないので、足音ではなく、柔らかく弾む音です。

```text
Cartoon sound effect, anime style. Tiny cute squishy steps of a small soft jelly creature: four soft, bouncy, rubbery puni puni boing pops, evenly spaced with short silence between. High pitched, adorable, gentle. Dry, no reverb. No music, no voices.
```

単独では良い音でした。ところが仮組みに入れると、アニメ版の湯の泡と混ざって聞き分けられません。どちらも短く弾む、粒のような音だったためです。

### 粒の形を分ける

湯を、粒のない流れの音に替えました。

```text
Cartoon sound effect, anime style background. A smooth, continuous, gentle flow of warm water into a small pool: soft low steady pouring, mellow and round. No bubbles, no drips, no pops, no splashes. Simple, warm, cozy, even and constant. Dry, no reverb. No music, no voices.
```

0.1秒ごとの音量の上下の幅(上位10%と下位10%の差)で、粒のなさを見ました。

| 音 | 上下の幅 | 音の重心(spectral centroid) |
|---|---|---|
| アニメ版の湯(泡あり) | 50dB | 約3.3kHz |
| 流れの音 1本目 | 15dB | 約6.7kHz |
| 流れの音 2本目 | 51dB | 約9.0kHz |
| 流れの音 3本目 | 13dB | 約6.9kHz |
| キャラの動く音 | — | 約11kHz |

1本目と3本目は、途切れない音になりました。

### 高さは、指示文ではなく加工で分ける

指示文の `low` は効かず、3本とも前の音より高くなりました。キャラの動く音(約11kHz)に近づいています。
高さは、scipy のローパスフィルターで下げました。

```python
from scipy.signal import butter, sosfiltfilt
yu = sosfiltfilt(butter(4, 2000, "low", fs=SR, output="sos"), yu, axis=1)
```

音量は、1秒ごとの音量の中央が -55dB になるようにそろえました。下地の音は、平均より中央でそろえるほうが、たまに出る強い音に引っ張られません。

### 最後は仮組みで、耳で決める

3本とも同じ加工をかけ、それぞれで仮組みを作って聞き比べました。選んだのは2本目です。
数値では、ときどき強い音が出るので(上下の幅 51dB)、一番被りそうに見えた1本でした。数値で分かるのは粒の有無と高さまでで、被るかどうかは聞くまで分かりませんでした。

## 4. 1本から、短い音を切り出して使い回す

キャラの動く音は、全部で8か所に置きます。8本作る代わりに、1本(4秒)に数回鳴らして作り、1音ずつ切り出しました。

音の始まりは librosa で拾いました。

```python
on = librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=True, delta=0.2)
```

選んだ1本では、10か所が拾えました。そのうち、前後と重ならず、強さが十分な4つ(0.09、0.86、2.65、3.29秒)を使いました。
切り出しは、始まりの0.01秒前から0.15秒ぶん。最後の0.03秒で音量を0にして、切り口の「プツッ」という音を消しています。

```python
def pop(t, length=0.15):
    a = int(SR * (t - 0.01)); b = a + int(SR * length)
    y = step[:, a:b].copy()
    f = int(SR * 0.03)
    y[:, -f:] *= np.linspace(1, 0, f)
    return y
pops = [pop(t) for t in (0.09, 0.86, 2.65, 3.29)]
for k, t in enumerate(moves):
    place(pops[k % len(pops)], t)  # 同じ音が続かないよう、4音を順に替える
```

## 5. 絵コンテの秒数どおりに並べる(仮組み)

音は単独では選べないので、毎回、絵コンテの秒数どおりに並べた仮組みを作って聞きました。
動画は36秒。声は別の回に作ったもの(24kHz モノラル)なので、44.1kHz ステレオにそろえてから足しています。

音量の置き方です。

| 音 | 置き方 |
|---|---|
| 声 | 一番大きい所を -3dB にそろえる |
| キャラの動く音 | 一番大きい所を -9dB(声より6dB 小さく) |
| 戸(遠く) | 生成した音から -12dB |
| 灯り(戸の向こう) | 生成した音から -8dB |
| 湯(下地) | 1秒ごとの中央を -55dB |
| BGM | 平均を -32dB(声より約15dB 小さく)。台詞の間はさらに6dB 下げる |

BGM の台詞の間だけ下げる処理(ダッキング)は、前後0.3秒で滑らかに下げ・戻しています。

```python
duck = np.ones(bgm.shape[1], dtype=np.float32)
for a, b in [(7.8, 9.2), (16.8, 20.8)]:  # 台詞の区間(秒)
    i, j, r = int(SR * a), int(SR * b), int(SR * 0.3)
    duck[i - r:i] = np.minimum(duck[i - r:i], np.linspace(1, 0.5, r))
    duck[i:j] = 0.5
    duck[j:j + r] = np.minimum(duck[j:j + r], np.linspace(0.5, 1, r))
bgm *= duck
```

BGM は生成ではなく、フリーBGMサイト OpenTracks(旧 DOVA-SYNDROME)の曲を使いました。音源ファイルの再配布は禁止なので、曲と、曲の入った仮組みは公開リポジトリに置いていません。

## うまくいかなかったこと

- 声のAI(Qwen3-TTS の VoiceDesign)に環境音を頼んだ。説明に効果音の指示文、台詞に擬音語(「ちょろちょろ……ぽこっ」)を渡すと、擬音語を読み上げた声になった。音のある所の98%に、話し声の高さ(約300Hz)があった。
- 静かさを重ねた指示文は、無音になった(上の 2.)。
- `low` は効かず、加工で直した(上の 3.)。
- 数値で選ぼうとした湯の音は、耳で選んだ1本と逆だった(上の 3.)。

## コード

スクリプトと指示文は、リポジトリに置いています。

https://github.com/h-takeshita-henteco-shoji-com/tried/tree/main/2026/10-09-かわいいキャラのショート動画をAIで作る-10-声と音を付ける/assets

- `scripts/stable_audio.py`: Stable Audio Open で生成(修正入り)。指示文の組を引数で切り替える
- `scripts/rough_mix.py`: 声と効果音を絵コンテの秒数どおりに並べる。ローパス、切り出し、ダッキングもここ
- `scripts/qwen_ambient.py`: Qwen3-TTS に環境音を頼んだ試し
- `sound-prompts.md`: 使った指示文と、書き直した理由

効果音は Stable Audio Open で作りました(Powered by Stability AI)。
