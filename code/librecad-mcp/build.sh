#!/bin/zsh
# plugin を組み立てて、LibreCAD の利用者の plugin フォルダに置く。
# 使い方: code/librecad-mcp/build.sh [--restart]
#   --restart: LibreCAD を起動し直し、メニュー「プラグイン → MCP bridge」まで押す
#              (開いている図面は保存されずに閉じる。試しの図面だけのときに使う)
set -e
HERE=${0:A:h}
SRC=${LIBRECAD_SRC:-$HOME/librecad-src/lc}
BUILD=${LIBRECAD_BUILD:-$HOME/librecad-build}
QT=/opt/homebrew/opt/qt@5

mkdir -p $BUILD
cd $BUILD
LIBRECAD_SRC=$SRC $QT/bin/qmake $HERE/plugin/mcpbridge.pro
make -s

# Qt の参照先を、LibreCAD 同梱の Qt に向け直す(2つの Qt を読み込ませないため)
for f in QtWidgets QtGui QtNetwork QtCore; do
  install_name_tool -change $QT/lib/$f.framework/Versions/5/$f \
    @executable_path/../Frameworks/$f.framework/Versions/5/$f libmcpbridge.dylib 2>/dev/null
done
codesign -f -s - libmcpbridge.dylib

mkdir -p ~/Documents/LibreCAD/plugins
cp libmcpbridge.dylib ~/Documents/LibreCAD/plugins/
echo "installed: ~/Documents/LibreCAD/plugins/libmcpbridge.dylib"

if [[ "$1" == "--restart" ]]; then
  $HERE/restart.sh
fi
