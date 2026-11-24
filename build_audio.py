#!/usr/bin/env python3
"""Assemble the finished stereo master: narration + ducked score, -16 LUFS.

Runs on the build machine (GitHub Actions), never on the phone.  Uses only the
timeline in narration.json, so the audio is sample-locked to the shot plan.
"""
import json, math, os, subprocess, wave
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
SR = 48000

# one track per act, and how far into the track that act starts
# cue per act, chosen so every track outlasts its act (offsets skip intros)
SCORE = [
    ("Convergence", 0),            # cold open  103 s
    ("MemoriesOfStone", 30),       # act I      281 s
    ("Penumbra", 20),              # act II     309 s
    ("Unraveling", 40),            # act III    256 s
    ("Katabasis_I", 30),           # act IV     246 s
    ("TheLongDark", 20),           # act V      301 s
    ("AdriftAmongInfiniteStars", 20),  # act VI  187 s
]


def decode(path, ch, sr=SR):
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", path, "-f", "s16le",
        "-ac", str(ch), "-ar", str(sr), "-"])
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    return a.reshape(-1, ch) if ch > 1 else a


def write_wav(path, data, sr=SR):
    if data.ndim == 1:
        data = np.stack([data, data], 1)
    pcm = (np.clip(data, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def fit(a, n):
    """Pad or trim to exactly n frames, along time only (works for stereo)."""
    if len(a) >= n:
        return a[:n]
    pad = [(0, n - len(a))] + [(0, 0)] * (a.ndim - 1)
    return np.pad(a, pad, mode="constant")


def main():
    meta = json.load(open(os.path.join(ROOT, "narration.json")))
    starts, ends, total = meta["starts"], meta["ends"], meta["total"]
    os.makedirs(os.path.join(ROOT, "audio"), exist_ok=True)

    # ---- narration track, placed exactly on the timeline
    narr = np.zeros(int(round(total * SR)) + SR, np.float32)
    for s, a, b in zip(meta["sections"], starts, ends):
        seg = decode(os.path.join(ROOT, "narration", s + ".mp3"), 1)
        seg = fit(seg, int(round((b - a) * SR)))
        i = int(round(a * SR))
        narr[i:i + len(seg)] += seg
    narr = narr[:int(round(total * SR))]
    print("narration", len(narr) / SR, "s")

    # ---- score bed: equal-power crossfade at every act boundary
    n = len(narr)
    bed = np.zeros((n, 2), np.float32)
    fade = int(7.0 * SR)
    for i, (name, offset) in enumerate(SCORE):
        a = int(round(starts[i] * SR))
        b = int(round((starts[i + 1] if i + 1 < len(starts) else total) * SR))
        # each cue runs to the boundary plus one fade, so the next cue's fade-in
        # and this cue's fade-out overlap: equal power, no hole at the cut
        need = (b - a) + fade
        path = os.path.join(ROOT, "music", name + ".mp3")
        seg = decode(path, 2)
        seg = fit(seg[offset * SR:], need)
        fi = fade if i > 0 else int(2.0 * SR)
        t = np.linspace(0, 1, fi, dtype=np.float32)
        seg[:fi] *= np.sin(t * math.pi / 2)[:, None]         # fade up
        t = np.linspace(0, 1, fade, dtype=np.float32)
        seg[-fade:] *= np.cos(t * math.pi / 2)[:, None]      # fade down
        end = min(a + need, n)
        bed[a:end] += seg[:end - a]
    rms = float(np.sqrt((bed ** 2).mean()))
    bed *= (10 ** (-26 / 20)) / max(rms, 1e-9)
    print("bed rms set to -26 dBFS")

    # ---- duck the score under speech (block follower, fast attack, slow release)
    blk = 240                                   # 5 ms envelope blocks
    nb = len(narr) // blk
    env = np.abs(narr[:nb * blk]).reshape(nb, blk).max(1)
    thr = 0.010
    target = np.clip((env - thr) / (thr * 2.5), 0, 1)
    duck = np.empty_like(target)
    g = 0.0
    for i in range(nb):
        v = float(target[i])
        tau = 0.025 if v > g else 0.55
        coef = 1 - math.exp(-blk / (SR * tau))
        g += (v - g) * coef
        duck[i] = g
    duck = np.pad(np.repeat(duck, blk), (0, len(narr) - nb * blk), mode="edge")
    gain = (1.0 - duck * (1.0 - 10 ** (-11 / 20)))[:, None]
    mix = narr[:, None] + bed * gain
    mix = np.tanh(mix * 1.02) / 1.02
    head, tail = int(1.2 * SR), int(6.0 * SR)
    mix[:head] *= np.linspace(0, 1, head, dtype=np.float32)[:, None]
    mix[-tail:] *= np.linspace(1, 0, tail, dtype=np.float32)[:, None] ** 1.4
    write_wav(os.path.join(ROOT, "audio", "mix_raw.wav"), mix)

    # ---- master
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, "audio", "mix_raw.wav"),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", "48000", "-c:a", "pcm_s16le", os.path.join(ROOT, "audio", "master.wav")],
        check=True)
    print("wrote audio/master.wav",
          os.path.getsize(os.path.join(ROOT, "audio", "master.wav")) // (1024 * 1024), "MB")


if __name__ == "__main__":
    main()
