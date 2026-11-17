#!/usr/bin/env python3
"""Animatic 2.0 (276 s): real validated images + local compositions + temporary voices. Local only, no network, no credits.
Usage: python3 build_animatic_v2.py [--frames N]  (N = render only first N seconds for a quick test)
Output: animatic/ANIMATIC_2.0_276s.mp4, animatic/animatic_2.0_report.json
--clean : rendu propre (aucun bandeau technique, aucun sous-titre incrusté, vidéo seule, 1080p) -> animatic/MASTER_CLEAN_1080p_video_prep.mp4 + master_clean_report.json (n'écrase rien)"""
import sys, json, subprocess, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, str(Path(__file__).parent))
from shots_data import SHOTS, FPS, TOTAL
import carnet_animatic as CA            # reuse timeline renderer + dialogue timing
R = Path(__file__).resolve().parent.parent; OUT = R/"animatic"
W0, H0 = 2752, 1536; FW, FH = 1920, 1080
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; DS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
import font_amatic_sc; AM = str(Path(font_amatic_sc.__file__).parent/"files/AmaticSC-Bold.ttf")
fnt = lambda p, s: ImageFont.truetype(p, s)

P = lambda *a: R.joinpath(*a)
IMG = {  # shot -> source image / clip  (SH03 = v006 LOCKED 17/11, v005 conservée)
 1: P("references/p1/SH01_classe_v001.png"), 2: P("references/p4/post/SH02_composite_final.png"),
 3: P("references/p4/post/SH03_gaze_head_v006.png"), 7: P("references/p4/SH07_younes_boite_v001.png"),
 8: P("references/p4/post/SH08_composite_final.png"), 9: P("references/p4/SH09_younes_mere_v001.png"),
 13: P("references/p2/SH13_rue1944_v001.png"), 14: P("references/p2/SH14_amina_pere_marche_v001.png"),
 15: P("references/p2/SH15_pere_explique_v001.png"), 16: P("references/p2/SH16_table_feuille_v001.png"),
 21: P("references/p2/SH21_maison1953_soir_v001.png"), 22: P("references/p2/SH22_radio_v001.png"),
 25: P("references/p2/SH25_fenetre_v001.png"), 26: P("references/p1/SH26_fenetre_Amina_v001.png"),
 27: P("references/p3/SH27_foule_rabat1955_v001.png"), 28: P("references/p3/SH28_amina_pere_foule_v001.png"),
 29: P("references/p3/post/SH29_composite_final.png"), 31: P("references/p3/post/SH31_composite_final_v002_clean.png"),  # v002: 2 taches retouchées localement (original conservé)
 32: P("references/p3/SH32_pere_amina_nouvelle_v001.png"), 34: P("references/p3/SH34_amina_ferme_carnet_v001.png"),
 35: P("references/p4/SH35_classe_presentation_v001.png"), 37: P("references/p4/post/SH37_composite_final.png"),
 38: P("references/p1/SH38_cahier_final_v001.png"), 17: P("references/p3/post/SH17_composite_final.png"),
 10: P("references/p1/post/SH10_composite_final.png"),
}
CLIP = {10: P("references/p1/post/SH10_master_1080p_v001.mp4"), 16: P("references/p2/post/SH16_composite_v001.mp4"),
        19: P("references/p2/post/SH19_edit_6.50s.mp4"), 24: P("references/p2/post/SH24_composite_v001.mp4"),
        30: P("references/p3/post/SH30_composite_v001.mp4")}
# crops of existing images (re-use): shot -> (source image, zoom0, zoom1, centre0, centre1)
CROP = {4: (IMG[2], 2.0, 2.0, (1000, 760), (1000, 760)), 5: (IMG[3], 2.3, 2.7, (1850, 640), (1850, 640)),
        11: (IMG[10], 1.0, 1.25, (1376, 768), (1376, 768)), 18: (IMG[16], 1.5, 1.7, (1500, 960), (1500, 960)),
        23: (IMG[21], 1.8, 2.0, (1500, 900), (1500, 900)), 36: (IMG[35], 2.6, 3.0, (1040, 560), (1040, 560))}
CAMZ = {"static": (1.0, 1.0), "push_in": (1.0, 1.08), "push_in_slow": (1.0, 1.04), "push_in_strong": (1.0, 1.2),
        "pull_out": (1.08, 1.0), "pan_right": (1.08, 1.08), "pan_left": (1.08, 1.08)}
