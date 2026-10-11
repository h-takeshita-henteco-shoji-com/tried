---
title: Claude Code から Hugging Face MCP で Wan 2.2 FLF2V を呼び、キャラの静止画をスタイルを保ったまま動かす(first/last frame・キーフレーム)
tags: [ClaudeCode, HuggingFace, MCP, 動画生成AI, ffmpeg]
---

キャラクターのショート動画(36秒、10カット)の静止画を、動画生成AIで動かしました。経緯と試行錯誤はnoteに書いています。
https://note.com/tried_hs/n/nbe8d90eceaa0

この記事では、Claude Code から Hugging Face の MCP サーバー経由で Wan 2.2 の First-Last-Frame-to-Video(FLF2V)を呼び、スタイルを保ったまま動かす手順と、アーティファクトの抑え方を扱います。

## 結論

- Claude Code に Hugging Face MCP サーバーを接続すると、`dynamic_space` ツールで、MCP 対応の Space を事前登録なしで呼べた。Wan 2.2 FLF2V は `mcp-tools/wan-2-2-first-last-frame` で動いた。
- 入力画像は公開URLで渡す必要がある。GitHub の public リポジトリに push し、`raw.githubusercontent.com` のコミット固定URLを渡した。
- first frame と last frame の両方を渡すと、背景・線・色は、生成した8本すべてで保たれた。動画モデルにありがちな、モデル固有のスタイルへの上書きは起きなかった。
- プロンプトで直せたのは、パーツの有無や形だった(脚が生える、持ち物が消える、目の形が変わる)。ネガティブプロンプトに中国語で追記すると効いた。
- モーションそのもの(登り方、繰り返し回数)は、プロンプトでは直らなかった。中間のキーフレームを用意し、セグメントに分けて生成すると、そのセグメントは直った。
- ただし、側面視の「垂直面を登る」モーションは、キーフレームを追加しても、地面から壁面へ移る瞬間に「立ち上がる」形になった。
- 出力は 480×864・16fps。`duration_seconds` に n を渡すと、16n+1 フレーム(n+0.06秒)になる。

## 環境

- Claude Code(macOS、Apple M5)
- Hugging Face MCP サーバー(`https://huggingface.co/mcp`)
- Space: `mcp-tools/wan-2-2-first-last-frame`(Wan 2.2、diffusers のパイプライン)
- 入力画像: 768×1376(9:16)。黒の太い輪郭線とフラットな塗りの2Dイラスト。キャラはナメクジとカピバラ
- 確認と結合: ffmpeg 7.1(`imageio-ffmpeg` 同梱のバイナリ)

## 1. Claude Code に Hugging Face MCP を接続する

