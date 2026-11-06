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
    "in": 0.0, "loop": true, "lufs": -34, "gain_db": 0,
    "fade_in": 1.0, "fade_out": 1.0, "label": "ambiance"}
 ]
}
Un piste avec "lufs" est d'abord normalisee a ce niveau (loudnorm), puis "gain_db" est ajoute.
Ne modifie, ne supprime, n'ecrase jamais une source ; les sorties vont dans 12_EDITING/AUDIO/ (versionnees).
"""
from __future__ import annotations

import json
import subprocess
import sys
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


def track_filter(i: int, t: dict, total: float) -> str:
    """Construit la chaine de filtres d'une piste ; sortie [a<i>]."""
    start = float(t.get("start", 0.0))
    dur = t.get("dur")
    src_in = float(t.get("in", 0.0))
    chain = []
    if t.get("loop"):
        chain.append("aloop=loop=-1:size=2147483647")
    if src_in:
        chain.append(f"atrim=start={src_in},asetpts=PTS-STARTPTS")
    avail = total - start
    length = float(dur) if dur else avail
    length = min(length, avail)
    chain.append(f"atrim=duration={length:.3f},asetpts=PTS-STARTPTS")
    chain.append("aformat=sample_rates=48000:channel_layouts=stereo")
    if t.get("lufs") is not None:
        chain.append(f"loudnorm=I={float(t['lufs'])}:TP=-1.5:LRA=11")
    gain = float(t.get("gain_db", 0.0))
    if gain:
        chain.append(f"volume={gain}dB")
    fi, fo = float(t.get("fade_in", 0.0)), float(t.get("fade_out", 0.0))
    if fi:
        chain.append(f"afade=t=in:st=0:d={fi}")
    if fo:
        chain.append(f"afade=t=out:st={max(length - fo, 0):.3f}:d={fo}")
    ms = int(round(start * 1000))
    chain.append(f"adelay={ms}|{ms}")
    return f"[{i}:a]" + ",".join(chain) + f"[a{i}]"


def build_command(spec: dict, root: Path, out_wav: Path) -> list[str]:
    total = total_duration(spec, root)
    tracks = spec["tracks"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for t in tracks:
        f = root / t["file"]
        if not f.exists():
            raise SystemExit(f"source introuvable : {f}")
        cmd += ["-i", str(f)]
    parts = [track_filter(i, t, total) for i, t in enumerate(tracks)]
    labels = "".join(f"[a{i}]" for i in range(len(tracks)))
    mix = f"{labels}amix=inputs={len(tracks)}:normalize=0:duration=longest,apad,atrim=duration={total:.3f}"
    if spec.get("target_lufs") is not None:
        mix += f",loudnorm=I={float(spec['target_lufs'])}:TP=-1.5:LRA=11"
    mix += "[out]"
    cmd += ["-filter_complex", ";".join(parts + [mix]), "-map", "[out]", "-ar", "48000", str(out_wav)]
    return cmd


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
    subprocess.run(build_command(spec, root, out_wav), check=True)
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
