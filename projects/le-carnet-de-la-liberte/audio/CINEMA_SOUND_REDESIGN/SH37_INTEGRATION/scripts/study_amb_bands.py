#!/usr/bin/env python3
"""Étude : que contient la piste AMB (source M7c, à l'échelle du mix) avant, pendant et après le bruitage de plume ? Mesures uniquement."""
import subprocess, json
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; SR = 48000; S0 = 265.0
rd = lambda p, ss, t: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(ss),"-t",str(t),"-i",str(p),"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def bp(x, lo, hi): X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); X[(f < lo) | (f >= hi)] = 0; return np.fft.irfft(X, len(x), axis=0)
def fshift(x, d): n = len(x); X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(n)[:,None]; return np.fft.irfft(X*np.exp(-2j*np.pi*f*d), n, axis=0)
amb = rd(R/"audio/sfx_m7c/ambience_foley_m7c.wav", S0, 10); G = 5.397; AM = G*fshift(amb, 47.7)       # contribution AMB dans le mix (gain mesuré +14,6 dB)
bands = [(30,150),(150,500),(500,1000),(1000,1500),(1500,2100),(2100,4000),(4000,8000),(8000,16000)]
wins = {"avant la plume (266,0–267,4 s)": (266.0, 267.4), "PLUME (268,0–270,2 s)": (268.0, 270.2), "après : vent + cahier (270,8–273,0 s)": (270.8, 273.0)}
out = {}
print(f"{'bande (Hz)':>12} | " + " | ".join(f"{k:>38}" for k in wins))
for lo, hi in bands:
    row = []
    for k, (a, b) in wins.items():
        s = bp(AM, lo, hi)[int((a-S0)*SR):int((b-S0)*SR)]; v = round(float(db(s)),1); row.append(v); out.setdefault(k, {})[f"{lo}-{hi}"] = v
    print(f"{lo:5d}-{hi:5d} | " + " | ".join(f"{v:>34.1f} dBFS" for v in row))
tot = {k: round(float(db(AM[int((a-S0)*SR):int((b-S0)*SR)])),1) for k, (a, b) in wins.items()}; print("large bande (dBFS) :", tot)
Path(__file__).resolve().parents[1].joinpath("analysis/etude_bandes_AMB.json").write_text(json.dumps({"bandes_dBFS_échelle_mix": out, "large_bande": tot}, indent=1, ensure_ascii=False))
