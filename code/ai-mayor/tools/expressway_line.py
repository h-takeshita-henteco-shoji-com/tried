"""九州自動車道の線と、区間ごとの構造(高架か地上か)を作る(#73)。

国土地理院ベクトルタイルの道路中心線(fetch_expressways.py を FULL=1 で取得)から、九州自動車道だけを取り出す。
データには路線名がないので、川と同じく、通るはずの地点(インターチェンジなど)を順にたどる。
区間の構造は、データの state(通常部 / 橋・高架 / トンネル)をそのまま使う。

出力: ~/.cache/ai-mayor-dem/expressway_kyushu.json
  points: [[x, z], ...](ゲーム上の座標、m)。北の端から南の端へ
  elevated: 各点が「橋・高架」の区間にあるか
使い方: python3 expressway_line.py
出典: 国土地理院ベクトルタイル(道路中心線)を加工して作成
"""
import heapq
import json
import math
import os

SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
CENTER = (33.59018, 130.40987)
R = 6371008.8
STEP = 48.0
EDGE = 8600.0
MAIN_WIDTHS = {"5.5m-13m未満", "13m-19.5m未満", "19.5m以上"}  # 本線。ランプ(5.5m未満)は外す
HEIGHT = 10.0      # 高架の高さ(地面から、m)
RAMP = 5           # 地上と高架の間を上げ下げする点の数(48m × 5 = 240m。勾配は約4%)
LOOP_ALONG = 150.0  # 寄り道とみなす、線に沿って進んだ長さの下限(m)
LOOP_NEAR = 40.0    # 寄り道とみなす、戻ってきた点の近さ(m)。上りと下りの間隔(約26m)より少し広い
GROUND_PTS = 6     # all のとき、インターチェンジの前後と地図の端で地上にする点の数(約290m)

# 北から南へ、通るはずの地点(ゲーム座標)。地図に高速道路の線を描いて読み取った(緯度経度で推測すると外れた)
ROUTE = [
    (5200.0, 8400.0),    # 北の端の手前(古賀の方)
    (3360.0, 3840.0),    # 途中(久山の方)
    (3648.0, 2208.0),    # 福岡インター
    (4160.0, -960.0),    # 途中
    (3888.0, -3280.0),   # 太宰府インター
    (5680.0, -8500.0),   # 南の端の手前(筑紫野の方)
]


def to_game(lat, lon):
    north = math.radians(lat - CENTER[0]) * R
    east = math.radians(lon - CENTER[1]) * R * math.cos(math.radians(lat))
    return east / 2, north / 2


