#!/usr/bin/env python3
"""Écrit LE_CARNET_SOUND_V2.RPP depuis manifest/items.csv + markers.csv et l'organisation de scripts/lib_carnet.lua (même structure).
Le .RPP porte : 48 kHz, pistes/bus en dossiers, items (positions, offsets, volumes, fondus, muets), marqueurs/régions.
Les enveloppes, traitements et envois sont ajoutés par scripts/01_completer_projet_rpp.lua (API REAPER), car leur syntaxe binaire n'est pas écrite à la main."""
import csv, re, uuid
from pathlib import Path
B = Path(__file__).resolve().parents[1]
lay = re.findall(r'\{"(\w+)",\s+"([^"]+)",\s+(-?\d)\}', (B/"scripts/lib_carnet.lua").read_text(encoding="utf-8"))
G = lambda: "{" + str(uuid.uuid4()).upper() + "}"
ITEM_TRACK = {"DX":"DX","AMB":"AMB","MUS":"MUS","MUS_ALT":"MUS_ALT","FOL_A":"FOL_A","FOL_B":"FOL_B","REF_MIX":"REF_MIX","REF_MST":"REF_MST"}
items = list(csv.DictReader(open(B/"manifest/items.csv", encoding="utf-8")))
kind = lambda f: "MP3" if f.lower().endswith(".mp3") else ("WAVE" if f.lower().endswith(".wav") else "FLAC")
def item(r):
    vol = 10**(float(r["volume_db"])/20)
    return f'''    <ITEM
      POSITION {float(r["position_s"]):.6f}
      LENGTH {float(r["length_s"]):.6f}
      LOOP 0
      FADEIN 1 {float(r["fade_in_s"]):.3f} 0 1 0 0 0
      FADEOUT 1 {float(r["fade_out_s"]):.3f} 0 1 0 0 0
      MUTE {r["mute"]} 0
        NAME "{r["name"].replace('"', "'")}"
      VOLPAN {vol:.6f} 0 1 -1
      SOFFS {float(r["source_offset_s"]):.6f}
      <SOURCE {kind(r["file"])}
        FILE "media/{r["file"]}"
      >
    >
'''
ISBUS = {"1": "ISBUS 1 1", "0": "ISBUS 0 0", "-1": "ISBUS 2 -1", "-2": "ISBUS 2 -2"}
tracks = ""
for key, name, depth in lay:
    its = "".join(item(r) for r in items if ITEM_TRACK.get(r["track"]) == key)
    mute = 1 if key == "REFF" else 0
    tracks += f'''  <TRACK {G()}
    NAME "{name}"
    VOLPAN 1 0 -1 -1 1
    MUTESOLO {mute} 0 0
    {ISBUS[depth]}
    NCHAN 2
    TRACKID {G()}
    MAINSEND 1 0
{its}  >
'''
mk = ""; idx = 1
for r in csv.DictReader(open(B/"manifest/markers.csv", encoding="utf-8")):
    s = float(r["Start"]); nm = r["Name"].replace('"', "'")
    if r["End"]:
        mk += f'  MARKER {idx} {s:.4f} "{nm}" 1 0 1 R {G()} 0\n  MARKER {idx} {float(r["End"]):.4f} "" 1 0 1 R {G()} 0\n'
    else:
        mk += f'  MARKER {idx} {s:.4f} "{nm}" 0 0 1 R {G()} 0\n'
    idx += 1
rpp = f'''<REAPER_PROJECT 0.1 "7.0/win64" 1763650000
  RIPPLE 0
  AUTOXFADE 129
  CURSOR 0
  LOOP 0
  SAMPLERATE 48000 1 0
{mk}  MASTER_NCH 2 2
  MASTER_VOLUME 1 0 -1 -1 1
  MASTER_FX 1
{tracks}>
'''
rpp = rpp.replace('        NAME "', '      NAME "'); (B/"LE_CARNET_SOUND_V2.RPP").write_text(rpp, encoding="utf-8")
print("RPP :", len(rpp), "octets ;", len(lay), "pistes ;", len(items), "items ;", idx-1, "marqueurs/régions")
