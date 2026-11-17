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
def lufs(p):
    import re
    o = subprocess.run(["ffmpeg", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
def lufs_proc(p, af):
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-af", af, t.name], check=True); return lufs(t.name)
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
    place = []; spans = []; dlg_l = np.zeros(n, np.float32); dlg_r = np.zeros(n, np.float32); env = np.zeros(n, np.float32); used = []
    for L in lines:
        k = L["key"]; fin = A/"voices_final"/f"{k}.wav"; tmp = R/"animatic/voices"/f"{k}.wav"
        vd = A/sys.argv[sys.argv.index("--voices-dir")+1]/f"{k}.wav" if "--voices-dir" in sys.argv else None
        if fin.exists(): src, kind = fin, "final_dir"
        elif vd is not None and vd.exists(): src, kind = vd, "voices_dir"
        else: src, kind = tmp, "temp"
        used.append((k, kind))
        RADIO_V2 = "highpass=f=320,lowpass=f=3300,equalizer=f=1600:width_type=o:width=1.2:g=5,acompressor=threshold=-20dB:ratio=4:attack=5:release=80,acrusher=bits=10:mode=log:aa=1:mix=0.15,aecho=0.8:0.6:18:0.12"
        af = (RADIO_V2 if "--radio-v2" in sys.argv else "highpass=f=450,lowpass=f=3000,acrusher=bits=9:mode=log:aa=1:mix=0.35") if L["character"] == "VOIX RADIO" and (kind == "temp" or "--radio-fx" in sys.argv or "--radio-v2" in sys.argv) else None
        at = rh.get(k, {}).get("atempo_max"); af2 = (af+"," if af else "")+f"atempo={at}" if at else af
        x = dec(src, af2)
        if "--lufs-balance" in sys.argv:
            I = lufs(src) if not (af and "--radio-v2" in sys.argv) else lufs_proc(src, af); g = -23.0 - I; x = x*10**((g + GAIN_DB.get(L["character"], 0))/20); place.append({"key": k, "lufs_src": I, "gain_db": round(g, 2)})
        else: x = x/(np.abs(x).max()+1e-9)*0.5*10**(GAIN_DB.get(L["character"], 0)/20)
        st0 = rh.get(k, {}).get("start_s", L["start_s"]); spans.append((k, st0, st0+len(x)/SR, kind))
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
    if "--ambience-wav" in sys.argv:
        aw = A/sys.argv[sys.argv.index("--ambience-wav")+1]
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(aw), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], check=True, capture_output=True).stdout
        st2 = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2); bl = np.zeros(n, np.float32); br = np.zeros(n, np.float32); e = min(n, len(st2)); bl[:e] = st2[:e, 0]; br[:e] = st2[:e, 1]
        bl = (bl+music)*duck; br = (br+music)*duck; bus = (bl+br)/2
    else:
        bus = (ambi+music)*duck; bl = br = bus
    L = dlg_l+bl; Rr = dlg_r+br; st = np.stack([L, Rr], 1); st = st/max(1.0, np.abs(st).max()/0.89)
    (OUT/"stems").mkdir(exist_ok=True)
    def wr(p, a):
        with wave.open(str(p), "wb") as w_: w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((np.clip(a, -1, 1)*32767).astype(np.int16).tobytes())
    wr(OUT/"stems/dialogue.wav", np.stack([dlg_l, dlg_r], 1)); wr(OUT/"stems/ambience_music_ducked.wav", np.stack([bl, br], 1)); wr(OUT/"mix_premaster.wav", st)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(OUT/"mix_premaster.wav"), "-af", "loudnorm=I=-16:TP=-1.5:LRA=9" + (",alimiter=limit=0.82:level=disabled:attack=1:release=50" if "--limiter" in sys.argv else ""), "-ar", "48000", "-ac", "2", str(OUT/f"MIX_276s_{ver}.wav")], check=True)
    (OUT/"mix_report.json").write_text(json.dumps({"version": ver, "rhythm_applied": sorted(rh), "provisional_voices": {k: v["status"] for k, v in prov.items()}, "lines": len(lines), "sources": used, "levels": place, "spans": [(k, round(a, 2), round(b, 2), kd) for k, a, b, kd in sorted(spans, key=lambda t: t[1])], "overlaps": [(a[0], b[0], round(a[2]-b[1], 2)) for i, a in enumerate(sorted(spans, key=lambda t: t[1])) for b in sorted(spans, key=lambda t: t[1])[i+1:] if b[1] < a[2]], "flags": sys.argv[2:], "music": [str(m.name) for m in mus[:1]], "ducking_db": -9}, indent=1))
    print("mix ok", sum(1 for _, s in used if s == "final"), "final /", len(used), "lines; music:", [m.name for m in mus[:1]])
if __name__ == "__main__": main()
