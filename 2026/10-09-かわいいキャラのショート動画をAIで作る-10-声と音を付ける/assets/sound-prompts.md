# 音の指示文

## 方針

- 音は3つ作る。湯の音、遠くで戸の閉まる音(カット1)、灯りの消える音(カット9)。
- 人は音だけで出す(10-06 世界観設定書)。声や足音は入れない。戸とスイッチの音だけにする。
- どれも「遠く」「小さく」を基本にする。この回は、台詞が無いことで伝える回のため。
- 指示文は日本語の版と英語の版を用意する。効果音を作るAIは英語のほうが通りやすいことがある。
- 結果は `generated/yu_elevenlabs_1.mp3` のように、音の名前・AI・回数で名前を付ける。
  - 湯の音: `yu`、戸の音: `door`、灯りの音: `light`

## 湯の音(全カット)

動画は35秒。作れる長さに上限があるAIでは、短く作ってつなぐ。
つなぎ目が分からないよう、変化の少ない音にする。

日本語の版:

```
ぬるい温泉の湯だまり。湯口から細く湯が流れ込み、静かにちょろちょろと鳴る。ときどき小さな泡がはじける。夕方の屋外で、風はない。音楽や人の声は入れない。
```

英語の版:

```
A small, quiet outdoor hot spring pool at dusk. A thin trickle of warm water flowing in, soft continuous gurgling, an occasional tiny bubble. No wind, no music, no voices. Calm, steady, loopable.
```

### 書き直した版(Stable Audio Open 用)

上の英語の版は、Stable Audio Open でほぼ無音(1秒ごとの音量が -62dB 前後)になった。
「quiet」「calm」「no wind」と静かさを重ねたためだと考え、水の音を前に出して書き直した。

```
Close-up field recording of warm water trickling and gurgling into a small stone hot spring pool. Gentle steady stream of water, soft splashing, small bubbles popping. Natural outdoor ambience at dusk. No music, no voices.
```

## 遠くで戸の閉まる音(カット1)

日本語の版:

```
離れた建物の中で、木の引き戸がゆっくり閉まる音。カラカラと滑って、最後にコトンと小さく当たる。遠く、こもって聞こえる。人の声や足音は入れない。
```

英語の版:

```
A wooden Japanese sliding door slowly closing inside a distant building. Soft rolling slide, then a small gentle thud at the end. Far away and muffled. No voices, no footsteps.
```

## 灯りの消える音(カット9)

絵コンテでは「スイッチか、戸の閉まる音」。両方を作って選ぶ。
戸の音はカット1と同じになるので、スイッチを先に試す。

日本語の版(スイッチ):

```
戸の向こうの部屋で、古い壁のスイッチを1回だけ切る音。カチッと短く小さい。遠く、こもって聞こえる。そのあとは静か。人の声は入れない。
```

英語の版(スイッチ):

```
A single click of an old wall light switch being turned off, in a room behind a closed door. Short, small, far away and muffled. Silence after. No voices.
```

## アニメ向けの版(Stable Audio Open 用)

写実的な版は、どれも現実的すぎた。アニメで使うので、大げさで聞き分けやすい音にする。リアリティーは要らない。

- 「cartoon」「anime」の効果音だと書く。Stable Audio Open は効果音サイト(Freesound)の音で学習していて、cartoon の札の音が多い。
- 1音ずつはっきり鳴らす。響き(リバーブ)は付けない。
- 英語の擬音語(plip、plop、tok、click)で、音の形を伝える。
- 「遠く」「こもった」は外す。戸の音の遠さは、あとで音量を下げて出す。

湯の音(36秒):

```
Cartoon sound effect, anime style. Cute bubbling water: clear, round plip plop bubble pops, one by one, with a light trickling stream underneath. Exaggerated, playful, crisp and close. Dry, no reverb. No music, no voices.
```

戸の音(3秒):

```
Cartoon sound effect, anime style. A Japanese wooden sliding door: a quick exaggerated swoosh slide, then one clear hollow wooden tok at the end. Punchy, crisp, easy to recognize. Dry, no reverb. No music, no voices.
```

灯りの音(2秒):

```
Cartoon sound effect, anime style. A single exaggerated light switch click, a bright crisp plastic click, then silence. Punchy and clear. Dry, no reverb. No music, no voices.
```

### アニメ向けの湯の音を、流れの音に替えた版

泡の「ぽこっ」が、ぬめの「ぷに」と被って聞き分けにくい。
粒のない、低く途切れない流れの音にする。ぬめの「ぷに」は高い音なので、高さでも分ける。

```
Cartoon sound effect, anime style background. A smooth, continuous, gentle flow of warm water into a small pool: soft low steady pouring, mellow and round. No bubbles, no drips, no pops, no splashes. Simple, warm, cozy, even and constant. Dry, no reverb. No music, no voices.
```

## ぬめが動くときの音(カット2・3・10)

ぬめは台詞がほとんどない。動きに音が付くと、どこで何をしているかが伝わる。
ナメクジには足がないので、足音ではなく、柔らかく弾む「ぷに」にする。
1本に4回入れて作り、あとで1音ずつ切り出して動きに合わせて置く。鳴らし続けはしない。

```
Cartoon sound effect, anime style. Tiny cute squishy steps of a small soft jelly creature: four soft, bouncy, rubbery puni puni boing pops, evenly spaced with short silence between. High pitched, adorable, gentle. Dry, no reverb. No music, no voices.
```

## BGM

入れるかどうかを、音を並べてから決める。
声と音を絵コンテの秒数どおりに置いた仮組みを作り、聞いて判断する。
