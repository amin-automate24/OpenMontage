#!/usr/bin/env python3
"""LE DÉFI DE LA LIBERTÉ — quiz scolaire séparé (55 s, 1920×1080, 25 ips), NON FINAL.
Rendu 100 % local (Pillow + numpy + FFmpeg). Polices OFL : Cinzel (identité du générique du film) et Inter (lisibilité projecteur).
Aucune image externe, aucune voix, aucune musique ; carillon original synthétisé (3 révélations). Refuse d'écraser."""
import subprocess, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R = Path(__file__).resolve().parent.parent; O = R/"deliverables/QUIZ_SCOLAIRE_2026-11-20"
W, H, FPS, N = 1920, 1080, 25, 1375
CIN = str(R/"assets/fonts/ofl/cinzel-latin-700-normal.woff"); INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
def F(path, s): return ImageFont.truetype(path, s, layout_engine=ImageFont.Layout.RAQM)
def FI(w, s): return F(INTER.format(w), s)
IVORY, GOLD, DIM = (244, 236, 220), (214, 176, 98), (150, 132, 104)
GREEN, GREEN_B = (24, 112, 66), (120, 196, 140)
PANEL, PANEL_B = (58, 44, 33), (150, 118, 66)
NB = " "                                    # espace insécable avant ? ! :
SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 192, 1728, 108, 972      # zone titre 10 %
QUIZ = [
 dict(q=["Quel document les nationalistes marocains", f"ont-ils présenté le 11 janvier 1944{NB}?"],
      c=["Un traité commercial", "Le Manifeste de l’indépendance", "Une nouvelle Constitution"], ok=1,
      e=["Le Manifeste du 11 janvier 1944", "réclamait l’indépendance du Maroc."]),
 dict(q=[f"Que s’est-il passé le 20 août 1953{NB}?"],
      c=["Le retour du sultan au Maroc", "La reconnaissance de l’indépendance", "L’exil du sultan Mohammed Ben Youssef"], ok=2,
      e=["Le sultan Mohammed Ben Youssef a été déposé", "et contraint à l’exil avec sa famille."]),
 dict(q=["En quelle année la France a-t-elle reconnu", f"officiellement l’indépendance du Maroc{NB}?"],
      c=["1956", "1955", "1944"], ok=0,
      e=["La France a reconnu l’indépendance du Maroc", "le 2 mars 1956."])]
T_OPEN, T_Q, T_ANS, T_CLOSE = 100, 375, 275, 150   # images : 4 s, 15 s (11 + 4), 6 s
BOXES = []                                        # (nom, bbox) pour le QC des marges et chevauchements
def ease(x): x = min(1.0, max(0.0, x)); return x*x*(3-2*x)
# ---------- fond et décor (étoile à huit branches, frises discrètes) ----------
def star(d, cx, cy, r, col, w=2):
    for rot in (0, 45):
        pts = [(cx+r*math.cos(math.radians(rot+45+90*k)), cy+r*math.sin(math.radians(rot+45+90*k))) for k in range(4)]
        d.polygon(pts, outline=col, width=w)
def background():
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx-W/2)/(W*0.62))**2+((yy-H/2)/(H*0.62))**2)
    base = np.array([34, 26, 20], np.float32); img = base*np.clip(1.18-0.55*r, 0.55, 1.18)[..., None]
    img += np.random.default_rng(20).normal(0, 1.1, (H, W, 1))
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay); col = GOLD+(70,)
    for y in (58, 1022):                                  # frises haut/bas (zone d'action, hors texte)
        d.line([(150, y), (W-150, y)], fill=col, width=1)
        for x in range(190, W-150, 120): star(d, x, y, 9, col, 1)
    for (x, y) in ((96, 96), (W-96, 96), (96, H-96), (W-96, H-96)): star(d, x, y, 22, GOLD+(90,), 2); star(d, x, y, 10, GOLD+(60,), 1)
    return Image.alpha_composite(im, lay)
BG = np.asarray(background().convert("RGB"), np.float32)
# ---------- calques (RGBA recadrés sur leur boîte) ----------
class Layer:
    def __init__(self, name, im):
        bb = im.getbbox(); self.x0, self.y0 = bb[0], bb[1]; c = np.asarray(im.crop(bb), np.float32)/255
        self.rgb, self.a = c[..., :3]*255, c[..., 3:4]; BOXES.append((name, bb))
    def comp(self, out, k, dy=0):
        if k <= 0: return
        y0 = self.y0+dy; h, w = self.a.shape[:2]; a = self.a*k
        out[y0:y0+h, self.x0:self.x0+w] = out[y0:y0+h, self.x0:self.x0+w]*(1-a)+self.rgb*a
