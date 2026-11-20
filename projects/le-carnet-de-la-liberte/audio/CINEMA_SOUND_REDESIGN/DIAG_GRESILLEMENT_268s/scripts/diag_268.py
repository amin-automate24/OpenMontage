#!/usr/bin/env python3
"""Diagnostic ciblé du grésillement 268–278 s : mesures par composant (lecture seule). Reproduit la lecture du projet REAPER v2 (volume d'item × enveloppe × fondus).
Mesures uniquement : aucune écoute. Écrit analysis/diag_268_mesures.json (refuse d'écraser)."""
import subprocess, csv, json, wave
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; B = R/"audio/CINEMA_SOUND_REDESIGN"; SR = 48000; T0, T1 = 262.0, 280.0
rd = lambda p, ss=None, t=None: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error"]+(["-ss",str(ss)] if ss is not None else [])+(["-t",str(t)] if t else [])+["-i",str(p),"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def band(x, lo, hi):
    m = x.mean(1); X = np.abs(np.fft.rfft(m*np.hanning(len(m))))**2; f = np.fft.rfftfreq(len(m), 1/SR); sel = (f >= lo) & (f < hi)
    return 10*np.log10(X[sel].sum()/ (len(m)**2) * 8 + 1e-20)
def flat(x, lo=6000, hi=16000):
    m = x.mean(1); X = np.abs(np.fft.rfft(m*np.hanning(len(m))))**2; f = np.fft.rfftfreq(len(m), 1/SR); P = X[(f >= lo) & (f < hi)]+1e-20
    return float(np.exp(np.mean(np.log(P)))/np.mean(P))     # 1 = bruit blanc ; ~0 = tonal/musical
def stats(x):
    r = {}
    for k in range(int(T1-T0)):
        s = x[int(k*SR):int((k+1)*SR)]; t = T0+k
        if len(s) < SR: continue
        r[f"{t:.0f}"] = {"RMS": round(db(s),1), "HF6-16k": round(band(s,6000,16000),1), "planéité_6-16k": round(flat(s),3)}
    return r
# --- sources du projet REAPER v2 (même fenêtre de lecture que les items)
M = B/"REAPER_V2/media"; items = list(csv.DictReader(open(B/"REAPER_V2/manifest/items.csv", encoding="utf-8"))); env = {}
for r in csv.DictReader(open(B/"REAPER_V2/manifest/envelopes.csv", encoding="utf-8")): env.setdefault(r["track"], []).append((float(r["time_s"]), float(r["value_linear"])))
L = int((T1-T0)*SR); t = T0+np.arange(L)/SR; comp = {}
def item_sig(it):
    pos, ln, so = float(it["position_s"]), float(it["length_s"]), float(it["source_offset_s"]); a, b = max(pos, T0), min(pos+ln, T1)
    if b <= a: return np.zeros((L,2))
    x = rd(M/it["file"], so+(a-pos), b-a); y = np.zeros((L,2)); i0 = int((a-T0)*SR); y[i0:i0+len(x)] = x[:L-i0]; y *= 10**(float(it["volume_db"])/20)
    fi, fo = float(it["fade_in_s"]), float(it["fade_out_s"]); g = np.ones(L)
    if fi > 0: g *= np.where(t < pos+fi, np.sin(np.clip((t-pos)/fi,0,1)*np.pi/2)**2, 1)
    if fo > 0: g *= np.where(t > pos+ln-fo, np.cos(np.clip((t-(pos+ln-fo))/fo,0,1)*np.pi/2)**2, 1)
    return y*g[:,None]
tr_of = {"DX":"DX","AMB":"AMB","MUS":"MUS","MUS_ALT":"MUS_ALT","FOL_A":"FOL","FOL_B":"FOL","REF_MIX":"REF","REF_MST":"REF"}
used = {}
for it in items:
    k = tr_of[it["track"]]
    if int(it["mute"]) == 1 and k != "REF": continue
    if k == "REF": continue
    s = item_sig(it)
    if np.abs(s).max() > 0: used.setdefault(k, []).append((it["name"], s, float(it["volume_db"]), it["file"]))
