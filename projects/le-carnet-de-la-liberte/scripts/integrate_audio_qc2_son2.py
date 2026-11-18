#!/usr/bin/env python3
"""QC2 SON2 — script d'intégration PRÉPARÉ, NON EXÉCUTÉ (en attente de validation artistique écrite).
Base : QC2 SON1 (SH26–29 intégral, = QC1 ailleurs). Deux zones remplacées, rien d'autre :
  Z1 SH06  : page Mixkit 1105 atténuée de 10 dB (27,83–29,80 s)  -> additif calibré, SANS reprise du gain du loudnorm dynamique de M9T.1
  Z2 SH12 + rue 1944 : brise 2427, oiseaux 2472, pas 1270, fond -2 dB sous A1 (61,55–85,99 s) -> M9T.1 recalé (47 éch.), corrigé du seul écart de gain mesuré
Pas de normalisation globale. Hors zones : identique à SON1 échantillon par échantillon. Nuit 1953 (119–164 s) = QC1 ; 163,5–193 s = SON1.
Usage : python3 scripts/integrate_audio_qc2_son2.py            (analyse seule, n'écrit rien)
        python3 scripts/integrate_audio_qc2_son2.py --execute  (écrit un NOUVEAU WAV + JSON ; refuse d'écraser)"""
import sys, json, wave, hashlib, subprocess, re
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parent.parent; SR = 48000; M = R/"audio/mixes"; EXEC = "--execute" in sys.argv
def rd(p):
    with wave.open(str(p)) as w: assert w.getframerate() == SR and w.getnchannels() == 2; return np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, 2).astype(np.float64)
def wr(p, x):
    assert not Path(p).exists(), f"refuse d'écraser {p}"; Path(p).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(p), "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(np.round(x), -32768, 32767).astype("<i2").tobytes())
