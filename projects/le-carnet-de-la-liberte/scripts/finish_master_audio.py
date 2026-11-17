#!/usr/bin/env python3
"""Classroom finishing chain, two-pass (local, FFmpeg only). Usage: finish_master_audio.py <src_version> <new_version>
Reads audio/mixes/<src>/mix_premaster.wav, writes audio/mixes/<new>/MIX_276s_<new>.wav (+ report). Never overwrites an existing version.
Chain: high-pass 70 Hz -> gentle compression (3:1) -> loudnorm two-pass (-16 LUFS integrated, TP -1.0, linear) -> limiter (-1.5 dBFS ceiling)."""
import sys, json, subprocess, re
from pathlib import Path
A = Path(__file__).resolve().parent.parent/"audio"; src, new = sys.argv[1], sys.argv[2]
OUT = A/"mixes"/new
if OUT.exists(): sys.exit(f"{OUT} exists")
OUT.mkdir(parents=True)
pre = "highpass=f=70,acompressor=threshold=-31dB:ratio=3:attack=15:release=400:makeup=5"
i = str(A/"mixes"/src/"mix_premaster.wav")
o1 = subprocess.run(["ffmpeg", "-nostats", "-i", i, "-af", pre+",loudnorm=I=-16:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(o1[o1.rindex("{"):o1.rindex("}")+1])
ln = f"loudnorm=I=-16:TP=-1.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
out = str(OUT/f"MIX_276s_{new}.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", i, "-af", f"{pre},{ln},alimiter=limit=0.84:level=disabled:attack=1:release=60", "-ar", "48000", "-ac", "2", out], check=True)
o2 = subprocess.run(["ffmpeg", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
res = {"integrated_lufs": float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o2)[-1]), "lra": float(re.findall(r"LRA:\s+(-?[\d.]+) LU", o2)[-1]), "true_peak_dbtp": float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", o2)[-1])}
(OUT/"finish_report.json").write_text(json.dumps({"source": src, "chain": pre+" | loudnorm 2-pass | alimiter", "result": res}, indent=1)); print(res)
