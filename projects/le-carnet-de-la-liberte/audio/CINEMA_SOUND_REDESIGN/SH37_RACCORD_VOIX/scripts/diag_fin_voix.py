#!/usr/bin/env python3
"""Diagnostic du raccord voix/ambiance de SH37 (fin de la voix de Younes, Y5). Mesures uniquement, lecture seule.
Décompose le mix final sans perte en : voix (stem dialogue × gain local), musique MF (piste Mixkit 599 × gain), ambiance AMB (source M7c × gain+retard mesurés), résidu non expliqué."""
import subprocess, json
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; SR = 48000; S0 = 264.0; N = 10
rd = lambda p, ss, t: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(ss),"-t",str(t),"-i",str(p),"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def bp(x, lo, hi): X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); X[(f < lo) | (f >= hi)] = 0; return np.fft.irfft(X, len(x), axis=0)
def fshift(x, d): n = len(x); X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(n)[:,None]; return np.fft.irfft(X*np.exp(-2j*np.pi*f*d), n, axis=0)
mix = rd(R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav", S0, N); L = len(mix); t = S0+np.arange(L)/SR
D = np.roll(rd(R/"audio/mixes/M6/stems/dialogue.wav", S0, N), 47, axis=0); amb = rd(R/"audio/sfx_m7c/ambience_foley_m7c.wav", S0, N)
AMBs = 5.397*fshift(amb, 47.7)
trk = rd(R/"assets/music/mixkit/mixkit_599_possible_dreams.mp3", 140, 8); MF = np.zeros((L,2)); i0 = int((268.0-S0)*SR); MF[i0:i0+len(trk)] = trk[:L-i0]
MF *= np.clip((t-268.0)/1.0, 0, 1)[:,None]**2 if False else np.sin(np.clip((t-268.0)/1.0, 0, 1)*np.pi/2)[:,None]**2   # fondu d'entrée 1 s (repère MF)
MF = np.roll(MF, 47, axis=0)
# gains locaux (voix : fenêtres de 100 ms ; musique : bloc 268,3–270,3 sur la bande 200–2000 Hz hors voix/plume)
a, b = int((266.5-S0)*SR), int((268.0-S0)*SR); w = int(0.1*SR); g = np.zeros(L)
for k in range(a, b, w//2):
    x = D[k:k+w]; y = mix[k:k+w]-AMBs[k:k+w]; ex = (x*x).sum(); g[k:k+w//2] = (x*y).sum()/ex if ex > 1e-6*w else 0.0
DX = g[:,None]*D
s1, s2 = int((268.3-S0)*SR), int((270.3-S0)*SR); m, c = bp(mix-AMBs-DX, 200, 2000)[s1:s2], bp(MF, 200, 2000)[s1:s2]; aMF = float((m*c).sum()/(c*c).sum()); MUS = aMF*MF
RES = mix-AMBs-DX-MUS
comps = {"mix (master)": mix, "voix DX": DX, "musique MF": MUS, "ambiance AMB": AMBs, "résidu": RES}
print(f"gain musique MF = {aMF:.2f} ; AMB g = 5.397 (retard 47,7 éch.)")
print("— niveaux RMS (dBFS) et énergie 2–8 kHz par 50 ms, 267,35 → 268,35 s —")
hdr = f"{'t (s)':>7} | " + " | ".join(f"{k:>13}" for k in comps)
print(hdr)
out = {}
for tt in np.arange(267.35, 268.36, 0.05):
    i, j = int((tt-S0)*SR), int((tt+0.05-S0)*SR); row = []
    for k, x in comps.items():
        v = (round(float(db(x[i:j])),1), round(float(db(bp(x[i:j], 2000, 8000))),1)); row.append(v); out.setdefault(k, {})[f"{tt:.2f}"] = v
    print(f"{tt:7.2f} | " + " | ".join(f"{v[0]:6.1f}/{v[1]:6.1f}" for v in row))
print("— énergie 2–8 kHz par 0,25 s, 266,5 → 270,5 s (dBFS) : mix | voix | musique | AMB | résidu —")
for tt in np.arange(266.5, 270.5, 0.25):
    i, j = int((tt-S0)*SR), int((tt+0.25-S0)*SR); print(f"{tt:6.2f} | " + " | ".join(f"{db(bp(x[i:j],2000,8000)):6.1f}" for x in comps.values()))
json.dump(out, open(Path(__file__).resolve().parents[1]/"analysis/decomposition_fin_voix.json","w"), indent=1)
