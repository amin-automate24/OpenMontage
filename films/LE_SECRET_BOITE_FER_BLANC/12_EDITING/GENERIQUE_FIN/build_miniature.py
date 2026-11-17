#!/usr/bin/env python3
"""Miniature YouTube 1280x720 : image du generique + titre arabe/francais. Refuse d'ecraser. Usage : build_miniature.py OUT.jpg"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
HERE = Path(__file__).resolve().parent
W, H = 1280, 720
GOLD, WHITE, RED, GREEN = (232, 190, 70), (252, 248, 238), (193, 39, 45), (0, 110, 58)
AR = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
out = Path(sys.argv[1])
if out.exists(): sys.exit(f"refus d'ecraser {out}")
im = Image.open(HERE / "GEN_image_finale_v1.png").convert("RGB").resize((W, H), Image.LANCZOS)
im = ImageEnhance.Contrast(im).enhance(1.12); im = ImageEnhance.Color(im).enhance(1.1)
im = im.filter(ImageFilter.UnsharpMask(2, 80, 2))
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
for y in range(H):  # degrade sombre haut et bas pour la lisibilite
    a_top = max(0, 1 - y / 330) ** 1.3 * 215; a_bot = max(0, (y - 520) / 200) ** 1.4 * 200
    d.line((0, y, W, y), fill=(0, 0, 0, int(max(a_top, a_bot))))
im = Image.alpha_composite(im.convert("RGBA"), ov)
def text(img, s, f, y, fill, ar=False, stroke=0, spacing=0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(layer)
    kw = dict(direction="rtl", language="ar") if ar else {}
    if spacing and not ar:
        w = sum(dd.textlength(c, font=f) + spacing for c in s) - spacing; x = (W - w) / 2
        for c in s:
            dd.text((x, y), c, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255)); x += dd.textlength(c, font=f) + spacing
    else:
        w = dd.textlength(s, font=f, **kw); x = (W - w) / 2
        dd.text((x, y), s, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255), **kw)
    sh = layer.filter(ImageFilter.GaussianBlur(6)); sh = Image.eval(sh.split()[3], lambda v: int(v * 0.8))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 255)); img = Image.composite(black, img, sh)
    return Image.alpha_composite(img, layer)
im = text(im, "المسيرة الخضراء", ImageFont.truetype(AR, 190, layout_engine=ImageFont.Layout.RAQM), 18, GOLD, ar=True, stroke=3)
im = text(im, "LA MARCHE VERTE", ImageFont.truetype(FB, 100), 232, WHITE, stroke=3, spacing=8)
d2 = ImageDraw.Draw(im); lw = 520
d2.rectangle(((W - lw) / 2, 362, (W + lw) / 2, 368), fill=RED + (255,)); d2.rectangle(((W - lw) / 2, 372, (W + lw) / 2, 378), fill=GREEN + (255,))
im = text(im, "LE SECRET DE LA BOÎTE EN FER BLANC", ImageFont.truetype(FB, 46), 624, GOLD, stroke=2, spacing=3)
im = text(im, "Court-métrage · 6 novembre 1975", ImageFont.truetype(FI, 36), 678, WHITE, stroke=2)
im.convert("RGB").save(out, "JPEG", quality=92, optimize=True)
print(out, out.stat().st_size)
