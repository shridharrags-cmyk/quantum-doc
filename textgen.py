#!/usr/bin/env python3
"""Render lower-third captions and source lines to transparent PNGs."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
IVORY = (237, 230, 214)
GOLD = (201, 162, 39)

def F(name, size):
    return ImageFont.truetype(os.path.join(ROOT, "fonts", name), size)

def tracked_w(d, text, f, tr):
    return sum(d.textlength(c, font=f) for c in text) + tr * max(0, len(text) - 1)

def tracked(d, xy, text, f, fill, tr):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + tr

def render(shot):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cap, src = shot.get("cap"), shot.get("src")
    chip = shot.get("chip")
    if chip:
        f = F("JetBrainsMono.ttf", 19)
        tw = tracked_w(d, chip, f, 3)
        d.line([(132, 96), (132 + tw, 96)], fill=GOLD + (150,), width=2)
        tracked(d, (132, 116), chip, f, IVORY + (190,), 3)
    if cap:
        f = F("InstrumentSerif-Italic.ttf", 42)
        # wrap
        words, lines, cur = cap.split(), [], ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if d.textlength(t, font=f) <= 980:
                cur = t
            else:
                lines.append(cur); cur = wd
        if cur: lines.append(cur)
        y = 928 - (len(lines) - 1) * 48
        d.line([(134, y - 26), (188, y - 26)], fill=GOLD + (170,), width=2)
        for ln in lines:
            d.text((134, y), ln, font=f, fill=(10, 9, 7, 150))
            d.text((132, y - 2), ln, font=f, fill=IVORY + (238,))
            y += 48
    if src:
        f = F("JetBrainsMono.ttf", 17)
        tw = d.textlength(src, font=f)
        x = 1788 - tw
        d.text((x, 1002), src, font=f, fill=(10, 9, 7, 140))
        d.text((x, 1000), src, font=f, fill=(206, 198, 181, 150))
    out = os.path.join(ROOT, "assets/text", shot["id"] + ".png")
    im.save(out)
    return out

def main():
    plan = json.load(open(os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else "shots.json")))
    os.makedirs(os.path.join(ROOT, "assets/text"), exist_ok=True)
    n = 0
    for s in plan["shots"]:
        if s.get("cap") or s.get("src") or s.get("chip"):
            s["text"] = os.path.relpath(render(s), ROOT)
            n += 1
    json.dump(plan, open(os.path.join(ROOT, "shots.json"), "w"), indent=1)
    print("text layers", n)

if __name__ == "__main__":
    main()
