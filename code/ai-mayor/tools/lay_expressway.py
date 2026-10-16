"""マップエディターで、九州自動車道を引く(#73)。Mod の窓口を直接呼ぶ。

expressway_line.py の出力を使い、上りと下りの2本の一方通行で引く。
- 中心線から左右 OFFSET m ずつずらす。左側通行(日本)の並び: 南へ向かう車線が東側、北へ向かう車線が西側
- 点ごとの地面からの高さは、data(データの「橋・高架」だけ高架)か all(インターチェンジの前後と地図の端だけ地上)
- 両端は地図の端まで延ばし、つなぎ口(Highway Connection)にする

使い方: python3 lay_expressway.py data|all
"""
import json
import math
import os
import sys
import urllib.parse
import urllib.request

BASE = os.environ.get("AIMAYOR_URL", "http://127.0.0.1:8781")
SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
OFFSET = 13.0
EDGE = 8620.0     # 地図の端(±8640)の少し内側。つなぎ口の道具が、端の外へ動かす
LOOK = 5          # 端の向きを測るとき、何点内側の点を使うか(約240m)
TRIM_NORTH = 6    # 北の端のデータで使わない点の数
EDGE_GAP = 15.0   # 地図の端で、上りと下りを中心線から東西に離す距離


def call(path, body=None, timeout=180, **params):
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{BASE}{path}" + (f"?{q}" if q else "")
    with urllib.request.urlopen(url, data=body.encode() if body is not None else None, timeout=timeout) as r:
        return json.loads(r.read().decode())


def offset_line(pts, d):
    """進む向きの左側へ d m ずらした線。"""
    out = []
    for i, (x, z) in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        dx, dz = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dz) or 1
        out.append((x - dz / n * d, z + dx / n * d))
    return out


def to_edge(inner, outer):
    """inner から outer の向きへ延ばし、地図の端の手前(EDGE)に届く点を返す。"""
    dx, dz = outer[0] - inner[0], outer[1] - inner[1]
    n = math.hypot(dx, dz) or 1
    ux, uz = dx / n, dz / n
    t = 0.0
    while max(abs(outer[0] + ux * t), abs(outer[1] + uz * t)) < EDGE:
        t += 4.0
    return (outer[0] + ux * t, outer[1] + uz * t)


def extend_to_edge(pts, heights):
    """中心線の両端を、地図の端の手前(EDGE)まで 48m おきに延ばす。
    向きは、端から LOOK 点内側の点から測る(データの端の1区間は向きが乱れていることがあるため)。"""
    def ext(end, inner):
        dx, dz = end[0] - inner[0], end[1] - inner[1]
        n = math.hypot(dx, dz) or 1
        ux, uz = dx / n, dz / n
        out, t = [], 48.0
        while max(abs(end[0] + ux * t), abs(end[1] + uz * t)) < EDGE:
            out.append((end[0] + ux * t, end[1] + uz * t))
            t += 48.0
        out.append(to_edge(end, (end[0] + ux * t, end[1] + uz * t)) if out else to_edge(inner, end))
        return out
    head = ext(pts[0], pts[min(LOOK, len(pts) - 1)])[::-1]
    tail = ext(pts[-1], pts[max(len(pts) - 1 - LOOK, 0)])
    return head + pts + tail, [0.0] * len(head) + heights + [0.0] * len(tail)


def lay(pts, heights, name):
    """pts の順が進む向き。pts の最初と最後は地図の端の点。そこをつなぎ口にする。"""
    heights = heights[:]
    for i in (0, 1, 2, -1, -2, -3):
        heights[i] = 0.0  # 地図の端は地上
    # つなぎ口の線の内側の点は、地図の端から60m以上離す。50m以内だと、つなぎ口の道具がその点にも「外」の印を付けるため
    def far(p):
        return 8640 - max(abs(p[0]), abs(p[1])) >= 60
    s = next(i for i in range(1, len(pts)) if far(pts[i]))
    e = next(i for i in range(len(pts) - 2, 0, -1) if far(pts[i]))
    body = ";".join(f"{x:.1f},{z:.1f},{h:.1f}" for (x, z), h in zip(pts[s:e + 1], heights[s:e + 1]))
    main = call("/net/build", body=body, prefab="Highway", pay="false")
    print(name, "main", {k: main.get(k) for k in ("ok", "nodes", "segments", "snapped", "split", "error")})
    a = call("/editor/outside", body=f"{pts[0][0]:.1f},{pts[0][1]:.1f};{pts[s][0]:.1f},{pts[s][1]:.1f}", prefab="Highway")
    b = call("/editor/outside", body=f"{pts[e][0]:.1f},{pts[e][1]:.1f};{pts[-1][0]:.1f},{pts[-1][1]:.1f}", prefab="Highway")
    for label, r in (("start", a), ("end", b)):
        print(name, label, {k: r.get(k) for k in ("ok", "connectionPrefab", "markedNodes", "error")})


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "data"
    e = json.load(open(f"{SRC}/expressway_kyushu.json"))
    pts = [tuple(p) for p in e["points"]]  # 北から南へ
    h = e["heightData" if mode == "data" else "heightAll"]
    # 北の端のデータは、最初の数点がランプのように折り返している。使わない
    pts, h = pts[TRIM_NORTH:], h[TRIM_NORTH:]
    pts, h = extend_to_edge(pts, h)
    print("center line", len(pts), "points, ends", [round(v) for v in pts[0]], [round(v) for v in pts[-1]])
    south = offset_line(pts, OFFSET)                       # 南へ向かう車線(左側 = 東)
    north_pts = pts[::-1]
    north = offset_line(north_pts, OFFSET)                 # 北へ向かう車線(左側 = 西)
    # 地図の端の点は、中心線の端から東西に EDGE_GAP m ずつ離す(斜めにずらすと、端で2本が寄り集まるため)
    (nx, nz), (sx, sz) = pts[0], pts[-1]
    south[0], south[-1] = (nx + EDGE_GAP, nz), (sx + EDGE_GAP, sz)
    north[0], north[-1] = (sx - EDGE_GAP, sz), (nx - EDGE_GAP, nz)
    lay(south, h, "southbound")
    lay(north, h[::-1], "northbound")
    print(call("/editor/state")["outsideConnections"])


if __name__ == "__main__":
    main()
