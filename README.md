# The Machine That Borrows the Universe

A ~28 minute documentary about quantum computing, cut from archival photographs,
rendered entirely on GitHub Actions.

## What is in here

| path | what it is |
| --- | --- |
| `script/` | the narration script, one file per act |
| `narration/` | recorded narration: `s00`–`s06` MP3 + WebVTT cues |
| `music/` | score, Scott Buckley, CC BY 4.0 |
| `src/` | source stills from Wikimedia Commons (see `CREDITS.md`) |
| `beats.py` | the edit: which photograph, for how long, with what camera move |
| `prep.py` | crops and tones stills into 3200×1800 plates |
| `timeline.py` | act start/end times, recomputed from the MP3s |
| `make_plan.py` | beats + timeline → `shots.json` |
| `textgen.py` | lower-third captions and source lines → transparent PNGs |
| `build_audio.py` | narration + ducked score → `audio/master.wav` at −16 LUFS |
| `render.py` | renders a shard of shots to x264 segments |
| `tools/` | subtitles, poster, source manifests, a small test plan |

## How it renders

Nothing heavy runs locally. `.github/workflows/render.yml` has three stages:

1. **plan** — builds plates, text layers, `shots.json`, the subtitle file and the
   audio master; uploads them as artifacts.
2. **render** — 16 parallel shards. Each renders its shots frame by frame in
   floating point from the 3200×1800 plates, pipes raw RGB into ffmpeg, and
   adds grain, vignette and grade there. Each shard concatenates to `seg_XX.mp4`.
3. **assemble** — concatenates the 16 segments without re-encoding, muxes the
   audio, builds the poster, verifies duration and frame count, and publishes a
   release with the finished MP4, the SRT and the poster PNG.

Everything is keyed to `narration.json`: picture and sound are cut from the same
timeline, so they cannot drift.

### Running it

```bash
gh workflow run render.yml -f shards=16 -f crf=19
```

Outputs land on the run's release page. Artifacts expire after 2 days (segments)
and 7 days (final film).

## Re-cutting the film

Change `beats.py` (lengths in seconds, zoom range, focus, pan) and re-run. Long
stills are automatically split into two or three shots with different camera
moves, so a 20-second photograph is never dead air.

To change the words: edit `narration/s0X.txt`, regenerate that act with
`edge-tts --voice en-US-AndrewNeural --rate=+0% --pitch=+0Hz -f narration/s0X.txt
--write-media narration/s0X.mp3 --write-subtitles narration/s0X.vtt`, and push.
`timeline.py` and `make_plan.py` re-derive everything downstream.

## Licence

Narration and edit: this project. Photographs: Wikimedia Commons, per file.
Score: CC BY 4.0, Scott Buckley. See `CREDITS.md`.
