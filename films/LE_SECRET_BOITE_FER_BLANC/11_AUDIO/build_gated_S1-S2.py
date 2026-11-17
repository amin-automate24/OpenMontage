#!/usr/bin/env python3
"""Genere les effets S1-S2 module par le mouvement reel des plans (film_motion). Nouveaux fichiers uniquement."""
import subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import film_motion as fm

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "12_EDITING" / "FILM_S1-S2_cut_v1.mp4"
S = ROOT / "11_AUDIO" / "SOUND_EFFECTS"
OUT = S / "GATED"
JOBS = [
    ("SFX_s1_perles_bois_jUesQk8LD0.mp3", 20.9, 28.0, (0.05, 0.05, 0.55, 0.7), 1.0, "G_s1-04_perles"),
    ("SFX_s1_pas_zellige_EbAQBaauuO.mp3", 28.2, 35.6, (0.2, 0.1, 0.8, 0.95), 1.2, "G_s1-05_pas"),
    ("SFX_s1_escalier_rampe_eI7XzexdqL.mp3", 46.0, 53.8, (0.1, 0.1, 0.9, 0.95), 1.2, "G_s1-08_escalier"),
    ("SFX_s1_porte_grince_XmOoWoxBfo.mp3", 61.8, 65.2, (0.2, 0.1, 0.9, 0.95), 1.2, "G_s1-10_porte"),
    ("SFX_s2_pas_poussiere_mE6vDaThJQ.mp3", 77.0, 94.4, (0.15, 0.15, 0.85, 0.95), 1.4, "G_s2-03b-04_pas"),
    ("SFX_s2_tapis_laine_jUesFgfLD0.mp3", 94.6, 101.0, (0.25, 0.4, 0.8, 0.85), 1.0, "G_s2-05_tapis"),
    ("SFX_s2_coffre_couvercle_P3f9sY142C.mp3", 101.6, 109.5, (0.4, 0.3, 0.95, 0.9), 1.2, "G_s2-06_coffre"),
    ("SFX_s2_boite_glisse_P3f9sWr42C.mp3", 117.3, 120.0, (0.05, 0.05, 0.95, 0.95), 1.0, "G_s2-08_glisse"),
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
