#!/usr/bin/env python3
"""Comparatif SH37 (fenêtre 267–273 s, identique pour A/B/C) — sources existantes, 0 crédit, aucun fichier existant modifié ; refuse d'écraser.
Base sans perte = mix QC2_SON2. Décomposition mesurée : mix = reste + g·AMB(retard fractionnaire), g et retard estimés sur la bande 4–8 kHz (267,7–270,3 s).
A = mix inchangé ; B = AMB −20 dB (267,45→270,65 s, rampes cosinus 0,2 s / 0,3 s) ; C = AMB −60 dB sur la même zone + plume réelle Mixkit 2369 (4 gestes, niveau discret)."""
import subprocess, json, wave
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; D = R/"audio/CINEMA_SOUND_REDESIGN/SH37_VALIDATION"; SR = 48000; S0 = 265.0
rd = lambda p, ss, t, sr=SR: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(ss),"-t",str(t),"-i",str(p),"-f","f32le","-ac","2","-ar",str(sr),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def wr(p, x):
    p = Path(p); assert not p.exists(), f"refus d'écraser {p}"
    with wave.open(str(p),"wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(np.round(x*32767),-32768,32767).astype("<i2").tobytes())
def fshift(x, d): n = len(x); X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(n)[:,None]; return np.fft.irfft(X*np.exp(-2j*np.pi*f*d), n, axis=0)
def bp(x, lo, hi): X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); X[(f < lo) | (f >= hi)] = 0; return np.fft.irfft(X, len(x), axis=0)
mix = rd(R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav", S0, 10); amb = rd(R/"audio/sfx_m7c/ambience_foley_m7c.wav", S0, 10); L = len(mix); t = S0+np.arange(L)/SR
a, b = int((267.7-S0)*SR), int((270.3-S0)*SR); hm = bp(mix, 4000, 8000)[a:b]
best = min(((db(hm-(g:=float((hm*(ha:=bp(fshift(amb,d),4000,8000)[a:b])).sum()/(ha*ha).sum()))*ha)-db(hm), d, g) for d in np.arange(46.0, 50.01, 0.1)))
_, DELAY, G = best; AMBs = G*fshift(amb, DELAY); REST = mix-AMBs
def ramp_curve(depth_db):
    g = np.zeros(L); up = (t >= 267.45) & (t < 267.65); hold = (t >= 267.65) & (t <= 270.35); dn = (t > 270.35) & (t <= 270.65)
    g[up] = depth_db*np.sin((t[up]-267.45)/0.2*np.pi/2)**2; g[hold] = depth_db; g[dn] = depth_db*np.cos((t[dn]-270.35)/0.3*np.pi/2)**2; return 10**(g/20)
A = mix.copy(); Bv = REST + AMBs*ramp_curve(-20.0)[:,None]; Cbase = REST + AMBs*ramp_curve(-60.0)[:,None]
# plume réelle Mixkit 2369 : 4 gestes (la source ne dure que 1,19 s, dont 0,55 s actives), positions et vitesses légèrement différentes
pen = rd(R/"assets/sfx/mixkit/mixkit_2369_writing_scribble_on_paper.wav", 0, 0.60, 44100).mean(1)   # lu à 44,1 kHz (fréquence native)
def stroke(rate, gain_db):
    n = len(pen); x = np.interp(np.arange(0, n-1, rate), np.arange(n), pen)                  # rééchantillonnage (vitesse/hauteur ±5 %)
    m = len(x); fi, fo = int(0.02*44100), int(0.08*44100); x = x.copy(); x[:fi] *= np.sin(np.linspace(0,np.pi/2,fi))**2; x[-fo:] *= np.cos(np.linspace(0,np.pi/2,fo))**2
    x48 = np.interp(np.arange(int(m*SR/44100))/SR*44100, np.arange(m), x); return x48*10**(gain_db/20)
STROKES = [(267.80, 1.00, 0.0), (268.50, 0.97, -2.0), (269.20, 1.04, -1.0), (269.85, 0.99, -4.0)]
penc = np.zeros(L)
for tt, rate, gd in STROKES: s = stroke(rate, gd); i0 = int((tt-S0)*SR); penc[i0:i0+len(s)] += s[:L-i0]
act = np.abs(penc) > 1e-4; TARGET = -42.0                                                    # RMS visé sur les parties actives (dBFS) : plume discrète, ≈ 23 dB sous la musique (~−19 dBFS RMS)
penc *= 10**((TARGET-20*np.log10(np.sqrt(np.mean(penc[act]**2))))/20)
Cv = Cbase + np.stack([penc, penc], 1)
cut = lambda x: x[int((267.0-S0)*SR):int((273.0-S0)*SR)]
W = {"A": cut(A), "B": cut(Bv), "C": cut(Cv)}; assert all(len(v) == 6*SR for v in W.values())
def beeps(n):
    tone = lambda: (np.sin(2*np.pi*1000*np.arange(int(0.12*SR))/SR)*10**(-24/20)*np.minimum(1, np.minimum(np.arange(int(0.12*SR)), int(0.12*SR)-np.arange(int(0.12*SR)))/(0.01*SR)))
    seq = []; [seq.extend([tone(), np.zeros(int(0.12*SR))]) for _ in range(n)]; y = np.concatenate(seq)[:-int(0.12*SR)]; return np.stack([y, y], 1)
sil = lambda s: np.zeros((int(round(s*SR)), 2)); parts, idx, pos = [], [], 0.0
for k, (name, nb) in enumerate([("A", 1), ("B", 2), ("C", 3)]):
    if k: parts.append(sil(1.0)); pos += 1.0
    bp_ = beeps(nb); parts += [bp_, sil(0.5)]; start_b = pos; pos += len(bp_)/SR+0.5; idx.append((name, nb, start_b, pos, pos+6.0)); parts.append(W[name]); pos += 6.0
full = np.concatenate(parts); wr(D/"audio/SH37_comparatif_A_B_C_267-273.wav", full)
(D/"audio/SH37_comparatif_INDEX.txt").write_text("SH37 — comparatif A / B / C, fenêtre du film 267,000–273,000 s (identique pour les trois), 6,000 s chacune\n"
  "Repères : A = 1 bip, B = 2 bips, C = 3 bips (1 kHz, 0,12 s, −24 dBFS), puis 0,5 s de silence, puis la version ; 1,000 s de silence entre la fin d'une version et les bips de la suivante.\n"
  + "\n".join(f"  {n} : bips à {s:6.3f} s ({nb} bip{'s' if nb > 1 else ''}) · version de {a_:6.3f} s à {b_:6.3f} s" for n, nb, s, a_, b_ in idx)
  + f"\nDurée totale : {len(full)/SR:.3f} s.\n"
  "A : bruitage synthétique original (mix du master, inchangé) · B : bruitage atténué de −20 dB (267,45–270,65 s) · C : bruitage synthétique retiré (−60 dB) + plume réelle Mixkit 2369 (4 gestes), niveau discret.\nÀ écouter : le crépitement, la naturalité de la plume, l'équilibre avec la musique.\n", encoding="utf-8")
# ===== mesures =====
def lufs(x):
    p = D/"analysis/_t.wav"; p.unlink(missing_ok=True); wr(p, x); o = subprocess.run(["ffmpeg","-nostdin","-hide_banner","-i",str(p),"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr.split("Summary:")[-1]; p.unlink()
    g = lambda k: float(__import__("re").findall(k+r":\s+(-?[\d.]+)", o)[0]); return {"I_LUFS": g("I"), "TP_dBTP": g("Peak")}
res = {"décomposition": {"retard_éch": round(float(DELAY),2), "gain_AMB_dB": round(20*np.log10(G),2), "réduction_HF_4-8k_en_retirant_AMB_dB": round(float(db(bp(REST,4000,8000)[a:b])-db(bp(mix,4000,8000)[a:b])),1)}, "plume_réelle": {"gestes": STROKES, "RMS_actif_dBFS": TARGET, "crête_dBFS": round(float(20*np.log10(np.abs(penc).max())),1), "énergie_4-8k_dBFS_sur_267.7-270.3": round(float(db(bp(np.stack([penc,penc],1),4000,8000)[a:b])),1)}}
zone = slice(int((267.45-267.0)*SR), int((270.65-267.0)*SR)); out = np.ones(6*SR, bool); out[zone] = False
for n, x in W.items():
    h = bp(x, 4000, 8000); r = {"HF_4-8k_par_0.5s_dBFS": [round(float(db(h[int(k*0.5*SR):int((k+1)*0.5*SR)])),1) for k in range(12)], "RMS_267.7-270.3_dBFS": round(float(db(x[int(0.7*SR):int(3.3*SR)])),1),
         "crête_échantillon_dBFS": round(float(20*np.log10(np.abs(x).max())),2), "écrêtés": int((np.abs(x) >= 0.9999).sum()), "perte_mono_zone_dB": round(float(db((x[zone][:,0]+x[zone][:,1])/2)-db(x[zone])),2)}
    r.update(lufs(x))
    if n != "A":
        d = x-W["A"]; r["écart_max_vs_A_hors_zone"] = float(np.abs(d[out]).max()); r["écart_RMS_vs_A_dans_zone_dBFS"] = round(float(db(d[zone])),1)
        r["énergie_de_la_différence_par_bande_dBFS"] = {f"{lo}-{hi}": round(float(db(bp(d, lo, hi)[zone])),1) for lo, hi in [(50,1000),(1000,2000),(2000,4000),(4000,8000)]}
        r["musique_50-2000Hz_RMS_zone_dBFS (A: {:.1f})".format(float(db(bp(W["A"],50,2000)[zone])))] = round(float(db(bp(x,50,2000)[zone])),1)
    res[n] = r
# contrôle sur le fichier livré : échantillons 16 bits identiques à A hors de la zone modifiée, pour B et C
import wave as _w
with _w.open(str(D/"audio/SH37_comparatif_A_B_C_267-273.wav")) as w: q = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1,2)
seg = lambda s: q[int(round(s*SR)):int(round(s*SR))+6*SR]
res["fichier_livré_échantillons_différents_de_A_hors_zone_267.45-270.65"] = {n: int((seg(st)[out] != seg(0.62)[out]).sum()) for n, st in (("B", 8.48), ("C", 16.58))}
res["fichier_livré_durée_s"] = round(len(q)/SR, 3)
(D/"analysis/sh37_mesures.json").write_text(json.dumps(res, indent=1, ensure_ascii=False)); print(json.dumps(res, indent=1, ensure_ascii=False)); print((D/"audio/SH37_comparatif_INDEX.txt").read_text())
