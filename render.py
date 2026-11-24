#!/usr/bin/env python3
"""Frame renderer for THE MACHINE THAT BORROWS THE UNIVERSE.

Renders a contiguous run of shots, one x264 segment per shot, then concatenates
them into out/seg_XX.mp4.  All camera motion is done at float precision from a
high-resolution plate; grain, vignette and grade are applied by ffmpeg.
"""
import argparse, json, math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- utilities
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def smooth(x):
    return x * x * (3 - 2 * x)

def lerp(a, b, t):
    return a + (b - a) * t

def hexc(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))

# ---------------------------------------------------------------- plates
class Plate:
    """A prepared still, already cropped to 16:9 and treated."""
    def __init__(self, path):
        self.im = Image.open(path).convert("RGB")
        self.w, self.h = self.im.size

    def view(self, cx, cy, scale, ow, oh):
        """Crop a float-precision window and resize to (ow, oh)."""
        scale = max(1.0, scale)
        sw, sh = self.w / scale, self.h / scale
        a = sw / ow
        # keep the window entirely inside the plate: no black edges, ever
        c = min(max(0.0, cx - (ow / 2) * a), max(0.0, self.w - sw))
        f = min(max(0.0, cy - (oh / 2) * a), max(0.0, self.h - sh))
        return self.im.transform((ow, oh), Image.AFFINE, (a, 0, c, 0, a, f),
                                 resample=Image.BICUBIC)

class PlateCache:
    def __init__(self, cap=4):
        self.cap, self.d, self.order = cap, {}, []

    def get(self, path):
        if path in self.d:
            self.order.remove(path); self.order.append(path)
            return self.d[path]
        p = Plate(path)
        self.d[path] = p; self.order.append(path)
        while len(self.order) > self.cap:
            k = self.order.pop(0); self.d.pop(k, None)
        return p

# ---------------------------------------------------------------- text
def font(name, size):
    return ImageFont.truetype(os.path.join(ROOT, "fonts", name), size)

