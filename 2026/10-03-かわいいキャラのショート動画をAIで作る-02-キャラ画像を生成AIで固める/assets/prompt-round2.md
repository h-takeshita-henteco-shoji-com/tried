# 指示文 v2(2周目: 体は Kling、顔は GPT Image)

1周目の4枚から「体は Kling 3.0、表情は GPT Image 2.5」を採ることになった。
2周目は、2枚を参照画像として渡して合成する方法を主にし、文章だけの v2 を予備にする。
アンカーが決まったら、同じチャットで三面図と表情シートを作る。

## 決めたこと

- 体: Kling の「ドーム型で、下に向かって広がり、底の縁が柔らかく波打って地面に接する」形を採る。Kling の太い黒線、光沢、泣き顔、汗2粒は採らない(仮定。太い線も好みなら追加で試す)。
- 顔と触角: GPT Image の「点目2つ、短い直線の口、太くて先が丸い大きな触角、左右で長さが違う」を採る。
- 向きは正面のまま。採った2枚がどちらも正面だったため。
- 1周目の反省を反映する3点。触角の形を文章で決める。露は「背中の上の丸い水玉」と位置と形で書く。心配そうな気持ちは触角の向きだけで出し、顔では出さない。
- 色は v1 と同じ。体 #CFC8BE、輪郭 #8E867C、露 #DCEBF2、背景 #F4F1EC。

## A. 参照合成(主): Nano Banana Pro または GPT Image

画像を2枚添付する。1枚目 `images/round1/kling3.0.png`、2枚目 `images/round1/gptimage2.5sunburst.png`。
新しいチャットで送る。

```
Create one new character design by combining two reference images. This is an original 2D illustrated mascot based on a slug.

From image 1, take ONLY the body silhouette: a soft dome that widens toward the bottom, with a gently wavy base resting flat on the ground. Do not take anything else from image 1: no thick black outline, no gloss or highlights, no sad face, no tears, no sweat drops.

From image 2, take the face and the antennae: two tiny black dot eyes with no highlights, a short straight-line mouth, and two large thick antennae with rounded tips, roughly the same thickness from base to tip, slightly different in length. Both antennae tilt slightly forward. The face itself stays neutral; the worried feeling comes only from the antenna direction.

Color: body is one flat matte color #CFC8BE with no pattern or gradient. Thin outline #8E867C. One round dew drop #DCEBF2 sits on top of the back, drawn as a round bead, not a teardrop. Plain solid background #F4F1EC.

Style: flat 2D illustration, solid fills, minimal or no shading, clean slightly hand-drawn outline, quiet understated mood.

Composition: full body, front view, centered, the character fills about 60% of a square frame. Nothing else in the frame.

Do not include: big eyes, shiny eyes, blush, slime, wet sheen, breathing hole, mottled texture, fabric, stitches, plush or costume look, 3D, photorealism, text, watermark, shell, other characters, any prop other than the single dew drop.
```

直しの送り方(同じチャットで続ける):

```
Keep the same character. Change only [直す点]. Keep the body shape, face, antennae, colors, outline, and background exactly the same.
```

## B. 文章のみ(予備): v1 からの差分

参照合成がうまくいかないとき、または他ツールでも同条件で見たいときに使う。v1 の本文のうち、次の段落を差し替える。

```
Shape:
The body is one soft dome-shaped lump that widens toward the bottom. The base is gently wavy and rests flat on the ground. The body is about 1.3 times wider than it is tall. No taper, no separate head, no arms, no legs, no shell.
Two large, thick antennae rise from the top of the body. Each antenna is like a thick finger with a rounded tip, roughly the same thickness from base to tip. The two antennae are slightly different in length. Both tilt slightly forward. The worried feeling comes only from the antenna direction.

Face:
Two tiny black dot eyes on the front of the body. No pupils, no highlights, no eyelashes.
A very small, straight-line mouth. The face is neutral. No blush.

Color:
(v1 と同じ。露の行だけ差し替え)
One round dew drop, #DCEBF2, sits on top of the back, drawn as a round bead, not a teardrop.

Composition:
The character is centered and fills about 60% of a square frame. Nothing else in the frame.
```

## C. アンカー確定後: 三面図と表情シート

アンカーを添付し、同じチャットで送る。表情は顔ではなく触角だけで出す、という設定書の方針をここで試す。

```
Same character as the reference image. Do not redesign the character.

Make a character sheet on a plain #F4F1EC background, two rows, evenly spaced, no text and no labels.

Top row, four views of the same character: front view, three-quarter view, side view, back view. Same size in every view.

Bottom row, four expressions of the same character, front view. Show each feeling ONLY by the direction of the two antennae. The eyes and mouth stay exactly the same in all four:
1. worried: both antennae tilt forward
2. content: both antennae stand up and lean slightly apart
3. tired: both antennae droop sideways
4. startled: both antennae stand straight up

Same art style, same flat colors, same thin outline, same dew drop on the back. No shading, no gloss, no slime, no blush, no shell.
```

## 保存と記録

- 2周目の画像は `assets/images/round2/` に、ツール名と連番で置く。例: `nanobanana-pro-01.png`、`gptimage-01.png`、`sheet-01.png`。
- 使った方式(A か B か)、ツール、何回目の直しかを `log.md` の結果欄に書く。
- A と B の両方を試せたら、参照画像の有無で何が変わったかを1行書く。記事の材料になる。
