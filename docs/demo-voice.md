# Demo video: opening + neural voice

Final video = **30 s opening** (problem → solution → full picture) + **product demo**, both voiced by a neural narrator.
Opening rules: first-30-seconds guide (10 / 10 / 10, readable muted, one message per scene).

| Scene | Time | Title (= first spoken sentence) | Shows |
|---|---|---|---|
| Problem | 0–10 s | Your AI remembers everything — and still books the wrong flight. | You → personal AI + memories → Flight A $320, overnight layover (red). "Which memory made it do that?" |
| Solution | 10–20 s | Let AI remember. Keep every memory accountable. | Memories → RecallGuard replay → without M003/M002 no change (green), without M001 changed (red). Same case fixed: Flight A struck → Quarantine M001 → Flight C. Legend HIGH/MEDIUM/LOW. |
| Full picture | 20–30 s | Remove one memory. Replay. See what changes. | REMEMBER → DECIDE (Nemotron on Nebius Token Factory) → **REPLAY (RecallGuard)** → RE-DECIDE (Nemotron on Nebius) → QUARANTINE (you). |

Same data as the product (M001–M003, Flight A $320 / C $355). Colors: green = no effect, red = culprit, blue = RecallGuard.

## Files

| File | Purpose |
|---|---|
| `demo/intro/intro.html` | Self-animating 30 s opening (timeline in JS) |
| `demo/intro/narration-intro.json` | Cue sheet: start seconds + spoken text (change voice/text without re-recording) |
| `demo/record-intro.mjs` | Records the opening → `artifacts/intro-raw.webm` |
| `demo/narration.json` | Demo captions + spoken text |
| `scripts/voice.py` | Kokoro neural TTS: cue sheet → clips → mixed onto video (lines auto-fit their slot) |
| `scripts/mux-audio.py` | Places demo clips at timestamps recorded by Playwright |
| `scripts/assemble-video.sh` | Opening + demo → `artifacts/recallguard-final.mp4` |

## Voice

Kokoro (open model, Apache-2.0) runs **locally** — no text leaves the machine. Voice `af_heart`, loudness-normalised to −16 LUFS.
Needs a Python env with `kokoro-onnx` + `soundfile` and the model files (`kokoro-v1.0.onnx`, `voices-v1.0.bin`) in `$KOKORO_ENV/model`.

```bash
export KOKORO_ENV=/path/to/tts-env     # default: the IntentChain env on this machine
```

## Rebuild

```bash
cd demo && node record-intro.mjs && cd ..
ffmpeg -y -ss "$(cat artifacts/intro-lead.txt)" -i artifacts/intro-raw.webm -t 30.5 -an -c:v libx264 -pix_fmt yuv420p -r 30 artifacts/intro-silent.mp4
$KOKORO_ENV/bin/python -I scripts/voice.py artifacts/intro-silent.mp4 artifacts/intro-voice.mp4 demo/intro/narration-intro.json
scripts/record-demo.sh          # demo + voice
scripts/assemble-video.sh       # → artifacts/recallguard-final.mp4 (≈2:16)
```
