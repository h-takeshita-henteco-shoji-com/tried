# LibreCAD を MCP で操作する

AI が LibreCAD の中の図面を、直接操作できるようにします。
DXF ファイルを書き換えるのではなく、開いている図面を読み書きします。
必要な機能の一覧と、どこまで足したかは `requirements.md` にあります。

## 仕組み

LibreCAD 本体は改造しません。本体の plugin の仕組みを使います。

- `plugin/mcpbridge.cpp` : 127.0.0.1:7471 で、1行1件の JSON の命令を受けます
- `plugin/lc_ops.cpp` : 命令の中身です。本体の内部の部品(RS_Document、RS_Modification など)を直接呼びます
- `server.py` : MCP server(Python、mcp 2.x)。AI からの呼び出しを plugin への命令に変えます。測る・検証・差分はここで計算します

```
AI(Claude など) --MCP(stdio)--> server.py --TCP 7471--> plugin --> LibreCAD の図面
```

plugin は、メニューの「プラグイン → MCP bridge」で待ち受けを始めます。
小さな窓が開いている間だけ命令を受けます。窓は modal ではないので、人も同時に図面を触れます。
命令は、そのとき前面にある図面に効きます。`open_drawing` や `new_drawing` のあとも、開いた図面を追います。

### 本体の内部を呼べる理由

plugin の API(Document_Interface)には、寸法を描く、元に戻す、DXF を開く、がありません。
mac 版の LibreCAD は、実行ファイルが C++ の関数を公開しています(約11,000個)。
そこで plugin を `-undefined dynamic_lookup` で組み、本体の関数に実行時につなぎます。

条件が1つあります。**本体と同じ版のソースの header で組むこと。**
版がずれると部品の作りが合わず、LibreCAD が落ちます(2.2.1 の header で 2.2.1.6 に入れたら落ちた)。

## 道具

| 分類 | 道具 |
|---|---|
| 状態 | ping, doc_info, operation_log, set_vars |
| ファイル | open_drawing, new_drawing, save, save_as |
| 読み取り | list_entities(画層・種類・範囲で絞る), get_entity, list_blocks, list_fonts |
| 描く | add_line, add_polyline, add_circle, add_arc, add_text, add_dim_linear, add_dim_aligned, add_hatch, define_block, add_insert |
| 直す | set_props, move, copy, rotate, scale, mirror, delete, stretch, undo, redo |
| 画層 | layers, set_layer |
| 確かめる | zoom, screenshot, measure, find_near, check_connectivity, validate, snapshot, diff |

- 寸法は `label`(書かれた文字)、`measured`(LibreCAD の表示の値)、`distance`(線の長さ)を返します
- 移動・伸縮・元に戻すのあとは、図形の id が変わります。結果の `new_ids` を使うか、読み直します
- `validate` は、文字だけ古い寸法、重なった図形、壁の切れ目、傾いた線(縦横のはずの画層)を見つけます

## build の手順(macOS、LibreCAD 2.2.1.6)

```bash
brew install qt@5                      # 5.15.19。LibreCAD 同梱の Qt と同じ版
git clone --depth 1 --branch v2.2.1.6 --filter=blob:none --sparse \
  https://github.com/LibreCAD/LibreCAD.git ~/librecad-src/lc
(cd ~/librecad-src/lc && git sparse-checkout set plugins librecad/src libraries)

code/librecad-mcp/build.sh             # 組み立てて ~/Documents/LibreCAD/plugins に置く
code/librecad-mcp/build.sh --restart   # さらに LibreCAD を起動し直し、MCP bridge まで押す
```

- 本体の版は、LibreCAD の crash の記録か「ヘルプ → バージョン情報」で確かめます
- `build.sh` は、Qt の参照先を LibreCAD 同梱の Qt に向け直します(2つの Qt を読み込ませないため)
- アプリ本体(`/Applications/LibreCAD.app`)は書き換えません
- `--restart` は、開いている図面を保存せずに閉じます。試しの図面だけのときに使います

## AI からつなぐ

```json
{"mcpServers":{"librecad":{"command":"uv","args":["run","-q","<このフォルダ>/server.py"]}}}
```

```bash
claude -p "<指示>" --mcp-config mcp.json --strict-mcp-config --allowedTools="mcp__librecad__*"
```

## 試験

LibreCAD で MCP bridge を開いた状態で流します。

```bash
cd tests && python3 test_all.py   # plugin の全命令。/tmp/lcmcp/house.dxf(#135 の図面の写し)を使う
uv run --with "mcp>=2.3,<3" python tests/test_server.py .          # server の道具(このフォルダで)
```

## 分かっている制約

- 日本語の文字は、書体 `unicode` か `kst32b` で描きます。`standard` と `kochigothic` には漢字がありません
- 新しい図面の寸法は、文字の高さ $DIMTXT が 2.5 です。mm の住宅図面では `set_vars` で 100〜300 にします
- 図面が1枚も開いていないと、plugin のメニューは押せません
- 閉じたポリラインで描いた壁には端点がないため、`check_connectivity` では切れ目が出ません
- 画面の画像は、LibreCAD の表示をそのまま撮ります。小さな文字は四角で表示されます
- `stretch` は、円の中心が窓に入らないと円を動かしません。通り芯の丸印が線から離れて残ることがあり、`validate` はこれを見ません
