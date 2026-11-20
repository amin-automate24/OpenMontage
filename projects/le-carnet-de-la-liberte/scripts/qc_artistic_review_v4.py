#!/usr/bin/env python3
"""QC des copies de relecture artistique v4 (lecture seule) : images, 25 ips, couverture sans trou ni doublon,
correspondance des images de bord avec le master, synchronisation audio, masters v4 inchangés. Écrit un manifeste."""
import subprocess, json, re, hashlib, sys
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parent.parent; D = R/"deliverables"; O = D/"ARTISTIC_REVIEW_v4_NON_FINAL"
MST = {k: D/f"NON_FINAL_v4/LE_CARNET_DE_LA_LIBERTE_{k}_NON_FINAL_v4_1080p.mp4" for k in ("CINEMA", "SCOLAIRE")}
REF = {"CINEMA": "f619676bad01381460f20c2970f17297eb414a42cb5ace297b717a5b7dadb92b", "SCOLAIRE": "a499cc4dc37d8ba1d2f010407f5ee783507e52a9a59c779d156292a03d626a62"}
def sh(a): return subprocess.run(a, capture_output=True)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""): h.update(c)
    return h.hexdigest()
def probe(p):
    j = json.loads(sh(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=codec_type,width,height,r_frame_rate,avg_frame_rate,nb_read_frames,duration,bit_rate:format=duration", "-of", "json", str(p)]).stdout)
    v = [s for s in j["streams"] if s["codec_type"] == "video"][0]; a = [s for s in j["streams"] if s["codec_type"] == "audio"][0]
    return v, a
def frame(p, i, scale=True):
    vf = "scale=960:540:flags=lanczos," if scale else ""
    b = sh(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{i/25:.4f}", "-i", str(p), "-frames:v", "1", "-vf", vf+"format=gray", "-f", "rawvideo", "-"]).stdout
    return np.frombuffer(b, np.uint8).astype(float)
def psnr(a, b): m = np.mean((a-b)**2); return 99.0 if m == 0 else 10*np.log10(255**2/m)
def pcm(p): return np.frombuffer(sh(["ffmpeg", "-nostdin", "-v", "error", "-i", str(p), "-vn", "-ac", "2", "-ar", "48000", "-f", "s16le", "-"]).stdout, "<i2").reshape(-1, 2).astype(float)
L = []; ok = True; rows = []
def chk(c, t):
    global ok; ok &= bool(c); L.append(("OK  " if c else "ÉCHEC ") + t)
def edge_ok(f, j, K, g):  # image j du fichier f doit être l'image globale g du master (meilleure correspondance parmi g-1..g+1)
    x = frame(f, j, scale=False); s = {d: psnr(x, frame(MST[K], g+d)) for d in (-1, 0, 1) if 0 <= g+d < 7475}
    return s[0] >= max(s.values()) - 0.5 and s[0] > 30, s[0]
for K in ("CINEMA", "SCOLAIRE"):
    full = O/f"{K}_v4_REVIEW_540p_NON_FINAL.mp4"; v, a = probe(full)
    chk(v["nb_read_frames"] == "7475" and v["r_frame_rate"] == "25/1" and v["avg_frame_rate"] == "25/1" and abs(float(a["duration"])-299) < 0.03 and (v["width"], v["height"]) == (960, 540),
        f"{full.name} : {v['nb_read_frames']} images, {v['r_frame_rate']} ips, vidéo {float(v['duration']):.3f} s / audio {float(a['duration']):.3f} s, {v['width']}×{v['height']}")
    res = [edge_ok(full, j, K, j) for j in (0, 3001, 3639, 6903, 7474)]
    chk(all(r[0] for r in res), f"{full.name} : images 0/3001/3639/6903/7474 = mêmes images du master (PSNR {', '.join(f'{r[1]:.1f}' for r in res)} dB)")
    rows.append((full.name, 0, 7474, full.stat().st_size))
    segs = sorted((O/"segments").glob(f"{K}_v4_REVIEW_540p_NON_FINAL_seg*.mp4")); nxt = 0; tot = 0; aud = []
    for s in segs:
        a0, a1 = map(int, re.search(r"_f(\d+)-(\d+)\.mp4", s.name).groups()); v, a = probe(s); n = int(v["nb_read_frames"])
        e0, e1 = edge_ok(s, 0, K, a0), edge_ok(s, n-1, K, a1)
        chk(a0 == nxt and n == a1-a0+1 and v["r_frame_rate"] == "25/1" and abs(float(a["duration"])-n/25) < 0.03 and e0[0] and e1[0],
            f"{s.name} : {n} images ({a0}-{a1}), {n/25:.2f} s, audio {float(a['duration']):.3f} s ; 1re/dernière image = master {a0}/{a1} (PSNR {e0[1]:.1f}/{e1[1]:.1f} dB)")
        nxt = a1+1; tot += n; aud.append(pcm(s)); rows.append((f"segments/{s.name}", a0, a1, s.stat().st_size))
    chk(tot == 7475 and nxt == 7475, f"{K} segments : {len(segs)} fichiers, {tot} images, couverture 0-7474 continue, sans trou ni doublon")
    cat = np.concatenate(aud); ref = pcm(MST[K]); n = min(len(cat), len(ref))
    x = ref[:480000, 0]; y = cat[:480000+4096, 0]; N = 1 << 21
    lag = int(np.argmax(np.fft.irfft(np.fft.rfft(y, N)*np.conj(np.fft.rfft(x, N)))[:4096]))
    d = cat[:n]-ref[:n]; snr = 10*np.log10(np.mean(ref[:n]**2)/np.mean(d**2))
    chk(lag == 0 and abs(len(cat)-len(ref)) <= 2048 and snr > 20, f"{K} audio des segments mis bout à bout : décalage {lag} échantillon, {len(cat)} vs {len(ref)} échantillons, RSB {snr:.1f} dB vs master (AAC 128k)")
    chk(sha(MST[K]) == REF[K], f"Master {K} v4 inchangé (SHA-256 {REF[K][:16]}…)")
for c in sorted((O/"contact_sheets").glob("*.jpg")): rows.append((f"contact_sheets/{c.name}", None, None, c.stat().st_size))
man = O/"MANIFESTE_RELECTURE_ARTISTIQUE_v4_NON_FINAL.md"; assert not man.exists()
t = "# Relecture artistique v4 — NON FINAL (19/11/2026)\n" + f"QC : {'CONFORME' if ok else 'NON CONFORME'} (mesures automatiques).\n\n| Fichier | Images master | Taille |\n|---|---|---|\n"
t += "".join(f"| {n} | {'' if a is None else f'{a}-{b}'} | {s/1e6:.2f} Mo |\n" for n, a, b, s in rows)
t += "\n## QC\n" + "\n".join(f"- {x}" for x in L) + "\n"
man.write_text(t); print(t)
