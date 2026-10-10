---
title: Qwen3-TTS VoiceDesignの声を、説明文を変えずに後処理で詰める(EQ・PSOLA・WORLD)
tags: [Qwen3-TTS, 音声合成, Python, Praat, WORLD]
---

キャラクター動画の声を Qwen3-TTS の VoiceDesign で作りました。経緯と試行錯誤はnoteに書いています。
https://note.com/tried_hs/n/n89ca44732228

この記事では、気に入った1本を「説明文を書き直さずに」仕上げた手順だけを扱います。

## 結論

- VoiceDesign は、説明文を変えると声の主ごと入れ替わる。気に入った1本が出たら、説明文はもう触らないほうがよい。
- 仕上げは後処理で行った。声の要素を1つずつ、ほかを変えずに動かせる。
  - 声の角(高い音の強さ): scipy の高域シェルフで削る
  - 高さ: Praat(parselmouth)の PSOLA で上げる。librosa の `pitch_shift` はエコーが出た
  - 抑揚: Praat の PSOLA で、ピッチ曲線の上下の幅だけを広げる
  - かすれ: WORLD(pyworld)で非周期成分だけを減らす
- 別の台詞を読ませるときは、**加工前**の音声を Base モデルでクローンし、出力に同じ加工をかける。
- Base モデルは、Mac では float32 で動かす必要があるという報告に従った。約7.8GBのメモリを使う。16GB機では、常駐している Docker などを止める必要があった。

## 環境

- MacBook(Apple M5、メモリ16GB)、macOS 26.6.2
- Python 3.12、torch 2.14.1(MPS)、transformers 4.57.3
- qwen-tts 0.1.1
  - `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`(float16)
  - `Qwen/Qwen3-TTS-12Hz-1.7B-Base`(float32)
- scipy 1.18.1、librosa 1.0.0、praat-parselmouth 0.4.7、pyworld-prebuilt 0.3.6.post1

```bash
uv venv --python 3.12
uv pip install qwen-tts soundfile praat-parselmouth pyworld-prebuilt
```

`pyworld` は、この環境ではビルド時のリンクで失敗しました。ビルド済みの `pyworld-prebuilt` なら入ります。import 名は `pyworld` のままです。

## 1. VoiceDesign で当たりを付ける

説明文は、属性を短く並べる型にしました(ElevenLabs の公式ガイドの型に沿った)。

```text
Native Japanese speaker. Elderly, androgynous voice, mid-low pitch. Timbre: soft, warm, slightly husky. Pace: very slow and relaxed. Volume: quiet, murmuring to oneself. Emotion: calm, sleepy, content.
```

```python
import torch, soundfile as sf
from qwen_tts import Qwen3TTSModel

m = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="mps", dtype=torch.float16)
for seed in [1, 2, 3]:
    torch.manual_seed(seed)
    wavs, sr = m.generate_voice_design(text=TEXT, instruct=INSTRUCT, language="Japanese")
    sf.write(f"don_B_{seed}.wav", wavs[0], sr)
```

同じ説明文でも、seed ごとに別の声が出ます。今回は seed=1 の1本を残しました。

### うまくいかなかったこと: 説明文で柔らかくする

残した1本は少し怖く聞こえました。そこで、説明文の2か所だけを書き換えました。

- `slightly husky` → `round and gently breathy`
- `calm, sleepy, content` → `kind, gentle, content, with a faint smile`

柔らかくはなりました。ただ、話し方の癖まで変わり、元の1本より悪くなりました。
seed を揃えても、説明文が違えば別の声になります。VoiceDesign の説明文は、声を微調整する道具としては使えませんでした。

## 2. 後処理で1要素ずつ動かす

元の音声は `don_B_1.wav` です。以下の加工は、どれも1つの要素だけを動かします。

### 声の角: 高域シェルフ

ローパスで分けた高域だけを下げ、元の低域に足し戻します。音量は RMS で揃えます。

```python
from scipy.signal import butter, sosfilt

def shelf(x, sr, fc, gain_db):
    lo = sosfilt(butter(2, fc, "low", fs=sr, output="sos"), x)
    return lo + (x - lo) * 10 ** (gain_db / 20)

y = shelf(x, sr, 4000, -4)
y *= np.sqrt(np.mean(x**2) / np.mean(y**2))
```

| 版 | 設定 | 結果 |
|---|---|---|
| soft1 | 4kHz以上を-4dB | 採用 |
| soft2 | 3kHz以上を-8dB | 不採用 |
| soft3 | 2.5kHz以上を-8dB、6kHz以上をさらに-10dB | 不採用 |

### 高さ: librosa ではなく PSOLA

