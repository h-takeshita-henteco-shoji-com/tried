"""マップエディターで、川が再現できるかを試す(#73)。Mod の窓口を直接呼ぶ。

手順:
  python3 river_trial.py carve  naka [width] [bank]   川筋を掘る(river_line.py の出力を使う)
  python3 river_trial.py source naka [rate] [freeboard] [count]  上流の端に水源を置く
  python3 river_trial.py watch  naka [seconds]        時間を動かし、10秒ごとに水を測る。最後に止める
  python3 river_trial.py measure naka                  今の水を1回だけ測る
  python3 river_trial.py rebridge naka                 川と交わる道路(九州自動車道など)を橋に作り替え、その場所を掘り直す
  川の名前の代わりに all と書くと、naka,mikasa,muromi,tatara の4本をまとめて扱う(naka,muromi のように並べてもよい)
  python3 river_trial.py reset                          水源を全部消し、地形を掘る前に戻す

測るもの:
  - 川筋の水深。水深0.3m未満の点を「途切れ」と数える
  - 両岸の外(川の中心から width/2 + bank + 16m)の水深。0.3m以上の点を「あふれ」と数える
"""
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = os.environ.get("AIMAYOR_URL", "http://127.0.0.1:8781")
SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
WET = 0.3


def call(path, body=None, timeout=120, **params):
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{BASE}{path}" + (f"?{q}" if q else "")
    data = body.encode() if body is not None else None
    with urllib.request.urlopen(url, data=data, timeout=timeout) as r:
        return json.loads(r.read().decode())


RIVERS = ["naka", "mikasa", "muromi", "tatara"]


def load(name):
    return json.load(open(f"{SRC}/river_{name}.json"))


def names_of(arg):
    return RIVERS if arg == "all" else arg.split(",")


def side_points(pts, offset):
    """各点で、川の向きに直角な左右 offset の位置。"""
    out = []
    for i, (x, z, _) in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        dx, dz = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dz) or 1
        nx, nz = -dz / n, dx / n
        out.append((x + nx * offset, z + nz * offset))
        out.append((x - nx * offset, z - nz * offset))
    return out


def measure(r, width=64, bank=32):
    pts = r["points"]
    center = call("/editor/water_profile", body=";".join(f"{x},{z}" for x, z, _ in pts))["points"]
    sides = call("/editor/water_profile", body=";".join(f"{x},{z}" for x, z in side_points(pts, width / 2 + bank + 16)))["points"]
    depth = [p[4] for p in center]
    dry = [i for i, d in enumerate(depth) if d < WET]
    # 両岸の外の点が、曲がった所で隣の川筋の上に来ることがある。川の中心から width/2 + bank 以内の点は数えない
    reach = width / 2 + bank
    def in_channel(px, pz):
        return any(math.hypot(px - x, pz - z) < reach for x, z, _ in pts)
    over = [i // 2 for i, p in enumerate(sides) if p[4] >= WET and not in_channel(p[0], p[1])]
    return {
        "centerDepthMin": round(min(depth), 2),
        "centerDepthMax": round(max(depth), 2),
        "dryPoints": len(dry),
        "dryFrom": dry[:1] and dry[0],
        "dryTo": dry[-1:] and dry[-1],
        "overflowPoints": len(set(over)),
        "overflowAt": sorted(set(over))[:10],
        "depthEvery10": [round(d, 2) for d in depth[::10]],
    }


def main():
    cmd = sys.argv[1]
    if cmd == "reset":
        for s in call("/editor/water_sources")["sources"]:
            call("/editor/water_source/remove", id=s["id"])
        print(call("/editor/terrain/restore"))
        return

    names = names_of(sys.argv[2] if len(sys.argv) > 2 else "naka")
    rivers = {n: load(n) for n in names}
    if cmd == "carve":
        width = float(sys.argv[3]) if len(sys.argv) > 3 else 64
        bank = float(sys.argv[4]) if len(sys.argv) > 4 else 32
        for n, r in rivers.items():
            # ゲームは地形の更新を一度に約2km四方しか反映しないので、10点(約480m)ずつ送る
            pts, changed = r["points"], 0
            for i in range(0, len(pts) - 1, 9):
                body = ";".join(f"{x},{z},{y}" for x, z, y in pts[i:i + 10])
                changed += call("/editor/carve", body=body, width=width, bank=bank)["changedPoints"]
            print(n, "changedPoints", changed)
    elif cmd == "source":
        # source <川> [上流の端の水量] [余裕] [合流地点の水量]。合流地点の水量が0なら、上流の端だけ
        rate = int(sys.argv[3]) if len(sys.argv) > 3 else 400
        freeboard = float(sys.argv[4]) if len(sys.argv) > 4 else 1.5
        join_rate = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        for n, r in rivers.items():
            spots = [(len(r["points"]) - 1, rate)]
            if join_rate > 0:
                spots += [(s["index"], join_rate) for s in r.get("sources", []) if s["index"] < len(r["points"]) - 3]
            for i, q in spots:
                # 目標の水面 = 川底 + (掘った深さ - 余裕)
                x, z, bed = r["points"][i]
                g = r["ground"][i]
                target = bed + max(0.5, (g - bed) - freeboard)
                res = call("/editor/water_source", x=x, z=z, rate=q, target=round(target, 2))
                print(n, i, res.get("id"), res.get("rate"), res.get("target"), res.get("error", ""))
    elif cmd == "rebridge":
        for n, r in rivers.items():
            body = ";".join(f"{x},{z}" for x, z, _ in r["points"])
            res = call("/editor/rebridge", body=body)
            print(n, res)
        print("掘り直す:")
        main_args = sys.argv[:]
        sys.argv = [sys.argv[0], "carve", sys.argv[2]]
        main()
        sys.argv = main_args
    elif cmd == "measure":
        for n, r in rivers.items():
            print(n, json.dumps(measure(r), ensure_ascii=False))
    elif cmd == "watch":
        seconds = int(sys.argv[3]) if len(sys.argv) > 3 else 120
        print(call("/time", paused="false"))
        t0 = time.time()
        try:
            while time.time() - t0 < seconds:
                time.sleep(10)
                for n, r in rivers.items():
                    m = measure(r)
                    print(f"{time.time() - t0:5.0f}s {n}", json.dumps(m, ensure_ascii=False), flush=True)
        finally:
            print(call("/time", paused="true"))


if __name__ == "__main__":
    main()
