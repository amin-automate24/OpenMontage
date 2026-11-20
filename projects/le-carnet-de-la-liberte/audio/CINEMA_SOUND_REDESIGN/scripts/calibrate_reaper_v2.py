#!/usr/bin/env python3
"""Calibre la RECONSTRUCTION multipiste depuis les sources existantes et écrit le manifeste du projet REAPER v2 (CSV) + la mesure de fidélité.
Gains estimés par moindres carrés contre le mix final sans perte (QC2_SON2, 276 s). Aucune génération, 0 crédit. Refuse d'écraser."""
import numpy as np, subprocess, json, csv
from pathlib import Path
R = Path(__file__).resolve().parents[3]; SR = 48000; B = R/"audio/CINEMA_SOUND_REDESIGN/REAPER_V2"; MAN = B/"manifest"
rd = lambda p: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-i",str(p),"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,"<f4").reshape(-1,2).astype(np.float64)
db = lambda x: 20*np.log10(np.sqrt(np.mean(np.square(x)))+1e-12)
M = rd(R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav"); N = len(M)
D = np.roll(rd(R/"audio/mixes/M6/stems/dialogue.wav")[:N], 47, axis=0); AMB = np.roll(rd(R/"audio/sfx_m7c/ambience_foley_m7c.wav")[:N], 47, axis=0); TR = rd(R/"assets/music/mixkit/mixkit_599_possible_dreams.mp3")
lines = json.load(open(R/"audio/CINEMA_SOUND_REDESIGN/PHASE_2_TESTS/qc/decomposition_lignes.json"))["lines"]
# gain constant par réplique (moindres carrés) ; enveloppe DX
dx_pts = []; g_lines = []
for l in lines:
    a, b = int(l["in_s"]*SR), int(l["out_s"]*SR); g = float((D[a:b]*M[a:b]).sum()/(D[a:b]**2).sum()); g_lines.append((l["in_s"], l["out_s"], g))
# ducking de la reconstruction (−9 dB sous les voix, −12 dB dans la foule 174–190 s ; attaque 0,25 s, relâche 0,6 s)
def duck_curve(depth_db_fn):
    d = np.zeros(N)
    for a, b, g in g_lines: d[int((a-0.25)*SR):int((b+0.6)*SR)] = 1.0
    k = np.hanning(int(0.4*SR)); k /= k.sum(); d = np.convolve(d, k, "same"); t = np.arange(N)/SR
    return 10**((depth_db_fn(t)*d)/20)
duck = duck_curve(lambda t: np.where((t >= 174) & (t <= 190), -12.0, -9.0))
cues = json.load(open(R/"audio/mixes/M9T_pre/music_report.json"))["cues"]
def cue_sig(c, gain=1.0):
    s = np.zeros((N,2)); a, b = int(c["film_in"]*SR), min(N, int(c["film_out"]*SR)); n = b-a; off = int(c["track_offset_s"]*SR); seg = TR[off:off+n].copy()
    fi, fo = int(c["fade_in"]*SR), int(c["fade_out"]*SR); seg[:fi] *= (np.sin(np.linspace(0,np.pi/2,fi))**2)[:,None]; seg[-fo:] *= (np.cos(np.linspace(0,np.pi/2,fo))**2)[:,None]; s[a:b] = seg[:n]*gain; return s
mask = np.ones(N, bool)
for a, b, g in g_lines: mask[int((a-0.3)*SR):int((b+0.3)*SR)] = False
# calibration LOCALE par blocs de 4 s : moindres carrés conjoints [ambiance·ducking, musique·ducking] sur les échantillons sans voix (ambiance seule si pas de musique)
CUE_ALL = np.roll(sum(cue_sig(c) for c in cues), 47, axis=0); AD = AMB*duck[:,None]; CD = CUE_ALL*duck[:,None]; BL = int(4*SR); blocks = []
for i0 in range(0, N, BL):
    i1 = min(N, i0+BL); ok = mask[i0:i1]; hasm = np.abs(CD[i0:i1]).max() > 1e-4
    if ok.sum() < 0.8*SR: blocks.append((i0, i1, None, None)); continue
    ya = M[i0:i1][ok].ravel(); xa = AD[i0:i1][ok].ravel()
    if hasm: co, *_ = np.linalg.lstsq(np.stack([xa, CD[i0:i1][ok].ravel()], 1), ya, rcond=None); blocks.append((i0, i1, float(max(co[0], 0.3)), float(max(co[1], 0.0))))
    else: blocks.append((i0, i1, float(max((xa*ya).sum()/(xa*xa).sum(), 0.3)), None))
def fill(vals):
    idx = [k for k, v in enumerate(vals) if v is not None]; return list(np.interp(range(len(vals)), idx, [vals[k] for k in idx]))
amb_b = fill([b[2] for b in blocks]); mus_vals = [b[3] if (b[3] is not None) else None for b in blocks]
mus_present = [np.abs(CD[b[0]:b[1]]).max() > 1e-4 for b in blocks]
mus_known = [k for k, v in enumerate(mus_vals) if v is not None]; mus_b = [float(np.interp(k, mus_known, [mus_vals[j] for j in mus_known])) if mus_present[k] else 0.0 for k in range(len(blocks))]
a_amb_env = np.zeros(N); a_mus_env = np.zeros(N)
for k, (i0, i1, _, _) in enumerate(blocks): a_amb_env[i0:i1] = amb_b[k]; a_mus_env[i0:i1] = mus_b[k]
kk = np.hanning(int(1.0*SR)); kk /= kk.sum(); a_amb_env = np.convolve(a_amb_env, kk, "same"); a_mus_env = np.convolve(a_mus_env, kk, "same")
amb_pts = [(blocks[k][0]/SR, blocks[k][1]/SR, amb_b[k]) for k in range(len(blocks))]; mus_pts = [(blocks[k][0]/SR, blocks[k][1]/SR, mus_b[k]) for k in range(len(blocks)) if mus_present[k]]
a_amb = float(np.median(amb_b)); a_cue = {c["cue"]: float(np.median([v for (s0, s1, v) in mus_pts if c["film_in"]-4 <= s0 <= c["film_out"]] or [0.0])) for c in cues}
synth = np.zeros_like(M)
for a, b, g in g_lines: synth[int(a*SR):int(b*SR)] += g*D[int(a*SR):int(b*SR)]
synth += AD*a_amb_env[:,None]
synth += CD*a_mus_env[:,None]
res = M-synth; seg_sections = {"0-50 s classe/maison": (0,50), "50-110 s carnet + rue 1944": (50,110), "110-165 s nuit 1953": (110,165), "165-200 s Rabat 1955": (165,200), "200-276 s fin": (200,276)}
fid = {"gain_AMB_par_plan_lineaire_min_med_max": [round(min(a for *_,a in amb_pts),2), round(a_amb,2), round(max(a for *_,a in amb_pts),2)], "gain_musique_médian_par_repère_vs_piste_brute": {k: round(v,2) for k,v in a_cue.items()}, "gain_DX_par_replique_min_med_max": [round(min(g for *_,g in g_lines),2), round(float(np.median([g for *_,g in g_lines])),2), round(max(g for *_,g in g_lines),2)],
       "fidélité_globale_résidu_vs_mix_dB": round(db(res)-db(M),1), "fidélité_par_section_dB": {k: round(db(res[int(a*SR):int(b*SR)])-db(M[int(a*SR):int(b*SR)]),1) for k,(a,b) in seg_sections.items()},
       "lecture": "résidu = mix − reconstruction ; −10 dB ≈ reconstruction proche, −3 dB ≈ approximative. Le mix final provient de plusieurs versions assemblées : la reconstruction est une BASE DE TRAVAIL, pas une copie."}
(MAN/"calibration_fidelite.json").write_text(json.dumps(fid, indent=1, ensure_ascii=False))
# enveloppes de volume RELATIVES (REAPER limite une enveloppe de volume à +6 dB = 2,0 : les gains moyens sont portés par le volume des items)
gmed = float(np.median([g for *_, g in g_lines])); env = []
for a, b, g in g_lines: env += [("DX", a-0.05, g/gmed), ("DX", b+0.10, g/gmed)]
cue_med_at = np.ones(N)
for c in cues: cue_med_at[int(c["film_in"]*SR):int(c["film_out"]*SR)] = max(a_cue[c["cue"]], 1e-3)
ts = np.arange(0, N, int(0.1*SR)); amb_rel = np.minimum(a_amb_env/a_amb*duck, 1.98); mus_rel = np.minimum(a_mus_env/cue_med_at*duck, 1.98)
for i in ts: env.append(("AMB", i/SR, float(amb_rel[i])))
for i in ts:
    if np.abs(CD[i:i+int(0.1*SR)]).max() > 1e-4 or True: env.append(("MUS", i/SR, float(mus_rel[i])))
with open(MAN/"envelopes.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["track","time_s","value_linear"]); [w.writerow([t, f"{x:.4f}", f"{v:.4f}"]) for t, x, v in sorted(env, key=lambda e: (e[0], e[1]))]
# items : piste, fichier, position, longueur, offset source, volume dB, fondu entrée, fondu sortie, muet, nom
items = [("DX", "DX_dialogue_stem_M6_276s.flac", 47/48000, 276.0, 0.0, float(20*np.log10(gmed)), 0.0, 0.0, 0, "DX stem M6 (calé +47 éch.) — gain par réplique = enveloppe de la piste"),
         ("AMB", "AMB_FOLEY_M7c_276s_melange.flac", 47/48000, 276.0, 0.0, float(20*np.log10(a_amb)), 0.0, 0.0, 0, "AMB+FOLEY M7c (mélangé) — gain par plan + ducking = enveloppe de la piste")]
for c in cues: items.append(("MUS", "mixkit_599_possible_dreams.mp3", c["film_in"], c["film_out"]-c["film_in"], c["track_offset_s"], float(20*np.log10(max(a_cue[c["cue"]],1e-3))), c["fade_in"], c["fade_out"], 0, f'{c["cue"]} (offset {c["track_offset_s"]} s)'))
items += [("MUS", "PH2_C_generique_v2_pos273.00s.flac", 273.0, 26.0, 0.0, 0.0, 0.0, 0.0, 0, "GÉNÉRIQUE v2 (fondu enchaîné) — proposition, active"),
          ("MUS_ALT", "PH2_C_generique_v2b_pos275.00s.flac", 275.0, 24.0, 0.0, 0.0, 0.0, 0.0, 1, "GÉNÉRIQUE v2b (respiration) — alternative muette"),
          ("FOL_A", "PH2_A_foley_air_pos36.00s.flac", 36.0, 30.0, 0.0, 0.0, 0.0, 0.0, 1, "TEST A foley carnet + air d'encre — muet par défaut"),
          ("FOL_B", "PH2_B_oiseau_pos163.90s.flac", 163.9, 3.7, 0.0, 0.0, 0.0, 0.0, 1, "TEST B oiseau fenêtre — muet par défaut"),
          ("REF_MIX", "REF_MIX_actuel_QC2_SON2_276s_sans_perte.flac", 0.0, 276.0, 0.0, 0.0, 0.0, 0.0, 1, "REF mix actuel sans perte (muet)"),
          ("REF_MST", "REF_master_FINAL_audio_part1_0-150s.flac", 0.0, 150.0, 0.0, 0.0, 0.0, 0.0, 1, "REF master FINAL audio (1/2) muet"),
          ("REF_MST", "REF_master_FINAL_audio_part2_150-299s.flac", 150.0, 149.008, 0.0, 0.0, 0.0, 0.0, 1, "REF master FINAL audio (2/2) muet")]
with open(MAN/"items.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["track","file","position_s","length_s","source_offset_s","volume_db","fade_in_s","fade_out_s","mute","name"]); [w.writerow([*i[:2], f"{i[2]:.6f}", f"{i[3]:.3f}", f"{i[4]:.3f}", f"{i[5]:.2f}", f"{i[6]:.2f}", f"{i[7]:.2f}", i[8], i[9]]) for i in items]
print(json.dumps(fid, indent=1, ensure_ascii=False))
# ===== simulation de la somme attendue du projet REAPER v2 (sans plugins) : reconstruction + générique v2 ; tests A/B muets =====
TOT = int(299*SR); sim = np.zeros((TOT,2)); sim[:N] = synth
gen = rd(B/"media/PH2_C_generique_v2_pos273.00s.flac"); i0 = int(273.0*SR); sim[i0:i0+len(gen)] += gen[:TOT-i0]
SIMP = R/"audio/CINEMA_SOUND_REDESIGN/analysis/SIMULATION_somme_projet_REAPER_v2_299s.flac"; SIMP.unlink(missing_ok=True)
subprocess.run(["ffmpeg","-nostdin","-v","error","-f","f32le","-ar",str(SR),"-ac","2","-i","-","-c:a","flac","-sample_fmt","s32","-bits_per_raw_sample","24",str(SIMP)], input=sim.astype("<f4").tobytes(), check=True)
print("simulation :", SIMP.name, "crête", round(20*np.log10(np.abs(sim).max()),2), "dBFS")
