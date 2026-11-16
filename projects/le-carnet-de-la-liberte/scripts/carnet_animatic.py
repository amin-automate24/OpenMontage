#!/usr/bin/env python3
"""Local animatic builder for LE CARNET DE LA LIBERTE (no network, no paid calls).

Usage: python3 carnet_animatic.py [--no-video]
Outputs (relative to project root):
  animatic/dialogue_mix.wav, animatic/dialogue_timing.json,
  animatic/contact_sheet.png, animatic/ANIMATIC_1.0_LOCAL_PLACEHOLDER.mp4
Voices are INTERNAL espeak-ng placeholders - never publish.
"""
import json, math, os, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
from shots_data import SHOTS, SCENES, LINES, VOICES, CAMERAS, FPS, TOTAL, validate

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "animatic"
VOX = OUT / "voices"
W, H = 1920, 1080
SR = 48000
FD = "/usr/share/fonts/truetype/dejavu/"
def font(sz, bold=False, serif=False, italic=False):
    name = "DejaVuSerif" if serif else "DejaVuSans"
    if bold: name += "-Bold"
    return ImageFont.truetype(FD + name + ".ttf", sz)

PAL = {  # scene -> (bg_top, bg_bottom, accent, text)
    1: ((247, 240, 222), (222, 205, 170), (80, 130, 140), (50, 40, 30)),
    2: ((240, 220, 180), (214, 180, 130), (150, 100, 60), (55, 38, 24)),
    3: ((214, 168, 100), (150, 106, 58), (96, 62, 30), (45, 28, 14)),
    4: ((112, 132, 150), (52, 66, 80), (170, 190, 205), (235, 240, 245)),
    5: ((240, 200, 120), (225, 160, 80), (180, 90, 40), (60, 36, 18)),
    6: ((248, 242, 226), (226, 210, 178), (80, 130, 140), (50, 40, 30)),
}
CHAR_COL = {"Younes": (70, 120, 190), "Maîtresse": (150, 90, 120), "Mère": (170, 110, 90), "Père": (110, 80, 50),
            "Amina 11": (200, 140, 80), "Amina 20": (190, 120, 110), "Amina 22": (200, 130, 100), "Amina 23": (205, 125, 95),
            "Habitants": (130, 110, 90), "Foule": (170, 110, 70), "Élèves": (120, 150, 160), "Radio": (90, 70, 60)}


