#!/usr/bin/env python3
"""Phase 2 — trois tests AVANT/APRÈS (sources existantes uniquement, 0 crédit). Refuse d'écraser.
BASE sans perte du master audio = audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav (master AAC = ce WAV, gain 0,9963, retard 0, résidu −29,9 dB = bruit AAC).
Décomposition exacte : mix = g_réplique · DIALOGUE(stem M6, retard 47 éch.) + FOND, où g est estimé réplique par réplique (moindres carrés) et FOND = mix − g·DIALOGUE
(somme exacte par construction : AVANT = DIALOGUE·g + FOND, au bit près aux arrondis flottants). Les dialogues ne sont JAMAIS modifiés (Younes inclus).
Usage : build_phase2_tests.py"""
import subprocess, json, sys, wave
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; SR = 48000
OUT = R/"audio/CINEMA_SOUND_REDESIGN/PHASE_2_TESTS"; MIXW = R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav"; DXS = R/"audio/mixes/M6/stems/dialogue.wav"
SFX = R/"assets/sfx/mixkit"; MUS = R/"assets/music/mixkit/mixkit_599_possible_dreams.mp3"; LAG = 47
def rd(p, n=None):
    x = np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-i",str(p),"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout, "<f4").reshape(-1,2).astype(np.float64)
    if n: y = np.zeros((n,2)); e = min(n,len(x)); y[:e] = x[:e]; return y
    return x
def wr(p, x, bits=16):
    p = Path(p); assert not p.exists(), f"refus d'écraser {p}"
    with wave.open(str(p),"wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(np.round(x*32767),-32768,32767).astype("<i2").tobytes())
def sec(a,b=None): return slice(int(round(a*SR)), None if b is None else int(round(b*SR)))
def ramp(n, kind="cos"): t = np.linspace(0,1,n); return np.sin(t*np.pi/2)**2
def env_gain(n, pts):  # courbe de gain linéaire par morceaux en dB : pts=[(t,dB),...]
    t = np.arange(n)/SR; ts, ds = zip(*pts); return 10**(np.interp(t, ts, ds)/20)
def db(x): return 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def lp(x, fc):  # passe-bas FFT douce (sert à des textures, pas aux voix)
    X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); X[f > fc] *= 0; return np.fft.irfft(X, len(x), axis=0)
def lowpass1(x, fc):  # 1 pôle
    a = np.exp(-2*np.pi*fc/SR); y = np.empty_like(x); s = np.zeros(x.shape[1])
    for i in range(len(x)): s = (1-a)*x[i] + a*s; y[i] = s
    return y
def db_ratio(ref, x): return float(np.sqrt(np.mean(ref**2)/np.mean(x**2)))   # compense la perte d'énergie : même sonie, seule la largeur change
def width(x, k):  # réduction latérale : S×k
    m = (x[:,0]+x[:,1])/2; s = (x[:,0]-x[:,1])/2*k; return np.stack([m+s, m-s], 1)
N = int(276*SR); M = rd(MIXW, N); D = np.roll(rd(DXS, N), LAG, axis=0); D[:LAG] = 0
# --- segmentation des répliques sur l'enveloppe du stem
W = int(0.02*SR); e = np.sqrt(np.convolve(D[:,0]**2, np.ones(W)/W, "same")); act = e > 10**(-48/20); segs = []; on = None; hold = int(0.35*SR)
for k in range(len(act)-1):
    if act[k] and on is None: on = k
    if (not act[k]) and on is not None and not act[k:k+hold].any():
        if (k-on)/SR >= 0.25: segs.append((max(0, on-int(0.05*SR)), min(N, k+int(0.12*SR))))
        on = None
