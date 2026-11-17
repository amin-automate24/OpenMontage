#!/usr/bin/env python3
"""Effets S3 modules par le mouvement reel (film_motion). Nouveaux fichiers uniquement."""
import subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import film_motion as fm
ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "12_EDITING" / "S3_cut_v1.mp4"
S = ROOT / "11_AUDIO" / "SOUND_EFFECTS"
OUT = S / "GATED"
JOBS = [
    ("SFX_s3_tissu_noeud_aFRuRZWfSh.mp3", 0.0, 6.4, (0.2, 0.2, 0.8, 0.8), 1.2, "G_s3-01_tissu"),
    ("SFX_s3_grains_montent_cpLMLUe0eP.mp3", 12.8, 20.0, (0.2, 0.1, 0.8, 0.8), 1.0, "G_s3-03_grains"),
    ("SFX_s3_traits_pigment_eI7o7AgdqL.mp3", 32.0, 40.0, (0.1, 0.1, 0.9, 0.9), 1.0, "G_s3-06_traits"),
    ("SFX_s3_drapeaux_TdlplRwVNR.mp3", 47.0, 55.4, (0.3, 0.2, 0.9, 0.8), 1.0, "G_s3-08_drapeaux"),
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
