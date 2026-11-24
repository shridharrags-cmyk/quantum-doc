#!/usr/bin/env python3
"""Prepare source photographs into 3200x1800 treated plates."""
import json, os, sys
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
PW, PH = 3200, 1800

def crop_cover(im, w, h, focus=(0.5, 0.5)):
    im = ImageOps.exif_transpose(im).convert("RGB")
    sw, sh = im.size
    s = max(w / sw, h / sh)
    nw, nh = int(sw * s + 0.5), int(sh * s + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    cx, cy = focus
    x = int((nw - w) * cx)
    y = int((nh - h) * cy)
    return im.crop((x, y, x + w, y + h))

def duotone(im, shadow=(18, 15, 12), mid=(120, 104, 82), high=(243, 236, 220)):
    g = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
    # filmic S-curve
    g = np.clip(g, 0, 1)
    g = g * g * (3 - 2 * g) * 0.35 + g * 0.65
    out = np.empty(g.shape + (3,), dtype=np.float32)
    lo = np.array(shadow, np.float32); mi = np.array(mid, np.float32); hi = np.array(high, np.float32)
    m = g < 0.5
    t = np.where(m, g / 0.5, (g - 0.5) / 0.5)[..., None]
    out = np.where(m[..., None], lo + (mi - lo) * t, mi + (hi - mi) * t)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def mono(im):
    g = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
    g = g * g * (3 - 2 * g) * 0.28 + g * 0.72
    out = np.stack([g * 246 + 6, g * 242 + 5, g * 232 + 4], -1)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def grade(im, sat=0.94, warm=1.0, contrast=1.04):
    a = np.asarray(im, dtype=np.float32)
    lum = a @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * sat
    a = (a - 128) * contrast + 128
    a[..., 0] *= warm
    a[..., 2] *= (2.0 - warm)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def prep(src, dst, treat="color", focus=(0.5, 0.5)):
    im = Image.open(src)
    im = crop_cover(im, PW, PH, focus)
    if treat == "duo":
        im = duotone(im)
    elif treat == "mono":
        im = mono(im)
    else:
        im = grade(im)
    im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=52, threshold=2))
    im.save(dst, quality=88, subsampling=1, optimize=True)

def main():
    p = sys.argv[1]
    man = json.load(open(p if os.path.isabs(p) else os.path.join(ROOT, p)))
    os.makedirs(os.path.join(ROOT, "assets/plates"), exist_ok=True)
    for item in man:
        dst = os.path.join(ROOT, "assets/plates", item["id"] + ".jpg")
        if os.path.exists(dst) and not item.get("force"):
            continue
        try:
            prep(os.path.join(ROOT, item["src"]), dst, item.get("treat", "color"),
                 item.get("focus", (0.5, 0.5)))
            print("ok", item["id"], os.path.getsize(dst) // 1024, "KB", flush=True)
        except Exception as e:
            print("FAIL", item["id"], e, flush=True)

if __name__ == "__main__":
    main()
