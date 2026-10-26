"""OBS の録画を、この端末から始める・止める・確かめる(#103)。

OBS の WebSocket サーバー(ツール > WebSocket サーバー設定)を使う。
パスワードはリポジトリに置かない。OBS の設定ファイルから読む。

使い方:
  uv run --with obsws-python python code/ai-mayor/tools/obs_record.py status
  uv run --with obsws-python python code/ai-mayor/tools/obs_record.py start ~/ai-mayor-recordings/base
  uv run --with obsws-python python code/ai-mayor/tools/obs_record.py stop
  uv run --with obsws-python python code/ai-mayor/tools/obs_record.py pause
  uv run --with obsws-python python code/ai-mayor/tools/obs_record.py resume

start は、録画の置き場所を渡したフォルダにしてから始める。stop は、できたファイルのパスを返す。
pause と resume は、月と月の間の待ち時間を録画に入れないために足した。ただし今の設定(簡易モードで、録画を配信と同じ設定で書く)では
OBS が一時停止を受け付けない(pause は ok を返すが止まらない)。月ごとに stop と start で別のファイルにする。
設定(2026-10-25 に入れた): ゲームの窓だけ(macOS 画面キャプチャのウィンドウ)、横1920・毎秒30コマ、6000kbps、断片化 MP4。
"""
import json
import os
import sys
from pathlib import Path

import obsws_python as obs

CONFIG = Path.home() / "Library/Application Support/obs-studio/plugin_config/obs-websocket/config.json"


def client() -> obs.ReqClient:
    conf = json.loads(CONFIG.read_text())
    if not conf.get("server_enabled"):
        sys.exit("OBS の WebSocket サーバーが無効。ツール > WebSocket サーバー設定で有効にする")
    return obs.ReqClient(host="127.0.0.1", port=conf.get("server_port", 4455),
                         password=conf.get("server_password", ""), timeout=10)


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    c = client()
    if cmd == "start":
        folder = os.path.expanduser(sys.argv[2]) if len(sys.argv) > 2 else os.path.expanduser("~/ai-mayor-recordings")
        os.makedirs(folder, exist_ok=True)
        c.set_record_directory(folder)
        c.start_record()
        print(json.dumps({"ok": True, "recording": True, "directory": folder}, ensure_ascii=False))
    elif cmd == "pause":
        c.pause_record()
        print(json.dumps({"ok": True, "paused": True}, ensure_ascii=False))
    elif cmd == "resume":
        c.resume_record()
        print(json.dumps({"ok": True, "paused": False}, ensure_ascii=False))
    elif cmd == "stop":
        r = c.stop_record()
        print(json.dumps({"ok": True, "recording": False, "file": r.output_path}, ensure_ascii=False))
    else:
        s = c.get_record_status()
        v = c.get_video_settings()
        print(json.dumps({"ok": True, "recording": s.output_active, "paused": s.output_paused, "duration": s.output_timecode,
                          "bytes": s.output_bytes, "directory": c.get_record_directory().record_directory,
                          "output": f"{v.output_width}x{v.output_height}@{v.fps_numerator}"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
