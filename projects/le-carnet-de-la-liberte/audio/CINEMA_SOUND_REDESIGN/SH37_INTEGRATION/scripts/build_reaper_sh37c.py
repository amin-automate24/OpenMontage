#!/usr/bin/env python3
"""Intégration SH37 version C dans une COPIE DE TRAVAIL du projet REAPER v2 — sans modifier ni écraser aucun fichier existant (nouveaux fichiers uniquement) :
  media/PH3_SH37_AMB_selectif_delta_pos267.00s.flac   couche « delta » : lue avec la piste AMB, elle retire seulement la bande > 2,1 kHz de l'ambiance entre 267,45 et 270,50 s
  media/SH37_plume_reelle_mixkit_2369.wav              copie du média Mixkit (4 items de plume réelle sur une nouvelle piste FOL)
  LE_CARNET_SOUND_V2_SH37C.RPP                         copie du .RPP v2 + 2 pistes nouvelles ; manifest_sh37c/ ; scripts/08 (activer) et 09 (retour immédiat)
Simule aussi la lecture REAPER de 265 à 275 s (avant / après) pour vérifier l'arithmétique d'intégration. Refuse d'écraser."""
import subprocess, csv, json, re, shutil, wave
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[4]; B = R/"audio/CINEMA_SOUND_REDESIGN"; V2 = B/"REAPER_V2"; M = V2/"media"; D = B/"SH37_INTEGRATION"; SR = 48000; T0, T1 = 262.0, 280.0
rd = lambda p, ss=None, t=None, sr=SR: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error"]+(["-ss",str(ss)] if ss is not None else [])+(["-t",str(t)] if t else [])+["-i",str(p),"-f","f32le","-ac","2","-ar",str(sr),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
def wr(p, x):
    p = Path(p); assert not p.exists(), f"refus d'écraser {p}"
    with wave.open(str(p),"wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(np.round(x*32767),-32768,32767).astype("<i2").tobytes())
def bp(x, lo, hi): X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); X[(f < lo) | (f >= hi)] = 0; return np.fft.irfft(X, len(x), axis=0)
def lowsplit(x, f1=1800.0, f2=2100.0):
    X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1/SR); h = np.where(f <= f1, 1.0, np.where(f >= f2, 0.0, np.cos((f-f1)/(f2-f1)*np.pi/2)**2)); return np.fft.irfft(X*h[:,None], len(x), axis=0)
L = int((T1-T0)*SR); t = T0+np.arange(L)/SR
items = list(csv.DictReader(open(V2/"manifest/items.csv", encoding="utf-8"))); env = {}
for r in csv.DictReader(open(V2/"manifest/envelopes.csv", encoding="utf-8")): env.setdefault(r["track"], []).append((float(r["time_s"]), float(r["value_linear"])))
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
    if int(it["mute"]) == 1 or k not in ("DX","AMB","MUS"): continue
    comp[k] = comp.get(k, 0) + item_sig(it)
for k in comp: p = sorted(env[k]); comp[k] = comp[k]*np.interp(t, [a for a,_ in p], [v for _,v in p])[:,None]
BEFORE = sum(comp.values()); AMBsim = comp["AMB"]
def curve(depth_db, a0=267.45, a1=267.65, b0=270.30, b1=270.50):
    g = np.zeros(L); up = (t >= a0) & (t < a1); hold = (t >= a1) & (t <= b0); dn = (t > b0) & (t <= b1)
    g[up] = depth_db*np.sin((t[up]-a0)/(a1-a0)*np.pi/2)**2; g[hold] = depth_db; g[dn] = depth_db*np.cos((t[dn]-b0)/(b1-b0)*np.pi/2)**2; return 10**(g/20)
HI = AMBsim-lowsplit(AMBsim); DELTA = -HI*(1-curve(-60.0))[:,None]                         # delta = AMB_sélectif − AMB (exact, par linéarité)
za, zb = int((267.0-T0)*SR), int((271.0-T0)*SR); assert np.abs(DELTA[:za]).max() == 0 and np.abs(DELTA[zb:]).max() < 1e-12
dst = M/"PH3_SH37_AMB_selectif_delta_pos267.00s.flac"; assert not dst.exists()
subprocess.run(["ffmpeg","-nostdin","-v","error","-f","f32le","-ar",str(SR),"-ac","2","-i","-","-c:a","flac","-sample_fmt","s32","-bits_per_raw_sample","24",str(dst)], input=DELTA[za:zb].astype("<f4").tobytes(), check=True)
pen_dst = M/"SH37_plume_reelle_mixkit_2369.wav"; assert not pen_dst.exists(); shutil.copyfile(R/"assets/sfx/mixkit/mixkit_2369_writing_scribble_on_paper.wav", pen_dst)
# gestes de plume réelle : 4 items (position, vitesse de lecture, gain item dB = −16,1 + gain du geste) — identiques à la version C choisie
STROKES = [(267.80, 1.00, 0.0), (268.50, 0.97, -2.0), (269.20, 1.04, -1.0), (269.85, 0.99, -4.0)]; NET = -16.1
pen = rd(pen_dst, 0, 0.60, 44100).mean(1); SRP = 44100
def stroke(rate, gain_db):
    n = len(pen); x = np.interp(np.arange(0, n-1, rate), np.arange(n), pen); m = len(x); fi, fo = int(0.02*SRP), int(0.08*SRP); x = x.copy(); x[:fi] *= np.sin(np.linspace(0,np.pi/2,fi))**2; x[-fo:] *= np.cos(np.linspace(0,np.pi/2,fo))**2
    return np.interp(np.arange(int(m*SR/SRP))/SR*SRP, np.arange(m), x)*10**(gain_db/20)
