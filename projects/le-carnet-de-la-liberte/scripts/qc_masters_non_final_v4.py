#!/usr/bin/env python3
"""QC automatique des masters NON FINAL v4 (lecture seule) : format, durée, audio, couleur, étalonnage nuit, absence de
changement hors SH21-SH23, générique, sous-titres, SHA-256. Écrit un rapport concis ; refuse d'écraser."""
import subprocess, re, json, hashlib, sys
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parent.parent; D = R/"deliverables"; O = D/"NON_FINAL_v4"
V3 = {k: D/f"NON_FINAL/LE_CARNET_DE_LA_LIBERTE_{k}_NON_FINAL_v3_1080p.mp4" for k in ("CINEMA", "SCOLAIRE")}
V4 = {k: O/f"LE_CARNET_DE_LA_LIBERTE_{k}_NON_FINAL_v4_1080p.mp4" for k in ("CINEMA", "SCOLAIRE")}
SRT3 = D/"NON_FINAL/LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v3_FR.srt"; SRT4 = O/"LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v4_FR.srt"
TEST = D/"NON_FINAL_CANDIDATES/TEST_SH20-SH25_NUIT1953_v1/TEST_SH20-SH25_NUIT1953_NON_FINAL_v1.mp4"
G0, G1, N = 3001, 3639, 7475
def sh(a): return subprocess.run(a, capture_output=True, text=True)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""): h.update(c)
    return h.hexdigest()
def probe(p):
    j = json.loads(sh(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,"
          "nb_read_frames,pix_fmt,color_space,color_primaries,color_transfer,color_range,sample_rate,channels:format=duration", "-of", "json", str(p)]).stdout)
    v = [s for s in j["streams"] if s["codec_type"] == "video"][0]; a = [s for s in j["streams"] if s["codec_type"] == "audio"][0]
    return v, a, float(j["format"]["duration"])
def perframe_psnr(a, b, extra_b=""):
    """PSNR Y image par image entre a et b (pleine résolution)."""
    st = Path("/tmp")/f"psnr_{abs(hash((str(a), str(b), extra_b)))}.log"
    sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(a), "-i", str(b), "-lavfi", f"[0:v]setpts=PTS-STARTPTS[x];[1:v]{extra_b}setpts=PTS-STARTPTS[y];[x][y]psnr=stats_file={st}", "-f", "null", "-"])
    return np.array([float(m) if m != "inf" else 99.0 for m in re.findall(r"psnr_y:([\d.inf]+)", st.read_text())])
def yavg(p, t0=None, dur=None):
    a = ["ffmpeg", "-nostdin", "-hide_banner"] + (["-ss", str(t0), "-t", str(dur)] if t0 is not None else []) + ["-i", str(p), "-an", "-vf", "signalstats,metadata=mode=print:file=-", "-f", "null", "-"]
    return np.array([float(x) for x in re.findall(r"YAVG=([\d.]+)", sh(a).stdout)])
def pcm_md5(p): return sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(p), "-vn", "-f", "md5", "-"]).stdout.strip()
def ebu(p):
    e = sh(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(p), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]; tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1]; return float(I), float(tp)
L = []; ok = True
def chk(cond, txt):
    global ok; ok &= bool(cond); L.append(("OK  " if cond else "ÉCHEC ") + txt)
