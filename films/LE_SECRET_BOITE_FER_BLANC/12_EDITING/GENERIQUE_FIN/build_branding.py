#!/usr/bin/env python3
"""Logo (titre) + banniere YouTube + avatar du film. Refuse d'ecraser. Usage : build_branding.py DOSSIER_SORTIE"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
GOLD, WHITE, RED, GREEN = (232, 190, 70), (252, 248, 238), (193, 39, 45), (0, 110, 58)
AR = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
SR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
def f(p, s, ar=False): return ImageFont.truetype(p, s, layout_engine=ImageFont.Layout.RAQM) if ar else ImageFont.truetype(p, s)
def centered(d, W, text, font, y, fill, ar=False, spacing=0, stroke=0):
    if ar:
        w = d.textlength(text, font=font, direction="rtl", language="ar"); d.text(((W - w) / 2, y), text, font=font, fill=fill + (255,), direction="rtl", language="ar", stroke_width=stroke, stroke_fill=(0, 0, 0, 255)); return
    w = sum(d.textlength(c, font=font) + spacing for c in text) - spacing; x = (W - w) / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255)); x += d.textlength(c, font=font) + spacing
def flag(d, W, y, w, t):
    d.rectangle(((W - w) / 2, y, (W + w) / 2, y + t), fill=RED + (255,)); d.rectangle(((W - w) / 2, y + t * 2, (W + w) / 2, y + t * 3), fill=GREEN + (255,))
def save(im, name, **kw):
    p = OUT / name
    if p.exists(): sys.exit(f"refus d'ecraser {p}")
    im.save(p, **kw); print(p, p.stat().st_size)
# 1) logo titre (fond transparent) + variante fond noir
W, H = 2000, 800
lg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lg)
centered(d, W, "المسيرة الخضراء", f(AR, 300, True), 60, GOLD, ar=True)
centered(d, W, "LA MARCHE VERTE", f(SR, 130), 450, WHITE, spacing=26)
flag(d, W, 680, 560, 7)
save(lg, "LOGO_LA_MARCHE_VERTE_transparent.png")
blk = Image.new("RGBA", (W, H), (8, 6, 4, 255)); blk.alpha_composite(lg); save(blk.convert("RGB"), "LOGO_LA_MARCHE_VERTE_fond_noir.png")
# 2) banniere YouTube 2560x1440 (zone sure 1546x423 au centre)
src = Image.open(HERE / "GEN_image_finale_v1.png").convert("RGB")
BW, BH = 2560, 1440
bg = src.resize((BW, int(src.height * BW / src.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(3, 60, 2))
bg = bg.crop((0, 0, BW, BH)) if bg.height >= BH else bg.resize((BW, BH))
bg = ImageEnhance.Brightness(bg).enhance(0.62)
ov = Image.new("RGBA", (BW, BH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
for y in range(BH): od.line((0, y, BW, y), fill=(0, 0, 0, int(120 * abs(y - BH / 2) / (BH / 2))))
for x in range(BW): od.line((x, 0, x, BH), fill=(0, 0, 0, int(150 * (abs(x - BW / 2) / (BW / 2)) ** 2)))
bn = Image.alpha_composite(bg.convert("RGBA"), ov); bd = ImageDraw.Draw(bn)
centered(bd, BW, "المسيرة الخضراء", f(AR, 150, True), 520, GOLD, ar=True, stroke=3)
centered(bd, BW, "LA MARCHE VERTE", f(SR, 64), 706, WHITE, spacing=20, stroke=2)
flag(bd, BW, 790, 260, 4)
centered(bd, BW, "COURT-MÉTRAGE · 6 NOVEMBRE 1975", f(SI, 34), 836, GOLD, spacing=6, stroke=1)
save(bn.convert("RGB"), "BANNIERE_YOUTUBE_2560x1440.jpg", quality=92, optimize=True)
# 3) avatar carre 800x800 (titre arabe sur la foule)
S = 800
sq = src.crop((int(src.width * 0.18), 0, int(src.width * 0.18) + src.height, src.height)).resize((S, S), Image.LANCZOS)
sq = ImageEnhance.Brightness(sq).enhance(0.55); av = sq.convert("RGBA"); ad = ImageDraw.Draw(av)
centered(ad, S, "المسيرة", f(AR, 150, True), 250, GOLD, ar=True, stroke=3)
centered(ad, S, "الخضراء", f(AR, 150, True), 410, GOLD, ar=True, stroke=3)
flag(ad, S, 610, 200, 4)
save(av.convert("RGB"), "AVATAR_LA_MARCHE_VERTE_800x800.jpg", quality=93)
