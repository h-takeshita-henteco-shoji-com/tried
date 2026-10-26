"""出発点の街を、真上から格子状に撮る(地図の素材)。MCP を通さず MOD の窓口を直接呼ぶ。

撮り方は #89 の地図(10-21 の assets/scripts/stitch_map.py)と同じ: size 4000、pitch 90、yaw 0。
写真は tiles/ に置く。リポジトリには入れない(使い終えたら外へ移す)。
"""
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:8781"
HERE = Path(__file__).resolve().parent.parent
XS = range(-2500, 4501, 1500)
ZS = range(-1800, 2101, 1300)


def call(path, **p):
    q = urllib.parse.urlencode(p)
    with urllib.request.urlopen(f"{BASE}{path}?{q}", timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    out = HERE / "tiles"
    out.mkdir(exist_ok=True)
    info = call("/info")
    print(info.get("date"), info.get("population"))
    centers = {}
    for x in XS:
        for z in ZS:
            cam = call("/camera", x=x, z=z, size=4000, pitch=90, yaw=0)
            if not cam.get("ok"):
                sys.exit(f"camera failed {x},{z}: {cam}")
            time.sleep(1.0)
            shot = call("/screenshot", view="current")
            dest = out / f"tile_{x}_{z}.jpg"
            subprocess.run(["sips", "-s", "format", "jpeg", "-Z", "1512", shot["path"], "--out", str(dest)],
                           check=True, capture_output=True)
            cur = cam.get("current", {})
            # 地図の端では、ゲームが見る場所をずらす。実際に見ている点でつなぐ
            centers[dest.name] = [cur.get("x", x), cur.get("z", z)]
            print(dest.name, cur.get("offset"))
    (out / "centers.json").write_text(json.dumps(centers, indent=1))


if __name__ == "__main__":
    main()
