"""地理院タイルの標高タイル(DEM10B)を取得し、1枚の標高配列につなぐ。

出力(既定は ~/.cache/ai-mayor-dem/):
  tiles/14/{x}/{y}.png  取得したタイル
  mosaic.npy            標高(m)。float32。海などデータなしは NaN
  mosaic.json           配列の左上タイル番号とズーム

使い方: python3 fetch_dem.py
範囲は #41 で決めた水平1/2縮尺の地図全体(実寸34.56km四方)に、周りの余白を足したもの。
出典: 国土地理院 標高タイル(基盤地図情報 数値標高モデル DEM10B)
"""
import io
import json
import math
import os
import time
import urllib.error
import urllib.request

import numpy as np
from PIL import Image

CENTER = (33.59018, 130.40987)  # 天神駅と博多駅の中間
HALF_M = 17280 + 1000           # 地図の半辺(実寸)+余白1km
Z = 14
URL = "https://cyberjapandata.gsi.go.jp/xyz/dem_png/{z}/{x}/{y}.png"
OUT = os.path.expanduser(os.environ.get("OUT", "~/.cache/ai-mayor-dem"))
R = 6371008.8


def offset_to_latlon(east_m, north_m):
    lat = CENTER[0] + math.degrees(north_m / R)
    lon = CENTER[1] + math.degrees(east_m / (R * math.cos(math.radians(CENTER[0]))))
    return lat, lon


def latlon_to_tile(lat, lon, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    s = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n
    return x, y


def decode(img):
    """標高PNGを標高(m)に戻す。x = R*2^16 + G*2^8 + B、単位0.01m。2^23 はデータなし。"""
    a = np.asarray(img.convert("RGB"), dtype=np.int64)
    x = (a[..., 0] << 16) + (a[..., 1] << 8) + a[..., 2]
    h = np.where(x < 2 ** 23, x, x - 2 ** 24).astype(np.float32) * 0.01
    h[x == 2 ** 23] = np.nan
    return h


def fetch(x, y):
    path = f"{OUT}/tiles/{Z}/{x}/{y}.png"
    if os.path.exists(path):
        return Image.open(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        data = urllib.request.urlopen(URL.format(z=Z, x=x, y=y), timeout=30).read()
    except urllib.error.HTTPError as e:
        if e.code == 404:  # 海だけのタイルは存在しない
            return None
        raise
    open(path, "wb").write(data)
    time.sleep(0.1)
    return Image.open(io.BytesIO(data))


def main():
    north, west = offset_to_latlon(-HALF_M, HALF_M)
    south, east = offset_to_latlon(HALF_M, -HALF_M)
    x0, y0 = (int(v) for v in latlon_to_tile(north, west, Z))
    x1, y1 = (int(v) for v in latlon_to_tile(south, east, Z))
    nx, ny = x1 - x0 + 1, y1 - y0 + 1
    print(f"tiles x {x0}-{x1}, y {y0}-{y1} ({nx * ny} tiles)")
    mosaic = np.full((ny * 256, nx * 256), np.nan, dtype=np.float32)
    missing = 0
    for ty in range(y0, y1 + 1):
        for tx in range(x0, x1 + 1):
            img = fetch(tx, ty)
            if img is None:
                missing += 1
                continue
            mosaic[(ty - y0) * 256:(ty - y0 + 1) * 256, (tx - x0) * 256:(tx - x0 + 1) * 256] = decode(img)
    np.save(f"{OUT}/mosaic.npy", mosaic)
    json.dump({"z": Z, "x0": x0, "y0": y0, "nx": nx, "ny": ny, "center": CENTER, "half_m": HALF_M},
              open(f"{OUT}/mosaic.json", "w"), indent=1)
    print(f"mosaic {mosaic.shape}, missing tiles {missing}, NaN {np.isnan(mosaic).mean():.1%}")


if __name__ == "__main__":
    main()