Hugging Face の [MCP 設定ページ](https://huggingface.co/settings/mcp) で「Claude Code」を選ぶと、コマンドが表示されます。

```bash
claude mcp add hf-mcp-server -t http "https://huggingface.co/mcp?login"
```

末尾の `?login` は OAuth でログインする方式です。トークンをコマンドに書かずに済みます。
Claude Code を再起動し、`/mcp` から hf-mcp-server を選んで認証します。

public リポジトリで作業している場合は、`--scope project` を付けないでください。付けると、設定がリポジトリの `.mcp.json` に書き込まれます。デフォルトの local スコープなら、`~/.claude.json` にだけ保存されます。

### Space を探して、パラメータを確認する

設定ページの「Dynamic Spaces」がオンなら、Space を設定ページに登録しなくても、`dynamic_space` で呼べます。

```json
{"operation": "discover"}
```

`discover` で、MCP 対応の Space の一覧が返ります。FLF2V の Space は `mcp-tools/wan-2-2-first-last-frame` でした。

注意点として、同名の `multimodalart/wan-2-2-first-last-frame` は MCP に対応していません。`view_parameters` を呼ぶと `HTTP 404` になりました。MCP 対応版は `mcp-tools/` の方です。

```json
{"operation": "view_parameters", "space_name": "mcp-tools/wan-2-2-first-last-frame"}
```

返ってきたパラメータです。

| パラメータ | 型 | デフォルト |
|---|---|---|
| `start_image_pil` | file URL | — |
| `end_image_pil` | file URL | — |
| `prompt` | string | — |
| `negative_prompt` | string | 中国語のネガティブプロンプト(下記) |
| `duration_seconds` | number | 2.1 |
| `steps` | number | 8 |
| `guidance_scale` / `guidance_scale_2` | number | 1 / 1 |
| `seed` | number | 42 |
| `randomize_seed` | boolean | true |

`negative_prompt` のデフォルトは、Wan 公式の例と同じ中国語のネガティブプロンプトです(`色调艳丽，过曝，静态，细节模糊不清，字幕，……`)。

## 2. 入力画像を公開URLで渡す

画像パラメータは `string (file URL)` で、公開された http(s) のURLしか受け付けません。ローカルファイルは直接渡せませんでした。

GitHub の public リポジトリに push して、raw URL を渡しました。

```text
https://raw.githubusercontent.com/<owner>/<repo>/<commit>/<path>
```

- ブランチ名ではなく、コミットハッシュで固定する。あとで画像を作り直しても、渡した画像が変わらない。
- パスにマルチバイト文字があれば、URLエンコードする(`urllib.parse.quote`)。
- 渡す前に `curl -sI <URL>` で `HTTP/2 200` を確認する。

Claude Code に依頼すると、`dynamic_space` の `invoke` が呼ばれます。

```json
{
  "operation": "invoke",
  "space_name": "mcp-tools/wan-2-2-first-last-frame",
  "tool_name": "wan_2_2_first_last_frame_generate_video",
  "parameters": {
    "start_image_pil": "https://raw.githubusercontent.com/.../py-cut09.png",
    "end_image_pil": "https://raw.githubusercontent.com/.../py-cut10.png",
    "prompt": "...",
    "duration_seconds": 3,
    "randomize_seed": false,
    "seed": 1177087716
  }
}
```

レスポンスは、Space 上の一時ファイルのURL(`.../gradio_api/file=/tmp/gradio/.../xxx.mp4`)と、使った seed です。URLは長くは残らないので、すぐに `curl -sL -o` で保存しました。

## 3. 結果の確認: フレームを並べる

動画は、再生するより、フレームを並べた方がアーティファクトに気づけました。

```bash
# 6フレームおきに9枚を横に並べる
ffmpeg -i in.mp4 -vf "select='not(mod(n\,6))',scale=240:-1,tile=9x1" -frames:v 1 strip.png
# キャラ周辺だけ crop して、2フレームおきに12枚
ffmpeg -i in.mp4 -vf "select='between(n\,18\,40)*not(mod(n\,2))',crop=300:400:0:400,tile=6x2" -frames:v 1 zoom.png
```

## 4. 1本目: スタイルは保たれ、キャラが崩れた

夜、ナメクジのキャラが石を降りて、葉の下へ入るカットです。first frame と last frame は、Python で合成した静止画です。

```text
Flat 2D cartoon animation at night. A small pale slug-like creature slowly slides down off the flat stone to the left and creeps under the big leaf in the lower left. The capybara in the hot water stays still with its eyes open. Static camera. Keep the same simple thick black outlines and flat colors as the input images. Steam drifts gently.
```

- 背景、石、葉、湯気の線と色は保たれた。線の太さも変わらなかった。
- 石を降りる約0.5秒で、ナメクジに脚のような突起が2本出て、体が縦に伸びた(ウサギのように見える)。
- 背中の水筒が、途中で消えた。
- カピバラの目が、途中だけ半円から丸い目(ハイライトつき)に変わった。

## 5. パーツの有無や形は、プロンプトで直る

seed を1本目と同じに固定し、プロンプトとネガティブプロンプトだけを変えました。

```text
Flat 2D cartoon animation at night. A small pale slug with no legs glides slowly like a slug, keeping its low rounded bean-shaped body pressed flat against the surface. It slides down off the flat stone to the left and creeps under the big leaf in the lower left. Its round blue canteen stays on its back the whole time, strapped across its body. The capybara in the hot water does not move; its eyes stay the same half-closed half-circle shape. Static camera. Keep the same simple thick black outlines and flat colors as the input images. Steam drifts gently.
```

ネガティブプロンプトは、デフォルトの中国語の文の後ろに追記しました。

```text
(デフォルトの文)，腿，脚，四肢，兔子，身体拉长，跳跃，水壶消失，眼睛变圆，眼睛高光，表情变化
```

(脚、足、四肢、ウサギ、体が伸びる、ジャンプ、水筒が消える、目が丸くなる、目のハイライト、表情の変化)

| アーティファクト | 1本目 | 2本目 |
|---|---|---|
| 脚のような突起・縦長 | 出た | 出ない |
| 水筒が消える | 消えた | 付いたまま |
| カピバラの目が丸くなる | 丸くなった | 半円のまま |
| 新しいアーティファクト | — | 降りる瞬間、頭から縦に落ちるように見える |

パーツの有無や形は、プロンプトで直りました。降り方は、別の崩れ方に変わっただけでした。

## 6. モーションは、キーフレームで決める

### 登るモーションで立ち上がる

ナメクジが石のふもとから、石の上に登るカットです。2本目と同じ書き方で、モーションの部分だけ変えました。

```text
... It first lowers its two antennae once, then slowly climbs up the front face of the stone like a slug, keeping its low rounded bean-shaped body pressed against the surface, and arrives on the top edge of the stone. ... It keeps facing right. ...
```

登る約0.7秒で、体が縦に伸び、触角がまっすぐ立ちました。ネガティブプロンプトに `站立`(立ち上がる)、`飞起来`(飛び上がる)を追記しても変わりませんでした。

### セグメントに分けて、結合する

中間のキーフレームを Python で作り、セグメントごとに生成して結合しました。

1. first frame → 中間キーフレーム(石の角を乗り越えかけた姿)、2秒
2. 中間キーフレーム → last frame、1秒

中間キーフレームは、体を15〜45°回転させて石の壁面に置く案も試しました。どれも石の前に浮いて見えたので、「体の前半が角に乗り、後ろが少し垂れる」姿にしています。

結合するときは、後ろのセグメントの先頭フレームを落とします。前のセグメントの最終フレームと同じ画像だからです。

```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
  "[1:v]trim=start_frame=1,setpts=PTS-STARTPTS[b];[0:v][b]concat=n=2:v=1[v]" \
  -map "[v]" -c:v libx264 -pix_fmt yuv420p out.mp4
```

3セグメントなら、2本目と3本目の両方の先頭フレームを落とします。つなぎ目は、フレームを並べても見分けにくい程度でした。

| 生成方法 | 中間→last frame | first frame→中間(登る所) |
|---|---|---|
| 1本で生成 | — | 約0.7秒、立ち上がる |
| 2セグメント(乗り越えかけ) | 立ち上がりもジャンプもなく、last frame に収まる | 約0.7秒、立ち上がる |
| 3セグメント(壁面に貼り付いた姿を追加) | 同上 | 地面から壁面へ移る約0.5秒、立ち上がる |

キーフレームで固定したセグメントは直りました。ただ、地面から垂直面へ移る瞬間は、キーフレームを追加しても「立ち上がる」形になりました。3セグメント版のプロンプトには `pressed flat against the stone like a sticker` と書いています。

## 7. first frame と last frame に同じ画像を渡す(ループするモーション)

その場で繰り返すモーション(葉の裏を3回なめる)は、first frame と last frame に同じ画像を渡しました。

```text
... Without moving its body from the spot, it tilts only its head up a little and licks the underside of the leaf with a tiny tongue, three times, then returns to the same pose. Its two antennae stay tilted forward. ...
```

- 体はその場にとどまり、最後は first frame と同じ姿に戻った。両端を同じ画像にする方法は、位置の固定に効いた。
- なめたのは1回だけだった。舌は葉の裏ではなく前方下へ出て、元の画像にない大きなピンクの舌が生成された。
- 「触角は前に倒したまま」も守られず、上に開いた。

回数と方向は、プロンプトでは制御できませんでした。このカットは、最終的に動画生成AIを使わず Python で作り直しています(noteを参照)。

## 8. 出力の仕様

| 項目 | 値 |
|---|---|
| 解像度 | 480×864(入力は 768×1376) |
| フレームレート / フレーム数 | 16fps。`duration_seconds` が1・2・3で、17・33・49フレーム |
| 長さ | 1.06秒・2.06秒・3.06秒 |
| 音声 | なし |

他のカット(Python で生成した 768×1376)と並べるときは、ffmpeg でアップスケールしました。

```bash
ffmpeg -i wan.mp4 -vf "scale=768:1376:flags=lanczos,fps=24,setsar=1" out.mp4
```

## うまくいかなかったこと

- `multimodalart/wan-2-2-first-last-frame` を MCP で呼んだ。MCP 非対応で `HTTP 404` だった(1.)。
- ネガティブプロンプトに `站立`(立ち上がる)を追記しても、登るモーションで立ち上がった(6.)。
- 中間キーフレームを、体を回転させて作った。15〜45°のどれも浮いて見えた(6.)。
- 「3回なめる」は1回になり、舌の方向も違った(7.)。

## コード

スクリプト、プロンプト、生成した動画は、リポジトリに置いています。

https://github.com/h-takeshita-henteco-shoji-com/tried/tree/main/2026/10-10-かわいいキャラのショート動画をAIで作る-12-静止画を動画にする/assets

- `scripts/cut03_start.py`、`scripts/cut03_mid.py`: カット3の first frame と中間キーフレームを生成する
- `prompts-cut03-split.md`: セグメントに分けたときのプロンプト
- `scripts/rough_cut.py`: 全カットをアップスケール・結合し、音声を付ける
- `generated/wan-*.mp4`: Wan 2.2 で生成した動画
