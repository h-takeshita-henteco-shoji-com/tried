# kaigo-rag

訪問介護の介護報酬のルールを引くRAGを、複数の方式で比べるためのコードです。
Issue #154 の実施記録で使います。器は SQLite 1つです。全文検索は FTS5、ベクトル検索は vec1 を使います。

非公式の検証です。請求の判断には使わないでください。

## 使う資料

公開されている厚労省の告示・省令・通知と、Q&A集だけを使います。

- 介護サービス関係Q&A集(令和8年9月掲載版、厚生労働省): https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/hukushi_kaigo/kaigo_koureisha/qa/index.html
- 告示19号・95号・94号、省令37号、老企25号・36号の溶け込み版: 全老健「法令・Q&A検索システム」 https://hourei.roken.or.jp/
  - 告示・通知の本文は、著作権法13条により権利の目的になりません。チャンクに切る加工をしています
- 介護保険法: 同じく全老健の法令検索(総則、保険給付、事業者及び施設の3章だけ)
- 老計10号(訪問介護におけるサービス行為ごとの区分等について、平成30年改正の溶け込み版): 枚方市が載せている PDF https://www.city.hirakata.osaka.jp/cmsfiles/contents/0000046/46318/tsuuchi_houmon_10.pdf
  - 厚労省は改正通知だけを PDF で出しています。PDF から文字を取るのに `pdftotext`(poppler)を使います

原文と中間データはリポジトリに入れません。下の手順で作り直せます。

## 手順

```bash
uv sync
# vec1(SQLite 本体の ext/vec1/vec1.c)をビルドする
cc -O3 -DNDEBUG -I/opt/homebrew/opt/sqlite/include -dynamiclib ext/vec1.c -o ext/vec1.dylib

uv run python src/fetch.py         # 原文を data/raw に取る
uv run python src/chunk_docs.py    # 告示・省令・通知をチャンクに切る
uv run python src/build_qa.py      # Q&A集を1問1件にする
uv run python src/make_set_a.py    # 問題集を分け、A(言い換え)を作る(claude -p を使う)
uv run python src/build_corpus.py  # コーパスをまとめる(B の40問は外す)
uv run python src/embed.py         # ruri-v3-310m で埋め込む
uv run python src/build_index.py   # SQLite に FTS5 と vec1 の索引を作る
uv run python src/make_set_b.py    # B(根拠)の正解を pooling と判定で付ける(claude -p を使う)
uv run python src/evaluate.py      # 基本3種を並べて採点する
uv run python src/sweep_vec1.py    # vec1 の nprobe と rerank の効き方を測る

# 検索を賢くする3種
uv run python src/make_context.py        # Contextual: 文書チャンクの位置づけを Haiku に書かせる
uv run python src/build_variants.py path # 見出しのパスを足した版の索引
uv run python src/build_variants.py ctx  # 位置づけの文を足した版の索引
uv run python src/make_hyde.py           # HyDE: 仮の答えを Sonnet に書かせる
uv run python src/evaluate.py smart      # リランカー・HyDE・文脈を足す版を採点する
uv run python src/judge_extra.py <未判定の候補.json>  # pool を広げる(新しい方式の未判定の上位を判定する)
uv run python src/evaluate_doc_only.py   # 告示・通知だけを対象に採点する

# 検索をAIに任せる2種(答えまで出す)
uv run python src/server.py &            # 道具のサーバー(検索・全文・目次)を起動する
uv run python src/answer.py llm          # 資料なしで答える(比較の下限)
uv run python src/answer.py rag          # 上位5件を渡して1回で答える
uv run python src/answer.py agentic      # エージェント検索(search と read を何度でも)
uv run python src/answer.py pageindex    # PageIndex 方式(目次の tree と read だけ)
uv run python src/judge_answers.py llm rag agentic pageindex  # 方式を伏せて、答えを 2/1/0 で判定する
uv run python src/score_answers.py llm rag agentic pageindex  # 集計する。未判定の根拠は judge_extra.py で判定する

# 資料を足す(老計10号、介護保険法)。既存の id を動かさないよう末尾に足す
uv run python src/add_docs.py            # build_corpus.py を回し直したら、これも回し直す
uv run python src/pool_new_docs.py       # 足した資料で上位に入った候補を集める
uv run python src/judge_extra.py data/unjudged_newdocs.json
KAIGO_TAG=_v2 uv run python src/answer.py agentic   # 答えを別のファイル(answers_agentic_v2.jsonl)に書く
KAIGO_GRADES=results/answer_grades_v2.jsonl uv run python src/judge_answers.py llm rag agentic pageindex rag_v2 agentic_v2 pageindex_v2

# 判定を固める。Sonnet をあと2回(並び順を変える)、Opus を1回
KAIGO_GRADES=results/answer_grades_v2_r2.jsonl KAIGO_SEED=r2 uv run python src/judge_answers.py <上と同じ7方式>
KAIGO_GRADES=results/answer_grades_v2_r3.jsonl KAIGO_SEED=r3 uv run python src/judge_answers.py <上と同じ7方式>
KAIGO_GRADES=results/answer_grades_v2_opus.jsonl KAIGO_JUDGE=opus uv run python src/judge_answers.py <上と同じ7方式>
uv run python src/vote_answers.py        # 多数決、ぶれ、Opus との一致、方式の差(符号検定)

# GraphRAG(用語と参照のグラフ。LLM は使わない)
uv run python src/build_graph.py         # 同じ SQLite に entity・mention・ref の表を作る
uv run python src/pool_graph.py && uv run python src/judge_extra.py data/unjudged_graph.json  # グラフの候補を判定して足す
uv run python src/evaluate.py graph      # 検索としての GraphRAG を採点する
KAIGO_TAG=_v2 uv run python src/answer.py graph     # エージェントの道具に related を足して答える
KAIGO_GRADES=results/answer_grades_graph_r1.jsonl KAIGO_SEED=gr1 uv run python src/judge_answers.py rag_v2 agentic agentic_v2 pageindex_v2 graph_v2  # r2、r3 も同じ
uv run python src/vote_answers.py graph

# 取り込みの部品: LiteParse と pdftotext、OCR の比較(老計10号の PDF)
uvx --from liteparse lit parse data/raw/rokei10/hirakata.pdf --no-ocr --format markdown -o /tmp/hirakata.md
pdftotext data/raw/rokei10/hirakata.pdf /tmp/hirakata.txt
pdftoppm -r 200 -f 2 -l 2 -png data/raw/rokei10/hirakata.pdf /tmp/pg
uvx --from liteparse lit parse /tmp/pg-2.png --ocr-language jpn --format text -o /tmp/ocr_tess.txt
swift src/ocr_vision.swift /tmp/pg-2.png > /tmp/ocr_vision.txt   # macOS Vision(手元で完結)

# GraphRAG のライブラリ(訪問介護の範囲 data/subset_houmon.json、608件)
uv run python src/graph_lightrag.py build          # LightRAG の索引(claude -p の Haiku で用語と関係を抜き出す。約140分)
uv run python src/graph_lightrag.py retrieve_all   # A と B を5つの mode で引き、results/lib_lightrag.json に書く(約7分)
uv run python src/pool_lightrag.py && uv run python src/judge_extra.py data/unjudged_lightrag.json  # LightRAG の候補を判定して足す
uv run python src/llm_shim.py &                    # OpenAI と同じ形の中継(Microsoft GraphRAG と HippoRAG 用)
# Microsoft GraphRAG は別の環境に入れる(uv venv /tmp/gr_ms/.venv && uv pip install graphrag==3.3.0)
# data/msgraphrag/ に settings.yaml と prompts/ を置く(graphrag init の後、LLM を中継に向け、指示文に日本語で書くよう足した)
# 入力 data/msgraphrag/input/subset.jsonl は、範囲の608件を1件ずつ {"id","title","text"} にしたもの
/tmp/gr_ms/.venv/bin/graphrag index --root data/msgraphrag
/tmp/gr_ms/.venv/bin/python src/graph_msgraphrag.py  # local と basic で引き、results/lib_msgraphrag.json に書く
uv run python src/pool_lightrag.py msgraphrag && uv run python src/judge_extra.py data/unjudged_msgraphrag.json
# HippoRAG 2 も別の環境(uv venv /tmp/gr_hippo/.venv && uv pip install hipporag==2.0.0a3 "pyarrow<17")
/tmp/gr_hippo/.venv/bin/python src/graph_hipporag.py build          # 用語と三つ組を Haiku で抜き出す(1件に2回)
/tmp/gr_hippo/.venv/bin/python src/graph_hipporag.py retrieve_all   # HippoRAG 2 と DPR で引き、results/lib_hipporag.json に書く
uv run python src/pool_lightrag.py hipporag && uv run python src/judge_extra.py data/unjudged_hipporag.json
uv run python src/evaluate.py subset               # 範囲の中で、基準の方式と results/lib_*.json を並べて採点する

# note の記事の図(数字は log.md と親テーマの下調べから写した)
uv run --with matplotlib python src/make_figures.py ../../2026/11-08-訪問介護の困りごとをAIで解く-01-ルールを引けるRAGを複数の方式で比べる/assets
```

