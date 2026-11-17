#!/usr/bin/env python3
"""M4 sound design — 100 % procedural (numpy synthesis, seed fixed): no third-party samples, rights owned by the project.
Writes audio/sfx_m4/ambience_foley_m4.wav (stereo 48 kHz) + audio/sfx_m4/cues_m4.json. Does not touch any existing file."""
import json, wave, sys, numpy as np
from pathlib import Path
R = Path(__file__).resolve().parent.parent; OUT = R/"audio/sfx_m4"; SR = 48000; T = 276.0; N = int(T*SR)
rng = np.random.default_rng(1956)
sys.path.insert(0, str(Path(__file__).parent)); from shots_data import SHOTS
SH = {s["n"]: (s["start"], s["start"]+s["dur"]) for s in SHOTS}
def db(x): return 10**(x/20)
def _unused(): pass
    # vectorised via scipy-free recursion in chunks
def fft_band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/SR); m = ((f >= lo) & (f <= hi)).astype(float)
    # soft skirts
    m = np.convolve(m, np.hanning(64)/np.hanning(64).sum(), mode="same"); return np.fft.irfft(X*m, len(x)).astype(np.float32)
def noise(d, lo, hi): x = rng.standard_normal(int(d*SR)).astype(np.float32); y = fft_band(x, lo, hi); return y/(np.sqrt(np.mean(y**2))+1e-9)
def slow_am(n, rate, depth):
    k = max(4, int(n/SR*rate)+3); pts = 1-depth*rng.random(k); t = np.linspace(0, k-1, n); return np.interp(t, np.arange(k), pts).astype(np.float32)
def env(n, a, r):
    e = np.ones(n, np.float32); ia = max(1, int(a*SR)); ir = max(1, int(r*SR)); e[:ia] = np.linspace(0, 1, ia); e[-ir:] *= np.linspace(1, 0, ir); return e
L = np.zeros(N, np.float32); Rr = np.zeros(N, np.float32); cues = []
def put(sig, t0, gain_db, pan=0.0, name=None):
    i0 = int(t0*SR); e = min(len(sig), N-i0)
    if e <= 0: return
    gl, gr = np.cos((pan+1)*np.pi/4)*1.414, np.sin((pan+1)*np.pi/4)*1.414
    L[i0:i0+e] += sig[:e]*db(gain_db)*gl; Rr[i0:i0+e] += sig[:e]*db(gain_db)*gr
    if name: cues.append({"t": round(t0, 2), "dur": round(e/SR, 2), "cue": name, "gain_db": gain_db})
def bed(t0, t1, lo, hi, gain_db, am_rate=0.15, am_depth=0.5, fade=1.5, name=None, stereo_decor=True):
    d = t1-t0+fade; n = int(d*SR)
    a = noise(d, lo, hi)*slow_am(n, am_rate, am_depth)*env(n, fade, fade)
    b = noise(d, lo, hi)*slow_am(n, am_rate, am_depth)*env(n, fade, fade) if stereo_decor else a
    i0 = int(max(0, t0-fade/2)*SR); e = min(n, N-i0)
    L[i0:i0+e] += a[:e]*db(gain_db); Rr[i0:i0+e] += b[:e]*db(gain_db)
    if name: cues.append({"t": round(t0, 2), "dur": round(t1-t0, 2), "cue": name, "gain_db": gain_db})
# --- elementary foley ---
def click(dur=0.012, lo=2000, hi=7000): n = int(dur*SR); return noise(dur, lo, hi)*np.exp(-np.linspace(0, 8, n)).astype(np.float32)
def thud(f0=110, dur=0.25): t = np.arange(int(dur*SR))/SR; return (np.sin(2*np.pi*f0*t)*np.exp(-t*18)+0.3*noise(dur, 80, 600)*np.exp(-t*30)).astype(np.float32)
def page(dur=0.45): n = int(dur*SR); e = np.sin(np.linspace(0, np.pi, n))**1.5; return (noise(dur, 900, 6000)*e*slow_am(n, 30, 0.6)).astype(np.float32)
def pen(dur):  # handwriting scratch: bursts of strokes
    n = int(dur*SR); g = (rng.random(int(dur*12)+2) > 0.35).astype(float); g = np.repeat(g, int(SR/12)+1)[:n]
    g = np.convolve(g, np.hanning(600)/300, mode="same"); return (noise(dur, 2500, 8000)*g*slow_am(n, 9, 0.7)).astype(np.float32)
