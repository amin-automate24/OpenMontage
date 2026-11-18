#!/usr/bin/env python3
"""MAQUETTES (NON FINAL, non intégrées) : SH06 sans superposition craie/carton ; SH33 apparitions accélérées (frise complète ~8 s).
Réutilise la chaîne QC2 (build_qc2) en remplaçant uniquement le rendu de SH06 et le calendrier d'apparition de SH33. Écrit des fichiers neufs dans animatic/qc2/."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); sys.argv += [] 
import numpy as np
from PIL import Image, ImageDraw
import build_qc2 as Q2
B = Q2.B
_fc = B.frame_custom
def frame_custom(s, t):
    if s["n"] != 6: return _fc(s, t)
    u = t/s["dur"]
    a = B.cam_frame(B.load(B.IMG[2]), 2.6, 3.0, (1650, 520), (1650, 520), u)          # même cadrage tableau que QC2
    p = B.paper(); fr = Image.blend(a, p, B.ease(float(np.clip((t-0.40)/0.90, 0, 1))))   # 1) la craie disparaît sous la page (27,9–28,8 s)
    k = B.ease(float(np.clip((t-1.30)/0.40, 0, 1)))                                    # 2) PUIS « 18 novembre » apparaît (28,8–29,2 s) : aucune superposition
    if k > 0:
        lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text((B.FW//2, B.FH//2), "18 novembre", font=B.fnt(B.AM, 200), fill=(70, 42, 24, int(255*k)), anchor="mm")
        fr = Image.alpha_composite(fr.convert("RGBA"), lay).convert("RGB")
    return fr
B.frame_custom = frame_custom
REV = [0.6, 1.4, 2.3, 3.3, 4.5, 6.0]                                                  # SH33 : intervalles 0,8→1,5 s ; frise complète à 6,0 s => 8,0 s de lecture
F = B.CA.font; W = B.CA.W
def draw_overlay(d, s, pal, state=None, t=None):
    ov = s.get("overlay") or {}
    if s["n"] != 33 or ov.get("kind") != "timeline": return Q2._dov(d, s, pal, state, t)
    items = ov["items"]; n = len(items)
    d.text((W // 2, 140), "LIGNE DU TEMPS", font=F(60, serif=True, bold=True), fill=(80, 50, 30), anchor="mm")
    shown = n if t is None else sum(t >= r for r in REV)
    d.line([420, 260, 420, 260 + (n - 1) * 120 + 40], fill=(120, 80, 40), width=8)
    if ov.get("footer") and shown >= n: d.text((W // 2, 940), ov["footer"], font=F(34, bold=True), fill=(120, 40, 30), anchor="mm")
    for j, (dt, tx) in enumerate(items[:shown]):
        y = 270 + j * 120
        d.ellipse([402, y - 4, 438, y + 32], fill=(170, 60, 40))
        d.text((480, y + 14), dt, font=F(42, bold=True), fill=(70, 40, 20), anchor="lm")
        d.text((960, y + 14), tx, font=F(32), fill=(50, 35, 25), anchor="lm")
B.CA.draw_overlay = draw_overlay
if __name__ == "__main__": Q2.main()