def tracked(draw, xy, text, fnt, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x

def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ---------------------------------------------------------------- shots
def photo_frame(plate, shot, i, n, W, H):
    t = i / max(1, n - 1)
    z0, z1 = shot.get("zoom", [1.0, 1.06])
    # gentle ease so the move starts and ends without a snap
    e = 0.55 * t + 0.45 * smooth(t)
    z = lerp(z0, z1, e)
    fx, fy = shot.get("focus", [0.5, 0.5])
    px, py = shot.get("pan", [0.0, 0.0])
    cx = plate.w * (fx + px * (e - 0.5))
    cy = plate.h * (fy + py * (e - 0.5))
    return plate.view(clamp(cx, 0, plate.w), clamp(cy, 0, plate.h), z, W, H)

# ---------------------------------------------------------------- cards
INK = hexc("0B0C0E")
IVORY = hexc("EDE6D6")
GOLD = hexc("C9A227")
DIM = (150, 143, 128)

def card_frame(shot, i, n, W, H):
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    kind = shot.get("card", "chapter")
    reveal = min(smooth(clamp(i / 26.0)), smooth(clamp((n - i) / 20.0)))
    if kind == "chapter":
        num = shot.get("num", "I")
        title = shot.get("title", "")
        sub = shot.get("sub", "")
        f_num = font("InstrumentSerif-Italic.ttf", 210)
        f_t = font("InstrumentSerif-Regular.ttf", 66)
        f_s = font("JetBrainsMono.ttf", 24)
        col = tuple(int(c * reveal) for c in IVORY)
        d.text((132, 250), num, font=f_num, fill=tuple(int(c * reveal * 0.9) for c in GOLD))
        d.line([(140, 520), (140 + 120 * reveal, 520)], fill=tuple(int(c * reveal) for c in GOLD), width=3)
        d.text((140, 560), title.upper(), font=f_t, fill=col)
        if sub:
            tracked(d, (146, 660), sub.upper(), f_s, tuple(int(c * reveal * 0.65) for c in IVORY), 4)
    elif kind == "title":
        title = shot.get("title", "")
        sub = shot.get("sub", "")
        f_t = font("InstrumentSerif-Regular.ttf", 96)
        f_s = font("JetBrainsMono.ttf", 22)
        lines = wrap(d, title, f_t, W - 300)
        lh = int(f_t.size * 1.12)
        y = H / 2 - lh * len(lines) / 2 + 40
        for ln in lines:
            w = d.textlength(ln, font=f_t)
            d.text(((W - w) / 2, y), ln, font=f_t, fill=tuple(int(c * reveal) for c in IVORY))
            y += lh
        if sub:
            w = sum(d.textlength(c, font=f_s) + 5 for c in sub.upper())
            tracked(d, ((W - w) / 2, y + 46), sub.upper(), f_s,
                    tuple(int(c * reveal * 0.7) for c in GOLD), 5)

    elif kind == "quote":
        q = shot.get("quote", "")
        who = shot.get("who", "")
        f_q = font("InstrumentSerif-Italic.ttf", shot.get("size", 56))
        f_w = font("JetBrainsMono.ttf", 24)
        lines = wrap(d, q, f_q, W - 420)
        lh = int(f_q.size * 1.28)
        y = (H - lh * len(lines)) // 2 - 40
        for ln in lines:
            w = d.textlength(ln, font=f_q)
            d.text(((W - w) / 2, y), ln, font=f_q, fill=tuple(int(c * reveal) for c in IVORY))
            y += lh
        if who:
            w = d.textlength(who.upper(), font=f_w)
            tracked(d, ((W - w) / 2, y + 56), who.upper(), f_w,
                    tuple(int(c * reveal * 0.7) for c in GOLD), 2)
    elif kind == "stat":
        big = shot.get("big", "")
        lab = shot.get("label", "")
        f_b = font("InstrumentSerif-Regular.ttf", shot.get("size", 190))
        f_l = font("JetBrainsMono.ttf", 26)
        w = d.textlength(big, font=f_b)
        d.text(((W - w) / 2, H / 2 - f_b.size * 0.62), big, font=f_b,
               fill=tuple(int(c * reveal) for c in IVORY))
        w2 = d.textlength(lab.upper(), font=f_l)
        tracked(d, ((W - w2) / 2, H / 2 + f_b.size * 0.42), lab.upper(), f_l,
                tuple(int(c * reveal * 0.65) for c in GOLD), 3)
    return im

# ---------------------------------------------------------------- procedural
def bloch_vector(im, cx, cy, r, theta, phi, alpha=255):
    d = ImageDraw.Draw(im, "RGBA")
    # sphere
    for k in range(28):
        rr = r * (1 - k / 28)
        v = int(16 + 70 * (1 - k / 28))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(v, v + 2, v + 6, 30))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 118, 108, 90), width=2)
    d.arc([cx - r, cy - r * 0.34, cx + r, cy + r * 0.34], 0, 360, fill=(120, 118, 108, 60), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(120, 118, 108, 45), width=1)
    d.line([cx, cy - r, cx, cy + r], fill=(120, 118, 108, 45), width=1)
    x = cx + r * math.sin(theta) * math.cos(phi)
    y = cy - r * math.cos(theta)
    d.line([cx, cy, x, y], fill=(201, 162, 39, alpha), width=5)
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(237, 230, 214, alpha))

