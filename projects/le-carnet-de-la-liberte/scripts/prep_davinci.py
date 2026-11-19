#!/usr/bin/env python3
"""Préparation DaVinci Resolve Free (sans rendu) : FCPXML 1.8 « LÉGÈRE » (38 plans + générique découpés dans le master CINÉMA v3)
et « COMPLÈTE » (gabarit pour clips ProRes par plan, non encore générés), LUT .cube nuit 1953, liste des plans."""
import sys, json, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(R/"scripts"))
import build_qc2 as Q
OUT = R/"deliverables/DAVINCI_PREP"; ROOT = "file:///C:/LE_CARNET_DE_LA_LIBERTE/MEDIA/"
MP4 = "LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v3_1080p.mp4"; WAV = "MIX_276s_QC2_SON2.wav"; N_TOTAL = 7475
shots, acc = [], 0
for s in Q.B.SHOTS:
    n = int(round(s["dur"]*25)); shots.append(dict(n=s["n"], start=acc, frames=n, transition="fondu 0,5 s intégré" if (s["n"] in Q.DISSOLVE and acc > 0) else "coupe", lieu=s["loc"])); acc += n
assert acc == 6903
shots.append(dict(n=39, start=6903, frames=572, transition="coupe (générique V005)", lieu="GÉNÉRIQUE"))
f = lambda k: f"{k}/25s"
def fcpxml(name, mode):
    root = ET.Element("fcpxml", version="1.8"); res = ET.SubElement(root, "resources")
    ET.SubElement(res, "format", id="r1", name="FFVideoFormat1080p25", frameDuration="1/25s", width="1920", height="1080")
    if mode == "legere":
        ET.SubElement(res, "asset", id="r2", name=MP4, src=ROOT+MP4, start="0s", duration=f(N_TOTAL), hasVideo="1", hasAudio="1", format="r1", audioSources="1", audioChannels="2", audioRate="48000")
    else:
        for i, s in enumerate(shots):
            nm = f"PLAN_SH{s['n']:02d}.mov" if s["n"] <= 38 else "GENERIQUE_V005.mov"
            ET.SubElement(res, "asset", id=f"v{i}", name=nm, src=ROOT+"PRORES/"+nm, start="0s", duration=f(s["frames"]), hasVideo="1", format="r1")
        ET.SubElement(res, "asset", id="a1", name=WAV, src=ROOT+WAV, start="0s", duration=f(6900), hasAudio="1", audioSources="1", audioChannels="2", audioRate="48000")
    ev = ET.SubElement(ET.SubElement(root, "library"), "event", name="LE CARNET DE LA LIBERTE")
    seq = ET.SubElement(ET.SubElement(ev, "project", name=name), "sequence", format="r1", duration=f(N_TOTAL), tcStart="0s", tcFormat="NDF", audioLayout="stereo", audioRate="48k")
    spine = ET.SubElement(seq, "spine")
    for i, s in enumerate(shots):
        lab = f"SH{s['n']:02d}" if s["n"] <= 38 else "GENERIQUE"
        if mode == "legere": c = ET.SubElement(spine, "asset-clip", ref="r2", name=lab, offset=f(s["start"]), start=f(s["start"]), duration=f(s["frames"]), format="r1", tcFormat="NDF")
        else:
            c = ET.SubElement(spine, "asset-clip", ref=f"v{i}", name=lab, offset=f(s["start"]), start="0s", duration=f(s["frames"]), format="r1", tcFormat="NDF")
            if i == 0: ET.SubElement(c, "asset-clip", ref="a1", name="MIX QC2 SON2 (validé)", lane="-1", offset="0s", start="0s", duration=f(6900))
        ET.SubElement(c, "marker", start=f(s["start"]) if mode == "legere" else "0s", duration="1/25s", value=f"{lab} — {s['transition']} — {s['lieu']}")
    ET.indent(root); p = OUT/f"{name}.fcpxml"
    p.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n' + ET.tostring(root, encoding="unicode"), encoding="utf-8"); return p
for name, mode in (("CARNET_TIMELINE_LEGERE_v3", "legere"), ("CARNET_TIMELINE_COMPLETE_PRORES_gabarit", "complete")):
    p = fcpxml(name, mode); t = ET.parse(p); sp = t.getroot().find(".//spine")
    clips = sp.findall("asset-clip"); offs = [int(c.get("offset").split("/")[0]) for c in clips]; durs = [int(c.get("duration").split("/")[0]) for c in clips]
    assert offs == [sum(durs[:i]) for i in range(len(durs))] and sum(durs) == N_TOTAL; print("ok", p.name, len(clips), "clips,", sum(durs), "images")
# LUT nuit 1953 : même courbe que le comparatif (ffmpeg curves, spline cubique naturelle)
X = np.array([0, .08, .25, .5, .8, 1.]); Y = np.array([0, .10, .33, .58, .84, 1.])
def spline(x, y):
    n = len(x); h = np.diff(x); A = np.zeros((n, n)); b = np.zeros(n); A[0, 0] = A[-1, -1] = 1
    for i in range(1, n-1): A[i, i-1:i+2] = [h[i-1], 2*(h[i-1]+h[i]), h[i]]; b[i] = 3*((y[i+1]-y[i])/h[i]-(y[i]-y[i-1])/h[i-1])
    c = np.linalg.solve(A, b)
    def F(t):
        i = np.clip(np.searchsorted(x, t)-1, 0, n-2); d = t-x[i]; bb = (y[i+1]-y[i])/h[i]-h[i]*(2*c[i]+c[i+1])/3; dd = (c[i+1]-c[i])/(3*h[i])
        return np.clip(y[i]+bb*d+c[i]*d**2+dd*d**3, 0, 1)
    return F
F = spline(X, Y); N = 33; g = np.linspace(0, 1, N)
with open(OUT/"NUIT1953_SH21-23_releve_doux.cube", "w") as fh:
    fh.write('TITLE "Carnet - nuit 1953 releve ombres/tons moyens (comparatif)"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
    for b_ in g:
        for gg in g:
            for r in g: fh.write(f"{F(r):.6f} {F(gg):.6f} {F(b_):.6f}\n")
json.dump(shots, open(OUT/"LISTE_PLANS_38_PLUS_GENERIQUE.json", "w"), ensure_ascii=False, indent=1); print("LUT + liste écrites")
