---
description: テーマをGitHub Issueに起票する(単独・親・子)
---

テーマをGitHub Issueとして起票します。引数: $ARGUMENTS

## 手順

0. 引数が `drafts/` 配下のパスなら、その `draft.md` を読み、きっかけと案から次の3つを組み立てます。起票後は手順6を行います。
1. 引数と会話から、次の3つを決めます。足りなければ1回だけまとめて質問します。
   - 種別: 単独 / 親 / 子(子の場合は親Issue番号)
   - タイトル: 主題を短く(フォルダ名にも使うので20字以内)
   - 本文: 「何を試すか」「なぜ気になるか」を各1〜2文
2. 本文に顧客案件や機密に当たる内容が含まれていないか確認します。含まれていれば起票せず、その旨を伝えます。
3. Issueを作成します。
   ```bash
   gh issue create --title "<タイトル>" --label "候補" --body "<本文>"
   ```
   - 親の場合は本文の末尾に「子Issueは最初の2〜3件だけ作り、やりながら足す」と追記します。
   - 親の場合はタイトルの先頭に「[親] 」を付けます。
4. 子の場合は、サブイシューとして親に紐づけます。
   ```bash
   CHILD_ID=$(gh api repos/{owner}/{repo}/issues/<子番号> --jq .id)
   gh api -X POST repos/{owner}/{repo}/issues/<親番号>/sub_issues -F sub_issue_id=$CHILD_ID
   ```
5. 作成したIssueの番号とURLを報告します。
6. drafts から起票した場合は、`draft.md` の `status` を `起票済` に、`issue` を作成した番号に書き換えます。フォルダは消しません。

## 注意

- 既存のIssueと重複していないか `gh issue list --label 候補` で確認してから作成します。
- 子を作る前に、親がopenであることを確認します。
