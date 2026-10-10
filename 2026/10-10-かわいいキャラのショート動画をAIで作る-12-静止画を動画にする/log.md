---
date: 2026-10-10
title: 静止画を動画にする
issue: 21
parent: 1
ai:
minutes:
result:
status: 未公開
url:
qiita_url:
---

## 試したこと

清書した静止画(#19)を、動画生成AIで動かす。
同じ静止画と指示で、動画生成AIを2つ以上比べる。
成果物はカットごとの動画、採用した方、比較メモ。

### 手法の選定

時間の上限は60分。

動きの大きさで作り方を分ける。「線の少なさ」が画風の芯なので、線を変えずに済む動きはAIに渡さない。

- 小さい動き: Python で層を動かす。AIは使わない。
  - カット1、5: 湯気の層を横に流す。
  - カット4、7: 触角を数度ずつ揺らす(#19 の `antenna.py`)。
  - カット8の鼻を沈める動き: どんを下げ、湯を上げる。
- 大きい動き: 動画生成AIに始点と終点の絵を渡し、間を埋めさせる。
  - カット2(葉の裏を3回なめる)、3(石に登る)、10(石を降りて葉の下へ)。
  - カット8の口の開け閉めは、Python でできなければAIに回す。
  - 終点の絵は #19 の `compose.py` で位置と角度を変えて作る。
- 作らない: カット6はカット5の使い回し。カット9は編集で背景を重ねる。

始点だけ渡す方式は見送った。動きの行き先がAIまかせになり、#19 で2匹の比率・向き・触角が外れたのと同じことが起きやすいため。

### 比べるAI

比較はカット3と10で行う。60分で2カットずつ比べられる数として、2つに絞った。

- Hugging Face 上の Wan 2.2。Space は `multimodalart/wan-2-2-first-last-frame`。Claude Code から MCP(AIに外部の道具をつなぐ仕組み)経由で呼ぶ。
  - 制限は Space が使う共有GPU(ZeroGPU)の時間にかかる。MCP でもブラウザでも同じ枠を使う。
  - 無料は1日数分、PRO(月9ドル)は1日25〜40分(資料で数字が違う)。1本で60〜90秒使う見込み。
  - まず無料で試し、良ければPROにする。PROなら大きい動き4カット×数回でも1日で収まる見込み。
  - 心配は解像度。速さのため480p前後で出すSpaceが多い。静止画は768×1376。
  - モデルと Space の作者の、両方の使用条件を確かめる。
- Veo(Google)。元の絵が Gemini 系なので、相性を見る。勝手に付く音は捨てる。

Kling は見送った。10-03 で画風の上書きが強かったため、比較の相手は Veo にした。

### 比べるAIを組み直す(Higgsfield)

試したかったのは Hugging Face ではなく、Higgsfield(複数の動画生成AIをまとめて使えるサービス)の MCP だった。上の案を組み直した。

- Hugging Face の MCP は接続まで済んだ。分かったことは2つ。
  - `multimodalart/...` は MCP 非対応だった(404)。MCP 対応版は `mcp-tools/wan-2-2-first-last-frame`。
  - 絵は公開URLで渡す必要がある。手元のファイルは直接渡せない。
  - 今日は使わない。接続は残す。
- Higgsfield の MCP は公式。1つの接続で Veo 3.1、Kling 3.0、Seedance 2.0 などを呼べる。動画は最長15秒、縦長も出せる。
- 始点と終点の両方を渡せるのは Kling 3.0 と Seedance 2.0 / 2.5。Veo 3.1 は始点だけ。
- 費用は有料プランのクレジット。MCP からは無制限枠の対象外で、毎回クレジットを使う。Kling 3.0 は5秒・720pで約7クレジット。
- 比較: Kling 3.0 と Seedance に、カット3と10の始点と終点を渡す。指示文と絵を揃える。
- Veo は始点だけになるため比較から外す。時間が余れば参考に1本作る。
- 10-03 で「まとめサービス経由は規約を確かめられないので、決定稿は公式で作る」と決めた。Higgsfield はまとめサービスにあたる。今日は比較まで行い、採用するカットの規約は公開前に確かめる。

始点と終点の絵:
- カット10: 始点は `py-cut09.png`(石の上のぬめ)、終点は `py-cut10.png`(葉の下へ入りかけ)。新しく作らない。
- カット3: 終点は `py-cut03.png`(登りきった姿)。始点(段差の前で触角を下げたぬめ)を Python で作る。

見る点:
- 線が増えたり、コマごとに揺れたりしないか。
- ぬめの比率と向きが守られるか。
- 跳んで見える、ウサギに見える、の崩れ(#19 で起きた)が出ないか。
- 解像度。1本の生成時間と、使ったクレジット。

順番: 接続 → カット3の始点の絵 → 2つのモデルで生成 → 比較 → 残りの大きい動きの作り方を決める → 時間が残れば小さい動き。
Issue では小さい動きを先にする予定だった。接続でつまずいても比較の時間を残すため、比較を先にした。

### Higgsfield をやめ、Hugging Face の無料枠に戻す

- Higgsfield の MCP は接続できた。アカウントは無料プランで、残り10クレジットだった。
- 9:16・5秒・音なしの料金を問い合わせた。Kling 3.0 は7.5、Seedance 2.0 は22.5、Seedance 2.5(720p)は35クレジット。10クレジットでは Kling が1本だけ。
- 比較(2カット×2モデル×2回)には約120クレジット要る。有料プランが前提になる。
- 費用をかけない方針にして、Higgsfield をやめた。Hugging Face の無料枠(ZeroGPU)で作る。
- 絵は GitHub の main にある静止画を、raw の公開URLで渡す。

## 結果

### カット10(Wan 2.2、始点と終点)

- Space: `mcp-tools/wan-2-2-first-last-frame`。Claude Code から MCP の `dynamic_space` で呼んだ。
- 始点 `py-cut09.png`、終点 `py-cut10.png`(#19)。長さ3秒。段数8、禁止の指示文は既定のまま。
- 指示文: "Flat 2D cartoon animation at night. A small pale slug-like creature slowly slides down off the flat stone to the left and creeps under the big leaf in the lower left. The capybara in the hot water stays still with its eyes open. Static camera. Keep the same simple thick black outlines and flat colors as the input images. Steam drifts gently."
- 結果: `assets/generated/wan-cut10-1.mp4`。コマの並び: `assets/work/wan-cut10-1-strip.png`、`wan-cut10-1-f24-34.png`。
- 出力は480×864、16コマ/秒、3.06秒。静止画(768×1376)より小さい。
- 1回目で通った。費用は0。
- 良かった点:
  - 背景、石、葉、湯気の線と色は崩れなかった。線の太さも保たれた。
  - ぬめは石の上を左へ滑り、石の前の面を降りて葉の手前に着いた。始点から終点まで、つながって動いた。
- 崩れた点:
  - 石を降りる約0.5秒(24〜30コマ目)で、ぬめに脚のような2本の垂れが出た。体も縦に伸び、ウサギに見えた。#19 と同じ崩れ。
  - 降りる途中で、水筒が消えた。
  - どんの目が、途中で半円から丸い目(白い光つき)に変わった。最後は半円に戻る。

### カット10の2回目(指示文を直す)

- 1回目の崩れ3つを、指示文と禁止の指示文で抑えられるかを見た。シードは1回目と同じ1177087716に固定した。
- 指示文に足したこと: 脚がない、豆型の低い体のまま滑る、水筒を背負ったまま、どんの目は半円のまま。
  - "A small pale slug with no legs glides slowly like a slug, keeping its low rounded bean-shaped body pressed flat against the surface. ... Its round blue canteen stays on its back the whole time, strapped across its body. The capybara in the hot water does not move; its eyes stay the same half-closed half-circle shape."
- 禁止の指示文は、既定の中国語の文の後ろに足した。Wan は中国語の指示に従いやすいため。
  - 足した語: 腿、脚、四肢、兔子、身体拉长、跳跃、水壶消失、眼睛变圆、眼睛高光、表情变化。
- 結果: `assets/generated/wan-cut10-2.mp4`。コマの並び: `assets/work/wan-cut10-2-strip.png`、`wan-cut10-2-f18-40.png`。
- 直ったこと:
  - どんの目は、最後まで半円のままだった。
  - 水筒は、降りる間も背中に付いたままだった。
  - 脚のような垂れは出なかった。ウサギのような縦長も出なかった。
- 新しく出た崩れ:
  - 石を降りる約0.5秒(30〜38コマ目)で、ぬめが頭から縦に落ちるように見えた。水筒が上、顔が下になる。
  - 降りる間、触角が細い線になり、ほぼ消えた。体は丸い玉に見えた。
  - 降りる直前(30コマ目)に、触角が横へ長く伸びた。
- 崩れは0.5秒だけで、夜で暗く、ぬめも小さい。カット10はこの2回目で良しとして、カット3へ進んだ。

### カット3の始点の絵

- 終点は #19 の `py-cut03.png`(登りきった姿、触角70°)。
- 始点を Python で作った: `assets/generated/py-cut03-start.png`、作り方は `assets/scripts/cut03_start.py`。
  - ぬめは石の前の面のふもとで、右(石の側)を向く。触角は40°(前に倒す)。
  - 大きさと背景の切り出しは、終点と同じにした。
- Wan には公開URLで渡す必要がある。始点の絵は手元にしかないため、作業ブランチを途中で push した。「push は /publish でまとめる」の決まりから外れる。

### カット3(Wan 2.2、始点と終点)

- 始点 `py-cut03-start.png`、終点 `py-cut03.png`。長さ3秒、シード1177087716。
- 指示文と禁止の指示文は、カット10の2回目と同じ書き方にした。動きの部分だけ変えた。
  - "It first lowers its two antennae once, then slowly climbs up the front face of the stone like a slug, keeping its low rounded bean-shaped body pressed against the surface, and arrives on the top edge of the stone. ... It keeps facing right."
- 結果: `assets/generated/wan-cut03-1.mp4`。コマの並び: `assets/work/wan-cut03-1-strip.png`、`wan-cut03-1-grid.png`。
- 良かった点:
  - 背景は動かず、線と色も保たれた。
  - 登る前に、触角を顔の前へ垂らす動きが出た(8〜16コマ目)。絵コンテの「触角を一度下げる」に合う。
  - 水筒は最後まで付いていた。登った後、石の上を右へ滑って終点の姿に収まった。
- 崩れた点:
  - 登る約0.75秒(20〜32コマ目)で、ぬめが縦に立ち上がった。体が伸び、触角は上へまっすぐ立ち、ウサギに見えた。#19 と同じ崩れ。
  - 石の上の角を越える所で、体が宙に浮き、跳んで見えた。
  - 4コマ目あたりで、顔に黒い鼻のような点が出た。

## 学び