def load_graph():
    feats = json.load(open(f"{SRC}/expressways_full.geojson"))["features"]
    adj, main = {}, set()
    for f in feats:
        p = f["properties"]
        if f["geometry"]["type"] != "LineString":
            continue
        # 本線の幅の区分でない区間(ランプなど)も、途切れを埋めるために使う。ただし通りにくくする
        weight = 1.0 if p.get("rnkWidth") in MAIN_WIDTHS else 5.0
        elevated = p.get("state") == "橋・高架"
        keys = [(round(x, 1), round(z, 1)) for x, z in (to_game(lat, lon) for lon, lat in f["geometry"]["coordinates"])]
        if weight == 1.0:
            main.update(keys)
        for a, b in zip(keys, keys[1:]):
            d = math.dist(a, b) * weight
            adj.setdefault(a, []).append((b, d, elevated))
            adj.setdefault(b, []).append((a, d, elevated))
    # タイルの境目で途切れた端どうしを、5m以内ならつなぐ
    cell = {}
    for k in adj:
        cell.setdefault((int(k[0] // 5), int(k[1] // 5)), []).append(k)
    for (cx, cz), ks in cell.items():
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for a in ks:
                    for b in cell.get((cx + dx, cz + dz), []):
                        if a < b and math.dist(a, b) <= 5 and all(n != b for n, _, _ in adj[a]):
                            adj[a].append((b, math.dist(a, b), False))
                            adj[b].append((a, math.dist(a, b), False))
    return adj, main


def shortest(adj, a, b):
    dist, prev = {a: 0.0}, {}
    heap = [(0.0, a)]
    while heap:
        d, u = heapq.heappop(heap)
        if u == b:
            break
        if d > dist[u]:
            continue
        for v, w, e in adj[u]:
            if d + w < dist.get(v, 1e18):
                dist[v], prev[v] = d + w, (u, e)
                heapq.heappush(heap, (d + w, v))
    if b not in dist:
        raise SystemExit(f"つながらない: {a} -> {b}")
    path, flags = [b], []
    while path[-1] != a:
        u, e = prev[path[-1]]
        path.append(u)
        flags.append(e)
    return path[::-1], flags[::-1]


def main():
    adj, main = load_graph()
    nodes, snaps = [], []
    for p in ROUTE:
        # 通る地点は本線の点に寄せる。ランプの点に寄せると、ランプを回って戻る輪ができる(#77、福岡インター)
        k = min(main, key=lambda k: math.dist(k, p))
        nodes.append(k)
        snaps.append(round(math.dist(k, p)))
    path, flags = [nodes[0]], []
    for a, b in zip(nodes, nodes[1:]):
        pa, fa = shortest(adj, a, b)
        path += pa[1:]
        flags += fa

    # 同じ点を2度通ったら、その間の寄り道(ランプへ入って戻る)を取り除く
    clean, cflags, seen = [path[0]], [], {path[0]: 0}
    for k, e in zip(path[1:], flags):
        if k in seen:
            cut = seen[k]
            clean, cflags = clean[:cut + 1], cflags[:cut]
            seen = {n: i for i, n in enumerate(clean)}
            continue
        seen[k] = len(clean)
        clean.append(k)
        cflags.append(e)
    path, flags = clean, cflags

    # 近くの点に戻ってきた寄り道も取り除く(#77)。福岡インターでは、行きと帰りで別の点を通り、上の処理で残った。
    # 線に沿って LOOP_ALONG m 以上進んだのに、前の点から LOOP_NEAR m 以内に戻っていたら、その間を寄り道とみなす
    i = 0
    while i < len(path):
        along, cut = 0.0, None
        for j in range(i + 1, len(path)):
            along += math.dist(path[j - 1], path[j])
            if along >= LOOP_ALONG and math.dist(path[i], path[j]) <= LOOP_NEAR:
                cut = j
        if cut is not None:
            path, flags = path[:i + 1] + path[cut + 1:], flags[:i] + flags[cut:]
        i += 1

    # 48m おきに点を打ち、各点の構造は、その点を含む区間の構造にする
    pts, elev = [path[0]], [flags[0] if flags else False]
    carry = 0.0
    for (a, b), e in zip(zip(path, path[1:]), flags):
        seg = math.dist(a, b)
        t = STEP - carry
        while t <= seg:
            pts.append((a[0] + (b[0] - a[0]) * t / seg, a[1] + (b[1] - a[1]) * t / seg))
            elev.append(e)
            t += STEP
        carry = seg - (t - STEP)
    pts.append(path[-1])
    elev.append(flags[-1] if flags else False)

    # 地図の内側だけにする
    keep = [i for i, (x, z) in enumerate(pts) if max(abs(x), abs(z)) <= EDGE]
    pts = [pts[i] for i in keep]
    elev = [elev[i] for i in keep]
    length = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))

    # 点ごとの地面からの高さ(m)を、2つのやり方で出す。高さは前後 RAMP 点かけて上げ下げする
    def heights(flags):
        h = [HEIGHT if f else 0.0 for f in flags]
        out = h[:]
        for i in range(len(h)):
            # いちばん近い「高架でない点」までの点の数で、ランプにする
            if h[i] == 0.0:
                continue
            near = min((abs(i - j) for j in range(max(0, i - RAMP), min(len(h), i + RAMP + 1)) if h[j] == 0.0), default=RAMP)
            out[i] = HEIGHT * min(1.0, near / RAMP)
        # 高架の前後も、ランプの分だけ持ち上げる(高架に入る手前で上り始める)
        for i in range(len(h)):
            if h[i] == 0.0:
                near = min((abs(i - j) for j in range(max(0, i - RAMP), min(len(h), i + RAMP + 1)) if h[j] > 0.0), default=None)
                if near is not None:
                    out[i] = max(out[i], HEIGHT * (1 - near / RAMP))
        return [round(v, 1) for v in out]

    # data: データの「橋・高架」だけ高架。all: インターチェンジの前後と地図の端だけ地上
    ics = [min(range(len(pts)), key=lambda i: math.dist(pts[i], p)) for p in (ROUTE[2], ROUTE[4])]
    all_flags = [not (i < GROUND_PTS or i >= len(pts) - GROUND_PTS or any(abs(i - c) <= GROUND_PTS for c in ics))
                 for i in range(len(pts))]
    out = {
        "points": [[round(x, 1), round(z, 1)] for x, z in pts],
        "elevated": elev,
        "heightData": heights(elev),
        "heightAll": heights(all_flags),
        "interchanges": ics,
        "snap": snaps,
    }
    json.dump(out, open(f"{SRC}/expressway_kyushu.json", "w"))
    print(f"{len(pts)} points, {length / 1000:.1f}km(game), elevated {sum(elev) / len(elev):.0%}, snap {snaps}")
    print("north end", out["points"][0], "south end", out["points"][-1])


if __name__ == "__main__":
    main()
