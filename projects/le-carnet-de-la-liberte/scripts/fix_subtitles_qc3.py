#!/usr/bin/env python3
"""SRT QC3 v001 : retimings seulement (texte identique à SUBTITLES_FR_QC1.srt, sauf 2 coupures de ligne et la séparation
de « Non, Amina. »), calés sur les pauses mesurées dans le stem dialogue M6. Écrit animatic/SUBTITLES_FR_QC3_v001.srt (nouveau)."""
import re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
def ts(s): h, m, r = s.split(':'); sec, ms = r.split(','); return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
def fmt(t): ms = int(round(t*1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000); return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
raw = (R/'animatic/SUBTITLES_FR_QC1.srt').read_text(encoding='utf-8')
cues = [[ts(a), ts(b), t.strip('\n').split('\n')] for n, a, b, t in re.findall(r'(\d+)\n(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)\n(.*?)(?:\n\n|\n*\Z)', raw, re.S)]
C = {i+1: c for i, c in enumerate(cues)}
C[7][1] = 44.80; C[8][0] = 44.95
C[10][1] = 79.80; C[11][0] = 79.88                       # 2e phrase du père dite dès 79,88 s (pause 79,68-79,88)
C[13][0] = 95.06
C[14][0] = 99.70; C[14][1] = 102.06; C[15][0] = 102.14
C[15][2] = ["C'est pouvoir décider de l'avenir", "de son pays, librement et avec souveraineté."]
C[17][0] = 129.574
C[19] = [137.55, 139.20, ["Non, Amina."]]                # dit seul 137,71-138,41 ; reprise à 139,38
C[20] = [139.30, 145.30, ["Malgré les épreuves, beaucoup de Marocains", "poursuivent la lutte pour l'indépendance."]]
C[24][0] = 216.62; C[24][1] = 221.62; C[25][0] = 221.70  # début après la coupe SH31/SH32 (216,60)
C[28][0] = 253.55; C[28][1] = 258.30; C[29][0] = 258.38; C[29][1] = 260.90   # pause 258,27-258,47
C[30][1] = 262.60; C[31][0] = 262.68; C[31][1] = 265.01; C[32][1] = 269.00  # pause 264,89-265,23 ; dernière réplique tenue jusqu’à 269,0 s (avant SH38)
out = []; prev = None
for i in sorted(C):
    a, b, t = C[i]; assert b > a and (prev is None or a-prev >= 0.079), (i, a, prev); prev = b
    out.append(f"{i}\n{fmt(a)} --> {fmt(b)}\n"+"\n".join(re.sub(r" ([?!:;])", "\u00a0\\1", l) for l in t)+"\n")   # espace insécable avant ? ! : ;
O = R/'animatic/SUBTITLES_FR_QC3_v001.srt'; assert not O.exists(); O.write_text("\n".join(out), encoding='utf-8')
norm = lambda s: re.sub(r'\s+', ' ', s.replace('\u00a0', ' ')).strip()
assert norm(' '.join(' '.join(c[2]) for c in cues)) == norm(' '.join(' '.join(C[i][2]) for i in sorted(C))), "texte modifié"
for i in sorted(C):
    a, b, t = C[i]; n = len(' '.join(t)); r = n/(b-a)
    if r > 15 or max(len(l) for l in t) > 42: print('reste', i, f'{a:.2f}-{b:.2f}', f'{r:.1f} car/s', max(len(l) for l in t), 'car.')
print('écrit', O)