_cache = {}
def load(p):
    if p not in _cache: _cache[p] = Image.open(p).convert("RGB")
    return _cache[p]
ease = lambda x: x*x*(3-2*x)

def cam_frame(img, z0, z1, c0, c1, u):
    u = ease(u); z = z0+(z1-z0)*u; cx = c0[0]+(c1[0]-c0[0])*u; cy = c0[1]+(c1[1]-c0[1])*u
    W, H = img.size; cw, ch = W/z, H/z
    ox = min(max(cx-cw/2, 0), W-cw); oy = min(max(cy-ch/2, 0), H-ch)
    return img.resize((FW, FH), Image.LANCZOS, box=(ox, oy, ox+cw, oy+ch))

def paper(color=(238, 224, 184)):
    im = Image.new("RGB", (FW, FH), color); a = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:FH, 0:FW]; v = 1-0.18*(((xx-FW/2)/(FW/2))**2+((yy-FH/2)/(FH/2))**2)
    return Image.fromarray(np.clip(a*v[..., None], 0, 255).astype(np.uint8))

def tint(img, kind):
    a = np.asarray(img).astype(np.float32)
    if kind == "autumn": a = a*np.array([1.10, 0.95, 0.78])
    if kind == "winter": g = a.mean(axis=2, keepdims=True); a = (a*0.45+g*0.55)*np.array([0.85, 0.95, 1.15])
    if kind == "spring": a = a*np.array([0.95, 1.08, 0.92])
    if kind == "dusk": a = a*np.array([0.82, 0.92, 1.12])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def card(draw, box, text, font, fill=(20, 28, 38, 215), ink=(240, 240, 235)):
    x0, y0, x1, y1 = box; draw.rounded_rectangle(box, 26, fill=fill)
    draw.text(((x0+x1)//2, (y0+y1)//2), text, font=font, fill=ink, anchor="mm")

def flag(img, box):
    """Vector Moroccan flag (red field, green interlaced pentagram), drawn locally - never generated."""
    x0, y0, x1, y1 = box; d = ImageDraw.Draw(img, "RGBA"); d.rectangle(box, fill=(193, 39, 45))
    cx, cy = (x0+x1)/2, (y0+y1)/2; r = (y1-y0)*0.30
    import math
    pts = [(cx+r*math.sin(2*math.pi*k/5), cy-r*math.cos(2*math.pi*k/5)) for k in range(5)]
    order = [0, 2, 4, 1, 3, 0]; w = max(3, int((y1-y0)*0.035))
    for a, b in zip(order, order[1:]): d.line([pts[a], pts[b]], fill=(0, 98, 51), width=w)
    return img

# ---------------------------------------------------------------- per-shot custom frames
def make_overlay(s, img, t):
    n = s["n"]; d = ImageDraw.Draw(img, "RGBA")
    if n == 21: card(d, (560, 90, 1360, 230), "20 AOÛT 1953", fnt(DS, 78))
    if n == 22: card(d, (560, 90, 1360, 190), "Reconstitution fictive", fnt(DS, 56))
    if n == 27: d.rounded_rectangle((160, 80, 1760, 210), 20, fill=(20, 20, 20, 225)); d.text((960, 145), "16 novembre 1955 — Retour du sultan Mohammed Ben Youssef.", font=fnt(DS, 46), fill=(255, 245, 220), anchor="mm")
    if n == 29:
        card(d, (420, 70, 1500, 200), "18 NOVEMBRE 1955", fnt(DJ, 74), fill=(238, 224, 184, 235), ink=(80, 50, 30))
        d.rounded_rectangle((200, 880, 1720, 960), 18, fill=(0, 0, 0, 185)); d.text((960, 920), "« Le sultan annonce une nouvelle étape vers l'indépendance. »", font=fnt(DS, 40), fill=(255, 245, 220), anchor="mm")
    if n == 31: card(d, (520, 70, 1400, 200), "2 MARS 1956", fnt(DJ, 74), fill=(238, 224, 184, 235), ink=(80, 50, 30))
    if n in (17, 31):  # QC M3 : mention « non archive » (H3b / H4-H5), sur toute la durée du plan
        txt = s["overlay"]["sub"]; fo = fnt(DS, 38); w = d.textlength(txt, font=fo)
        y = 62 if n == 17 else 960   # SH17 : haut (sous-titres en bas) ; SH31 : bas (aucune réplique)
        d.rounded_rectangle((960-w/2-34, y, 960+w/2+34, y+66), 16, fill=(15, 15, 15, 215)); d.text((960, y+33), txt, font=fo, fill=(255, 238, 200), anchor="mm")
    if n == 26 and t > s["dur"]-1.5:
        a = min(1, (t-(s["dur"]-1.5))/1.5); img = Image.blend(img, Image.new("RGB", (FW, FH), (255, 255, 255)), a*a)
    if n == 34 and t > s["dur"]-1.0:
        a = (t-(s["dur"]-1.0)); img = Image.blend(img, Image.new("RGB", (FW, FH), (0, 0, 0)), a*0.9)
    return img

def frame_custom(s, t):
    n = s["n"]; u = t/s["dur"]
    if n == 6:   # chalk date -> notebook page
        a = cam_frame(load(IMG[2]), 2.6, 3.0, (1650, 520), (1650, 520), u); p = paper(); d = ImageDraw.Draw(p)
        d.text((FW//2, FH//2), "18 novembre", font=fnt(AM, 200), fill=(70, 42, 24), anchor="mm")
        return Image.blend(a, p, ease(min(1, u*1.3)))
    if n == 12:  # ink on the page becomes the 1944 street
        a = cam_frame(load(IMG[10]), 1.2, 3.0, (1376, 900), (1376, 900), u); b = cam_frame(load(IMG[13]), 1.15, 1.0, (1376, 768), (1376, 768), u)
        return Image.blend(a, b, ease(np.clip((u-0.35)/0.5, 0, 1)))
    if n == 20:  # ink darkens, pages turn to 1953
        a = cam_frame(load(IMG[10]), 1.8, 3.0, (1376, 900), (1376, 900), u); a = tint(a, "dusk")
        p = tint(paper((222, 208, 176)), "dusk"); d = ImageDraw.Draw(p); d.text((FW//2, FH//2), "1953", font=fnt(AM, 360), fill=(48, 56, 72), anchor="mm")
        return Image.blend(a, p, ease(np.clip((u-0.3)/0.6, 0, 1)))
    if n == 25:  # seasons at the window, pages dated 1953 / 1954 / 1955
        i = min(2, int(t/(s["dur"]/3))); kind = ["autumn", "winter", "spring"][i]
        f = tint(cam_frame(load(IMG[25]), 1.0, 1.06, (1376, 768), (1376, 768), u), kind); d = ImageDraw.Draw(f, "RGBA")
        d.rounded_rectangle((1280, 520, 1840, 980), 24, fill=(240, 226, 186, 235), outline=(110, 80, 50), width=6)
        d.text((1560, 700), ["1953", "1954", "1955"][i], font=fnt(AM, 230), fill=(70, 60, 80), anchor="mm")
        d.text((1560, 880), ["automne", "hiver", "printemps"][i], font=fnt(AM, 80), fill=(110, 90, 70), anchor="mm"); return f
    if n == 33:  # timeline (reuse local graphic)
        return CA.render_base(s, t=t).convert("RGB")
    if n == 38:
        f = cam_frame(load(IMG[38]), 1.0, 1.0, (1376, 768), (1376, 768), 0); f = flag(f, (800, 120, 1130, 320))
        f = f.resize((FW, FH)); d = ImageDraw.Draw(f, "RGBA"); tf = min(1, t/1.0); d.rectangle((0, 0, FW, FH), fill=(0, 0, 0, int(80*tf)))
        d.text((FW//2, 520), "LE CARNET DE LA LIBERTÉ", font=fnt(DJ, 100), fill=(255, 245, 220, int(255*tf)), anchor="mm")
        d.text((FW//2, 660), "18 NOVEMBRE — FÊTE DE L'INDÉPENDANCE DU MAROC", font=fnt(DS, 40), fill=(255, 235, 200, int(255*tf)), anchor="mm")
        if t > s["dur"]-1.5: d.text((FW//2, 790), "FIN", font=fnt(DJ, 60), fill=(255, 245, 220, 255), anchor="mm")
        return f
    return None

class ClipReader:
    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}", "-"], stdout=subprocess.PIPE)
        self.last = None
    def next(self):
        b = self.p.stdout.read(FW*FH*3)
        if len(b) == FW*FH*3: self.last = Image.frombytes("RGB", (FW, FH), b)
        return self.last
    def close(self): self.p.stdout.close(); self.p.kill()

def main():
    limit = None; only = None; clean = "--clean" in sys.argv
    if "--shots" in sys.argv: only = {int(x) for x in sys.argv[sys.argv.index("--shots")+1].split(",")}
    if "--frames" in sys.argv: limit = float(sys.argv[sys.argv.index("--frames")+1])
    OUT.mkdir(exist_ok=True)
    timing = json.loads((OUT/"dialogue_timing.json").read_text())["lines"]
    out = OUT/("MASTER_CLEAN_1080p_video_prep.mp4" if clean else "ANIMATIC_2.0_partial.mp4" if only else ("ANIMATIC_2.0_test.mp4" if limit else "ANIMATIC_2.0_276s.mp4"))
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}", "-r", str(FPS), "-i", "-",
                           *([] if (only or clean) else ["-i", str(OUT/"dialogue_mix.wav")]), "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
                           *(["-an"] if (only or clean) else ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest"]), "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    fs = fnt(DS, 38); ft = fnt(DS, 24); prev = None; report = []
    for s in SHOTS:
        if limit and s["start"] > limit: break
        if only and s["n"] not in only: continue
        n = s["n"]; nfr = int(round(s["dur"]*FPS)); rd = ClipReader(CLIP[n]) if n in CLIP else None
        tr = int(0.5*FPS) if (s.get("trans_in") == "dissolve" or n in (7, 13, 21, 27)) and prev is not None else 0
        if n == 31: tr = 0   # QC M3 : plus de fondu enchaîné depuis SH30 (l'écriture de SH30 transparaissait) -> ouverture au noir 0,4 s
        for f in range(nfr):
            t = f/FPS; u = f/max(1, nfr-1); fr = None
            if rd is not None: fr = rd.next()
            if fr is None:
                c = frame_custom(s, t)
                if c is not None: fr = c
                elif n in CROP: src, z0, z1, c0, c1 = CROP[n]; fr = cam_frame(load(src), z0, z1, c0, c1, u)
                else:
                    z0, z1 = CAMZ[s["cam"]]; fr = cam_frame(load(IMG[n]), z0, z1, (W0/2, H0/2), (W0/2, H0/2), u)
            fr = make_overlay(s, fr.copy(), t)
            if f < tr and prev is not None: fr = Image.blend(prev, fr, ease(f/tr))
            if n == 31 and t < 0.4: fr = Image.blend(Image.new("RGB", (FW, FH), (0, 0, 0)), fr.convert("RGB"), ease(t/0.4))
            gt = s["start"]+t
            if not clean:
                d = ImageDraw.Draw(fr, "RGBA"); gt = s["start"]+t
                d.text((14, 14), f"ANIMATIC 2.0 · voix de repère · SH{n:02d} · {CA.tc(gt)[:5]}", font=ft, fill=(255, 220, 120, 230))
                for tm in timing:
                    if tm["shot"] == n and tm["start"] <= gt <= tm["end"]+0.25:
                        ls = CA.wrap(f"{tm['speaker']} : « {tm['text']} »", fs, 1700, d); y0 = FH-60-46*len(ls)
                        d.rectangle([100, y0-10, FW-100, FH-40], fill=(0, 0, 0, 165))
                        for i, ln in enumerate(ls): d.text((FW//2, y0+20+i*46), ln, font=fs, fill=(255, 255, 255), anchor="mm")
            ff.stdin.write(fr.convert("RGB").tobytes())
        prev = fr.convert("RGB")
        if rd: rd.close()
        report.append({"shot": n, "start": s["start"], "dur": s["dur"], "source": "clip" if n in CLIP else ("custom" if n in (6, 12, 20, 25, 33, 38) else ("crop" if n in CROP else "image"))})
    ff.stdin.close(); ff.wait()
    (OUT/("master_clean_report.json" if clean else "animatic_2.0_report.json")).write_text(json.dumps(report, indent=1))
    print("done", out)

if __name__ == "__main__":
    main()
