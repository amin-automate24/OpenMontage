#!/usr/bin/env python3
"""Generique de fin 'La Marche Verte' (video seule 1920x1080 24 i/s, 58,3 s) : image + calques texte (Pillow/raqm) animes par FFmpeg.
Usage : build_generique_fin.py OUT.mp4   (refuse d'ecraser). Sources en lecture seule."""
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).resolve().parent
IMG = HERE / "GEN_image_finale_v1.png"
DUR = 58.3
GOLD, WHITE, RED, GREEN = (212, 175, 55), (245, 240, 228), (193, 39, 45), (0, 98, 51)
AR = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
FRB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FRR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FRI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
W, H = 1920, 1080
ROLES = [  # (groupe, debut, fin, [(role, nom provisoire)])
    (1, 24.0, 29.6, [("RÉALISATION", "[Nom]"), ("SCÉNARIO", "[Nom]"), ("DIRECTION ARTISTIQUE", "[Nom]")]),
    (2, 30.0, 35.6, [("CRÉATION DES PERSONNAGES", "[Nom]"), ("CRÉATION DES DÉCORS", "[Nom]"), ("ANIMATION", "[Nom]")]),
    (3, 36.0, 41.8, [("MONTAGE", "[Nom]"), ("MUSIQUE ET CONCEPTION SONORE", "[Nom]"), ("PRODUCTION", "[Nom / Société]")]),
]
def font(p, s, ar=False):
    return ImageFont.truetype(p, s, layout_engine=ImageFont.Layout.RAQM) if ar else ImageFont.truetype(p, s)
def centered(d, text, f, y, fill, spacing=0, ar=False):
    if ar:
        w = d.textlength(text, font=f, direction="rtl", language="ar")
        d.text(((W - w) / 2, y), text, font=f, fill=fill + (255,), direction="rtl", language="ar")
        return
    if spacing:
        w = sum(d.textlength(c, font=f) + spacing for c in text) - spacing
        x = (W - w) / 2
        for c in text:
            d.text((x, y), c, font=f, fill=fill + (255,)); x += d.textlength(c, font=f) + spacing
    else:
        w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill + (255,))
def flagline(d, y, w=420):
    d.rectangle(((W - w) / 2, y, (W + w) / 2 - 1, y + 4), fill=RED + (255,))
    d.rectangle(((W - w) / 2, y + 8, (W + w) / 2 - 1, y + 12), fill=GREEN + (255,))
def layer(draw_fn):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(im)); return im
def build_layers(td):
    L = []  # (png, t_in, d_in, t_out, d_out)
    def add(name, fn, a, b, di=1.2, do=1.2):
        p = Path(td) / f"{name}.png"; layer(fn).save(p); L.append((p, a, di, b, do))
    # voile sombre pour la lisibilite
    def dim(alpha):
        def f(d): d.rectangle((0, 0, W, H), fill=(0, 0, 0, alpha))
        return f
    add("dim_credits", dim(150), 22.5, 43.8, 1.5, 1.5)
    add("dim_final", dim(130), 44.8, 55.0, 1.5, 1.5)
    # degrade haut pour le titre
    def top(d):
        for y in range(0, 620):
            d.line((0, y, W, y), fill=(0, 0, 0, int(170 * (1 - y / 620))))
    add("top", top, 5.0, 23.0, 2.0, 1.5)
    # bande sombre douce derriere titre francais et mention (lisibilite sur la foule)
    def band(d):
        for y in range(360, 760):
            k = 1 - abs(y - 560) / 200
            d.line((0, y, W, y), fill=(0, 0, 0, int(200 * max(k, 0) ** 0.8)))
    add("band", band, 6.5, 22.8, 2.0, 1.5)
    add("titre_ar", lambda d: centered(d, "المسيرة الخضراء", font(AR, 170, True), 150, GOLD, ar=True), 6.0, 22.5, 2.2, 1.5)
    add("titre_fr", lambda d: centered(d, "LA MARCHE VERTE", font(FRB, 84), 400, WHITE, spacing=16), 7.4, 22.5, 2.0, 1.5)
    add("titre_flag", lambda d: flagline(d, 520), 8.6, 22.5, 1.6, 1.5)
    add("mention", lambda d: centered(d, "Un court-métrage inspiré d’un moment historique du Maroc", font(FRI, 44), 585, WHITE), 12.5, 22.5, 1.8, 1.5)
    for g, a, b, items in ROLES:
        def f(d, items=items, g=g):
            y0 = 330
            for i, (role, nom) in enumerate(items):
                y = y0 + i * 170
                centered(d, role, font(FRB, 32), y, GOLD, spacing=6)
                centered(d, nom, font(FRR, 58), y + 50, WHITE)
            if g == 3:
                centered(d, "Réalisé avec l’aide de l’intelligence artificielle", font(FRI, 28), 900, (200, 195, 185))
        add(f"credits_{g}", f, a, b, 1.0, 1.0)
    add("final_ar", lambda d: centered(d, "عاش المغرب", font(AR, 150, True), 330, GOLD, ar=True), 45.8, 53.8, 2.2, 2.2)
    add("final_fr", lambda d: centered(d, "VIVE LE MAROC", font(FRB, 82), 570, WHITE, spacing=14), 47.0, 53.8, 2.0, 2.2)
    add("final_flag", lambda d: flagline(d, 700, 480), 48.2, 53.8, 1.6, 2.2)
    return L
def main(out):
    out = Path(out)
    if out.exists(): sys.exit(f"refus d'ecraser {out}")
    with tempfile.TemporaryDirectory() as td:
        L = build_layers(td)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "24", "-t", f"{DUR}", "-i", str(IMG)]
        for p, *_ in L: cmd += ["-loop", "1", "-framerate", "24", "-t", f"{DUR}", "-i", str(p)]
        n = int(DUR * 24)
        parts = [f"[0:v]scale=3840:2160:flags=lanczos,zoompan=z='1+0.085*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=24,"
                 f"unsharp=5:5:0.5,vignette=PI/6,fade=t=in:st=0:d=2.5,fade=t=out:st={DUR-4.0}:d=4.0,format=yuv420p[base0]"]
        last = "base0"
        for i, (p, a, di, b, do) in enumerate(L, start=1):
            parts.append(f"[{i}:v]format=rgba,fade=t=in:st={a}:d={di}:alpha=1,fade=t=out:st={b}:d={do}:alpha=1[l{i}]")
            parts.append(f"[{last}][l{i}]overlay=0:0:format=auto:shortest=0[o{i}]"); last = f"o{i}"
        parts.append(f"[{last}]fade=t=out:st={DUR-4.0}:d=4.0,format=yuv420p[v]")
        cmd += ["-filter_complex", ";".join(parts), "-map", "[v]", "-t", f"{DUR}", "-r", "24",
                "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", str(out)]
        subprocess.run(cmd, check=True)
    print(out)
if __name__ == "__main__":
    main(sys.argv[1])
