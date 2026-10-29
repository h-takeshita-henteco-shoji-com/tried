"""マップを格子状に測り、陸地と海の分布を作る(#124。読むだけ)。

ゲームの窓口の /height を、格子の点ごとに呼ぶ。地面が水面より高ければ陸地、そうでなければ水。
    python3 code/ai-mayor/tools/scan_map.py --step 288 --out /tmp/mapscan/grid.json
"""
import argparse, json, time, urllib.request

BASE = "http://127.0.0.1:8781"
HALF = 8640


def height(x, z):
    with urllib.request.urlopen(f"{BASE}/height?x={x}&z={z}", timeout=15) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", type=int, default=288)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    xs = list(range(-HALF, HALF + 1, a.step))
    zs = list(range(HALF, -HALF - 1, -a.step))  # 北の行から
    t = time.time()
    grid = []
    for z in zs:
        row = []
        for x in xs:
            try:
                h = height(x, z)
                row.append([round(h["ground"], 1), round(h["water"], 1)])
            except Exception:
                row.append(None)
        grid.append(row)
    json.dump({"step": a.step, "xs": xs, "zs": zs, "grid": grid}, open(a.out, "w"))
    print(f"{len(xs)}x{len(zs)} 点、{time.time() - t:.0f} 秒")


if __name__ == "__main__":
    main()
