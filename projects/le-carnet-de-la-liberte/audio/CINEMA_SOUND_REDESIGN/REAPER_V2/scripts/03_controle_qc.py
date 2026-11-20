#!/usr/bin/env python3
"""Contrôle technique d'un export REAPER (FFmpeg requis dans le PATH ; numpy facultatif pour la synchronisation).
Mesures uniquement — aucune écoute n'est remplacée. Usage : python 03_controle_qc.py exports\\MIX.wav [media\\REF_master_FINAL_audio_299s_AAC_decode.flac]
Vérifie : durée (299,000 s ±1 image), écrêtage, crête vraie, sonie intégrée, LRA, perte en mono, silences > 0,5 s sous −60 dBFS, synchronisation contre la référence."""
import subprocess, re, sys, json
def ff(args): return subprocess.run(["ffmpeg","-nostdin","-hide_banner"]+args, capture_output=True, text=True).stderr
def probe(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p], capture_output=True, text=True).stdout)
def rms(args): return float(re.findall(r"RMS level dB:\s*(-?[\d.]+|-inf)", ff(args))[-1].replace("-inf","-200"))
def qc(p, ref=None):
    r = {"fichier": p, "durée_s": round(probe(p), 3)}; r["durée_ok_299s_±0,04"] = abs(r["durée_s"]-299.0) <= 0.04
    e = ff(["-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"]).split("Summary:")[-1]; g = lambda k: float(re.findall(k+r":\s+(-?[\d.]+)", e)[0])
    r.update({"sonie_intégrée_LUFS": g("I"), "LRA_LU": g("LRA"), "crête_vraie_dBTP": g("Peak")}); r["crête_vraie_ok_≤−1"] = r["crête_vraie_dBTP"] <= -1.0
    a = ff(["-i", p, "-af", "astats=measure_overall=Peak_level+Number_of_samples:measure_perchannel=none", "-f", "null", "-"])
    pk = re.findall(r"Peak level dB:\s*(-?[\d.]+)", a); r["crête_échantillon_dBFS"] = float(pk[-1]) if pk else None; r["écrêtage_probable"] = (r["crête_échantillon_dBFS"] or -99) >= -0.01
    r["perte_mono_dB"] = round(rms(["-i", p, "-af", "pan=mono|c0=0.5*c0+0.5*c1,astats", "-f", "null", "-"]) - rms(["-i", p, "-af", "astats", "-f", "null", "-"]), 2)
    s = ff(["-i", p, "-af", "silencedetect=noise=-60dB:d=0.5", "-f", "null", "-"])
    r["silences_>0,5s_sous_−60dBFS"] = [(float(a_), float(b_)) for a_, b_ in zip(re.findall(r"silence_start: (-?[\d.]+)", s), re.findall(r"silence_end: ([\d.]+)", s))]
    # dynamique des dialogues : RMS de chaque réplique (fenêtres du manifeste), écart max–min, et différence avec la référence
    import csv as _csv, os as _os
    man = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "manifest", "dialogue_lines.csv")
    if _os.path.exists(man):
        lines = [(float(x["in_s"]), float(x["out_s"])) for x in _csv.DictReader(open(man, encoding="utf-8"))]
        lv = lambda q, a, b: rms(["-ss", str(a), "-t", str(b-a), "-i", q, "-af", "astats", "-f", "null", "-"])
        d = [(a, round(lv(p, a, b), 1), round(lv(ref, a, b), 1) if ref else None) for a, b in lines]
        r["dialogues_RMS_dBFS"] = [{"réplique_s": a, "export": x, "référence": y, "écart_dB": (round(x-y, 1) if y is not None else None)} for a, x, y in d]
        xs = [x for _, x, _ in d]; r["dialogues_étendue_max_min_dB"] = round(max(xs)-min(xs), 1)
        if ref: ys = [y for *_, y in d]; r["dialogues_étendue_référence_dB"] = round(max(ys)-min(ys), 1)
    if ref:
        try:
            import numpy as np
            rd = lambda q, ss: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(ss),"-t","20","-i",q,"-ac","1","-ar","48000","-f","f32le","-"],capture_output=True).stdout,"<f4")
            res = []
            for ss in (40.0, 170.0, 250.0):
                x, y = rd(p, ss), rd(ref, ss); n = 2**21; X = np.fft.rfft(x, n); Y = np.fft.rfft(y, n); c = np.fft.irfft(X*np.conj(Y), n); k = int(np.argmax(np.abs(c))); k = k if k < n//2 else k-n
                res.append({"fenêtre_s": ss, "décalage_échantillons": k, "corrélation_normalisée": round(float(np.abs(c).max()/np.sqrt((x**2).sum()*(y**2).sum())), 3)})
            r["synchronisation_vs_référence"] = res
        except ImportError: r["synchronisation_vs_référence"] = "numpy absent : test non fait"
    return r
if __name__ == "__main__":
    out = qc(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None); print(json.dumps(out, indent=1, ensure_ascii=False))
