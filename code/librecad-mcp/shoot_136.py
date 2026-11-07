"""#136 の課題1で各モデルが保存した図面を LibreCAD で開き、矩計図の範囲を画面写真に撮る。

寸法は、ezdxf で描くとファイルに入った絵のまま出るが、LibreCAD は図面の設定から描き直す。
人が CAD で開いたときの見え方を比べるため、LibreCAD の画面で撮る。

使い方(LibreCAD を restart.sh で起動しておく):
  uv run python code/librecad-mcp/shoot_136.py
  uv run python code/librecad-mcp/shoot_136.py --day <その日のフォルダ> --task P-1 --window 54800,-11300,62000,-4600  (#146)
"""
import argparse
from pathlib import Path

from run_eval_mcp import REPO, lc_call

RES = REPO / "2026/11-05-AIと図面のコラボレーション-05-AIに矩計図と平面詳細図を描かせる/results/2026-11-05"
OUT = RES / "librecad"
WINDOW = [[46600, -11300], [52900, -5300]]


def main():
    global RES, OUT, WINDOW
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=None)
    ap.add_argument("--task", default="K-1")
    ap.add_argument("--window", default=None, help="x0,y0,x1,y1")
    a = ap.parse_args()
    if a.day:
        RES = sorted((Path(a.day).resolve() / "results").iterdir())[-1]
        OUT = RES / "librecad"
    if a.window:
        x0, y0, x1, y1 = map(float, a.window.split(","))
        WINDOW = [[x0, y0], [x1, y1]]
    OUT.mkdir(exist_ok=True)
    for dxf in sorted(RES.glob(f"{a.task}-*/*/drawing-changed.dxf")):
        mode, model = dxf.parts[-3][4:], dxf.parts[-2].split("__")[0]
        if not lc_call("open", path=str(dxf)).get("ok"):
            print("開けない:", dxf)
            continue
        png = OUT / f"{mode}-{model}.png"
        print(png.name, lc_call("screenshot", path=str(png), window=WINDOW).get("ok"))


if __name__ == "__main__":
    main()
