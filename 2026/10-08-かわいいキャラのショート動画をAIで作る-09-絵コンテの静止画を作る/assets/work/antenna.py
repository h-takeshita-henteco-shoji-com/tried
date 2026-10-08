"""ぬめの触角を前に倒す。根元から離れるほど大きく回し、付け根の線をつなげたまま曲げる。"""
import numpy as np
from PIL import Image
from scipy import ndimage

def _warp(a, px, py, y0, deg, ramp):
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    d = np.clip((y0 - yy) / ramp, 0, 1)
    th = np.radians(deg) * (3 * d**2 - 2 * d**3)  # smoothstep
    dx, dy = xx - px, yy - py
    c, s = np.cos(th), np.sin(th)
    # 出力の点を逆に回して、元の点を探す
    sx = px + c * dx - s * dy
    sy = py + s * dx + c * dy
    return np.stack([ndimage.map_coordinates(a[..., k], [sy, sx], order=1, cval=0) for k in range(4)], -1)

def tilt(im, pivot, y0, deg, ramp=160, x_max=10**9, pad=350):
    """触角(y0より上、x_maxより左)だけを pivot 中心に回す。deg>0 で左へ倒す。"""
    a = np.asarray(im.convert("RGBA")).astype(float)
    a = np.pad(a, ((pad, 0), (pad, 0), (0, 0)))
    px, py, y0, x_max = pivot[0] + pad, pivot[1] + pad, y0 + pad, x_max + pad
    ant = a.copy()
    ant[y0:] = 0
    ant[:, x_max:] = 0
    base = a.copy()
    base[:y0, :x_max] = 0
    warped = _warp(ant, px, py, y0, deg, ramp)
    out = Image.fromarray(base.astype(np.uint8), "RGBA")
    out.alpha_composite(Image.fromarray(warped.clip(0, 255).astype(np.uint8), "RGBA"))
    return out.crop(out.getbbox())

if __name__ == "__main__":
    side = Image.open("work/nume-side.png")
    for deg in (30, 40, 50):
        tilt(side, pivot=(240, 430), y0=388, deg=deg, x_max=328).save(f"work/nume-side-tilt{deg}.png")
