#!/usr/bin/env python3
"""Remontage phase 1 (autorisé 17/11) — built on build_animatic_v2 (QC1 state), which is NOT modified.
Changes: (1) camera grammar per shot (static for dialogue, lateral tracks/pans where motivated, push-ins kept only where
motivated); (2) dissolves kept only for time/era passages (SH06, SH12, SH20, SH25, SH27 from white, SH35), hard cuts elsewhere;
(3) SH16 mention and SH33 timeline text enlarged (local overlay). Same shots, same durations, same overlays/cartons, no grade.
Usage: build_animatic_v3.py --out-name X.mp4 [--range t0 t1]  (refuses to overwrite)."""
import sys, json, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import build_animatic_v2 as B
from PIL import Image, ImageDraw
W0, H0 = B.W0, B.H0; C = (W0/2, H0/2)
# ---- 1. camera plan: shot -> (zoom0, zoom1, centre0, centre1); applied as CROP on the same source image
CAM = {
  1:  (1.06, 1.06, (1300, 768), (1452, 768)),   # classe : travelling latéral lent (plan d'ensemble)
  7:  (1.05, 1.05, (1320, 768), (1420, 768)),   # Younes vers la boîte : léger panoramique accompagnant
  9:  (1.03, 1.03, C, C),                       # dialogue mère/fils : plan fixe
  14: (1.06, 1.06, (1300, 768), (1452, 768)),   # Amina et son père marchent : travelling d'accompagnement
  15: (1.03, 1.03, C, C),                       # le père explique : fixe
  18: (1.6, 1.6, (1500, 960), (1500, 960)),     # dialogue intérieur 1944 : fixe (même cadre que le recadrage QC1, sans zoom)
  26: (1.06, 1.0, C, C),                        # Amina à la fenêtre : léger recul, ouverture vers l'extérieur
  28: (1.05, 1.0, C, C),                        # Amina et son père avancent : recul de caméra (portrait reste dans le cadre)
  32: (1.03, 1.03, C, C),                       # annonce du père : fixe
}
for n, (z0, z1, c0, c1) in CAM.items(): B.CROP[n] = (B.CROP[n][0] if n in B.CROP else B.IMG[n], z0, z1, c0, c1)
DISSOLVE = {6, 12, 20, 25, 27, 35}             # passages de temps / d'époque uniquement
# ---- 3. legibility (local overlays)
_ov = B.make_overlay
def make_overlay(s, img, t):
    img = _ov(s, img, t)
    if s["n"] == 16:   # mention « non archive » agrandie (30 -> 38 px), même texte, même place
        d = ImageDraw.Draw(img, "RGBA"); txt = "ILLUSTRATION PÉDAGOGIQUE — reconstitution, non archive"; fo = B.fnt(B.DS, 38); w = d.textlength(txt, font=fo)
        d.rounded_rectangle((960-w/2-30, 962, 960+w/2+30, 1052), 14, fill=(28, 22, 16, 235)); d.text((960, 1007), txt, font=fo, fill=(255, 240, 205), anchor="mm")
    return img
B.make_overlay = make_overlay
_font = B.CA.font
def big_font(sz, bold=False, serif=False, italic=False):   # SH33 only: descriptions 28 -> 34 px, note 30 -> 34 px, dates 44 -> 48 px
    sz = {28: 34, 30: 34, 44: 48}.get(sz, sz); return _font(sz, bold, serif, italic)
_rb = B.CA.render_base
def render_base(s, t=None):
    if s["n"] != 33: return _rb(s, t)
    B.CA.font = big_font
    try: return _rb(s, t)
    finally: B.CA.font = _font
B.CA.render_base = render_base

def retime():   # PROPOSITION SH25/SH33 (comparaison seulement) : -3 s chacun, rendus à SH26/SH34 ; durée totale et répliques inchangées
    for x in B.SHOTS:
        if x["n"] == 25: x["dur"] = 9.0
        if x["n"] == 26: x["start"] = 160.5; x["dur"] = 14.5
        if x["n"] == 33: x["dur"] = 11.0
        if x["n"] == 34: x["start"] = 236.5; x["dur"] = 13.5
def main():
    if "--retime" in sys.argv: retime()
    a = sys.argv; name = a[a.index("--out-name")+1]; out = B.OUT/"remontage_v3"/name
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
            fr = make_overlay(s, fr.copy(), t)
            if f < tr: fr = Image.blend(prev, fr, B.ease(f/tr))
            if n == 31 and t < 0.4: fr = Image.blend(Image.new("RGB", (B.FW, B.FH), (0, 0, 0)), fr.convert("RGB"), B.ease(t/0.4))
            gt = s0+t
            if t0 <= gt < t1: ff.stdin.write(fr.convert("RGB").tobytes())
        prev = fr.convert("RGB")
        if rd: rd.close()
        rep.append({"shot": n, "start": s0, "dur": s["dur"], "cam": list(CAM.get(n, (None,)))[:2] if n in CAM else ("crop" if n in B.CROP else s.get("cam")), "transition_in": "fondu 0,5 s" if tr else "coupe"})
    ff.stdin.close(); ff.wait()
    out.with_suffix(".json").write_text(json.dumps(rep, indent=1, ensure_ascii=False)); print("done", out)
if __name__ == "__main__": main()
