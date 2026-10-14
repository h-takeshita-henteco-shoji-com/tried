---
date: 2026-10-12
title: ゲームとMod開発環境を整える
issue: 40
parent: 39
ai: Claude Code (Opus 5.5)
minutes: 60
result: 成功(Modの読み込みと有効化まで)
status: 公開済
url: https://note.com/tried_hs/n/n70e3d774db73
qiita_url:
---

記事は #41 と1本にまとめる。`url` には #41 の記事の URL を入れる。

## 試したこと

MacにCities: Skylines(初代)を入れ、Mod開発の環境を整える。
何もしないModを1つ作り、ゲームのコンテンツマネージャーに表示されて有効にできるまで進める。
ゲームの版、DLC、Mac(チップ、メモリ)、開発の道具の版を記録する。
あわせて、Modのコードの置き場所を決め、ゲーム本体のDLLを除外する `.gitignore` を設定する。
成果物は、読み込まれたMod、環境の記録、コードの置き場所の決定。

## 結果

### 環境

- Mac: Apple M5(10コア)、メモリ16GB、macOS 26.6.2
- ゲーム: Cities: Skylines 1.21.1-f9(Steam版、build 22724702)
- ゲーム本体はx86_64のみ。Rosetta 2で動く。エンジンはUnity 5.6.7f1、描画はMetal
- DLC: なし(本体のみ)。Steamの「管理」→「DLC」で確認した
- DLCのファイルは持っていなくても全部インストールされる。ファイルやログからは持っているかを判定できない
- .NET SDK 10.0.401。`dotnet-install.sh` で `~/.dotnet` に入れた
- Modの対象: .NET Framework 3.5(`net35`)、C# 7.3

### 何もしないModの読み込み

- `code/ai-mayor/` にModを作り、`dotnet build` でビルドした(警告0、エラー0)
- ビルド後、DLLを `~/Library/Application Support/Colossal Order/Cities_Skylines/Addons/Mods/AIMayor/` に自動で置く
- 起動ログ(`~/Library/Logs/Unity/Player.log`)に `Assembly AIMayor, Version=1.0.0.0 ... loaded.` が出た
- コンテンツマネージャーの「Mod」に「AI Mayor」が表示され、有効にできた

### 詰まった所

- Homebrewの `dotnet-sdk` はpkgを使うため、sudoのパスワードを求めて失敗した
- 公式の `dotnet-install.sh` でホーム配下に入れて回避した。sudoは要らない
- `Colossal Order` フォルダは初回起動まで存在しない。ビルド時の配置で先に作られた

### コードの置き場所

- リポジトリ直下の `code/ai-mayor/` に1か所で置く。日付フォルダにはコピーしない
- 記事からはこのフォルダへリンクする
- ゲーム本体のDLLは `.csproj` からゲームのフォルダを直接参照する。リポジトリには入れない
- 念のため `code/ai-mayor/.gitignore` で `bin/` `obj/` `*.dll` `*.mdb` `*.pdb` を除外した

## 学び

- MacでもModは作れる。ゲーム本体はIntel版のままで、Rosetta 2の上で動く
- ビルドに要るのは.NET SDKだけだった。MonoやVisual Studioは要らない
- 参照アセンブリのパッケージ(`Microsoft.NETFramework.ReferenceAssemblies.net35`)で、Macからでも `net35` 向けにビルドできる
- 読み込みの成否は、画面を見る前に `Player.log` で確かめられる。AIにも確認を任せやすい
