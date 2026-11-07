#!/usr/bin/env python3
"""film_mix : mixage audio pilote par un JSON de reperes (ffmpeg), sources en lecture seule.

Usage :
  python3 scripts/film_mix.py plan  MIX.json   # liste les pistes et le calendrier
  python3 scripts/film_mix.py render MIX.json  # rend 12_EDITING/AUDIO/<output>.wav (+ .mp4 si "video")

MIX.json :
{
 "project": "..",                     # racine du projet, relative au dossier du JSON (ou absolue)
 "output": "MIX_S1-S2_v1",            # nom de base, versionne automatiquement (_v2 ...) si existe
 "duration": 140.4,                   # secondes (sinon duree de la video)
 "video": "12_EDITING/FILM_S1-S2_cut_v1.mp4",   # optionnel : produit aussi un mp4 (video copiee + audio AAC)
 "target_lufs": -16,                  # loudness finale (optionnel)
 "tracks": [
   {"file": "11_AUDIO/AMBIENCE/x.mp3", "start": 0.0, "dur": 30,   # dur : decoupe/boucle
    "in": 0.0, "loop": true, "lufs": -34, "gain_db": 0, "smooth": false,
    "fade_in": 1.0, "fade_out": 1.0, "label": "ambiance"}
 ]
}
Une piste avec "lufs" est normalisee a ce niveau par un GAIN STATIQUE mesure (jamais de loudnorm dynamique),
puis "gain_db" est ajoute. "norm_whole": true mesure le fichier source ENTIER (utile pour decouper une musique en
segments sans aplatir son crescendo). "smooth": true lisse les rafales d'une ambiance. "loop": true boucle la source.
Ne modifie, ne supprime, n'ecrase jamais une source ; les sorties vont dans 12_EDITING/AUDIO/ (versionnees).
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def versioned(path: Path) -> Path:
    if not path.exists():
        return path
    n = 2
    while True:
        cand = path.with_name(f"{path.stem}_v{n}{path.suffix}")
        if not cand.exists():
            return cand
        n += 1


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def load(mix_path: Path) -> tuple[dict, Path]:
    spec = json.loads(mix_path.read_text())
    root = (mix_path.resolve().parent / spec.get("project", ".")).resolve()
    return spec, root


def total_duration(spec: dict, root: Path) -> float:
    if spec.get("duration"):
        return float(spec["duration"])
    if spec.get("video"):
        return probe_duration(root / spec["video"])
    raise SystemExit("duration ou video requis")


def prep_track(i: int, t: dict, root: Path, tmpdir: Path, total: float) -> tuple[Path, float]:
    """Pre-rend la piste (decoupe, boucle, lissage) en WAV 48 kHz stereo et calcule un GAIN STATIQUE mesure.
    Pas de loudnorm dynamique : le niveau cible `lufs` est atteint par un gain constant (fiable, deterministe)."""
    src = root / t["file"]
    if not src.exists():
        raise SystemExit(f"source introuvable : {src}")
    start = float(t.get("start", 0.0))
    length = min(float(t["dur"]) if t.get("dur") else total - start, total - start)
    chain = []
    if float(t.get("in", 0.0)):
        chain.append(f"atrim=start={float(t['in'])},asetpts=PTS-STARTPTS")
    chain.append(f"atrim=duration={length:.3f},asetpts=PTS-STARTPTS")
    chain.append("aformat=sample_rates=48000:channel_layouts=stereo")
    if t.get("smooth"):
        # lisse les rafales / variations rapides d'une ambiance (niveau plus regulier, plus fluide)
        chain.append("acompressor=threshold=0.015:ratio=10:attack=250:release=1000:makeup=2,dynaudnorm=f=1500:g=51:p=0.9:m=10")
    out = tmpdir / f"track_{i}.wav"
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if t.get("loop"):
        cmd += ["-stream_loop", "-1"]
    cmd += ["-i", str(src), "-af", ",".join(chain), "-t", f"{length:.3f}", "-ar", "48000", "-ac", "2", str(out)]
    subprocess.run(cmd, check=True)
    gain = float(t.get("gain_db", 0.0))
    if t.get("lufs") is not None:
        try:
            m = measure_lufs(src) if t.get("norm_whole") else measure_lufs(out)
            if m > -60:  # piste quasi silencieuse : pas de normalisation
                gain += float(t["lufs"]) - m
        except (SystemExit, ValueError):
            pass
    return out, gain


def track_filter(i: int, t: dict, total: float, gain: float, length: float) -> str:
    """Chaine de filtres d'une piste pre-rendue ; sortie [a<i>]."""
    start = float(t.get("start", 0.0))
    chain = []
    if gain:
        chain.append(f"volume={gain:.2f}dB")
    fi, fo = float(t.get("fade_in", 0.0)), float(t.get("fade_out", 0.0))
    if fi:
        chain.append(f"afade=t=in:st=0:d={fi}")
    if fo:
        chain.append(f"afade=t=out:st={max(length - fo, 0):.3f}:d={fo}")
    ms = int(round(start * 1000))
    chain.append(f"adelay={ms}|{ms}")
    return f"[{i}:a]" + ",".join(chain) + f"[a{i}]"


