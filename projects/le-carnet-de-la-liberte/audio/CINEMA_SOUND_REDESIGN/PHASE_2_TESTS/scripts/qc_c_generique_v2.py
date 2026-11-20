#!/usr/bin/env python3
"""QC générique — v1 vs v2 vs v2b : mesures uniquement (aucune écoute). Écrit qc/QC_C_GENERIQUE_V2.json ; refuse d'écraser."""
import subprocess, re, json, wave
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; O = R/"audio/CINEMA_SOUND_REDESIGN/PHASE_2_TESTS"; SR = 48000
rd = lambda p: (lambda w: np.frombuffer(w.readframes(w.getnframes()),"<i2").reshape(-1,2).astype(np.float64)/32768)(wave.open(str(p)))
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def eb(p):
    o = subprocess.run(["ffmpeg","-nostdin","-hide_banner","-i",str(p),"-af","ebur128=peak=true:metadata=1,ametadata=mode=print:file=-","-f","null","-"],capture_output=True,text=True)
    S = [float(x) for x in re.findall(r"r128\.S=(-?[\d.]+)", o.stdout)]; summ = o.stderr.split("Summary:")[-1]
    g = lambda k: float(re.findall(k+r":\s+(-?[\d.]+)", summ)[0]); return S, {"I_LUFS": g("I"), "LRA_LU": g("LRA"), "TP_dBTP": g("Peak")}
res = {}
files = {"AVANT": "C_generique_AVANT.wav", "v1": "C_generique_APRES.wav", "v2": "C_generique_APRES_v2.wav", "v2b": "C_generique_APRES_v2b_respiration.wav"}
base = rd(O/"C_generique"/files["AVANT"])
for k, f in files.items():
    x = rd(O/"C_generique"/f); S, g = eb(O/"C_generique"/f); S = np.array(S); t = np.arange(len(S))*0.1+268.0
    sel = lambda a, b: S[(t >= a) & (t < b)]
    r = dict(g); r["crête_échantillon_dBFS"] = round(20*np.log10(np.abs(x).max()),2); r["échantillons_écrêtés"] = int((np.abs(x) >= 0.9999).sum()); r["images_25ips"] = len(x)/SR*25
    r["court_terme_LUFS"] = {"carton1_276-282_min/max": [round(float(sel(277,282).min()),1), round(float(sel(277,282).max()),1)], "carton2_282-285.5_min/max": [round(float(sel(282,285.4).min()),1), round(float(sel(282,285.4).max()),1)], "carton3_285.5-295_min/max": [round(float(sel(285.5,295).min()),1), round(float(sel(285.5,295).max()),1)], "296-298_min": round(float(sel(296,298).min()),1)}
    add = x - base; r["ajout_seul_RMS_dBFS_277-295"] = round(db(add[int(9*SR):int(27*SR)]),1) if k != "AVANT" else None
    r["ajout_seul_perte_mono_dB"] = round(db((add[:,0]+add[:,1])/2) - db(add), 2) if k != "AVANT" else None
    rs = [db(x[int(j*SR):int((j+1)*SR)]) for j in range(31)]
    jumps = [abs(rs[j+1]-rs[j]) for j in range(8,30) if rs[j+1] > -90 and rs[j] > -90]
    r["plus_grand_saut_RMS_dB_par_s_apres_276"] = round(max(jumps), 1) if jumps else 0.0
    fr = np.sqrt(np.mean(x[:len(x)//4800*4800].mean(1).reshape(-1,4800)**2,1)); sil = [round(i*0.1+268,1) for i in np.nonzero(20*np.log10(fr+1e-12) < -60)[0]]; r["blocs_100ms_sous_-60dBFS"] = (sil[0], sil[-1], len(sil)) if sil else None
    r["identique_à_AVANT_avant_272.9_s"] = bool(np.abs((x-base)[:int(4.9*SR)]).max() == 0.0)
    res[k] = r
p = O/"qc/QC_C_GENERIQUE_V2.json"; assert not p.exists(); p.write_text(json.dumps(res, indent=1, ensure_ascii=False))
for k, r in res.items(): print(k, r["I_LUFS"], "LUFS | TP", r["TP_dBTP"], "| LRA", r["LRA_LU"], "| ST", r["court_terme_LUFS"], "| ajout RMS", r["ajout_seul_RMS_dBFS_277-295"], "| mono", r["ajout_seul_perte_mono_dB"], "| saut", r["plus_grand_saut_RMS_dB_par_s_apres_276"], "| silences", r["blocs_100ms_sous_-60dBFS"], "| clip", r["échantillons_écrêtés"], "| identique<272.9", r["identique_à_AVANT_avant_272.9_s"])
