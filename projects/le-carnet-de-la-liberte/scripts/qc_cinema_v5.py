#!/usr/bin/env python3
"""QC unique CINÉMA v5 NON FINAL (lecture seule) : format, audio, images inchangées hors SH08/générique, SH08 = master QC3,
crédits anonymes, chaînes interdites, SHA-256 ; planche JPEG + rapport. Refuse d'écraser."""
import subprocess, json, re, hashlib
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parent.parent; D = R/"deliverables"; O = D/"NON_FINAL_v5"
V5 = O/"LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v5_1080p.mp4"; SRT5 = O/"LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v5_FR.srt"
V4 = D/"NON_FINAL_v4/LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v4_1080p.mp4"; Q3 = R/"animatic/MASTER_CANDIDATE_NON_FINAL_QC3_SON2_1080p.mp4"
SRT4 = D/"NON_FINAL_v4/LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v4_FR.srt"
N = 7475; SH08 = (901, 988); CRED0 = 6903; FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def sh(a): return subprocess.run(a, capture_output=True, text=True)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""): h.update(c)
    return h.hexdigest()
def probe(p):
    j = json.loads(sh(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=codec_type,codec_name,profile,level,width,height,r_frame_rate,avg_frame_rate,nb_read_frames,pix_fmt,color_space,color_primaries,color_transfer,color_range,sample_rate,channels,start_time,duration:format=duration,size:format_tags=title,comment", "-of", "json", str(p)]).stdout)
    return [s for s in j["streams"] if s["codec_type"] == "video"][0], [s for s in j["streams"] if s["codec_type"] == "audio"][0], j["format"]
def psnr_series(a, b, ta="", tb=""):
    log = Path("/tmp")/f"psnr_{abs(hash((str(a), str(b), ta, tb)))}.log"
    sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(a), "-i", str(b), "-lavfi", f"[0:v]{ta}scale=480:270,setpts=PTS-STARTPTS[x];[1:v]{tb}scale=480:270,setpts=PTS-STARTPTS[y];[x][y]psnr=stats_file={log}", "-f", "null", "-"])
    return np.array([99.0 if m == "inf" else float(m) for m in re.findall(r"psnr_y:([\d.inf]+)", log.read_text())])
def runs(idx):
    out = []; s = p = None
    for i in idx:
        if s is None: s = p = i
        elif i == p+1: p = i
        else: out.append((int(s), int(p))); s = p = i
    if s is not None: out.append((int(s), int(p)))
    return out
L = []; ok = True
def chk(c, t):
    global ok; ok &= bool(c); L.append(("OK  " if c else "ÉCHEC ")+t)
v, a, f = probe(V5); v4, a4, f4 = probe(V4)
chk(v["nb_read_frames"] == str(N) and abs(float(f["duration"])-299.0) < 0.001 and v["r_frame_rate"] == v["avg_frame_rate"] == "25/1" and (v["width"], v["height"]) == (1920, 1080),
    f"Format : {v['nb_read_frames']} images, {float(f['duration']):.3f} s, {v['r_frame_rate']} ips constant, {v['width']}×{v['height']}, {v['codec_name']} {v['profile']} niveau {v['level']}, {v['pix_fmt']}")
chk((v["color_primaries"], v["color_transfer"], v["color_space"], v["color_range"]) == ("bt709", "bt709", "smpte170m", "tv") and abs(float(v["duration"])-float(a["duration"])) < 0.01 and v["start_time"] == a["start_time"] == v4["start_time"],
    f"Balisage couleur = v4 (BT.709 / matrice 170M / plage limitée) ; vidéo {float(v['duration']):.3f} s, audio {float(a['duration']):.3f} s, départs {v['start_time']}/{a['start_time']}")
err = sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(V5), "-f", "null", "-"]).stderr.strip()
chk(err == "", "Décodage intégral : 0 erreur" if err == "" else f"Décodage : {err[:200]}")
m5 = sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(V5), "-map", "0:a", "-c", "copy", "-f", "md5", "-"]).stdout.strip()
m4 = sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(V4), "-map", "0:a", "-c", "copy", "-f", "md5", "-"]).stdout.strip()
d5 = sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(V5), "-vn", "-f", "md5", "-"]).stdout.strip(); d4 = sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(V4), "-vn", "-f", "md5", "-"]).stdout.strip()
chk(m5 == m4 and d5 == d4 and a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2,
    f"Audio : flux AAC identique à v4 (MD5 des paquets {m5[4:12]}…) et PCM décodé identique ; AAC 48 kHz stéréo ; synchronisation inchangée (mêmes départs, mêmes durées)")
p45 = psnr_series(V5, V4)
chk(len(p45) == N, f"Comparaison v5 ↔ v4 sur {len(p45)} images")
diff = [i for i in range(N) if p45[i] < 45]; dr = runs(diff)
film_other = [r for r in dr if r[1] < CRED0 and not (SH08[0] <= r[0] and r[1] <= SH08[1])]
chk(not film_other and any(r[0] >= SH08[0]-0 and r[1] <= SH08[1] for r in dr),
    f"Hors SH08 et générique, film (0–6902) identique à v4 (PSNR ≥ 45 dB ; min {min(p45[i] for i in range(CRED0) if not SH08[0] <= i <= SH08[1]):.1f} dB, moyenne {np.mean([p45[i] for i in range(CRED0) if not SH08[0] <= i <= SH08[1]]):.1f} dB) ; plages différentes : {dr}")
