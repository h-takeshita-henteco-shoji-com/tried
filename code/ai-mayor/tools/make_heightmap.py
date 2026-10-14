"""fetch_dem.py でつないだ標高配列から、Cities: Skylines の高さマップを作る。

出力: 1081×1081、16ビット白黒PNG。画素値 0〜65535 がゲーム上の高さ 0〜1024m に対応する。
水平: 実寸34.56km四方を1081点(間隔32m)で切り出す。ゲーム上は17.28km四方(間隔16m)。
高さ: ゲーム上の高さ = 海面 + 標高 × VSCALE。海(データなし)は海面より下げる。

使い方: python3 make_heightmap.py  (高さの縮尺は既定0.5。VSCALE=0.75 などで変える)
出力先は ~/.cache/ai-mayor-dem/heightmaps/。マップエディターの Heightmaps フォルダにも置く。
高さマップは公開しない(#42 で決定)。リポジトリにも置かない。
出典: 国土地理院 標高タイル(基盤地図情報 数値標高モデル DEM10B)を加工して作成
"""
import json
import math
import os
import shutil

import numpy as np
from PIL import Image
from scipy import ndimage

SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
GAME_DIR = os.path.expanduser(
    "~/Library/Application Support/Colossal Order/Cities_Skylines/Addons/MapEditor/Heightmaps")
N = 1081                 # 高さマップの1辺の画素数
STEP_M = 32.0            # 画素の間隔(実寸)。ゲーム上は16m
GAME_MAX_M = 1024.0      # 画素値65535にあたるゲーム上の高さ
SEA_LEVEL = 40.0         # ゲーム上の海面の高さ
SEA_DEPTH = 20.0         # 沖の海の深さ(海面からの深さ)
SHORE_PX = 6             # 海岸から沖の深さに達するまでの画素数
VSCALE = float(os.environ.get("VSCALE", "0.5"))  # #42 で0.5に決めた
R = 6371008.8


def target_latlon(center):
    """中心から東西南北に32m間隔の正方形格子を作り、各点の緯度経度を返す。"""
    k = (np.arange(N) - (N - 1) / 2) * STEP_M
    east, north = np.meshgrid(k, -k)  # 上が北
    lat = center[0] + np.degrees(north / R)
    # 東西の距離は、その点の緯度の緯線に沿って測る
    lon = center[1] + np.degrees(east / (R * np.cos(np.radians(lat))))
    return lat, lon


def latlon_to_mosaic(lat, lon, meta):
    """緯度経度を、ウェブメルカトルの標高配列の行・列(画素の中心基準)に変換する。"""
    n = 2 ** meta["z"]
    x = (lon + 180) / 360 * n
    s = np.sin(np.radians(lat))
    y = (0.5 - np.log((1 + s) / (1 - s)) / (4 * np.pi)) * n
    return (y - meta["y0"]) * 256 - 0.5, (x - meta["x0"]) * 256 - 0.5


def main():
    meta = json.load(open(f"{SRC}/mosaic.json"))
    dem = np.load(f"{SRC}/mosaic.npy")
    sea = np.isnan(dem)

    # 8m→32mに縮めるので、先に約4画素の平均でならす。海の画素は平均から外す
    land = np.where(sea, 0, dem)
    w = ndimage.uniform_filter((~sea).astype(np.float32), 4)
    avg = ndimage.uniform_filter(land, 4) / np.maximum(w, 1e-6)

    lat, lon = target_latlon(meta["center"])
    rows, cols = latlon_to_mosaic(lat, lon, meta)
    h = ndimage.map_coordinates(avg, [rows, cols], order=1)
    land_frac = ndimage.map_coordinates(w, [rows, cols], order=1)
    is_sea = land_frac < 0.5

    # 海: 海岸からの距離に応じて、沖の深さまでなだらかに下げる
    dist = ndimage.distance_transform_edt(is_sea)
    depth = SEA_DEPTH * np.clip(dist / SHORE_PX, 0, 1)
    game = np.where(is_sea, SEA_LEVEL - np.maximum(depth, 1.0), SEA_LEVEL + np.maximum(h, 0) * VSCALE)

    clipped = (game > GAME_MAX_M).mean()
    px = np.clip(np.round(game / GAME_MAX_M * 65535), 0, 65535).astype(np.uint16)

    out = f"{SRC}/heightmaps"
    os.makedirs(out, exist_ok=True)
    name = f"fukuoka_h2_v{int(VSCALE * 100):03d}.png"
    Image.fromarray(px).save(f"{out}/{name}")
    os.makedirs(GAME_DIR, exist_ok=True)
    shutil.copy(f"{out}/{name}", f"{GAME_DIR}/{name}")
    print(f"{name}: land max {game[~is_sea].max():.1f}m, sea {is_sea.mean():.1%}, "
          f"clipped {clipped:.3%}")


if __name__ == "__main__":
    main()
