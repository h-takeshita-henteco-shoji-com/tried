"""月例の前の定点の写真を、決まった4か所で撮る(#103。council-design.md の10.7)。

親が毎月呼ぶ。MCP を通さず MOD の窓口を直接呼ぶので、画像を会話に読み込まない。

使い方:
  python3 code/ai-mayor/tools/fixed_photos.py <運営のフォルダ> <月(数)>
例:
  python3 code/ai-mayor/tools/fixed_photos.py 2026/10-25-...-02-基準の市長に12か月任せて録画する 2
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request

BASE = os.environ.get("AIMAYOR_URL", "http://127.0.0.1:8781")

# 場所: (x, z, size, pitch, yaw)。council-design.md の10.7
SPOTS = {
    "west": (-2000, -1000, 4000, 60, 0),
    "east": (2200, -600, 4000, 60, 0),
    "cargo": (3300, -1450, 1000, 45, 0),
    "center-east": (1900, 350, 1500, 50, 0),
}


def call(path: str, **params) -> dict:
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    with urllib.request.urlopen(f"{BASE}{path}?{q}", timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> None:
    folder, month = sys.argv[1], int(sys.argv[2])
    out = os.path.join(folder, "assets", "fixed")
    os.makedirs(out, exist_ok=True)
    info = call("/info")
    print(f"date {info.get('date')} population {info.get('population')}")
    for name, (x, z, size, pitch, yaw) in SPOTS.items():
        cam = call("/camera", x=x, z=z, size=size, pitch=pitch, yaw=yaw)
        if not cam.get("ok"):
            sys.exit(f"camera failed at {name}: {cam}")
        time.sleep(0.5)
        shot = call("/screenshot", view="current")
        if not shot.get("ok"):
            sys.exit(f"screenshot failed at {name}: {shot}")
        dest = os.path.join(out, f"m{month:02d}-{name}.jpg")
        # ゲームの画面の幅(1512)に縮めて JPEG にする
        subprocess.run(["sips", "-s", "format", "jpeg", "-Z", "1512", shot["path"], "--out", dest],
                       check=True, capture_output=True)
        print(dest)


if __name__ == "__main__":
    main()
