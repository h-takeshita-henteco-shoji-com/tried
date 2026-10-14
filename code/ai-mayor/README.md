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

## 地形のツール

`tools/` に、福岡の地形を作るスクリプトを置いています。

- `range_map.py`: 再現範囲の地図を描く(OpenStreetMap のタイルを使用)
- `fetch_dem.py`: 国土地理院の標高タイルを取得し、1枚の配列につなぐ
- `make_heightmap.py`: 標高の配列から、1081×1081 の16ビット高さマップを作る

標高データと高さマップは公開しません。リポジトリにも置きません。
出力はすべて `~/.cache/ai-mayor-dem/` に置きます。

```bash
pip install numpy scipy pillow
python3 code/ai-mayor/tools/fetch_dem.py
python3 code/ai-mayor/tools/make_heightmap.py
```

標高データの出典: 国土地理院 標高タイル(基盤地図情報 数値標高モデル DEM10B)
