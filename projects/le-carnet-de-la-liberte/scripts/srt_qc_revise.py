#!/usr/bin/env python3
"""SRT revision (QC 17/11): same text as SUBTITLES_FR_M5_sans_noms.srt (no word changed), re-timed on dialogue_timing.json
and re-flowed: <= 42 chars/line, <= 2 lines/cue (long lines split into consecutive cues at punctuation, time shared by
characters), no overlap (>= 120 ms gap), end = voice end + 0.35 s, extended up to +0.8 s only if reading speed > 15 cps.
Writes animatic/SUBTITLES_FR_QC1.srt (refuses to overwrite)."""
import json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent/"animatic"; OUT = R/"SUBTITLES_FR_QC1.srt"
if OUT.exists(): sys.exit("exists")
blocks = (R/"SUBTITLES_FR_M5_sans_noms.srt").read_text(encoding="utf-8").strip().split("\n\n")
texts = [" ".join(b.split("\n")[2:]).strip() for b in blocks]
T = json.loads((R/"dialogue_timing.json").read_text())["lines"]; assert len(T) == len(texts)
def wrap(s, w=42):
    out, cur = [], ""
    for word in s.split():
        if cur and len(cur)+1+len(word) > w: out.append(cur); cur = word
        else: cur = (cur+" "+word).strip()
    return out+[cur]
WEAK = {"le","la","les","de","des","du","un","une","et","en","à","a","que","qui","notre","nos","son","sa","ses","ce","cette","pour","par","sur","dans","au","aux","l'","d'","est"}
def balanced2(s):              # best 2-line split (both <= 42), most balanced, prefer after punctuation
    ws = s.split(); best = None
    for i in range(1, len(ws)):
        a, b = " ".join(ws[:i]), " ".join(ws[i:])
        if len(a) <= 42 and len(b) <= 42:
            sc = abs(len(a)-len(b)) - (10 if re.search(r"[,.;:!?»]$", a) else 0) + (12 if ws[i-1].lower() in WEAK else 0) + (60 if ws[i-1] in ("Mohammed", "Ben") else 0)
            if best is None or sc < best[0]: best = (sc, [a, b])
    return best[1] if best else None
def fits(s): return len(s) <= 42 or balanced2(s) is not None
def chunks(s):                 # fewest cues (each <= 2 lines of <= 42), split points balanced and preferably after punctuation
    if fits(s): return [s]
    ws = s.split(); best = None
    for i in range(1, len(ws)):
        a, b = " ".join(ws[:i]), " ".join(ws[i:])
        if fits(a) and fits(b):
            sc = abs(len(a)-len(b)) - (40 if re.search(r"[.!?;:]$", a) else 20 if a.endswith(",") else 0) + (12 if ws[i-1].lower() in WEAK else 0) + (60 if ws[i-1] in ("Mohammed", "Ben") else 0)
            if best is None or sc < best[0]: best = (sc, [a, b])
    if best: return best[1]
    k = len(ws)//2; return chunks(" ".join(ws[:k]))+chunks(" ".join(ws[k:]))
cues = []
for i, (tx, l) in enumerate(zip(texts, T)):
    s, e = l["start"]-0.05, l["end"]; nxt = T[i+1]["start"]-0.05-0.12 if i+1 < len(T) else 276.0
    end = min(e+0.35, nxt)
    if len(tx)/(end-s) > 15: end = max(end, min(e+0.8, nxt, s+len(tx)/15))
    cs = chunks(tx); tot = sum(len(c) for c in cs); t0 = s
    for k, c in enumerate(cs):
        t1 = end if k == len(cs)-1 else t0+(end-s)*len(c)/tot
        cues.append((t0, t1 if k == len(cs)-1 else t1-0.04, c)); t0 = t1
def tc(x): h = int(x//3600); m = int(x%3600//60); s = x%60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}".replace(",1000", ",999")
lines = []
for n, (a, b, c) in enumerate(cues, 1):
    body = [c] if len(c) <= 42 else balanced2(c)
    assert body and all(len(x) <= 42 for x in body), c
    lines.append(f"{n}\n{tc(a)} --> {tc(b)}\n"+"\n".join(body))
OUT.write_text("\n\n".join(lines)+"\n", encoding="utf-8")
cps = [len(c)/(b-a) for a, b, c in cues]; ov = sum(1 for i in range(1, len(cues)) if cues[i][0] < cues[i-1][1])
late = max(b-T[[k for k in range(len(T)) if T[k]["start"]-0.05 <= a][-1]]["end"] for a, b, c in cues)
print(f"{len(cues)} cues | max line {max(len(x) for _,_,c in cues for x in ([c] if len(c)<=42 else balanced2(c)))} | overlaps {ov} | cps max {max(cps):.1f}, >15: {sum(x>15 for x in cps)}, >17: {sum(x>17 for x in cps)} | min dur {min(b-a for a,b,_ in cues):.2f} s | max end after voice {late:.2f} s")
if (Path("/dev/stdin").exists()): pass