def text_im(lines, font, col, y0, lh, x=None, anchor="ma", spacing=0, align_left=False):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    for i, t in enumerate(lines):
        y = y0+i*lh
        if spacing:
            ws = [d.textlength(ch, font=font) for ch in t]; tw = sum(ws)+spacing*(len(t)-1); xx = W/2-tw/2
            for ch, w_ in zip(t, ws): d.text((xx, y), ch, font=font, fill=col, anchor="la"); xx += w_+spacing
        else: d.text((W/2 if x is None else x, y), t, font=font, fill=col, anchor="la" if align_left else anchor)
    return im
def width(t, font): return ImageDraw.Draw(Image.new("L", (1, 1))).textlength(t, font=font)
def divider(y, wdt=260):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    d.line([(W/2-wdt, y), (W/2-30, y)], fill=GOLD+(200,), width=2); d.line([(W/2+30, y), (W/2+wdt, y)], fill=GOLD+(200,), width=2)
    star(d, W/2, y, 14, GOLD+(230,), 2); return im
# ---------- écran d'ouverture et de clôture ----------
OPEN = [Layer("titre", text_im(["LE DÉFI DE LA LIBERTÉ"], F(CIN, 104), GOLD, 395, 0, spacing=4)),
        Layer("filet_titre", divider(550)),
        Layer("sous-titre", text_im(["3 QUESTIONS POUR TESTER TES CONNAISSANCES"], FI("SemiBold", 48), IVORY, 615, 0, spacing=3))]
CLOSE = [Layer("bravo", text_im([f"BRAVO{NB}!"], F(CIN, 132), GOLD, 300, 0, spacing=6)),
         Layer("filet_bravo", divider(490)),
         Layer("message", text_im(["CONNAÎTRE NOTRE HISTOIRE,", "C’EST AUSSI PRÉPARER NOTRE AVENIR."], FI("Bold", 60), IVORY, 560, 90, spacing=2))]
# ---------- écrans de question ----------
CH_Y, CH_H, CH_GAP, CH_X0, CH_X1 = 404, 104, 20, 270, 1650
def panel(i, txt, state):              # state : normal | correct
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im); y = CH_Y+i*(CH_H+CH_GAP)
    fill, border = (GREEN+(255,), GREEN_B+(255,)) if state == "correct" else (PANEL+(235,), PANEL_B+(255,))
    d.rounded_rectangle([CH_X0, y, CH_X1, y+CH_H], radius=22, fill=fill, outline=border, width=4 if state == "correct" else 2)
    cx, cy = CH_X0+70, y+CH_H/2
    d.ellipse([cx-40, cy-40, cx+40, cy+40], fill=(GOLD if state != "correct" else IVORY)+(255,))
    d.text((cx, cy+2), "ABC"[i], font=F(CIN, 50), fill=(40, 30, 22, 255), anchor="mm")
    f = FI("SemiBold", 54); assert width(txt, f) < CH_X1-CH_X0-260, txt
    d.text((CH_X0+140, cy), txt, font=f, fill=IVORY+(255,), anchor="lm")
    if state == "correct":                                   # coche dessinée (indépendante des glyphes)
        x, yy = CH_X1-80, cy; d.line([(x-26, yy+2), (x-8, yy+22), (x+28, yy-22)], fill=IVORY+(255,), width=10, joint="curve")
    return Layer(f"choix_{'ABC'[i]}_{state}", im)
QL = []
for n, q in enumerate(QUIZ):
    fq = FI("Bold", 60); assert all(width(t, fq) <= SAFE_X1-SAFE_X0 for t in q["q"]), q["q"]
    qy = 205 if len(q["q"]) == 2 else 248
    fe = FI("Medium", 46); assert all(width(t, fe) <= SAFE_X1-SAFE_X0 for t in q["e"]), q["e"]
    QL.append(dict(
        head=Layer(f"q{n+1}_entete", text_im([f"QUESTION {n+1} / 3"], FI("SemiBold", 40), GOLD, 122, 0, spacing=6)),
        q=Layer(f"q{n+1}_question", text_im(q["q"], fq, IVORY, qy, 76)),
        ch=[panel(i, t, "normal") for i, t in enumerate(q["c"])], okp=panel(q["ok"], q["c"][q["ok"]], "correct"),
        lab=Layer(f"q{n+1}_bonne_reponse", text_im([f"BONNE RÉPONSE{NB}: {'ABC'[q['ok']]}"], F(CIN, 38), GREEN_B, 790, 0, spacing=4)),
        exp=Layer(f"q{n+1}_explication", text_im(q["e"], fe, IVORY, 846, 58)), ok=q["ok"]))