def creak(dur=0.7, f0=320, f1=210):
    t = np.arange(int(dur*SR))/SR; f = np.linspace(f0, f1, len(t)); ph = 2*np.pi*np.cumsum(f)/SR
    pulse = (np.sin(ph) > 0.92).astype(np.float32); y = fft_band(pulse, 150, 2500); y /= np.abs(y).max()+1e-9; return (y*env(len(t), 0.05, 0.2)).astype(np.float32)
def chirp_bird(): d = rng.uniform(0.06, 0.14); t = np.arange(int(d*SR))/SR; f = np.linspace(rng.uniform(3000, 4200), rng.uniform(4300, 5600), len(t)); return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.linspace(0, np.pi, len(t)))).astype(np.float32)
def cricket(): t = np.arange(int(0.12*SR))/SR; return (np.sin(2*np.pi*4300*t)*(np.sin(2*np.pi*25*t) > 0)*np.sin(np.linspace(0, np.pi, len(t)))).astype(np.float32)
def murmur(d, nvoices=8, lo=250, hi=1400):
    n = int(d*SR); y = np.zeros(n, np.float32)
    for _ in range(nvoices):
        sy = (rng.random(int(d*5)+2) > 0.45).astype(float); g = np.convolve(np.repeat(sy, int(SR/5)+1)[:n], np.hanning(2400)/1200, mode="same")
        c = rng.uniform(lo, hi); y += noise(d, c*0.7, c*1.5)*g.astype(np.float32)*slow_am(n, 0.3, 0.6)
    return y/(np.sqrt(np.mean(y**2))+1e-9)
def whoosh(d, rising=True): n = int(d*SR); e = np.linspace(0, 1, n)**2 if rising else np.linspace(1, 0, n)**2; return (noise(d, 200, 3000)*e*np.sin(np.linspace(0, np.pi, n))).astype(np.float32)
# ===== Scene 1 — classe 2026 (0-30)
bed(0, 30, 60, 380, -50, name="classe: ton de pièce chaud (lp 380 Hz)")
put(murmur(30, 6, 300, 1100)*env(int(30*SR), 2, 2), 0, -55, 0.2, "classe: murmure lointain d'élèves (très bas)")
a, b = SH[2]; t = a+0.8
while t < a+3.2: put(click(0.01, 2500, 7000), t, -36, -0.2); t += rng.uniform(0.08, 0.22)
cues.append({"t": a+0.8, "dur": 2.4, "cue": "craie au tableau (SH02, pendant l'écriture de la date)", "gain_db": -36})
put(thud(160, 0.12), SH[3][0]+0.1, -40, 0.15, "chaise/bras levé discret (SH03)")
put(whoosh(2.0), SH[6][0]+0.3, -42, 0, "transition date -> page (SH06)")
# ===== Scene 2 — maison 2026 (30-65)
bed(30, 61.5, 50, 300, -52, am_rate=0.1, name="maison 2026: ton de pièce")
for k in range(int(30), int(61)):
    put(click(0.006, 1800, 3500)*0.7, k+0.02, -50, -0.4)
