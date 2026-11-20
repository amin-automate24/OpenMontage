#!/usr/bin/env python3
"""QC du MASTER FINAL CINÉMA (remultiplexage sans réencodage de CINÉMA v5) : format, décodage, identité des flux
(paquets + images décodées + PCM), métadonnées, SRT public, SHA-256. Écrit le rapport et les empreintes ; refuse d'écraser."""
import subprocess, re, hashlib, json, shutil
from pathlib import Path
R = Path(__file__).resolve().parent.parent; D = R/"deliverables/FINAL_CINEMA"
F = D/"LE_CARNET_DE_LA_LIBERTE_CINEMA_FINAL_1080p.mp4"; V5 = R/"deliverables/NON_FINAL_v5/LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v5_1080p.mp4"
SRT5 = R/"deliverables/NON_FINAL_v5/LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v5_FR.srt"; SRTP = D/"LE_CARNET_DE_LA_LIBERTE_FR.srt"
V5SHA = "596d4a227c8753494f503e22eb12d9b1252411bdad4744abb1963f9a9ed5505e"
def sh(a): return subprocess.run(a, capture_output=True, text=True)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""): h.update(c)
    return h.hexdigest()
L = []; ok = True
def chk(c, t):
    global ok; ok &= bool(c); L.append(("OK  " if c else "ÉCHEC ")+t)
j = json.loads(sh(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=codec_type,codec_name,profile,width,height,r_frame_rate,avg_frame_rate,nb_read_frames,start_time,duration,sample_rate,channels,color_space,color_primaries,color_transfer,color_range:format=duration:format_tags:stream_tags", "-of", "json", str(F)]).stdout)
v = [s for s in j["streams"] if s["codec_type"] == "video"][0]; a = [s for s in j["streams"] if s["codec_type"] == "audio"][0]
chk(v["nb_read_frames"] == "7475", f"Nombre d'images : {v['nb_read_frames']} (attendu 7 475)")
chk(abs(float(j["format"]["duration"])-299.0) < 0.001 and abs(float(v["duration"])-299.0) < 0.001 and abs(float(a["duration"])-299.0) < 0.001, f"Durée : conteneur {float(j['format']['duration']):.3f} s, vidéo {float(v['duration']):.3f} s, audio {float(a['duration']):.3f} s")
chk((v["width"], v["height"]) == (1920, 1080) and v["r_frame_rate"] == v["avg_frame_rate"] == "25/1", f"Résolution {v['width']}×{v['height']}, cadence {v['r_frame_rate']} constante ; H.264 {v['profile']} ; AAC {a['sample_rate']} Hz, {a['channels']} canaux")
chk((v["color_primaries"], v["color_transfer"], v["color_space"], v["color_range"]) == ("bt709", "bt709", "smpte170m", "tv"), "Balisage couleur conservé (BT.709 / matrice 170M / plage limitée) — indispensable à la lecture")
err = sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(F), "-f", "null", "-"]).stderr.strip()
chk(err == "", "Décodage complet : 0 erreur" if not err else f"Décodage : {err[:200]}")
def pk(p, s): return sh(["ffprobe", "-v", "error", "-select_streams", s, "-show_entries", "packet=pts,dts,duration,size,flags", "-of", "csv=p=0", str(p)]).stdout
def md5c(p, m): return sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(p), "-map", m, "-c", "copy", "-f", "md5", "-"]).stdout.strip()
pv5, pvf, pa5, paf = pk(V5, "v:0"), pk(F, "v:0"), pk(V5, "a:0"), pk(F, "a:0")
chk(pv5 == pvf and len(pvf.splitlines()) == 7475, f"Flux vidéo : {len(pvf.splitlines())} paquets, horodatages/tailles/drapeaux identiques à v5 ; données {md5c(F,'0:v')[4:12]}… = v5 {md5c(V5,'0:v')[4:12]}…")
chk(md5c(F, "0:v") == md5c(V5, "0:v"), "Données des paquets vidéo identiques (MD5 sur flux copié)")
chk(pa5 == paf and md5c(F, "0:a") == md5c(V5, "0:a"), f"Flux audio : {len(paf.splitlines())} paquets identiques à v5 (horodatages, tailles, données)")
fm = lambda p, m: [l.split(",")[-1].strip() for l in sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(p), "-map", m, "-f", "framemd5", "-"]).stdout.splitlines() if not l.startswith("#")]
fv5, fvf = fm(V5, "0:v"), fm(F, "0:v"); fa5, faf = fm(V5, "0:a"), fm(F, "0:a")
chk(fv5 == fvf and len(fvf) == 7475, f"Images décodées identiques à v5 : {len(fvf)} empreintes MD5 image par image égales")
chk(fa5 == faf, f"Audio décodé identique à v5 : {len(faf)} trames égales ; synchronisation inchangée (départs vidéo {v['start_time']} / audio {a['start_time']})")
tags = json.dumps({"format": j["format"].get("tags", {}), "streams": [s.get("tags", {}) for s in j["streams"]]}, ensure_ascii=False)
bad = re.compile(rb"benhida|tiddas|communautaire|gallica|agence rol|NON FINAL|diffusion non autoris|Lavf|Lavc", re.I); hits = 0
with open(F, "rb") as fh:
    prev = b""
    for c in iter(lambda: fh.read(1 << 24), b""): hits += len(bad.findall(prev[-64:]+c)); prev = c
