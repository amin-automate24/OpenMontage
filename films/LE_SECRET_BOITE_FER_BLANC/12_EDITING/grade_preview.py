#!/usr/bin/env python3
"""Planche avant/apres : grade_preview.py OUT.png  (images fixes tirees des segments, grade appliquee)."""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
from film_grades import GRADES_V1 as G
A = Path(__file__).parent / "AUDIO"
FR = [("MIX_S3_v4.mp4", 30, "S3 or"), ("MIX_S3_v4.mp4", 50, "S3 mur"), ("MIX_S3_v4.mp4", 62, "S3-10 foule"),
      ("MIX_S4_final_v4.mp4", 12, "S4 foule"), ("MIX_S5_v9.mp4", 4, "S5-01"), ("MIX_S5_v9.mp4", 20, "S5-03"),
      ("MIX_S6_v4.mp4", 4, "S6-01"), ("MIX_S6_v4.mp4", 20, "S6-03"), ("MIX_S6_v4.mp4", 72, "S6-10 drapeau")]
def frame(f, t, vf, out):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(A / f), "-frames:v", "1"]
    # le temps t des expressions : ffmpeg repart de 0 apres -ss en entree ; on utilise -ss en sortie pour garder t
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(A / f), "-ss", str(t), "-frames:v", "1"]
    if vf: cmd += ["-vf", vf]
    cmd += ["-vf", (vf + "," if vf else "") + "scale=560:-1"] if False else []
    cmd += [str(out)]
    subprocess.run(cmd, check=True)
rows = []
for f, t, label in FR:
    frame(f, t, "", "/tmp/_a.png"); frame(f, t, G[f], "/tmp/_b.png")
    a, b = [Image.open(p).convert("RGB").resize((560, 315)) for p in ("/tmp/_a.png", "/tmp/_b.png")]
    for im, tag in ((a, "avant"), (b, "apres")):
        d = ImageDraw.Draw(im); d.rectangle((0, 0, 150, 16), fill=(0, 0, 0)); d.text((3, 2), f"{label} {tag}", fill=(255, 255, 0))
    r = Image.new("RGB", (1120, 315)); r.paste(a, (0, 0)); r.paste(b, (560, 0)); rows.append(r)
s = Image.new("RGB", (1120, 315 * len(rows)))
for i, r in enumerate(rows): s.paste(r, (0, i * 315))
s.save(sys.argv[1])
