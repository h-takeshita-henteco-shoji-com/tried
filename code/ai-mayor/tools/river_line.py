"""川の本流の線と、川底の高さを作る(#73 の川の検証)。

河川中心線(fetch_rivers.py で取得)には川の名前がない。そこで、河口の地点から線をたどり、
いちばん遠くまで続く道筋を本流とみなす。
川底は、上流から河口へ向かって一様に下がるようにする(途中に高い所が残ると水が切れるため、#64)。
河口側で地面が低い区間は、川底を海面より下げて海の水を入れる(潮の入る川)。

出力: ~/.cache/ai-mayor-dem/river_<名前>.json
  points: [[x, z, 川底の高さ], ...](ゲーム上の座標、m)。carve_channel にそのまま渡せる
  ground: 各点の元の地面の高さ

使い方: python3 river_line.py naka   (all で全部。河口の緯度経度は MOUTHS に書く)
出典: 国土地理院ベクトルタイル(河川中心線)を加工して作成
"""
import heapq
import json
import math
import os
import sys

import numpy as np
from PIL import Image

SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
HEIGHTMAP = f"{SRC}/heightmaps/fukuoka_h2_v050_o4.png"  # 今のマップの元の高さマップ
CENTER = (33.59018, 130.40987)
R = 6371008.8
N = 1081
SEA_LEVEL = 40.0
TIDAL_BED = SEA_LEVEL - 4.0     # 潮の入る区間の川底
TIDAL_GROUND = SEA_LEVEL + 8.0  # 元の地面がこれより低い区間は、潮の入る川にする
DEPTH = 4.0                     # 上流の川底を、地面からどれだけ下げるか
MIN_SLOPE = 0.0005              # 川底の最小の勾配(1kmで0.5m下がる)
STEP = 48.0                     # 出力する点の間隔(ゲーム上m)

RAMP = 25                       # 潮の入る区間の上端から、上流の川底へなだらかにつなぐ点の数(約1.2km)
EDGE = 8400.0                   # 地図の端(±8640)より内側の点だけを使う
SNAP_SIDE = 80                  # 上流の点を谷底へ寄せるときに探す左右の幅(ゲーム上m)
TRIB_MIN = 1000.0               # 合流地点に水源を置く支流の長さの下限(ゲーム上m)
MAX_GROUND = 100.0              # 元の地面がこれより高い山の区間は、川として掘らない

# 川ごとに、河口と、本流が通るはずの地点(緯度経度、またはゲーム座標)を上流へ順に並べる。
# 平野では川どうしが細い水路でつながっているので、地点を決めないと別の川へ迷い込む(#73)。
# 最後の地点から先は、いちばん遠くまで続く道筋で上流へ延ばす。
ROUTES = {
    "naka": [(33.6003, 130.3975), (33.5000, 130.4230)],                        # 中洲の北 → 那珂川市
    "mikasa": [(33.6085, 130.4085), (33.5905, 130.4290), (33.5300, 130.4800),
               (33.5130, 130.5270)],                                            # 博多港の東 → 博多駅の東 → 大野城 → 太宰府
    "muromi": [(33.5935, 130.3490), (33.5600, 130.3460), (33.5120, 130.3310),
               (33.4700, 130.3050)],                                            # 百道の西 → 早良区 → 内野 → 曲渕
    "tatara": [(520.0, 2880.0), (33.6230, 130.4500), (33.6150, 130.5200)],      # 名島 → 粕屋 → 篠栗
}
MOUTHS = {k: v[0] for k, v in ROUTES.items()}
JOIN = 5.0                      # タイルの境目で途切れた線の端どうしを、この距離(ゲーム上m)以内ならつなぐ


def to_game(lat, lon):
    """緯度経度をゲーム上の座標に直す。水平1/2縮尺(server.py の latlon_to_game と同じ)。"""
    north = math.radians(lat - CENTER[0]) * R
    east = math.radians(lon - CENTER[1]) * R * math.cos(math.radians(lat))
    return east / 2, north / 2