def grad(top, bot):
    a = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(top)[None, None, :] * (1 - a) + np.array(bot)[None, None, :] * a)
    arr = np.repeat(arr, W, axis=1).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def draw_set(d, img, s, pal):
    key = s["set"]
    acc = pal[2]
    dark = tuple(int(c * 0.6) for c in pal[1])
    if key == "classroom":
        d.rectangle([260, 130, 1200, 620], fill=(46, 70, 60), outline=(110, 80, 50), width=10)  # board
        for i in range(4): d.rectangle([1300 + i * 140, 160, 1400 + i * 140, 420], fill=(200, 225, 235))  # windows
        d.polygon([(1300, 160), (1000, 1000), (1200, 1000), (1500, 160)], fill=(255, 245, 200))  # sun ray (flat)
        d.rectangle([0, 780, W, H], fill=dark)
        for i in range(5): d.rectangle([150 + i * 360, 760, 420 + i * 360, 800], fill=(150, 110, 70))
    elif key == "home2026":
        d.rectangle([0, 760, W, H], fill=dark)
        d.rectangle([1250, 180, 1700, 640], fill=(210, 230, 235), outline=(120, 90, 60), width=8)
        d.rectangle([180, 600, 620, 800], fill=(150, 110, 80))
    elif key == "street1944":
        d.rectangle([0, 820, W, H], fill=dark)
        for i, x in enumerate([0, 520, 1100, 1560]):
            d.rectangle([x, 120 + (i % 2) * 60, x + 420, 820], fill=tuple(int(c * (0.9 - 0.08 * i)) for c in pal[1]), outline=dark, width=6)
            d.rounded_rectangle([x + 140, 520, x + 280, 820], 70, fill=dark)
    elif key in ("home_day", "home_night", "window"):
        d.rectangle([0, 800, W, H], fill=dark)
        d.rounded_rectangle([1260, 140, 1640, 620], 190, fill=(255, 238, 190) if key != "home_night" else (60, 80, 110), outline=dark, width=10)
        d.rectangle([240, 640, 760, 820], fill=tuple(int(c * 0.7) for c in pal[1]))
        if key == "home_night": d.rectangle([1540, 520, 1780, 700], fill=(70, 55, 45))  # radio shelf
    elif key == "rabat":
        d.rectangle([0, 800, W, H], fill=dark)
        for i in range(7): d.rectangle([60 + i * 270, 260 + (i % 3) * 40, 260 + i * 270, 800], fill=tuple(int(c * 0.85) for c in pal[1]))
        for i in range(9):  # flag placeholders (red + green star = will be vector-composited later)
            x = 100 + i * 200
            d.line([x, 420, x, 640], fill=(80, 60, 40), width=6)
            d.rectangle([x, 420, x + 110, 500], fill=(190, 40, 40))
            d.text((x + 38, 432), "★", font=font(40), fill=(30, 120, 60))
    elif key == "flag":
        d.rectangle([0, 800, W, H], fill=dark)
        d.rectangle([760, 160, 1160, 400], fill=(190, 40, 40))
        d.text((900, 220), "★", font=font(120), fill=(30, 120, 60))
        d.rounded_rectangle([700, 640, 1220, 880], 20, fill=(246, 238, 215), outline=dark, width=6)
    elif key in ("page", "document", "timeline"):
        d.rounded_rectangle([200, 70, W - 200, H - 70], 30, fill=(238, 222, 180), outline=dark, width=8)


