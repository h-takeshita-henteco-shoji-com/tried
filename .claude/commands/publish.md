---
description: 公開後の書き戻し(URL・status 更新、Issue close、commit、push)。Qiita公開時は qiita を付ける
---

noteまたはQiitaに投稿したあとの書き戻しを行います。引数: $ARGUMENTS

- `<Issue番号> <noteのURL>` : noteの公開。下の「手順」をすべて行います。
- `<Issue番号> qiita <QiitaのURL>` : Qiitaの公開。下の「Qiitaの公開」だけを行います。

## 手順

1. 引数からIssue番号とURLを取り出します。URLが無ければ、未公開のままcommitとpushだけ行うか確認します。
2. Issue番号に対応するフォルダを探します。`log.md` の `issue:` の値で検索します。
   ```bash
   grep -rl "^issue: <番号>$" --include=log.md .
   ```
3. `log.md` の先頭項目を更新します。
   - `url:` に公開URLを書きます。
   - `status:` を `公開済` にします。
   - `ai:` `minutes:` `result:` が空なら、本文から推定して提案し、確認を取ってから埋めます。
4. `article.md` が存在するか確認します。無ければ、`log.md` の3点だけで1件と数える方針に従い、そのまま進めます。
5. Issueを更新してcloseします。
   ```bash
   gh issue edit <番号> --remove-label "実施中" --remove-label "執筆中" --add-label "公開済"
   gh issue comment <番号> --body "公開しました: <URL>"
   gh issue close <番号>
   ```
6. 親Issueがある場合、親の子が全部closeしたかを確認します。
   ```bash
   gh api repos/{owner}/{repo}/issues/<親番号>/sub_issues --jq '[.[] | select(.state=="open")] | length'
   ```
   - 0なら「親のまとめ記事を書いてから親をcloseする」よう伝えます。親は自動でcloseしません。
7. commitとpushを行います。コミットメッセージは `<日付> <タイトル> を公開 (#<番号>)` とします。
   ```bash
   git add <フォルダ>
   git commit -m "<日付> <タイトル> を公開 (#<番号>)"
   git push
   ```
8. 更新した項目、closeしたIssue、commitのハッシュを報告します。

## Qiitaの公開

noteの公開とIssueのcloseは済んでいる前提です。Issueの状態とラベルは変えません。

1. 手順2と同じ方法で、Issue番号に対応するフォルダを探します。
2. `log.md` の `qiita_url:` にURLを書きます。項目が無い古い `log.md` なら、`url:` の次の行に足します。
3. `qiita.md` があるか確認します。無ければ、書いた記事をリポジトリに残すか確認します。
4. `article.md` の末尾にQiitaの記事へのリンクがあるか確認します。無ければ足し、noteの記事にも同じリンクを足すよう伝えます。
5. Issueにコメントします。closeしたままにします。
   ```bash
   gh issue comment <番号> --body "Qiitaに技術の深掘りを公開しました: <URL>"
   ```
6. 手順7と同じ方法でcommitとpushを行います。コミットメッセージは `<日付> <タイトル> をQiitaに公開 (#<番号>)` とします。
7. 更新した項目とcommitのハッシュを報告します。

## 注意

- URLがnoteのドメインでない場合は、誤りでないか一度確認します。Qiitaの公開では、Qiitaのドメインかを確認します。
- `assets/` に機密に当たるファイル(APIキー、顧客名を含む画面写真)が無いか、commit前に目視で確認します。
