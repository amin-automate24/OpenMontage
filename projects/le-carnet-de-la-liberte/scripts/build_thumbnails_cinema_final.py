#!/usr/bin/env python3
"""Vignettes YouTube « LE CARNET DE LA LIBERTÉ » (CINÉMA FINAL) — 3 propositions composées à partir des images composites du film (2752×1536, identiques aux plans du master).
Aucune génération IA, aucun crédit. Travail à 3840×2160, export 1280×720 JPEG (< 2 Mo) + PNG 3840×2160. Police OFL Cinzel (celle du générique). Refuse d'écraser.
Usage : build_thumbnails_cinema_final.py [dossier_de_sortie]"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else R/"deliverables/FINAL_CINEMA/YOUTUBE_THUMBNAILS"
W, H = 3840, 2160; CIN7 = str(R/"assets/fonts/ofl/cinzel-latin-700-normal.woff")
GOLD_TOP, GOLD_BOT, EDGE = (252, 226, 150), (207, 150, 62), (34, 20, 12)
def font(s): return ImageFont.truetype(CIN7, s, layout_engine=ImageFont.Layout.RAQM)
def cover(path, box=None):
    im = Image.open(path).convert("RGB")
    if box: im = im.crop(box)
    s = max(W/im.width, H/im.height); im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    l, t = (im.width-W)//2, (im.height-H)//2
    return im.crop((l, t, l+W, t+H)).filter(ImageFilter.UnsharpMask(radius=2.2, percent=45, threshold=2))
def grade(im, vignette=0.22, warm=0.02):
    a = np.asarray(im, np.float32)/255
    a = a*a*(3-2*a)*0.35+a*0.65                          # courbe en S douce
    a[..., 0] *= 1+warm; a[..., 2] *= 1-warm
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx-W/2)/(W*0.62))**2+((yy-H/2)/(H*0.66))**2)
    a *= (1-vignette*np.clip(r-0.45, 0, 1)**1.6*1.9)[..., None]
    return Image.fromarray((np.clip(a, 0, 1)*255).astype(np.uint8))
def scrim(im, side, strength=0.62, extent=0.58, top=0.0):
    a = np.asarray(im, np.float32); x = np.linspace(0, 1, W)
    g = np.clip(1-x/extent, 0, 1) if side == "left" else np.clip(1-(1-x)/extent, 0, 1)
    g = (g**1.7*strength)[None, :]*np.ones((H, 1))
    if top: g = np.maximum(g, (np.clip(1-np.linspace(0, 1, H)/0.5, 0, 1)**2*top)[:, None]*np.ones((1, W)))
    a *= (1-g)[..., None]*1.0+0.0; return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def line_mask(text, size, spacing, stroke=0):
    f = font(size); d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    ws = [d0.textlength(c, font=f) for c in text]; tw = int(sum(ws)+spacing*(len(text)-1))+2*stroke+8; th = int(size*1.25)+2*stroke
    m = Image.new("L", (tw, th), 0); d = ImageDraw.Draw(m); x = stroke+4
    for c, w in zip(text, ws): d.text((x, stroke+size*0.05), c, font=f, fill=255, stroke_width=stroke, anchor="la"); x += w+spacing
    return m, tw, th
def title(im, lines, x, y, align="left", rule=True):
    """lines : [(texte, taille, espacement)] ; renvoie l'image et la boîte (x0, y0, x1, y1) du bloc de texte."""
    base = im.convert("RGBA"); cy = y; boxes = []
    layers = []
    for text, size, sp in lines:
        fill, tw, th = line_mask(text, size, sp); edge, _, _ = line_mask(text, size, sp, stroke=max(5, size//26))
        ox = x if align == "left" else x-tw
        layers.append((fill, edge, ox, cy, tw, th)); boxes.append((ox, cy, ox+tw, cy+th)); cy += int(size*1.02)
    for fill, edge, ox, oy, tw, th in layers:                       # ombre portée douce
        sh = Image.new("L", (W, H), 0); sh.paste(edge, (ox-int(0), oy)); sh = sh.filter(ImageFilter.GaussianBlur(26))
        base.paste(Image.new("RGBA", (W, H), (0, 0, 0, 255)), (14, 18), sh.point(lambda v: int(v*0.8)))
    for fill, edge, ox, oy, tw, th in layers:
        eg = Image.new("RGBA", (tw, th), EDGE+(255,)); base.paste(eg, (ox-0, oy), edge.crop((0, 0, tw, th)))
        gr = np.linspace(0, 1, th)[:, None, None]; col = np.array(GOLD_TOP)*(1-gr)+np.array(GOLD_BOT)*gr
        gimg = Image.fromarray(np.broadcast_to(col, (th, tw, 3)).astype(np.uint8)).convert("RGBA")
        sx = max(5, 0)  # le remplissage est décalé du trait pour rester centré dans le contour
        stroke = max(5, int(th/1.25/26)); fm, _, _ = line_mask("", 1, 0)
        base.paste(gimg, (ox+0, oy), fill.crop((0, 0, tw, th)) if False else _shift(fill, stroke, tw, th))
    x0 = min(b[0] for b in boxes); x1 = max(b[2] for b in boxes); y1 = boxes[-1][3]
    if rule:
        d = ImageDraw.Draw(base); ry = y1+12; rw = int((x1-x0)*0.92); rx = x0 if align == "left" else x1-rw
        d.line([(rx, ry), (rx+rw, ry)], fill=GOLD_BOT+(235,), width=7)
        cx = rx+rw//2; d.polygon([(cx, ry-22), (cx+22, ry), (cx, ry+22), (cx-22, ry)], fill=GOLD_TOP+(255,))
    return base.convert("RGB"), (x0, boxes[0][1], x1, y1)
def _shift(fill, stroke, tw, th):
    m = Image.new("L", (tw, th), 0); m.paste(fill, (stroke, 0)); return m
PROPS = {
 "A_la_lueur_du_carnet": dict(src="references/p2/post/SH24_composite_final.png", crop=None, side="left", scrim=(0.70, 0.55),
     lines=[("LE CARNET", 190, 8), ("DE LA", 122, 10), ("LIBERTÉ", 276, 11)], pos=(210, 150), align="left"),
 "B_le_carnet_d_Amina": dict(src="references/p1/post/SH10_composite_final.png", crop=None, side="left", scrim=(0.55, 0.62),
     lines=[("LE CARNET", 250, 10), ("DE LA LIBERTÉ", 188, 8)], pos=(230, 120), align="left"),
 "C_le_regard_d_Amina": dict(src="references/p1/SH26_fenetre_Amina_v001.png", crop=(150, 100, 2450, 1394), side="right", scrim=(0.72, 0.62),
     lines=[("LE CARNET", 240, 10), ("DE LA LIBERTÉ", 180, 8)], pos=(W-300, 190), align="right"),
}
if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, p in PROPS.items():
        png, jpg = OUT/f"{name}_3840x2160.png", OUT/f"{name}_YOUTUBE_1280x720.jpg"
        assert not png.exists() and not jpg.exists(), f"refus d'écraser {name}"
        im = grade(cover(R/p["src"], p["crop"])); im = scrim(im, p["side"], strength=p["scrim"][0], extent=p["scrim"][1], top=0.18)
        im, box = title(im, p["lines"], *p["pos"], align=p["align"])
        im.save(png, optimize=True); im.resize((1280, 720), Image.LANCZOS).save(jpg, quality=93, subsampling=0, optimize=True)
        print(name, "boîte du titre (3840×2160) :", box, "| JPEG", round(jpg.stat().st_size/1024), "Ko")
