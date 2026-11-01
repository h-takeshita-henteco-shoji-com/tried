# #132 で比べるモデル

3社のモデルを、小・中・大・最上位の4段階で比べる。
各社の公式ドキュメントで、2026-10-31 に確かめた。実施の直前に、版と料金をもう一度確かめる。

## 組み合わせ（12モデル）

| 段階 | Anthropic | OpenAI | Google |
|---|---|---|---|
| 小 | Claude Haiku 5.5（`claude-haiku-5-5`） | GPT-6 Luna（`gpt-6-luna`） | Gemini 3.5 Flash-Lite（`gemini-3.5-flash-lite`） |
| 中 | Claude Sonnet 5.5（`claude-sonnet-5-5`） | GPT-6.1 Terra（`gpt-6.1-terra`） | Gemini 3.8 Flash（`gemini-3.8-flash`） |
| 大 | Claude Opus 5.5（`claude-opus-5-5`） | GPT-6.1 Sol（`gpt-6.1-sol`） | Gemini 3.1 Pro Preview（`gemini-3.1-pro-preview`） |
| 最上位 | Claude Fable 5.1（`claude-fable-5-1`） | GPT-6 Astra（`gpt-6-astra`） | Gemini 4 Argon（`gemini-4-argon`） |

- Gemini の大は、プレビュー版しかない（2026-02 公開）。比べるときは、その旨を添える。
- Claude の小は Haiku 5.5（2026-10-07 公開）。Haiku 4.5 は旧版で、コンテキストが 200K しかない。

### Gemini 4 Carbon が出た場合

Google は 2026-10-28 に、Argon より上の最上位モデル Gemini 4 Carbon を発表した。
当面はサイバーセキュリティの防御企業に限って提供され、API の一覧と `agy models` にはまだない（2026-10-31 時点）。
発表時の料金は Argon と同じ 2 / 10（$/100万トークン）。のちに 4 / 20 に上がるという報道がある。

使えるようになったら、Google の段階を次のように当て直す。プレビュー版の 3.1 Pro を外せる。

| 段階 | Google |
|---|---|
| 小 | Gemini 3.5 Flash-Lite |
| 中 | Gemini 3.8 Flash |
| 大 | Gemini 4 Argon |
| 最上位 | Gemini 4 Carbon |

それまでは、Google を Flash と Argon の2段階（Argon を最上位）で試し、Carbon が出たら同じ問いで足す。

### 使う範囲（2026-10-31決定）

- Google は Flash と Argon の2段階で始める。全体は10モデル。Gemini 4 Carbon が出たら足す。
- 推論の強さは、low・medium・high の3段階をすべて試す。
- 実行は契約の CLI で行う（下の「契約（サブスクリプション）のCLIで使えるモデル」）。

## 各モデルの性質

| モデル | 公開日 | コンテキスト長 | 推論の既定 | 料金（入力/出力, $/100万トークン） |
|---|---|---|---|---|
| Claude Haiku 5.5 | 2026-10-07 | 1M | adaptive、effort medium | 10万以下 0.10/0.50、10万超 0.50/2.50 |
| Claude Sonnet 5.5 | 2026-09-28 | 1M | adaptive、effort high | 2 / 10 |
| Claude Opus 5.5 | 2026-09-22 | 1M | adaptive（止められない）、effort medium | 4 / 20 |
| Claude Fable 5.1 | 2026-09-01 | 1M | adaptive（止められない）、effort high | 10 / 50 |
| GPT-6 Luna | 2026-09-22 | 1,050,000（入力は922,000まで） | medium | 0.10 / 0.50 |
| GPT-6.1 Terra | 2026-10-26 | 同上 | medium | 1 / 5 |
| GPT-6.1 Sol | 2026-09-29 | 同上 | medium | 2 / 10 |
| GPT-6 Astra | 2026-09-03 | 同上 | 未確認（none は選べない） | 10 / 50 |
| Gemini 3.5 Flash-Lite | 2026-07-21 | 1,048,576 | minimal | 0.30 / 2.50 |
| Gemini 3.8 Flash | 2026-09-02 | 1,048,576 | medium | 0.75 / 3.75（2027-01-01 から 1.50 / 7.50） |
| Gemini 3.1 Pro Preview | 2026-02-19 | 1,048,576 | 未確認 | 200K以下 2/12、200K超 4/18 |
| Gemini 4 Argon | 2026-10-13 | 1,048,576 | medium | 2 / 10（2026-12-01 から 4 / 20） |

