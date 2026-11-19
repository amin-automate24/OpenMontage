#!/usr/bin/env python3
"""Exports NON FINAL (autorisation utilisateur du 19/11/2026, contrôle interne uniquement) :
SCOLAIRE (sous-titres FR incrustés) et CINÉMA (sans incrustation + SRT séparé).
Image = QC3 SON2 (copie décodée) + SH08 v003b (photo BnF/Agence Rol 156948) sur les seules images du plan SH08 + générique V005 minutage (BnF + Anefo).
Son = mix validé QC2 SON2 (WAV source du master), prolongé par du silence. Refuse d'écraser."""
import subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent; A = R/"animatic"; O = R/"deliverables/NON_FINAL"
MASTER = A/"MASTER_CANDIDATE_NON_FINAL_QC3_SON2_1080p.mp4"; SH08 = A/"qc2/MAQUETTE_SH08_v003b_APRES_raw.mp4"
GEN = A/("qc2/GENERIQUE_FIN_v005_minutage_BnF_Anefo_c3_12s6_c1rapide.mp4" if "--v2" in sys.argv else "qc2/GENERIQUE_FIN_v005_minutage_BnF_Anefo_c3_12s6.mp4")
SUF = "_v2" if "--v2" in sys.argv else ""; WAV = R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav"
ASS = A/"SUBTITLES_FR_QC3_v002_option_cue10_style1080.ass"
SH08_T0 = 36.04                                 # 1re image du plan SH08 dans QC3 (image 901)
N_FILM, N_GEN = 6903, 572; TOTAL = (N_FILM+N_GEN)/25
def run(name, subs):
    out = O/name; assert not out.exists(), f"refus d'écraser {out}"
    v = f"[0:v][1:v]overlay=0:0:eof_action=pass:repeatlast=0,trim=end_frame={N_FILM},setpts=PTS-STARTPTS[f];[2:v]setpts=PTS-STARTPTS[g];[f][g]concat=n=2:v=1:a=0[c]"
    v += f";[c]subtitles='{ASS}'[v]" if subs else ";[c]null[v]"
    a = f"[3:a]aresample=48000,apad=whole_dur={TOTAL}[a]"
    cmd = ["ffmpeg", "-v", "error", "-n", "-i", str(MASTER), "-itsoffset", str(SH08_T0), "-i", str(SH08), "-i", str(GEN), "-i", str(WAV),
           "-filter_complex", v+";"+a, "-map", "[v]", "-map", "[a]", "-t", f"{TOTAL}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "25", "-g", "50",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
           "-metadata", "title=LE CARNET DE LA LIBERTÉ — NON FINAL (contrôle interne)", "-metadata", "comment=NON FINAL — diffusion non autorisée", str(out)]
    subprocess.run(cmd, check=True); print("écrit", out)
O.mkdir(parents=True, exist_ok=True)
run(f"LE_CARNET_DE_LA_LIBERTE_SCOLAIRE_NON_FINAL{SUF}_1080p.mp4", True)
run(f"LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL{SUF}_1080p.mp4", False)
srt = O/f"LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL{SUF}_FR.srt"; assert not srt.exists()
srt.write_bytes((A/"SUBTITLES_FR_QC3_v002_option_cue10.srt").read_bytes()); print("écrit", srt)
