#!/usr/bin/env python3
"""M9T = TEST sonore QC2 (NON FINAL) : chaîne M7B.1 inchangée + lit M6 test (sélection Mixkit) ; ambiance −2 dB sous A1 (70,6–74,4 s) ; musique et ambiance −3 dB sous V1 (166,3–169,6 s). Dérivé de M8 : = M7B.1 chain unchanged (same voices, music B cues, ducking, finishing) with the M5 ambience/foley bed (real Mixkit recordings, perspective, J/L-cuts). Derived from M7B.1 script: Music B 'Possible Dreams' (Mixkit, licence archivée) on cues MA, MB, MC→MD (one continuous take), MF ; ME removed.
Changes vs M7B: softer electronic transitions (new ambience bed ambience_foley_m4_1.wav), crowd/music/dialogue rebalance in SH27-28,
softer 5 s cosine music exit on the title. Dialogue stem + positions identical to M6/M7B. Never overwrites. Usage: music_finish_m7b1.py"""
import sys, json, subprocess, wave, re, numpy as np
from pathlib import Path
R = Path(__file__).resolve().parent.parent; A = R/"audio"; SR = 48000; N = int(276.0*SR); VER = "M9T"
PRE = A/"mixes"/(VER+"_pre")
if PRE.exists() or (A/"mixes"/VER).exists(): sys.exit("version exists")
PRE.mkdir(parents=True)
def rd(p, n=N):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2); y = np.zeros((n, 2), np.float32); e = min(n, len(x)); y[:e] = x[:e]; return y
def wr(p, x):
    with wave.open(str(p), "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1)*32767).astype(np.int16).tobytes())
def lufs(x):
    p = PRE/"_t.wav"; wr(p, x); o = subprocess.run(["ffmpeg", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr; p.unlink(); return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
dlg = rd(A/"mixes/M6/stems/dialogue.wav"); amb = rd(A/"sfx_m6/ambience_foley_m6.wav")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(R/"assets/music/mixkit/mixkit_599_possible_dreams.mp3"), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
trk = np.frombuffer(raw, np.float32).reshape(-1, 2)
env = np.abs(dlg).max(axis=1); w = int(0.3*SR); c = np.cumsum(np.concatenate([[0], env])); sm = (c[w:]-c[:-w])/w; sm = np.concatenate([sm, np.full(N-len(sm), sm[-1])])
g_amb = np.clip(sm/0.05, 0, 1); g_mus = np.clip(sm/0.02, 0, 1)
t = np.arange(N)/SR
crowd = ((t >= 174.0) & (t <= 190.0)).astype(np.float32)
crowd = np.convolve(crowd, np.hanning(int(1.0*SR))/np.hanning(int(1.0*SR)).sum(), mode="same")      # fondu 1 s de la zone « foule »
depth_amb = (-9 + (-3)*crowd)                                                      # −9 dB sous la voix, −12 dB dans la foule
duck_amb = 10**((depth_amb*g_amb)/20)
amb_g = amb*duck_amb[:, None]*(10**((-2*crowd)/20))[:, None]                      # foule −2 dB (statique) pour laisser respirer musique et voix
CUES = [("MA", 50.5, 66.0, 1.5, 1.5, -31, 0), ("MB", 109.0, 121.0, 1.2, 2.0, -32, 110), ("MCMD", 151.5, 189.5, 3.0, 1.5, -32, 15), ("MF", 268.0, 276.0, 1.0, 5.0, -30, 140)]
mus = np.zeros((N, 2), np.float32); placed = []
for cid, a, b, fi, fo, tgt, off in CUES:
    L = int((b-a)*SR); seg = trk[int(off*SR):int(off*SR)+L].copy()
    if len(seg) < L: seg = np.vstack([seg, np.zeros((L-len(seg), 2), np.float32)])
    g = 10**((tgt-lufs(np.vstack([seg, np.zeros((SR, 2), np.float32)])))/20); seg *= g
    e = np.ones(L, np.float32); i1 = int(fi*SR); i2 = int(fo*SR)
    if i1: e[:i1] = np.sin(np.linspace(0, np.pi/2, i1))**2                         # entrée en cos² (douce)
    if i2: e[-i2:] *= np.cos(np.linspace(0, np.pi/2, i2))**2                        # sortie en cos² (plus douce que l'ancienne rampe)
    if cid == "MCMD": k = int((175.0-a)*SR); e[k:] *= 10**(1.5/20)
    mus[int(a*SR):int(a*SR)+L] += seg*e[:, None]; placed.append({"cue": cid, "film_in": a, "film_out": b, "fade_in": fi, "fade_out": fo, "track_offset_s": off, "target_lufs": tgt, "gain_db": round(20*np.log10(g), 1)})
duck_mus = (1-(1-10**(-9/20))*g_mus)[:, None]
def win(a, b, f): return np.clip(np.minimum((t-a)/f, (b-t)/f), 0, 1)
g_a1 = 10**((-2.0*(0.5-0.5*np.cos(np.pi*win(70.6, 74.4, 0.4))))/20)          # rue 1944 : fond −2 dB sous A1
g_v1 = 10**((-3.0*(0.5-0.5*np.cos(np.pi*win(166.3, 169.6, 0.4))))/20)        # V1 : musique + rumeur −3 dB
amb_g = amb_g*(g_a1*g_v1)[:, None]; duck_mus = duck_mus*g_v1[:, None]
mix = dlg+amb_g+mus*duck_mus; mix = mix/max(1.0, np.abs(mix).max()/0.89)
wr(PRE/"mix_premaster.wav", mix); wr(PRE/"music_bed_ducked.wav", mus*duck_mus); wr(PRE/"ambience_ducked.wav", amb_g)
for nm, a, b in (("SH22", 126.0, 134.0), ("SH23", 134.0, 145.5), ("SH29-33", 189.5, 239.5), ("ME", 244.8, 250.0)): assert np.abs(mus[int(a*SR):int(b*SR)]).max() == 0, nm
json.dump({"version": VER, "base": "M7B.1 (bed M5)", "track": "assets/music/mixkit/mixkit_599_possible_dreams.mp3", "cues": placed, "changes": ["transitions électroniques : whooshes −8 dB et filtrés (150–1400 Hz), recherche de station radio −7 dB et plus étroite", "foule SH27-28 : −2 dB statique, ducking sous voix −12 dB (au lieu de −9)", "sortie musicale du titre : cos² sur 5 s (avant : rampe carrée 2,5 s)", "ME supprimé"], "guards": "aucune musique sur SH22, SH23, SH29-33 ni ME : vérifié"}, open(PRE/"music_report.json", "w"), ensure_ascii=False, indent=1)
subprocess.run([sys.executable, str(R/"scripts/finish_master_audio.py"), VER+"_pre", VER], check=True)
