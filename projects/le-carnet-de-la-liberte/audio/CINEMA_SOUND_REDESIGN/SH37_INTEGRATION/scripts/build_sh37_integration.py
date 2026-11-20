#!/usr/bin/env python3
"""SH37 — intégration de la version C (plume réelle Mixkit 2369) avec correction SÉLECTIVE de l'ambiance. Fenêtre de test 265–275 s. 0 crédit ; refuse d'écraser.
Base sans perte = mix QC2_SON2 ; mix = reste + g·AMB (retard 47,7 éch., gain +14,6 dB, mesurés). Correction sélective : seule la bande > 2,1 kHz de la contribution AMB est atténuée
(crossover complémentaire 1,8–2,1 kHz : AMB = AMB_bas + AMB_haut, somme exacte), de −60 dB entre 267,45 et 270,50 s (rampes cosinus 0,2 s), donc le ton de pièce et le vent restent intacts.
Plume réelle : identique à la version C choisie (4 gestes, RMS actif −42 dBFS). Produit : C sélectif seul + comparatif (master / C global choisi / C sélectif)."""
import subprocess, json, wave, re
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; D = R/"audio/CINEMA_SOUND_REDESIGN/SH37_INTEGRATION"; SR = 48000; S0 = 265.0
rd = lambda p, ss, t, sr=SR: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(ss),"-t",str(t),"-i",str(p),"-f","f32le","-ac","2","-ar",str(sr),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def wr(p, x):
    p = Path(p); assert not p.exists(), f"refus d'écraser {p}"
    with wave.open(str(p),"wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(np.round(x*32767),-32768,32767).astype("<i2").tobytes())
def fshift(x, d): n = len(x); X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(n)[:,None]; return np.fft.irfft(X*np.exp(-2j*np.pi*f*d), n, axis=0)
def bp(x, lo, hi): X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); X[(f < lo) | (f >= hi)] = 0; return np.fft.irfft(X, len(x), axis=0)
def lowsplit(x, f1=1800.0, f2=2100.0):                                  # passe-bas à transition cosinus ; haut = x − bas (somme exacte)
    X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); h = np.where(f <= f1, 1.0, np.where(f >= f2, 0.0, np.cos((f-f1)/(f2-f1)*np.pi/2)**2)); return np.fft.irfft(X*h[:,None], len(x), axis=0)
