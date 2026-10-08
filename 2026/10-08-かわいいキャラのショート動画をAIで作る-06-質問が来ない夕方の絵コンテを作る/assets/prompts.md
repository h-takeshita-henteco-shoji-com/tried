# 絵コンテのラフの指示文

`storyboard.md` の10カットを、ラフの絵にする。
清書(背景つき、比率を守った静止画)は #19 で作る。今日はコマ割りと向きが分かればよい。

## 送り方

- 窓口は Gemini。10-07 で、どんの向きを変える絵が Nano Banana Pro では止まり、Gemini では通ったため。
- 2枚に分ける。A はカット1〜5、B はカット6〜10。1枚に10コマ入れると、コマが小さくなりすぎるため(10-05 で8枠が 512px に縮んだ)。
- 添付は `input/nume-anchor.png` と `input/don-anchor.png` の2枚。キャラの形の手本として使う。
- 気持ちの言葉は書かない。向きと形だけを書く(10-05、10-07 の学び)。
- 結果は `generated/gemini_A1.png` のように、シートと回数で名前を付ける。

## A. カット1〜5

```
Make a rough storyboard sheet: 5 tall vertical panels (9:16 each) in one row, numbered 1 to 5 above each panel. Simple sketch style: black pencil lines on white, light grey tone only, no color, no text inside the panels.

Characters (use the two attached images only as shape references):
- Nume: a small slug with a dome-shaped body and two thick antennae with round tips.
- Don: a large capybara with a folded towel on its head, relaxing in a hot spring. Only its head is above the water.
- Size: Don's head is about 3 times as tall as Nume's body.

Setting in every panel: the edge of a small outdoor hot spring pool. The water is on the right side. A flat stone sits on the left edge of the pool. Steam drifts from the right.

Panel 1: wide shot. Don's head in the water at the lower right, facing the viewer. The flat stone on the left is empty. Steam drifting.
Panel 2: close-up of the edge of a large butterbur leaf. Nume peeks out from under the leaf. Its antennae point forward and down.
Panel 3: Nume climbs a small step up onto the flat stone. Its antennae are lowered.
Panel 4: medium shot. Nume on the flat stone at the left, Don's head in the water at the right. Nume's body faces left, away from Don. Nume's antennae point forward and down, toward the left edge of the panel.
Panel 5: close-up of Don's head above the water, facing the viewer, eyes half-closed. One wisp of steam.
```

## B. カット6〜10

```
Make a rough storyboard sheet: 5 tall vertical panels (9:16 each) in one row, numbered 6 to 10 above each panel. Simple sketch style: black pencil lines on white, light grey tone only, no color, no text inside the panels.

Characters (use the two attached images only as shape references):
- Nume: a small slug with a dome-shaped body and two thick antennae with round tips.
- Don: a large capybara with a folded towel on its head, relaxing in a hot spring. Only its head is above the water.
- Size: Don's head is about 3 times as tall as Nume's body.

Setting: the edge of a small outdoor hot spring pool. The water is on the right side. A flat stone sits on the left edge of the pool.

Panel 6: close-up of Don's head above the water, facing the viewer, mouth slightly open.
Panel 7: close-up of Nume from behind, sitting on the flat stone. Its antennae point forward and down, toward the left. We see its back, not its face.
Panel 8: close-up of Don's head. Mouth closed. Only the nose tip is lowered into the water, so the water line touches the nose.
Panel 9: wide shot, same layout as a wide view of the pool: Nume on the flat stone at the left, Don's head in the water at the right. The sky is dark grey, like night.
Panel 10: night. Nume crawls down from the stone toward a large butterbur leaf at the far left. Don's head faces toward the leaf, eyes open.
```

## 1回目の結果

