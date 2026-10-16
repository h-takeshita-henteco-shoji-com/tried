"""国土数値情報の土地利用細分メッシュから、森林のマスを作る(#73)。

土地利用細分メッシュ(100m のマスごとの土地の使われ方)のうち「森林」(0500)のマスを、
ゲームの天然資源のマス(33.75m 四方、512×512)に写す。水平1/2縮尺なので、100m のマスはゲーム上で 50m 四方になる。
木の上限(マップは25万本)に収まるよう、1マスあたりの本数(density)も決める。

入力: ~/.cache/ai-mayor-dem/landuse/L03-b-21_5030/L03-b-21_5030.geojson
  取得元: https://nlftp.mlit.go.jp/ksj/gml/data/L03-b/L03-b-21/L03-b-21_5030-jgd2011_GML.zip
出力: ~/.cache/ai-mayor-dem/forest_cells.json
  cells: [[ix, iz], ...](天然資源のマスの番号)、density: 1マスあたりの本数
使い方: python3 forest_mask.py
出典: 国土数値情報(土地利用細分メッシュデータ、令和3年度)を加工して作成
"""
import json
import math
import os
import re

SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
LANDUSE = f"{SRC}/landuse/L03-b-21_5030/L03-b-21_5030.geojson"
CENTER = (33.59018, 130.40987)
R = 6371008.8
CELL = 33.75
GRID = 512
HALF = 8640.0
TREE_BUDGET = 230000   # マップの上限25万本より少し少なく
FOREST = "0500"
LINE = re.compile(r'"土地利用種別": "(\d+)".*?"coordinates": \[ \[ \[ ([\d.]+), ([\d.]+) \], \[ [\d.]+, [\d.]+ \], \[ ([\d.]+), ([\d.]+) \]')


def to_game(lat, lon):
    north = math.radians(lat - CENTER[0]) * R
    east = math.radians(lon - CENTER[1]) * R * math.cos(math.radians(lat))
    return east / 2, north / 2


def main():
    cells = set()
    forest_mesh = 0
    with open(LANDUSE, encoding="utf-8") as f:
        for line in f:
            m = LINE.search(line)
            if not m or m.group(1) != FOREST:
                continue
            lon0, lat0, lon1, lat1 = (float(m.group(i)) for i in (2, 3, 4, 5))
            # 東西の端は、マスの中心の緯度でそろえて計算する(端ごとに緯度を変えると、隣のマスとの間にすき間ができる)
            lat_c = (lat0 + lat1) / 2
            x0, _ = to_game(lat_c, min(lon0, lon1))
            x1, _ = to_game(lat_c, max(lon0, lon1))
            _, z0 = to_game(min(lat0, lat1), CENTER[1])
            _, z1 = to_game(max(lat0, lat1), CENTER[1])
            if x1 < -HALF or x0 > HALF or z1 < -HALF or z0 > HALF:
                continue
            forest_mesh += 1
            # このメッシュが重なる天然資源のマスに、中心が入るものを森林にする
            for ix in range(int(x0 / CELL + GRID / 2), int(x1 / CELL + GRID / 2) + 1):
                for iz in range(int(z0 / CELL + GRID / 2), int(z1 / CELL + GRID / 2) + 1):
                    cx = (ix - GRID / 2 + 0.5) * CELL
                    cz = (iz - GRID / 2 + 0.5) * CELL
                    if 0 <= ix < GRID and 0 <= iz < GRID and x0 <= cx <= x1 and z0 <= cz <= z1:
                        cells.add((ix, iz))
    density = max(1, min(5, TREE_BUDGET // max(len(cells), 1)))
    out = {"cells": sorted(cells), "density": density, "forestMesh": forest_mesh}
    json.dump(out, open(f"{SRC}/forest_cells.json", "w"))
    print(f"forest mesh {forest_mesh}, resource cells {len(cells)} ({len(cells) / GRID / GRID:.0%}), "
          f"density {density}, trees about {len(cells) * density}")


if __name__ == "__main__":
    main()
