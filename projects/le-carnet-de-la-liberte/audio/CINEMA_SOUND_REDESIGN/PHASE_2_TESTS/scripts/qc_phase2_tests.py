#!/usr/bin/env python3
"""QC phase 2 — mesures techniques uniquement (aucune écoute). Écrit qc/QC_PHASE2_MESURES.json ; refuse d'écraser."""
import subprocess, json, re, wave
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; O = R/"audio/CINEMA_SOUND_REDESIGN/PHASE_2_TESTS"; SR = 48000
def rd(p):
    with wave.open(str(p)) as w: assert w.getframerate() == SR and w.getnchannels() == 2; return np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1,2).astype(np.float64)/32768
def ebu(p):
    e = subprocess.run(["ffmpeg","-nostdin","-hide_banner","-i",str(p),"-af","ebur128=peak=true:framelog=quiet","-f","null","-"],capture_output=True,text=True).stderr
    g = lambda k: float(re.findall(k+r":\s+(-?[\d.]+)", e.split("Summary:")[-1])[0])
    return {"I_LUFS": g("I"), "LRA_LU": g("LRA"), "true_peak_dBTP": g("Peak")}
def stmax(p):
    e = subprocess.run(["ffmpeg","-nostdin","-i",str(p),"-af","ebur128=metadata=1,ametadata=mode=print:file=-","-f","null","-"],capture_output=True,text=True).stdout
    v = [float(x) for x in re.findall(r"r128\.S=(-?[\d.]+)", e)]; return round(max(v),1), round(float(np.percentile([x for x in v if x > -70], 10)),1)
def db(x): return 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def mono_loss(x): m = (x[:,0]+x[:,1])/2; return round(db(m)-db(x), 2)       # 0 dB = aucune perte ; négatif = perte en mono
lines = json.load(open(O/"qc/decomposition_lignes.json"))["lines"]
T = {"A_ouverture_carnet": (30.0, 65.0, [(50.5,65.0,"SH10–12 fond sans voix")], [(36.2,37.7),(60.7,65.9),(50.5,65.0)]),
     "B_sequence_1955": (160.0, 190.0, [(175.0,182.0,"SH27 sans voix")], [(164.1,167.3),(166.3,168.9),(182.3,185.0),(175.0,182.0)]),
     "C_generique": (268.0, 299.0, [(276.0,299.0,"générique")], [(274.6,299.0)])}
res = {}
for n,(a,b,mw,mod) in T.items():
    xb = rd(O/n/f"{n}_AVANT.wav"); xa = rd(O/n/f"{n}_APRES.wav"); r = {}
    r["durée_images_25ips"] = [len(xb)/SR*25, len(xa)/SR*25]
    r["crête_échantillon_dBFS"] = [round(20*np.log10(np.abs(xb).max()+1e-12),2), round(20*np.log10(np.abs(xa).max()+1e-12),2)]
    r["échantillons_écrêtés"] = [int((np.abs(xb)>=0.9999).sum()), int((np.abs(xa)>=0.9999).sum())]
    r["sonie_avant"] = ebu(O/n/f"{n}_AVANT.wav"); r["sonie_après"] = ebu(O/n/f"{n}_APRES.wav")
    r["court_terme_max_et_P10_LUFS"] = {"avant": stmax(O/n/f"{n}_AVANT.wav"), "après": stmax(O/n/f"{n}_APRES.wav")}
    # synchro : identité hors zones modifiées (écart nul = aucun décalage ni dérive)
    mask = np.ones(len(xb), bool)
    for s,e in mod: mask[max(0,int((s-a)*SR)-int(0.6*SR)):int((e-a)*SR)+int(1.2*SR)] = False
    r["écart_max_hors_zones_modifiées"] = float(np.abs(xa-xb)[mask].max()) if mask.any() else None
    r["échantillons_identiques_hors_zones_%"] = round(100*float(mask.mean()),1)
    # mono
    r["compat_mono_dB_global"] = [mono_loss(xb), mono_loss(xa)]
    r["compat_mono_fenêtres"] = {lab: [mono_loss(xb[int((s-a)*SR):int((e-a)*SR)]), mono_loss(xa[int((s-a)*SR):int((e-a)*SR)])] for s,e,lab in mw}
    # dialogues : niveau RMS de chaque réplique de la fenêtre, avant/après
    dl = []
    for l in lines:
        if l["in_s"] >= a and l["out_s"] <= b:
            s,e = int((l["in_s"]-a)*SR), int((l["out_s"]-a)*SR); dl.append({"réplique_s": l["in_s"], "avant_dBFS": round(db(xb[s:e]),2), "après_dBFS": round(db(xa[s:e]),2), "écart_dB": round(db(xa[s:e])-db(xb[s:e]),2)})
    r["dialogues"] = dl; res[n] = r
p = O/"qc/QC_PHASE2_MESURES.json"; assert not p.exists(); p.write_text(json.dumps(res, indent=1, ensure_ascii=False)); print(json.dumps(res, indent=1, ensure_ascii=False))
