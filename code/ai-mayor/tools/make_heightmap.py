"""fetch_dem.py でつないだ標高配列から、Cities: Skylines の高さマップを作る。

出力: 1081×1081、16ビット白黒PNG。画素値 0〜65535 がゲーム上の高さ 0〜1024m に対応する。
水平: 実寸34.56km四方を1081点(間隔32m)で切り出す。ゲーム上は17.28km四方(間隔16m)。
高さ: ゲーム上の高さ = 海面 + 持ち上げ + 標高 × VSCALE。海(データなし)は海面より下げる。
持ち上げ: 高さ0.5倍で海沿いの低地が海面すれすれになり、水につかったため(#64)。
海岸から内陸へ LAND_RAMP_PX 画素かけて、0から LAND_OFFSET まで上げる。

使い方: python3 make_heightmap.py  (高さの縮尺は既定0.5。VSCALE=0.75 などで変える)
出力先は ~/.cache/ai-mayor-dem/heightmaps/。マップエディターの Heightmaps フォルダにも置く。
高さマップは公開しない(#42 で決定)。リポジトリにも置かない。
川: fetch_rivers.py で取った河川中心線(通常部)を、幅3画素、深さ5mで掘る。両岸1画素は半分の深さ。
元の標高8m未満の低地では、川底を海面下4mにして海の水を入れる。
出典: 国土地理院 標高タイル(基盤地図情報 数値標高モデル DEM10B)、国土地理院ベクトルタイル(河川中心線)を加工して作成
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
LAND_OFFSET = float(os.environ.get("LAND_OFFSET", "4"))  # 陸地を海面から持ち上げる高さ(#64)
LAND_RAMP_PX = 4         # 海岸から持ち上げ切るまでの画素数
RIVERS = os.environ.get("RIVERS", "0") == "1"  # 河川中心線を掘り込む(#64 で試したが、水源の扱いが難しく既定では使わない)
RIVER_DEPTH = 5.0        # 川筋を周りより下げる深さ(ゲーム上m)
RIVER_WIDTH_PX = 3       # 川筋の幅(画素)
TIDAL_ELEV_M = 8.0       # 元の標高がこれ未満の低地では、川底を海面より下げて海の水を入れる
TIDAL_DEPTH = 4.0        # そのときの川底の深さ(海面から)
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


def river_mask(center):
    """河川中心線(通常部)を、高さマップの格子に描き込んだマスクを返す。"""
    from PIL import ImageDraw
    feats = json.load(open(f"{SRC}/rivers.geojson"))["features"]
    img = Image.new("L", (N, N), 0)
    draw = ImageDraw.Draw(img)
    for f in feats:
        p = f["properties"]
        if p.get("type") != "河川中心線（通常部）" or f["geometry"]["type"] != "LineString":
            continue
        pts = []
        for lon, lat in f["geometry"]["coordinates"]:
            north = math.radians(lat - center[0]) * R
            east = math.radians(lon - center[1]) * R * math.cos(math.radians(lat))
            pts.append(((N - 1) / 2 + east / STEP_M, (N - 1) / 2 - north / STEP_M))
        draw.line(pts, fill=255, width=RIVER_WIDTH_PX)
    return np.asarray(img) > 0


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
    # 陸: 海岸から内陸へ、なだらかに持ち上げる
    inland = ndimage.distance_transform_edt(~is_sea)
    lift = LAND_OFFSET * np.clip(inland / LAND_RAMP_PX, 0, 1)
    game = np.where(is_sea, SEA_LEVEL - np.maximum(depth, 1.0), SEA_LEVEL + lift + np.maximum(h, 0) * VSCALE)

    if RIVERS:
        core = river_mask(meta["center"]) & ~is_sea
        bank = ndimage.binary_dilation(core) & ~core & ~is_sea
        floor = ndimage.minimum_filter(game, 3)  # 周りの低い所を基準にして、川底が盛り上がらないようにする
        game = np.where(core, np.minimum(game, floor - RIVER_DEPTH), game)
        game = np.where(bank, np.minimum(game, floor - RIVER_DEPTH / 2), game)
        tidal = core & (h < TIDAL_ELEV_M)  # 下流の低地は潮の入る川にする
        game = np.where(tidal, np.minimum(game, SEA_LEVEL - TIDAL_DEPTH), game)
        print(f"river px {core.sum()}, below sea {(core & (game < SEA_LEVEL)).sum()}")

    clipped = (game > GAME_MAX_M).mean()
    px = np.clip(np.round(game / GAME_MAX_M * 65535), 0, 65535).astype(np.uint16)

    out = f"{SRC}/heightmaps"
    os.makedirs(out, exist_ok=True)
    name = f"fukuoka_h2_v{int(VSCALE * 100):03d}_o{int(LAND_OFFSET)}{'_r' if RIVERS else ''}.png"
    Image.fromarray(px).save(f"{out}/{name}")
    os.makedirs(GAME_DIR, exist_ok=True)
    shutil.copy(f"{out}/{name}", f"{GAME_DIR}/{name}")
    print(f"{name}: land max {game[~is_sea].max():.1f}m, sea {is_sea.mean():.1%}, "
          f"clipped {clipped:.3%}")


if __name__ == "__main__":
    main()