mix = rd(R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav", S0, 10); amb = rd(R/"audio/sfx_m7c/ambience_foley_m7c.wav", S0, 10); L = len(mix); t = S0+np.arange(L)/SR
DELAY, G = 47.7, 5.397                                                  # mesurés (étude SH37_VALIDATION)
AMBs = G*fshift(amb, DELAY); REST = mix-AMBs; LO = lowsplit(AMBs); HI = AMBs-LO
def curve(depth_db, a0, a1, b0, b1):
    g = np.zeros(L); up = (t >= a0) & (t < a1); hold = (t >= a1) & (t <= b0); dn = (t > b0) & (t <= b1)
    g[up] = depth_db*np.sin((t[up]-a0)/(a1-a0)*np.pi/2)**2; g[hold] = depth_db; g[dn] = depth_db*np.cos((t[dn]-b0)/(b1-b0)*np.pi/2)**2; return 10**(g/20)
# plume réelle : identique à la version C approuvée
pen = rd(R/"assets/sfx/mixkit/mixkit_2369_writing_scribble_on_paper.wav", 0, 0.60, 44100).mean(1)
def stroke(rate, gain_db):
    n = len(pen); x = np.interp(np.arange(0, n-1, rate), np.arange(n), pen); m = len(x); fi, fo = int(0.02*44100), int(0.08*44100); x = x.copy(); x[:fi] *= np.sin(np.linspace(0,np.pi/2,fi))**2; x[-fo:] *= np.cos(np.linspace(0,np.pi/2,fo))**2
    return np.interp(np.arange(int(m*SR/44100))/SR*44100, np.arange(m), x)*10**(gain_db/20)
STROKES = [(267.80, 1.00, 0.0), (268.50, 0.97, -2.0), (269.20, 1.04, -1.0), (269.85, 0.99, -4.0)]; penc = np.zeros(L)
for tt, rate, gd in STROKES: s = stroke(rate, gd); i0 = int((tt-S0)*SR); penc[i0:i0+len(s)] += s[:L-i0]
act = np.abs(penc) > 1e-4; PEN_SCALE = 10**((-42.0-20*np.log10(np.sqrt(np.mean(penc[act]**2))))/20); penc *= PEN_SCALE; PEN = np.stack([penc, penc], 1)
A = mix.copy()
Cg = REST + AMBs*curve(-60.0, 267.45, 267.65, 270.35, 270.65)[:,None] + PEN                     # version C approuvée (atténuation globale du bus AMB)
Cs = REST + LO + HI*curve(-60.0, 267.45, 267.65, 270.30, 270.50)[:,None] + PEN                 # version C avec correction sélective (> 2,1 kHz)
cut = lambda x: x[int((265.0-S0)*SR):int((275.0-S0)*SR)]
W = {"A": cut(A), "Cg": cut(Cg), "Cs": cut(Cs)}; assert all(len(v) == 10*SR for v in W.values())
wr(D/"audio/SH37_C_selectif_265-275.wav", W["Cs"])
def beeps(n):
    N = int(0.12*SR); tone = np.sin(2*np.pi*1000*np.arange(N)/SR)*10**(-24/20)*np.minimum(1, np.minimum(np.arange(N), N-np.arange(N))/(0.01*SR)); seq = []
    for _ in range(n): seq += [tone, np.zeros(N)]
    y = np.concatenate(seq)[:-N]; return np.stack([y, y], 1)
sil = lambda s: np.zeros((int(round(s*SR)), 2)); parts, idx, pos = [], [], 0.0
for k, (key, nb, lab) in enumerate([("A", 1, "master actuel (bruitage de synthèse)"), ("Cg", 2, "version C approuvée (atténuation globale AMB + plume réelle)"), ("Cs", 3, "version C sélective (atténuation > 2,1 kHz seulement + plume réelle)")]):
    if k: parts.append(sil(1.0)); pos += 1.0
    bp_ = beeps(nb); parts += [bp_, sil(0.5)]; s_ = pos; pos += len(bp_)/SR+0.5; idx.append((key, nb, s_, pos, pos+10.0, lab)); parts.append(W[key]); pos += 10.0
full = np.concatenate(parts); wr(D/"audio/SH37_comparatif_integration_265-275.wav", full)
(D/"audio/SH37_comparatif_integration_INDEX.txt").write_text("SH37 — comparatif d'intégration, fenêtre du film 265,000–275,000 s (identique pour les trois), 10,000 s chacune\n1 bip = master actuel · 2 bips = version C approuvée (atténuation globale) · 3 bips = version C sélective (proposée pour l'intégration)\n1,000 s de silence entre les versions ; 0,5 s de silence entre les bips et la version.\n"
  + "\n".join(f"  {k} ({nb} bip{'s' if nb > 1 else ''}) bips à {s:6.3f} s · version de {a:6.3f} s à {b:6.3f} s — {lab}" for k, nb, s, a, b, lab in idx) + f"\nDurée totale : {len(full)/SR:.3f} s.\n", encoding="utf-8")
# ===== mesures =====
def eb(x):
    p = D/"analysis/_t.wav"; p.unlink(missing_ok=True); wr(p, x); o = subprocess.run(["ffmpeg","-nostdin","-hide_banner","-i",str(p),"-af","ebur128=peak=true:metadata=1,ametadata=mode=print:file=-","-f","null","-"],capture_output=True,text=True); p.unlink()
    S = [float(v) for v in re.findall(r"r128\.S=(-?[\d.]+)", o.stdout)]; sm = o.stderr.split("Summary:")[-1]; g = lambda k: float(re.findall(k+r":\s+(-?[\d.]+)", sm)[0]); return {"I_LUFS": g("I"), "LRA_LU": g("LRA"), "TP_dBTP": g("Peak"), "court_terme_max_LUFS": round(max(S),1)}
zoneS = slice(int((267.65-265.0)*SR), int((270.30-265.0)*SR)); res = {"crossover_Hz": [1800, 2100], "HF_dip_dB": -60, "plume": {"gain_net_dB_source": round(20*np.log10(PEN_SCALE),1), "RMS_actif_dBFS": -42.0, "crête_dBFS": round(float(20*np.log10(np.abs(penc).max())),1), "gestes": STROKES}}
for n, x in W.items():
    r = {"HF_4-8k_par_0.5s_dBFS": [round(float(db(bp(x,4000,8000)[int(k*0.5*SR):int((k+1)*0.5*SR)])),1) for k in range(20)], "HF_2.1-8k_par_0.5s_dBFS": [round(float(db(bp(x,2100,8000)[int(k*0.5*SR):int((k+1)*0.5*SR)])),1) for k in range(20)], "crête_échantillon_dBFS": round(float(20*np.log10(np.abs(x).max())),2), "écrêtés": int((np.abs(x) >= 0.9999).sum()),
         "perte_mono_dB_zone": round(float(db((x[zoneS][:,0]+x[zoneS][:,1])/2)-db(x[zoneS])),2), "RMS_zone_dBFS": round(float(db(x[zoneS])),1), "bande_30-2100Hz_zone_dBFS": round(float(db(bp(x,30,2100)[zoneS])),1)}
    r.update(eb(x)); res[n] = r
# préservation du fond : AMB bas (30–2100 Hz) pendant la zone et du vent après 270,5 s ; différence version − A
for n, X in (("Cg", Cg), ("Cs", Cs)):
    d = cut(X)-W["A"]; pen_c = cut(PEN); dd = d-pen_c                  # on retire la plume réelle ajoutée pour isoler l'effet sur le fond
    res[n]["fond_modifié_30-2100Hz_dBFS_zone (A: {:.1f})".format(float(db(bp(cut(AMBs),30,2100)[zoneS])))] = round(float(db(bp(dd,30,2100)[zoneS])),1)
    res[n]["écart_fond_après_270.52_s_max"] = float(np.abs(dd[int((270.52-265.0)*SR):]).max())
    res[n]["écart_avant_267.4_s_max (voix Y5, musique…)"] = float(np.abs(dd[:int((267.4-265.0)*SR)]).max())
    # raccords : plus grand saut d'échantillon (dérivée) de dd autour des bornes + niveau par 100 ms
    ev = {}
    for nm, c in (("entrée_267.45-267.65", 267.55), ("sortie", 270.40 if n == "Cg" else 270.40)):
        s = dd[int((c-0.25-265.0)*SR):int((c+0.25-265.0)*SR)]; ev[nm] = {"saut_max_échantillon": round(float(np.abs(np.diff(s,axis=0)).max()),6), "RMS_100ms_dBFS": [round(float(db(s[k*4800:(k+1)*4800])),1) for k in range(5)]}
    res[n]["raccords_différence_vs_A"] = ev
def localjump(x, a, b): s = x[int((a-265.0)*SR):int((b-265.0)*SR)]; d = np.abs(np.diff(s, axis=0)); return round(float(d.max()),5)
res["raccords_saut_max_|Δéchantillon|_locaux (un clic ferait ressortir cette valeur au-dessus du master)"] = {zn: {n: localjump(W[n], a, b) for n in ("A","Cg","Cs")} for zn, (a, b) in {"entrée 267,35–267,80": (267.35, 267.80), "pendant 268,0–270,2": (268.0, 270.2), "sortie 270,25–270,70": (270.25, 270.70), "avant 266,0–267,3": (266.0, 267.3), "après 270,7–273,0": (270.7, 273.0)}.items()}
res["A_saut_max_échantillon_265-275"] = round(float(np.abs(np.diff(W["A"],axis=0)).max()),5)
for n in ("Cg","Cs"): res[n]["saut_max_échantillon_265-275"] = round(float(np.abs(np.diff(W[n],axis=0)).max()),5)
with wave.open(str(D/"audio/SH37_comparatif_integration_265-275.wav")) as w: q = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1,2)
qs = lambda s: q[int(round(s*SR)):int(round(s*SR))+10*SR]; zone = np.zeros(10*SR, bool); zone[int((267.40-265)*SR):int((270.55-265)*SR)] = True
res["fichier_livré"] = {"durée_s": round(len(q)/SR,3), "échantillons_16bits_différents_de_A_hors_[267.40;270.55]": {"Cg": int((qs(idx[1][3])[~zone] != qs(idx[0][3])[~zone]).sum()), "Cs": int((qs(idx[2][3])[~zone] != qs(idx[0][3])[~zone]).sum())}}
(D/"analysis/sh37_integration_mesures.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps({k: v for k, v in res.items() if k in ("fichier_livré",) or k.startswith("raccords")}, indent=1, ensure_ascii=False))
for n in ("A","Cg","Cs"):
    r = res[n]; print(n, "| HF4-8k/0,5 s 267→271:", r["HF_4-8k_par_0.5s_dBFS"][4:12], "| I", r["I_LUFS"], "| TP", r["TP_dBTP"], "| ST max", r["court_terme_max_LUFS"], "| crête", r["crête_échantillon_dBFS"], "| clip", r["écrêtés"], "| mono", r["perte_mono_dB_zone"], "| 30-2100 zone", r["bande_30-2100Hz_zone_dBFS"], "| saut", res.get(n+"_saut", r.get("saut_max_échantillon_265-275")))
for n in ("Cg","Cs"):
    r = res[n]; print(n, {k: v for k, v in r.items() if k.startswith(("fond","écart","raccords"))})
