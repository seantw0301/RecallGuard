#!/usr/bin/env python3
"""Generate narration audio (macOS `say`) for demo/narration.json -> artifacts/audio/*.wav + durations.json."""
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "audio"
OUT.mkdir(parents=True, exist_ok=True)
VOICE = "Samantha"

def speakable(t: str) -> str:
    for n, w in (("M001", "M one"), ("M002", "M two"), ("M003", "M three")):
        t = t.replace(n, w)
    t = t.replace("→", "to").replace("×", " times").replace("·", ",").replace("—", ",")
    t = t.replace("“", "").replace("”", "").replace("9 real", "nine real").replace("3×", "three times")
    return re.sub(r"\s+", " ", t).strip()

narr = json.loads((ROOT / "demo" / "narration.json").read_text())
durations = {}
for key, v in narr.items():
    aiff, wav = OUT / f"{key}.aiff", OUT / f"{key}.wav"
    subprocess.run(["say", "-v", VOICE, "-r", "175", "-o", str(aiff), speakable(v["text"])], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(aiff), "-ar", "44100", "-ac", "1", str(wav)], check=True)
    aiff.unlink()
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)],
                       capture_output=True, text=True, check=True).stdout
    durations[key] = round(float(d), 2)
(OUT / "durations.json").write_text(json.dumps(durations, indent=1))
print(durations)