PEN = np.zeros(L)
for tt, rate, gd in STROKES: s = stroke(rate, gd+NET); i0 = int((tt-T0)*SR); PEN[i0:i0+len(s)] += s[:L-i0]
AFTER = BEFORE + DELTA + np.stack([PEN, PEN], 1)
# manifeste SH37-C (lu par scripts/08) + RPP
MAN = V2/"manifest_sh37c"; MAN.mkdir(exist_ok=True); rows = []
for i, (tt, rate, gd) in enumerate(STROKES, 1): rows.append(("FOL_SH37", pen_dst.name, f"{tt:.3f}", f"{0.60/rate:.4f}", "0.000", f"{gd+NET:.1f}", "0.02", "0.08", f"{rate:.2f}", 0, f"SH37 plume réelle — geste {i}/4"))
rows.append(("AMB_SH37", dst.name, "267.000", "4.000", "0.000", "0.0", "0.0", "0.0", "1.00", 0, "SH37 correction sélective (delta >2,1 kHz)"))
cf = MAN/"items_sh37c.csv"; assert not cf.exists()
with open(cf, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["track_key","file","position_s","length_s","source_offset_s","volume_db","fade_in_s","fade_out_s","playrate","mute","name"]); w.writerows(rows)
rpp = (V2/"LE_CARNET_SOUND_V2.RPP").read_text(encoding="utf-8"); G = lambda: "{"+__import__("uuid").uuid4().hex.upper()[:8]+"-"+"-".join(__import__("uuid").uuid4().hex.upper()[i:i+4] for i in (0,4,8))+"-"+__import__("uuid").uuid4().hex.upper()[:12]+"}"
def item(r):
    vol = 10**(float(r[5])/20)
    return f'''    <ITEM
      POSITION {float(r[2]):.6f}
      LENGTH {float(r[3]):.6f}
      LOOP 0
      FADEIN 1 {float(r[6]):.3f} 0 1 0 0 0
      FADEOUT 1 {float(r[7]):.3f} 0 1 0 0 0
      MUTE {r[9]} 0
      NAME "{r[10]}"
      VOLPAN {vol:.6f} 0 1 -1
      SOFFS {float(r[4]):.6f}
      PLAYRATE {float(r[8]):.4f} 0 0 -1 0 0.0025
      <SOURCE {"FLAC" if r[1].endswith(".flac") else "WAVE"}
        FILE "media/{r[1]}"
      >
    >
'''
def track(name, its, depth_line="ISBUS 2 -1"): return f'  <TRACK {G()}\n    NAME "{name}"\n    VOLPAN 1 0 -1 -1 1\n    MUTESOLO 0 0 0\n    {depth_line}\n    NCHAN 2\n    TRACKID {G()}\n    MAINSEND 1 0\n' + "".join(item(r) for r in its) + "  >\n"
def append_after(text, track_name, new_block):
    m = re.search(r'  <TRACK \{[^}]+\}\n    NAME "'+re.escape(track_name)+r'"\n(?:    .*\n|      .*\n|    <.*\n)*?  >\n', text); assert m, track_name
    blk = m.group(0); assert "ISBUS 2 -1" in blk, "dernière piste d'un dossier attendue"
    return text.replace(blk, blk.replace("ISBUS 2 -1", "ISBUS 0 0")+new_block)
rpp = append_after(rpp, "AMB+FOLEY M7c (source mélangée)", track("AMB SH37 — correction sélective >2,1 kHz (delta)", [r for r in rows if r[0] == "AMB_SH37"]))
rpp = append_after(rpp, "FOL test B — oiseau fenêtre", track("FOL SH37 — plume réelle Mixkit 2369", [r for r in rows if r[0] == "FOL_SH37"]))
out = V2/"LE_CARNET_SOUND_V2_SH37C.RPP"; assert not out.exists(); out.write_text(rpp, encoding="utf-8")
# ===== simulation 265–275 : export + mesures =====
cut = lambda x: x[int((265.0-T0)*SR):int((275.0-T0)*SR)]; xb, xa = cut(BEFORE), cut(AFTER)
wr(D/"audio/SH37_C_integration_projet_REAPER_simule_265-275.wav", xa); wr(D/"audio/SH37_AVANT_projet_REAPER_simule_265-275.wav", xb)
zone = np.zeros(10*SR, bool); zone[int((267.40-265)*SR):int((270.55-265)*SR)] = True; d = xa-xb
res = {"delta": {"RMS_dBFS": round(float(db(DELTA[za:zb])),1), "crête_dBFS": round(float(20*np.log10(np.abs(DELTA).max())),1)}, "écart_AVANT_APRES_hors_zone_max": float(np.abs(d[~zone]).max()),
       "HF_4-8k_par_0.5s_267→271_dBFS": {"avant": [round(float(db(bp(xb,4000,8000)[int(k*0.5*SR):int((k+1)*0.5*SR)])),1) for k in range(4,12)], "après": [round(float(db(bp(xa,4000,8000)[int(k*0.5*SR):int((k+1)*0.5*SR)])),1) for k in range(4,12)]},
       "bas_30-2100Hz_modifié_hors_plume_dBFS": round(float(db(bp(d-np.stack([cut(PEN)]*2,1) if False else d - np.stack([PEN[int((265.0-T0)*SR):int((275.0-T0)*SR)]]*2,1), 30, 2100)[zone])),1),
       "crête_après_dBFS": round(float(20*np.log10(np.abs(xa).max())),2), "écrêtés": int((np.abs(xa) >= 0.9999).sum())}
(D/"analysis/sh37c_reaper_simulation.json").write_text(json.dumps(res, indent=1, ensure_ascii=False)); print(json.dumps(res, indent=1, ensure_ascii=False)); print(open(cf, encoding="utf-8").read())
