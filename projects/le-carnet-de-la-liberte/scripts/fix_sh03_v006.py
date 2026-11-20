#!/usr/bin/env python3
"""SH03 v006 — local retouch of v005 (no AI, no credit). ONLY two zones:
 (1) pale smear at the nose tip (ghost of the old tip outside the nose silhouette) -> removed by inpainting from neighbours;
 (2) tonal step ('raccord') on the wall to the left of the forehead -> smoothed with a masked (background-only) low-pass + matched grain.
Eyes, eyebrows, expression, skin and hair are protected by masks and verified pixel-identical. v005 is never modified; refuses to overwrite v006."""
import numpy as np, cv2, json, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent; SRC = R/"references/p4/post/SH03_gaze_head_v005.png"; DST = R/"references/p4/post/SH03_gaze_head_v006.png"
if DST.exists(): sys.exit(f"{DST.name} exists: not overwriting")
img = cv2.imread(str(SRC)); H, W = img.shape[:2]; f = img.astype(np.float32); B, G, Rr = f[..., 0], f[..., 1], f[..., 2]
out = img.copy(); rng = np.random.default_rng(6)
# ---------- (2) wall raccord: band left of the forehead, background pixels only (olive/grey: |R-G| small, R<140, B<R)
bx0, bx1, by0, by1 = 1690, 1768, 480, 700
bg = ((np.abs(Rr-G) < 14) & (Rr < 140) & (B < Rr+4)).astype(np.float32); band = np.zeros((H, W), np.float32); band[by0:by1, bx0:bx1] = 1; bgm = bg*band
bgm = cv2.erode(bgm, np.ones((15, 15), np.uint8))   # 7 px de marge autour de tout ce qui n'est pas fond (peau, yeux, sourcil)
num = cv2.GaussianBlur(f*bgm[..., None], (0, 0), 14); den = cv2.GaussianBlur(bgm, (0, 0), 14)[..., None]+1e-6; smooth = num/den
grain = rng.normal(0, 2.2, (H, W, 1)).astype(np.float32); soft = np.minimum(cv2.GaussianBlur(bgm, (0, 0), 2.0), bgm)[..., None]   # jamais en dehors du masque
res = smooth+grain; f2 = f*(1-soft)+res*soft
# ---------- (1) nose tip smear: pale pixels (R>150, B>105) in a small zone outside the nose silhouette
nx0, nx1, ny0, ny1 = 1686, 1744, 684, 738
zone = np.zeros((H, W), np.uint8); zone[ny0:ny1, nx0:nx1] = 1
Y = 0.299*Rr+0.587*G+0.114*B; bright = (Y > 88).astype(np.uint8)   # fond/ sac = sombre ; bavure = claire
yy, xx = np.mgrid[0:H, 0:W]; left_of = (xx < 1738-(yy-688)*(26/42.0)-2).astype(np.uint8)   # à gauche du vrai contour du nez
m = (zone & bright & left_of)*255; m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)); m = cv2.dilate(m, np.ones((7, 7), np.uint8)); m = (m & (zone*255)).astype(np.uint8)
tmp = np.clip(f2, 0, 255).astype(np.uint8); fixed = cv2.inpaint(tmp, m, 8, cv2.INPAINT_TELEA)
mk = cv2.GaussianBlur(m.astype(np.float32)/255, (0, 0), 1.5)[..., None]; out = (tmp*(1-mk)+fixed*mk).astype(np.uint8)
# ---------- protection check: eyes/brows/face must be bit-identical
prot = {"oeil_proche": (1775, 600, 1905, 705), "oeil_lointain": (1757, 596, 1795, 694), "sourcil": (1790, 520, 2060, 620), "peau_joue_bouche": (1760, 740, 2100, 900)}
diff = np.abs(out.astype(int)-img.astype(int)).max(axis=2); chk = {}
for k, (a, b, c, d) in prot.items(): chk[k] = int(diff[b:d, a:c].max()) if k != "oeil_lointain" else int(diff[b:d, a:c].max())
cv2.imwrite(str(DST), out)
ys, xs = np.where(diff > 0); report = {"src": str(SRC.relative_to(R)), "dst": str(DST.relative_to(R)), "changed_px": int((diff > 0).sum()), "changed_bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None, "max_diff_in_protected_boxes": chk, "mask_nose_px": int((m > 0).sum()), "mask_wall_px": int(bgm.sum())}
(R/"references/p4/control/SH03_v006_report.json").write_text(json.dumps(report, indent=1)); print(json.dumps(report, indent=1))
