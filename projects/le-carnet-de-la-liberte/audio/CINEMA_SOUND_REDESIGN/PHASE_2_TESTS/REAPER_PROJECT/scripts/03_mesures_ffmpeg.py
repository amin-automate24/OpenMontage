#!/usr/bin/env python3
"""Mesures FFmpeg d'un export (sonie, crête vraie, écrêtage, compatibilité mono, niveau court terme). Aucune écoute n'est remplacée par ce script.
Usage (Windows/Linux, ffmpeg dans le PATH) :  python 03_mesures_ffmpeg.py export.wav [reference.wav]"""
import subprocess, re, sys
def run(args): return subprocess.run(["ffmpeg","-nostdin","-hide_banner"]+args, capture_output=True, text=True).stderr
def measure(p):
    e = run(["-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"]).split("Summary:")[-1]
    g = lambda k: re.findall(k + r":\s+(-?[\d.]+)", e)[0]
    st = run(["-i", p, "-af", "astats=metadata=0:reset=0", "-f", "null", "-"])
    flat = re.findall(r"Number of samples at max.*?: (\d+)|Peak level dB: (-?[\d.]+)", st)
    rms = lambda s: float(re.findall(r"RMS level dB:\s*(-?[\d.]+)", s)[-1])
    stereo = rms(run(["-i", p, "-af", "astats", "-f", "null", "-"]))
    mono = rms(run(["-i", p, "-af", "pan=mono|c0=0.5*c0+0.5*c1,astats", "-f", "null", "-"]))
    return {"fichier": p, "I_LUFS": float(g("I")), "LRA_LU": float(g("LRA")), "crête_vraie_dBTP": float(g("Peak")), "perte_mono_dB": round(mono - stereo, 2)}
for p in sys.argv[1:]: print(measure(p))
