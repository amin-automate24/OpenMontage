#!/usr/bin/env python3
"""Integration of the 5 human Younes takes (Y1..Y5). Local, free. Default = dry-run (checks only, writes a report).
Usage: integrate_younes_voices.py --takes DIR --pick Y1=t2,Y2=t1,Y3=t1,Y4=t3,Y5=t1 [--apply]
Files expected in DIR: Y1_t1.wav ... (any sample rate/channels). Checks: duration vs window, peak, room noise (first 3 s), clipping.
--apply: writes cleaned 48 kHz mono 24-bit copies (high-pass 80 Hz only, NO loudness change) to audio/recording_younes/retenues/ ; never overwrites; originals untouched.
Promotion to audio/voices_final/ is a separate manual step after validation. Then: assemble_audio_versioned.py M5 --voices-dir voices_m2_lot/wav ... (finals take priority)."""
import sys, json, subprocess, re, csv
from pathlib import Path
R = Path(__file__).resolve().parent.parent; A = R/"audio"
def arg(n, d=None): return sys.argv[sys.argv.index(n)+1] if n in sys.argv else d
def probe(p):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate,channels:format=duration", "-of", "json", str(p)]); j = json.loads(o)
    return int(j["streams"][0]["sample_rate"]), int(j["streams"][0]["channels"]), float(j["format"]["duration"])
def stats(p, t0=None, t1=None):
    cmd = ["ffmpeg", "-nostats", "-v", "info"] + (["-ss", str(t0), "-t", str(t1-t0)] if t0 is not None else []) + ["-i", str(p), "-af", "astats=measure_perchannel=none:measure_overall=Peak_level+RMS_level", "-f", "null", "-"]
    o = subprocess.run(cmd, capture_output=True, text=True).stderr; pk = re.findall(r"Peak level dB:\s+(-?[\d.inf]+)", o); rm = re.findall(r"RMS level dB:\s+(-?[\d.inf]+)", o)
    f = lambda x: float(x[-1]) if x and "inf" not in x[-1] else -120.0
    return f(pk), f(rm)
def main():
    d = Path(arg("--takes", A/"recording_younes/prises")); picks = dict(x.split("=") for x in arg("--pick", "").split(",") if x); apply = "--apply" in sys.argv
    rows = {r["cle"]: r for r in csv.DictReader(open(A/"recording_younes/younes_lignes_enregistrement.csv", encoding="utf-8"))}
    rhythm = json.load(open(A/"rhythm_corrections_Y1_Y4_PROPOSED.json"))["corrections"]; rep = []; ok_all = True
    for k in ["Y1", "Y2", "Y3", "Y4", "Y5"]:
        t = picks.get(k); f = d/f"{k}_{t}.wav" if t else None; r = rows[k]; item = {"key": k, "pick": t}
        if not f or not f.exists(): item["status"] = "MANQUANT"; ok_all = False; rep.append(item); continue
        sr, ch, du = probe(f); pk, _ = stats(f); _, noise = stats(f, 0, min(3.0, du/2))
        win = float(r["duree_dispo_s"]); ext = rhythm.get(k, {}); win_ext = (ext["max_end_s"]-ext["start_s"]) if "max_end_s" in ext else win
        speech = du-5.0 if du > 6 else du   # 5 s de bruit de pièce en tête (procédure)
        item.update({"sr": sr, "ch": ch, "dur_file_s": round(du, 2), "peak_dbfs": pk, "room_noise_dbfs": noise, "window_s": win, "window_ext_s": round(win_ext, 2), "fits_window": speech <= win_ext+0.15, "est_speech_s": round(speech, 2)})
        flags = []
        if pk > -1.0: flags.append("ÉCRÊTAGE POSSIBLE (crête > −1 dBFS)")
        if pk < -30: flags.append("NIVEAU TROP BAS (crête < −30 dBFS)")
        if noise > -50: flags.append("BRUIT DE PIÈCE ÉLEVÉ (> −50 dBFS)")
        if not item["fits_window"]: flags.append("TROP LONG : atempo %.2f requis" % (speech/win_ext) if ext.get("atempo_max") else "TROP LONG pour la fenêtre")
        item["flags"] = flags; item["status"] = "OK" if not flags else "A REVOIR"; ok_all &= not flags
        if apply and not flags:
            out = A/"recording_younes/retenues"/f"{k}.wav"; out.parent.mkdir(parents=True, exist_ok=True)
            if out.exists(): item["status"] = "REFUSÉ : existe déjà (aucun écrasement)"
            else: subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-af", "highpass=f=80", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s24le", str(out)], check=True); item["retenue"] = str(out.relative_to(R))
        rep.append(item)
    out = A/"recording_younes"/("integration_report_APPLY.json" if apply else "integration_report_DRYRUN.json"); out.write_text(json.dumps({"all_ok": ok_all, "items": rep}, ensure_ascii=False, indent=1))
    for i in rep: print(i["key"], i["status"], i.get("flags", ""), i.get("est_speech_s", ""), "/", i.get("window_ext_s", ""))
    print("ALL OK" if ok_all else "À corriger avant intégration")
if __name__ == "__main__": main()