cues.append({"t": 30, "dur": 31, "cue": "horloge tic-tac discret 1 Hz", "gain_db": -50})
put(creak(0.8, 300, 200), SH[7][0]+0.8, -38, 0.1, "boîte en bois : charnière (SH07)"); put(thud(140, 0.2), SH[7][0]+1.7, -38, 0.1, "boîte : couvercle posé")
put(page(0.5), SH[10][0]+0.8, -38, 0, "ouverture du carnet (SH10)")
for i, dt in enumerate([0.4, 1.1, 1.8, 2.5, 3.3]): put(page(0.4), SH[11][0]+dt, -38-i, 0.1*(-1)**i)
cues.append({"t": SH[11][0], "dur": 3.7, "cue": "pages qui tournent au souffle de vent (SH11)", "gain_db": -38})
bed(SH[11][0], SH[11][1], 250, 900, -46, am_rate=0.6, am_depth=0.8, fade=1.0, name="souffle de vent (SH11)")
put(whoosh(3.5), SH[12][0], -40, 0, "transition encre -> rue 1944 (SH12)")
# ===== Scene 3 — rue 1944 (65-86) puis intérieur jour (86-120)
bed(63.5, 86, 120, 900, -47, am_rate=0.25, name="rue 1944: air extérieur")
put(murmur(21, 10, 250, 1300)*env(int(21*SR), 2, 2), 65, -49, -0.3, "rue 1944: habitants qui discutent (loin)")
t = 65.5
while t < 85: put(chirp_bird(), t, -46, rng.uniform(-0.7, 0.7)); t += rng.uniform(0.8, 3.0)
cues.append({"t": 65.5, "dur": 19.5, "cue": "oiseaux épars (rue)", "gain_db": -46})
t = SH[13][0]+0.3
while t < SH[14][1]: put(thud(rng.uniform(90, 130), 0.09), t, -45, 0.05); t += rng.uniform(0.5, 0.6)
cues.append({"t": SH[13][0], "dur": SH[14][1]-SH[13][0], "cue": "pas sur la pierre (Amina et son père)", "gain_db": -45})
bed(86, 120, 60, 350, -53, am_rate=0.1, name="intérieur jour 1944: ton de pièce")
put(page(0.25)*2, SH[16][0]+1.0, -36, 0.1, "feuille posée sur la table (SH16)")
put(pen(5.0), SH[19][0]+0.6, -40, 0.1, "plume sur le carnet (SH19, écrit — non dit, D8)")
for dt in (0.3, 1.2, 2.1, 3.0): put(page(0.4), SH[20][0]+dt, -39, 0)
cues.append({"t": SH[20][0], "dur": 3.5, "cue": "pages -> 1953 (SH20)", "gain_db": -39})
# ===== Scene 4 — nuit 1953 (120-175)
bed(120, 163.5, 50, 260, -54, am_rate=0.08, name="nuit 1953: intérieur feutré")
t = 120.3
while t < 163: put(cricket(), t, -50, rng.uniform(0.3, 0.8)); t += rng.uniform(0.6, 1.4)
cues.append({"t": 120.3, "dur": 43, "cue": "grillons au loin (fenêtre)", "gain_db": -50})
# radio (SH22): tuning, crackle + hum bed, switch off
tt = np.arange(int(0.7*SR))/SR; tun = np.sin(2*np.pi*np.cumsum(np.linspace(900, 2600, len(tt)))/SR)*0.5+noise(0.7, 400, 3000)*0.5
put(fft_band(tun.astype(np.float32), 400, 3200)*env(len(tt), 0.05, 0.2), 125.75, -38, 0, "radio : recherche de station (SH22)")
d = SH[22][1]-126.4; n = int(d*SR); crk = noise(d, 2000, 6000)*0.25; imp = (rng.random(n) > 0.9993).astype(np.float32)*rng.uniform(1, 3, n).astype(np.float32)
crk += fft_band(imp, 1500, 7000); hum = (np.sin(2*np.pi*50*np.arange(n)/SR)+0.4*np.sin(2*np.pi*150*np.arange(n)/SR)).astype(np.float32)*0.6
put((crk+hum)*env(n, 0.3, 0.3), 126.4, -44, 0, "radio : souffle, craquements et ronflement 50 Hz sous l'annonce")
put(click(0.02, 800, 4000)*2, SH[22][1]-0.05, -34, 0, "radio éteinte : clic (début du silence SH23)")
put(pen(4.5), SH[24][0]+0.8, -41, 0.1, "plume (SH24, écrit — non dit, D8)")
for i in range(6): put(page(0.45), SH[25][0]+0.8+i*1.9, -40, 0.1*(-1)**i)
bed(SH[25][0], SH[25][1], 200, 1200, -49, am_rate=0.5, am_depth=0.7, fade=1.5, name="saisons : vent qui passe (SH25)")
cues.append({"t": SH[25][0], "dur": 12, "cue": "pages du carnet 1953-1955 (SH25)", "gain_db": -40})
put(creak(0.9, 260, 180), SH[26][0]+0.3, -37, 0.4, "fenêtre qui s'ouvre (SH26)"); put(click(0.015, 1500, 5000), SH[26][0]+1.2, -38, 0.4)
put(murmur(11, 14, 300, 1600)*np.linspace(0, 1, int(11*SR)).astype(np.float32)**2, SH[26][0]+0.5, -44, 0.3, "rumeur de joie qui monte dehors (SH26 -> scène 5)")
# ===== Scene 5 — Rabat 1955 (175-189.5), intérieurs (189.5-250)
crowd = murmur(16, 30, 300, 2200); n = len(crowd); swell = slow_am(n, 0.4, 0.5)
put(crowd*swell*env(n, 1.0, 1.5), 174.0, -36, 0, "foule en liesse, Rabat 1955 (SH27-28, sous les dialogues)")
put(murmur(16, 20, 400, 2500)*env(n, 1.0, 1.5), 174.0, -40, -0.5); put(murmur(16, 20, 400, 2500)*env(n, 1.0, 1.5), 174.0, -40, 0.5)
for t in (176.2, 178.9, 181.0): put(noise(1.2, 500, 3500)*env(int(1.2*SR), 0.15, 0.8), t, -37, rng.uniform(-0.5, 0.5))
cues.append({"t": 176.2, "dur": 6, "cue": "3 vagues d'acclamations", "gain_db": -37})
bed(189.5, 250, 50, 320, -53, am_rate=0.1, name="intérieur 1955-56: ton de pièce")
put(page(0.5), SH[29][0]+0.2, -38, 0, "page 18 novembre 1955 (SH29)")
put(pen(3.0), SH[30][0]+6.5, -42, 0.1, "plume (SH30, après la réplique A6)")
put(page(0.5), SH[31][0]+0.2, -38, 0, "page 2 mars 1956 (SH31)")
put(page(0.35), SH[33][0]+0.2, -40, 0, "ligne du temps : entrée (SH33)")
put(thud(120, 0.3)*1.2, 248.3, -36, 0, "le carnet se referme (SH34)")
# ===== Scene 6 — classe 2026 (250-276)
bed(250, 270.5, 60, 380, -50, name="classe: ton de pièce")
put(murmur(20, 6, 300, 1100)*env(int(20*SR), 2, 2), 250, -56, 0.2, "classe: murmure très bas")
put(pen(2.6), 267.7, -40, 0.1, "Younes écrit dans son cahier (SH37, écrit — non dit)")
put(thud(150, 0.2), 270.7, -38, 0, "le cahier se referme (SH38)")
bed(270.5, 276.0, 200, 1500, -47, am_rate=0.6, am_depth=0.6, fade=1.0, name="vent léger, drapeau (SH38)")
# master fade out
fo = int(2.5*SR); L[-fo:] *= np.linspace(1, 0, fo); Rr[-fo:] *= np.linspace(1, 0, fo)
st = np.stack([L, Rr], 1); pk = np.abs(st).max(); st = st*min(1.0, 0.5/pk)
OUT.mkdir(parents=True, exist_ok=True)
with wave.open(str(OUT/"ambience_foley_m4.wav"), "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st, -1, 1)*32767).astype(np.int16).tobytes())
json.dump({"seed": 1956, "rights": "synthèse procédurale locale (numpy), aucun échantillon tiers ; droits détenus par le projet", "peak_scale": round(float(min(1.0, 0.5/pk)), 3), "cues": sorted(cues, key=lambda c: c["t"])}, open(OUT/"cues_m4.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(cues), "cues")
