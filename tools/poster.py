#!/usr/bin/env python3
"""Make the delivery poster from the finished film's key art plate."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
IVORY = (237, 230, 214)
GOLD = (201, 162, 39)


def F(name, size):
    return ImageFont.truetype(os.path.join(ROOT, "fonts", name), size)


def tracked(d, xy, text, f, fill, tr):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + tr
    return x


def main():
    plate = sys.argv[1] if len(sys.argv) > 1 else "assets/plates/chip_200.jpg"
    out = sys.argv[2] if len(sys.argv) > 2 else "out/poster.png"
    im = Image.open(os.path.join(ROOT, plate)).convert("RGB").resize((W, H), Image.LANCZOS)
    # darken the lower half so the type sits on something solid
    veil = Image.new("L", (W, H), 0)
    dv = ImageDraw.Draw(veil)
    for y in range(H):
        t = max(0.0, (y - H * 0.32) / (H * 0.68))
        dv.line([(0, y), (W, y)], fill=int(210 * t * t))
    im = Image.composite(Image.new("RGB", (W, H), (8, 8, 10)), im, veil)
    d = ImageDraw.Draw(im)

    f_t = F("InstrumentSerif-Regular.ttf", 92)
    f_s = F("JetBrainsMono.ttf", 20)
    lines = ["THE MACHINE THAT", "BORROWS THE UNIVERSE"]
    y = H - 330
    for ln in lines:
        d.text((120, y), ln, font=f_t, fill=IVORY)
        y += 104
    d.line([(122, y + 18), (222, y + 18)], fill=GOLD, width=3)
    tracked(d, (122, y + 46), "QUANTUM COMPUTING · 1900—2026", f_s, GOLD, 5)
    tracked(d, (122, 96), "A DOCUMENTARY", f_s, (200, 192, 176), 4)
    d.text((W - 300, H - 74), "28 MIN", font=f_s, fill=(170, 162, 148))
    os.makedirs(os.path.dirname(os.path.join(ROOT, out)), exist_ok=True)
    im.save(os.path.join(ROOT, out))
    print("poster", out)


if __name__ == "__main__":
    main()
