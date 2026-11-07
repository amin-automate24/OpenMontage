"""Film Studio — film-bible scaffolding, production log, technical QC and final export.

A thin persistence/QC layer for narrative short films produced through the
``cinematic`` pipeline. It does NOT orchestrate generation or make creative
decisions — the agent does that by following the pipeline's director skills
(see ``skills/meta/film-studio.md``). This script only:

  init    create projects/<id>/ (canonical OpenMontage layout via
          lib.checkpoint.init_project) plus the film-bible folders and the
          01_CONCEPT … 11_QC_REPORT templates and production_log.md
  log     append a timestamped entry to production_log.md
  qc      run a technical QC pass (ffprobe + EBU R128 loudness + black / freeze /
          silence detection) and write 09_quality_control/11_QC_REPORT_auto.md
          and .json — exits 1 when a critical issue is found
  export  encode the delivery files into 10_output/ (H.264/AAC MP4 + optional
          ProRes 422 HQ master + subtitles), refusing to change the aspect ratio
          unless an explicit --fit mode is given

Usage:
    python scripts/film_studio.py init le-veilleur --title "Le Veilleur"
    python scripts/film_studio.py log le-veilleur "SC01_SH002 regenerated: face drift" --kind retry
    python scripts/film_studio.py qc le-veilleur projects/le-veilleur/renders/final.mp4 --preset youtube
    python scripts/film_studio.py export le-veilleur projects/le-veilleur/renders/final.mp4 --preset youtube --master
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

TEMPLATES_DIR = REPO_ROOT / "docs" / "film-studio" / "templates"
DEFAULT_PROJECTS_DIR = REPO_ROOT / "projects"

# Film-bible folders (the brief's /film_project/ structure), created next to the
# canonical OpenMontage layout (artifacts/, assets/, renders/) so the Backlot
# board keeps working. 06_assets is a symlink to assets/ — one source of truth.
BIBLE_LAYOUT: dict[str, list[str]] = {
    "01_concept": ["01_CONCEPT.md"],
    "02_screenplay": ["02_SCREENPLAY.md"],
    "03_visual_bible": ["03_VISUAL_BIBLE.md", "04_CHARACTER_BIBLE.md"],
    "04_storyboard": ["05_STORYBOARD.md"],
    "05_prompts": ["06_VIDEO_PROMPTS.md", "08_MUSIC_PROMPTS.md"],
    "07_editing": ["07_SOUND_DESIGN.md", "09_EDITING_PLAN.md"],
    "08_subtitles": [],
    "09_quality_control": ["11_QC_REPORT.md"],
    "10_output": [],
}
EXTRA_DIRS = [
    "07_editing/10_TIMELINE",
    "assets/images/characters",
    "assets/images/storyboard",
    "assets/video",
    "assets/audio/sfx",
    "assets/audio/ambience",
    "assets/audio/dialogue",
]


@dataclass(frozen=True)
class DeliveryPreset:
    width: int
    height: int
    fps: Fraction
    loudness_lufs: float
    label: str


PRESETS: dict[str, DeliveryPreset] = {
    "youtube": DeliveryPreset(1920, 1080, Fraction(24), -14.0, "1920x1080 16:9 @24 — web/YouTube"),
    "cinema-scope": DeliveryPreset(1920, 804, Fraction(24), -14.0, "1920x804 2.39:1 @24"),
    "4k": DeliveryPreset(3840, 2160, Fraction(24), -14.0, "3840x2160 16:9 @24"),
    "vertical": DeliveryPreset(1080, 1920, Fraction(30), -14.0, "1080x1920 9:16 @30 — TikTok/Reels/Shorts"),
    "square": DeliveryPreset(1080, 1080, Fraction(30), -14.0, "1080x1080 1:1 @30 — Instagram feed"),
    "broadcast": DeliveryPreset(1920, 1080, Fraction(25), -23.0, "1920x1080 @25 — EBU R128 broadcast"),
}

TRUE_PEAK_MAX_DBTP = -1.0
LOUDNESS_TOLERANCE_LU = 2.0
AV_DRIFT_MAX_S = 0.10
BLACK_MIN_S = 0.5
FREEZE_MIN_S = 2.0
SILENCE_MIN_S = 3.0


# ---------------------------------------------------------------- helpers --

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _project_dir(project_id: str, projects_dir: Path) -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", project_id):
        raise SystemExit(f"project id must be kebab-case (got {project_id!r})")
    return projects_dir / project_id


def _require(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise SystemExit(f"{binary} not found on PATH")
    return path


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


# ------------------------------------------------------------------- init --

def init_film_project(project_id: str, title: str, projects_dir: Path = DEFAULT_PROJECTS_DIR,
                      style_playbook: Optional[str] = None) -> Path:
    from lib.checkpoint import init_project

    project = init_project(project_id, title=title, pipeline_type="cinematic",
                           pipeline_dir=projects_dir, style_playbook=style_playbook)
    for folder, docs in BIBLE_LAYOUT.items():
        (project / folder).mkdir(parents=True, exist_ok=True)
        for doc in docs:
            target = project / folder / doc
            if target.exists():
                continue  # never overwrite work in progress
            text = (TEMPLATES_DIR / doc).read_text(encoding="utf-8")
            target.write_text(text.replace("{title}", title), encoding="utf-8")
    for extra in EXTRA_DIRS:
        (project / extra).mkdir(parents=True, exist_ok=True)

    link = project / "06_assets"
    if not link.exists() and not link.is_symlink():
        try:
            link.symlink_to("assets", target_is_directory=True)
        except OSError:  # e.g. Windows without symlink privilege
            link.mkdir()
            (link / "README.md").write_text("Assets live in ../assets/ (canonical OpenMontage path).\n")

    log = project / "production_log.md"
    if not log.exists():
        log.write_text(
            f"# Production log — {title}\n\n"
            "Append-only. Operations, files, errors, retries, tools, decisions, remaining steps.\n\n"
            "| Date (UTC) | Kind | Entry |\n|---|---|---|\n",
            encoding="utf-8",
        )
        append_log(project_id, f"Project initialised (pipeline: cinematic)", kind="init",
                   projects_dir=projects_dir)
    return project


# -------------------------------------------------------------------- log --

LOG_KINDS = {"init", "op", "file", "error", "retry", "tool", "decision", "todo", "qc", "export"}


def append_log(project_id: str, entry: str, kind: str = "op",
               projects_dir: Path = DEFAULT_PROJECTS_DIR) -> None:
    if kind not in LOG_KINDS:
        raise SystemExit(f"kind must be one of {sorted(LOG_KINDS)}")
    log = _project_dir(project_id, projects_dir) / "production_log.md"
    if not log.exists():
        raise SystemExit(f"{log} not found — run `init` first")
    safe = entry.replace("|", "\\|").replace("\n", " ")
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"| {_now()} | {kind} | {safe} |\n")


# --------------------------------------------------------------------- qc --

def probe(path: Path) -> dict[str, Any]:
    res = _run([_require("ffprobe"), "-v", "error", "-print_format", "json",
                "-show_format", "-show_streams", str(path)])
    if res.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {res.stderr.strip()}")
    return json.loads(res.stdout)


def _ffmpeg_filter_log(path: Path, args: list[str]) -> str:
    res = _run([_require("ffmpeg"), "-hide_banner", "-nostats", "-i", str(path), *args, "-f", "null", "-"])
    return res.stderr


def measure_loudness(path: Path) -> dict[str, Optional[float]]:
    log = _ffmpeg_filter_log(path, ["-vn", "-af", "ebur128=peak=true", "-map", "0:a:0"])
    summary = log[log.rfind("Summary:"):] if "Summary:" in log else ""

    def grab(label: str) -> Optional[float]:
        m = re.search(label + r":\s+(-?[\d.]+|-inf)", summary)
        if not m or m.group(1) == "-inf":
            return None
        return float(m.group(1))

    return {"integrated_lufs": grab("I"), "lra_lu": grab("LRA"), "true_peak_dbtp": grab("Peak")}


def _intervals(log: str, start_key: str, end_key: str, duration: float) -> list[tuple[float, float]]:
    starts = [float(x) for x in re.findall(start_key + r"[:=]\s*(-?[\d.]+)", log)]
    ends = [float(x) for x in re.findall(end_key + r"[:=]\s*(-?[\d.]+)", log)]
    # An event still running at EOF (e.g. a freeze to the last frame) has no end marker.
    ends += [duration] * (len(starts) - len(ends))
    return list(zip(starts, ends))


def detect_events(path: Path, has_audio: bool, duration: float) -> dict[str, list[tuple[float, float]]]:
    vlog = _ffmpeg_filter_log(path, ["-an", "-vf",
                                     f"blackdetect=d={BLACK_MIN_S}:pix_th=0.10,"
                                     f"freezedetect=n=0.001:d={FREEZE_MIN_S}"])
    events = {
        "black": _intervals(vlog, "black_start", "black_end", duration),
        "freeze": _intervals(vlog, r"lavfi\.freezedetect\.freeze_start", r"lavfi\.freezedetect\.freeze_end", duration),
        "silence": [],
    }
    if has_audio:
        alog = _ffmpeg_filter_log(path, ["-vn", "-af", f"silencedetect=n=-50dB:d={SILENCE_MIN_S}"])
        events["silence"] = _intervals(alog, "silence_start", "silence_end", duration)
    return events


def run_qc(path: Path, preset: Optional[DeliveryPreset] = None) -> dict[str, Any]:
    info = probe(path)
    streams = info.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    duration = float(info.get("format", {}).get("duration", 0) or 0)
    findings: list[dict[str, str]] = []

    def add(severity: str, check: str, message: str) -> None:
        findings.append({"severity": severity, "check": check, "message": message})

    tech: dict[str, Any] = {"file": str(path), "duration_s": round(duration, 3),
                            "size_mb": round(int(info.get("format", {}).get("size", 0)) / 1e6, 2),
                            "container": info.get("format", {}).get("format_name")}
    if v is None:
        add("critical", "video_stream", "no video stream")
    else:
        fps = Fraction(v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1")
        tech.update({"width": v.get("width"), "height": v.get("height"),
                     "fps": round(float(fps), 3) if fps else None, "video_codec": v.get("codec_name"),
                     "pix_fmt": v.get("pix_fmt"), "video_duration_s": float(v.get("duration", duration) or duration)})
        if preset:
            if (v.get("width"), v.get("height")) != (preset.width, preset.height):
                add("critical", "resolution", f"{v.get('width')}x{v.get('height')} ≠ preset {preset.width}x{preset.height}")
            if fps and abs(float(fps) - float(preset.fps)) > 0.01:
                add("critical", "frame_rate", f"{float(fps):.3f} fps ≠ preset {float(preset.fps):g}")
        if v.get("pix_fmt") not in (None, "yuv420p") and v.get("codec_name") == "h264":
            add("warning", "pix_fmt", f"{v.get('pix_fmt')} — yuv420p is the safe delivery format")
    if a is None:
        add("warning", "audio_stream", "no audio stream — intentional silent film?")
    else:
        tech.update({"audio_codec": a.get("codec_name"), "sample_rate": a.get("sample_rate"),
                     "channels": a.get("channels"), "audio_duration_s": float(a.get("duration", duration) or duration)})
        if v is not None:
            drift = abs(tech["audio_duration_s"] - tech["video_duration_s"])
            tech["av_duration_drift_s"] = round(drift, 3)
            if drift > AV_DRIFT_MAX_S:
                add("critical", "av_sync", f"audio/video durations differ by {drift:.2f}s (> {AV_DRIFT_MAX_S}s)")
        loud = measure_loudness(path)
        tech.update(loud)
        target = preset.loudness_lufs if preset else -14.0
        if loud["integrated_lufs"] is None:
            add("critical", "loudness", "audio is silent (integrated loudness -inf)")
        elif abs(loud["integrated_lufs"] - target) > LOUDNESS_TOLERANCE_LU:
            add("warning", "loudness", f"{loud['integrated_lufs']} LUFS, target {target} ±{LOUDNESS_TOLERANCE_LU}")
        if loud["true_peak_dbtp"] is not None and loud["true_peak_dbtp"] > TRUE_PEAK_MAX_DBTP:
            add("critical", "true_peak", f"{loud['true_peak_dbtp']} dBTP > {TRUE_PEAK_MAX_DBTP} (clipping risk)")

    events = detect_events(path, a is not None, duration) if v is not None else {"black": [], "freeze": [], "silence": []}
    for s, e in events["black"]:
        edge = s < 1.0 or e > duration - 1.0  # fade in / fade out are expected
        add("info" if edge else "warning", "black_frames", f"black {s:.2f}s → {e:.2f}s")
    for s, e in events["freeze"]:
        add("warning", "frozen_video", f"frozen picture {s:.2f}s → {e:.2f}s (check it is an intended hold)")
    for s, e in events["silence"]:
        add("info", "silence", f"silence {s:.2f}s → {e:.2f}s (intended narrative silence?)")

    critical = [f for f in findings if f["severity"] == "critical"]
    return {"generated_at": _now(), "preset": preset.label if preset else None, "technical": tech,
            "events": events, "findings": findings, "verdict": "FAIL" if critical else "PASS"}


def write_qc_report(project_id: str, report: dict[str, Any],
                    projects_dir: Path = DEFAULT_PROJECTS_DIR) -> Path:
    qc_dir = _project_dir(project_id, projects_dir) / "09_quality_control"
    qc_dir.mkdir(parents=True, exist_ok=True)
    (qc_dir / "11_QC_REPORT_auto.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    t = report["technical"]
    lines = [f"# QC technique automatique — {report['verdict']}", "",
             f"Généré le {report['generated_at']} · preset : {report['preset'] or '—'}", "",
             "| Mesure | Valeur |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in t.items()]
    lines += ["", "## Constats", ""]
    if report["findings"]:
        lines += ["| Sévérité | Contrôle | Détail |", "|---|---|---|"]
        lines += [f"| {f['severity']} | {f['check']} | {f['message']} |" for f in report["findings"]]
    else:
        lines.append("Aucun constat.")
    lines += ["", "_Le contrôle visuel plan par plan (visages, continuité, artefacts) reste à faire "
              "dans 11_QC_REPORT.md — ce rapport ne le remplace pas._", ""]
    out = qc_dir / "11_QC_REPORT_auto.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ----------------------------------------------------------------- export --

def _video_filter(src_w: int, src_h: int, preset: DeliveryPreset, fit: Optional[str]) -> str:
    src_ar = Fraction(src_w, src_h)
    dst_ar = Fraction(preset.width, preset.height)
    if abs(float(src_ar) - float(dst_ar)) > 0.01:
        if fit is None:
            raise SystemExit(
                f"aspect ratio mismatch: source {src_w}x{src_h} ({float(src_ar):.3f}) vs preset "
                f"{preset.width}x{preset.height} ({float(dst_ar):.3f}). Check the framing, then pass "
                "--fit pad (letterbox/pillarbox, nothing cut) or --fit crop (centre crop, loses image).")
        if fit == "pad":
            return (f"scale={preset.width}:{preset.height}:force_original_aspect_ratio=decrease:flags=lanczos,"
                    f"pad={preset.width}:{preset.height}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1")
        return (f"scale={preset.width}:{preset.height}:force_original_aspect_ratio=increase:flags=lanczos,"
                f"crop={preset.width}:{preset.height},setsar=1")
    return f"scale={preset.width}:{preset.height}:flags=lanczos,setsar=1"


def _loudnorm_filter(path: Path, target: float) -> str:
    """Two-pass EBU R128 normalisation: measure, then apply linear gain."""
    base = f"loudnorm=I={target}:TP={TRUE_PEAK_MAX_DBTP - 0.5}:LRA=11"
    log = _ffmpeg_filter_log(path, ["-vn", "-af", base + ":print_format=json"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", log, re.S)
    if not m:
        return base
    meas = json.loads(m.group(0))
    return (f"{base}:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
            f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:"
            f"offset={meas['target_offset']}:linear=true")


def export_film(project_id: str, source: Path, preset_name: str = "youtube", *, master: bool = False,
                fit: Optional[str] = None, srt: Optional[Path] = None, normalize: bool = True,
                crf: int = 18, projects_dir: Path = DEFAULT_PROJECTS_DIR) -> dict[str, Path]:
    preset = PRESETS[preset_name]
    info = probe(source)
    v = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    if v is None:
        raise SystemExit("source has no video stream")
    has_audio = any(s.get("codec_type") == "audio" for s in info["streams"])
    vf = _video_filter(int(v["width"]), int(v["height"]), preset, fit)
    af = _loudnorm_filter(source, preset.loudness_lufs) if (has_audio and normalize) else None

    out_dir = _project_dir(project_id, projects_dir) / "10_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, Path] = {}
    ffmpeg = _require("ffmpeg")
    fps = f"{preset.fps.numerator}/{preset.fps.denominator}"

    def encode(dest: Path, vcodec: list[str], acodec: list[str], extra: list[str]) -> None:
        cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(source),
               "-map", "0:v:0", "-vf", f"{vf},fps={fps}", *vcodec]
        if has_audio:
            # -shortest: AAC priming + loudnorm resampling can leave an audio tail
            # longer than the picture, which QC would flag as A/V drift.
            cmd += ["-map", "0:a:0", *(["-af", af] if af else []), *acodec, "-ar", "48000", "-shortest"]
        cmd += [*extra, str(dest)]
        res = _run(cmd)
        if res.returncode != 0:
            raise RuntimeError(f"ffmpeg export failed for {dest.name}: {res.stderr.strip()[-800:]}")

    final = out_dir / "final_film.mp4"
    encode(final, ["-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p",
                   "-profile:v", "high", "-color_primaries", "bt709", "-color_trc", "bt709",
                   "-colorspace", "bt709"],
           ["-c:a", "aac", "-b:a", "320k"], ["-movflags", "+faststart"])
    outputs["final"] = final

    if master:
        # ProRes is the professional mezzanine codec; it belongs in a QuickTime
        # container (.mov), not MP4 — hence final_film_master.mov.
        m = out_dir / "final_film_master.mov"
        encode(m, ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le",
                   "-vendor", "apl0"], ["-c:a", "pcm_s24le"], [])
        outputs["master"] = m

    if srt:
        dest = out_dir / "final_film_subtitles.srt"
        shutil.copyfile(srt, dest)
        outputs["subtitles"] = dest
    return outputs


# -------------------------------------------------------------------- cli --

def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--projects-dir", type=Path, default=DEFAULT_PROJECTS_DIR)
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init", help="scaffold a film project")
    pi.add_argument("project_id")
    pi.add_argument("--title", required=True)
    pi.add_argument("--style-playbook")

    pl = sub.add_parser("log", help="append to production_log.md")
    pl.add_argument("project_id")
    pl.add_argument("entry")
    pl.add_argument("--kind", default="op", choices=sorted(LOG_KINDS))

    pq = sub.add_parser("qc", help="technical QC of a render")
    pq.add_argument("project_id")
    pq.add_argument("video", type=Path)
    pq.add_argument("--preset", choices=sorted(PRESETS))

    pe = sub.add_parser("export", help="encode delivery files into 10_output/")
    pe.add_argument("project_id")
    pe.add_argument("video", type=Path)
    pe.add_argument("--preset", default="youtube", choices=sorted(PRESETS))
    pe.add_argument("--master", action="store_true", help="also write a ProRes 422 HQ master (.mov)")
    pe.add_argument("--fit", choices=["pad", "crop"], help="required only when the aspect ratio changes")
    pe.add_argument("--srt", type=Path)
    pe.add_argument("--no-normalize", action="store_true", help="skip two-pass loudness normalisation")
    pe.add_argument("--crf", type=int, default=18)

    args = p.parse_args(argv)
    pdir: Path = args.projects_dir

    if args.cmd == "init":
        project = init_film_project(args.project_id, args.title, pdir, args.style_playbook)
        print(f"initialised {project}")
        return 0
    if args.cmd == "log":
        append_log(args.project_id, args.entry, args.kind, pdir)
        return 0
    if args.cmd == "qc":
        report = run_qc(args.video, PRESETS[args.preset] if args.preset else None)
        out = write_qc_report(args.project_id, report, pdir)
        append_log(args.project_id, f"QC {report['verdict']} on {args.video.name} → {out.name}", "qc", pdir)
        print(out.read_text(encoding="utf-8"))
        return 0 if report["verdict"] == "PASS" else 1
    if args.cmd == "export":
        outputs = export_film(args.project_id, args.video, args.preset, master=args.master, fit=args.fit,
                              srt=args.srt, normalize=not args.no_normalize, crf=args.crf, projects_dir=pdir)
        for kind, path in outputs.items():
            append_log(args.project_id, f"export {kind}: {path.name}", "export", pdir)
            print(f"{kind}: {path}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
