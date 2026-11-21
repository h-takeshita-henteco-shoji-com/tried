# social-sim

親テーマ #167「糸島の農業を社会学とAIで考える」で育てる、LLM で社会実験を回す土台です。
子00(#168)で作り、子01以降はルールと人物像の分布だけを差し替えて使います。
標準ライブラリだけで動きます(Python 3.12)。

## 動かし方

お金をかけずに配線を確かめるときは、でたらめに答える `dummy` を使います。

```bash
# 公共財ゲームを24人(6組)・10回、罰ありで回す。組み方は partner か stranger
python run.py game --llm dummy:0 --groups 6 --rounds 10 --punishment --matching partner

# 論文(reference/fg2000.json)と物差しごとに比べ、図にする
python compare.py runs/<日時>-game-partner-n runs/<日時>-game-partner-p --out runs/compare.json
uv run --with matplotlib python plot_compare.py runs/compare.json out.png

# 話し合いと減点の公共財ゲーム(#173、Bochet ほか 2006)。持ち点10・還元率0.4・4人組
python run.py game --llm dummy:0 --groups 6 --endowment 10 --punishment --rule bpp --chat 1,4,7   # チャット+減点
python run.py game --llm dummy:0 --groups 6 --endowment 10 --punishment --rule bpp --cheap-talk   # 数字だけ伝える+減点

# くせを測る(1回目の拠出を条件を変えて聞く、罰の並び順を変える)
python run.py probe --llm claude:claude-haiku-5-5 --n 12
```

AIは `claude -p` で呼びます。API キーは要りませんが、Claude Code にログインしている必要があります。
モデルは `--llm claude:<モデル名>` で差し替えます。`@low` のように付けると effort も変えられます。

## 部品

| 部品 | ファイル | 役目 |
|---|---|---|
| 人物像をつくる | `sim/persona.py`、`personas/*.json` | 分布の定義から、架空の人物を seed つきで作る。作った集団の割合を定義と比べる |
| AIを動かす | `sim/llm.py` | システムプロンプトと問いを渡し、JSON Schema に沿った答えを受け取る |
| ルールを動かす | `sim/games/public_goods.py` | 拠出の配分と罰の計算。テーマごとにここを差し替える |
| 記録と再現 | `sim/record.py` | 1回の実行を `runs/<日時>-<名前>/` に残す |
| くせの測定 | `sim/probes.py` | 言い回し・実験名・人物像・並び順を変えたときのずれと、費用を数える |

### 記録に残すもの

- `manifest.json`: モデル名と版、プロンプトのファイルとハッシュ、設定値、seed、git の版、人物の一覧と分布
- `calls.jsonl`: AIへの問いと答え。費用・トークン・時間つき
- `events.jsonl`: ラウンドごとの拠出・利得・罰

プロンプトは `prompts/` のファイルで持ち、git で版を管理します。中身のハッシュも記録に残します。

### `claude -p` の呼び方

- 空のフォルダから呼び、ツールと MCP と設定ファイルを外す。リポジトリの CLAUDE.md を読ませないため
- `--system-prompt` で既定のシステムプロンプト(約6,600トークン)を置き換える。1回の費用が下がる
- `--json-schema` で答えの形を決める。答えは `structured_output` から取る

## まだ決めていないこと

- 罰の費用と効き目は、#169 で論文に合わせた(`--rule fg2000` が既定。子00の試運転は `--rule flat`、#173 の Bochet ほかは `--rule bpp`)
- チャットは、人間は時間内に自由に話したが、AIでは1人ずつ順に `--chat-turns`(既定3)巡話す
- `personas/students.json` の割合は仮置き。統計に基づく分布は、糸島に置き換える段で作る

## 再生画面(Godot)

`viewer/` は、ゲームの記録を 3D で再生する Godot 4.6 のプロジェクトです。
AIを呼び直さずに記録だけを読むので、同じ記録からは同じ映像ができます。

- 登場人物: まるい体に大きな目と触角を付けた、自作のキャラクター。Godot の基本の形(球・カプセル)だけで組む
- 動き: 入れるときは腕を伸ばして金貨を投げ、減点では相手を指して赤い玉を飛ばす。受けた人は目をつぶって赤く光る
- 並び: 4人がテーブルの後ろに横一列に並ぶ。頭の上の名札に、性格・名前・いまの得点・順位を出す
- 判断の理由と作戦: 1人ずつ順に、話す人の上に大きな吹き出しで出す。作戦の段がある記録では、入れた理由・減点の理由は作戦と重なるので省く
- 話し合い(#173): チャットも、1発言ずつ吹き出しで出す。数字だけ伝える条件は、頭の上に言った量を出す
- 画面の下: 回ごとの入れた量と減点(「B→4」はBに4点)を表にする。終わった場面の分だけ埋まる

```bash
# 記録を再生用の JSON にまとめる
python viewer/export_replay.py runs/<日時>-game-p

# 動画に書き出す(窓が隠れるとコマが抜けるため、常に手前に出す。相対パスは viewer/ から数えるので絶対パスで渡す)
godot --path viewer --always-on-top --resolution 1920x1080 --fixed-fps 30 --write-movie "$PWD/viewer/out/replay.avi"
ffmpeg -i viewer/out/replay.avi -c:v libx264 -pix_fmt yuv420p -crf 20 viewer/out/replay.mp4
```

- 途中から確かめるときは、環境変数 `REPLAY_START=<秒>` で再生の開始位置を変えられます
- `main2d.tscn` は最初に作った 2D 版です。`main3d.tscn` が既定です
- `viewer/out/`(動画)と `viewer/.godot/`(Godot の作業ファイル)は git に入れません
