#!/usr/bin/env python3
"""Build the film's subtitle file from the per-act edge-tts VTTs.

Cue times in each VTT are relative to that act's MP3, so every cue is shifted
by the act's start time on the finished timeline.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TS = re.compile(r"(\d+):(\d+):(\d+)[.,](\d+)")


def secs(t):
    h, m, s, ms = TS.match(t).groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def stamp(t):
    if t < 0:
        t = 0.0
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def cues(path):
    lines = open(path, encoding="utf-8").read().replace("\r", "").split("\n")
    out, i = [], 0
    while i < len(lines):
        if "-->" in lines[i]:
            a, b = [x.strip().split()[0] for x in lines[i].split("-->")]
            i += 1
            text = []
            while i < len(lines) and lines[i].strip():
                text.append(lines[i].strip())
                i += 1
            # drop the repeated part-level cue that edge-tts emits
            body = " ".join(text).strip()
            if body and not body.startswith("&"):
                out.append((secs(a), secs(b), body))
        i += 1
    return out


def main():
    meta = json.load(open(os.path.join(ROOT, "narration.json")))
    rows = []
    for sec, start in zip(meta["sections"], meta["starts"]):
        p = os.path.join(ROOT, "narration", sec + ".vtt")
        if not os.path.exists(p) or os.path.getsize(p) < 200:
            print("no usable vtt for", sec, file=sys.stderr)
            continue
        for a, b, text in cues(p):
            rows.append((a + start, min(b + start, meta["total"]), text))
    rows.sort(key=lambda r: r[0])

    # merge cues that overlap so players never flicker two lines at once
    merged = []
    for a, b, text in rows:
        if merged and a < merged[-1][1] + 0.02:
            pa, pb, pt = merged[-1]
            merged[-1] = (pa, max(pb, b), pt if text in pt else (pt + " " + text))
        else:
            merged.append((a, b, text))

    out = os.path.join(ROOT, "out", "quantum.srt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for i, (a, b, text) in enumerate(merged, 1):
            f.write(f"{i}\n{stamp(a)} --> {stamp(b)}\n{text}\n\n")
    print("cues", len(merged), "->", out)


if __name__ == "__main__":
    main()
