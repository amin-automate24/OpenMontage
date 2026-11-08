#!/usr/bin/env python3
"""Teaser TikTok 1080x1920 (video seule) a partir du master 1080p etalonne : fond flou + plan 16:9 centre + legendes AR/FR.
Usage : build_teaser.py OUT.mp4  (refuse d'ecraser). Source en lecture seule."""
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MASTER = ROOT / "13_FINAL_EXPORT" / "LE_SECRET_BOITE_FER_BLANC_FINAL_1080p.mp4"
GEN = ROOT / "12_EDITING" / "GENERIQUE_FIN" / "GEN_image_finale_v1.png"
W, H = 1080, 1920
GOLD, WHITE = (232, 190, 70), (252, 248, 238)
AR = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
SR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
X = 0.3  # fondu enchaine
# (debut dans le master en s, duree, [lignes de legende (texte, police, taille, couleur, arabe?)])
CLIPS = [
 (209.0, 3.6, [("6 novembre 1975", SR, 56, WHITE, False)], True),
 (141.0, 3.6, [("Un enfant.", SI, 58, WHITE, False), ("Une vieille boîte en fer blanc.", SI, 46, GOLD, False)], False),
 (155.0, 3.2, [("Un grain de sable…", SI, 58, WHITE, False)], False),
 (176.0, 3.2, [("…qui réveille la mémoire.", SI, 56, WHITE, False)], False),
 (196.0, 4.0, [("Le passé reprend vie.", SI, 58, WHITE, False)], False),
 (224.5, 3.6, [("Un peuple. Une marche.", SI, 58, WHITE, False)], False),
 (242.0, 3.2, [("Un drapeau dans le vent.", SI, 56, WHITE, False)], False),
 (341.0, 3.6, [("Un regard. Une transmission.", SI, 52, WHITE, False)], False),
 (421.8, 4.2, [("Ce que l’on transmet", SI, 56, WHITE, False), ("ne s’oublie jamais.", SI, 56, GOLD, False)], False),
]
END_DUR = 5.2
def font(p, s, ar=False):
    return ImageFont.truetype(p, s, layout_engine=ImageFont.Layout.RAQM) if ar else ImageFont.truetype(p, s)
def draw_c(d, s, f, y, fill, ar=False, spacing=0):
    if ar:
        w = d.textlength(s, font=f, direction="rtl", language="ar"); d.text(((W - w) / 2, y), s, font=f, fill=fill + (255,), direction="rtl", language="ar", stroke_width=2, stroke_fill=(0, 0, 0, 255)); return
    if spacing:
        w = sum(d.textlength(c, font=f) + spacing for c in s) - spacing; x = (W - w) / 2
        for c in s:
            d.text((x, y), c, font=f, fill=fill + (255,), stroke_width=2, stroke_fill=(0, 0, 0, 255)); x += d.textlength(c, font=f) + spacing
    else:
        w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill + (255,), stroke_width=2, stroke_fill=(0, 0, 0, 255))
def caption_png(path, lines, top_title=False):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if top_title:
        draw_c(d, "المسيرة الخضراء", font(AR, 96, True), 205, GOLD, ar=True)
        draw_c(d, "LA MARCHE VERTE", font(SR, 40), 330, WHITE, spacing=14)
    y = 1330
    for s, fp, sz, col, ar in lines:
        draw_c(d, s, font(fp, sz, ar), y, col, ar); y += sz + 22
    im.save(path)
def end_png(path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    draw_c(d, "المسيرة الخضراء", font(AR, 120, True), 205, GOLD, ar=True)
    draw_c(d, "LA MARCHE VERTE", font(SR, 54), 360, WHITE, spacing=16)
    draw_c(d, "Un court-métrage", font(SI, 44), 1300, WHITE)
    draw_c(d, "Ce soir à 19h · YouTube : Ziad Rai", font(SR, 46), 1380, GOLD)
    draw_c(d, "عاش المغرب", font(AR, 84, True), 1500, GOLD, ar=True)
    im.save(path)
def main(out):
    out = Path(out)
    if out.exists(): sys.exit(f"refus d'ecraser {out}")
    with tempfile.TemporaryDirectory() as td:
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        parts = []; starts = []; t = 0.0
        for i, (ss, dur, lines, title) in enumerate(CLIPS):
            cmd += ["-ss", f"{ss}", "-t", f"{dur + 0.1}", "-i", str(MASTER)]
            starts.append(t); t += dur - X
        n = len(CLIPS)
        cmd += ["-loop", "1", "-framerate", "24", "-t", f"{END_DUR + 0.1}", "-i", str(GEN)]
        for i, (ss, dur, lines, title) in enumerate(CLIPS):
            fgh = 608
            parts.append(f"[{i}:v]fps=24,split=2[s{i}a][s{i}b]")
            parts.append(f"[s{i}a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:6,eq=brightness=-0.22:saturation=1.1[b{i}]")
            parts.append(f"[s{i}b]scale={W}:{fgh}:flags=lanczos,format=yuv420p[f{i}]")
            parts.append(f"[b{i}][f{i}]overlay=0:({H}-{fgh})/2-160,trim=0:{dur + 0.1},setpts=PTS-STARTPTS[v{i}]")
        # carton final : image du generique avec lent zoom
        e = n
        parts.append(f"[{e}:v]split=2[ea][eb]")
        parts.append(f"[ea]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:6,eq=brightness=-0.3[eb0]")
        parts.append(f"[eb]scale={W}:608:flags=lanczos,format=yuv420p[ef]")
        parts.append(f"[eb0][ef]overlay=0:({H}-608)/2-160,fps=24,trim=0:{END_DUR + 0.1},setpts=PTS-STARTPTS[v{e}]")
        label, tot = "v0", CLIPS[0][1]
        for i in range(1, n + 1):
            d = CLIPS[i][1] if i < n else END_DUR
            parts.append(f"[{label}][v{i}]xfade=transition=fade:duration={X}:offset={tot - X:.3f}[x{i}]")
            label, tot = f"x{i}", tot + d - X
            starts.append(0) if i == n else None
        # legendes
        caps = []
        t = 0.0
        for i, (ss, dur, lines, title) in enumerate(CLIPS):
            p = Path(td) / f"c{i}.png"; caption_png(p, lines, top_title=title); caps.append((p, t + 0.35, t + dur - 0.1)); t += dur - X
        pe = Path(td) / "end.png"; end_png(pe); caps.append((pe, t + 0.4, t + END_DUR))
        base = label
        for k, (p, a, b) in enumerate(caps):
            cmd += ["-loop", "1", "-framerate", "24", "-t", f"{tot + 1}", "-i", str(p)]
            idx = n + 1 + k
            parts.append(f"[{idx}:v]format=rgba,fade=t=in:st={a:.2f}:d=0.45:alpha=1,fade=t=out:st={b - 0.45:.2f}:d=0.45:alpha=1[cap{k}]")
            parts.append(f"[{base}][cap{k}]overlay=0:0:format=auto[o{k}]"); base = f"o{k}"
        parts.append(f"[{base}]fade=t=in:st=0:d=0.4,fade=t=out:st={tot - 0.9:.2f}:d=0.9,format=yuv420p[vout]")
        cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-t", f"{tot:.3f}", "-r", "24",
                "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", str(out)]
        subprocess.run(cmd, check=True)
    print(out, round(tot, 2))
if __name__ == "__main__":
    main(sys.argv[1])