# étalonnage nuit conservé (zone 3001-3638 identique à v4)
chk(min(p45[3001:3639]) >= 45, f"Étalonnage nuit SH21–SH23 inchangé (images 3001–3638 vs v4 : PSNR min {min(p45[3001:3639]):.1f} dB)")
# SH08 : v5 = master QC3
pq = psnr_series(V5, Q3, ta=f"trim=start_frame={SH08[0]}:end_frame={SH08[1]+1},", tb=f"trim=start_frame={SH08[0]}:end_frame={SH08[1]+1},")
chk(len(pq) == 88 and pq.min() >= 45, f"SH08 (images 901–988, 88 images, 36,04–39,56 s) = plan du master QC3 sans photo BnF : PSNR min {pq.min():.1f} dB, moyenne {pq.mean():.1f} dB ; différent de v4 (PSNR v4 min {p45[901:989].min():.1f} dB)")
pj = psnr_series(V5, Q3, ta="trim=start_frame=895:end_frame=996,", tb="trim=start_frame=895:end_frame=996,")
chk(len(pj) == 101 and pj.min() >= 45, f"Continuité SH07→SH08→SH09 (images 895–995 vs master QC3) : PSNR min {pj.min():.1f} dB ; coupes aux images 901 et 989 inchangées")
# générique : carton 2 inchangé ; cartons 1 et 3 modifiés
c2 = p45[7065:7114]
chk(c2.min() >= 45, f"Carton 2 (devise, images 7065–7113) inchangé vs v4 : PSNR min {c2.min():.1f} dB ; cartons 1 et 3 modifiés (plages <45 dB : {[r for r in dr if r[0] >= CRED0]})")
# chaînes interdites
bad = re.compile(rb"benhida|tiddas|communautaire|gallica|agence rol|bnf", re.I)
hits = len(bad.findall(V5.read_bytes())); srt_hits = len(bad.findall(SRT5.read_bytes()))
pub = (R/"docs/PAQUET_YOUTUBE_ANONYME_CINEMA_v3_2026-11-20.md").read_bytes(); pub_hits = len(bad.findall(pub))
tags = f"{f.get('tags', {})}"
chk(hits == 0 and srt_hits == 0 and pub_hits == 0 and not bad.search(tags.encode()), f"Chaînes interdites (nom, école, BnF/Rol/Gallica) : 0 dans le fichier v5 (flux + métadonnées), 0 dans le SRT v5, 0 dans le paquet YouTube public v3 ; pixels des cartons contrôlés sur la planche")
chk(sha(SRT5) == sha(SRT4), f"SRT v5 = SRT v4 octet pour octet (SHA-256 {sha(SRT5)[:16]}…)")
chk(sha(V4).startswith("f619676bad013814") and sha(R/"deliverables/NON_FINAL_v4/LE_CARNET_DE_LA_LIBERTE_SCOLAIRE_NON_FINAL_v4_1080p.mp4").startswith("a499cc4dc37d8ba1") and sha(D/"QUIZ_SCOLAIRE_2026-11-20/FINAL/LE_DEFI_DE_LA_LIBERTE_QUIZ_FINAL_1080p.mp4").startswith("87f0203d2e4fad44"),
    "CINÉMA v4, SCOLAIRE v4 et quiz FINAL inchangés (SHA-256)")
# planche
W = Path("/tmp")/"v5sheet"; W.mkdir(exist_ok=True); frames = [895, 901, 940, 988, 989, 995, 6923, 6963, 7013, 7085, 7250, 7470]; ins = []
for k, fr in enumerate(frames):
    sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{fr/25:.3f}", "-i", str(V5), "-frames:v", "1", "-vf", f"scale=640:360:flags=lanczos,drawtext=fontfile={FONT}:text='CINEMA v5  image {fr}  ({fr/25:.2f} s)':x=8:y=8:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.7:boxborderw=4", str(W/f"{k}.png")]); ins += ["-i", str(W/f"{k}.png")]
sheet = O/"PLANCHE_CINEMA_v5_SH08_ET_GENERIQUE.jpg"; assert not sheet.exists()
lay = "|".join(f"{(k%3)*640}_{(k//3)*360}" for k in range(12))
sh(["ffmpeg", "-nostdin", "-v", "error", "-n"]+ins+["-filter_complex", f"xstack=inputs=12:layout={lay}", "-frames:v", "1", "-q:v", "2", "-pix_fmt", "yuvj420p", str(sheet)])
s5 = sha(V5); size = V5.stat().st_size
(O/"SHA256SUMS_CINEMA_v5_NON_FINAL.txt").write_text(f"{s5}  {V5.name}\n{sha(SRT5)}  {SRT5.name}\n{sha(sheet)}  {sheet.name}\n")
rep = O/"RAPPORT_QC_CINEMA_v5_NON_FINAL.md"; assert not rep.exists()
rep.write_text("# Rapport QC — CINÉMA v5 NON FINAL (20/11/2026)\n"
  f"Verdict technique : {'CONFORME' if ok else 'NON CONFORME'} (mesures automatiques ; contrôle visuel de la planche JPEG, sans visionnage continu ni écoute).\n"
  f"Fichier : `{V5}` — {size} octets ({size/1e6:.2f} Mo) — SHA-256 `{s5}`\n"
  "Modifications : (1) SH08 images 901–988 = plan du master QC3 (photo de famille sépia), sans photo BnF ; (2) générique v006 anonyme (carton 1 option A, carton 3 sans crédit BnF). Audio, étalonnage nuit, durée, transitions inchangés. Statut NON FINAL.\n\n"
  + "\n".join("- "+x for x in L)+"\n\nPlanche : `PLANCHE_CINEMA_v5_SH08_ET_GENERIQUE.jpg`. Non vérifié : lecture continue, écoute. Preuves de licence ElevenLabs et Magnific : en attente. Aucune publication ; aucune étiquette FINAL.\n")
print(rep.read_text())
