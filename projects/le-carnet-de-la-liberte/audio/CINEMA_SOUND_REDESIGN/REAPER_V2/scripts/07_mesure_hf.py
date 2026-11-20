#!/usr/bin/env python3
"""Mesure l'énergie aiguë (>4 kHz) d'un WAV par tranche de 0,5 s sur ses 10 premières secondes : le crépitement du film (bruitage « plume ») donne ≈ −30 dBFS pendant ~2,6 s.
Usage : python 07_mesure_hf.py exports\\TEST_COURT_C_268-299.wav     (FFmpeg et numpy requis)   — mesure uniquement, aucune écoute."""
import subprocess, sys
import numpy as np
SR = 48000
x = np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-t","10","-i",sys.argv[1],"-af","pan=mono|c0=0.5*c0+0.5*c1","-f","f32le","-ar",str(SR),"-"],capture_output=True).stdout,"<f4").astype(np.float64)
def hf(s): X = np.fft.rfft(s); f = np.fft.rfftfreq(len(s), 1/SR); X[f < 4000] = 0; return 20*np.log10(np.sqrt(np.mean(np.fft.irfft(X, len(s))**2))+1e-12)
print("Énergie >4 kHz par 0,5 s (dBFS) depuis le début du fichier :")
for k in range(min(20, len(x)//(SR//2))): print(f"  {k*0.5:4.1f} s : {hf(x[k*SR//2:(k+1)*SR//2]):6.1f}")
