#!/usr/bin/env python3
"""Compute the narration timeline from the section MP3s.

Writes narration.json with the start/end of every act in seconds.  This is the
single source of truth for both the audio mix and the shot plan, so picture and
sound cannot drift apart.  Nothing is time-stretched: each act keeps its own
natural duration and the joins are filled with exact digital silence.
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SECTIONS = ["s00", "s01", "s02", "s03", "s04", "s05", "s06"]
PRE = 3.0      # silence before the first word
GAP = 2.6      # silence between acts (the chapter card sits in here)
TAIL = 9.0     # music-only tail after the last word


def duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", path])
    return float(out.strip())


def main():
    durations = []
    for s in SECTIONS:
        p = os.path.join(ROOT, "narration", s + ".mp3")
        if not os.path.exists(p):
            sys.exit("missing narration/" + s + ".mp3")
        durations.append(duration(p))

    starts, ends = [], []
    cursor = PRE
    for i, d in enumerate(durations):
        starts.append(cursor)
        ends.append(cursor + d)
        cursor += d + (GAP if i < len(SECTIONS) - 1 else TAIL)

    meta = dict(total=cursor, pre=PRE, gap=GAP, tail=TAIL,
                sections=SECTIONS, starts=starts, ends=ends, durations=durations)
    with open(os.path.join(ROOT, "narration.json"), "w") as f:
        json.dump(meta, f, indent=1)
    print(f"total {cursor:.1f}s ({cursor/60:.2f} min)")
    for s, d, a, b in zip(SECTIONS, durations, starts, ends):
        print(f"  {s:5} {d:7.2f}s  {a:8.2f} -> {b:8.2f}")


if __name__ == "__main__":
    main()
