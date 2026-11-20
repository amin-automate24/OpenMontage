#!/usr/bin/env python3
"""Prépare le PAQUET REAPER (Windows) : médias FLAC référencés en chemins relatifs, fichier .RPP, marqueurs CSV, scripts ReaScript Lua.
NON EXÉCUTÉ dans REAPER (REAPER n'existe pas dans cet environnement) : le .RPP est écrit selon le format texte documenté, sans validation par le logiciel.
Sources existantes uniquement (0 crédit). Refuse d'écraser les médias déjà copiés."""
import subprocess, csv, json, uuid, shutil
from pathlib import Path
R = Path(__file__).resolve().parents[4]; P = R/"audio/CINEMA_SOUND_REDESIGN/PHASE_2_TESTS/REAPER_PROJECT"; MED = P/"media"; MED.mkdir(parents=True, exist_ok=True)
def flac(src, dst):
    dst = MED/dst
    if not dst.exists(): subprocess.run(["ffmpeg","-nostdin","-v","error","-i",str(src),"-vn","-ar","48000","-c:a","flac","-sample_fmt","s32","-bits_per_raw_sample","24",str(dst)], check=True)
    return dst.name
dur = lambda f: float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(MED/f)],capture_output=True,text=True).stdout)
F = {"dx": flac(R/"audio/mixes/M6/stems/dialogue.wav", "DX_dialogue_stem_M6_276s.flac"),
     "amb": flac(R/"audio/sfx_m7c/ambience_foley_m7c.wav", "AMB_FOLEY_M7c_276s_melange.flac"),
     "mix": flac(R/"audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav", "REF_MIX_actuel_QC2_SON2_276s_sans_perte.flac"),
     "mst": flac(R/"deliverables/FINAL_CINEMA/LE_CARNET_DE_LA_LIBERTE_CINEMA_FINAL_1080p.mp4", "REF_master_FINAL_audio_299s_AAC_decode.flac")}
for s in ["mixkit_1103_stiff_paper_book_paging.wav","mixkit_2427_breeze_through_the_trees.wav","mixkit_2472_morning_birds.wav"]:
    if not (MED/s).exists(): shutil.copyfile(R/"assets/sfx/mixkit"/s, MED/s)
