#!/usr/bin/env python3
"""SH03 high-resolution gaze control sheet (local, no AI, no credit). Reads v001/v002/v005 untouched, writes references/p4/control/.
Measures: pupil centre (largest near-black blob in the near-eye box), teacher-eye target (fixed from the frame), ray angle vs horizontal."""
import numpy as np, cv2, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R = Path(__file__).resolve().parent.parent; OUT = R/"references/p4/control"; OUT.mkdir(exist_ok=True)
VERS = [("v001 (original)", R/"references/p4/SH03_younes_main_levee_v001.png"), ("v002 (régénération IA)", R/"references/p4/SH03_younes_main_levee_v002.png"), ("v005 (correction locale)", R/"references/p4/post/SH03_gaze_head_v005.png")]
TARGET = (925, 452)    # milieu des yeux de la maîtresse (flou de profondeur de champ), mesuré sur le plan
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30); FS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
def pupil(img):
    a = np.asarray(img.convert("RGB")); x0, y0, x1, y1 = 1780, 625, 1900, 700; box = a[y0:y1, x0:x1]
    v = box.max(axis=2); m = (v < 55).astype(np.uint8); m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m); best = None
    for i in range(1, n):
        if 120 < st[i, 4] < 2500 and (best is None or st[i, 4] > st[best, 4]): best = i
    return (x0+cen[best][0], y0+cen[best][1], int(st[best, 4])) if best else None
BOX = {0: dict(eye=(1050, 480, 1350, 720), head=(800, 200, 1560, 820), full=(500, 250, 2000, 900), pupil=False), 1: dict(eye=(1680, 540, 1980, 780), head=(1560, 300, 2300, 920), full=(700, 250, 2200, 900), pupil=True), 2: dict(eye=(1680, 540, 1980, 780), head=(1560, 300, 2300, 920), full=(700, 250, 2200, 900), pupil=True)}
rows = []; panels = []
for k, (name, p) in enumerate(VERS):
    im = Image.open(p).convert("RGB"); pu = pupil(im) if BOX[k]["pupil"] else None
    ang = None
    if pu:
        dx, dy = TARGET[0]-pu[0], TARGET[1]-pu[1]; ang = round(math.degrees(math.atan2(-dy, -dx)), 1)  # angle above horizontal, looking left
    rows.append({"version": name, "file": str(p.relative_to(R)), "pupil_xy": [round(pu[0], 1), round(pu[1], 1)] if pu else None, "pupil_px": pu[2] if pu else None, "target_direction_deg": ang})
    d = ImageDraw.Draw(im)
    if pu:
        d.line([(pu[0], pu[1]), TARGET], fill=(0, 255, 0), width=4); d.ellipse([TARGET[0]-45, TARGET[1]-45, TARGET[0]+45, TARGET[1]+45], outline=(255, 0, 0), width=5)
    eye = im.crop(BOX[k]["eye"]).resize((900, 720), Image.LANCZOS)
    head = Image.open(p).convert("RGB").crop(BOX[k]["head"]).resize((740, 620), Image.LANCZOS)
    full = im.crop(BOX[k]["full"]).resize((1000, 433), Image.LANCZOS)
    panels.append((name, full, eye, head))
Wd = 1000; sheet = Image.new("RGB", (Wd*len(panels)+40, 60+433+30+720+30+620+40), (24, 24, 24)); d = ImageDraw.Draw(sheet)
for i, (name, full, eye, head) in enumerate(panels):
    x = 20+i*Wd; d.text((x, 14), name, font=F, fill=(255, 220, 120)); sheet.paste(full, (x, 60)); sheet.paste(eye.resize((900, 720)), (x, 60+433+30)); sheet.paste(head, (x, 60+433+30+720+30))
d.text((20, sheet.height-34), "v001 : cadrage face caméra, regard à l'objectif, non comparable (pas de mesure). NON VALIDÉ — rayon vert = pupille -> yeux de la maîtresse (cercle rouge) ; recadrages natifs 2752x1536, agrandis x3 (yeux) et x1 (tête).", font=FS, fill=(230, 230, 230))
sheet.save(OUT/"SH03_control_hr_v001_v002_v005.png"); json.dump({"target_xy": TARGET, "rows": rows}, open(OUT/"SH03_control_measures.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(rows, ensure_ascii=False, indent=1))
