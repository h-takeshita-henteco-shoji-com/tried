# 今日使った指示文(送った順)

ツールはすべて Nano Banana 2.0 Pro(Gemini)。1回目のみ GPT Image 2.5 でも同じ文を送った。
同じチャットで続けられなかったため、毎回新しいチャットに直前の結果を1枚添付して送った。

## 1. 合成(参照2枚: input/kling3.0.png、input/gptimage2.5sunburst.png)

前回の `prompt-round2.md` の A をそのまま使った。本文はそちらを参照。

## 2. 輪郭を太い黒線に変え、露を触角の間に置く(参照: nanobanana2.0pro.png)

```
Redraw the character in the attached image with the same design. Do not redesign it. This is an original 2D illustrated mascot based on a slug.

Keep exactly: the dome-shaped body that widens toward the bottom with a gently wavy base, two tiny black dot eyes, the short straight-line mouth, the two large thick antennae with rounded tips and slightly different lengths, the flat matte body color #CFC8BE, and the plain solid background #F4F1EC.

Change only two things.

1. Outline: draw the whole character with a thick, bold, solid black outline of even width, like the line in a clean cartoon sticker. Apply it to the body silhouette, both antennae, and the dew drop. Keep the dot eyes and the straight mouth as they are, in the same black.

2. Dew drop: one round dew drop #DCEBF2 sits on the top of the back, centered between the two antennae, drawn as a round bead, not a teardrop. It should read as sitting on top of the body, not as a sweat drop on the side.

Style: flat 2D illustration, solid fills, no shading, no gloss, no highlights, no tears, no sweat drops, no slime, no blush, no shell, no text. Full body, front view, centered, square frame, the character fills about 60% of the frame.
```

結果: 輪郭は成功。露は頭の上に玉を載せた形になり失敗。

## 3. 露を体の縁の後ろからのぞかせる(参照: nanobanana2.0pro_2.png) → 決定稿

```
Redraw the character in the attached image with the same design. Do not redesign it.

Keep exactly: the dome-shaped body with a gently wavy base, the thick bold black outline of even width, two tiny black dot eyes, the short straight-line mouth, the two large thick antennae with rounded tips and slightly different lengths, the flat matte body color #CFC8BE, and the plain solid background #F4F1EC.

Change only the dew drop. Remove the ball sitting on top of the head. Instead, draw one round dew drop #DCEBF2 resting on the back, behind the body, peeking out from behind the upper-right edge of the body silhouette. Only the upper half of the drop is visible; the lower half is hidden behind the body. The drop has the same thick black outline, a flat fill, and one small white oval highlight near its top-left. It is a round bead, not a teardrop, and not a sweat drop.

Style: flat 2D illustration, solid fills, no shading, no gloss on the body, no tears, no sweat drops, no slime, no blush, no shell, no text. Full body, front view, centered, square frame, the character fills about 60% of the frame.
```

結果: 成功。`nanobanana2.0pro_3.png` を決定稿にした。

## 4. 三面図と表情シート(参照: nanobanana2.0pro_3.png)

```
Same character as the attached image. Do not redesign the character.

Make a character sheet on a plain #F4F1EC background, two rows, evenly spaced, no text and no labels. Square 1:1 image.

Top row, four views of the same character: front view, three-quarter view, side view, back view. Same size in every view. In the three-quarter, side, and back views, the single round dew drop sits on top of the back. In the front view it peeks out from behind the upper-right edge of the body, as in the attached image.

Bottom row, four expressions of the same character, front view. Show each feeling ONLY by the direction of the two antennae. The eyes and mouth stay exactly the same in all four:
1. worried: both antennae tilt forward
2. content: both antennae stand up and lean slightly apart
3. tired: both antennae droop sideways
4. startled: both antennae stand straight up

Same art style: flat 2D illustration, flat matte body color #CFC8BE, thick bold black outline of even width, two tiny black dot eyes, short straight-line mouth, one round dew drop #DCEBF2 with a small white highlight. No shading, no gloss, no slime, no blush, no shell, no tears, no sweat drops.
```

結果: 構成と触角の向きは成功。心配と疲れの枠で顔に眉が足された。512px と小さい。

## 次回に向けた直し案

- 表情の枠は「worried」などの気持ちの言葉を書かず、触角の向きだけを書く。気持ちの言葉が顔に出る引き金になる。
- 1枚8枠ではなく、1枠ずつ 1024px で作って並べる。解像度と輪郭の太さを保てる。
