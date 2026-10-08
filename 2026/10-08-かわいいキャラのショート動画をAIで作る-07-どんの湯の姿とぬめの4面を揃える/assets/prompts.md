# 今日使う指示文(下書き)

窓口は Gemini。10-07 で、向きを変える絵が Nano Banana Pro では止まったため。
順番は D1 → D2 → N1 →(時間が余れば N2)。

前の回の学びを3つ入れた。

- 湯に沈む姿は「温泉に浸かる」で書く(10-07、1b でモデレーションを避けた書き方)。
- 添付は1枚にする。2枚添付すると、どちらを土台にするかをAIが取り違えた(10-07、3b-fix)。
- 持ち物の細部を文章で書く。10-08 は体だけ「変えない」と書き、水筒と紐が4枚で揃わなかった。

## ぬめの持ち物の決まり(N1、N2 で共通に使う)

色は 10-08 の正面と背面(`input/nume-canteen-front-back.png`)から測った。

- 水筒: 丸い平らな水筒。塗りは水色 #A6D4E1 の1色。光(白い反射)、水の線、帯は入れない。
- 口: 水筒の上に短い首と、小さな青灰色 #6E8B9B のふた。
- 紐: 細い平らな帯が1本。薄い茶色 #B3966C。太さは輪郭線の約2倍。輪、結び目、2本目は無い。
- 掛け方: 水筒は背中の上に乗る。紐は右肩から体を斜めに横切る。

## D1. どんの湯の姿・正面(参照: input/don-anchor.png のみ)

```
Edit this character. Keep the same capybara design exactly: the boxy rounded head, the flat matte fur color #A9927A, the darker rounded muzzle patch with two small black dot nostrils, the short straight line mouth, the eyes drawn as small black half-circles with a flat straight line on top, the small round ears, the crooked folded white towel with blue stripes on the head, the thick bold black outline of even width, flat 2D style with no shading, and the plain background #F4F1EC.

The capybara is now soaking in a warm hot spring bath, relaxing like capybaras do at Japanese onsen. The water comes up to its chin: the bottom of the muzzle patch just touches the water line, and no shoulders or body are visible. The water surface is one straight horizontal line across the whole frame, with a flat light blue fill #CFE6EE below it. A thin black outline where the head meets the water.

Exact front view, the head upright and level, centered. Both eyes, both ears, and the towel are visible. No steam, no ripples, no splashes, no text. Square frame, the head fills about 60% of the frame width.
```

## D2. どんの湯の姿・少し左を向く(参照: D1 の結果のみ)

左は葉の側。カット10で、どんが葉の方を向く顔に使う。
10-07 の斜めは、体が回らず顔だけ寄った。今回は頭しか無いので、見える形で回り方を書く。

```
Edit this image. Keep everything the same: the capybara design, colors, towel, thick black outline, the flat hot spring water up to its chin, the straight water line, and the background.

Change only the angle of the head: turn the head about 30 degrees toward the viewer's left. The muzzle patch moves to the left of the head's center and points left. The left eye is close to the left edge of the head and looks slightly smaller; the right eye is fully visible. The right ear is fully visible, the left ear is partly behind the head. The towel turns together with the head.

The head stays upright and level, and the chin stays at the water line. No steam, no ripples, no text. Square frame.
```

## N1. ぬめの真横を作り直す(参照: input/nume-canteen-front-back.png のみ)

10-08 の真横(`input/nume-side-old.jpeg`)は、水筒に水の線が入り、紐が輪になった。
直す元に古い真横を使わず、揃っている正面と背面の並びを土台にする。

```
The attached image shows the same slug character from the front (left) and from the back (right). Draw this same slug in an exact side view, facing the viewer's left. Do not redesign it. Keep exactly: the body shape, the flat body color #CAC0B4, the wavy foot edge, the two antennae with rounded tips, the tiny black dot eye, the short straight line mouth, the thick bold black outline of even width, flat 2D style with no shading, and the plain background #F4F1EC.

In side view, only one eye is visible, near the front of the body on the left. The mouth is a short line below and in front of the eye. Both antennae point up; the far antenna is partly behind the near one.

Canteen and strap. Draw these details exactly:
1. Canteen: one round flat canteen, filled with one flat light blue color #A6D4E1. No white highlight, no water line inside, no band around it.
2. Canteen top: a short neck and a small blue-gray cap #6E8B9B.
3. Position: the canteen sits on the top of the back, behind the antennae, on the right side of the body.
4. Strap: one single thin flat band, light tan brown #B3966C, about twice as thick as the black outline. It runs from the canteen diagonally down across the side of the body toward the front bottom. No loops, no knots, no second strap.

No text. Square frame, the whole character fills about 60% of the frame width.
```

