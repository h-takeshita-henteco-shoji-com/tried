"""マップエディターで、森林のマスに木を植える(#73)。forest_mask.py の出力を使う。

川と高速道路を作った後に実行する(水・道路の上には植えないため)。
使い方: python3 plant_forest_cells.py
"""
import json
import os

from lay_expressway import call

SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
CHUNK = 4000


def main():
    f = json.load(open(f"{SRC}/forest_cells.json"))
    cells, density = f["cells"], f["density"]
    total = 0
    for i in range(0, len(cells), CHUNK):
        part = cells[i:i + CHUNK]
        r = call("/editor/forest_cells", body=";".join(f"{x},{z}" for x, z in part), density=density, seed=i + 1)
        if not r.get("ok"):
            print("stop:", r)
            break
        total += r["planted"]
        print(f"{i + len(part)}/{len(cells)} cells, planted {total}, trees {r['trees']}", flush=True)
    print(call("/editor/state")["resources"])


if __name__ == "__main__":
    main()