def envcurve(key):
    p = sorted(env.get(key, [])); 
    return np.interp(t, [a for a,_ in p], [v for _,v in p]) if p else np.ones(L)
for k, lst in used.items():
    tot = sum(s for _, s, _, _ in lst); e = envcurve(k) if k in ("DX","AMB","MUS") else np.ones(L); comp[k] = tot*e[:,None]
comp["_items_actifs_dans_268-278"] = {k: [(n, v, f) for n, _, v, f in lst] for k, lst in used.items()}
# --- références
mix = rd(R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav", T0, T1-T0); mst = rd(M/"REF_master_FINAL_audio_part2_150-299s.flac", T0-150, T1-T0)
raw_amb = rd(R/"audio/sfx_m7c/ambience_foley_m7c.wav", T0, T1-T0); raw_dx = rd(R/"audio/mixes/M6/stems/dialogue.wav", T0, T1-T0)
pad = lambda x: np.concatenate([x, np.zeros((L-len(x),2))]) if len(x) < L else x[:L]
mix, mst, raw_amb, raw_dx = pad(mix), pad(mst), pad(raw_amb), pad(raw_dx)
mine_v2 = rd(B/"PHASE_2_TESTS/C_generique/C_generique_APRES_v2.wav"); mine_v2 = np.concatenate([np.zeros((int((268-T0)*SR),2)), mine_v2])[:L]
total = sum(v for k, v in comp.items() if not k.startswith("_"))
out = {"fenêtre_s": [T0, T1], "master_FINAL_audio": stats(mst), "mix_QC2_SON2_sans_perte": stats(mix), "ma_C_generique_APRES_v2.wav": stats(mine_v2), "SOMME_projet_REAPER_simulée": stats(total)}
for k, v in comp.items():
    if not k.startswith("_"): out["bus_"+k] = stats(v)
out["source_brute_AMB_M7c_sans_gain"] = stats(raw_amb); out["source_brute_DX_stem"] = stats(raw_dx)
out["_items_actifs"] = comp["_items_actifs_dans_268-278"]
# enveloppes autour de 268–278
out["enveloppes_valeurs_268-278"] = {k: [(round(a,1), round(v,2)) for a, v in sorted(env.get(k, [])) if 267 <= a <= 279][::5] for k in ("AMB","MUS","DX")}
# différences sommées
out["écart_SOMME_moins_master_RMS_dB_par_s"] = {f"{T0+k:.0f}": round(db((total-mst)[int(k*SR):int((k+1)*SR)]) - db(mst[int(k*SR):int((k+1)*SR)]),1) for k in range(int(T1-T0))}
p = Path(__file__).resolve().parents[1]/"analysis/diag_268_mesures.json"; assert not p.exists(); p.write_text(json.dumps(out, indent=1, ensure_ascii=False))
hdr = f"{'s':>4} | " + " | ".join(f"{n:>20}" for n in ["master", "mix_QC2", "ma v2.wav", "SOMME REAPER", "bus AMB", "bus MUS", "bus DX", "AMB brute"])
print("RMS dBFS / HF6-16k dBFS / planéité(1=bruit blanc)"); print(hdr)
keys = ["master_FINAL_audio","mix_QC2_SON2_sans_perte","ma_C_generique_APRES_v2.wav","SOMME_projet_REAPER_simulée","bus_AMB","bus_MUS","bus_DX","source_brute_AMB_M7c_sans_gain"]
for k in range(5, 16):
    tt = f"{T0+k:.0f}"; row = []
    for kk in keys:
        v = out.get(kk, {}).get(tt); row.append(f"{v['RMS']:>6.1f}/{v['HF6-16k']:>6.1f}/{v['planéité_6-16k']:.2f}" if v else "—".center(20))
    print(f"{tt:>4} | " + " | ".join(f"{x:>20}" for x in row))
print("items actifs :", {k: [(n[:22], v) for n, v, f in lst] for k, lst in out["_items_actifs"].items()})
print("enveloppes :", out["enveloppes_valeurs_268-278"])