## N2. ぬめの斜めを作り直す(参照: input/nume-canteen-front-back.png のみ・時間が余れば)

10-08 の斜め(`input/nume-angle-old.jpeg`)は、体が回らず顔だけ左へ寄った。紐が太く濃い茶色になった。
体の回り方を、見える形で書く。

```
The attached image shows the same slug character from the front (left) and from the back (right). Draw this same slug in a three-quarter view, with the whole body turned about 45 degrees toward the viewer's left. Do not redesign it. Keep exactly: the body shape, the flat body color #CAC0B4, the wavy foot edge, the two antennae with rounded tips, the tiny black dot eyes, the short straight line mouth, the thick bold black outline of even width, flat 2D style with no shading, and the plain background #F4F1EC.

The whole body turns, not only the face. The face is on the left part of the body. The left eye is close to the left edge of the body; the right eye is fully visible. More of the right side of the body is visible. The antennae turn together with the body.

Canteen and strap. Draw these details exactly:
1. Canteen: one round flat canteen, filled with one flat light blue color #A6D4E1. No white highlight, no water line inside, no band around it.
2. Canteen top: a short neck and a small blue-gray cap #6E8B9B.
3. Position: the canteen sits on the upper back, half visible behind the right side of the body.
4. Strap: one single thin flat band, light tan brown #B3966C, about twice as thick as the black outline. It runs diagonally across the front of the body, from the lower left to the canteen at the upper right. No loops, no knots, no second strap.

No text. Square frame, the whole character fills about 60% of the frame width.
```

## 1回目の結果(Gemini)

- D1 → `generated/gemini_1.jpeg`。正面、手ぬぐい、顔は決定稿のまま。湯はあごまで来ず、ほおの下まで体が出た。背景の線と湯の線が別々に2本ある。
- D2 → `generated/gemini_2.jpeg`。左を向いた。湯の中に体が透けて見える。鼻の縦線と「へ」の字の口が増えた(10-07 と同じ崩れ)。
- N1 → `generated/gemini_3.jpeg`。真横にならず、正面のまま。水筒と紐は決まりどおり(光なし、水の線なし、細い薄茶の1本)。
- N2 → `generated/gemini_4.jpeg`。体は回らず、目と口が少し左へ寄っただけ。水筒と紐は決まりどおり。

## D1b. 湯をあごまで上げる(参照: generated/gemini_1.jpeg のみ)

どんは頭と体がひと続きの形で、「あご」がどこかAIに伝わらない。画像の中の位置で書く。

```
Edit this image. Keep the capybara exactly as it is: the face, the eyes, the muzzle patch, the mouth, the ears, the towel, the colors, and the thick black outline. Keep the exact front view.

Change only the water.
1. Raise the water surface so that it is just below the bottom of the darker muzzle patch. The bottom edge of the muzzle patch almost touches the water line. Everything below that line is hidden.
2. The water is opaque, one flat light blue color #CFE6EE. Nothing is visible through the water.
3. There is only one horizontal line in the image: the water line. Remove the separate background line above it. The plain background #F4F1EC meets the water directly.

No steam, no ripples, no text. Square frame.
```

## D2b. 少し左を向く・顔の線を増やさない(参照: D1b の結果のみ)

D2 は向きは出たが、顔の線が増え、体が透けた。増えた線を名指しして禁じる。

```
Edit this image. Keep everything the same: the capybara design, colors, towel, thick black outline, the opaque flat water up to just below the muzzle patch, the single straight water line, and the background.

Change only the angle of the head: turn the head about 30 degrees toward the viewer's left. The muzzle patch moves to the left of the head's center. The left eye is close to the left edge of the head; the right eye is fully visible. The towel turns together with the head.

Keep the face exactly as simple as now: the eyes are small black half-circles with a flat line on top, the muzzle patch has only two small black dot nostrils and one short straight horizontal mouth line. No vertical line from the nose, no downturned mouth corners, no extra lines on the muzzle or cheeks.

The water is opaque. Nothing is visible below the water line. No steam, no ripples, no text. Square frame.
```

