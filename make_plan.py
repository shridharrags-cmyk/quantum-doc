#!/usr/bin/env python3
"""Turn the beat sheet + narration timeline into shots.json.

Beats whose plate is missing are dropped and the remaining weights are
renormalised, so a missing photograph shortens nothing on the clock.
"""
import json, os, sys
from beats import BEATS

ROOT = os.path.dirname(os.path.abspath(__file__))
FPS = 24
CARD = 58  # ~2.4 s chapter card

# chapter card that opens each act; act 0 opens on the title instead
CARDS = {
    0: dict(kind="title", title="THE MACHINE THAT BORROWS THE UNIVERSE",
            sub="QUANTUM COMPUTING · 1900 — 2026"),
    1: dict(kind="chapter", num="I", title="The reluctant revolution", sub="1900 — 1935"),
    2: dict(kind="chapter", num="II", title="Information is physical", sub="1961 — 1996"),
    3: dict(kind="chapter", num="III", title="The machine", sub="1995 — 2020"),
    4: dict(kind="chapter", num="IV", title="The error", sub="2019 — 2024"),
    5: dict(kind="chapter", num="V", title="The race", sub="2025 — 2026"),
    6: dict(kind="chapter", num="VI", title="The ledger", sub=""),
}

PROMAP = {"surface": "surface", "willow_chart": "chart"}


ASSUME = "--assume-plates" in sys.argv


def plate_exists(key):
    if ASSUME:
        return True
    return os.path.exists(os.path.join(ROOT, "assets", "plates", key + ".jpg"))


def split_beat(b):
    """Cut a long still into two or three shots with different camera moves.

    The reference film cuts about every ten seconds; a 20 s photograph is dead
    air, so it is revisited with a new crop, a new direction and a new speed.
    """
    if b.get("kind", "photo") != "photo" or b["w"] < 13:
        return [b]
    parts = 3 if b["w"] >= 26 else 2
    out = []
    for k in range(parts):
        c = dict(b)
        c["w"] = b["w"] / parts
        z0, z1 = b["z"]
        f0, f1 = b["f"]
        if k == 1:
            c["z"] = (z1, z0)                       # pull back instead of push in
            c["f"] = (f0 + 0.055, f1 + 0.02)
            c["pan"] = (-b.get("pan", (0, 0))[0], b.get("pan", (0, 0))[1])
        elif k == 2:
            c["z"] = (z0 * 1.02, z1 * 1.07)         # tighter, slower
            c["f"] = (f0 - 0.05, f1 - 0.015)
            c["pan"] = (b.get("pan", (0, 0))[0], -b.get("pan", (0, 0))[1])
        if k:                                       # caption only on the first pass
            c.pop("cap", None)
        out.append(c)
    return out


def main():
    meta = json.load(open(os.path.join(ROOT, "narration.json")))
    starts, ends, total = meta["starts"], meta["ends"], meta["total"]
    secs = meta["sections"]
    shots, dropped, n = [], [], 0

    prev_end = 0
    for si, sec in enumerate(secs):
        s0 = int(round(starts[si] * FPS))
        s1 = int(round(ends[si] * FPS))
        card = CARDS.get(si)

        # chapter cards live in the silence between acts; the title card opens
        # the film from black; the credits run over the score's tail
        body_start = prev_end + CARD if card else prev_end
        if card:
            n += 1
            shots.append(dict(id=f"sh{n:03d}", kind="card", frames=CARD,
                              card=card["kind"], title=card.get("title", ""),
                              sub=card.get("sub", ""), num=card.get("num", ""),
                              fade_in=0, fade_out=0))

        beats = []
        for b in BEATS[si]:
            if b.get("kind", "photo") == "photo" and not plate_exists(b["k"]):
                dropped.append((sec, b["k"]))
                continue
            beats.append(b)
        if not beats:
            sys.exit("no beats left for " + sec)
        beats = [p for b in beats for p in split_beat(b)]

        span = s1 - body_start
        wsum = sum(b["w"] for b in beats)
        acc, cur = 0.0, body_start
        for j, b in enumerate(beats):
            acc += b["w"]
            end = s1 if j == len(beats) - 1 else body_start + int(round(span * acc / wsum))
            frames = end - cur
            if frames <= 0:
                continue
            n += 1
            sh = dict(id=f"sh{n:03d}", kind=b.get("kind", "photo"), frames=frames,
                      zoom=[float(b["z"][0]), float(b["z"][1])],
                      focus=[float(b["f"][0]), float(b["f"][1])],
                      pan=[float(b.get("pan", (0, 0))[0]), float(b.get("pan", (0, 0))[1])],
                      fade_in=0, fade_out=0)
            if sh["kind"] == "photo":
                sh["plate"] = f"assets/plates/{b['k']}.jpg"
            else:
                sh["proc"] = PROMAP.get(b["k"], b["k"])
            if b.get("cap"):
                sh["cap"] = b["cap"]
            if b.get("src"):
                sh["src"] = b["src"]
            shots.append(sh)
            cur = end
        prev_end = s1

    # credits over the last of the score
    tail = int(round(total * FPS)) - prev_end
    if tail > 30:
        n += 1
        shots.append(dict(id=f"sh{n:03d}", kind="card", frames=tail, card="credits",
                          title="", sub="", num="", fade_in=0, fade_out=0))

    # bookends: fade up from black, fade down at the end
    shots[0]["fade_in"] = 22
    shots[-1]["fade_out"] = 48

    plan = dict(fps=FPS, w=1920, h=1080,
                total_frames=sum(s["frames"] for s in shots), shots=shots)
    want = int(round(total * FPS))
    if plan["total_frames"] != want:
        sys.exit(f"plan covers {plan['total_frames']} frames, timeline wants {want}")
    shortest = min(x["frames"] for x in shots)
    print("shortest shot", shortest, "frames")
    json.dump(plan, open(os.path.join(ROOT, "shots.json"), "w"), indent=1)
    print(f"shots {len(shots)}  frames {plan['total_frames']}  "
          f"seconds {plan['total_frames']/FPS:.2f}")
    if dropped:
        print("dropped (no plate):", ", ".join(f"{s}:{k}" for s, k in dropped))


if __name__ == "__main__":
    main()
