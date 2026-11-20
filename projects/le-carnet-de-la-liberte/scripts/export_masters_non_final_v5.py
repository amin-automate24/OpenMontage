#!/usr/bin/env python3
"""CINÉMA v5 NON FINAL (autorisation du 20/11/2026 : crédits anonymes option A + retrait de la photo BnF en SH08, repli réencodage complet).
Dérivé de export_masters_non_final_v4.py (conservé) : plus de surimpression SH08 BnF (SH08 = plan du master QC3), générique v006 anonyme, piste audio AAC du v4 recopiée telle quelle. Réglages x264 et étalonnage nuit identiques à v4.
Masters NON FINAL v4 (autorisation utilisateur du 19/11/2026 « AUTHORIZED MASTER INTEGRATION — NON_FINAL ONLY »).
Pipeline identique à export_masters_non_final.py --v2 (sources 1re génération : QC3 SON2 + SH08 v003b + générique V005
c1rapide + mix WAV QC2 SON2 + ASS QC3 v002 cue10 ; x264 medium CRF 17 g50 ; AAC 192k) + balisage couleur v3
(primaires/transfert BT.709, matrice SMPTE 170M, plage limitée), avec UNE seule modification artistique :
LUT NUIT1953_SH21-23_releve_doux.cube — poids 0->1 de l'image globale 3001 à 3014 (SH21), plein jusqu'à 3638 (SH22-SH23),
aucun effet à partir de 3639 (SH24). Les images hors 3001-3638 ne subissent aucune conversion.
SCOLAIRE : sous-titres incrustés APRÈS l'étalonnage (texte non étalonné). Refuse d'écraser ; v3 et SRT intacts."""
import subprocess, shutil
from pathlib import Path
R = Path(__file__).resolve().parent.parent; A = R/"animatic"; O = R/"deliverables/NON_FINAL_v5"
MASTER = A/"MASTER_CANDIDATE_NON_FINAL_QC3_SON2_1080p.mp4"; V4 = R/"deliverables/NON_FINAL_v4/LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v4_1080p.mp4"
GEN = A/"qc2/GENERIQUE_FIN_v006_anonyme_c3_12s6.mp4"
ASS = A/"SUBTITLES_FR_QC3_v002_option_cue10_style1080.ass"; LUT = R/"deliverables/DAVINCI_PREP/NUIT1953_SH21-23_releve_doux.cube"
SRT_V3 = R/"deliverables/NON_FINAL/LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v3_FR.srt"
N_FILM, N_GEN = 6903, 572; TOTAL = (N_FILM+N_GEN)/25
G0, G1, RAMP = 3001, 3639, 13          # images globales : début SH21, début SH24 (exclu), rampe 3001->3014
for p in (MASTER, V4, GEN, ASS, LUT, SRT_V3): assert p.is_file(), f"source manquante : {p}"
def grade(i, o):
    k = f"clip(floor(T*25+0.5)/{RAMP},0,1)"       # j = image locale (0 = image globale 3001)
    return (f"[{i}]trim=start_frame={G0}:end_frame={G1},setpts=PTS-STARTPTS,scale=in_color_matrix=bt601:in_range=tv,format=gbrp,split[go][gg];"
            f"[gg]lut3d=file='{LUT}',format=gbrp[gl];[go][gl]blend=all_expr='A*(1-({k}))+B*({k})',"
            f"scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p[{o}]")
def run(name, subs):
    out = O/name; assert not out.exists(), f"refus d'écraser {out}"
    v = (f"[0:v]trim=end_frame={N_FILM},setpts=PTS-STARTPTS[f];[1:v]setpts=PTS-STARTPTS[g];"
         f"[f][g]concat=n=2:v=1:a=0[c];[c]split=3[p0][p1][p2];[p0]trim=end_frame={G0},setpts=PTS-STARTPTS[s0];"
         + grade("p1", "s1") + f";[p2]trim=start_frame={G1},setpts=PTS-STARTPTS[s2];[s0][s1][s2]concat=n=3:v=1:a=0[c2]")
    v += f";[c2]subtitles='{ASS}'[v]" if subs else ";[c2]null[v]"
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-n", "-i", str(MASTER), "-i", str(GEN), "-i", str(V4),
           "-filter_complex", v, "-map", "[v]", "-map", "2:a", "-t", f"{TOTAL}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "25", "-g", "50",
           "-colorspace", "smpte170m", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
           "-c:a", "copy", "-movflags", "+faststart",
           "-metadata", "title=LE CARNET DE LA LIBERTÉ — NON FINAL (contrôle interne)", "-metadata", "comment=NON FINAL — diffusion non autorisée", str(out)]
    subprocess.run(cmd, check=True); print("écrit", out)
if __name__ == "__main__":
    import sys
    O.mkdir(parents=True, exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("both", "cinema"):
        run("LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v5_1080p.mp4", False)
        srt = O/"LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v5_FR.srt"; assert not srt.exists()
        shutil.copyfile(SRT_V3, srt); print("écrit", srt, "(copie octet pour octet du SRT v3)")
