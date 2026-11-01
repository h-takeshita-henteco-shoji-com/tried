"""へんロボの立ち絵の白い背景を抜いて、透明なPNGにする(#132)。

キャラの中の線（口・眉・眼鏡）も白いため、画像の縁につながった白だけを背景として抜く。
縁の近くの淡い色は、白さに応じて半透明にし、輪郭のギザギザを防ぐ。

使い方: uv run --with pillow --with numpy --with scipy python cutout.py 入力.png 出力.png
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage


def main(src, dst):
    rgb = np.array(Image.open(src).convert("RGB")).astype(float)
    white = rgb.min(axis=2) > 225
    labels, _ = ndimage.label(white)
    edge = set(np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))) - {0}
    bg = np.isin(labels, list(edge))
    # 背景のすぐ外側の数画素は、白さに応じて半透明にする
    near = ndimage.binary_dilation(bg, iterations=3) & ~bg
    whiteness = (rgb.min(axis=2) - 150) / (255 - 150)
    alpha = np.full(bg.shape, 255.0)
    alpha[bg] = 0
    alpha[near] = np.clip((1 - whiteness[near]) * 255, 0, 255)
    out = np.dstack([rgb, alpha]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    img = img.crop(img.getbbox())
    img.save(dst)
    print(dst, img.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
