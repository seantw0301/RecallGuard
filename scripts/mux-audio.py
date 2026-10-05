#!/usr/bin/env python3
"""Mix per-caption audio at the timestamps recorded by the Playwright run into the demo video."""
import json, subprocess
from pathlib import Path

A = Path(__file__).resolve().parent.parent / "artifacts"
tl = json.loads((A / "audio" / "timeline.json").read_text())  # [{"key":..., "t": seconds}]
cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", str(A / "recallguard-demo.webm")]
for e in tl:
    cmd += ["-i", str(A / "audio" / f"{e['key']}.wav")]
parts = [f"[{i + 1}:a]adelay={int(e['t'] * 1000)}:all=1[a{i}]" for i, e in enumerate(tl)]
mix = "".join(f"[a{i}]" for i in range(len(tl))) + f"amix=inputs={len(tl)}:normalize=0[aout]"
cmd += ["-filter_complex", ";".join(parts + [mix]), "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest",
        str(A / "recallguard-demo-audio.mp4")]
subprocess.run(cmd, check=True)
print("wrote", A / "recallguard-demo-audio.mp4")
