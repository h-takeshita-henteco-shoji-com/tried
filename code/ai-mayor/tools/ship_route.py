"""博多湾の湾口から博多港まで、海の中だけを通る船の航路を作る(#73)。

高さマップの海のマス(海面より4m以上低い所)のうち、岸から64m以上離れたマスだけを通る最短の道筋を探し、
まっすぐ進めるところは点を間引く。出力: ~/.cache/ai-mayor-dem/ship_route.json
使い方: python3 ship_route.py
"""
import heapq
import json
import math
import os

import numpy as np
from PIL import Image
from scipy import ndimage

SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
START = (-4000.0, 8600.0)   # 地図の北の端(湾口の沖)
GOAL = (-650.0, 1750.0)     # 博多港の前


def main():
    hm = np.asarray(Image.open(f"{SRC}/heightmaps/fukuoka_h2_v050_o4.png")).astype(float) / 65535 * 1024
    water = hm < 36
    safe = ndimage.distance_transform_edt(water) >= 4
    rc = lambda x, z: (int(round(540 - z / 16)), int(round(x / 16 + 540)))
    xz = lambda r, c: ((c - 540) * 16, (540 - r) * 16)
    start, goal = rc(*START), rc(*GOAL)
    if not safe[goal]:
        rr, cc = np.nonzero(safe)
        i = np.argmin((rr - goal[0]) ** 2 + (cc - goal[1]) ** 2)
        goal = (rr[i], cc[i])
    dist, prev, heap = {start: 0}, {}, [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if u == goal:
            break
        if d > dist[u]:
            continue
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                v = (u[0] + dr, u[1] + dc)
                if (dr or dc) and 0 <= v[0] < 1081 and 0 <= v[1] < 1081 and safe[v]:
                    nd = d + math.hypot(dr, dc)
                    if nd < dist.get(v, 1e9):
                        dist[v], prev[v] = nd, u
                        heapq.heappush(heap, (nd, v))
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path = path[::-1]
    pts, i = [path[0]], 0
    while i < len(path) - 1:
        j = min(len(path) - 1, i + 60)
        while j > i + 1:
            a, b = path[i], path[j]
            n = int(math.dist(a, b)) + 1
            if all(water[int(round(a[0] + (b[0] - a[0]) * k / n)), int(round(a[1] + (b[1] - a[1]) * k / n))] for k in range(n + 1)):
                break
            j -= 1
        pts.append(path[j])
        i = j
    route = [xz(*p) for p in pts]
    route[0] = (route[0][0], 8620.0)
    json.dump({"ship": route}, open(f"{SRC}/ship_route.json", "w"))
    print(len(route), "points", route)


if __name__ == "__main__":
    main()
