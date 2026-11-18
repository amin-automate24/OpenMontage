#!/usr/bin/env python3
"""Intégration sonore QC2 SON1 (autorisée 19/11/2026), selon docs/PLAN_INTEGRATION_AUDIO_QC2.md.
QC1 (MIX_276s_M7B.2.wav) conservé À L'ÉCHANTILLON PRÈS hors 163,5-193,0 s ; dans la zone : M9T2.3 aligné (-47 éch.), niveau calé,
raccords complémentaires (cos²/sin², somme = 1, sources corrélées -> pas de bosse) 163,5-164,5 et 192,0-193,0. N'écrase rien."""
import sys, wave, json, numpy as np
from pathlib import Path
R = Path(__file__).resolve().parent.parent; SR = 48000
OUT = R/"audio/mixes/QC2_SON1/MIX_276s_QC2_SON1.wav"
if OUT.exists(): sys.exit("exists")
def rd(p):
    w = wave.open(str(p)); assert w.getframerate() == SR and w.getnchannels() == 2 and w.getsampwidth() == 2
    return np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, 2)
Q = rd(R/"audio/mixes/M7B.2/MIX_276s_M7B.2.wav"); N = rd(R/"audio/mixes/M9T2.3/MIX_276s_M9T2.3.wav"); n = len(Q)
def lag(a, b, maxlag=400):                      # décalage (éch.) qui aligne b sur a, par corrélation croisée
    a = a.mean(1).astype(np.float64); b = b.mean(1).astype(np.float64); L = len(a)+maxlag
    c = np.fft.irfft(np.fft.rfft(a, 2*L)*np.conj(np.fft.rfft(b, 2*L))); c = np.concatenate([c[-maxlag:], c[:maxlag+1]]); return int(np.argmax(c)-maxlag)
quiet = [(5, 15), (35, 45), (80, 90), (100, 110), (150, 160), (200, 215), (253, 262)]       # passages sans changement
lags = [lag(Q[int(a*SR):int(b*SR)], N[int(a*SR):int(b*SR)]) for a, b in quiet]; print("décalages mesurés (éch.) :", lags)
D = -int(np.median(lags)); assert len(set(lags)) == 1, "décalage non constant"   # lag < 0 : N est en retard de D échantillons sur QC1
assert D == 47; Na = np.zeros_like(N); Na[:n-D] = N[D:]
def corr(a, b): a = a.mean(1).astype(float); b = b.mean(1).astype(float); return float(np.corrcoef(a, b)[0, 1])
print("corrélation après alignement (passages inchangés) :", [round(corr(Q[int(a*SR):int(b*SR)], Na[int(a*SR):int(b*SR)]), 4) for a, b in quiet])
db = lambda x: 20*np.log10(np.sqrt((x.astype(np.float64)**2).mean())+1e-9)
offs = [db(Na[int(a*SR):int(b*SR)])-db(Q[int(a*SR):int(b*SR)]) for a, b in ((150, 160), (160, 163.4), (193.2, 200), (200, 215))]
g_in, g_out = float(offs[1]), float(offs[2])          # écart juste avant / juste après la zone (la normalisation dynamique de M9T2.3 dérive de 0,06 à 0,17 dB)
print("écarts de niveau hors zone (dB) :", [round(float(o), 3) for o in offs], "-> calage linéaire en dB : -%.3f (163,5 s) -> -%.3f (193,0 s)" % (g_in, g_out))
G = -(g_in+(g_out-g_in)*np.clip((np.arange(n)/SR-163.5)/(193.0-163.5), 0, 1))
a0, a1, b0, b1 = int(163.5*SR), int(164.5*SR), int(192.0*SR), int(193.0*SR)
w = np.zeros(n); w[a1:b0] = 1.0
w[a0:a1] = np.sin(np.linspace(0, np.pi/2, a1-a0))**2; w[b0:b1] = np.cos(np.linspace(0, np.pi/2, b1-b0))**2
mix = Q.astype(np.float64)*(1-w)[:, None]+Na.astype(np.float64)*(10**(G/20))[:, None]*w[:, None]
out = np.clip(np.round(mix), -32768, 32767).astype("<i2"); out[:a0] = Q[:a0]; out[b1:] = Q[b1:]       # hors zone : QC1 exact
assert np.array_equal(out[:a0], Q[:a0]) and np.array_equal(out[b1:], Q[b1:])
with wave.open(str(OUT), "wb") as f: f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(out.tobytes())
json.dump({"base": "MIX_276s_M7B.2.wav", "zone_s": [163.5, 193.0], "raccords_s": [[163.5, 164.5], [192.0, 193.0]], "alignement_echantillons": D, "calage_niveau_dB": [round(-g_in, 3), round(-g_out, 3)], "source_zone": "MIX_276s_M9T2.3.wav"}, open(OUT.with_suffix(".json"), "w"), indent=1)
print("ok", OUT)