for k in ("CINEMA", "SCOLAIRE"):
    v, a, d = probe(V4[k])
    chk(v["nb_read_frames"] == str(N) and abs(d-299.0) < 0.001 and v["r_frame_rate"] == "25/1" and (v["width"], v["height"]) == (1920, 1080),
        f"{k} v4 : {v['nb_read_frames']} images, {d:.3f} s, {v['r_frame_rate']} ips, {v['width']}×{v['height']}, {v['codec_name']} {v['pix_fmt']}")
    chk((v["color_primaries"], v["color_transfer"], v["color_space"], v["color_range"]) == ("bt709", "bt709", "smpte170m", "tv"),
        f"{k} balisage couleur : primaires {v['color_primaries']}, transfert {v['color_transfer']}, matrice {v['color_space']}, plage {v['color_range']} (= v3)")
    m3, m4 = pcm_md5(V3[k]), pcm_md5(V4[k]); I3, tp3 = ebu(V3[k]); I4, tp4 = ebu(V4[k])
    chk(m3 == m4 and a["channels"] == 2 and a["sample_rate"] == "48000",
        f"{k} audio : AAC {a['sample_rate']} Hz stéréo ; PCM décodé identique à v3 ({'MD5 égaux' if m3 == m4 else 'MD5 DIFFÉRENTS'}) ; {I4} LUFS / crête {tp4} dBFS (v3 : {I3} / {tp3})")
    p = perframe_psnr(V3[k], V4[k]); out = np.r_[p[:G0], p[G1:]]; inn = p[G0:G1]
    chk(len(p) == N and out.min() >= 45 and np.all(p[6903:] >= 45),
        f"{k} hors SH21-SH23 ({len(out)} images) : PSNR Y vs v3 min {out.min():.1f} dB / moyen {out.mean():.1f} dB (bruit d'encodage seul) ; générique 6903-7474 min {p[6903:].min():.1f} dB")
    full = p[3014:G1]; ramp = p[G0:3015]
    chk(full.max() < 40 and np.all(np.diff(ramp) < 0.5),
        f"{k} SH21-SH23 : LUT plein 3014-3638 (PSNR vs v3 {full.min():.1f}-{full.max():.1f} dB) ; rampe 3001-3014 décroissante en PSNR ({ramp[0]:.1f} → {ramp[-1]:.1f} dB, image 3001 = poids 0)")
    if k == "CINEMA":
        y3, y4 = yavg(V3[k]), yavg(V4[k]); dd = y4 - y3
        chk(abs(dd[3000]) < 0.5 and abs(dd[3639]) < 0.5 and dd[3001] < 0.6 and dd[3014] > 5 and dd[3638] > 5,
            f"Alignement rampe (ΔY v4-v3) : 3000 {dd[3000]:+.2f} | 3001 {dd[3001]:+.2f} | 3007 {dd[3007]:+.2f} | 3014 {dd[3014]:+.2f} | 3638 {dd[3638]:+.2f} | 3639 {dd[3639]:+.2f}")
        chk(abs(y4[3639]-y4[3638]) < abs(y3[3639]-y3[3638]), f"Coupe SH23→SH24 : saut de luminance {y3[3639]-y3[3638]:+.1f} (v3) → {y4[3639]-y4[3638]:+.1f} (v4)")
        pt = perframe_psnr(TEST, V4[k], extra_b="trim=start_frame=2889:end_frame=4089,")
        chk(len(pt) == 1200 and pt.min() >= 40, f"Conformité au test SH20-SH25 approuvé (images 2889-4088) : PSNR Y min {pt.min():.1f} dB / moyen {pt.mean():.1f} dB")
    else:
        # sous-titres incrustés après étalonnage : texte identique entre v3 et v4 sur une réplique dans la plage étalonnée (image 3200, cue 16)
        crop = "crop=1920:200:0:860"
        def ymax(p, f): return float(re.findall(r"YMAX=([\d.]+)", sh(["ffmpeg", "-nostdin", "-hide_banner", "-ss", f"{f/25}", "-i", str(p), "-frames:v", "1", "-vf", f"{crop},signalstats,metadata=mode=print:file=-", "-f", "null", "-"]).stdout)[0])
        diff_sub = [ymax(V4[k], f) - ymax(V4["CINEMA"], f) for f in (3200, 3400, 3550)]
        chk(all(x > 30 for x in diff_sub) and abs(ymax(V4[k], 3200) - ymax(V3[k], 3200)) <= 3,
            f"SCOLAIRE sous-titres incrustés présents dans SH21-SH23 (images 3200/3400/3550) et non étalonnés (YMAX texte v4 {ymax(V4[k],3200):.0f} vs v3 {ymax(V3[k],3200):.0f})")
s3, s4 = sha(SRT3), sha(SRT4)
chk(s3 == s4, f"SRT CINÉMA v4 = copie octet pour octet du SRT v3 (SHA-256 {s4[:16]}…) ; SRT v3 inchangé")
v3h = {p.name: sha(p) for p in list(V3.values()) + [SRT3]}
exp = {"LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v3_1080p.mp4": "922f58a4f8853a454ba61867330d5a61d4327b87026b717b0b32ab166ab698e6",
       "LE_CARNET_DE_LA_LIBERTE_SCOLAIRE_NON_FINAL_v3_1080p.mp4": "3853e69c4acddcead36a7b1de76676ea8cd9ed2700b55b07b3aab60e6451dafd",
       "LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v3_FR.srt": "2d9b2afaa68d84ed1fc212cdd4b760a1fd04c7028464ab6b4d7fd1cc4f01c22d"}
chk(v3h == exp, "Masters v3 et SRT v3 inchangés (SHA-256 identiques aux valeurs de référence)")
sums = {p.name: sha(p) for p in sorted(O.glob("LE_CARNET_*"))}
(O/"SHA256SUMS_NON_FINAL_v4.txt").write_text("".join(f"{h}  {n}\n" for n, h in sums.items()))
rep = O/"RAPPORT_QC_NON_FINAL_v4_2026-11-19_r2.md"; assert not rep.exists(), "refus d'écraser le rapport"
rep.write_text("# Rapport QC r2 — masters NON FINAL v4 (19/11/2026) — contrôle interne, diffusion non autorisée\n"
    f"Résultat global : {'CONFORME' if ok else 'NON CONFORME'} — mesures automatiques (aucune écoute ni lecture humaine).\n"
    "Modification unique : LUT nuit 1953 sur SH21 (rampe 3001→3014) et SH22-SH23 (plein) ; SH20, SH24, SH25 et tous les autres plans inchangés.\n\n"
    + "\n".join(f"- {x}" for x in L) + "\n\n## SHA-256\n" + "".join(f"- `{h}`  {n}\n" for n, h in sums.items())
    + "\nNote : le rapport r1 signalait un faux échec (critère exigeant une forte différence dès l'image 3001, où le poids du LUT est nul par construction) ; critère corrigé, masters inchangés.\n" + "\n## Points ouverts\n- Droits SH08 (BnF/Rol 156948) : toujours EN ATTENTE (conditions Gallica non consultées).\n- Validation visuelle et auditive humaine des v4 requise. Statut : NON FINAL.\n")
print(rep.read_text())
