#!/usr/bin/env python3
"""Phase 1 — mesures (lecture seule) de la bande-son du master CINÉMA FINAL et des stems existants.
Aucune écriture hors audio/CINEMA_SOUND_REDESIGN/analysis/. Refuse d'écraser. Mesures numériques uniquement (aucune écoute)."""
import subprocess, json, re, wave, sys
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[3]; OUT = R/"audio/CINEMA_SOUND_REDESIGN/analysis"; SR = 48000
MP4 = R/"deliverables/FINAL_CINEMA/LE_CARNET_DE_LA_LIBERTE_CINEMA_FINAL_1080p.mp4"
def rd_wav(p):
    with wave.open(str(p)) as w: assert w.getframerate() == SR; n = w.getnchannels(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, n).astype(np.float64)/32768
    return x
def db(x): return 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
tmp = OUT/"master_audio_decoded.wav"
if not tmp.exists(): subprocess.run(["ffmpeg","-nostdin","-v","error","-i",str(MP4),"-vn","-c:a","pcm_s16le",str(tmp)],check=True)
M = rd_wav(tmp); N = len(M)
# loudness M/S par 100 ms (ebur128)
e = subprocess.run(["ffmpeg","-nostdin","-hide_banner","-i",str(MP4),"-vn","-af","ebur128=framelog=verbose","-f","null","-"],capture_output=True,text=True).stderr
rows = [(float(m.group(1)),float(m.group(2)),float(m.group(3))) for m in re.finditer(r"t:\s*([\d.]+)\s+TARGET:.*?M:\s*(-?[\d.]+|-inf)\s+S:\s*(-?[\d.]+|-inf)", e) if True] if False else []
for m in re.finditer(r"t:\s*([\d.]+)\s+TARGET:\S+\s+LUFS\s+M:\s*(-?[\d.]+)\s+S:\s*(-?[\d.]+)", e): rows.append((float(m.group(1)),float(m.group(2)),float(m.group(3))))
S_by_s = {}
for t,m_,s_ in rows:
    k = int(t)
    if s_ > -70: S_by_s[k] = s_
# dialogues : détection par enveloppe sur le stem dialogue (276 s)
D = rd_wav(R/"audio/stems/dialogue.wav").mean(1); W = int(0.02*SR); env = np.sqrt(np.convolve(D**2, np.ones(W)/W, "same")); thr = 10**(-48/20)
act = env > thr; idx = np.nonzero(np.diff(act.astype(int)))[0]
st = list(idx[::2]) if act[0] == 0 else [0]+list(idx[::2]); 
segs = []; i = 0; on = None
for k in range(0, len(act)-1):
    if act[k] and on is None: on = k
    if (not act[k]) and on is not None:
        # fermeture seulement après 0.35 s de silence
        if not act[k:k+int(0.35*SR)].any(): segs.append((on, k)); on = None
lines = []
for a, b in segs:
    if (b-a)/SR < 0.25: continue
    x = D[a:b]; lines.append({"in_s":round(a/SR,2),"out_s":round(b/SR,2),"dur_s":round((b-a)/SR,2),"rms_dBFS":round(db(x),1),"peak_dBFS":round(20*np.log10(np.abs(x).max()+1e-12),1)})
# ambiance+musique (hors dialogue) et mix par plan
AM = rd_wav(R/"audio/stems/ambience_music_ducked.wav")
import csv
shots = list(csv.DictReader(open(R/"shotlist/shot_list.csv")))
per = []
for r in shots:
    a, b = float(r["start_s"]), float(r["start_s"])+float(r["dur_s"]); sl = slice(int(a*SR), min(int(b*SR), N))
    ss = [S_by_s[k] for k in range(int(a), int(b)) if k in S_by_s]
    xm = M[sl]; xa = AM[sl] if len(AM) >= sl.stop else AM[sl]
    corr = float(np.corrcoef(xm[:,0], xm[:,1])[0,1]) if xm[:,0].std() > 0 and xm[:,1].std() > 0 else None
    per.append({"shot":r["id"],"in_s":a,"out_s":round(b,2),"has_dialogue":bool(r["dialogue"]),"mix_rms_dBFS":round(db(xm),1),"bed_rms_dBFS(ambiance+musique)":round(db(xa),1),"short_term_LUFS_min":min(ss) if ss else None,"short_term_LUFS_max":max(ss) if ss else None,"stereo_corr":None if corr is None else round(corr,2)})
# silences (< -60 dBFS RMS sur 100 ms) dans le mix final
w = int(0.1*SR); fr = np.sqrt(np.mean(M[:len(M)//w*w].mean(1).reshape(-1, w)**2, 1)); sil = np.nonzero(db_ := 20*np.log10(fr+1e-12) < -60)[0]
runs = []; 
for k in sil:
    if runs and k == runs[-1][1]+1: runs[-1][1] = k
    else: runs.append([k, k])
silences = [{"in_s":round(a*0.1,1),"out_s":round((b+1)*0.1,1)} for a,b in runs if (b-a+1) >= 3]
# bandes spectrales globales + crêtes + stéréo
X = np.fft.rfft(M.mean(1)); f = np.fft.rfftfreq(N, 1/SR); P = np.abs(X)**2; tot = P.sum()
bands = {n: round(10*np.log10(P[(f>=lo)&(f<hi)].sum()/tot+1e-12),1) for n,(lo,hi) in {"<100Hz":(0,100),"100-500":(100,500),"500-2k":(500,2000),"2k-6k":(2000,6000),">6k":(6000,24000)}.items()}
res = {"file":str(MP4.relative_to(R)),"duration_s":round(N/SR,3),"sample_peak_dBFS":round(20*np.log10(np.abs(M).max()),2),"clipped_samples":int((np.abs(M)>=0.9999).sum()),"stereo_corr_global":round(float(np.corrcoef(M[:,0],M[:,1])[0,1]),3),"band_energy_dB_rel":bands,"dialogue_lines_detected":len(lines),"dialogue_lines":lines,"per_shot":per,"silences_lt_-60dBFS_ge_0.3s":silences,"ebur128_tail":e.strip().splitlines()[-14:]}
p = OUT/"mesures_master_audio.json"; assert not p.exists(), "refuse d'écraser"; p.write_text(json.dumps(res, ensure_ascii=False, indent=1))
print(json.dumps({k:v for k,v in res.items() if k not in ("dialogue_lines","per_shot","ebur128_tail")}, ensure_ascii=False, indent=1))
print("lignes:", len(lines)); [print(l) for l in lines]
[print(p_["shot"],p_["in_s"],p_["mix_rms_dBFS"],p_["bed_rms_dBFS(ambiance+musique)"],p_["short_term_LUFS_min"],p_["short_term_LUFS_max"],p_["stereo_corr"],"D" if p_["has_dialogue"] else "") for p_ in per]
