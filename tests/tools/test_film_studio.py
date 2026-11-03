"""Tests for scripts/film_studio.py — scaffolding, log, QC and export (local ffmpeg only)."""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("film_studio", REPO_ROOT / "scripts" / "film_studio.py")
fs = importlib.util.module_from_spec(_spec)
sys.modules["film_studio"] = fs  # dataclasses resolve their module via sys.modules
_spec.loader.exec_module(fs)

needs_ffmpeg = pytest.mark.skipif(not (shutil.which("ffmpeg") and shutil.which("ffprobe")),
                                  reason="ffmpeg/ffprobe not installed")


def _make_clip(path: Path, *, size="1280x720", rate=24, duration=4, freeze=False, volume=0.3) -> Path:
    src = f"color=c=gray:size={size}:rate={rate}:duration={duration}" if freeze \
        else f"testsrc2=size={size}:rate={rate}:duration={duration}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", src,
                    "-f", "lavfi", "-i", f"sine=frequency=440:duration={duration}:sample_rate=48000",
                    "-af", f"volume={volume}", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-shortest", str(path)], check=True)
    return path


def test_init_creates_bible_and_canonical_layout(tmp_path):
    project = fs.init_film_project("my-film", "Mon Film", projects_dir=tmp_path)
    for folder, docs in fs.BIBLE_LAYOUT.items():
        for doc in docs:
            text = (project / folder / doc).read_text(encoding="utf-8")
            assert "Mon Film" in text and "{title}" not in text
    for canonical in ("artifacts", "assets/video", "renders", "project.json"):
        assert (project / canonical).exists()
    assert (project / "06_assets").resolve() == (project / "assets").resolve()
    assert "init" in (project / "production_log.md").read_text(encoding="utf-8")


def test_init_never_overwrites_existing_docs(tmp_path):
    project = fs.init_film_project("my-film", "Mon Film", projects_dir=tmp_path)
    concept = project / "01_concept" / "01_CONCEPT.md"
    concept.write_text("edited by the director", encoding="utf-8")
    fs.init_film_project("my-film", "Mon Film", projects_dir=tmp_path)
    assert concept.read_text(encoding="utf-8") == "edited by the director"


def test_log_escapes_table_breaking_chars(tmp_path):
    fs.init_film_project("my-film", "Mon Film", projects_dir=tmp_path)
    fs.append_log("my-film", "a | b\nc", kind="retry", projects_dir=tmp_path)
    last = (tmp_path / "my-film" / "production_log.md").read_text(encoding="utf-8").splitlines()[-1]
    assert "| retry | a \\| b c |" in last


def test_rejects_non_kebab_project_id(tmp_path):
    with pytest.raises(SystemExit):
        fs.init_film_project("../escape", "x", projects_dir=tmp_path)


@needs_ffmpeg
def test_qc_flags_wrong_resolution_as_critical(tmp_path):
    clip = _make_clip(tmp_path / "c.mp4")
    report = fs.run_qc(clip, fs.PRESETS["youtube"])
    assert report["verdict"] == "FAIL"
    assert any(f["check"] == "resolution" for f in report["findings"])


@needs_ffmpeg
def test_qc_detects_frozen_picture(tmp_path):
    clip = _make_clip(tmp_path / "frozen.mp4", duration=5, freeze=True)
    report = fs.run_qc(clip)
    assert any(f["check"] == "frozen_video" for f in report["findings"])


@needs_ffmpeg
def test_export_refuses_silent_aspect_change(tmp_path):
    fs.init_film_project("my-film", "Mon Film", projects_dir=tmp_path)
    clip = _make_clip(tmp_path / "c.mp4")
    with pytest.raises(SystemExit, match="aspect ratio mismatch"):
        fs.export_film("my-film", clip, "vertical", projects_dir=tmp_path)


@needs_ffmpeg
def test_export_then_qc_passes_delivery_spec(tmp_path):
    fs.init_film_project("my-film", "Mon Film", projects_dir=tmp_path)
    clip = _make_clip(tmp_path / "c.mp4")  # 1280x720 → upscaled to 1920x1080, same 16:9 ratio
    srt = tmp_path / "subs.srt"
    srt.write_text("1\n00:00:00,000 --> 00:00:01,000\nBonjour\n", encoding="utf-8")
    outputs = fs.export_film("my-film", clip, "youtube", srt=srt, projects_dir=tmp_path)
    assert outputs["subtitles"].name == "final_film_subtitles.srt"
    report = fs.run_qc(outputs["final"], fs.PRESETS["youtube"])
    assert report["verdict"] == "PASS", report["findings"]
    assert abs(report["technical"]["integrated_lufs"] - (-14.0)) <= fs.LOUDNESS_TOLERANCE_LU
