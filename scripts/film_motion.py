#!/usr/bin/env python3
"""film_motion : cale un effet sonore sur le MOUVEMENT reel d'un plan (enveloppe de mouvement video).

Commandes :
  python3 scripts/film_motion.py env  VIDEO T0 T1 [--roi x0,y0,x1,y1]
      affiche le profil de mouvement (0..1) toutes les 0,25 s entre T0 et T1 (secondes du film).
  python3 scripts/film_motion.py gate SFX VIDEO T0 T1 OUT.wav [--roi x0,y0,x1,y1] [--floor 0.0] [--power 1.0]
      produit OUT.wav (duree T1-T0) : l'effet SFX (boucle/decoupe) module par le mouvement ;
      le son suit le geste, il est muet quand rien ne bouge.

--roi : zone d'interet en fractions de l'image (0..1), ex. 0.25,0.45,0.75,0.8. Sans ROI : image entiere.
Ne modifie jamais une source ; OUT doit etre un nouveau fichier (refus d'ecraser).
"""
from __future__ import annotations

import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SR = 48000
FPS = 12
W = 160


def _decode_frames(video: Path, t0: float, t1: float, roi):
    h_out = None
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", str(video),
           "-vf", f"fps={FPS},scale={W}:-2,format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    # hauteur : deduite de la taille de la 1re image (ffprobe)
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(video)],
        capture_output=True, text=True, check=True).stdout.strip()
    vw, vh = (int(x) for x in probe.split("x"))
    h_out = int(round(W * vh / vw / 2) * 2)
    n = len(raw) // (W * h_out)
    frames = np.frombuffer(raw[: n * W * h_out], dtype=np.uint8).reshape(n, h_out, W).astype(np.float32)
    if roi:
        x0, y0, x1, y1 = roi
        frames = frames[:, int(y0 * h_out): max(int(y1 * h_out), int(y0 * h_out) + 1), int(x0 * W): max(int(x1 * W), int(x0 * W) + 1)]
    return frames


def envelope(video: Path, t0: float, t1: float, roi=None, smooth_s: float = 0.25) -> np.ndarray:
    """Enveloppe de mouvement normalisee 0..1 echantillonnee a FPS Hz."""
    fr = _decode_frames(video, t0, t1, roi)
    if len(fr) < 2:
        return np.zeros(max(len(fr), 1))
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    d = np.concatenate([[d[0]], d])
    k = max(int(round(smooth_s * FPS)), 1)
    d = np.convolve(d, np.ones(k) / k, mode="same")
    ref = np.percentile(d, 95) or 1.0
    return np.clip(d / ref, 0, 1)


def _decode_audio(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def gate(sfx: Path, video: Path, t0: float, t1: float, out: Path, roi=None, floor: float = 0.0, power: float = 1.0) -> Path:
    if out.exists():
        raise SystemExit(f"refus d'ecraser : {out}")
    n = int((t1 - t0) * SR)
    a = _decode_audio(sfx)
    if len(a) == 0:
        raise SystemExit("effet vide")
    reps = int(np.ceil(n / len(a)))
    a = np.tile(a, reps)[:n]
    env = envelope(video, t0, t1, roi)
    xs = np.linspace(0, 1, len(env))
    g = np.interp(np.linspace(0, 1, n), xs, env) ** power
    g = floor + (1 - floor) * g
    y = a * g.astype(np.float32)
    fade = min(int(0.02 * SR), n // 4)
    if fade:
        y[:fade] *= np.linspace(0, 1, fade)
        y[-fade:] *= np.linspace(1, 0, fade)
    pcm = np.clip(y * 32767, -32768, 32767).astype("<i2")
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return out


def _roi(args):
    if "--roi" in args:
        return tuple(float(x) for x in args[args.index("--roi") + 1].split(","))
    return None


def _opt(args, name, default):
    return float(args[args.index(name) + 1]) if name in args else default


def main(argv):
    if len(argv) >= 5 and argv[1] == "env":
        env = envelope(Path(argv[2]), float(argv[3]), float(argv[4]), _roi(argv))
        t0 = float(argv[3])
        step = max(int(0.25 * FPS), 1)
        for i in range(0, len(env), step):
            print(f"{t0 + i / FPS:7.2f}s  {'#' * int(env[i] * 40):40s} {env[i]:.2f}")
        return 0
    if len(argv) >= 7 and argv[1] == "gate":
        out = gate(Path(argv[2]), Path(argv[3]), float(argv[4]), float(argv[5]), Path(argv[6]),
                   _roi(argv), _opt(argv, "--floor", 0.0), _opt(argv, "--power", 1.0))
        print(out)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