- OpenAI は、272K トークンを超えると入力2倍・出力1.5倍の料金になる。
- 3社とも画像を読める。

## 条件をそろえるときの注意

**推論の強さ**
既定の値がモデルごとに違う。Fable と Opus は思考を止められず、Astra は none を選べない。
完全にはそろわないため、使った設定をそのまま記録する。

**画像の縮小**
各社が内部で画像を縮める仕様が違う。

- Claude: 長辺 2,576px・4,784 トークンまで。
- OpenAI: 32×32px を1単位として数える。Astra の high は 2,500 単位まで（3000×2000px は約1600×1067px に縮む）。`detail: "original"` なら元の寸法を保つ。Luna・Terra・Sol は未確認。
- Gemini: `media_resolution` で1枚のトークン数を選ぶ（low 280、medium 560、high 1120、ultra_high 2240）。

条件をそろえるには、PNG を長辺 2,576px 程度に縮めてから送る案がある。

**DXF の渡し方**
DXF は約54万〜93万トークンあり、本文としてはそのまま渡せない。

- Claude: Files API で上げたファイルを、コード実行に渡せる。コード実行の環境に ezdxf は入っていない。
- OpenAI: Code Interpreter にファイルを渡せる。ezdxf の有無は未確認。
- Gemini: コード実行に渡したファイルも、コンテキストを消費する。本文で渡すのと変わらない。

API のコード実行では、3社を同じ条件にできない。
3社で同じ条件にするには、文字と図形の一覧に縮めて渡すか、手元で動くCLIを使う。

## 契約（サブスクリプション）のCLIで使えるモデル

API キーではなく、各社の契約のまま、対話なしで1回ずつ実行できるかを確かめた（2026-10-31）。
「1+1の答えだけ書いて」を送り、答えが返ったものを ○ とした。

| 段階 | Claude（`claude -p`） | OpenAI（`codex exec`） | Google（`agy -p`） |
|---|---|---|---|
| 小 | ○ Haiku 5.5 | ○ Luna | × Flash-Lite は一覧にない |
| 中 | ○ Sonnet 5.5 | ○ Terra | ○ 3.8 Flash（low・medium・high） |
| 大 | ○ Opus 5.5 | ○ Sol | × 3.1 Pro Preview は一覧にない |
| 最上位 | ○ Fable 5.1 | ○ Astra | ○ 4 Argon（low・medium・high） |

- Google は、Gemini CLI の個人向けログインが終了していた。後継の Antigravity CLI（`agy`、1.4.10）を使う。
- `agy models` の一覧は、Gemini 4 Argon、Gemini 3.8 Flash、Claude Opus 5.5、Claude Sonnet 5.5、GPT-OSS 120B だけ。
- Google の小と大を試すには、Gemini の API キーが要る。
- 推論の強さは、`codex exec -c model_reasoning_effort=…`、`agy --effort …` またはモデル名の末尾（-low など）で指定する。

CLI は「コードを書くAI」として動くため、各社の独自の指示文と道具が入る。
純粋なモデルの比較ではなく、CLI ごとの比較になる。この条件を記録する。
作業フォルダのファイルを読めるため、正解の記録が見えない別のフォルダで実行する。

## 期限のあるもの

- Gemini 4 Argon は 2026-12-01、Gemini 3.8 Flash は 2027-01-01 に値上げ。
- Claude Haiku 4.5 は「2026-10-15 より前には廃止しない」とされ、その日を過ぎている。
- Claude Sonnet 4.5 は 2026-11-30、GPT-5 系は 2026-12-11 に停止。

## 出典

- Anthropic: https://platform.claude.com/docs/en/about-claude/models/overview 、https://platform.claude.com/docs/en/about-claude/pricing 、https://platform.claude.com/docs/en/build-with-claude/vision 、https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool
- OpenAI: https://developers.openai.com/api/docs/models 、https://developers.openai.com/api/docs/pricing 、https://developers.openai.com/api/docs/guides/images-vision 、https://developers.openai.com/api/docs/guides/tools-code-interpreter
- Google: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/ 、https://ai.google.dev/gemini-api/docs/models 、https://ai.google.dev/gemini-api/docs/pricing 、https://ai.google.dev/gemini-api/docs/media-resolution 、https://ai.google.dev/gemini-api/docs/code-execution
