#!/usr/bin/env python3
"""M9T.1 = même automation QC1 (M7B.2), appliquée au test M9T — gain automation only, no new sound, no new effect.
1) 169.4-182.4 s (SH26 end / SH27, between V1 and A5): crowd+music -2.5 dB (1 s cosine ramps, no dialogue touched).
2) Quiet passages SH10-12 (48.4-70.9 s) and SH33 (224.3-240.3 s): level-dependent lift only where momentary
   loudness < -29 LUFS: gain = min(7, 0.7*(-29-M)) dB, smoothed 1.5 s, 0.5 s fades at window edges -> calm parts
   become audible but stay calm (relative silences kept). M7B.1 untouched; never overwrites."""
import re, sys, wave, numpy as np
from pathlib import Path
R = Path(__file__).resolve().parent.parent; SRC = R/"audio/mixes/M9T2/MIX_276s_M9T2.wav"; OUT = R/"audio/mixes/M9T2.1/MIX_276s_M9T2.1.wav"
if OUT.exists(): sys.exit("exists")
w = wave.open(str(SRC)); sr = w.getframerate(); n = w.getnframes(); x = np.frombuffer(w.readframes(n), "<i2").reshape(-1, 2).astype(np.float64)/32768
t = np.arange(n)/sr; g = np.zeros(n)                       # gain in dB
def win(a, b, f): return np.clip(np.minimum((t-a)/f, (b-t)/f), 0, 1)
r = win(169.4, 182.4, 1.0); g += -2.5*(0.5-0.5*np.cos(np.pi*r))
tm, M = [], []; cur = None
for l in open(sys.argv[1]):
    m = re.search(r"pts_time:([\d.]+)", l); cur = float(m.group(1)) if m else cur
    m = re.search(r"r128.M=(-?[\d.]+|-inf)", l)
    if m and cur is not None: tm.append(cur); M.append(-90.0 if "inf" in m.group(1) else float(m.group(1)))
tm, M = np.array(tm), np.array(M); lift = np.clip(0.7*(-29-M), 0, 7)
k = int(1.5/np.median(np.diff(tm))); lift = np.convolve(lift, np.ones(k)/k, "same")
L = np.interp(t, tm, lift); mask = np.maximum(win(48.4, 70.9, 0.5), win(224.3, 240.3, 0.5)); g += L*mask
g += 0.2   # make-up so integrated stays -16.0 LUFS (peaks stay < -1 dBTP, checked)
y = x*10**(g/20)[:, None]
pk = np.abs(y).max(); print("gain dB min/max", round(g.min(), 2), round(g.max(), 2), "sample peak", round(20*np.log10(pk), 2))
d = (np.random.rand(*y.shape)-np.random.rand(*y.shape))/32768
TMP = OUT.with_name("_tmp.wav"); o = wave.open(str(TMP), "wb"); o.setnchannels(2); o.setsampwidth(2); o.setframerate(sr); o.writeframes(np.clip(np.round((y+d)*32767), -32768, 32767).astype("<i2").tobytes()); o.close()
import subprocess; subprocess.run(["ffmpeg", "-v", "error", "-n", "-i", str(TMP), "-af", "alimiter=limit=0.84:level=disabled:attack=1:release=60", "-c:a", "pcm_s16le", str(OUT)], check=True); TMP.unlink(); print("ok", OUT)
