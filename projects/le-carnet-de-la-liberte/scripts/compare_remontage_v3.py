#!/usr/bin/env python3
"""Comparison clips (control only, NON FINAL, 720p): AVANT = QC1 master segment ; APRÈS = remontage v3 video segment + M8.1 audio.
Usage: compare_remontage_v3.py NAME t0 t1 VIDEO_V3 [AUDIO]  -> animatic/remontage_v3/COMPARAISON_NAME.mp4 (refuses to overwrite)."""
import sys, subprocess
from pathlib import Path
R = Path(__file__).resolve().parent.parent; V = R/"animatic/remontage_v3"
name, t0, t1, vid = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), V/sys.argv[4]
aud = R/(sys.argv[5] if len(sys.argv) > 5 else "audio/mixes/M8.1/MIX_276s_M8.1.wav")
out = V/f"COMPARAISON_{name}.mp4"
if out.exists(): sys.exit("exists")
QC1 = R/"animatic/MASTER_CANDIDATE_NON_FINAL_QC1_1080p.mp4"; FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; d = t1-t0
lab = lambda txt: f"scale=1280:720,drawbox=x=0:y=0:w=1280:h=46:color=black@0.75:t=fill,drawtext=fontfile={FONT}:text='{txt}':x=14:y=10:fontsize=26:fontcolor=0xFFDC78"
fc = (f"[0:v]trim=start={t0}:duration={d},setpts=PTS-STARTPTS,{lab('AVANT  QC1')}[v0];[0:a]atrim=start={t0}:duration={d},asetpts=PTS-STARTPTS[a0];"
      f"[1:v]trim=duration={d},setpts=PTS-STARTPTS,{lab('APRES  remontage v3 + son M8.1 (NON FINAL)')}[v1];[2:a]atrim=start={t0}:duration={d},asetpts=PTS-STARTPTS[a1];"
      f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-n", "-i", str(QC1), "-i", str(vid), "-i", str(aud), "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "22", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], check=True)
print("ok", out)
