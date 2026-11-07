#!/usr/bin/env python3
"""Cartons d'introduction et de generique (video seule, fond noir) : build_cards.py (refuse d'ecraser)."""
import subprocess, sys, tempfile
from pathlib import Path
R = Path(__file__).resolve().parent; OUT = R / "CARDS"
FR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
INTRO_DUR = 8.5
CREDITS = [  # (texte, police, taille, espace apres)
 ("LE SECRET DE LA BOÎTE", FB, 64, 6), ("EN FER BLANC", FB, 64, 70),
 ("Un film de fiction inspiré de la Marche Verte", FI, 38, 6), ("6 novembre 1975", FI, 38, 90),
 ("En hommage aux participants de la Marche Verte", FI, 34, 110),
 ("PERSONNAGES", FB, 30, 18), ("Yassine, huit ans", FR, 36, 6), ("Le grand-père, jeune puis âgé", FR, 36, 6),
 ("Les personnages sont fictifs", FI, 30, 100),
 ("IMAGES ET ANIMATION", FB, 30, 18), ("Midjourney", FR, 36, 6), ("Magnific · Nano Banana 2", FR, 36, 6),
 ("Kling 2.6 · Kling 3.0 · Kling Omni", FR, 36, 100),
 ("MUSIQUE ET SONS", FB, 30, 18), ("Musique originale générée · Google Lyria 3 Pro", FR, 36, 6),
 ("Effets sonores et ambiances · Magnific", FR, 36, 100),
 ("MONTAGE, ÉTALONNAGE ET MIXAGE", FB, 30, 18), ("FFmpeg · OpenMontage", FR, 36, 100),
 ("ARCHIVES", FB, 30, 18), ("Un insert : photographie d'archive, 1975", FR, 36, 100),
 ("Les images et les sons de ce film sont générés par intelligence artificielle.", FI, 30, 6),
 ("Ils ne constituent pas des archives, à l'exception de l'insert signalé.", FI, 30, 100),
 ("Le Coran et le drapeau sont traités avec respect.", FI, 30, 140),
 ("Merci", FB, 50, 0),
]
CRED_DUR = 50.0
def run(cmd): subprocess.run(cmd, check=True)
def txt(td, i, s):
    p = Path(td) / f"l{i}.txt"; p.write_text(s, encoding="utf-8"); return p
def intro(out):
    with tempfile.TemporaryDirectory() as td:
        a = "if(lt(t,1.5),0,if(lt(t,3),(t-1.5)/1.5,if(lt(t,6.2),1,if(lt(t,7.8),(7.8-t)/1.6,0))))"
        lines = [("LE SECRET DE LA BOÎTE", FB, 78, -80), ("EN FER BLANC", FB, 78, 20), ("6 novembre 1975", FI, 38, 140)]
        vf = ",".join(
            f"drawtext=fontfile={f}:textfile={txt(td, i, s)}:fontsize={sz}:fontcolor=0xE8DCC0:x=(w-text_w)/2:y=(h-text_h)/2+({dy}):alpha='{a}'"
            for i, (s, f, sz, dy) in enumerate(lines))
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:r=24:d={INTRO_DUR}",
             "-vf", vf + ",format=yuv420p", "-c:v", "libx264", "-crf", "14", str(out)])
def credits(out):
    with tempfile.TemporaryDirectory() as td:
        y, parts, speed = 0, [], 62
        for i, (s, f, sz, gap) in enumerate(CREDITS):
            parts.append(f"drawtext=fontfile={f}:textfile={txt(td, i, s)}:fontsize={sz}:fontcolor=0xE8DCC0:"
                         f"x=(w-text_w)/2:y=h+{y}-t*{speed}")
            y += sz + gap + 10
        fade = f"fade=t=in:st=0:d=1.2,fade=t=out:st={CRED_DUR - 2.5}:d=2.5"
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:r=24:d={CRED_DUR}",
             "-vf", ",".join(parts) + f",{fade},format=yuv420p", "-c:v", "libx264", "-crf", "14", str(out)])
if __name__ == "__main__":
    for name, fn in (("INTRO_v1.mp4", intro), ("CREDITS_v1.mp4", credits)):
        p = OUT / name
        if p.exists(): sys.exit(f"refus d'ecraser {p}")
        fn(p); print(p)
