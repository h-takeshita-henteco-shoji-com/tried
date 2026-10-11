# AI Mayor

親テーマ #39「AIは最高の市長になれるか」で育てる Cities: Skylines(初代)の Mod です。
日付フォルダにはコピーせず、コードはここだけに置きます。

## ビルド

Mac で確認済みです(Apple M5、.NET SDK 10.0.401)。

```bash
dotnet build code/ai-mayor/src/AIMayor.csproj -c Release
```

ビルド後、DLL を次のフォルダへ自動で置きます。

`~/Library/Application Support/Colossal Order/Cities_Skylines/Addons/Mods/AIMayor/`

ゲーム本体の DLL は Steam のインストール先を直接参照します。
リポジトリには入れません。場所が違う場合は `-p:GameDir=...` で上書きします。
