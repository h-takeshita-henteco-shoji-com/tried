---
description: 市役所と議会のハーネスで、街を1か月運営する(運営のフォルダ、何か月目)
---

市役所と議会のハーネス(`code/ai-mayor/mayor/council-design.md`)で、街を1か月運営します。
引数 $ARGUMENTS は「運営のフォルダ 何か月目」です(例: `2026/10-30-AIは最高の市長になれるか-25-計画の市長に任せる 3`)。

## 手順

1. 引数を読む。運営のフォルダは絶対パスに直す。月は1〜12。2桁の月を `MM` とする
   - 運営のフォルダに `council/` がなければ作る
   - 1か月目は、前の月のファイルがなくてよい
2. hooks が読む状態のファイルを書く(`council-interfaces.md` の3)
   ```bash
   mkdir -p ~/.cache/ai-mayor
   python3 -c 'import json,sys; json.dump({"runDir": sys.argv[1], "month": int(sys.argv[2]), "advanced": False}, open(sys.argv[3], "w"))' "<運営のフォルダ>" <月> ~/.cache/ai-mayor/council-current.json
   ```
3. ゲームの窓口につながるかを `city_info` で確かめる。ダイアログが出ていたら、人に伝えて止める
4. `set_panel_title` で `AI Mayor - City Council` を出す
5. Workflow で `code/ai-mayor/mayor/council-month.js` を回す。args は `{"runDir": "<運営のフォルダ>", "month": <月>}`
   - 止まった段で返ったら(`stoppedAt` がある、または `done.stop` が true)、理由を人に伝えて、ここで止める。片づけたら、同じ月を `resumeFromRunId` で再開する
6. Workflow の返り値を、そのまま `<運営のフォルダ>/council/mMM-run.json` に書く
7. 月の終わりの確かめ
   ```bash
   python3 code/ai-mayor/tools/check_council_month.py "<運営のフォルダ>" <月>
   ```
   出力を、市政ノートの「型から外れたこと」に貼る。外れたことがなければ「なし」と書く
8. 会話の記録を、役ごとに抜き出す(`council-design.md` の9.2)
   ```bash
   python3 code/ai-mayor/tools/extract_transcript.py <id> "<運営のフォルダ>/transcripts/mMM-<役>.md" --raw-dir ~/ai-mayor-transcripts/council
   ```
   id は Workflow の記録から読む。役は mayor-desk、mayor-field、assembly、8つの局(財政局 finance を含む)。差し戻しがあった月は、再調査した局を `<局>-recheck` の名前で足す
9. 台帳と議事録を作る
   ```bash
   python3 code/ai-mayor/tools/make_council_ledger.py "<運営のフォルダ>" <月>
   python3 code/ai-mayor/tools/make_council_minutes.py "<運営のフォルダ>" <月>
   ```
10. 段ごと・局ごとのトークン数と時間を、市政ノートの費用の欄に書く(Workflow の記録から)
11. 人に報告する。順番は次のとおり
    - 運営した期間(ゲーム内の日付)と、止まった理由
    - 編成方針の重点
    - 局の案の数、採った施策、差し戻し(再調査した案)、議会の判断(議案の点1〜4と、財政の点5。1か月目は長期計画の判定)
    - 実行の結果と見回り
    - hooks の拒否と、型から外れたこと
    - 議事録のパス

## 注意

- この手順は Workflow を呼ぶ。人がこの手順を呼んだことが、Workflow を回す同意になる
- 月の途中で人が止めたいときは、Workflow を止め、状態のファイルはそのままにする
- commit と push はしない。`/publish` でまとめて行う
- 4人の市長(#89〜#93)の比べの決まり(`compare.md`)と同じく、運営を始めたら12か月が終わるまで、ハーネスの部品(`council-design.md` の12の「固めるもの」)を変えない
