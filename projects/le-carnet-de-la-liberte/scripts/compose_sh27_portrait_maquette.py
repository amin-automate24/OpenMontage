#!/usr/bin/env python3
"""SH27 portrait MAQUETTE (local, NO AI, 0 credit). Two printed-portrait cards held on sticks by the crowd, with a NEUTRAL GREY PLACEHOLDER panel
(labelled) — NO face is drawn, generated or reconstructed. Purpose: validate placement, scale, perspective, light. The authentic photograph
(Commons 'Mohammed V (1953).jpg', Nationaal Archief/Anefo) is NOT used until provenance and CC0 licence are verified and archived.
Reads references/p3/post/SH27_flags_v002.png ; writes references/p3/post/SH27_maquette_portraits_PLACEHOLDER_v002.png (never overwrites)."""
import sys, math, numpy as np, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = Path(__file__).resolve().parent.parent; SRC = R/"references/p3/post/SH27_flags_v002.png"; DST = R/"references/p3/post/SH27_maquette_portraits_PLACEHOLDER_v002.png"
if DST.exists(): sys.exit("exists")
base = Image.open(SRC).convert("RGB"); F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
def card(w, h, panel=(150, 146, 138)):
    c = Image.new("RGBA", (w+20, h+20), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rectangle([10, 10, w+10, h+10], fill=(232, 224, 205, 255)); d.rectangle([22, 22, w-2, h-2], fill=panel+(255,))
    d.text((w/2+10, h/2-8), "PORTRAIT RÉEL", font=F, fill=(60, 56, 50), anchor="mm"); d.text((w/2+10, h/2+16), "À INTÉGRER", font=F, fill=(60, 56, 50), anchor="mm")
    d.text((w/2+10, h/2+44), "NON VALIDÉ", font=F, fill=(150, 30, 30), anchor="mm"); return c
def place(img, cx, cy, w, h, rot, stick_to):
    c = card(w, h).rotate(rot, expand=True, resample=Image.BICUBIC)
    # warm grade + slight haze so it sits in the scene
    arr = np.asarray(c).astype(np.float32); arr[..., :3] = arr[..., :3]*np.array([1.0, 0.96, 0.88])*0.96+np.array([236, 206, 168])*0.04; c = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(img, "RGBA"); bx, by = cx, cy+h/2
    d.line([(bx, by), stick_to], fill=(150, 112, 60, 255), width=7)                    # stick held in the raised hand
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sh.paste((40, 30, 20, 90), mask=c.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(6))
    img.paste(sh, (int(cx-c.width/2+8), int(cy-c.height/2+10)), sh); img.paste(c, (int(cx-c.width/2), int(cy-c.height/2)), c)
place(base, 1075, 735, 150, 195, -3, (1072, 868)); place(base, 2640, 622, 150, 195, 3, (2632, 742))
base.save(DST); print("ok", DST.name)