def build_command(spec: dict, root: Path, out_wav: Path, tmpdir: Path) -> list[str]:
    total = total_duration(spec, root)
    tracks = spec["tracks"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    parts = []
    for i, t in enumerate(tracks):
        wav, gain = prep_track(i, t, root, tmpdir, total)
        start = float(t.get("start", 0.0))
        length = min(float(t["dur"]) if t.get("dur") else total - start, total - start)
        cmd += ["-i", str(wav)]
        parts.append(track_filter(i, t, total, gain, length))
    labels = "".join(f"[a{i}]" for i in range(len(tracks)))
    mix = f"{labels}amix=inputs={len(tracks)}:normalize=0:duration=longest,apad,atrim=duration={total:.3f}[out]"
    cmd += ["-filter_complex", ";".join(parts + [mix]), "-map", "[out]", "-ar", "48000", "-t", f"{total:.3f}", str(out_wav)]
    return cmd


def measure_lufs(path: Path) -> float:
    """Loudness integree (EBU R128) mesuree sur le fichier entier."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    last = [ln for ln in r.stderr.splitlines() if ln.strip().startswith("I:")]
    if not last:
        raise SystemExit("mesure LUFS impossible")
    return float(last[-1].split()[1])


def apply_static_gain(wav: Path, target_lufs: float) -> float:
    """Gain constant (pas de compression dynamique) pour atteindre target_lufs ; limiteur de crete."""
    gain = target_lufs - measure_lufs(wav)
    tmp = wav.with_name(wav.stem + "_tmp.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af",
                    f"volume={gain:.2f}dB,alimiter=limit=0.79:level=disabled", str(tmp)], check=True)
    tmp.replace(wav)
    return gain


def plan(spec: dict, root: Path) -> str:
    total = total_duration(spec, root)
    lines = [f"duree {total:.1f}s, {len(spec['tracks'])} pistes"]
    for t in sorted(spec["tracks"], key=lambda x: float(x.get("start", 0))):
        s = float(t.get("start", 0))
        d = float(t["dur"]) if t.get("dur") else total - s
        lines.append(f"{s:7.1f} -> {min(s + d, total):7.1f}  {t.get('label', ''):28s} {Path(t['file']).name}")
    return "\n".join(lines)


def render(mix_path: Path) -> list[Path]:
    spec, root = load(mix_path)
    out_dir = root / "12_EDITING" / "AUDIO"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_wav = versioned(out_dir / f"{spec['output']}.wav")
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(build_command(spec, root, out_wav, Path(td)), check=True)
    if spec.get("target_lufs") is not None:
        apply_static_gain(out_wav, float(spec["target_lufs"]))
    outs = [out_wav]
    if spec.get("video"):
        out_mp4 = out_wav.with_suffix(".mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(root / spec["video"]), "-i", str(out_wav),
             "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out_mp4)],
            check=True,
        )
        outs.append(out_mp4)
    return outs


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in ("plan", "render"):
        print(__doc__)
        return 2
    mix_path = Path(argv[2])
    if argv[1] == "plan":
        spec, root = load(mix_path)
        print(plan(spec, root))
    else:
        for p in render(mix_path):
            print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
