# 指示文 v1(1周目: ぬめの正面アンカー)

4ツールに同じ本文を渡し、正面1枚ずつ作って画風を比べるための指示文。
本文は英語版を正とし、4ツールすべてに英語版を渡す。日本語版は、時間が余ったら Nano Banana と GPT Image にだけ追加で渡し、日本語理解の差を見る。
ツール固有の設定は末尾にだけ足す。本文は変えない。

## 決めたこと(設定書からの追加)

- 1周目は主人公のぬめだけ。どんは、ぬめの画風が決まってから同じ画風で作る。
- 目は体の前面に置く小さな点にする。触角の先に目を置く案(現実のナメクジに近い)は、1周目で形が外れたときの代案にする。
- 基本の表情は「少し心配そう」。触角を少し前に傾けて出す。
- 背中に露のしずくを1粒乗せる。運ぶ物があると役割が絵で伝わる。
- 色は `palette.png` の値で固定する。体 #CFC8BE、輪郭 #8E867C、露 #DCEBF2、背景 #F4F1EC。苔の緑 #7FB069 は場面の絵で使い、アンカーには入れない。
- 「ゆるさ」は触角の長さを左右で少し変えることで出す。

## 本文(英語版、正)

```
Subject:
An original 2D illustrated mascot character based on a slug. Full body, front view, facing the viewer.

Shape:
The body is one short, round, bean-like lump. No taper, no separate head, no arms, no legs, no shell.
The flat underside rests on the ground.
Two antennae rise from the top of the body. They are large relative to the body. The two antennae are slightly different in length. Both tilt slightly forward, as if a little worried.

Face:
Two tiny black dot eyes on the front of the body. No pupils, no highlights, no eyelashes.
A very small, simple mouth drawn as a short line. No blush on the cheeks.

Color:
The body is one flat matte color, #CFC8BE. No pattern, no spots, no gradient.
Thin outline in #8E867C.
One small dew drop, #DCEBF2, sits on the back of the body.
Plain solid background, #F4F1EC.

Style:
Flat 2D illustration with solid color fills. Minimal or no shading. Clean, slightly hand-drawn outline. Simple shapes that read clearly as a small silhouette. Quiet and understated mood.

Composition:
The character is centered, fills about two thirds of the frame, square image. Nothing else in the frame.

Do not include:
No big eyes, no shiny eyes, no blush, no slime, no wet glossy sheen, no breathing hole, no mottled texture, no fabric, no stitches, no plush or costume look, no 3D render, no photorealism, no text, no watermark, no shell, no other characters, no props other than the single dew drop.
```

## 本文(日本語版、追加実験用)

```
主題:
ナメクジをモチーフにした、2Dイラストのオリジナルマスコットキャラクター。全身、正面、こちらを向いている。

形:
体は豆のように短く丸い、ひとつの塊。先細りにしない。頭と胴を分けない。腕も脚も殻もない。
平らな底面が地面に接している。
体の上から2本の触角が伸びる。触角は体に対して大きい。2本の長さは少し違う。どちらも少し前に傾き、少し心配そうに見える。

顔:
体の前面に、小さな黒い点の目が2つ。瞳もハイライトもまつ毛もない。
ごく小さい口を短い線で描く。頬の赤みはない。

色:
体は #CFC8BE の一色、マットな平塗り。模様、斑点、グラデーションはない。
輪郭線は #8E867C の細い線。
背中に #DCEBF2 の露のしずくが1粒乗っている。
背景は #F4F1EC の無地。

画風:
平塗りの2Dイラスト。陰影はないか最小限。清潔で、少し手描き感のある輪郭線。小さなシルエットでも判別できる単純な形。静かで控えめな雰囲気。

構図:
キャラクターを中央に置き、画面の3分の2ほどの大きさ。正方形。他には何も置かない。

含めないもの:
大きな目、光る目、頬の赤み、粘液、濡れた光沢、呼吸孔、まだら模様、布、縫い目、ぬいぐるみや着ぐるみの質感、3D、写実、文字、透かし、殻、他のキャラクター、露のしずく以外の小道具。
```

## ツール別の末尾と設定

### Nano Banana(Gemini)

- Gemini アプリのモデルは Flash(3.6 Flash)を選ぶ。Flash と Pro では画像生成に Nano Banana 2 が使われる。Flash-Lite は Nano Banana 2 Lite になり、参照画像の複数指定と繰り返し編集ができないため使わない。
- 本文をそのまま貼る。参照画像は渡さない。
- 画像サイズは正方形。
- 無料枠なら透かしが入る。比較用はそれで良い。決定稿は有料枠で作り直す。
- 1回に1枚しか出ないので、同じ本文を4回送って4枚得る。

### GPT Image(ChatGPT)

- 本文をそのまま貼る。参照画像は渡さない。
- 正方形、高品質。
- 1回に1枚なので、4回送る。「同じ指示で別案を」と頼むと前の絵に寄るため、新しいチャットで送る。

### Midjourney

- 本文の改行を取り、1行にして `/imagine` に貼る。先頭の `Subject:` などのラベルは残して良い。
- 末尾に `--niji 7 --ar 1:1 --s 100` を足す。1回で4枚出る。
- 時間があれば `--v 7 --ar 1:1 --style raw --s 50` でも1回出し、niji との差を見る。参照画像でキャラを固定する `--oref` は v7 でしか使えないため、2周目で Midjourney を使うなら v7 に切り替える。

### Stable Diffusion 3.5 Medium(Draw Things)

- Positive: 本文をそのまま貼る(ラベルも残す)。
- Negative: `photorealistic, 3D render, glossy, wet, slime, big eyes, blush, plush, fabric, stitches, snail shell, text, watermark, cluttered background, extra limbs`
- 設定: 1024x1024、steps 30、CFG 4.5、sampler は既定、seed は `20261003` で固定して開始。良い絵が出たら seed を控える。
- 4枚出す。seed を 1 ずつ増やす。

## 保存の約束

- 画像は `assets/images/round1/<ツール名>.png` に置く(実際の置き方に合わせて変更)。
- 各ツールで使った本文のバージョン(v1)、設定、seed を `log.md` の結果欄に書く。
- 直した指示文は v2、v3 と番号を上げ、このファイルの末尾に差分を書く。
