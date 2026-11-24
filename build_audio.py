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
SCORE = [
    ("MemoriesOfStone", 0),
    ("Convergence", 0),
    ("Unraveling", 20),
    ("Penumbra", 10),
    ("TheLongDark", 20),
    ("Katabasis_I", 30),
    ("AdriftAmongInfiniteStars", 10),
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
    """Pad or trim to exactly n samples."""
    if len(a) >= n:
        return a[:n]
    return np.pad(a, (0, n - len(a)), mode="constant")


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
    write_wav(os.path.join(ROOT, "audio", "narr.wav"), narr)
    print("narration", len(narr) / SR, "s")

    # ---- score bed: equal-power crossfade at every act boundary
    n = len(narr)
    bed = np.zeros((n, 2), np.float32)
    fade = int(7.0 * SR)
    for i, (name, offset) in enumerate(SCORE):
        a = int(round(starts[i] * SR))
        b = int(round((ends[i + 1] if i + 1 < len(ends) else total) * SR))
        need = max(b - a, SR) + fade
        path = os.path.join(ROOT, "music", name + ".mp3")
        seg = decode(path, 2)
        seg = fit(seg[offset * SR:], need)
        t = np.linspace(0, 1, fade, dtype=np.float32)
        if i > 0:
            seg[:fade] *= np.sin(t * math.pi / 2)[:, None]   # fade up
        seg[-fade:] *= np.cos(t * math.pi / 2)[:, None]      # fade down
        end = min(a + need, n)
        bed[a:end] += seg[:end - a]
    rms = float(np.sqrt((bed ** 2).mean()))
    bed *= (10 ** (-26 / 20)) / max(rms, 1e-9)
    write_wav(os.path.join(ROOT, "audio", "bed.wav"), bed)
    print("bed rms set to -26 dBFS")

    # ---- duck the score under speech (block follower, fast attack, slow release)
    env = np.abs(narr)
    k = int(0.03 * SR)
    env = np.convolve(env, np.ones(k, np.float32) / k, mode="same")
    thr = 0.010
    target = np.clip((env - thr) / (thr * 2.5), 0, 1)
    duck = np.empty_like(target)
    g, blk = 0.0, 256
    for i in range(0, len(target), blk):
        v = float(target[i:i + blk].max())
        tau = 0.025 if v > g else 0.55
        coef = 1 - math.exp(-blk / (SR * tau))
        g += (v - g) * coef
        duck[i:i + blk] = g
    gain = (1.0 - duck * (1.0 - 10 ** (-11 / 20)))[:, None]
    mix = narr[:, None] + bed * gain
    mix = np.tanh(mix * 1.02) / 1.02
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
