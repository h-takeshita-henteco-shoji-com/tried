"""背景色(クリーム)を外周から塗りつぶして透明にし、キャラだけを切り抜く。"""
import numpy as np
from PIL import Image
from scipy import ndimage

def cutout(im, tol=28, crop_bottom=None):
    a = np.asarray(im.convert("RGB")).astype(int)
    if crop_bottom:
        a = a[:crop_bottom]
    bg = a[2, 2]
    near = np.abs(a - bg).sum(axis=2) < tol
    lab, _ = ndimage.label(near)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    outside = np.isin(lab, list(edge))
    alpha = np.where(outside, 0, 255).astype(np.uint8)
    alpha = ndimage.binary_opening(alpha > 0, iterations=1).astype(np.uint8) * 255
    rgba = np.dstack([a.astype(np.uint8), alpha])
    out = Image.fromarray(rgba, "RGBA")
    return out.crop(out.getbbox())

if __name__ == "__main__":
    views = Image.open("input/nume-4views.png")
    w = views.width // 4
    for i, name in enumerate(["front", "angle", "side", "back"]):
        cutout(views.crop((i * w, 0, (i + 1) * w, views.height))).save(f"work/nume-{name}.png")
    # どんは水面の線より上だけを使う(線は y=568 付近)
    for name in ["front", "left"]:
        cutout(Image.open(f"input/don-bath-{name}.png"), crop_bottom=566).save(f"work/don-{name}.png")
    for f in ["nume-front","nume-angle","nume-side","nume-back","don-front","don-left"]:
        print(f, Image.open(f"work/{f}.png").size)
