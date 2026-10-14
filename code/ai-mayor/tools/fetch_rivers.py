"""国土地理院ベクトルタイルの河川中心線(ズーム16)を取得し、1つの GeoJSON にまとめる。

範囲は中央25タイル(実寸19.2km四方)。川の再現がいちばん効く範囲に絞り、配信元への負担を抑える。
出力: ~/.cache/ai-mayor-dem/rivers.geojson
出典: 国土地理院ベクトルタイル(河川中心線)
"""
import json
import math
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

CENTER = (33.59018, 130.40987)
HALF_M = 9600 + 500   # 中央25タイルの半辺(実寸)+余白
Z = 16
URL = "https://cyberjapandata.gsi.go.jp/xyz/experimental_rvrcl/{z}/{x}/{y}.geojson"
OUT = os.path.expanduser("~/.cache/ai-mayor-dem")
R = 6371008.8


def tile(lat, lon):
    n = 2 ** Z
    s = math.sin(math.radians(lat))
    return int((lon + 180) / 360 * n), int((0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n)


def get(xy):
    x, y = xy
    path = f"{OUT}/rvrcl/{Z}/{x}/{y}.geojson"
    if os.path.exists(path):
        return json.load(open(path))
    try:
        data = urllib.request.urlopen(URL.format(z=Z, x=x, y=y), timeout=30).read()
    except urllib.error.HTTPError as e:
        if e.code == 404:  # 川のないタイルは存在しない
            return None
        raise
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(data)
    time.sleep(0.05)
    return json.loads(data)


def main():
    dlat = math.degrees(HALF_M / R)
    dlon = math.degrees(HALF_M / (R * math.cos(math.radians(CENTER[0]))))
    x0, y0 = tile(CENTER[0] + dlat, CENTER[1] - dlon)
    x1, y1 = tile(CENTER[0] - dlat, CENTER[1] + dlon)
    xys = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
    print(f"{len(xys)} tiles")
    feats = []
    with ThreadPoolExecutor(4) as ex:
        for d in ex.map(get, xys):
            if d:
                feats += d["features"]
    json.dump({"type": "FeatureCollection", "features": feats}, open(f"{OUT}/rivers.geojson", "w"), ensure_ascii=False)
    print(f"{len(feats)} features")


if __name__ == "__main__":
    main()
