---
description: 今日の記録を始める(フォルダ作成、log.md 雛形、ラベルを実施中に)
---

Issue番号 $ARGUMENTS のテーマで、今日の実施記録を始めます。

## 手順

1. Issueの情報を取得します。親子関係はGraphQLで確認します。
   ```bash
   gh issue view $ARGUMENTS --json number,title,body,labels,state
   gh api graphql -f query='query { repository(owner:"{owner}", name:"{repo}") { issue(number:$ARGUMENTS) { parent { number title } subIssues(first:1) { totalCount } } } }'
   ```
   - stateがclosedなら中止して伝えます。
   - subIssuesのtotalCountが1以上なら親Issueです。親はフォルダを持たないため中止し、子Issueの番号を指定するよう伝えます。
2. フォルダ名を決めます。日付は今日の日付を使います。
   - 単独: `YYYY/MM-DD-<主題>`
   - 子: `YYYY/MM-DD-<親の主題>-<連番2桁>-<子の主題>`
     連番は、親の既存の子のうちフォルダを持つものの数+1とします。
   - 主題はIssueタイトルから「[親] 」などの接頭辞を除き、空白はハイフンにします。
3. フォルダと `assets/` を作り、`log.md` を次の雛形で作成します。
   ```markdown
   ---
   date: YYYY-MM-DD
   title: <Issueタイトル>
   issue: <番号>
   parent: <親番号。単独なら空>
   ai:
   minutes:
   result:
   status: 未公開
   url:
   qiita_url:
   ---

   ## 試したこと

   <Issue本文の「何を試すか」を転記>

   ## 結果

   ## 学び
   ```
4. Issueのラベルを `候補` から `実施中` に付け替え、フォルダのパスをコメントします。
   ```bash
   gh issue edit $ARGUMENTS --remove-label "候補" --add-label "実施中"
   gh issue comment $ARGUMENTS --body "実施記録: <フォルダのパス>"
   ```
5. 作成したフォルダのパスと、所要時間の上限を決めるよう促す一言を報告します。

## 注意

- commitやpushはこの手順では行いません。1日の終わりに `/publish` でまとめて行います。
- 同じ日付のフォルダが既にあれば、上書きせず中止して伝えます。