chk(hits == 0, f"Métadonnées : seules restent `title=LE CARNET DE LA LIBERTÉ`, marque/version de conteneur, langues et noms de gestionnaires génériques ({tags}) ; 0 occurrence de nom, d'école, de BnF/Gallica/Rol, de « NON FINAL » ou de balise d'encodeur dans le fichier")
L.append("INFO Le flux H.264 conserve son message SEI technique x264 (réglages d'encodage, aucune donnée personnelle) : le retirer modifierait le flux vidéo, ce qui est exclu.")
s5 = SRT5.read_bytes(); assert not SRTP.exists(); shutil.copyfile(SRT5, SRTP)
t = s5.decode("utf-8"); cues = re.findall(r"(\d\d):(\d\d):(\d\d),(\d+) --> (\d\d):(\d\d):(\d\d),(\d+)", t); end = max(int(c[4])*3600+int(c[5])*60+int(c[6])+int(c[7])/1000 for c in cues)
chk(SRTP.read_bytes() == s5 and not s5.startswith(b"\xef\xbb\xbf") and len(cues) == 32 and end <= 299.0 and not re.search(r"benhida|tiddas|communautaire", t, re.I),
    f"SRT public `LE_CARNET_DE_LA_LIBERTE_FR.srt` = copie octet pour octet du SRT v5 ; UTF-8 sans BOM, 32 répliques, fin {end:.3f} s ≤ 299 s ; aucun nom de personne réelle ni d'établissement")
chk(sha(V5) == V5SHA, "CINÉMA v5 NON FINAL inchangé (SHA-256 vérifié après opérations)")
sf, ssrt = sha(F), sha(SRTP); size = F.stat().st_size
(D/"SHA256SUMS_CINEMA_FINAL.txt").write_text(f"{sf}  {F.name}\n{ssrt}  {SRTP.name}\n")
rep = D/"RAPPORT_QC_CINEMA_FINAL.md"; assert not rep.exists()
rep.write_text(f"# Rapport QC — MASTER FINAL CINÉMA (20/11/2026)\nVerdict : {'CONFORME' if ok else 'NON CONFORME'} (mesures automatiques).\n"
  f"Fichier : `{F}` — {size} octets — SHA-256 `{sf}`\nSource : CINÉMA v5 NON FINAL, SHA-256 `{V5SHA}` (vérifié avant et après) ; remultiplexage `ffmpeg -c copy` sans réencodage, métadonnées nettoyées.\n\n"
  + "\n".join("- "+x for x in L) + f"\n\nSRT public : `{SRTP.name}` — SHA-256 `{ssrt}`.\n")
print(rep.read_text())
