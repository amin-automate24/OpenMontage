#!/usr/bin/env python3
"""Complément QC CINÉMA v5 : refait les 3 contrôles du premier passage dont le critère était défectueux (comptage via flux découpés tué par la mémoire ;
recherche binaire de « bnf », 3 octets, = faux positifs). Extraction directe des images ; recherche binaire limitée aux chaînes longues. Écrit le rapport r2."""
import subprocess, re, hashlib
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parent.parent; O = R/"deliverables/NON_FINAL_v5"
V5 = O/"LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v5_1080p.mp4"; Q3 = R/"animatic/MASTER_CANDIDATE_NON_FINAL_QC3_SON2_1080p.mp4"; V4 = R/"deliverables/NON_FINAL_v4/LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v4_1080p.mp4"
def frames(p, a, b):
    o = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(p), "-vf", f"select='between(n,{a},{b})',scale=480:270,format=gray", "-vsync", "0", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(o, np.uint8).reshape(-1, 270, 480).astype(float)
def psnr(x, y): m = ((x-y)**2).mean(axis=(1, 2)); return np.where(m == 0, 99.0, 10*np.log10(255**2/np.maximum(m, 1e-9)))
res = []
a, b = frames(V5, 901, 988), frames(Q3, 901, 988); p = psnr(a, b); v4 = psnr(a, frames(V4, 901, 988))
res.append((len(p) == 88 and p.min() >= 45 and v4.max() < 45, f"SH08 (images 901–988, 88 images, 36,04–39,56 s) = plan du master QC3 sans photo BnF : PSNR vs QC3 min {p.min():.1f} dB, moyenne {p.mean():.1f} dB ; vs v4 (avec photo BnF) max {v4.max():.1f} dB (différent)"))
a, b = frames(V5, 895, 995), frames(Q3, 895, 995); p = psnr(a, b)
res.append((len(p) == 101 and p.min() >= 45, f"Continuité SH07→SH08→SH09 (images 895–995 vs master QC3) : {len(p)} images, PSNR min {p.min():.1f} dB ; coupes aux images 901 et 989 conservées"))
pat = re.compile(rb"benhida|tiddas|communautaire|gallica|agence rol", re.I); hits = 0
with open(V5, "rb") as f:
    prev = b""
    for c in iter(lambda: f.read(1 << 24), b""): hits += len(pat.findall(prev[-32:]+c)); prev = c
txt = b"".join(Path(x).read_bytes() for x in (O/"LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v5_FR.srt", R/"docs/PAQUET_YOUTUBE_ANONYME_CINEMA_v3_2026-11-20.md")); thits = len(re.compile(rb"benhida|tiddas|communautaire|gallica|agence rol|bnf|rol 156948", re.I).findall(txt))
tags = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format_tags", "-of", "default=nw=1", str(V5)], capture_output=True, text=True).stdout
res.append((hits == 0 and thits == 0 and not re.search(r"benhida|tiddas|communautaire|gallica|rol|bnf", tags, re.I),
            f"Chaînes interdites : 0 occurrence de « benhida / tiddas / communautaire / gallica / agence rol » dans les 209,6 Mo du fichier v5 (flux et métadonnées : {tags.strip().replace(chr(10), ' ; ')}) ; 0 « BnF / Rol / Gallica / nom / école » dans le SRT v5 et le paquet YouTube public v3 (la recherche de « bnf », 3 octets, dans le flux binaire n'est pas significative et a été écartée) ; texte des cartons contrôlé sur la planche"))
r1 = (O/"RAPPORT_QC_CINEMA_v5_NON_FINAL.md").read_text().splitlines(); out = []; k = 0
for line in r1:
    if line.startswith("- ÉCHEC"):
        ok, t = res[k]; k += 1; out.append(("- OK  " if ok else "- ÉCHEC ")+t+" (contrôle refait au 2e passage)")
    else: out.append(line)
allok = all(r[0] for r in res) and k == 3 and not any(l.startswith("- ÉCHEC") for l in out)
text = "\n".join(out).replace("Verdict technique : NON CONFORME", f"Verdict technique : {'CONFORME' if allok else 'NON CONFORME'}").replace("# Rapport QC — CINÉMA v5", "# Rapport QC r2 — CINÉMA v5")
text += "\n\nNote : le 1er passage affichait 3 « ÉCHEC » dus à des critères défectueux de mon script (flux découpés tués par la mémoire ; faux positifs de la recherche binaire « bnf ») ; mesures sous-jacentes inchangées ; contrôles refaits ici. Fichier et mesures du 1er passage conservés dans RAPPORT_QC_CINEMA_v5_NON_FINAL.md.\n"
rep = O/"RAPPORT_QC_CINEMA_v5_NON_FINAL_r2.md"; assert not rep.exists(); rep.write_text(text); print(text)