## N1b. 古い真横を土台に、水筒と紐だけ直す(参照: input/nume-side-old.jpeg のみ)

N1 は正面と背面の並びに引っぱられ、正面のまま描かれた。向きは古い真横がすでに正しい。
10-07 の 3b-fix2 と同じく、向きの合った1枚を直す形にする。

```
Edit this image. Keep the side view facing the viewer's left exactly as it is: the body shape, the body color, the wavy foot edge, the two antennae, the eye, the mouth, the thick black outline, and the background. Do not turn the character toward the viewer.

Change only the canteen and the strap. Draw these details exactly:
1. Canteen: keep its position and round shape on the top of the back, but fill it with one flat light blue color #A6D4E1. Remove the white highlight and the water line inside it. No band around it.
2. Canteen top: a short neck and a small blue-gray cap #6E8B9B.
3. Strap: replace the brown loops with one single thin flat band, light tan brown #B3966C, about twice as thick as the black outline. It runs from the canteen diagonally down across the side of the body toward the front bottom. No loops, no knots, no second strap.

No text. Square frame.
```

## 2回目の結果(Gemini)

- D1b → `generated/gemini_5.jpeg`。湯の線は少し上がったが、体は湯の手前に描かれ、沈んで見えない。線は2本のまま。
- D2b → `generated/gemini_6.jpeg`。湯が消え、全身の決定稿に横線が1本引かれただけ。ただし左を向いた顔は良い。鼻の縦線も「へ」の字も無く、決定稿の顔のまま。
- N1b → `generated/gemini_7.jpeg`。成功。真横のまま、水筒は水色1色で光も水の線も無い。紐は薄茶の1本で、輪が消えた。

## 湯は Python で重ねる

AIは2回とも、体を湯で隠せなかった。湯は平らな水色と1本の線なので、画像処理で描ける。
決定稿(`input/don-anchor.png`)と D2b の顔(`gemini_6.jpeg`)の、鼻のまわりのすぐ下(y=572)から下を湯で塗った。

- 正面 → `generated/don-bath-front.png`
- 左向き → `generated/don-bath-left.png`

## N2b. 真横から斜めへ回す(参照: generated/gemini_7.jpeg のみ・時間が余れば)

10-08 と N2 は、正面から回そうとして、ほとんど回らなかった。AIは回し足りない。
逆に真横から正面の側へ回せば、回し足りなくても斜めで止まるはず。

```
Edit this image. Keep the same slug design exactly: the body color, the wavy foot edge, the antennae with rounded tips, the tiny black dot eyes, the short straight line mouth, the thick black outline, the background, and the canteen and strap details (one flat light blue canteen #A6D4E1 with no highlight and no water line, a small blue-gray cap #6E8B9B, one single thin light tan strap #B3966C with no loops).

Change only the angle: turn the whole body about 45 degrees toward the viewer, so it becomes a three-quarter view facing the viewer's left. Now both eyes are visible: the near eye is fully visible, the far eye is close to the left edge of the body. The mouth is between the eyes, slightly to the left. Both antennae are visible side by side. The canteen is on the upper back, half visible behind the right side of the body. The strap runs diagonally across the front of the body, from the lower left up to the canteen.

No text. Square frame.
```

## N3. 背面の水筒から光を消す(参照: input/nume-back.png のみ・時間が余れば)

10-08 の背面だけ、水筒に白い光が入っている。ほかの3面に揃える。

```
Edit this image. Keep everything exactly as it is: the back view, the slug's body, the antennae, the canteen's position, shape, neck and cap, the strap, the thick black outline, and the background.

Change only the canteen fill: one flat light blue color #A6D4E1. Remove the white highlight. No water line, no band, no shading.

No text. Square frame.
```

## 3回目の結果(Gemini)

- N2b → `generated/gemini_8.jpeg`。成功。両目が左に寄って見え、斜めになった。水筒と紐は決まりどおり。触角は真横の重なり方のまま。
- N3 → `generated/gemini_9.jpeg`。成功。水筒の光が消え、水色1色になった。

## ぬめの4面

正面(10-08 の `正面.jpeg`)、斜め(N2b)、真横(N1b)、背面(N3)を Python で横に並べた。
→ `generated/nume-4views.png`
