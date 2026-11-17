#!/usr/bin/env python3
"""Delivery check: 1920x1080, H.264, AAC stereo, duration < 300 s (target 276 s). Exit 1 on failure."""
import json, subprocess, sys
f = sys.argv[1]
j = json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_name,codec_type,width,height,r_frame_rate,channels,sample_rate","-show_entries","format=duration,size","-of","json",f],capture_output=True,text=True).stdout)
v = next(s for s in j["streams"] if s["codec_type"]=="video"); a = next(s for s in j["streams"] if s["codec_type"]=="audio"); d = float(j["format"]["duration"])
chk = {"1920x1080": (v["width"],v["height"])==(1920,1080), "h264": v["codec_name"]=="h264", "aac": a["codec_name"]=="aac", "stereo": a["channels"]==2, "<300s": d<300, "~276s": abs(d-276)<2}
print(f, round(d,2), "s", round(int(j["format"]["size"])/1e6,1), "MB", chk); sys.exit(0 if all(chk[k] for k in ("1920x1080","h264","aac","stereo","<300s")) else 1)