- A: `generated/絵コンテ1/gemini_1.jpeg`。B: `generated/絵コンテ1/gemini_2.jpeg`。
- ぬめの露が全コマで消えた。指示文で、ぬめを「ドーム形の体と触角」とだけ書き、露を書き落とした。
- ぬめの触角は「前に倒す」が効かず、まっすぐ立った(4、9)。
- 2はぬめの顔に眉が足され、困り顔になった。
- 4はぬめがどんに背を向けているか読めない。7は背中から見た絵のはずが、顔が下に出て形が崩れた。
- 5は湯気が口から出て、たばこの煙に見える。
- 10はぬめが葉の方へ動いていない。
- 狙いどおり: 8の鼻を沈めた顔、10のどんの開いた目、比率(約3倍)。

## 先に、水筒つきのぬめを固める(N1〜N4)

ラフ A2、B2 より先に送る。参照画像に露が残ったまま文章で水筒を足すと、AIは画像に引っぱられ、コマごとに水筒の形も揺れるため。
10-05 の学び「一貫性は1枚のアンカーで取る」に従う。

- 窓口は Gemini。添付は1枚だけ(10-07 で、2枚添付すると土台を取り違えたため)。
- 1枠ずつ 1024px で作る(10-05 で8枠を1枚にしたら 512px に縮んだため)。
- N1 → N2〜N4 の順。N2〜N4 は N1 の結果だけを添付する。
- ラフで必要なのは正面と後ろ。斜めと横は時間が余れば作る。

### N1. 正面の決定稿(添付: input/nume-anchor.png)

```
Same slug character as the attached image. Do not redesign it. Keep exactly: the dome-shaped body with the wavy bottom edge, the flat matte body color, the two thick antennae with round tips and their different lengths, the two black dot eyes, the short straight line mouth, the thick bold black outline of even width, flat fills with no shading, and the plain background #F4F1EC.

Change only one thing: remove the round water drop behind the body on the upper right. Delete it completely.

Add a canteen instead. A small round flat canteen, about one quarter of the body width, flat light blue fill, thick black outline, a tiny cap on top. It hangs on Nume's back, so from the front only its upper half peeks out from behind the upper right edge of the body outline. A thin strap runs diagonally across the front of the body, from the upper right edge down to the lower left edge, drawn as two thin parallel black lines with a flat light brown fill. The strap does not cover the eyes or the mouth.

No eyebrows, no blush, no text. Front view, centered, square frame.
```

### N2. 後ろ(添付: N1 の結果)

```
Same slug character as the attached image. Do not redesign it. Keep the body shape, body color, antennae, thick black outline, flat fills and the plain background #F4F1EC.

Draw it from directly behind. No face is visible: no eyes, no mouth. Both antennae are seen from behind.
The round canteen is fully visible in the middle of its back, with the tiny cap on top. The strap runs from the canteen over the right shoulder of the dome and disappears around the left side.

No text. Square frame, centered.
```

### N3. 斜め(添付: N1 の結果、時間が余れば)

```
Same slug character as the attached image. Do not redesign it. Keep the body shape, body color, antennae, eyes, mouth, thick black outline, flat fills and the plain background #F4F1EC.

Turn the whole body 45 degrees to the left: the face moves toward the left side of the body, and both eyes are still visible. The canteen on the back now shows more, peeking out from behind the right side of the body. The strap crosses the front of the body diagonally.

No eyebrows, no text. Square frame, centered.
```

### N4. 横(添付: N1 の結果、時間が余れば)

```
Same slug character as the attached image. Do not redesign it. Keep the body shape, body color, antennae, thick black outline, flat fills and the plain background #F4F1EC.

Side view, facing left. One eye and the mouth are near the left end of the body. The body is a long low dome. The canteen sits on the top of the back, near the right end, fully visible from the side, with the strap running down the side of the body.

No eyebrows, no text. Square frame, centered.
```

## 2回目(A2、B2): 水筒を足し、崩れたコマを直す

- 露をやめ、丸い水筒を紐で斜めがけにする(本人の判断)。理由は `../log.md`。
- 添付は2枚。ぬめは `input/nume-canteen-front-back.png`(N1 の正面と N2 の後ろを Python で横に並べた1枚)、どんは `input/don-anchor.png`。古い `nume-anchor.png` は添付しない。
- 参照画像の露は名指しで消す。10-07 で「〜にする」より「〜を消す」が効いたため。N1 を使えば不要だが、残しておく。
- 触角は「前に倒す」をやめ、角度と指す先で書く。
- 顔は「点の目2つと短い直線の口だけ。眉なし」を両方のシートに書く。

