#!/usr/bin/env python3
"""Générique de fin (MAQUETTE, NON FINAL) — 10,0 s, 1920×1080, 25 fps, fond sombre, ivoire et or, fondus doux.
Polices OFL (assets/fonts/ofl) : Cinzel (titres), Cormorant Garamond (texte), Amiri (arabe). Audio : silence (aucune nouvelle musique).
Usage : python3 scripts/build_generique_fin.py --out animatic/qc2/GENERIQUE_FIN_v001.mp4 [--sans-credit-photo]"""
import sys, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = Path(__file__).resolve().parent.parent; FD = R/"assets/fonts/ofl"; W, H, FPS, DUR = 1920, 1080, 25, 10.0
a = sys.argv; OUT = R/a[a.index("--out")+1]; PHOTO = "--sans-credit-photo" not in a
assert not OUT.exists(), "refus d'écraser"
F = lambda f, s: ImageFont.truetype(str(FD/f), s, layout_engine=ImageFont.Layout.RAQM)
CIN5, CIN7 = "cinzel-latin-500-normal.woff", "cinzel-latin-700-normal.woff"; COR5, COR6 = "cormorant-garamond-latin-500-normal.woff", "cormorant-garamond-latin-600-normal.woff"; AMI = "amiri-arabic-400-normal.woff"
IVORY, GOLD = (242, 232, 213), (201, 164, 92)
def bg():
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx-W/2)/(W*0.62))**2+((yy-H/2)/(H*0.62))**2)
    base = np.array([20, 16, 13], np.float32); g = (base*(1.25-0.55*np.clip(r, 0, 1.3)))[..., None] if False else None
    k = np.clip(1.15-0.6*r, 0.45, 1.15)[..., None]; img = np.clip(base*k, 0, 255)
    img += np.random.default_rng(18).normal(0, 1.2, (H, W, 1))               # grain très léger (évite le banding au projecteur)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
BG = bg()
def ease(x): x = min(1, max(0, x)); return x*x*(3-2*x)
# éléments : (texte, police, taille, couleur, y, t_in, t_out, espacement des lettres, direction)
L = [("LE CARNET DE LA LIBERTÉ", CIN5, 62, GOLD, 300, 0.9, 5.7, 6, None),
     ("Court-métrage écrit, réalisé et produit par", COR5, 46, IVORY, 455, 1.5, 5.7, 0, None),
     ("AMIN BENHIDA", CIN7, 116, IVORY, 560, 1.9, 5.7, 10, None),
     ("Enseignant à l’École communautaire de Tiddas", COR5, 44, IVORY, 690, 2.5, 5.7, 0, None),
     ("Dieu, la Patrie, le Roi", COR6, 66, GOLD, 395, 6.3, 9.3, 1, None),
     ("الله، الوطن، الملك", AMI, 84, GOLD, 520, 6.6, 9.3, 0, "rtl")]
CREDIT = ["Photographie : Mohammed V et son fils Moulay Hassan, Paris, 5 août 1931 — Agence Rol.",
          "Source : gallica.bnf.fr / Bibliothèque nationale de France."]
def text_layer(txt, font, size, col, y, alpha, spacing, direction, dy=0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); f = F(font, size)
    if spacing:
        ws = [d.textlength(ch, font=f) for ch in txt]; tw = sum(ws)+spacing*(len(txt)-1); x = W/2-tw/2
        for ch, w_ in zip(txt, ws): d.text((x, y+dy), ch, font=f, fill=col+(int(255*alpha),), anchor="lm"); x += w_+spacing
    else:
        d.text((W/2, y+dy), txt, font=f, fill=col+(int(255*alpha),), anchor="mm", direction=direction)
    return lay
def frame(t):
    img = BG.copy()
    for (txt, font, size, col, y, ti, to, sp, dr) in L:
        al = ease((t-ti)/0.8)*(1-ease((t-to)/0.6)); dy = 14*(1-ease((t-ti)/1.2))       # fondu + légère montée
        if al > 0: img = Image.alpha_composite(img, text_layer(txt, font, size, col, y, al, sp, dr, dy))
    # filets dorés
    for (y, ti, to) in ((370, 1.2, 5.7), (465, 6.5, 9.3)):
        al = ease((t-ti)/0.8)*(1-ease((t-to)/0.6)); wl = 260*ease((t-ti)/1.0)
        if al > 0:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).line([(W/2-wl, y), (W/2+wl, y)], fill=GOLD+(int(200*al),), width=2); img = Image.alpha_composite(img, lay)
    if PHOTO:
        al = ease((t-7.0)/0.8)*(1-ease((t-9.3)/0.6))
        if al > 0:
            for i, s in enumerate(CREDIT): img = Image.alpha_composite(img, text_layer(s, COR5, 36, IVORY, 836+i*48, al*0.85, 0, None))
    out = img.convert("RGB")
    if t > 9.3: out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), ease((t-9.3)/0.7))
    if t < 0.6: out = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), out, ease(t/0.6))
    return out
OUT.parent.mkdir(parents=True, exist_ok=True)
ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-f", "lavfi", "-t", str(DUR), "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(OUT)], stdin=subprocess.PIPE)
for i in range(int(DUR*FPS)): ff.stdin.write(frame(i/FPS).tobytes())
ff.stdin.close(); ff.wait(); print("écrit", OUT)
