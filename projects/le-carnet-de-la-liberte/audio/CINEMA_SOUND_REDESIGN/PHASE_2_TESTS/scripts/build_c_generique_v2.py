#!/usr/bin/env python3
"""Générique v2 — reprise musicale audible et progressive, sources existantes uniquement (Mixkit 599), 0 crédit. Refuse d'écraser (v1 conservée).
Principe : (1) la fin de piste (offset 135,21 → 159,31 s) est calée pour que sa décroissance propre tombe sur 299,0 s ; (2) enveloppe de gain « cible » par segment
(niveau RMS visé, rampe d'entrée de 2,7 s depuis la fin de MF, plateau sur les cartons 1–2, descente lente sur le carton 3), et non gain uniforme ;
(3) largeur stéréo 60 % à sonie conservée (compatibilité mono) ; (4) dernier fondu cosinus de 1,6 s pour atteindre zéro sans coupure. AVANT = mix 276 s + silence."""
import subprocess, json, wave
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; SR = 48000; O = R/"audio/CINEMA_SOUND_REDESIGN/PHASE_2_TESTS/C_generique"
rd = lambda p: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-i",str(p),"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
def wr(p, x):
    p = Path(p); assert not p.exists(), f"refus d'écraser {p}"
    with wave.open(str(p),"wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(np.round(x*32767),-32768,32767).astype("<i2").tobytes())
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
N = int(276*SR); TOT = int(299*SR)
M = rd(R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav")[:N]; before = np.zeros((TOT,2)); before[:N] = M
tr = rd(R/"assets/music/mixkit/mixkit_599_possible_dreams.mp3"); T_END = len(tr)/SR
E_BODY = 144.7                       # fin du CORPS de la piste : sa propre décroissance d'éditeur commence à ~144,8 s (mesuré) et n'est pas utilisée
def shape_db(tf, variant):
    """Enveloppe RELATIVE (dB, 0 = plateau). Les micro-dynamiques de la musique sont conservées (gain lent, pas d'aplatissement)."""
    if variant == "v2":     # fondu enchaîné avec la queue de MF (qui s'éteint de 273 à 276 s)
        pts_t = [273.0, 274.0, 275.0, 276.0, 277.0, 278.0, 288.0, 294.0, 297.5, 299.0]
        pts_d = [-30.0, -19.0, -11.0, -5.5, -2.0, 0.0, 0.0, -5.5, -14.5, -24.5]
    else:                   # v2b : « respiration » d'environ 1 s après MF, entrée à 275,0 s
        pts_t = [275.0, 276.0, 277.0, 278.0, 279.0, 288.0, 294.0, 297.5, 299.0]
        pts_d = [-34.0, -17.0, -8.0, -3.0, 0.0, 0.0, -5.5, -14.5, -24.5]
    return np.interp(tf, pts_t, pts_d)
PLATEAU_DB = -21.5                  # niveau RMS visé (dBFS) du plateau, MF à ~−17 dBFS dans le mix : audible sur téléphone, sous les cartons lisibles
def make(variant, T_IN):
    n = int(round((299.0-T_IN)*SR)); off = E_BODY-(299.0-T_IN); seg = tr[int(round(off*SR)):int(round(off*SR))+n].copy(); assert len(seg) == n
    ref = db(seg[int(round((279.0-T_IN)*SR)):int(round((288.0-T_IN)*SR))]); g0 = PLATEAU_DB-ref            # gain statique calé sur le plateau
    tf = T_IN + np.arange(n)/SR; g = 10**((g0+shape_db(tf, variant))/20); music = seg*g[:,None]
    m_ = (music[:,0]+music[:,1])/2; s_ = (music[:,0]-music[:,1])/2; w = np.stack([m_+0.6*s_, m_-0.6*s_], 1); w *= np.sqrt(np.mean(music**2)/np.mean(w**2)); music = w
    f = int(0.9*SR); music[-f:] *= (np.cos(np.linspace(0,np.pi/2,f))**2)[:,None]                           # dernier fondu court : le niveau y est déjà à ~−46 dBFS
    a = int(0.8*SR); music[:a] *= (np.sin(np.linspace(0,np.pi/2,a))**2)[:,None]
    out = before.copy(); i0 = int(round(T_IN*SR)); out[i0:i0+n] += music; return out, off, g0
after, OFF, G0 = make("v2", 273.0); alt, OFF_B, G0B = make("v2b", 275.0); T_IN = 273.0
peak = max(float(np.abs(after[int(268*SR):]).max()), float(np.abs(alt[int(268*SR):]).max()))
# vérifications internes
rms_s = [round(db(after[int(t*SR):int((t+1)*SR)]),1) for t in range(268,299)]
rms_b = [round(db(alt[int(t*SR):int((t+1)*SR)]),1) for t in range(268,299)]
step = lambda r: round(max(abs(r[i+1]-r[i]) for i in range(len(r)-1) if r[i+1] > -90 and r[i] > -90), 1)
w268 = slice(int(268*SR), TOT); xb = before[w268]; xa = after[w268]
assert len(xb) == len(xa) == 31*SR
wr(O/"C_generique_APRES_v2.wav", xa)
def flac_layer(path, x):
    path = Path(path); path.unlink(missing_ok=True)
    subprocess.run(["ffmpeg","-nostdin","-v","error","-f","f32le","-ar",str(SR),"-ac","2","-i","-","-c:a","flac","-sample_fmt","s32","-bits_per_raw_sample","24",str(path)], input=x.astype("<f4").tobytes(), check=True)
MED = R/"audio/CINEMA_SOUND_REDESIGN/REAPER_V2/media"; MED.mkdir(parents=True, exist_ok=True)
flac_layer(MED/"PH2_C_generique_v2_pos273.00s.flac", (after-before)[int(273.0*SR):TOT]); flac_layer(MED/"PH2_C_generique_v2b_pos275.00s.flac", (alt-before)[int(275.0*SR):TOT])
xalt = alt[w268]; wr(O/"C_generique_APRES_v2b_respiration.wav", xalt)
wr(O/"C_generique_AB_AVANT_puis_APRES_v2.wav", np.concatenate([xb, np.zeros((SR,2)), xa]))
v1 = rd(O/"C_generique_APRES.wav")  # v1 conservée, intacte
wr(O/"C_generique_COMPARAISON_AVANT_v1_v2.wav", np.concatenate([xb, np.zeros((SR,2)), v1, np.zeros((SR,2)), xa]))
(O/"MODIFICATIONS_v2.txt").write_text("C_generique_APRES_v2 — fenêtre 268,00–299,00 s (775 images)\n"
 f"- Musique : Mixkit 599, CORPS de piste (offset {OFF:.2f}→{E_BODY:.2f} s, avant la décroissance d'éditeur de la piste, mesurée dès 144,8 s) ; entrée à 273,0 s en fondu enchaîné avec la queue de MF (qui s'éteint de 273 à 276 s)\n"
 f"- Gain statique calé pour un plateau à {PLATEAU_DB} dBFS RMS sur 279–288 s (MF dans le mix : ≈ −17 dBFS) ; enveloppe lente : montée 273→278 s, plateau 278–288 s sur les cartons 1 et 2 (carton 3 dès 285,5 s), descente continue 288→299 s (−5,5 dB à 294 s, −14,5 dB à 297,5 s, −24,5 dB à 299 s) ; dynamiques internes de la musique conservées\n"
 "- Stéréo 60 % à sonie conservée ; fondu d'entrée 0,8 s ; fondu final 0,9 s déjà à bas niveau (aucune coupure)\n"
 "- v2b_respiration : même musique, entrée à 275,0 s (≈ 1 s de respiration après MF) au lieu d'un fondu enchaîné\n"
 "- v1 (C_generique_APRES.wav) conservée à l'identique ; aucun son généré ; l'image n'est pas modifiée\n", encoding="utf-8")
json.dump({"offset_piste_s": round(OFF,3), "fin_corps_piste_s": E_BODY, "entrée_film_s": T_IN, "gain_statique_dB": round(G0,2), "crête_dBFS": round(20*np.log10(peak),2), "RMS_par_seconde_268_299_dBFS_v2": rms_s, "RMS_par_seconde_268_299_dBFS_v2b": rms_b, "plus_grand_saut_RMS_dB_par_s": {"v2": step(rms_s), "v2b": step(rms_b)}}, open(O.parent/"qc/generique_v2_enveloppe.json","w"), indent=1)
print("v2 RMS/s", rms_s); print("v2b RMS/s", rms_b); print("saut max v2", step(rms_s), "| v2b", step(rms_b), "dB/s ; crête", round(20*np.log10(peak),2), "dBFS")
