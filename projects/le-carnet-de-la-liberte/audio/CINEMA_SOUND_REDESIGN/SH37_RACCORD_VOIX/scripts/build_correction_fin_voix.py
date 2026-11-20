#!/usr/bin/env python3
"""SH37 — correction localisée du reste de plume de synthèse juste après la voix de Younes. Aucune réduction de bruit générale : on soustrait la composante > 2,1 kHz de LA plume connue (source AMB M7c),
avec son gain TEMPOREL mesuré (fenêtres de 50 ms, bande 4–8 kHz où la plume domine), au lieu du gain unique de la version précédente. Voix, musique, ton de pièce et vent ne sont pas touchés.
Sources existantes, 0 crédit, refuse d'écraser. Fenêtre du comparatif : 265,0–273,0 s."""
import subprocess, json, wave, re
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; B = R/"audio/CINEMA_SOUND_REDESIGN"; D = B/"SH37_RACCORD_VOIX"; SR = 48000; S0 = 265.0
rd = lambda p, ss, t, sr=SR: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(ss),"-t",str(t),"-i",str(p),"-f","f32le","-ac","2","-ar",str(sr),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def wr(p, x):
    p = Path(p); assert not p.exists(), f"refus d'écraser {p}"
    with wave.open(str(p),"wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(np.round(x*32767),-32768,32767).astype("<i2").tobytes())
def fshift(x, d): n = len(x); X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(n)[:,None]; return np.fft.irfft(X*np.exp(-2j*np.pi*f*d), n, axis=0)
def bp(x, lo, hi): X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); X[(f < lo) | (f >= hi)] = 0; return np.fft.irfft(X, len(x), axis=0)
def lowsplit(x, f1=1800.0, f2=2100.0):
    X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); h = np.where(f <= f1, 1.0, np.where(f >= f2, 0.0, np.cos((f-f1)/(f2-f1)*np.pi/2)**2)); return np.fft.irfft(X*h[:,None], len(x), axis=0)