BAR_Y, BAR_X0, BAR_X1 = 812, CH_X0, CH_X1
FNUM = FI("SemiBold", 40)
# ---------- composition image par image ----------
def frame(f):
    out = BG.copy()
    if f < T_OPEN:
        k = ease(f/15)*ease((T_OPEN-1-f)/10)
        for i, L in enumerate(OPEN): L.comp(out, ease((f-4*i)/15)*ease((T_OPEN-1-f)/10), dy=int(round(10*(1-ease((f-4*i)/15)))))
        return out
    if f >= T_OPEN+3*T_Q:
        j = f-(T_OPEN+3*T_Q); fin = ease((T_CLOSE-1-j)/18)
        for i, L in enumerate(CLOSE): L.comp(out, ease((j-6*i)/15)*fin, dy=int(round(10*(1-ease((j-6*i)/15)))))
        return out
    n, j = divmod(f-T_OPEN, T_Q); q = QL[n]; fo = ease((T_Q-1-j)/8)          # fondu de sortie sur 8 images
    q["head"].comp(out, ease(j/10)*fo); q["q"].comp(out, ease((j-2)/12)*fo, dy=int(round(8*(1-ease((j-2)/12)))))
    rv = ease((j-T_ANS)/8)                                                    # révélation à 11,00 s (8 images)
    for i, L in enumerate(q["ch"]):
        a = ease((j-8-4*i)/10)*fo
        if i == q["ok"]: L.comp(out, a*(1-rv)); q["okp"].comp(out, a*rv)
        else: L.comp(out, a*(1-0.62*rv))
    if j < T_ANS:                                                             # compte à rebours discret (barre + secondes)
        a = ease((j-14)/10)
        if a > 0:
            frac = 1-j/T_ANS; x1 = BAR_X0+(BAR_X1-120-BAR_X0)*frac
            out[BAR_Y-3:BAR_Y+3, BAR_X0:BAR_X1-120] = out[BAR_Y-3:BAR_Y+3, BAR_X0:BAR_X1-120]*(1-0.35*a)+np.array(DIM, np.float32)*0.35*a
            xi = int(x1)
            if xi > BAR_X0: out[BAR_Y-3:BAR_Y+3, BAR_X0:xi] = out[BAR_Y-3:BAR_Y+3, BAR_X0:xi]*(1-a)+np.array(GOLD, np.float32)*a
            NUMS[math.ceil((T_ANS-j)/FPS)].comp(out, a)
    else:
        q["lab"].comp(out, rv*fo); q["exp"].comp(out, ease((j-T_ANS-4)/10)*fo)
    return out
NUMS = {s: Layer(f"compte_{s}", text_im([str(s)], FNUM, GOLD, BAR_Y-24, 0, x=BAR_X1-50, anchor="ma")) for s in range(1, 12)}
def chime(dur):
    sr = 48000; a = np.zeros(int(dur*sr), np.float32)
    def note(t0, f0, amp):
        t = np.arange(int(1.4*sr))/sr; env = (1-np.exp(-t/0.012))*np.exp(-t/0.42)
        s = amp*env*(np.sin(2*np.pi*f0*t)+0.18*np.sin(2*np.pi*2*f0*t)+0.05*np.sin(2*np.pi*3*f0*t))
        i0 = int(t0*sr); a[i0:i0+len(s)] += s[:len(a)-i0]
    for n in range(3):
        t = (T_OPEN+n*T_Q+T_ANS)/FPS; note(t, 1046.5, 0.07); note(t+0.13, 1318.5, 0.06)   # do6 puis mi6, carillon doux
    return np.repeat(a[:, None], 2, axis=1)
if __name__ == "__main__":
    O.mkdir(parents=True, exist_ok=True); out = O/"LE_DEFI_DE_LA_LIBERTE_QUIZ_NON_FINAL_1080p.mp4"; assert not out.exists(), "refus d'écraser"
    for name, (x0, y0, x1, y1) in BOXES:
        if not name.startswith(("compte",)): assert x0 >= SAFE_X0-60 and x1 <= SAFE_X1+60 and y0 >= SAFE_Y0 and y1 <= SAFE_Y1, (name, x0, y0, x1, y1)
    wav = O/"_quiz_audio_tmp.wav"; aud = chime(N/FPS)
    import wave
    with wave.open(str(wav), "wb") as w_: w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(48000); w_.writeframes((np.clip(aud, -1, 1)*32767).astype("<i2").tobytes())
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav),
        "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
        "-profile:v", "high", "-level", "4.0", "-g", "50", "-r", str(FPS), "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{N/FPS}", "-movflags", "+faststart",
        "-metadata", "title=LE DÉFI DE LA LIBERTÉ — quiz scolaire NON FINAL", "-metadata", "comment=NON FINAL — à valider avant projection", str(out)], stdin=subprocess.PIPE)
    for f in range(N): p.stdin.write(np.clip(frame(f)+0.5, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close(); assert p.wait() == 0; wav.unlink(); print("écrit", out)
