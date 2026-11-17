#!/usr/bin/env python3
"""Automated audio assembly (FFmpeg + numpy, local, free).
Dialogue: audio/voices_final/<KEY>.wav if present, else the temporary espeak line animatic/voices/<KEY>.wav.
Beds: per-scene ambience generated locally (placeholder-quality) ; music: first file of music_library/ per cue if present.
Mix: dialogue first (intelligibility) - ambience/music ducked under speech, light stereo placement, -16 LUFS integrated, TP <= -1 dB.
Versioned variant: never writes audio/MIX_276s.wav ; output audio/mixes/<version>/.
Usage: assemble_audio_versioned.py <version> [--rhythm]"""
import json, subprocess, sys, numpy as np, wave
from pathlib import Path
R = Path(__file__).resolve().parent.parent; A = R/"audio"; SR = 48000; TOTAL = 276.0
sys.path.insert(0, str(Path(__file__).parent)); from shots_data import SCENES
PAN = {"LA MAÎTRESSE": -0.15, "YOUNES": 0.10, "LA MÈRE": 0.15, "AMINA": 0.0, "LE PÈRE": -0.10, "VOIX RADIO": 0.0, "VOIX HORS CHAMP": 0.25}
GAIN_DB = {"VOIX RADIO": -2.0, "VOIX HORS CHAMP": -3.0}
def dec(path, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)] + (["-af", af] if af else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, check=True, capture_output=True).stdout, dtype=np.float32)
def bed(kind, dur):
    f = {"classe": "anoisesrc=c=pink:a=0.5:r=48000,bandpass=f=900:w=1.6", "maison": "anoisesrc=c=brown:a=0.4:r=48000,lowpass=f=500",
         "rue": "anoisesrc=c=pink:a=0.5:r=48000,bandpass=f=1200:w=2", "nuit": "anoisesrc=c=brown:a=0.35:r=48000,lowpass=f=250",
         "foule": "anoisesrc=c=pink:a=0.6:r=48000,bandpass=f=1500:w=2.5,tremolo=f=0.35:d=0.35"}[kind]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", f"{f}:d={dur}".replace(":d=", ",atrim=0:") if False else f, "-t", str(dur), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], check=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32); x = x/(np.abs(x).max()+1e-9); return x[:int(dur*SR)]
SCENE_BED = {1: "classe", 2: "maison", 3: "rue", 4: "nuit", 5: "foule", 6: "classe"}
def main():
    ver = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    if not ver: sys.exit("version required, e.g. v2")
    OUT = A/"mixes"/ver
    if OUT.exists(): sys.exit(f"{OUT} exists: choose a new version")
    OUT.mkdir(parents=True)
    rh = {}
    if "--rhythm" in sys.argv: rh.update(json.loads((A/"rhythm_corrections_Y1_Y4_PROPOSED.json").read_text())["corrections"])
    if "--rhythm-file" in sys.argv:
        for f in sys.argv[sys.argv.index("--rhythm-file")+1].split(","): rh.update(json.loads((A/f).read_text())["corrections"])
    prov = json.loads((A/"voices_status.json").read_text()) if (A/"voices_status.json").exists() else {}
    lines = json.loads((A/"elevenlabs_script_multilingual_v2.json").read_text())["lines"]; n = int(TOTAL*SR)
    dlg_l = np.zeros(n, np.float32); dlg_r = np.zeros(n, np.float32); env = np.zeros(n, np.float32); used = []
    for L in lines:
        k = L["key"]; fin = A/"voices_final"/f"{k}.wav"; tmp = R/"animatic/voices"/f"{k}.wav"
        src = fin if fin.exists() else tmp; used.append((k, "final" if fin.exists() else "temp"))
        af = "highpass=f=450,lowpass=f=3000,acrusher=bits=9:mode=log:aa=1:mix=0.35" if L["character"] == "VOIX RADIO" and not fin.exists() else None
        at = rh.get(k, {}).get("atempo_max"); af2 = (af+"," if af else "")+f"atempo={at}" if at else af
        x = dec(src, af2); x = x/(np.abs(x).max()+1e-9)*0.5*10**(GAIN_DB.get(L["character"], 0)/20)
        i0 = int(rh.get(k, {}).get("start_s", L["start_s"])*SR); p = PAN.get(L["character"], 0.0); gl = np.cos((p+1)*np.pi/4); gr = np.sin((p+1)*np.pi/4)
        e = min(len(x), n-i0); dlg_l[i0:i0+e] += x[:e]*gl*1.414; dlg_r[i0:i0+e] += x[:e]*gr*1.414; env[i0:i0+e] = np.maximum(env[i0:i0+e], np.abs(x[:e]))
    # smoothed speech envelope -> ducking curve (up to -9 dB under speech, 0.25 s attack/0.6 s release)
    w = int(0.3*SR); sm = np.convolve(env, np.ones(w)/w, mode="same"); duck = 1-(1-10**(-9/20))*np.clip(sm/0.05, 0, 1)
    ambi = np.zeros(n, np.float32)
    for sc, inf in SCENES.items():
        i0, i1 = int(inf["start"]*SR), int(inf["end"]*SR); seg = bed(SCENE_BED[sc], inf["end"]-inf["start"]+1.0)[:i1-i0+SR]
        fade = int(1.0*SR); seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        e = min(len(seg), n-i0); ambi[i0:i0+e] += seg[:e]*10**(-33/20)
    music = np.zeros(n, np.float32); mus = sorted((R/"music_library").glob("*.*")) if (R/"music_library").exists() else []
    if mus: m = dec(mus[0]); e = min(len(m), n); music[:e] = m[:e]/(np.abs(m).max()+1e-9)*10**(-22/20)
    bus = (ambi+music)*duck
    L = dlg_l+bus; Rr = dlg_r+bus; st = np.stack([L, Rr], 1); st = st/max(1.0, np.abs(st).max()/0.89)
    (OUT/"stems").mkdir(exist_ok=True)
    def wr(p, a):
        with wave.open(str(p), "wb") as w_: w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((np.clip(a, -1, 1)*32767).astype(np.int16).tobytes())
    wr(OUT/"stems/dialogue.wav", np.stack([dlg_l, dlg_r], 1)); wr(OUT/"stems/ambience_music_ducked.wav", np.stack([bus, bus], 1)); wr(OUT/"mix_premaster.wav", st)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(OUT/"mix_premaster.wav"), "-af", "loudnorm=I=-16:TP=-1.5:LRA=9", "-ar", "48000", "-ac", "2", str(OUT/f"MIX_276s_{ver}.wav")], check=True)
    (OUT/"mix_report.json").write_text(json.dumps({"version": ver, "rhythm_applied": sorted(rh), "provisional_voices": {k: v["status"] for k, v in prov.items()}, "lines": len(lines), "sources": used, "music": [str(m.name) for m in mus[:1]], "ducking_db": -9}, indent=1))
    print("mix ok", sum(1 for _, s in used if s == "final"), "final /", len(used), "lines; music:", [m.name for m in mus[:1]])
if __name__ == "__main__": main()
