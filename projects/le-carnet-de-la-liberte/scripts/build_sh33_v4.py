#!/usr/bin/env python3
"""SH33 v4 (ajustement local, NON VALIDÉ) — « ligne du temps » : mêmes textes historiques (6 entrées + note, inchangés), mêmes 14 s.
Lisibilité : date 46 px gras, description 36 px (au lieu de 32) sur une ligne sous la date, note 34 px gras, contraste renforcé ; rendu en 2x (3840x2160)
puis recadrage caméra -> texte net même en zoom. Mouvement : chaque entrée apparaît en fondu (0,6 s, glissement 16 px) pendant qu'un léger travelling/zoom
(zoom 1,12 max, trajectoire lissée par noyau gaussien, vitesse continue) accompagne l'entrée active ; retour à la vue d'ensemble à 10,8 s, puis vue stable
de 12,0 s à 14,0 s (images strictement identiques). Aucun autre plan modifié ; v3c et QC1 intacts.
Usage: build_sh33_v4.py --out-name X.mp4 --range 225.5 239.5 (refuse d'écraser)."""
import sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import build_animatic_v3 as V
from PIL import Image, ImageDraw
B = V.B; F = B.CA.font; K = 2; W, H = 1920*K, 1080*K
ITEMS = [('11 janvier 1944', "Manifeste de l'indépendance."), ('20 août 1953', 'Exil du souverain.'), ('16 novembre 1955', 'Son retour.'),
         ('18 novembre 1955', 'Discours du Trône.'), ('2 mars 1956', "Reconnaissance française de l'indépendance."), ('7 avril 1956', 'Fin du protectorat espagnol dans le Nord.')]
FOOT = "Le processus d'unification territoriale s'est poursuivi après 1956."
S33 = next(s for s in B.SHOTS if s["n"] == 33); ov = S33["overlay"]
assert [tuple(i) for i in ov["items"]] == ITEMS and ov["footer"] == FOOT, "textes historiques modifiés ?"
DUR, FPS = S33["dur"], B.FPS; T0 = [0.8+1.7*j for j in range(6)]; FADE = 0.6; Y0, PITCH, DESC_DY = 262, 112, 50
def ss(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
def grad():
    y = np.linspace(0, 1, H)[:, None, None]; top = np.array([237, 198, 118]); bot = np.array([224, 159, 79]); return (top*(1-y)+bot*y)*np.ones((1, W, 1))
def build_layers():
    base = Image.fromarray(grad().astype(np.uint8), "RGB").convert("RGBA"); d = ImageDraw.Draw(base)
    d.rounded_rectangle([200*K, 70*K, 1720*K, 1010*K], 24*K, fill=(237, 221, 179, 255), outline=(130, 95, 55, 255), width=6*K)
    d.text((960*K, 140*K), "LIGNE DU TEMPS", font=F(60*K, serif=True, bold=True), fill=(80, 50, 30), anchor="mm")
    d.line([420*K, Y0*K, 420*K, (Y0+5*PITCH+8)*K], fill=(120, 80, 40), width=8*K)
    rows = []
    for j, (dt, tx) in enumerate(ITEMS):
        y = Y0+j*PITCH; box = (380*K, (y-34)*K, 1720*K, (y+DESC_DY+40)*K); L = Image.new("RGBA", (box[2]-box[0], box[3]-box[1]), (0, 0, 0, 0)); e = ImageDraw.Draw(L); ox, oy = box[0], box[1]
        e.ellipse([402*K-ox, (y-18)*K-oy, 438*K-ox, (y+18)*K-oy], fill=(170, 60, 40, 255))
        e.text((480*K-ox, y*K-oy), dt, font=F(46*K, bold=True), fill=(60, 34, 16), anchor="lm")
        e.text((480*K-ox, (y+DESC_DY)*K-oy), tx, font=F(36*K), fill=(38, 26, 18), anchor="lm"); rows.append((L, box))
    fo = Image.new("RGBA", (1520*K, 70*K), (0, 0, 0, 0)); e = ImageDraw.Draw(fo); e.text((760*K, 35*K), FOOT, font=F(34*K, bold=True), fill=(120, 40, 30), anchor="mm")
    return base, rows, (fo, (200*K, 925*K))
BASE, ROWS, FOOTL = build_layers()
# ---- camera path (zoom, centre y in 1x px), piecewise-linear waypoints then Gaussian-smoothed
ZF = 1.12
def focus(j): return min(max(Y0+j*PITCH+25, 540/ZF+0), 1080-540/ZF)
wp = [(0.0, 1.0, 540.0), (0.9, ZF, focus(0))]
for j in range(6):
    wp += [(T0[j]+0.8 if j < 5 else 9.8, ZF, focus(j))]
    if j < 5: wp += [(T0[j+1], ZF, focus(j+1))]
wp += [(10.8, 1.0, 540.0), (DUR, 1.0, 540.0)]
tt = np.arange(0, int(round(DUR*FPS)))/FPS; zz = np.interp(tt, [w[0] for w in wp], [w[1] for w in wp]); cy = np.interp(tt, [w[0] for w in wp], [w[2] for w in wp])
def smooth(x, sig=0.4):
    k = np.exp(-0.5*(np.arange(-int(3*sig*FPS), int(3*sig*FPS)+1)/(sig*FPS))**2); k /= k.sum(); p = np.pad(x, (len(k)//2, len(k)//2), mode="edge"); return np.convolve(p, k, mode="valid")
zz = smooth(zz); cy = smooth(cy); stable = tt >= 12.0
zz[stable] = 1.0; cy[stable] = 540.0
def frame(t):
    i = min(len(tt)-1, int(round(t*FPS))); canvas = BASE.copy()
    for j, (L, box) in enumerate(ROWS):
        a = float(ss((t-T0[j])/FADE))
        if a <= 0: continue
        Lr = L.copy(); Lr.putalpha(Lr.getchannel("A").point(lambda v, a=a: int(v*a))); canvas.alpha_composite(Lr, (box[0], box[1]+int(round((1-a)*16*K))))
    af = float(ss((t-10.4)/0.8))
    if af > 0: fo = FOOTL[0].copy(); fo.putalpha(fo.getchannel("A").point(lambda v: int(v*af))); canvas.alpha_composite(fo, FOOTL[1])
    z = zz[i]; cw, ch = 1920/z, 1080/z; ox = 960-cw/2; oy = min(max(cy[i]-ch/2, 0), 1080-ch)
    return canvas.convert("RGB").resize((1920, 1080), Image.LANCZOS, box=(ox*K, oy*K, (ox+cw)*K, (oy+ch)*K))
_cache = {}
_orig = B.frame_custom
def frame_custom(s, t):
    if s["n"] != 33: return _orig(s, t)
    i = int(round(t*FPS))
    if i >= int(12.0*FPS): i = int(12.0*FPS)          # vue d'ensemble stable : même image
    if i not in _cache: _cache.clear(); _cache[i] = frame(i/FPS)
    return _cache[i]
B.frame_custom = frame_custom
if __name__ == "__main__":
    np.save("/tmp/claude-0/sh33_cam.npy", np.stack([tt, zz, cy])); V.main()