B の判定は、pool を広げながら何回かに分けて付けた。`data/set_b.round1.jsonl` が1回目の後。`data/unjudged_round2.json`(検索を賢くする方式)、`data/unjudged_answers.json`(答えが挙げた根拠)、`data/unjudged_newdocs.json`(足した資料)、`data/unjudged_graph.json`(GraphRAG)、`data/unjudged_lightrag.json`(LightRAG)、`data/unjudged_msgraphrag.json`(Microsoft GraphRAG)、`data/unjudged_hipporag.json`(HippoRAG 2)が、後から判定した候補。

エージェントは `claude -p` で動かす。道具は `/tmp/kaigo-agent` に写した `tool.py` だけを Bash で許し、B の問いと中身が同じ Q&A は道具から隠す。

## 問題集

- `data/set_a.jsonl` A 言い換え問題(100問): 訪問介護の Q&A の問いを、現場の話し言葉に書き換えた。正解は元の Q&A
- `data/set_b.jsonl` B 根拠問題(40問): コーパスから外した Q&A の問い。正解は、答えの根拠になるチャンク(判定2)
- `data/split.json` どの Q&A を A と B に使ったか
- `data/qa_equiv.json` 中身が同じ Q&A のまとまり。Q&A集の約半分は、別のサービス種別に同じ問いと答えで載っている
- `data/hyde.jsonl` HyDE の仮の答え / `data/context_doc.jsonl` Contextual Retrieval の位置づけの文
- `results/` 採点の結果(JSON)。`answers_<方式>.jsonl` は答えと道具の呼び出し、`answer_grades.jsonl` は答えの判定
  - `*.v1.json` と `answer_grades.jsonl` は資料を足す前、`*.v2.json`、`answers_*_v2.jsonl`、`answer_grades_v2.jsonl` は足した後
