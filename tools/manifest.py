#!/usr/bin/env python3
"""Build assets/manifest.json from whatever stills are present in src/.

Treatment is per subject: archival prints get a warm duotone, modern hardware
photography keeps its colour with a gentle grade.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DUO = {"planck", "einstein", "bohr", "heisenberg", "schrodinger", "born", "dirac",
       "solvay", "bell", "feynman", "landauer", "shannon", "eniac", "colossus",
       "punched", "vacuumtube", "difference", "abacus", "sliderule", "filament",
       "bletchley", "apollo"}

FOCUS = {
    "planck": [0.5, 0.34], "einstein": [0.5, 0.36], "bohr": [0.5, 0.34],
    "heisenberg": [0.5, 0.34], "schrodinger": [0.5, 0.33], "born": [0.5, 0.35],
    "dirac": [0.5, 0.34], "feynman": [0.5, 0.34], "landauer": [0.5, 0.38],
    "shannon": [0.5, 0.34], "bell": [0.5, 0.37], "clauser": [0.5, 0.34],
    "aspect": [0.5, 0.36], "zeilinger": [0.5, 0.35], "deutsch": [0.5, 0.34],
    "shor": [0.5, 0.34], "preskill": [0.5, 0.34], "wineland": [0.5, 0.34],
    "haroche": [0.5, 0.38], "benioff": [0.5, 0.40],
}


def main():
    man = []
    for f in sorted(os.listdir(os.path.join(ROOT, "src"))):
        if not f.endswith(".jpg"):
            continue
        key = f[:-4]
        man.append(dict(id=key, src="src/" + f,
                        treat="duo" if key in DUO else "color",
                        focus=FOCUS.get(key, [0.5, 0.5])))
    with open(os.path.join(ROOT, "assets", "manifest.json"), "w") as fh:
        json.dump(man, fh, indent=1)
    print("manifest", len(man), "stills")


if __name__ == "__main__":
    main()