def load_graph():
    # 地図全体のデータ(fetch_rivers.py を FULL=1 で実行)があれば、それを使う
    path = f"{SRC}/rivers_full.geojson" if os.path.exists(f"{SRC}/rivers_full.geojson") else f"{SRC}/rivers.geojson"
    feats = json.load(open(path))["features"]
    adj = {}
    for f in feats:
        if f["geometry"]["type"] != "LineString":
            continue
        kind = f["properties"].get("type")
        pts = [to_game(lat, lon) for lon, lat in f["geometry"]["coordinates"]]
        # 本流の線の途中に、短い細河川が挟まっていることがある。40m以下の細河川だけを、つなぎとして使う
        if kind != "河川中心線（通常部）" and not (kind == "細河川（通常部）" and
                                                   sum(math.dist(a, b) for a, b in zip(pts, pts[1:])) <= 40):
            continue
        keys = [(round(x, 1), round(z, 1)) for x, z in pts]
        weight = 1.0 if kind == "河川中心線（通常部）" else 3.0  # つなぎの細河川は、なるべく通らない
        for a, b in zip(keys, keys[1:]):
            if max(abs(a[0]), abs(a[1]), abs(b[0]), abs(b[1])) > EDGE:
                continue
            d = math.dist(a, b) * weight
            adj.setdefault(a, []).append((b, d))
            adj.setdefault(b, []).append((a, d))

    # 近い点どうしをつなぐ(タイルの境目で線が途切れているため)
    cell = {}
    for k in adj:
        cell.setdefault((int(k[0] // JOIN), int(k[1] // JOIN)), []).append(k)
    joined = 0
    for (cx, cz), ks in cell.items():
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for a in ks:
                    for b in cell.get((cx + dx, cz + dz), []):
                        if a < b and math.dist(a, b) <= JOIN and all(n != b for n, _ in adj[a]):
                            adj[a].append((b, math.dist(a, b)))
                            adj[b].append((a, math.dist(a, b)))
                            joined += 1
    print(f"graph: {len(adj)} nodes, joined {joined}")
    return adj


def component_sizes(adj):
    size, seen = {}, set()
    for k in adj:
        if k in seen:
            continue
        stack, comp = [k], []
        seen.add(k)
        while stack:
            u = stack.pop()
            comp.append(u)
            for v, _ in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        for u in comp:
            size[u] = len(comp)
    return size


def dijkstra(adj, start):
    dist, prev = {start: 0.0}, {}
    heap = [(0.0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist.get(v, 1e18):
                dist[v], prev[v] = d + w, u
                heapq.heappush(heap, (d + w, v))
    return dist, prev


def trace(prev, start, end):
    path = [end]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return path[::-1]


def main_stem(adj, route):
    """河口から地点を順にたどり、最後の地点から先はいちばん遠い点まで延ばした道筋(河口が先頭)。
    地点は、200点以上つながった線のいちばん近い点に吸い付ける。"""
    size = component_sizes(adj)
    snaps, nodes = [], []
    for p in route:
        k = min((k for k in adj if size[k] >= 200), key=lambda k: math.dist(k, p))
        snaps.append(math.dist(k, p))
        nodes.append(k)
    path = [nodes[0]]
    for a, b in zip(nodes, nodes[1:]):
        dist, prev = dijkstra(adj, a)
        if b not in dist:
            raise SystemExit(f"地点 {b} へつながらない")
        path += trace(prev, a, b)[1:]
    # 最後の地点から先: すでに通った点は使わずに、いちばん遠い点まで
    used = set(path[:-1])
    sub = {k: [(v, w) for v, w in vs if v not in used] for k, vs in adj.items() if k not in used}
    dist, prev = dijkstra(sub, nodes[-1])
    far = max(dist, key=dist.get)
    path += trace(prev, nodes[-1], far)[1:]
    # 同じ点を2度通ったら、その間の寄り道(支流へ入って戻る行き止まり)を取り除く
    clean, seen = [], {}
    for k in path:
        if k in seen:
            del clean[seen[k] + 1:]
            seen = {n: i for i, n in enumerate(clean)}
            continue
        seen[k] = len(clean)
        clean.append(k)
    path = clean
    length = sum(math.dist(a, b) for a, b in zip(path, path[1:]))
    return path, max(snaps), length


def resample(path, step):
    out = [path[0]]
    carry = 0.0
    for a, b in zip(path, path[1:]):
        seg = math.dist(a, b)
        t = step - carry
        while t <= seg:
            out.append((a[0] + (b[0] - a[0]) * t / seg, a[1] + (b[1] - a[1]) * t / seg))
            t += step
        carry = seg - (t - step)
    if math.dist(out[-1], path[-1]) > 1:
        out.append(path[-1])
    return out


def ground_at(hm, x, z):
    """高さマップから、ゲーム上の (x, z) の地面の高さ(m)を補間して返す。上が北。"""
    col = x / 16 + (N - 1) / 2
    row = (N - 1) / 2 - z / 16
    c0, r0 = int(math.floor(col)), int(math.floor(row))
    fc, fr = col - c0, row - r0
    v = (hm[r0, c0] * (1 - fc) * (1 - fr) + hm[r0, c0 + 1] * fc * (1 - fr)
         + hm[r0 + 1, c0] * (1 - fc) * fr + hm[r0 + 1, c0 + 1] * fc * fr)
    return float(v) / 65535 * 1024


def main():
    names = sys.argv[1:] or ["naka"]
    if names == ["all"]:
        names = list(MOUTHS)
    # 先に作った川の道筋は、後の川では通れないようにする(細いつなぎを通って別の川へ迷い込まないため)
    adj = load_graph()
    for name in names:
        path = build(name, adj)
        for k in path[1:]:
            for v, _ in adj.pop(k, []):
                adj[v] = [(n, d) for n, d in adj.get(v, []) if n != k]


def confluences(adj, path, min_len):
    """本流の道筋に、長さ min_len 以上の支流がつながる点を返す(点、支流の長さ)。"""
    on_path = set(path)
    found = []
    for k in path:
        for v, _ in adj.get(k, []):
            if v in on_path:
                continue
            # 支流を、本流に戻らずにたどれるだけたどって長さを測る(上限 5km)
            seen, stack, total = {k, v}, [v], 0.0
            while stack and total < 5000:
                u = stack.pop()
                for w, d in adj.get(u, []):
                    if w not in seen and w not in on_path:
                        seen.add(w)
                        stack.append(w)
                        total += d
            if total >= min_len:
                found.append((k, total))
    return found


def build(name, adj):
    route = [to_game(a, b) if abs(a) < 90 else (a, b) for a, b in ROUTES[name]]  # 緯度経度か、ゲーム座標か
    lat, lon = ROUTES[name][0]
    path, snap, length = main_stem(adj, route)
    joins = confluences(adj, path, TRIB_MIN)
    pts = resample(path, STEP)
    hm = np.asarray(Image.open(HEIGHTMAP)).astype(np.float64)

    # 上流の点を、左右 SNAP_SIDE m 以内でいちばん低い地点へ寄せる。
    # 川の線のデータと高さマップの谷底がずれていると、水が溝からこぼれて本当の谷底へ流れ出るため(#73 の検証)
    moved = []
    for i, (x, z) in enumerate(pts):
        if ground_at(hm, x, z) < TIDAL_GROUND:
            moved.append((x, z))
            continue
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        dx, dz = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dz) or 1
        nx, nz = -dz / n, dx / n
        cands = [(x + nx * o, z + nz * o) for o in range(-SNAP_SIDE, SNAP_SIDE + 1, 16)]
        moved.append(min(cands, key=lambda p: ground_at(hm, *p)))
    # 寄せた後の線を、前後3点の平均でならす(ジグザグにしない)
    pts = [moved[0]] + [tuple(sum(c) / 3 for c in zip(*moved[i - 1:i + 2])) for i in range(1, len(moved) - 1)] + [moved[-1]]

    # 河口を、海に届くまで沖へ延ばす(河口の点が海岸より陸側にあると、海の水が入らないため)
    (x0, z0), (x1, z1) = pts[0], pts[1]
    n = math.hypot(x0 - x1, z0 - z1) or 1
    ux, uz = (x0 - x1) / n, (z0 - z1) / n
    ext = []
    for k in range(1, 15):
        p = (x0 + ux * STEP * k, z0 + uz * STEP * k)
        ext.append(p)
        if ground_at(hm, *p) < SEA_LEVEL - 2:
            break
    pts = ext[::-1] + pts

    ground = [ground_at(hm, x, z) for x, z in pts]
    # 山の区間は掘らない。元の地面が MAX_GROUND m を超えたら、そこで川を終える(急な沢では水が溝からこぼれるため)
    for i, g in enumerate(ground):
        if g > MAX_GROUND and i > 10:
            pts, ground = pts[:i], ground[:i]
            break

    # 川底: 上流(末尾)から河口(先頭)へ、下がるだけにする
    bed = [0.0] * len(pts)
    prev = None
    for i in range(len(pts) - 1, -1, -1):
        g = ground[i]
        b = TIDAL_BED if g < TIDAL_GROUND else g - DEPTH
        if prev is not None:
            b = min(b, prev - MIN_SLOPE * STEP)
        bed[i] = b
        prev = b

    # 潮の入る区間の上端から上流へ、川底をなだらかにつなぐ(段差があると水が途切れる、#73 の検証)
    tidal_top = max((i for i, g in enumerate(ground) if g < TIDAL_GROUND), default=-1)
    if 0 <= tidal_top < len(pts) - 1:
        end = min(tidal_top + RAMP, len(pts) - 1)
        for i in range(tidal_top + 1, end + 1):
            ramp = bed[tidal_top] + (bed[end] - bed[tidal_top]) * (i - tidal_top) / (end - tidal_top)
            bed[i] = min(bed[i], ramp)

    # 合流地点を、出力する点の番号に直す。潮の入る区間(海の水が入る)には置かない。近すぎる合流はまとめる
    sources = []
    for k, trib in sorted(joins, key=lambda j: -j[1]):
        i = min(range(len(pts)), key=lambda j: math.dist(pts[j], k))
        if ground[i] < TIDAL_GROUND or any(abs(i - j) < 10 for j, _ in sources):
            continue
        sources.append((i, round(trib)))
    # 潮の入る区間から上流へなだらかにつなぐ区間の上端にも置く(境目で水が途切れやすいため)
    ramp_end = min(tidal_top + RAMP, len(pts) - 1) if tidal_top >= 0 else -1
    if 0 <= ramp_end < len(pts) - 1 and not any(abs(ramp_end - j) < 5 for j, _ in sources):
        sources.append((ramp_end, 0))
    sources.sort()

    out = {
        "name": name,
        "sources": [{"index": i, "tributaryLength": t} for i, t in sources],  # 合流地点(支流の長さはゲーム上m)
        "mouth": [lat, lon],
        "snapDistance": round(snap, 1),  # 地点を吸い付けた距離の最大
        "lengthGameM": round(length, 1),
        "points": [[round(x, 1), round(z, 1), round(b, 2)] for (x, z), b in zip(pts, bed)],
        "ground": [round(g, 2) for g in ground],
    }
    dst = f"{SRC}/river_{name}.json"
    json.dump(out, open(dst, "w"))
    tidal = sum(1 for g in ground if g < TIDAL_GROUND)
    print(f"{dst}: {len(pts)} points, length {length / 1000:.1f}km(game), snap {snap:.0f}m, "
          f"tidal {tidal} points, bed {bed[0]:.1f}..{bed[-1]:.1f}m, ground {min(ground):.1f}..{max(ground):.1f}m")
    print("source:", out["points"][-1], "mouth:", out["points"][0], "confluences:", [i for i, _ in sources])
    return path


if __name__ == "__main__":
    main()
