#!/usr/bin/env python3
"""Miniature YouTube v3 minimaliste (1280x720) : Yassine et son grand-pere main dans la main + titre AR/FR. Refuse d'ecraser. Usage : build_miniature_v3.py OUT.jpg"""
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
src = Image.open(HERE / "MINIATURE_image_main_dans_la_main_v1.png").convert("RGB")
src = ImageEnhance.Contrast(src).enhance(1.08)
# fond : meme image agrandie, floue et assombrie ; image nette posee en bas, bords fondus
bg = src.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(22)); bg = ImageEnhance.Brightness(bg).enhance(0.45)
ih = 650; iw = int(src.width * ih / src.height)
fg = src.resize((iw, ih), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 70, 2))
import numpy as np
xs = np.minimum(np.arange(iw), np.arange(iw)[::-1]).astype(float)
side = np.clip(xs / 170, 0, 1) ** 1.4
top = np.clip(np.arange(ih) / 230, 0, 1) ** 1.5
mask = Image.fromarray((np.outer(top, side) * 255).astype("uint8"), "L")
canvas = bg.copy(); canvas.paste(fg, ((W - iw) // 2, H - ih), mask)
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
for y in range(H):
    a_top = max(0, 1 - y / 220) ** 1.3 * 150; a_bot = max(0, (y - 610) / 110) ** 1.3 * 190
    d.line((0, y, W, y), fill=(0, 0, 0, int(max(a_top, a_bot))))
im = Image.alpha_composite(canvas.convert("RGBA"), ov)
def text(img, s, f, y, fill, ar=False, stroke=0, spacing=0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(layer)
    if spacing and not ar:
        w = sum(dd.textlength(c, font=f) + spacing for c in s) - spacing; x = (W - w) / 2
        for c in s:
            dd.text((x, y), c, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255)); x += dd.textlength(c, font=f) + spacing
    else:
        kw = dict(direction="rtl", language="ar") if ar else {}
        w = dd.textlength(s, font=f, **kw); x = (W - w) / 2
        dd.text((x, y), s, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255), **kw)
    sh = layer.filter(ImageFilter.GaussianBlur(6)); sh = Image.eval(sh.split()[3], lambda v: int(v * 0.8))
    return Image.alpha_composite(Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), img, sh), layer)
im = text(im, "المسيرة الخضراء", ImageFont.truetype(AR, 66, layout_engine=ImageFont.Layout.RAQM), 26, GOLD, ar=True, stroke=1)
im = text(im, "LA MARCHE VERTE", ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", 34), 112, WHITE, stroke=1, spacing=17)
d2 = ImageDraw.Draw(im); lw = 130
d2.rectangle(((W - lw) / 2, 166, (W + lw) / 2, 167), fill=RED + (255,)); d2.rectangle(((W - lw) / 2, 171, (W + lw) / 2, 172), fill=GREEN + (255,))
im = text(im, "LE SECRET DE LA BOÎTE EN FER BLANC", ImageFont.truetype(FI, 28), 674, GOLD, stroke=1, spacing=4)
im.convert("RGB").save(out, "JPEG", quality=92, optimize=True)
print(out, out.stat().st_size)