mix = rd(R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav", S0, 10); amb = rd(R/"audio/sfx_m7c/ambience_foley_m7c.wav", S0, 10); L = len(mix); t = S0+np.arange(L)/SR
DELAY = 47.75; AS = fshift(amb, DELAY)                                    # source AMB calée (retard mesuré par fenêtres : 47,75 éch.)
# --- gain temporel de la plume dans le mix : LS par fenêtres de 50 ms (pas 25 ms) en 4–8 kHz, uniquement là où la plume existe dans la source
hm, ha = bp(mix, 4000, 8000), bp(AS, 4000, 8000); W, H = int(0.05*SR), int(0.025*SR); cs, gs = [], []
for i in range(int((267.55-S0)*SR), int((270.60-S0)*SR), H):
    x, y = ha[i:i+W], hm[i:i+W]
    if db(x) > -65.0: cs.append((i+W/2)/SR+S0); gs.append(float((x*y).sum()/(x*x).sum()))
cs, gs = np.array(cs), np.array(gs); gs = np.clip(gs, 3.5, 7.5); gsm = np.convolve(np.pad(gs, (2,2), mode="edge"), np.hanning(5)/np.hanning(5).sum(), "valid")
gt = np.interp(t, cs, gsm); AMBt = gt[:,None]*AS                                                 # contribution AMB à gain temporel
G1 = 5.397; AMB1 = G1*fshift(amb, 47.7)                                                         # version précédente (gain unique)
def curve(a0=267.45, a1=267.65, b0=270.30, b1=270.50, depth=-60.0):
    g = np.zeros(L); up = (t >= a0) & (t < a1); hold = (t >= a1) & (t <= b0); dn = (t > b0) & (t <= b1)
    g[up] = depth*np.sin((t[up]-a0)/(a1-a0)*np.pi/2)**2; g[hold] = depth; g[dn] = depth*np.cos((t[dn]-b0)/(b1-b0)*np.pi/2)**2; return 10**(g/20)
dip = curve()                                         # v1 : rampe d'entrée 267,45–267,65 s (telle que livrée)
dip2 = curve(a0=267.80, a1=267.95)                     # v2 : rampe décalée après la fin de la voix (267,62 s) : tout ce qui précède 267,80 s reste identique au bit près
# plume réelle : identique à la version C choisie
pen = rd(R/"assets/sfx/mixkit/mixkit_2369_writing_scribble_on_paper.wav", 0, 0.60, 44100).mean(1)
def stroke(rate, gain_db):
    n = len(pen); x = np.interp(np.arange(0, n-1, rate), np.arange(n), pen); m = len(x); fi, fo = int(0.02*44100), int(0.08*44100); x = x.copy(); x[:fi] *= np.sin(np.linspace(0,np.pi/2,fi))**2; x[-fo:] *= np.cos(np.linspace(0,np.pi/2,fo))**2
    return np.interp(np.arange(int(m*SR/44100))/SR*44100, np.arange(m), x)*10**(gain_db/20)
penc = np.zeros(L)
for tt, rate, gd in [(267.80, 1.00, 0.0), (268.50, 0.97, -2.0), (269.20, 1.04, -1.0), (269.85, 0.99, -4.0)]: s = stroke(rate, gd); i0 = int((tt-S0)*SR); penc[i0:i0+len(s)] += s[:L-i0]
act = np.abs(penc) > 1e-4; penc *= 10**((-42.0-20*np.log10(np.sqrt(np.mean(penc[act]**2))))/20); PEN = np.stack([penc, penc], 1)
A = mix.copy()
# C sélectif v1 (livré, non validé) : reste = mix − gain unique·AMB ; AMB_bas conservé ; AMB_haut × creux
LO1 = lowsplit(AMB1); HI1 = AMB1-LO1; C1 = (mix-AMB1) + LO1 + HI1*dip[:,None] + PEN
# C sélectif v2 (correction) : on ne soustrait que le HAUT de la plume, à gain temporel ; tout le reste du mix est laissé tel quel
HIt = AMBt-lowsplit(AMBt); C2 = mix - HIt*(1-dip2)[:,None] + PEN; C2_sp = mix - HIt*(1-dip2)[:,None]            # C2 et contrôle « sans plume réelle »
cut = lambda x: x[int((265.0-S0)*SR):int((273.0-S0)*SR)]
V = {"A": cut(A), "C1": cut(C1), "C2": cut(C2), "C2sp": cut(C2_sp)}; assert all(len(v) == 8*SR for v in V.values())
def beeps(n):
    N = int(0.12*SR); tone = np.sin(2*np.pi*1000*np.arange(N)/SR)*10**(-24/20)*np.minimum(1, np.minimum(np.arange(N), N-np.arange(N))/(0.01*SR)); seq = []
    for _ in range(n): seq += [tone, np.zeros(N)]
    y = np.concatenate(seq)[:-N]; return np.stack([y, y], 1)
sil = lambda s: np.zeros((int(round(s*SR)), 2)); parts, idx, pos = [], [], 0.0
labs = [("A", 1, "master actuel (plume de synthèse d'origine)"), ("C1", 2, "C sélectif v1 — livré, NON validé (gain unique)"), ("C2", 3, "C sélectif v2 — correction localisée (gain temporel)"), ("C2sp", 4, "contrôle : v2 SANS la plume réelle (pour isoler la cause)")]
for k, (key, nb, lab) in enumerate(labs):
    if k: parts.append(sil(1.0)); pos += 1.0
    bp_ = beeps(nb); parts += [bp_, sil(0.5)]; s_ = pos; pos += len(bp_)/SR+0.5; idx.append((key, nb, s_, pos, pos+8.0, lab)); parts.append(V[key]); pos += 8.0
full = np.concatenate(parts); (D/"audio").mkdir(exist_ok=True); wr(D/"audio/SH37_raccord_voix_comparatif_265-273.wav", full); wr(D/"audio/SH37_C2_correction_265-273.wav", V["C2"])
(D/"audio/SH37_raccord_voix_comparatif_INDEX.txt").write_text("SH37 — comparatif centré sur la fin de la voix de Younes (fin de parole ≈ 267,60 s) : fenêtre du film 265,000–273,000 s identique pour toutes les versions (8,000 s)\nContexte : 2,6 s avant la fin de la voix, 2,7 s après la fin de la plume de synthèse (270,3 s).\nRepères : 1 bip = master actuel · 2 bips = C sélectif v1 (livré, non validé) · 3 bips = C sélectif v2 (correction proposée) · 4 bips = contrôle (v2 sans la plume réelle).\n1,000 s de silence entre les versions ; 0,5 s entre les bips et la version.\n"
  + "\n".join(f"  {k} ({nb} bip{'s' if nb > 1 else ''}) bips à {s:6.3f} s · version de {a:6.3f} s à {b:6.3f} s — {lab}" for k, nb, s, a, b, lab in idx) + f"\nDurée totale : {len(full)/SR:.3f} s.\nDans chaque version, la voix de Younes finit à 2,60 s après le début de la version (267,60 s du film).\n", encoding="utf-8")
# ===== mesures =====
def flat(x, lo=2000, hi=8000, w=2400):
    o = []; m = x.mean(1)
    for i in range(0, len(m)-w+1, w):
        P = np.abs(np.fft.rfft(m[i:i+w]*np.hanning(w)))**2; f = np.fft.rfftfreq(w, 1/SR); P = P[(f >= lo) & (f < hi)]+1e-20; o.append(np.exp(np.mean(np.log(P)))/np.mean(P))
    return round(float(np.median(o)),3)
def eb(x):
    p = D/"analysis/_t.wav"; p.unlink(missing_ok=True); wr(p, x); o = subprocess.run(["ffmpeg","-nostdin","-hide_banner","-i",str(p),"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr.split("Summary:")[-1]; p.unlink()
    g = lambda k: float(re.findall(k+r":\s+(-?[\d.]+)", o)[0]); return {"I_LUFS": g("I"), "TP_dBTP": g("Peak")}
# reste de plume dans chaque version : gain LS de la plume AMB HF (4–8 kHz) par fenêtres de 100 ms, rapporté au gain de A
Ar = {}
res = {"gain_temporel_plume": {"fenêtres": int(len(cs)), "min_med_max": [round(float(gsm.min()),2), round(float(np.median(gsm)),2), round(float(gsm.max()),2)], "gain_unique_v1": G1, "débuts_268.0_268.4": [round(float(np.interp(x, cs, gsm)),2) for x in (268.0, 268.2, 268.4)]}}
rows = []
for lo in np.arange(267.9, 270.4, 0.1):
    a, b = int((lo-265.0)*SR), int((lo+0.1-265.0)*SR); h = ha[int((lo-S0)*SR):int((lo+0.1-S0)*SR)]
    if db(h) < -65: continue
    r = {"t": round(float(lo),2)}
    for n, x in V.items(): hx = bp(x, 4000, 8000)[a:b]; r[n] = round(float((hx*h).sum()/(h*h).sum()),2)
    rows.append(r)
res["gain_résiduel_de_la_plume_dans_le_rendu (A = gain réel dans le mix ; 0 = plume absente)"] = rows
for n, x in V.items():
    zone = slice(int((267.65-265.0)*SR), int((270.30-265.0)*SR)); post = slice(int((267.62-265.0)*SR), int((268.00-265.0)*SR)); zz = slice(int((268.0-265.0)*SR), int((270.3-265.0)*SR))
    r = {"HF_4-8k_par_0.5s_265→273_dBFS": [round(float(db(bp(x,4000,8000)[int(k*0.5*SR):int((k+1)*0.5*SR)])),1) for k in range(16)], "HF_2-8k_268.0-270.3_dBFS": round(float(db(bp(x,2000,8000)[zz])),1), "planéité_2-8k_268.0-270.3": flat(x[zz]), "planéité_2-8k_267.62-268.0": flat(x[post]), "crête_dBFS": round(float(20*np.log10(np.abs(x).max())),2), "écrêtés": int((np.abs(x) >= 0.9999).sum()), "perte_mono_zone_dB": round(float(db((x[zone][:,0]+x[zone][:,1])/2)-db(x[zone])),2), "RMS_zone_dBFS": round(float(db(x[zone])),1)}
    r.update(eb(x)); res[n] = r
# voix et raccords : écart C2 − A avant 267,95 s (hors plume réelle ajoutée à partir de 267,80 s) et après 270,52 s
for n in ("C1", "C2"):
    d = (V[n]-V["A"]) - (cut(PEN) if True else 0); d_pre = d[:int((267.78-265.0)*SR)]; d_post = d[int((270.52-265.0)*SR):]
    res[n]["écart_vs_A_avant_267.78_s_max (voix de Younes incluse)"] = float(np.abs(d_pre).max()); res[n]["écart_vs_A_après_270.52_s_max (vent, cahier)"] = float(np.abs(d_post).max())
    dv = d[int((267.0-265.0)*SR):int((267.78-265.0)*SR)]; res[n]["écart_vs_A_267.0–267.78_s_RMS_dBFS (fin de voix)"] = round(float(db(dv)),1)
    res[n]["bande_30-2100Hz_modifiée_hors_plume_réelle_zone_dBFS"] = round(float(db(bp(d, 30, 2100)[int((267.65-265.0)*SR):int((270.3-265.0)*SR)])),1)
def lj(x, a, b): s = x[int((a-265.0)*SR):int((b-265.0)*SR)]; return round(float(np.abs(np.diff(s, axis=0)).max()),5)
res["sauts_max_locaux"] = {zn: {n: lj(V[n], a, b) for n in V} for zn, (a, b) in {"fin de voix 267,3–267,9": (267.3, 267.9), "268,0–270,2": (268.0, 270.2), "sortie 270,25–270,70": (270.25, 270.70)}.items()}
with wave.open(str(D/"audio/SH37_raccord_voix_comparatif_265-273.wav")) as w: q = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1,2)
qs = lambda s: q[int(round(s*SR)):int(round(s*SR))+8*SR]; zmask = np.zeros(8*SR, bool); zmask[int((267.40-265)*SR):int((270.55-265)*SR)] = True
res["fichier_livré"] = {"durée_s": round(len(q)/SR,3), "16bits_différents_de_A_hors_[267.40;270.55]": {n: int((qs(idx[i][3])[~zmask] != qs(idx[0][3])[~zmask]).sum()) for i, n in enumerate(("A","C1","C2","C2sp")) if i}}
(D/"analysis/correction_fin_voix_mesures.json").write_text(json.dumps(res, indent=1, ensure_ascii=False)); 
print(json.dumps(res["gain_temporel_plume"], ensure_ascii=False)); print("gain de plume retrouvé dans chaque rendu (A = référence) :"); [print("  ", r) for r in rows]
for n in ("A","C1","C2","C2sp"): r = res[n]; print(n, "| HF4-8k 267.5→270.5:", r["HF_4-8k_par_0.5s_265→273_dBFS"][5:11], "| 2–8k zone", r["HF_2-8k_268.0-270.3_dBFS"], "| planéité 268–270,3", r["planéité_2-8k_268.0-270.3"], "| I", r["I_LUFS"], "| TP", r["TP_dBTP"], "| clip", r["écrêtés"], "| mono", r["perte_mono_zone_dB"])
for n in ("C1","C2"): print(n, {k: v for k, v in res[n].items() if k.startswith(("écart","bande"))})
print(res["sauts_max_locaux"]); print(res["fichier_livré"])
