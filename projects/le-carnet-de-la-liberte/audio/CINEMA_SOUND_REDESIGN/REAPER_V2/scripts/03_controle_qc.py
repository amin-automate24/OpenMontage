#!/usr/bin/env python3
"""Contrôle technique d'un export REAPER (FFmpeg requis dans le PATH ; numpy facultatif pour la synchronisation).
Mesures uniquement — aucune écoute n'est remplacée. Usage : python 03_controle_qc.py exports\\MIX.wav [media\\REF_master_FINAL_audio_299s_AAC_decode.flac] [début_en_s]  (début déduit du nom TEST_COURT_X_268-299)
Vérifie : durée (299,000 s ±1 image), écrêtage, crête vraie, sonie intégrée, LRA, perte en mono, silences > 0,5 s sous −60 dBFS, synchronisation contre la référence."""
import subprocess, re, sys, json
def ff(args): return subprocess.run(["ffmpeg","-nostdin","-hide_banner"]+args, capture_output=True, text=True).stderr
import os as _o
def ref_at(ref, a, b):
    """Référence master : fichier unique, ou 2 parties (0–150 s / 150–299 s) si le fichier complet est absent. Renvoie (fichier, début, fin) relatifs au fichier choisi."""
    if ref and _o.path.exists(ref): return ref, a, b
    base = _o.path.dirname(ref) if ref else "media"; p1 = _o.path.join(base, "REF_master_FINAL_audio_part1_0-150s.flac"); p2 = _o.path.join(base, "REF_master_FINAL_audio_part2_150-299s.flac")
    return (p1, a, b) if (a + b)/2 < 150.0 else (p2, a-150.0, b-150.0)
def probe(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p], capture_output=True, text=True).stdout)
def rms(args): return float(re.findall(r"RMS level dB:\s*(-?[\d.]+|-inf)", ff(args))[-1].replace("-inf","-200"))
def qc(p, ref=None, off=0.0):
    import os
    m_ = re.search(r"(\d+)-(\d+)\D*$", os.path.splitext(os.path.basename(p))[0])
    if m_ and off == 0.0: off = float(m_.group(1))          # TEST_COURT_C_268-299 : début de la fenêtre dans le film
    r = {"fichier": p, "début_dans_le_film_s": off, "durée_s": round(probe(p), 3)}
    r["durée_ok"] = abs(r["durée_s"]-299.0) <= 0.04 if off == 0.0 else (abs(r["durée_s"]-float(m_.group(2))+off) <= 0.04 if m_ else None)
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
        lines = [(float(x["in_s"])-off, float(x["out_s"])-off) for x in _csv.DictReader(open(man, encoding="utf-8")) if float(x["in_s"]) >= off and float(x["out_s"]) <= off + r["durée_s"]]
        lv = lambda q, a, b: rms(["-ss", str(a), "-t", str(b-a), "-i", q, "-af", "astats", "-f", "null", "-"])
        d = [(a+off, round(lv(p, a, b), 1), round(lv(ref_at(ref, a+off, b+off)[0], *ref_at(ref, a+off, b+off)[1:]), 1) if ref else None) for a, b in lines]
        r["dialogues_RMS_dBFS"] = [{"réplique_s": a, "export": x, "référence": y, "écart_dB": (round(x-y, 1) if y is not None else None)} for a, x, y in d]
        xs = [x for _, x, _ in d]
        if xs: r["dialogues_étendue_max_min_dB"] = round(max(xs)-min(xs), 1)
        if ref and xs: ys = [y for *_, y in d]; r["dialogues_étendue_référence_dB"] = round(max(ys)-min(ys), 1)
    if ref:
        try:
            import numpy as np
            rd = lambda q, ss: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(ss),"-t","20","-i",q,"-ac","1","-ar","48000","-f","f32le","-"],capture_output=True).stdout,"<f4")
            res = []; D = r["durée_s"]; L = min(10.0, 0.2*D)
            for fr in (0.1, 0.5, 0.8):
                ss = fr*D
                rd2 = lambda q, s0: np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(s0),"-t",str(L),"-i",q,"-ac","1","-ar","48000","-f","f32le","-"],capture_output=True).stdout,"<f4")
                rf = ref_at(ref, ss+off, ss+off+L); x, y = rd2(p, ss), rd2(rf[0], rf[1])
                if len(y) == 0 or float((y**2).mean()) < 1e-9: res.append({"position_dans_l_export_s": round(ss, 1), "résultat": "non applicable : la référence est silencieuse ici (ex. générique)"}); continue
                n = 2**21; X = np.fft.rfft(x, n); Y = np.fft.rfft(y, n); c = np.fft.irfft(X*np.conj(Y), n); k = int(np.argmax(np.abs(c))); k = k if k < n//2 else k-n
                res.append({"position_dans_l_export_s": round(ss, 1), "décalage_échantillons": k, "corrélation_normalisée": round(float(np.abs(c).max()/np.sqrt((x**2).sum()*(y**2).sum()+1e-30)), 3)})
            r["synchronisation_vs_référence"] = res
        except ImportError: r["synchronisation_vs_référence"] = "numpy absent : test non fait"
    return r
if __name__ == "__main__":
    out = qc(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, float(sys.argv[3]) if len(sys.argv) > 3 else 0.0); print(json.dumps(out, indent=1, ensure_ascii=False))