def proc_frame(shot, i, n, W, H):
    proc = shot["proc"]
    t = i / max(1, n - 1)
    if proc == "bloch":
        im = Image.new("RGB", (W, H), INK)
        d = ImageDraw.Draw(im)
        lab = font("JetBrainsMono.ttf", 22)
        tracked(d, (120, 96), "ONE QUBIT / TWO AMPLITUDES", lab, DIM, 4)
        bloch_vector(im, 660, 560, 300, math.pi * (0.22 + 0.28 * t), math.pi * (0.3 + 1.6 * t))
        f = font("JetBrainsMono.ttf", 46)
        tracked(d, (1150, 486), "|ψ⟩ = α|0⟩ + β|1⟩", f, IVORY, 1)
        fm = font("JetBrainsMono.ttf", 26)
        tracked(d, (1150, 566), "|α|² + |β|² = 1", fm, GOLD, 1)
        d.text((1150, 626), "measurement returns one bit", font=fm, fill=DIM)
        return im
    if proc == "bits":
        im = Image.new("RGB", (W, H), INK)
        d = ImageDraw.Draw(im)
        f = font("InstrumentSerif-Regular.ttf", 46)
        fm = font("JetBrainsMono.ttf", 22)
        tracked(d, (120, 96), "CLASSICAL BIT / QUANTUM BIT", fm, DIM, 4)
        d.text((150, 220), "a bit", font=f, fill=IVORY)
        d.text((150, 300), "one of two states", font=fm, fill=DIM)
        for k, v in enumerate(("0", "1")):
            on = (int(t * 6) % 2) == k
            box = [180 + k * 210, 420, 330 + k * 210, 570]
            d.rectangle(box, outline=GOLD if on else (70, 68, 62), width=4)
            d.text((box[0] + 55, box[1] + 42), v, font=font("InstrumentSerif-Regular.ttf", 70),
                   fill=IVORY if on else (90, 86, 78))
        d.text((1030, 220), "a qubit", font=f, fill=IVORY)
        d.text((1030, 300), "a direction on a sphere", font=fm, fill=DIM)
        bloch_vector(im, 1230, 520, 200, math.pi * 0.5, math.pi * (2 * t))
        return im
    if proc == "surface":
        im = Image.new("RGB", (W, H), INK)
        d = ImageDraw.Draw(im)
        fm = font("JetBrainsMono.ttf", 20)
        fs = font("InstrumentSerif-Regular.ttf", 46)
        tracked(d, (120, 96), "SURFACE CODE  /  ONE LOGICAL QUBIT", fm, DIM, 3)
        n_, cell = 5, 84
        x0, y0 = 200, 300
        pulse = 0.5 + 0.5 * math.sin(t * math.pi * 2)
        for r in range(n_):
            for c in range(n_):
                x, y = x0 + c * cell, y0 + r * cell
                data = (r + c) % 2 == 0
                col = (201, 162, 39) if data else (86, 118, 128)
                d.rectangle([x, y, x + cell - 12, y + cell - 12], outline=col, width=3)
        # the patch that carries one logical qubit
        d.rectangle([x0 - 14, y0 - 14, x0 + 3 * cell - 12 + 14, y0 + 3 * cell - 12 + 14],
                    outline=(int(237 * (0.55 + 0.45 * pulse)), 230, 214), width=3)
        d.text((x0 - 12, y0 + n_ * cell + 26), "one logical qubit  (d = 3)", font=fm, fill=IVORY)

        cx = 800
        d.text((cx, 288), "not one particle", font=fs, fill=IVORY)
        d.text((cx, 348), "a patch of many, measured together", font=fm, fill=DIM)
        # legend
        d.rectangle([cx, 432, cx + 26, 458], outline=(201, 162, 39), width=3)
        d.text((cx + 42, 434), "data qubits  (d²)", font=fm, fill=IVORY)
        d.rectangle([cx, 486, cx + 26, 512], outline=(86, 118, 128), width=3)
        d.text((cx + 42, 488), "check qubits  (d²−1)", font=fm, fill=IVORY)
        rows = ((3, "17", ""), (5, "49", ""), (7, "101", "Google's memory"))
        for k, (dist, phys, note) in enumerate(rows):
            d.text((cx, 578 + k * 40), f"d = {dist}", font=fm, fill=DIM)
            d.text((cx + 130, 578 + k * 40), f"→  {phys} physical qubits", font=fm,
                   fill=IVORY if dist == 7 else DIM)
            if note:
                d.text((cx + 130, 604 + k * 40), note, font=fm, fill=GOLD)
        return im
    if proc == "chart":
        im = Image.new("RGB", (W, H), INK)
        d = ImageDraw.Draw(im)
        fm = font("JetBrainsMono.ttf", 20)
        fs = font("InstrumentSerif-Regular.ttf", 42)
        tracked(d, (120, 96), "GOOGLE WILLOW  /  LOGICAL ERROR PER CYCLE", fm, DIM, 3)
        ox, oy, w, h = 300, 880, 1180, 430
        lo, hi = 0.05, 1.0
        def ypos(v):
            t = (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
            return oy - t * h
        for v, lab in ((1.0, "1.0"), (0.3, "0.3"), (0.1, "0.1"), (0.05, "0.05")):
            y = ypos(v)
            d.line([ox, y, ox + w, y], fill=(46, 44, 40), width=1)
            d.text((ox - 74, y - 10), lab, font=fm, fill=DIM)
        d.line([ox, oy, ox + w, oy], fill=(90, 86, 78), width=2)
        d.line([ox, oy, ox, oy - h - 10], fill=(90, 86, 78), width=2)
        vals = {3: 0.62, 5: 0.29, 7: 0.143}
        pts = []
        for dist in sorted(vals):
            v = vals[dist]
            x = ox + (dist - 3) / 4 * w
            y = ypos(v)
            pts.append((x, y))
            d.text((x - 26, oy + 22), f"d={dist}", font=fm, fill=IVORY)
        for a, b in zip(pts, pts[1:]):
            d.line([a, b], fill=(201, 162, 39), width=3)
        for (x, y), dist in zip(pts, sorted(vals)):
            d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=GOLD)
            dy = -46 if dist == 7 else -40
            d.text((x + 22, y + dy), f"{vals[dist]*100:.2f}%", font=fm, fill=IVORY)
        d.text((ox - 30, 190), "logical error per cycle", font=fs, fill=IVORY)
        tracked(d, (ox - 26, 262), "×2.14 PER +2 DISTANCE", fm, GOLD, 3)
        d.text((ox - 26, 300), "better hardware alone does not fix it", font=fm, fill=DIM)
        d.text((ox - 26, 330), "the code has to grow with the machine", font=fm, fill=DIM)
        return im
    return Image.new("RGB", (W, H), INK)