def sec(a, b): return slice(int(round(a*SR)), int(round(b*SR)))
def db(x): return 20*np.log10(np.sqrt(np.mean(np.square(x)))/32768 + 1e-12)
def xfade(n): t = np.linspace(0, np.pi/2, n); return np.sin(t)**2, np.cos(t)**2          # (entrée, sortie) complémentaires
S  = rd(M/"QC2_SON1/MIX_276s_QC2_SON1.wav"); Q = rd(M/"M7B.2/MIX_276s_M7B.2.wav"); B = rd(M/"M9T.1/MIX_276s_M9T.1.wav")
Aq = rd(M/"M7B.1_pre/ambience_ducked.wav"); An = rd(M/"M9T_pre/ambience_ducked.wav")
Mq = rd(M/"M7B.1_pre/music_bed_ducked.wav"); Mn = rd(M/"M9T_pre/music_bed_ducked.wav")
F6 = rd(R/"audio/sfx_m6/ambience_foley_m6.wav"); F6a = rd(R/"audio/sfx_m6_att10/ambience_foley_m6.wav")   # F6a = sortie de scripts/sound_design_m6_att10_test.py (page -10 dB), à générer avant (local, gratuit)
D = 47                                           # retard constant M9T.1 vs QC1 (alimiter supplémentaire), mesuré = 79-32
Ba = np.zeros_like(B); Ba[:len(B)-D] = B[D:]; N = min(len(S), len(Q), len(Ba))
Z1 = (27.80, 29.85); Z2 = (61.50, 86.00); XF = int(0.05*SR)                       # zones intérieures ; fondus 50 ms
rep = {"base": "QC2_SON1", "zones": {"Z1_SH06": Z1, "Z2_SH12_rue1944": Z2}}
# --- 1. Vérifications de périmètre (bloquantes) ---
assert np.array_equal(S[:sec(0, 163.5).stop], Q[:sec(0, 163.5).stop]), "SON1 != QC1 avant 163,5 s"
assert np.abs(Mn[:sec(0, 163.5).stop] - Mq[:sec(0, 163.5).stop]).max() == 0, "musique B différente avant 163,5 s"
dA = np.abs(An[:sec(0, 118).stop] - Aq[:sec(0, 118).stop]).max(1); nz = np.nonzero(dA > 0)[0]
segs = np.split(nz, np.nonzero(np.diff(nz) > SR//2)[0]+1); ext = [(s[0]/SR, s[-1]/SR) for s in segs]
rep["ambience_diff_segments_s"] = [(round(a, 2), round(b, 2)) for a, b in ext]
assert len(ext) == 2 and ext[0][0] >= Z1[0] and ext[0][1] <= Z1[1] and ext[1][0] >= Z2[0] and ext[1][1] <= Z2[1], "ambiance modifiée hors zones"   # => 78–86 s : seuls les oiseaux 2472 diffèrent
# --- 2. Z2 : M9T.1 recalé, corrigé du seul écart de gain (loudnorm dynamique) mesuré hors éléments ---
def lowband(x, hi=1500):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/SR); X[f >= hi] = 0; return np.fft.irfft(X, len(x))
def eps_db(a, b): q = lowband(Q[sec(a, b), 0]); x = lowband(Ba[sec(a, b), 0]); return 20*np.log10(np.sqrt(np.mean(x**2))/np.sqrt(np.mean(q**2)))
ea, eb = eps_db(59.0, 61.4), eps_db(86.5, 89.0); rep["eps_db_anchors"] = {"59.0-61.4": round(ea, 3), "86.5-89.0": round(eb, 3)}
assert abs(ea) < 0.3 and abs(eb) < 0.3, "écart de gain inattendu autour de Z2"
a, b = sec(*Z2).start, sec(*Z2).stop; eps = np.interp(np.arange(a, b), [a, b], [ea, eb])
z2 = Ba[a:b]*(10**(-eps/20))[:, None]
# --- 3. Z1 : additif (QC1 + delta ambiance) ; gain calibré sur le niveau VALIDÉ de la page atténuée (-11,4 dBFS), pas sur le gain de M9T.1 ---
a1, b1 = sec(*Z1).start, sec(*Z1).stop; L0 = 32                                  # latence de finition commune QC1 (mesurée)
dAtt = (F6a[a1-L0:b1-L0] - F6[a1-L0:b1-L0])                                        # delta page -10 dB (ambiance) ; env d'ambiance = 1 ici (assert)
assert np.abs(An[sec(27.9, 29.7)] - F6[sec(27.9, 29.7)]).max() < 4, "ducking inattendu en SH06"
dOld = An[a1-L0:b1-L0] - Aq[a1-L0:b1-L0] + dAtt                                    # (page atténuée - ancien whoosh M4.1)
# gain mix/ambiance : régression de (B-Q) sur (An-Aq) retardé, fenêtre de la page, avec dérive epsilon*Q
pk_mix = np.abs(Ba[sec(28.40, 28.50)]).max(); pk_amb = np.abs(An[sec(28.40, 28.50).start-L0:sec(28.40, 28.50).stop-L0]).max(); G0 = pk_mix/pk_amb   # rapport crête mix M9T.1 / crête ambiance (la régression est faussée par la dérive du loudnorm)
assert 5 < G0 < 20, f"gain mix/ambiance inattendu {G0}"
rep["z1_fit"] = {"G_M9T1": float(G0), "G_dB": float(20*np.log10(abs(G0))), "note": "regression monoregresseur"}
def z1_with(G): return Q[a1:b1] + G*dOld
lo, hi = 0.5*G0, 2.0*G0; G1 = G0
for _ in range(40):                                                               # bissection : crête 28,40–28,50 s = -11,4 dBFS (niveau validé)
    mid = (lo+hi)/2; pk = 20*np.log10(np.abs(z1_with(mid)[sec(28.40, 28.50).start-a1:sec(28.40, 28.50).stop-a1]).max()/32768)
    lo, hi = (mid, hi) if pk < -11.4 else (lo, mid); G1 = mid
z1 = z1_with(G1); rep["z1_gain"] = {"G1": float(G1), "G1_vs_G_M9T1_dB": float(20*np.log10(G1/G0))}
# --- 4. Assemblage : SON1 + zones, fondus complémentaires cos²/sin² de 50 ms aux bords uniquement ---
O = S[:N].copy()
for (za, zb, z) in ((a1, b1, z1), (a, b, z2)):
    w = np.ones(zb-za); fi, fo = xfade(XF); w[:XF] = fi; w[-XF:] = fo; O[za:zb] = S[za:zb]*(1-w)[:, None] + z*w[:, None]
# --- 5. Contrôles (bloquants) ---
outside = np.ones(N, bool); outside[a1:b1] = False; outside[a:b] = False
assert np.array_equal(O[outside], S[:N][outside]), "modification hors zones"
rep["voix_A1_71-74_stem"] = "dialogue.wav inchangé (non touché) ; musique B inchangée (assert premaster)"
rep["pic_page_28.4-28.5_dBFS"] = round(float(20*np.log10(np.abs(O[sec(28.40, 28.50)]).max()/32768)), 2)
for nm, (u, v) in {"jonction_27.80": (27.7, 27.9), "jonction_29.85": (29.8, 29.95), "jonction_61.50": (61.4, 61.6), "jonction_86.00": (85.9, 86.1)}.items():
    rep[nm+"_max_saut_ech"] = float(np.abs(np.diff(O[sec(u, v), 0])).max())
rep["rms_dBFS_hors_zone_diff_vs_SON1"] = round(float(db(O[outside] - S[:N][outside])), 1) if outside.any() else None
print(json.dumps(rep, indent=1, ensure_ascii=False))
if EXEC:
    out = M/"QC2_SON2/MIX_276s_QC2_SON2.wav"; wr(out, O); rep["sha256"] = hashlib.sha256(out.read_bytes()).hexdigest()
    (M/"QC2_SON2/MIX_276s_QC2_SON2.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False)); print("écrit", out)
else: print("ANALYSE SEULE : rien écrit. Ajouter --execute après validation artistique écrite.")