if not (MED/"mixkit_599_possible_dreams.mp3").exists(): shutil.copyfile(R/"assets/music/mixkit/mixkit_599_possible_dreams.mp3", MED/"mixkit_599_possible_dreams.mp3")
G = lambda: "{"+str(uuid.uuid4()).upper()+"}"
def item(pos, length, name, file, kind="FLAC", soffs=0.0, vol=1.0, fi=0.0, fo=0.0, mute=0):
    return f'''    <ITEM
      POSITION {pos:.6f}
      SNAPOFFS 0
      LENGTH {length:.6f}
      LOOP 0
      ALLTAKES 0
      FADEIN 1 {fi:.3f} 0 1 0 0 0
      FADEOUT 1 {fo:.3f} 0 1 0 0 0
      MUTE {mute} 0
      NAME "{name}"
      VOLPAN {vol:.6f} 0 1 -1
      SOFFS {soffs:.6f}
      <SOURCE {kind}
        FILE "media/{file}"
      >
    >
'''
def track(name, items="", folder=0, vol_db=0.0, mute=0, note=""):  # folder : 1 début de dossier, 0 normal, -1 dernier enfant (ferme le dossier)
    isbus = {1: "ISBUS 1 1", 0: "ISBUS 0 0", -1: "ISBUS 2 -1"}[folder]
    v = 10**(vol_db/20)
    return f'''  <TRACK {G()}
    NAME "{name}"
    VOLPAN {v:.6f} 0 -1 -1 1
    MUTESOLO {mute} 0 0
    {isbus}
    NCHAN 2
    MAINSEND 1 0
{items}  >
'''
LAG = 47/48000
mus = json.load(open(R/"audio/mixes/M9T_pre/music_report.json"))["cues"]
mx = "".join(item(c["film_in"], c["film_out"]-c["film_in"], f'{c["cue"]} (offset {c["track_offset_s"]} s)', "mixkit_599_possible_dreams.mp3", "MP3", soffs=c["track_offset_s"], vol=10**(c["gain_db"]/20), fi=c["fade_in"], fo=c["fade_out"]) for c in mus)
cm_len = dur("PH2_C_musique_generique_pos274.60s.flac")
trk = ""
trk += track("DX — DIALOGUES", folder=1)
trk += track("DX stem M6 (calé +47 éch.)", item(LAG, 276.0, "dialogue stem M6", F["dx"]), folder=-1)
trk += track("AMB — AMBIANCES", folder=1)
trk += track("AMB+FOLEY M7c (mélangé)", item(0, 276.0, "ambience_foley_m7c", F["amb"]), folder=-1)
trk += track("FX — FOLEY / SFX", folder=1)
trk += track("PH2-A foley carnet + air d'encre", item(36.0, dur("PH2_A_foley_air_pos36.00s.flac"), "PH2 A", "PH2_A_foley_air_pos36.00s.flac"))
trk += track("PH2-B oiseau fenêtre", item(163.9, dur("PH2_B_oiseau_pos163.90s.flac"), "PH2 B", "PH2_B_oiseau_pos163.90s.flac"), folder=-1)
trk += track("MX — MUSIQUE", folder=1)
trk += track("MX thème (cues Mixkit 599, M9T)", mx)
trk += track("PH2-C reprise du thème (générique)", item(274.6, cm_len, "PH2 C", "PH2_C_musique_generique_pos274.60s.flac"), folder=-1)
trk += track("REF mix actuel (sans perte, MUET)", item(0, 276.0, "mix QC2_SON2", F["mix"]), mute=1)
trk += track("REF master FINAL (AAC décodé, MUET)", item(0, 299.0, "master FINAL", F["mst"]), mute=1)
# marqueurs : plans, répliques détectées, cartons, régions de test
rows = []
for r in csv.DictReader(open(R/"shotlist/shot_list.csv")): rows.append((float(r["start_s"]), "Plan "+r["id"]+" — "+r["description"][:50].replace('"', "'"), 0))
for l in json.load(open(P.parent/"qc/decomposition_lignes.json"))["lines"]: rows.append((l["in_s"], f'réplique {l["in_s"]:.2f}', 0))
for t_, n_ in [(276.12,"Carton 1 (générique)"),(282.0,"Carton 2"),(285.5,"Carton 3"),(36.04,"Coupe SH08 (mesurée)"),(163.56,"Coupe SH26 (mesurée)")]: rows.append((t_, n_, 0))
rows.sort(); mk = ""; i = 1
for t_, n_, _ in rows: mk += f'  MARKER {i} {t_:.4f} "{n_}" 0 0 1 R {G()} 0\n'; i += 1
for name, a, b in [("TEST A ouverture du carnet", 30.0, 65.0), ("TEST B séquence 1955", 160.0, 190.0), ("TEST C générique", 268.0, 299.0)]:
    mk += f'  MARKER {i} {a:.4f} "{name}" 1 0 1 B {G()} 0\n  MARKER {i} {b:.4f} "" 1 0 1 B {G()} 0\n'; i += 1
rpp = f'''<REAPER_PROJECT 0.1 "7.0/win64" 1763600000
  RIPPLE 0
  AUTOXFADE 129
  SAMPLERATE 48000 0 0
  TEMPO 120 4 4
  CURSOR 0
  ZOOM 20 0 0
  PROJOFFS 0 0 0
  LOOP 0
  <NOTES 0
    LE CARNET DE LA LIBERTE - Phase 2 sonore (PREPARATOIRE). Sources existantes uniquement. Non ouvert dans REAPER par l'auteur du paquet.
    Les pistes REF (muettes) servent a comparer au master FINAL. Image : charger la video du master FINAL dans REAPER (Insert > Media file) sur une piste video ; ne jamais l'ecraser.
  >
{mk}{trk}>
'''
(P/"LE_CARNET_SOUND_PHASE2.RPP").write_text(rpp, encoding="utf-8")
with open(P/"markers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["#","Name","Start","End","Color"])
    for k, (t_, n_, _) in enumerate(rows, 1): w.writerow([f"M{k}", n_, f"{t_:.4f}", "", ""])
    for k, (n_, a, b) in enumerate([("TEST A ouverture du carnet",30.0,65.0),("TEST B séquence 1955",160.0,190.0),("TEST C générique",268.0,299.0)], 1): w.writerow([f"R{k}", n_, f"{a:.4f}", f"{b:.4f}", ""])
print("RPP écrit", (P/"LE_CARNET_SOUND_PHASE2.RPP").stat().st_size, "octets;", i-1, "marqueurs/régions")
