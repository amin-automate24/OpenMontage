#!/usr/bin/env python3
"""Assemblage S1-S6 : fondus enchaines video + acrossfade audio aux jonctions. Sources en lecture seule.
Usage : build_film_assembly.py OUT.mp4 [XFADE_SECONDS]"""
import subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent
A = R / "AUDIO"
SEG = [  # (fichier, gain audio dB)
    (A / "MIX_S1-S2_final_v5.mp4", 1.0),
    (A / "MIX_S3_v1.mp4", 0.0),
    (A / "MIX_S4_final_v4.mp4", 0.0),
    (A / "MIX_S5_v8.mp4", 0.0),
    (A / "MIX_S6_v4.mp4", 0.0),
]
out = Path(sys.argv[1]); X = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
if out.exists():
    sys.exit(f"refus d'ecraser {out}")
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=duration","-of","csv=p=0",str(p)],capture_output=True,text=True,check=True).stdout.strip())
ds = [dur(p) for p, _ in SEG]
cmd = ["ffmpeg","-y","-loglevel","error"]
for p, _ in SEG: cmd += ["-i", str(p)]
parts = []
for i, ((p, g), d) in enumerate(zip(SEG, ds)):
    parts.append(f"[{i}:v]trim=0:{d:.4f},setpts=PTS-STARTPTS,fps=24,settb=AVTB[v{i}]")
    parts.append(f"[{i}:a]atrim=0:{d:.4f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB[a{i}]")
vl, al, tot = "v0", "a0", ds[0]
for i in range(1, len(SEG)):
    parts.append(f"[{vl}][v{i}]xfade=transition=fade:duration={X}:offset={tot - X:.4f}[xv{i}]")
    parts.append(f"[{al}][a{i}]acrossfade=d={X}:c1=qsin:c2=qsin[xa{i}]")
    vl, al, tot = f"xv{i}", f"xa{i}", tot + ds[i] - X
parts.append(f"[{al}]alimiter=limit=0.89:level=disabled[aout]")
cmd += ["-filter_complex", ";".join(parts), "-map", f"[{vl}]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
print(out, round(tot, 2))
