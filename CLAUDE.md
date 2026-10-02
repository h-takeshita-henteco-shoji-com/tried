# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリの性質

AIを使って「やってみた」記録を1日1件ずつ残す、文書中心のリポジトリです。
ビルド、lint、テストは存在しません。成果物はMarkdownと `assets/` 内のファイルです。
運用方針の正本は `README.md` です。方針に迷ったらREADMEを優先します。

## 3つの定型手順で回す

毎日の作業は `.claude/commands/` の3手順で行います。手順の中身を変えるときは、READMEの「1日の流れ」との整合を保ちます。

- `/new-theme` : テーマをGitHub Issueに起票する(単独・親・子)
- `/start-day <Issue番号>` : 日付フォルダと `log.md` 雛形を作り、ラベルを `実施中` にする
- `/publish <Issue番号> <URL>` : URLとstatusを書き戻し、Issueをclose、commitとpush

commitとpushは `/publish` でまとめて行います。`/start-day` では行いません。

## テーマ管理はGitHub Issuesで行う

- 1テーマ1Issue。状態はラベル `候補` `実施中` `執筆中` `公開済` で持ちます。公開したらcloseします。
- 複数日かかるテーマは親子に分けます。親は GitHub のサブイシュー機能で子を束ねます。
- **親Issueはフォルダを持ちません。** `/start-day` に親番号が渡されたら中止します。
- 子は事前に全部作らず、2〜3件ずつ足します。親は子が全部closeした日に、まとめ記事を書いてからcloseします。
- サブイシューの操作はREST `repos/{owner}/{repo}/issues/{n}/sub_issues` と GraphQL の `parent` / `subIssues` を使います。

## フォルダと記録の型

- 単独テーマ: `YYYY/MM-DD-主題/`
- 親子テーマの子: `YYYY/MM-DD-親の主題-連番2桁-子の主題/`
- 各フォルダは `log.md`(実施記録)、`article.md`(公開記事)、`assets/` を持ちます。
- `log.md` 先頭のYAML項目(date, title, issue, parent, ai, minutes, result, status, url)は一覧表の自動生成に使うため、キー名を変えません。
- 本文の最低ラインは「試したこと・結果・学び」の3点です。この3点だけでも1件と数えます。
- `INDEX.md` は自動生成の対象です。手で編集しません(生成の仕組みは未決定)。

## article.md の書き方(note向け)

公開先はnoteで、貼り付け後の手直しを減らすための制約があります。
文章は結論の列挙ではなく、物語として書きます。動機から始め、途中の迷いや驚きを起きた順に残し、学びはその日の場面に戻して閉じます。

- 表を使わない。比較は箇条書きか画像にする
- 見出しは2段まで
- 専門用語に言い換えを添える(読者に非技術者を含む)
- コードは短く抜粋し、全文はリポジトリへのリンクにする

## 公開前の確認

リポジトリとIssuesはどちらも公開です。顧客案件に関わる内容、APIキー、顧客名を含む画面写真は置きません。`/publish` のcommit前に `assets/` を目視で確認します。