# ---------------------------------------------------------------- ffmpeg
def encode_shot(shot, frames_iter, out_path, text_path, W, H, fps):
    n = shot["frames"]
    dur = n / fps
    vf = ["noise=alls=5:allf=t+u", "vignette=angle=PI/4.6",
          "eq=contrast=1.055:brightness=-0.004:saturation=0.94"]
    fi, fo = shot.get("fade_in", 0), shot.get("fade_out", 0)
    if fi:
        vf.append(f"fade=t=in:st=0:d={fi/fps:.3f}")
    if fo:
        vf.append(f"fade=t=out:st={max(0,dur-fo/fps):.3f}:d={fo/fps:.3f}")
    inputs = ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    if text_path and os.path.exists(text_path):
        inputs += ["-loop", "1", "-i", text_path]
        tf = f"[1:v]format=rgba,fade=t=in:st=0:d=0.65:alpha=1"
        if dur > 1.8:
            tf += f",fade=t=out:st={dur-0.65:.3f}:d=0.65:alpha=1"
        fc = ("[0:v]" + ",".join(vf) + "[bg];" + tf + "[tx];[bg][tx]overlay=0:0:format=auto[o]")
        mapv = "[o]"
    else:
        fc = "[0:v]" + ",".join(vf) + "[o]"
        mapv = "[o]"
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + [
        "-filter_complex", fc, "-map", mapv, "-t", f"{dur:.4f}",
        "-c:v", "libx264", "-preset", os.environ.get("PRESET", "medium"),
        "-crf", os.environ.get("CRF", "19"),
        "-pix_fmt", "yuv420p", "-g", "48", "-keyint_min", "48", "-sc_threshold", "0",
        "-x264-params", "keyint=48:min-keyint=48:scenecut=0:bframes=3:ref=3",
        "-threads", "2", out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in frames_iter:
        p.stdin.write(f.tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg failed for " + shot["id"])

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", default="shots.json")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--of", type=int, default=1)
    ap.add_argument("--out", default="out")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--selftest", action="store_true",
                    help="render one still frame per shot kind at low res, no video")
    args = ap.parse_args()

    with open(os.path.join(ROOT, args.plan)) as f:
        plan = json.load(f)
    W, H, fps = plan.get("w", 1920), plan.get("h", 1080), plan.get("fps", 24)
    shots = plan["shots"]
    if args.limit:
        shots = shots[:args.limit]

    if args.selftest:
        os.makedirs("/tmp/opencode/selftest", exist_ok=True)
        cache = PlateCache(6)
        seen = {}
        for s in shots:
            k = s["kind"] + ":" + s.get("proc", "")
            if k in seen:
                continue
            seen[k] = True
            n = s["frames"]
            i = n // 2
            w, h = (640, 360) if s["kind"] == "photo" else (1920, 1080)
            if s["kind"] == "photo":
                p = os.path.join(ROOT, s["plate"])
                if not os.path.exists(p):
                    continue
                fr = photo_frame(cache.get(p), s, i, n, w, h)
            elif s["kind"] == "card":
                fr = card_frame(s, i, n, w, h)
            else:
                fr = proc_frame(s, i, n, w, h)
            out = f"/tmp/opencode/selftest/{s['id']}_{k.replace(':', '_')}.png"
            fr.save(out)
            print("selftest", out)
        return

    # split the plan into equal-cost shards by frame count
    total = sum(s["frames"] for s in shots)
    target = total / args.of
    bounds, acc = [0], 0
    for idx, s in enumerate(shots):
        acc += s["frames"]
        if len(bounds) < args.of and acc >= target * len(bounds) - target * 0.15:
            bounds.append(idx + 1)
    while len(bounds) < args.of + 1:
        bounds.append(len(shots))
    bounds[-1] = len(shots)
    mine = shots[bounds[args.shard]:bounds[args.shard + 1]]

    tmp = os.path.join(ROOT, args.out, f"tmp_{args.shard:02d}")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(os.path.join(ROOT, args.out), exist_ok=True)
    cache = PlateCache(5)

    for k, shot in enumerate(mine):
        n = shot["frames"]
        out_path = os.path.join(tmp, f"shot_{k:04d}.mp4")
        tp = shot.get("text")
        tp = os.path.join(ROOT, tp) if tp else None
        if shot["kind"] == "photo":
            plate = cache.get(os.path.join(ROOT, shot["plate"]))
            gen = (photo_frame(plate, shot, i, n, W, H) for i in range(n))
        elif shot["kind"] == "card":
            gen = (card_frame(shot, i, n, W, H) for i in range(n))
        else:
            gen = (proc_frame(shot, i, n, W, H) for i in range(n))
        encode_shot(shot, gen, out_path, tp, W, H, fps)
        print(f"[shard {args.shard}] {k+1}/{len(mine)} {shot['id']} {n}f", flush=True)

    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for k in range(len(mine)):
            f.write(f"file '{tmp}/shot_{k:04d}.mp4'\n")
    seg = os.path.join(ROOT, args.out, f"seg_{args.shard:02d}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c", "copy", seg], check=True)
    print("WROTE", seg, os.path.getsize(seg) // 1024, "KB", flush=True)

if __name__ == "__main__":
    main()
