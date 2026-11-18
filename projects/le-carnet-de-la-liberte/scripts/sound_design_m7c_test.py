#!/usr/bin/env python3
"""M7c (raccord SH28->SH29, 19/11 : queue de foule (cos²)^0.45) — dérivé de M7b :\nM7b (finition 19/11 : la foule finit à 190,0 s, fondu cos² 2 s) — dérivé de M7 :\nM7 TEST sonore (décisions audio M9T.1, 19/11) — dérivé de M4.1 (--soft) : SEULE l'ambiance de foule 1955 (SH26 rumeur, SH27-28 foule) est réelle (Mixkit 364) ;\nacclamations (Mixkit 462, 437) ATTÉNUÉES (−8 dB) et filtrées 250–3200 Hz, entrée 0,8 s (moins « stade moderne »). Tout le reste = M4.1 synthétique.\nÉcrit audio/sfx_m7/ambience_foley_m7c.wav ; n'écrase rien.\nORIGINAL M4 DOC: M4 sound design — 100 % procedural (numpy synthesis, seed fixed): no third-party samples, rights owned by the project.
Writes audio/sfx_m4/ambience_foley_m4.wav (stereo 48 kHz) + audio/sfx_m4/cues_m4.json. Does not touch any existing file."""
import json, wave, sys, numpy as np
from pathlib import Path
R = Path(__file__).resolve().parent.parent; OUT = R/"audio/sfx_m7c"; SR = 48000; T = 276.0; N = int(T*SR)
SOFT = True   # M7B.1 : transitions électroniques atténuées (mêmes tirages aléatoires)
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
# ---------------- M6 test: real samples (sélection), SANS réverbération ----------------
import subprocess
MK = R/"assets/sfx/mixkit"; _cache = {}
def smp(i):
    if i not in _cache:
        f = next(MK.glob(f"mixkit_{i}_*.wav")); raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy(); e = np.sqrt((x**2).mean(1)); thr = np.percentile(e, 50)
        rms = np.sqrt((x[e >= thr]**2).mean())+1e-9; _cache[i] = x/rms          # active-part RMS = 1 (same scale as the synthetic noise)
    return _cache[i]
