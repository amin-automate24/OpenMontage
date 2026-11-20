#!/usr/bin/env python3
"""SH27/SH28 v002 (local compositing, NO AI, 0 credit): vector Moroccan flags (red field, green interlaced pentagram) attached to poles already
present in the validated crowd images. Originals (references/p3/SH27_..._v001.png, SH28_..._v001.png) are never modified. Never overwrites outputs."""
import math, sys, numpy as np, cv2
from pathlib import Path
from PIL import Image, ImageDraw
R = Path(__file__).resolve().parent.parent; OUT = R/"references/p3/post"; OUT.mkdir(exist_ok=True)
RED = (193, 39, 45); GREEN = (0, 98, 51); HAZE = np.array([236, 206, 168], np.float32)
def flag_tex(w, h):
    S = 3; im = Image.new("RGB", (w*S, h*S), RED); d = ImageDraw.Draw(im); cx, cy = w*S/2, h*S/2; r = h*S*0.30
    pts = [(cx+r*math.sin(2*math.pi*k/5), cy-r*math.cos(2*math.pi*k/5)) for k in range(5)]
    for a, b in zip([0, 2, 4, 1, 3, 0], [2, 4, 1, 3, 0]): d.line([pts[a], pts[b]], fill=GREEN, width=max(3, int(h*S*0.035)))
    return np.asarray(im.resize((w, h), Image.LANCZOS))
def add_flag(canvas, top, bottom, w, h, haze, phase, wind=1.0):
    """hoist edge along the pole (from 'top' down by h), flag flies perpendicular to the pole, to the right (wind)."""
    H, W = canvas.shape[:2]; S = 2; tex = flag_tex(w*S, h*S).astype(np.float32)
    d = np.array(bottom, np.float32)-np.array(top, np.float32); d /= np.linalg.norm(d)      # along pole, downward
    fly = np.array([d[1]*-1, d[0]], np.float32)                                                # perpendicular
    if fly[0] < 0: fly = -fly
    fly = fly*wind
    uu, vv = np.meshgrid(np.arange(w*S)/(w*S-1), np.arange(h*S)/(h*S-1))
    amp = 0.085*h*S; wave = amp*uu*np.sin(2*math.pi*(1.25*uu)+phase)                           # amplitude grows toward the free edge
    dwave = np.cos(2*math.pi*(1.25*uu)+phase)*uu                                                # slope -> shading
    droop = 0.05*h*S*uu**2                                                                      # slight gravity droop
    shade = 1.0+0.20*dwave*0.9-0.05*uu
    px = np.array(top, np.float32)[None, None, :]+(fly[None, None, :]*(uu*w*S)[..., None]/S)+(d[None, None, :]*(vv*h*S)[..., None]/S)+d[None, None, :]*((wave+droop)[..., None]/S)*0.35+np.array([-d[1], d[0]], np.float32)[None, None, :]*0
    # waving displaces the cloth along the pole axis and slightly across the fly direction
    px = px+fly[None, None, :]*(-(wave*0.25)[..., None]/S)
    cloth = np.clip(tex*shade[..., None], 0, 255)*(1-haze)+HAZE*haze
    cloth = cloth*np.array([1.0, 0.97, 0.90], np.float32)                                      # warm backlit grade
    layer = np.zeros((H, W, 3), np.float32); alpha = np.zeros((H, W), np.float32); wgt = np.zeros((H, W), np.float32)
    xs = np.clip(np.round(px[..., 0]).astype(int), 0, W-1); ys = np.clip(np.round(px[..., 1]).astype(int), 0, H-1)
    for dx in (0, 1):
        for dy in (0, 1):
            xx = np.clip(xs+dx, 0, W-1); yy = np.clip(ys+dy, 0, H-1); np.add.at(layer, (yy, xx), cloth); np.add.at(wgt, (yy, xx), 1)
    m = (wgt > 0); layer[m] /= wgt[m][..., None]; alpha[m] = 1.0
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)); alpha = cv2.GaussianBlur(alpha, (0, 0), 0.8)
    # fill small holes from forward splatting
    lay = layer.copy()
    for c in range(3): lay[..., c] = np.where(wgt > 0, layer[..., c], cv2.blur(layer[..., c], (3, 3))*9/np.maximum(cv2.blur((wgt > 0).astype(np.float32), (3, 3))*9, 1))
    a = alpha[..., None]; canvas[:] = canvas*(1-a)+lay*a
    # pole sleeve: thin line along the hoist edge in pole colour
    p0 = tuple(int(v) for v in top); p1 = tuple(int(v) for v in (np.array(top)+d*h)); col = tuple(float(v) for v in (150, 112, 60))
    cv2.line(canvas, p0, p1, col, max(3, int(h*0.035)), cv2.LINE_AA)
def run(src, dst, flags):
    if dst.exists(): sys.exit(f"{dst.name} exists")
    img = cv2.cvtColor(cv2.imread(str(src)), cv2.COLOR_BGR2RGB).astype(np.float32)
    for f in flags: add_flag(img, **f)
    cv2.imwrite(str(dst), cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)); print("ok", dst.name, len(flags), "flags")
SH27 = [dict(top=(1411, 366), bottom=(1250, 840), w=270, h=180, haze=0.05, phase=0.3), dict(top=(1905, 357), bottom=(1720, 1030), w=280, h=187, haze=0.05, phase=1.4),
        dict(top=(1153, 370), bottom=(1080, 760), w=210, h=140, haze=0.15, phase=2.2), dict(top=(2295, 462), bottom=(2240, 680), w=170, h=113, haze=0.20, phase=0.9),
        dict(top=(305, 498), bottom=(350, 740), w=150, h=100, haze=0.10, phase=1.9)]
SH28 = [dict(top=(1394, 372), bottom=(1290, 620), w=190, h=127, haze=0.15, phase=0.6), dict(top=(310, 514), bottom=(350, 650), w=140, h=93, haze=0.15, phase=2.0),
        dict(top=(2292, 520), bottom=(2260, 640), w=130, h=87, haze=0.25, phase=1.2)]
if __name__ == "__main__":
    run(R/"references/p3/SH27_foule_rabat1955_v001.png", OUT/"SH27_flags_v002.png", SH27)
    run(R/"references/p3/SH28_amina_pere_foule_v001.png", OUT/"SH28_flags_v002.png", SH28)
