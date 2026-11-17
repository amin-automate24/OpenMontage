#!/usr/bin/env python3
"""Music trial mixes (local, NON FINAL). Reuses M6 stems (dialogue, ambience/foley ducked) + one licensed track placed on the
validated cues (MA, MB, MC→MD continuous, MF; ME optional). Music ducked −9 dB under speech. Writes audio/mixes/<VER>_pre/mix_premaster.wav,
then scripts/finish_master_audio.py makes audio/mixes/<VER>/ (−16 LUFS, −1 dBTP). Never overwrites (refuses existing versions).
Usage: music_essai.py <VER> <track.mp3> "<offsets json>" """
import sys, json, subprocess, wave, numpy as np, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent; A = R/"audio"; SR = 48000; N = int(276.0*SR)
ver, track, offs = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
PRE = A/"mixes"/f"{ver}_pre"
if PRE.exists() or (A/"mixes"/ver).exists(): sys.exit("version exists")
def rd(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2); y = np.zeros((N, 2), np.float32); e = min(N, len(x)); y[:e] = x[:e]; return y
def lufs(x):
    p = PRE/"_tmp.wav"
    with wave.open(str(p), "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1)*32767).astype(np.int16).tobytes())
    o = subprocess.run(["ffmpeg", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr; p.unlink()
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
PRE.mkdir(parents=True)
dlg = rd(A/"mixes/M6/stems/dialogue.wav"); amb = rd(A/"mixes/M6/stems/ambience_music_ducked.wav")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(track), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
trk = np.frombuffer(raw, np.float32).reshape(-1, 2)
# cues: (id, film_in, film_out, fade_in, fade_out, target LUFS of the music segment before ducking)
CUES = [("MA", 50.5, 66.0, 1.5, 1.5, -31), ("MB", 109.0, 121.0, 1.2, 2.0, -32), ("MCMD", 151.5, 189.5, 3.0, 1.5, -32), ("MF", 268.0, 276.0, 1.0, 2.5, -29)]
if "ME" in offs: CUES.insert(3, ("ME", 244.8, 250.0, 1.5, 1.0, -32))
mus = np.zeros((N, 2), np.float32); placed = []
for cid, a, b, fi, fo, tgt in CUES:
    o = offs[cid]; L = int((b-a)*SR); seg = trk[int(o*SR):int(o*SR)+L].copy()
    if len(seg) < L: seg = np.vstack([seg, np.zeros((L-len(seg), 2), np.float32)])
    g = 10**((tgt-lufs(np.vstack([seg, np.zeros((SR, 2), np.float32)])))/20); seg *= g
    e = np.ones(L, np.float32); i1 = int(fi*SR); i2 = int(fo*SR)
    if i1: e[:i1] = np.linspace(0, 1, i1)**2
    if i2: e[-i2:] *= np.linspace(1, 0, i2)**2
    if cid == "MCMD": k = int((175.0-a)*SR); e[k:] *= 10**(1.5/20)   # légère montée sur la joie populaire (même prise continue, pas de second morceau)
    mus[int(a*SR):int(a*SR)+L] += seg*e[:, None]; placed.append({"cue": cid, "film_in": a, "film_out": b, "track_offset_s": o, "target_lufs": tgt, "gain_db": round(20*np.log10(g), 1)})
# ducking from dialogue envelope (fast moving average via cumsum)
env = np.abs(dlg).max(axis=1); w = int(0.3*SR); c = np.cumsum(np.concatenate([[0], env])); sm = (c[w:]-c[:-w])/w; sm = np.concatenate([sm, np.full(N-len(sm), sm[-1])])
duck = (1-(1-10**(-9/20))*np.clip(sm/0.02, 0, 1))[:, None]
mix = dlg+amb+mus*duck; mix = mix/max(1.0, np.abs(mix).max()/0.89)
with wave.open(str(PRE/"mix_premaster.wav"), "wb") as wv: wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((np.clip(mix, -1, 1)*32767).astype(np.int16).tobytes())
with wave.open(str(PRE/"music_bed_ducked.wav"), "wb") as wv: wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((np.clip(mus*duck, -1, 1)*32767).astype(np.int16).tobytes())
# guard: no music on SH22 / SH33
for nm, a, b in (("SH22", 126.0, 134.0), ("SH33", 225.5, 239.5)): assert np.abs(mus[int(a*SR):int(b*SR)]).max() == 0, nm
json.dump({"version": ver, "track": str(Path(track)), "cues": placed, "ducking_db": -9, "guards": "no music on SH22 (126-134) and SH33 (225.5-239.5): verified"}, open(PRE/"music_report.json", "w"), ensure_ascii=False, indent=1)
subprocess.run([sys.executable, str(R/"scripts/finish_master_audio.py"), f"{ver}_pre", ver], check=True)