G = np.zeros(N); DX = np.zeros_like(M); lines = []; WL = int(0.12*SR); HP = int(0.02*SR)
def smooth(v, k):
    k = max(1, k) | 1; pad = np.pad(v, (k//2, k//2), mode="edge"); return np.convolve(pad, np.ones(k)/k, "valid")
for a,b in segs:
    xs, ys = D[a:b], M[a:b]; g0 = (xs*ys).sum()/(xs*xs).sum()
    cs = list(range(0, max(1, len(xs)-WL), HP)); gl = []
    for c in cs:
        x = xs[c:c+WL]; y = ys[c:c+WL]; ex = (x*x).sum()
        gl.append((x*y).sum()/ex if ex > 1e-6*WL else np.nan)
    gl = np.array(gl); ok = ~np.isnan(gl)
    gl = np.interp(np.arange(len(gl)), np.nonzero(ok)[0], gl[ok]) if ok.any() else np.full(len(gl), g0)
    gl = np.clip(smooth(gl, 7), 0.5*g0, 2.0*g0); tc = np.array(cs) + WL/2
    gs = np.interp(np.arange(len(xs)), tc, gl); G[a:b] = gs; DX[a:b] = gs[:,None]*xs
    r = ys - DX[a:b]; lines.append({"in_s": round(a/SR,2), "out_s": round(b/SR,2), "g_const": round(float(g0),3), "g_local_min": round(float(gl.min()),3), "g_local_max": round(float(gl.max()),3), "RMS_reste_vs_mix_dB": round(float(db(r)-db(ys)),1)})
BED = M - DX
assert np.abs((DX+BED)-M).max() < 1e-9
(OUT/"qc/decomposition_lignes.json").write_text(json.dumps({"lines": lines, "lag_samples": LAG, "note": "gain LOCAL (fenêtres 120 ms, pas 20 ms, lissé) mixage/stem ; RMS_reste_vs_mix_dB = niveau du FOND dans la réplique par rapport au mix (plus bas = séparation plus nette ; contient aussi le vrai fond)"}, indent=1, ensure_ascii=False))
def gated(x_len, t0, t1, fi, fo): g = np.zeros(x_len); g[sec(t0,t1)] = 1; n = int(fi*SR); m = int(fo*SR); i0 = int(t0*SR); i1 = int(t1*SR); g[i0:i0+n] *= ramp(n); g[i1-m:i1] *= ramp(m)[::-1]; return g
def place(L, src, t0, peak_db, dur=None, fi=0.02, fo=0.2, off=0.0):
    s = src[int(off*SR):] if off else src
    if dur: s = s[:int(dur*SR)]
    s = s/(np.abs(s).max()+1e-12)*10**(peak_db/20); n = len(s); i = int(round(t0*SR)); s = s.copy(); a = int(fi*SR); o = int(fo*SR)
    if a: s[:a] *= ramp(a)[:,None]
    if o: s[-o:] *= ramp(o)[::-1][:,None]
    L[i:i+n] += s[:max(0, len(L)-i)] if i+n > len(L) else s
Z = lambda n: np.zeros((n,2))
# ===== TEST A : 30,0 → 65,0 s (SH07–SH12) =====
A0, A1 = 30.0, 65.0; Ln = N; LA = Z(Ln); log_A = []
cover = rd(SFX/"mixkit_1103_stiff_paper_book_paging.wav"); place(LA, cover, 36.20, -21, dur=1.5, fo=0.3); log_A.append("36,20 s : froissement doux du carnet/de la photo (Mixkit 1103, crête −21 dBFS, 1,5 s) — SH08 gros plan sur la couverture")
breeze = rd(SFX/"mixkit_2427_breeze_through_the_trees.wav"); sw = lowpass1(breeze[:int(7*SR)], 1400)
place(LA, sw, 60.7, -31, dur=5.2, fi=2.6, fo=1.6); log_A.append("60,70–65,90 s : souffle d'air filtré (Mixkit 2427, passe-bas 1,4 kHz, crête −31 dBFS) qui monte vers l'entrée dans l'encre (SH12 61,5 s)")
BEDw = BED.copy(); wA = width(BED[sec(50.5,65.0)], 0.6); wA *= db_ratio(BED[sec(50.5,65.0)], wA); gw = gated(Ln, 50.5, 65.0, 1.0, 1.0)[sec(50.5,65.0)][:,None]; BEDw[sec(50.5,65.0)] = BED[sec(50.5,65.0)]*(1-gw) + wA*gw
log_A.append("50,5–65,0 s : largeur stéréo du fond ramenée à 60 % (corrélation stéréo ~0 → positive), sonie du fond conservée (gain de compensation), fondus de 1 s, aucune voix dans cette fenêtre")
A_after = DX + BEDw + LA
# ===== TEST B : 160,0 → 190,0 s (SH25 fin, SH26–SH28) =====
B0, B1 = 160.0, 190.0; LB = Z(N); log_B = []
birds = rd(SFX/"mixkit_2472_morning_birds.wav"); place(LB, birds, 164.1, -33, dur=3.2, fi=0.8, fo=1.0, off=2.0); log_B.append("164,10–167,30 s : premier chant d'oiseau à l'ouverture de la fenêtre (Mixkit 2472, crête −33 dBFS) — SH26")
BEDb = BED.copy(); LIFT_DB = 1.5; DXb = DX*10**(LIFT_DB/20)
log_B.append("Réplique V1 (166,5 s) et A5 (182,5 s) : composante voix du mix relevée de +1,5 dB (les deux répliques de la fenêtre) ; fond inchangé (la séparation musique/ambiance du mix final n'est pas fiable : abaisser le fond sous la voix n'est donc pas testé)")
wB = width(BEDb[sec(175.0,182.0)], 0.6); wB *= db_ratio(BEDb[sec(175.0,182.0)], wB); gb = gated(N, 175.0, 182.0, 1.0, 1.0)[sec(175.0,182.0)][:,None]; BEDb[sec(175.0,182.0)] = BEDb[sec(175.0,182.0)]*(1-gb) + wB*gb
log_B.append("175,0–182,0 s (SH27, sans voix) : largeur stéréo du fond ramenée à 60 % à sonie conservée, fondus de 1 s")
B_after = DXb + BEDb + LB
# ===== TEST C : 268,0 → 299,0 s (fin SH38 + générique) =====
C0, C1 = 268.0, 299.0; TOT = int(299*SR); C_before = np.zeros((TOT,2)); C_before[:N] = M
tr = rd(MUS); seg_m = tr[:int(26*SR)].copy(); n = len(seg_m)
gC = env_gain(n, [(0,-60),(1.5,-40),(5.0,-33),(10.5,-26),(17.0,-23),(20.5,-23),(23.5,-60),(26,-60)]) if False else None
cur = lambda t: np.interp(t, [0,2.0,6.5,11.5,18.0,21.0,24.4], [-60,-42,-34,-27,-24.5,-24.5,-70])   # dB, t = temps depuis 274,6 s
tt = np.arange(int(24.4*SR))/SR; cm = tr[:len(tt)]*10**(cur(tt)/20)[:,None]; mono_music_avant = float(db((cm[:,0]+cm[:,1])/2)-db(cm)); cm_w = width(cm, 0.6); cm_w *= db_ratio(cm, cm_w); mono_music_apres = float(db((cm_w[:,0]+cm_w[:,1])/2)-db(cm_w)); cm = cm_w
C_after = C_before.copy(); i0 = int(round(274.6*SR)); C_after[i0:i0+len(cm)] += cm[:TOT-i0]
log_C = ["274,6–299,0 s : reprise progressive du thème (Mixkit 599, début de piste = exposition du thème, lue depuis 0 s), entrée sous la fin de MF, montée de −60 à −24,5 dB (re pleine échelle de la piste) jusqu'à ~292,6 s, sortie progressive jusqu'à 299,0 s ; largeur stéréo de la musique ramenée à 60 % à sonie conservée (compatibilité mono)",
         "Aucune voix, aucun texte à l'écran modifié ; cartons 1 (276–282 s), 2 (282–285,5 s), 3 (285,5–299 s)"]
# ===== mesures voix / fond (voix isolée = composante DX, identique avant/après par construction) =====
vf = {"fond_mono_musique_generique_dB": {"avant_traitement_largeur": round(mono_music_avant,2), "apres": round(mono_music_apres,2)}, "lignes": []}
for l in lines:
    a, b = int(l["in_s"]*SR), int(l["out_s"]*SR)
    for nm, (w0, w1, BEDa, DXa) in {"A": (A0, A1, BEDw, DX), "B": (B0, B1, BEDb, DXb)}.items():
        if l["in_s"] >= w0 and l["out_s"] <= w1:
            add = (LA if nm == "A" else LB)[a:b]
            vf["lignes"].append({"test": nm, "réplique_s": l["in_s"], "voix_isolée_dBFS_avant": round(db(DX[a:b]),2), "voix_isolée_dBFS_après": round(db(DXa[a:b]),2), "fond_dBFS_avant": round(db(BED[a:b]),2), "fond_dBFS_après": round(db(BEDa[a:b]+add),2), "rapport_voix_fond_avant_dB": round(db(DX[a:b])-db(BED[a:b]),2), "rapport_voix_fond_après_dB": round(db(DXa[a:b])-db(BEDa[a:b]+add),2), "avertissement": "indicatif : le FOND estimé contient encore des résidus de voix"})
(OUT/"qc/voix_fond.json").write_text(json.dumps(vf, indent=1, ensure_ascii=False))
# ===== couches ajoutées, exportées pour le projet REAPER (FLAC 24 bits, à poser à la position indiquée) =====
def wflac(path, x):
    path = Path(path)
    if path.exists(): path.unlink()           # fichiers dérivés de CE script uniquement
    subprocess.run(["ffmpeg","-nostdin","-v","error","-f","f32le","-ar",str(SR),"-ac","2","-i","-","-c:a","flac","-sample_fmt","s32","-bits_per_raw_sample","24",str(path)], input=x.astype("<f4").tobytes(), check=True)
MED = OUT/"REAPER_PROJECT/media"; MED.mkdir(parents=True, exist_ok=True)
wflac(MED/"PH2_A_foley_air_pos36.00s.flac", LA[sec(36.0,66.0)]); wflac(MED/"PH2_B_oiseau_pos163.90s.flac", LB[sec(163.9,167.6)]); wflac(MED/"PH2_C_musique_generique_pos274.60s.flac", cm)
# ===== exports (WAV 16 bits 48 kHz) =====
def cut(x, a, b): return x[sec(a,b)]
for name, (a,b), bef, aft, lg in [("A_ouverture_carnet",(A0,A1),M, A_after, log_A), ("B_sequence_1955",(B0,B1),M, B_after, log_B), ("C_generique",(C0,C1),C_before, C_after, log_C)]:
    d = OUT/name; xb = cut(bef,a,b); xa = cut(aft,a,b); assert len(xb) == len(xa) == int(round((b-a)*SR))
    wr(d/f"{name}_AVANT.wav", xb); wr(d/f"{name}_APRES.wav", xa)
    gap = np.zeros((int(1.0*SR),2)); beep = 0.0
    wr(d/f"{name}_AB_AVANT_puis_APRES.wav", np.concatenate([xb, gap, xa]))
    (d/"MODIFICATIONS.txt").write_text(f"{name} — fenêtre {a:.2f}–{b:.2f} s du master (début/fin sur des images entières à 25 ips)\n" + "\n".join("- "+z for z in lg) + "\n")
print("ok")
np.save(OUT/"qc/_tmp_dx.npy", DX[:1])  # marqueur de fin
(OUT/"qc/_tmp_dx.npy").unlink()
