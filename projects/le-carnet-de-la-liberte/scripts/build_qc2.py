#!/usr/bin/env python3
"""QC2 NON FINAL (autorisé 18/11/2026) = état QC1 (build_animatic_v2, non modifié) + UNIQUEMENT les substitutions visuelles de
docs/SUBSTITUTIONS_PREVUES_QC1_vers_QC2_v2.md : SH13 coupe franche ; SH14 travelling ; SH15 plan fixe ; SH16 mention 38 px ;
SH27 175,0/5,5 s ; SH28 180,5/9,0 s (recul 1,05->1,0) ; SH33 frise v3c (14 s, apparition 1,5 s, vue complète stable 9-14 s).
SH25/26/34 et tous les autres plans = QC1. Audio : non produit ici (le mix QC1 est recopié tel quel au muxage).
Usage: build_qc2.py --out-name X.mp4 [--range t0 t1]   (refuse d'écraser)"""
import sys, json, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import build_animatic_v2 as B
from PIL import Image, ImageDraw
W0, H0 = B.W0, B.H0; C = (W0/2, H0/2)
CAM = {14: (1.06, 1.06, (1300, 768), (1452, 768)), 15: (1.03, 1.03, C, C), 28: (1.05, 1.0, C, C)}
for n, (z0, z1, c0, c1) in CAM.items(): B.CROP[n] = (B.CROP[n][0] if n in B.CROP else B.IMG[n], z0, z1, c0, c1)
SHOT_OVR = {27: (175.0, 5.5), 28: (180.5, 9.0)}
for x in B.SHOTS:
    if x["n"] in SHOT_OVR: x["start"], x["dur"] = SHOT_OVR[x["n"]]
# fondus = exactement ceux de QC1 (build_animatic_v2.main) sauf SH13 (coupe)
DISSOLVE = ({x["n"] for x in B.SHOTS if x.get("trans_in") == "dissolve"} | {7, 13, 21, 27}) - {13, 31}
_ov = B.make_overlay
def make_overlay(s, img, t):
    img = _ov(s, img, t)
    if s["n"] == 16:
        d = ImageDraw.Draw(img, "RGBA"); txt = "ILLUSTRATION PÉDAGOGIQUE — reconstitution, non archive"; fo = B.fnt(B.DS, 38); w = d.textlength(txt, font=fo)
        d.rounded_rectangle((960-w/2-30, 962, 960+w/2+30, 1052), 14, fill=(28, 22, 16, 235)); d.text((960, 1007), txt, font=fo, fill=(255, 240, 205), anchor="mm")
    return img
B.make_overlay = make_overlay
_dov = B.CA.draw_overlay
def draw_overlay(d, s, pal, state=None, t=None):   # SH33 : frise v3c ; apparition 1,5 s/entrée (1re à 1,5 s, 6e + note à 9,0 s) puis vue complète stable
    ov = s.get("overlay") or {}
    if s["n"] != 33 or ov.get("kind") != "timeline": return _dov(d, s, pal, state, t)
    F = B.CA.font; W = B.CA.W; items = ov["items"]; n = len(items)
    d.text((W // 2, 140), "LIGNE DU TEMPS", font=F(60, serif=True, bold=True), fill=(80, 50, 30), anchor="mm")
    shown = n if t is None else (0 if t < 1.5 else min(n, int((t-1.5)/1.5)+1))
    d.line([420, 260, 420, 260 + (n - 1) * 120 + 40], fill=(120, 80, 40), width=8)
    if ov.get("footer") and shown >= n: d.text((W // 2, 940), ov["footer"], font=F(34, bold=True), fill=(120, 40, 30), anchor="mm")
    for j, (dt, tx) in enumerate(items[:shown]):
        y = 270 + j * 120
        d.ellipse([402, y - 4, 438, y + 32], fill=(170, 60, 40))
        d.text((480, y + 14), dt, font=F(42, bold=True), fill=(70, 40, 20), anchor="lm")
        d.text((960, y + 14), tx, font=F(32), fill=(50, 35, 25), anchor="lm")
B.CA.draw_overlay = draw_overlay
def main():
    a = sys.argv; name = a[a.index("--out-name")+1]; out = B.OUT/"qc2"/name
    if out.exists(): sys.exit("refus : fichier existant")
    t0, t1 = (float(a[a.index("--range")+1]), float(a[a.index("--range")+2])) if "--range" in a else (0.0, 1e9)
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{B.FW}x{B.FH}", "-r", str(B.FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(B.FPS), "-an", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    prev = None; rep = []
    for s in B.SHOTS:
        n = s["n"]; s0, s1 = s["start"], s["start"]+s["dur"]
        if s1 <= t0 or s0 >= t1: continue
        nfr = int(round(s["dur"]*B.FPS)); rd = B.ClipReader(B.CLIP[n]) if n in B.CLIP else None
        tr = int(0.5*B.FPS) if (n in DISSOLVE and prev is not None) else 0
        for f in range(nfr):
            t = f/B.FPS; u = f/max(1, nfr-1); fr = rd.next() if rd is not None else None
            if fr is None:
                c = B.frame_custom(s, t)
                if c is not None: fr = c
                elif n in B.CROP: src, z0, z1, c0, c1 = B.CROP[n]; fr = B.cam_frame(B.load(src), z0, z1, c0, c1, u)
                else: z0, z1 = B.CAMZ[s["cam"]]; fr = B.cam_frame(B.load(B.IMG[n]), z0, z1, (W0/2, H0/2), (W0/2, H0/2), u)
            fr = B.make_overlay(s, fr.copy(), t)
            if f < tr: fr = Image.blend(prev, fr, B.ease(f/tr))
            if n == 31 and t < 0.4: fr = Image.blend(Image.new("RGB", (B.FW, B.FH), (0, 0, 0)), fr.convert("RGB"), B.ease(t/0.4))
            if t0 <= s0+t < t1: ff.stdin.write(fr.convert("RGB").tobytes())
        prev = fr.convert("RGB")
        if rd: rd.close()
        rep.append({"shot": n, "start": s0, "dur": s["dur"], "frames": nfr, "transition_in": "fondu 0,5 s" if tr else "coupe"})
    ff.stdin.close(); ff.wait(); out.with_suffix(".json").write_text(json.dumps(rep, indent=1, ensure_ascii=False)); print("done", out)
if __name__ == "__main__": main()