def draw_chars(d, s, pal):
    for (label, xf, sc) in s["chars"]:
        col = CHAR_COL.get(label, (120, 120, 120))
        cx = int(xf * W)
        if label == "Radio":
            d.rounded_rectangle([cx - 260, 360, cx + 260, 720], 40, fill=col, outline=(30, 20, 10), width=8)
            d.ellipse([cx - 120, 450, cx + 120, 690], fill=(255, 210, 120), outline=(30, 20, 10), width=6)
            d.text((cx - 70, 380), "RADIO", font=font(50, True), fill=(255, 220, 160))
            continue
        hh = int(165 * sc)
        body_h = int(330 * sc)
        base = 930
        top = base - body_h
        d.rounded_rectangle([cx - int(90 * sc), top, cx + int(90 * sc), base], int(60 * sc), fill=col)
        d.ellipse([cx - hh // 2, top - hh + 20, cx + hh // 2, top + 20], fill=tuple(min(255, c + 60) for c in col), outline=(40, 30, 20), width=4)
        d.text((cx, top + int(80 * sc)), label, font=font(max(18, int(30 * min(sc, 1.3)))), fill=(255, 255, 255), anchor="mm")


def wrap(text, fnt, maxw, d):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def centered(d, text, y, fnt, fill, maxw=1500):
    for ln in wrap(text, fnt, maxw, d):
        d.text((W // 2, y), ln, font=fnt, fill=fill, anchor="mm")
        y += int(fnt.size * 1.25)
    return y


def draw_overlay(d, s, pal, state=None, t=None):
    ov = s.get("overlay")
    if not ov: return
    k = ov["kind"]
    txt = pal[3]
    if k == "board":
        d.text((730, 320), ov["text"], font=font(54, True), fill=(235, 235, 225), anchor="mm")
    elif k == "date_card":
        d.rounded_rectangle([560, 90, 1360, 230], 30, fill=(20, 28, 38), outline=pal[2], width=5)
        d.text((W // 2, 160), ov["text"], font=font(78, True), fill=(235, 240, 245), anchor="mm")
    elif k == "page":
        d.rounded_rectangle([420, 200, 1500, 880], 24, fill=(240, 226, 186), outline=(110, 80, 50), width=8)
        d.text((W // 2, 480), ov["text"], font=font(92, serif=True, bold=True), fill=(80, 50, 30), anchor="mm")
        if ov.get("sub"): d.text((W // 2, 640), "(" + ov["sub"] + ")", font=font(34, italic=True), fill=(120, 90, 60), anchor="mm")
    elif k == "cover":
        d.rounded_rectangle([520, 150, 1400, 900], 30, fill=(120, 76, 44), outline=(60, 36, 20), width=10)
        d.text((W // 2, 500), ov["text"], font=font(66, serif=True, bold=True), fill=(240, 215, 160), anchor="mm")
    elif k == "handwriting":
        d.rounded_rectangle([360, 130, 1560, 360], 24, fill=(242, 230, 192), outline=(110, 80, 50), width=6)
        centered(d, "« " + ov["text"] + " »", 245, font(54, serif=True, italic=True), (60, 40, 25), 1100)
    elif k == "document":
        d.text((W // 2, 160), ov["text"], font=font(54, serif=True, bold=True), fill=(70, 45, 25), anchor="mm")
        for i in range(10): d.line([440, 300 + i * 52, 1480, 300 + i * 52], fill=(160, 130, 90), width=5)
        d.rectangle([300, 120, 1620, 960], outline=(130, 95, 55), width=6)
        d.text((W // 2, 1005), ov["sub"], font=font(32, bold=True), fill=(130, 40, 40), anchor="mm")
    elif k == "page_illus":
        d.text((W // 2, 170), ov["text"], font=font(84, serif=True, bold=True), fill=(80, 50, 30), anchor="mm")
        d.rectangle([420, 260, 1500, 700], fill=(206, 186, 140), outline=(120, 90, 55), width=6)
        d.text((W // 2, 480), "[ illustration pédagogique ]", font=font(44, italic=True), fill=(120, 90, 60), anchor="mm")
        if ov.get("caption"): centered(d, ov["caption"], 790, font(46, serif=True), (60, 38, 22), 1300)
        d.text((W // 2, 1000), ov["sub"], font=font(30, bold=True), fill=(130, 40, 40), anchor="mm")
    elif k == "lower_text":
        d.rounded_rectangle([160, 80, W - 160, 210], 20, fill=(20, 20, 20))
        centered(d, ov["text"], 145, font(48, bold=True), (255, 245, 220), 1500)
    elif k == "date_to_page":
        d.rounded_rectangle([420, 250, 1500, 800], 24, fill=(240, 226, 186), outline=(110, 80, 50), width=8)
        d.text((W // 2, 520), ov["text"], font=font(110, serif=True, bold=True), fill=(80, 50, 30), anchor="mm")
        d.text((W // 2, 700), "(" + ov["sub"] + ")", font=font(32, italic=True), fill=(120, 90, 60), anchor="mm")
    elif k == "ink_to_street":
        d.text((W // 2, 520), "L'encre devient la rue de 1944", font=font(70, serif=True, italic=True), fill=pal[3], anchor="mm")
    elif k == "pages_to":
        d.text((W // 2, 460), ov["text"], font=font(220, serif=True, bold=True), fill=(60, 66, 80), anchor="mm")
        d.text((W // 2, 700), "(" + ov["sub"] + ")", font=font(36, italic=True), fill=(60, 50, 40), anchor="mm")
    elif k == "montage":
        yrs, seas = ov["years"], ov["seasons"]
        i = min(len(yrs) - 1, int((t or 0) / (s["dur"] / len(yrs))))
        d.rounded_rectangle([420, 160, 1500, 920], 24, fill=(240, 226, 186), outline=(110, 80, 50), width=8)
        d.text((W // 2, 450), yrs[i], font=font(230, serif=True, bold=True), fill=(70, 60, 80), anchor="mm")
        d.text((W // 2, 700), "(" + seas[i] + " à la fenêtre)", font=font(48, italic=True), fill=(110, 90, 70), anchor="mm")
    elif k == "timeline":
        items = ov["items"]
        d.text((W // 2, 140), "LIGNE DU TEMPS", font=font(60, serif=True, bold=True), fill=(80, 50, 30), anchor="mm")
        n = len(items)
        reveal = 1.2  # seconds between reveals
        shown = n if t is None else min(n, int(t / reveal) + 1)
        d.line([420, 260, 420, 260 + (n - 1) * 120 + 40], fill=(120, 80, 40), width=8)
        for j, (dt, tx) in enumerate(items[:shown]):
            y = 270 + j * 120
            d.ellipse([402, y - 4, 438, y + 32], fill=(170, 60, 40))
            d.text((480, y + 14), dt, font=font(46, bold=True), fill=(70, 40, 20), anchor="lm")
            d.text((1010, y + 14), tx, font=font(38), fill=(50, 35, 25), anchor="lm")
    elif k == "title":
        d.rectangle([0, 0, W, H], fill=(0, 0, 0, 0))
    # flash_end / fade_out_end handled in frame loop


def render_base(s, t=None):
    pal = PAL[s["scene"]]
    if s["scene"] == 5 and s["n"] in (27, 28): pal = PAL[5]
    if s["set"] == "window" and s["scene"] == 4: pal = PAL[5]
    img = grad(pal[0], pal[1])
    d = ImageDraw.Draw(img, "RGBA")
    draw_set(d, img, s, pal)
    draw_chars(d, s, pal)
    draw_overlay(d, s, pal, t=t)
    ov = s.get("overlay")
    if ov and ov["kind"] == "title":
        d.rectangle([0, 0, W, H], fill=(0, 0, 0, 90))
    return img


def make_hud(s):
    """Static RGBA overlay (top bar, bottom info)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([0, 0, W, 54], fill=(0, 0, 0, 170))
    d.text((16, 27), f"ANIMATIC 1.0 — PLACEHOLDER — voix synthétiques internes — NE PAS PUBLIER", font=font(22, bold=True), fill=(255, 210, 90), anchor="lm")
    d.rectangle([0, H - 62, W, H], fill=(0, 0, 0, 170))
    meth = {"STILL_CAM": "image fixe + mouvement caméra", "I2V": "IMAGE→VIDÉO (clip animé)", "CARD_COMP": "carton/graphique local", "TRANSITION": "transition locale"}[s["method"]]
    d.text((16, H - 31), f"SH{s['n']:02d} [{s['kind']}] SC{s['scene']} | {s['framing']} | cam: {s['cam']} | {meth} | {s['loc']}", font=font(22), fill=(255, 255, 255), anchor="lm")
    if s["flags"]:
        d.text((W - 16, H - 31), "⚠ revue historique: " + ",".join(s["flags"]), font=font(22, bold=True), fill=(255, 150, 120), anchor="rm")
    return layer


def tc(t):
    fr = int(round((t - int(t)) * FPS)) % FPS
    return f"{int(t)//60:02d}:{int(t)%60:02d}:{fr:02d}"


# ---------------------------------------------------------------- audio
def espeak(key, path):
    spk, text = LINES[key]
    vk = key if key in VOICES else key[0]
    var, pitch, speed = VOICES[vk]
    subprocess.run(["espeak-ng", "-v", var, "-p", str(pitch), "-s", str(speed), "-w", str(path), text], check=True)


def load48(path, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)]
    if af: cmd += ["-af", af]
    cmd += ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def build_audio():
    VOX.mkdir(parents=True, exist_ok=True)
    mix = np.zeros(int(TOTAL * SR) + SR, dtype=np.float32)
    timing = []
    for s in SHOTS:
        for key, off in s["lines"]:
            p = VOX / f"{key}.wav"
            if not p.exists(): espeak(key, p)
            af = None
            gain = 1.0
            if key == "R1": af = "highpass=f=450,lowpass=f=3000,acrusher=bits=9:mode=log:aa=1:mix=0.35"; gain = 0.9
            if key == "V1": af = "lowpass=f=2500,aecho=0.8:0.6:60:0.25"; gain = 0.75
            a = load48(p, af) * gain
            st = s["start"] + off
            i0 = int(st * SR)
            mix[i0:i0 + len(a)] += a
            dur = len(a) / SR
            end = st + dur
            win_end = s["start"] + s["dur"]
            timing.append(dict(key=key, speaker=LINES[key][0], text=LINES[key][1], shot=s["n"], scene=s["scene"],
                               start=round(st, 2), synth_dur=round(dur, 2), end=round(end, 2),
                               shot_end=round(win_end, 2), slack_synth=round(win_end - end, 2),
                               human_end_x1_2=round(st + dur * 1.2, 2), slack_human_x1_2=round(win_end - (st + dur * 1.2), 2),
                               fits_synth=end <= win_end + 1e-6, fits_human_x1_2=(st + dur * 1.2) <= win_end + 1e-6))
    pk = np.abs(mix).max()
    mix = mix / pk * 0.7 if pk > 0 else mix
    mix = mix[: int(TOTAL * SR)]
    OUT.mkdir(exist_ok=True)
    stereo = np.stack([mix, mix], axis=1)
    pcm = (np.clip(stereo, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(OUT / "dialogue_mix.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return timing, mix


def analyse(timing):
    per_scene = {}
    for sc, info in SCENES.items():
        dur = info["end"] - info["start"]
        sp = sum(t["synth_dur"] for t in timing if t["scene"] == sc)
        per_scene[sc] = dict(title=info["title"], duration=dur, speech_synth=round(sp, 1), speech_x1_2=round(sp * 1.2, 1),
                             load_synth_pct=round(100 * sp / dur), load_human_pct=round(100 * sp * 1.2 / dur))
    return per_scene


# ---------------------------------------------------------------- video
def ease(x): return x * x * (3 - 2 * x)


def contact_sheet():
    cols, rows = 6, 7
    tw, th = 480, 270
    sheet = Image.new("RGB", (cols * tw, rows * (th + 30)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, s in enumerate(SHOTS):
        base = render_base(s, t=s["dur"] * 0.6).convert("RGB").resize((tw, th), Image.BILINEAR)
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        sheet.paste(base, (x, y + 30))
        d.text((x + 6, y + 15), f"SH{s['n']:02d} {tc(s['start'])[:5]} {s['dur']:.1f}s {s['framing']} [{s['method']}]", font=font(15, bold=True), fill=(255, 255, 255), anchor="lm")
    sheet.save(OUT / "contact_sheet.png")


def render_video(timing):
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(OUT / "dialogue_mix.wav"),
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart",
           str(OUT / "ANIMATIC_1.0_LOCAL_PLACEHOLDER.mp4")]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    prev_last = None
    fnt_tc = font(30, bold=True)
    fnt_sub = font(40, bold=True)
    for s in SHOTS:
        nfr = int(round(s["dur"] * FPS))
        z0, z1, px, py = CAMERAS[s["cam"]]
        hud = make_hud(s)
        ov = s.get("overlay") or {}
        dynamic = ov.get("kind") in ("montage", "timeline")
        base = None if dynamic else render_base(s)
        cache = {}
        tr = s.get("trans_in", "cut")
        trlen = int(0.6 * FPS) if tr == "dissolve" else 0
        for f in range(nfr):
            t = f / FPS
            if dynamic:
                key = int(t * 2)
                if key not in cache: cache[key] = render_base(s, t=t)
                b = cache[key]
            else:
                b = base
            u = ease(f / max(1, nfr - 1))
            z = z0 + (z1 - z0) * u
            cw, ch = W / z, H / z
            ox = (W - cw) / 2 + px * (u - 0.5) * (W - cw) * 2 * 0.5
            oy = (H - ch) / 2
            fr = b.transform((W, H), Image.EXTENT, (ox, oy, ox + cw, oy + ch), Image.BILINEAR) if z != 1.0 or px else b.copy()
            if f < trlen and prev_last is not None:
                fr = Image.blend(prev_last, fr, ease(f / trlen))
            # end effects
            k = ov.get("kind")
            if k == "flash_end" and t > s["dur"] - 1.5:
                a = min(1, (t - (s["dur"] - 1.5)) / 1.5)
                fr = Image.blend(fr, Image.new("RGB", (W, H), (255, 255, 255)), a * a)
            if k == "fade_out_end" and t > s["dur"] - 1.0:
                a = (t - (s["dur"] - 1.0)) / 1.0
                fr = Image.blend(fr, Image.new("RGB", (W, H), (0, 0, 0)), a * 0.9)
            if k == "title":
                tf = min(1, t / 1.0)
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
                dd.text((W // 2, 430), ov["text"], font=font(110, serif=True, bold=True), fill=(255, 245, 220, int(255 * tf)), anchor="mm")
                dd.text((W // 2, 590), ov["sub"], font=font(42, bold=True), fill=(255, 235, 200, int(255 * tf)), anchor="mm")
                if t > s["dur"] - 1.5: dd.text((W // 2, 760), ov["end"], font=font(60, serif=True, bold=True), fill=(255, 245, 220, 255), anchor="mm")
                fr = Image.alpha_composite(fr.convert("RGBA"), lay).convert("RGB")
            if k == "handwriting" and ov.get("late") and t < 1.5 + 2.8:  # appears while Younes speaks Y5
                pass
            fr = Image.alpha_composite(fr.convert("RGBA"), hud)
            d = ImageDraw.Draw(fr)
            gt = s["start"] + t
            d.text((W - 16, 27), f"{tc(gt)} / 04:30:00   shot {s['n']:02d}/38", font=fnt_tc, fill=(255, 255, 255), anchor="rm")
            # subtitle
            for tm in timing:
                if tm["shot"] == s["n"] and tm["start"] <= gt <= tm["end"] + 0.25:
                    txt = f"{tm['speaker']} : « {tm['text']} »"
                    ls = wrap(txt, fnt_sub, 1700, d)
                    y0 = H - 100 - 52 * len(ls)
                    d.rectangle([100, y0 - 14, W - 100, H - 80], fill=(0, 0, 0, 175))
                    for i, ln in enumerate(ls):
                        d.text((W // 2, y0 + 22 + i * 52), ln, font=fnt_sub, fill=(255, 255, 255), anchor="mm")
            ff.stdin.write(fr.convert("RGB").tobytes())
        prev_last = fr.convert("RGB") if False else b.convert("RGB")
    ff.stdin.close()
    ff.wait()


def main():
    probs = validate()
    if probs:
        print("VALIDATION FAILED", probs); sys.exit(1)
    OUT.mkdir(exist_ok=True)
    timing, _ = build_audio()
    per_scene = analyse(timing)
    (OUT / "dialogue_timing.json").write_text(json.dumps(dict(lines=timing, per_scene=per_scene), ensure_ascii=False, indent=2))
    contact_sheet()
    if "--no-video" not in sys.argv:
        render_video(timing)
    print("done")
    for sc, v in per_scene.items(): print(sc, v)
    print("lines not fitting @x1.2:", [t["key"] for t in timing if not t["fits_human_x1_2"]])
    print("lines not fitting synth:", [t["key"] for t in timing if not t["fits_synth"]])


if __name__ == "__main__":
    main()