最初は `librosa.effects.pitch_shift` で半音0.5〜1.5上げました。エコーが掛かったような声になりました。
`pitch_shift` は位相ボコーダで伸縮してから再標本化します。話し声では位相のずれが残響のように聞こえやすい、というのが見立てです。

Praat の PSOLA(重畳加算)に替えました。

```python
import parselmouth
from parselmouth.praat import call

snd = parselmouth.Sound(path)
m = call(snd, "To Manipulation", 0.01, 60, 400)
tier = call(m, "Extract pitch tier")
call(tier, "Multiply frequencies", snd.xmin, snd.xmax, 2 ** (steps / 12))
call([tier, m], "Replace pitch tier")
call(m, "Get resynthesis (overlap-add)").save(out, "WAV")
```

最終的には、高さは変えずに残しました。

### 抑揚: ピッチ曲線の幅だけを広げる

同じ Manipulation で、ピッチ点を対数(音程)の上で中央値から k 倍に引き伸ばします。平均の高さはほぼ保たれます。

```python
pts = [(call(tier, "Get time from index", i), call(tier, "Get value at index", i))
       for i in range(1, call(tier, "Get number of points") + 1)]
center = statistics.median(math.log(f) for _, f in pts)
call(tier, "Remove points between", snd.xmin, snd.xmax)
for t, f in pts:
    call(tier, "Add point", t, math.exp(center + (math.log(f) - center) * k))
```

k = 0.7、1.3、1.5、1.7、2.0、2.5、3.0、3.5 を作り、**3.0** を採用しました。
元の声がつぶやくような平らな抑揚だったため、大きめの倍率で自然に聞こえたのだと思います。

### かすれ: WORLD の非周期成分を減らす

WORLD で「F0・スペクトル包絡・非周期成分」に分け、有声区間の非周期成分だけを累乗して小さくします。F0 には小さなメディアンフィルタをかけ、震えの不揃いをならします。

```python
import pyworld as pw
from scipy.signal import medfilt

f0, t = pw.harvest(x, sr)
sp = pw.cheaptrick(x, f0, t, sr)
ap = pw.d4c(x, f0, t, sr)
v = f0 > 0
ap[v] = ap[v] ** 1.5          # 0〜1 の値なので累乗で小さくなる
f0[v] = medfilt(f0, 5)[v]
y = pw.synthesize(f0, sp, ap, sr)
```

WORLD は分解して組み立て直すだけで音が変わります。そのため、加工なし(累乗1.0、フィルタなし)で組み立て直した版も並べて比べました。今回は採用しませんでした。

## 3. 別の台詞を、同じ声と加工で読ませる

本番の台詞を読ませるため、`don_B_1.wav` を Base モデルでクローンしました。
渡すのは **加工前** の音声と、その文字起こしです。文字起こしを渡すと ICL モード(参照音声の続きとして生成するモード)になり、話し方も引き継がれやすくなります。

```python
m = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="mps", dtype=torch.float32)
prompt = m.create_voice_clone_prompt(ref_audio="don_B_1.wav", ref_text=REF_TEXT)
wavs, sr = m.generate_voice_clone(
    text="……んー。今日は、ぬるい寄りだな。", language="Japanese", voice_clone_prompt=prompt)
```

出力に、採用した加工(soft1 と抑揚3.0倍)を同じ順でかけます。
加工後の音声をクローン元にすると、加工の効果がどこまで残るかが読めません。加工前で声を写し、加工は最後にかけるほうが、台詞をまたいで揃えやすいと判断しました。

### うまくいかなかったこと: メモリ

1回目は、10分たっても1本も出ませんでした。

- Base モデル(float32): 約7.8GB
- Docker Desktop の仮想マシン: 8GB

この2つで、16GBのメモリとスワップがほぼ埋まっていました。
Docker のコンテナを止めただけでは、仮想マシンが確保したメモリは戻りませんでした。Docker ごと止めると、1本10秒前後で生成できました。

float16 にすれば、メモリは半分で済みます。ただ、Mac の Base モデルでは NaN が出るという報告があり、今回は試していません。

## コード

使ったスクリプトは、リポジトリに置いています。

https://github.com/h-takeshita-henteco-shoji-com/tried/tree/main/2026/10-09-かわいいキャラのショート動画をAIで作る-11-ぬめとどんの声を設計する/assets/scripts

- `design.py`: VoiceDesign で生成
- `soften.py`: 声の角を削る
- `pitch.py`: PSOLA で高さを変える
- `intonation.py`: 抑揚の幅を変える
- `husky.py`: WORLD でかすれを減らす
- `clone.py`: Base モデルでクローンして読ませる
- `finish.py`: 採用した加工をまとめてかける
