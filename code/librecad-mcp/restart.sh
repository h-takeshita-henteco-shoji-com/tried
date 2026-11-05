#!/bin/zsh
# LibreCAD を起動し直し、メニュー「プラグイン → MCP bridge」まで押す。
# 開いている図面は保存されずに閉じる。試しの図面だけのときに使う。
# 終了の直後に起動を頼むと、macOS が受け付けないことがある。起動を確かめて、だめならやり直す。

MENU='menu item "MCP bridge" of menu 1 of menu bar item "プラグイン" of menu bar 1'

stop_librecad() {
  pkill -f "MacOS/LibreCAD" || true
  for i in {1..20}; do pgrep -f "MacOS/LibreCAD" >/dev/null || break; sleep 0.5; done
  pkill -9 -f "MacOS/LibreCAD" 2>/dev/null || true
  sleep 1.5
}

start_librecad() {
  for attempt in 1 2 3; do
    open -a LibreCAD
    for i in {1..30}; do
      osascript -e "tell application \"System Events\" to exists $MENU of process \"LibreCAD\"" 2>/dev/null | grep -q true && return 0
      sleep 0.5
    done
    stop_librecad
  done
  return 1
}

stop_librecad
start_librecad || { echo "LibreCAD did not start" >&2; exit 1; }
sleep 1
# plugin のメニューは、図面が1枚もないと押せない。図面がなければ新規を開く
osascript -e "tell application \"System Events\" to tell process \"LibreCAD\"
  if not (enabled of $MENU) then
    click menu item \"新規\" of menu 1 of menu bar item \"ファイル\" of menu bar 1
    delay 1
  end if
  click $MENU
end tell" >/dev/null
for i in {1..20}; do
  lsof -iTCP:7471 -sTCP:LISTEN >/dev/null && { echo "listening on 127.0.0.1:7471"; exit 0; }
  sleep 0.5
done
echo "MCP bridge did not start" >&2
exit 1