### A2. カット1〜5

```
Make a rough storyboard sheet: 5 tall vertical panels (9:16 each) in one row, numbered 1 to 5 above each panel. Simple sketch style: black pencil lines on white, light grey tone only, no color, no text inside the panels.

Characters (use the two attached images only as shape references; the Nume image shows its front view on the left and back view on the right):
- Nume: a small slug with a dome-shaped body and two thick antennae with round tips. Its face is only two dot eyes and one short straight line mouth. No eyebrows. Remove the round water drop on its back from the reference. Instead, Nume always wears a small round canteen on its back, hung on a thin strap that crosses its body diagonally. The canteen is visible in every panel where Nume appears.
- Don: a large capybara with a folded towel on its head, relaxing in a hot spring. Only its head is above the water. No eyebrows.
- Size: Don's head is about 3 times as tall as Nume's body.

Setting in every panel: the edge of a small outdoor hot spring pool. The water is on the right side. A flat stone sits on the left edge of the pool. A large butterbur leaf grows at the far left. Steam rises from the water surface only.

Panel 1: wide shot. Don's head in the water at the lower right, facing the viewer. The flat stone on the left is empty. Steam rising from the water.
Panel 2: close-up of the edge of the butterbur leaf. Nume peeks out from under the leaf, with the canteen on its back. Both antennae lean forward, almost horizontal, pointing to the left.
Panel 3: Nume climbs a small step up onto the flat stone. Both antennae bend down, touching the stone.
Panel 4: medium shot from behind Nume. Nume sits on the flat stone in the lower left, seen from the back: we see the dome back, the canteen and the strap, not its face. Both antennae lean forward, almost horizontal, pointing to the left edge of the panel. Don's head is in the water at the right, behind Nume, facing the viewer.
Panel 5: close-up of Don's head above the water, facing the viewer, eyes half-closed. One wisp of steam rises from the water surface beside its head, not from its mouth.
```

### B2. カット6〜10

```
Make a rough storyboard sheet: 5 tall vertical panels (9:16 each) in one row, numbered 6 to 10 above each panel. Simple sketch style: black pencil lines on white, light grey tone only, no color, no text inside the panels.

Characters (use the two attached images only as shape references; the Nume image shows its front view on the left and back view on the right):
- Nume: a small slug with a dome-shaped body and two thick antennae with round tips. Its face is only two dot eyes and one short straight line mouth. No eyebrows. Remove the round water drop on its back from the reference. Instead, Nume always wears a small round canteen on its back, hung on a thin strap that crosses its body diagonally. The canteen is visible in every panel where Nume appears.
- Don: a large capybara with a folded towel on its head, relaxing in a hot spring. Only its head is above the water. No eyebrows.
- Size: Don's head is about 3 times as tall as Nume's body.

Setting: the edge of a small outdoor hot spring pool. The water is on the right side. A flat stone sits on the left edge of the pool. A large butterbur leaf grows at the far left.

Panel 6: close-up of Don's head above the water, facing the viewer, mouth slightly open.
Panel 7: close-up of Nume seen from directly behind, sitting on the flat stone. We see only the dome back, the canteen and the strap. No face is visible. Both antennae lean forward, almost horizontal, pointing to the left.
Panel 8: close-up of Don's head. Mouth closed. Only the nose tip is lowered into the water, so the water line touches the nose.
Panel 9: wide shot. Nume on the flat stone at the left, seen from behind, antennae pointing to the left. Don's head in the water at the right. The sky is dark grey, like night.
Panel 10: night. The flat stone is empty. Nume crawls on the ground at the far left, halfway under the butterbur leaf, moving away from the pool; we see its back and the canteen. Don's head at the right turns toward the leaf, eyes open.
```
