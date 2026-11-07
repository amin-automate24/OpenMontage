#!/usr/bin/env python3
"""Effets S4 modules par le mouvement reel (film_motion). Nouveaux fichiers uniquement."""
import subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import film_motion as fm
ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "12_EDITING" / "S4_cut_v2.mp4"
S = ROOT / "11_AUDIO" / "SOUND_EFFECTS"
OUT = S / "GATED"
JOBS = [
    ("SFX_s4_pas_sable_XmOIiCZBfo.mp3", 18.8, 25.8, (0.05, 0.3, 0.95, 0.95), 1.0, "G_s4-03_pas"),
    ("SFX_s3_drapeaux_TdlplRwVNR.mp3", 25.8, 33.8, (0.2, 0.05, 0.95, 0.75), 1.0, "G_s4-04_drapeau"),
    ("SFX_s4_sable_doigts_Sy8JfiXUb8.mp3", 66.2, 74.2, (0.2, 0.2, 0.85, 0.9), 1.2, "G_s4-09_sable"),
]
tmp = Path(tempfile.mkdtemp())
for src, t0, t1, roi, power, name in JOBS:
    out = OUT / f"{name}_{t0:.1f}.wav"
    if out.exists():
        print("existe", out.name); continue
    norm = tmp / (name + ".wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(S / src), "-af", "loudnorm=I=-30:TP=-2:LRA=11", "-ar", "48000", "-ac", "1", str(norm)], check=True)
    fm.gate(norm, V, t0, t1, out, roi=roi, floor=0.0, power=power)
    print("ok", out.name)
