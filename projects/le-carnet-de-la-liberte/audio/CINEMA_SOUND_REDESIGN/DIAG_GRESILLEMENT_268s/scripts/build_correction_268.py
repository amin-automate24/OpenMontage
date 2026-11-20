#!/usr/bin/env python3
"""Correction MINIMALE du crépitement de 268–270,3 s, sur copie de travail uniquement (le master FINAL et le projet v2 d'origine ne sont pas modifiés).
Cause mesurée : bruitage de synthèse « plume » (sound_design_m4.py, pen(2.6) à 267,7 s) porté par la piste AMB, déjà présent dans le master.
Correction : creux de −20 dB sur l'ENVELOPPE DE VOLUME de la piste AMB entre 267,45 et 270,65 s (rampes cosinus 0,2/0,3 s), rien d'autre (ni DX, ni MUS, ni filtre, ni réduction de bruit générale).
Produit : 268–278 s (250 images) — MASTER original / AVANT (reconstruction REAPER simulée) / APRÈS ; + envelopes_correction_268.csv pour REAPER. Refuse d'écraser."""
import subprocess, csv, json, wave
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; B = R/"audio/CINEMA_SOUND_REDESIGN"; D = B/"DIAG_GRESILLEMENT_268s"; M = B/"REAPER_V2/media"; SR = 48000; T0, T1 = 262.0, 280.0
rd = lambda p, ss=None, t=None: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error"]+(["-ss",str(ss)] if ss is not None else [])+(["-t",str(t)] if t else [])+["-i",str(p),"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def wr(p, x):
    p = Path(p); assert not p.exists(), f"refus d'écraser {p}"
    with wave.open(str(p),"wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(np.round(x*32767),-32768,32767).astype("<i2").tobytes())
L = int((T1-T0)*SR); t = T0+np.arange(L)/SR
items = list(csv.DictReader(open(B/"REAPER_V2/manifest/items.csv", encoding="utf-8"))); env = {}
for r in csv.DictReader(open(B/"REAPER_V2/manifest/envelopes.csv", encoding="utf-8")): env.setdefault(r["track"], []).append((float(r["time_s"]), float(r["value_linear"])))
def item_sig(it):
    pos, ln, so = float(it["position_s"]), float(it["length_s"]), float(it["source_offset_s"]); a, b = max(pos, T0), min(pos+ln, T1)
    if b <= a: return np.zeros((L,2))
    x = rd(M/it["file"], so+(a-pos), b-a); y = np.zeros((L,2)); i0 = int((a-T0)*SR); y[i0:i0+len(x)] = x[:L-i0]; y *= 10**(float(it["volume_db"])/20)
    fi, fo = float(it["fade_in_s"]), float(it["fade_out_s"]); g = np.ones(L)
    if fi > 0: g *= np.where(t < pos+fi, np.sin(np.clip((t-pos)/fi,0,1)*np.pi/2)**2, 1)
    if fo > 0: g *= np.where(t > pos+ln-fo, np.cos(np.clip((t-(pos+ln-fo))/fo,0,1)*np.pi/2)**2, 1)
    return y*g[:,None]
comp = {}
for it in items:
    k = it["track"]
    if int(it["mute"]) == 1 or k.startswith("REF") or k not in ("DX","AMB","MUS"): continue
    comp[k] = comp.get(k, 0) + item_sig(it)
curve = lambda k: (lambda p: np.interp(t, [a for a,_ in p], [v for _,v in p]))(sorted(env[k]))
for k in comp: comp[k] = comp[k]*curve(k)[:,None]
# creux minimal sur AMB
def dip(t, a0=267.45, a1=267.65, b0=270.35, b1=270.65, depth=-20.0):
    g = np.zeros_like(t); up = (t >= a0) & (t < a1); hold = (t >= a1) & (t <= b0); dn = (t > b0) & (t <= b1)
    g[up] = depth*np.sin((t[up]-a0)/(a1-a0)*np.pi/2)**2; g[hold] = depth; g[dn] = depth*np.cos((t[dn]-b0)/(b1-b0)*np.pi/2)**2; return 10**(g/20)
GD = dip(t)
before = sum(comp.values()); after = before - comp["AMB"] + comp["AMB"]*GD[:,None]
mst = rd(M/"REF_master_FINAL_audio_part2_150-299s.flac", T0-150, T1-T0)
def cut(x): return x[int((268.0-T0)*SR):int((278.0-T0)*SR)]
w268 = {"MASTER": cut(mst), "AVANT": cut(before), "APRES": cut(after)}
(D/"audio").mkdir(exist_ok=True)
wr(D/"audio/268-278_MASTER_original.wav", w268["MASTER"]); wr(D/"audio/268-278_AVANT_projet_REAPER_simule.wav", w268["AVANT"]); wr(D/"audio/268-278_APRES_correction_plume.wav", w268["APRES"])
g = np.zeros((SR,2)); wr(D/"audio/268-278_AB_master_avant_apres.wav", np.concatenate([w268["MASTER"], g, w268["AVANT"], g, w268["APRES"]]))
# enveloppe corrigée pour REAPER : points d'AMB existants × creux, + points de rampe
pts = sorted(env["AMB"]); extra = [267.45, 267.55, 267.65, 270.35, 270.5, 270.65]
allt = sorted(set([a for a,_ in pts] + extra)); vals = np.interp(allt, [a for a,_ in pts], [v for _,v in pts]) * dip(np.array(allt))
with open(D/"../REAPER_V2/manifest/envelopes_correction_268.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["track","time_s","value_linear"]); [w.writerow(["AMB", f"{a:.4f}", f"{min(v,1.98):.4f}"]) for a, v in zip(allt, vals)]
# ===== mesures =====
def hf(x, lo=4000, hi=24000):
    X = np.fft.rfft(x.mean(1)); f = np.fft.rfftfreq(len(x), 1/SR); X[(f < lo) | (f >= hi)] = 0; return np.fft.irfft(X, len(x))
res = {"creux_dB": -20.0, "bornes_s": [267.45, 270.65]}
for n, x in w268.items():
    h = hf(x); r = {"HF>4k_par_0.5s_dBFS": [round(db(h[int(k*0.5*SR):int((k+1)*0.5*SR)]),1) for k in range(20)], "RMS_268-273_dBFS": round(db(x[:5*SR]),1), "crête_dBFS": round(20*np.log10(np.abs(x).max()),2), "écrêtés": int((np.abs(x) >= 0.9999).sum()),
         "perte_mono_dB_268-273": round(db((x[:5*SR,0]+x[:5*SR,1])/2)-db(x[:5*SR]),2)}
    res[n] = r
diff = w268["APRES"]-w268["AVANT"]; out = np.ones(len(diff), bool); out[int((267.4-268.0)*SR) if False else 0:int((270.7-268.0)*SR)] = False
res["APRES_moins_AVANT_hors_[268;270.7]_écart_max"] = float(np.abs(diff[out]).max())
res["APRES_moins_AVANT_dans_la_zone_RMS_dBFS"] = round(db(diff[:int(2.7*SR)]),1)
res["écart_AVANT_vs_MASTER_RMS_dB_268-273"] = round(db((w268["AVANT"]-w268["MASTER"])[:5*SR]) - db(w268["MASTER"][:5*SR]),1)
# autres bruitages « plume » de synthèse dans le master (mesure seulement, non corrigés)
for nm, a, b in [("plume SH19", 109.6, 114.6), ("plume SH24 (début, 146,3-149,9)", 146.3, 149.9), ("plume SH37 (cette fenêtre)", 267.7, 270.3)]:
    x = rd(M/"REF_master_FINAL_audio_part1_0-150s.flac" if b < 150 else M/"REF_master_FINAL_audio_part2_150-299s.flac", (a if b < 150 else a-150), b-a); h = hf(x)
    base = rd(M/"REF_master_FINAL_audio_part1_0-150s.flac" if b < 150 else M/"REF_master_FINAL_audio_part2_150-299s.flac", ((a-3) if b < 150 else a-153), 2.5); res.setdefault("autres_plumes_master_HF>4k_dBFS", {})[nm] = {"pendant": round(db(h),1), "2,5 s avant": round(db(hf(base)),1)}
(D/"analysis/correction_268_mesures.json").write_text(json.dumps(res, indent=1, ensure_ascii=False)); print(json.dumps(res, indent=1, ensure_ascii=False))
