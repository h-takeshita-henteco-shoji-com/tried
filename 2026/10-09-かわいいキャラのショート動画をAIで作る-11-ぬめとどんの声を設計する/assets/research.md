# ボイスデザインの調べもの

#20 で思った声が出なかった。原因が説明文の書き方か、AIの限界かを分けたい。
そのため、説明文の書き方とAIごとの癖を20分で調べた。

## 結論

- 説明文は「属性を短く並べる」型が効く。物語風の長文は効きにくい。
- 「性別を決めない」「とても遅く」は、説明文では効きにくい項目らしい。
- 「声の質」と「台詞の読み方」は分けて作る。声は説明文で、読み方は台詞側の記号や指示で寄せる。
- 同じ説明文でも毎回違う声が出る。書き直す前に、同じ文で数回作り直す。
- 良い声が出たら、その声を元にクローンして使い回す。毎回説明文から作ると、声がぶれる。

## 説明文の型

### ElevenLabs の公式の型

公式ガイドは、次の順で書く型を勧めている。

```
Native [言語]. [性別], [年齢]. [音質]. Persona: [2〜5語]. Emotion: [形容詞]. [声色・速さ・話し方を1〜2文]
```

- 言語と地域は最初に書く。書かないと、なまりがずれる。
- 「accent」の語は抑揚の説明に使わない。「emphasis」や「delivery」を使う。
- 「reverb」「echo」「phone」など音響効果の語は、音質を落とす。
- 試し読みの文は、声の性格に合わせる。
- Guidance Scale(説明文にどれだけ従うか)を上げると説明に忠実になる。下げると音質が上がる。

### Qwen3-TTS の型

Qwen3-TTS(Alibaba の音声生成AI。手元で動かせる)は、説明文を `instruct` という欄に入れる。

- 声を作る専用のモデルがある(`Qwen3-TTS-12Hz-1.7B-VoiceDesign`)。
- 日本語を含む10言語を話せる。ライセンスは Apache-2.0。
- 説明文は中国語か英語が確実とする記事がある。日本語の説明文で良い声が出たという記事もある。
- 効く項目は、性別・年齢・高さ・速さ・感情・声色・性格。なまりは効きにくい。
- 説明文を盛りすぎると壊れる。「鼻にかかった声」で、聞き取れない声になった例がある。
- 有名人の名前は使えない。性質で書く。
- 台詞の句読点は全角(。、?!)にする。

## AIごとの癖

- ElevenLabs: 長く具体的な説明ほど良い。性別は書くか、高さで言い換える。
- Qwen3-TTS: 毎回違う声が出る。気に入るまで同じ文で作り直す。落ち着いた低い声は、中国語なまりが残りやすい。
- Qwen3-TTS: 高く元気な声は、なまりが出にくい。

## #20 の説明文を見直す

#20 の説明文は、キャラの物語と禁止事項が多い。調べた型と比べると、次の点がずれている。

- 「冬を何度も越えたカピバラ」は、声の属性ではない。AIは声に変換できない。
- 「性別は決めない」は、どのAIも苦手。高さと声色で言い換える。
- 「〜しない」の禁止が多い。AIは否定を拾いにくい。ほしい性質を肯定で書く。
- 「答える前に間を置く」は、声の質ではなく読み方。台詞側で「……」や読点で作る。

## 出典

- [Qwen3-TTS(GitHub)](https://github.com/QwenLM/Qwen3-TTS)
- [ElevenLabs Voice Design ガイド](https://elevenlabs.io/docs/product-guides/voices/voice-design)
- [Qwen3-TTSで声を作った体験(気球人、note)](https://note.com/kikyujin/n/n59b9077d6aec)
- [Qwen3-TTS の日本語を M3 Mac で試す(DEV Community)](https://dev.to/tumf/qwen3-tts-surprised-by-the-quality-of-japanese-on-apple-silicon-m3-creating-rights-free-voices-k1d)
- [Qwen3 TTS Voice Design Prompting Guide(voicecreator.pro)](https://voicecreator.pro/blog/voice-prompting-guide)
