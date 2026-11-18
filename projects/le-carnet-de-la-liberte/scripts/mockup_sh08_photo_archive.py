#!/usr/bin/env python3
"""MAQUETTE SH08 (NON FINAL) : remplace la photographie de famille générée par la photo d'archive BnF / Agence Rol n° 156948
(Mohammed V et son fils Moulay Hassan, Hôtel de Crillon, Paris, 5 août 1931 ; domaine public). Seules opérations : recadrage hors
annotations d'inventaire, projection en perspective dans le tirage existant, tonalité sépia globale, vignette et grain légers.
Aucun visage généré ni retouché. Écrit un nouveau fichier ; l'original SH08_composite_final.png est conservé."""
import numpy as np
from pathlib import Path
from PIL import Image, ImageFilter, ImageDraw
R = Path(__file__).resolve().parent.parent
SRC = R/"references/p4/post/SH08_composite_final.png"; PH = R/"references/p4/post/sh08_photo_archive/BnF_Rol_156948_btv1b53248904z_1920px.jpg"
OUT = R/"references/p4/post/SH08_composite_photo_BnF_Rol156948_v002.png"
assert not OUT.exists(), "refus d'écraser"
src = Image.open(SRC).convert("RGB"); A = np.asarray(src).astype(np.float32); W, H = src.size
ph = Image.open(PH).convert("L").crop((400, 80, 1700, 1104)); w, h = ph.size
dst = [(1852, 726), (2282, 788), (2108, 1116), (1502, 1058)]          # TL, TR, BR, BL de l'émulsion du tirage (jusqu'au bord crème)
M, b = [], []
for (x, y), (u, v) in zip(dst, [(0, 0), (w, 0), (w, h), (0, h)]):
    M += [[x, y, 1, 0, 0, 0, -u*x, -u*y], [0, 0, 0, x, y, 1, -v*x, -v*y]]; b += [u, v]
c = np.linalg.solve(np.array(M, float), np.array(b, float))
g = np.asarray(ph.transform((W, H), Image.PERSPECTIVE, tuple(c), Image.BICUBIC, fillcolor=0).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)
poly = Image.new("L", (W, H), 0); ImageDraw.Draw(poly).polygon(dst, fill=255); P = np.asarray(poly) > 127
m = np.asarray(poly.filter(ImageFilter.GaussianBlur(2.5))).astype(np.float32)/255
mu, sd = A[P].mean(0), A[P].std(0); z = (g-g[P].mean())/(g[P].std()+1e-6)       # sépia calé sur l'ancienne émulsion
new = np.stack([mu[k]+z*sd[k]*0.95 for k in range(3)], 2)
yy, xx = np.mgrid[0:H, 0:W]; cx, cy = np.mean([p[0] for p in dst]), np.mean([p[1] for p in dst])
vig = np.clip(1-0.18*np.clip(np.sqrt(((xx-cx)/300)**2+((yy-cy)/200)**2)-0.6, 0, 1.5), 0.75, 1)[..., None]
new = new*vig + np.random.default_rng(1931).normal(0, 3.0, (H, W, 1))
out = A*(1-m[..., None]) + np.clip(new, 0, 255)*m[..., None]
Image.fromarray(out.round().astype(np.uint8)).save(OUT); print("écrit", OUT)
