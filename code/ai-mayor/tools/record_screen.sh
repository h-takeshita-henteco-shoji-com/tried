#!/bin/zsh
# ゲームの窓だけを、小さい動画で録画する(#103)。
# macOS の画面収録(Cmd+Shift+5)は大きさとコマの数を選べず、1時間で約35GBになった。
# ffmpeg で画面を取り込み、ゲームの窓の位置で切り抜き、横1920・毎秒30コマ・HEVC 6Mbps で書く。1時間で約2.7GB。
#
# 使い方:
#   code/ai-mayor/tools/record_screen.sh ~/ai-mayor-recordings/base/base-20261025-1800.mp4
# 止めるときは、この端末で q を押すか Ctrl+C。途中で落ちても、それまでの分は再生できる形(断片化した mp4)で書く。
#
# 注意:
# - 画面そのものを取り込むので、ゲームの窓の上にほかの窓を重ねない
# - 端末に「画面収録」の許可が要る(システム設定 > プライバシーとセキュリティ > 画面収録)
# - ゲームの窓を動かしたら、録画を止めて始め直す(切り抜く位置は始めたときに決まる)
set -e

out="${1:?録画のファイル名を渡す(.mp4)}"
mkdir -p "$(dirname "$out")"

# 画面の番号(ffmpeg -f avfoundation -list_devices true -i "" の Capture screen 0)
screen="${AIMAYOR_SCREEN:-$(ffmpeg -hide_banner -f avfoundation -list_devices true -i "" 2>&1 | sed -n 's/.*\[\([0-9]*\)\] Capture screen 0.*/\1/p' | head -1)}"

# ゲームの窓の位置と大きさ(ポイント)。Retina は2倍の画素
bounds=$(osascript -e 'tell application "System Events" to tell process "Cities" to get {position, size} of window 1')
read x y w h <<< "$(echo "$bounds" | tr -d ' ' | tr ',' ' ')"
scale="${AIMAYOR_SCREEN_SCALE:-2}"
cx=$((x * scale)); cy=$((y * scale)); cw=$((w * scale)); ch=$((h * scale))
# HEVC は幅と高さを偶数にする
cw=$((cw / 2 * 2)); ch=$((ch / 2 * 2))

echo "画面 $screen、窓 ${w}x${h}@${x},${y} → 切り抜き ${cw}x${ch}+${cx}+${cy} → $out"
exec ffmpeg -hide_banner -f avfoundation -capture_cursor 0 -framerate 30 -i "${screen}:none" \
  -vf "crop=${cw}:${ch}:${cx}:${cy},scale=1920:-2" \
  -c:v hevc_videotoolbox -b:v 6M -tag:v hvc1 -movflags +frag_keyframe+empty_moov "$out"