def seg(i, off, d):
    x = smp(i); n = int(d*SR); o = int(off*SR) % len(x); y = np.concatenate([x[o:]]+[x]*(n//len(x)+1))[:n]; return y.copy()
def fades(y, a, b):
    n = len(y); ia, ib = max(1, int(a*SR)), max(1, int(b*SR)); y[:ia] *= np.sin(np.linspace(0, np.pi/2, ia))[:, None]**2; y[-ib:] *= np.cos(np.linspace(0, np.pi/2, ib))[:, None]**2; return y
def band2(y, lo, hi): return np.stack([fft_band(y[:, 0].copy(), lo, hi), fft_band(y[:, 1].copy(), lo, hi)], 1)
_r2 = np.random.default_rng(55)                    # separate generator: never disturbs the M4.1 draws
def ir(rt, pre=0.0):
    n = int(rt*SR*1.2); t = np.arange(n)/SR; h = _r2.standard_normal((n, 2)).astype(np.float32)*np.exp(-6.9*t/rt)[:, None]
    if pre: h = np.concatenate([np.zeros((int(pre*SR), 2), np.float32), h]); return h/np.sqrt((h**2).sum(0))
    return h/np.sqrt((h**2).sum(0))
def verb(y, rt, wet_db, pre=0.0):
    h = ir(rt, pre); n = len(y)+len(h); N2 = 1 << (n-1).bit_length(); out = np.zeros((n, 2), np.float32)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(y[:, c], N2)*np.fft.rfft(h[:, c], N2), N2)[:n]
    w = out*db(wet_db); w[:len(y)] += y; return w
ROOM = (0.35, -17); STREET = (0.5, -15, 0.03); SQUARE = (0.9, -12, 0.04)
def putS(y, t0, gain_db, pan=0.0, name=None, persp=None):
    if persp: y = verb(y, persp[0], persp[1], persp[2] if len(persp) > 2 else 0.0)
    i0 = int(t0*SR); e = min(len(y), N-i0)
    if e <= 0: return
    gl, gr = np.cos((pan+1)*np.pi/4)*1.414, np.sin((pan+1)*np.pi/4)*1.414
    L[i0:i0+e] += y[:e, 0]*db(gain_db)*gl; Rr[i0:i0+e] += y[:e, 1]*db(gain_db)*gr
    if name: cues.append({"t": round(t0, 2), "dur": round(e/SR, 2), "cue": name, "gain_db": gain_db, "source": "Mixkit (enregistrement réel)"})
def drop(*a, **k): pass                        # synthetic element computed (random draws kept) but not mixed
def writing(d):                                # real pen-on-paper phrase built from two Mixkit takes
    out = np.zeros((int(d*SR), 2), np.float32); t = 0.0; k = 0
    while t < d-0.3:
        x = smp(2368 if k % 2 == 0 else 2369); x = x[:int(min(len(x)/SR, d-t)*SR)].copy(); x = fades(x, 0.03, 0.08); i = int(t*SR); out[i:i+len(x)] += x; t += len(x)/SR+_r2.uniform(0.15, 0.45); k += 1
    return out
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
def whoosh(d, rising=True): n = int(d*SR); e = np.linspace(0, 1, n)**2 if rising else np.linspace(1, 0, n)**2; return (noise(d, 150 if SOFT else 200, 1400 if SOFT else 3000)*e*np.sin(np.linspace(0, np.pi, n))).astype(np.float32)
# ===== Scene 1 — classe 2026 (0-30)
bed(0, 30, 60, 380, -50, name="classe: ton de pièce chaud (lp 380 Hz)")
put(murmur(30, 6, 300, 1100)*env(int(30*SR), 2, 2), 0, -55, 0.2, "classe: murmure lointain d'élèves (très bas)")
a, b = SH[2]; t = a+0.8
while t < a+3.2: put(click(0.01, 2500, 7000), t, -36, -0.2); t += rng.uniform(0.08, 0.22)
cues.append({"t": a+0.8, "dur": 2.4, "cue": "craie au tableau (SH02, pendant l'écriture de la date)", "gain_db": -36})
put(thud(160, 0.12), SH[3][0]+0.1, -40, 0.15, "chaise/bras levé discret (SH03)")
put(whoosh(2.0), SH[6][0]+0.3, -50 if SOFT else -42, 0, "transition date -> page (SH06)")
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
put(whoosh(3.5), SH[12][0], -48 if SOFT else -40, 0, "transition encre -> rue 1944 (SH12)")
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
tt = np.arange(int(0.7*SR))/SR; tun = np.sin(2*np.pi*np.cumsum(np.linspace(900, 2600, len(tt)))/SR)*(0.25 if SOFT else 0.5)+noise(0.7, 400, 3000)*0.5
put(fft_band(tun.astype(np.float32), 500 if SOFT else 400, 2200 if SOFT else 3200)*env(len(tt), 0.05, 0.2), 125.75, -45 if SOFT else -38, 0, "radio : recherche de station (SH22)")
d = SH[22][1]-126.4; n = int(d*SR); crk = noise(d, 2000, 6000)*0.25; imp = (rng.random(n) > 0.9993).astype(np.float32)*rng.uniform(1, 3, n).astype(np.float32)
crk += fft_band(imp, 1500, 7000); hum = (np.sin(2*np.pi*50*np.arange(n)/SR)+0.4*np.sin(2*np.pi*150*np.arange(n)/SR)).astype(np.float32)*0.6
put((crk+hum)*env(n, 0.3, 0.3), 126.4, -44, 0, "radio : souffle, craquements et ronflement 50 Hz sous l'annonce")
put(click(0.02, 800, 4000)*2, SH[22][1]-0.05, -34, 0, "radio éteinte : clic (début du silence SH23)")
put(pen(4.5), SH[24][0]+0.8, -41, 0.1, "plume (SH24, écrit — non dit, D8)")
for i in range(6): put(page(0.45), SH[25][0]+0.8+i*1.9, -40, 0.1*(-1)**i)
bed(SH[25][0], SH[25][1], 200, 1200, -49, am_rate=0.5, am_depth=0.7, fade=1.5, name="saisons : vent qui passe (SH25)")
cues.append({"t": SH[25][0], "dur": 12, "cue": "pages du carnet 1953-1955 (SH25)", "gain_db": -40})
put(creak(0.9, 260, 180), SH[26][0]+0.3, -37, 0.4, "fenêtre qui s'ouvre (SH26)"); put(click(0.015, 1500, 5000), SH[26][0]+1.2, -38, 0.4)
drop(murmur(11, 14, 300, 1600))
_y = band2(seg(364, 10, 11.0), 150, 900)*(np.linspace(0, 1, int(11*SR))**2)[:, None]; putS(_y, SH[26][0]+0.5, -38, 0.3, "SH26 : rumeur réelle derrière la fenêtre (Mixkit 364)")
# ===== Scene 5 — Rabat 1955 (175-189.5), intérieurs (189.5-250)
crowd = murmur(16, 30, 300, 2200); n = len(crowd); swell = slow_am(n, 0.4, 0.5)
drop(crowd, swell)
_cw = fades(seg(364, 20, 16.0), 1.0, 0.01); _i0 = int(14.0*SR); _fr = np.arange(len(_cw)-_i0)/(len(_cw)-_i0-1)   # M7c : queue 188,0->190,0 s en (cos²)^0.45 : décroissance lisse, sans creux avant SH29
_cw[_i0:] *= ((np.cos(_fr*np.pi/2)**2)**0.45)[:, None]
putS(_cw, 174.0, -35, 0, "foule réelle, Rabat 1955 (Mixkit 364) — M7c : finit à 190,0 s, queue (cos²)^0.45 188,0–190,0")
drop(murmur(16, 20, 400, 2500)); drop(murmur(16, 20, 400, 2500))
for t in (176.2, 178.9, 181.0): drop(noise(1.2, 500, 3500), rng.uniform(-0.5, 0.5))
putS(fades(band2(seg(462, 0, 6.0), 250, 3200), 0.8, 2.0), 176.0, -44, -0.2, "acclamations réelles atténuées −8 dB, filtrées (Mixkit 462)"); putS(fades(band2(seg(437, 0, 4.5), 250, 3200), 0.6, 1.4), 179.6, -46, 0.3, "ovation réelle atténuée −8 dB, filtrée (Mixkit 437)")
cues.append({"t": 176.2, "dur": 6, "cue": "3 vagues d'acclamations", "gain_db": -37})
bed(189.5, 250, 50, 320, -53, am_rate=0.1, name="intérieur 1955-56: ton de pièce")   # inchangé (tout changement de durée décalerait les tirages aléatoires suivants)
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
st = np.stack([L, Rr], 1); pk = np.abs(st).max(); st = st*1.0
OUT.mkdir(parents=True, exist_ok=True)
assert not (OUT/"ambience_foley_m7c.wav").exists(), "exists"
with wave.open(str(OUT/"ambience_foley_m7c.wav"), "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st, -1, 1)*32767).astype(np.int16).tobytes())
json.dump({"seed": 1956, "rights": "M4.1 synthétique + Mixkit 364/462/437 (Sound Effects Free License, approvals/licenses/SFX_LICENSES.json)", "cues": sorted(cues, key=lambda c: c["t"])}, open(OUT/"cues_m7c.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(cues), "cues")
