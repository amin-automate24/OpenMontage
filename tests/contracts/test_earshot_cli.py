"""``earshot`` wrapper contract: it only builds Earshot CLI calls.

The wrapper must not re-implement Earshot. These tests fake the subprocess and
check the exact argv for each operation, that JSON stdout is passed through,
that Earshot's one-line stderr error is surfaced, and that the bank search
filter narrows `sfx list` output. No Earshot install or models are needed.
"""

from __future__ import annotations

import json
import subprocess

import pytest

from tools.audio import earshot_cli
from tools.audio.earshot_cli import Earshot

BANK = {
    "version": "test",
    "sounds": [
        {"id": "cut_hit/sub", "category": "cut_hit", "kinds": ["hit"], "notes": "short sub hit"},
        {"id": "whoosh_fast/crisp", "category": "whoosh_fast", "kinds": ["whoosh"], "notes": "fast air"},
    ],
}


@pytest.fixture
def fake_cli(monkeypatch):
    calls = []

    def run(argv, **kwargs):
        calls.append(argv)
        if argv[1:3] == ["sfx", "list"]:
            out = BANK
        elif argv[1] == "critique" and argv[2] == "bad.wav":
            return subprocess.CompletedProcess(argv, 1, "", "earshot critique: error: cannot read bad.wav\n")
        else:
            out = {"summary": "ok"}
        return subprocess.CompletedProcess(argv, 0, json.dumps(out), "")

    monkeypatch.setattr(earshot_cli.shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(earshot_cli.subprocess, "run", run)
    return calls


def test_render_argv(fake_cli, tmp_path):
    out = tmp_path / "sfx" / "w.wav"
    res = Earshot().execute({
        "operation": "sfx_render", "sound_id": "whoosh_fast/crisp", "output_path": str(out),
        "dur": 0.8, "apex": 0.32, "pitch": "E5",
    })
    assert res.success, res.error
    assert fake_cli[-1][1:] == [
        "sfx", "render", "whoosh_fast/crisp", "-o", str(out), "--json",
        "--dur", "0.8", "--apex", "0.32", "--pitch", "E5",
    ]
    assert res.artifacts == [str(out)]


def test_critique_argv(fake_cli, tmp_path):
    mix, film = tmp_path / "mix.wav", tmp_path / "film.mp4"
    mix.write_bytes(b"x")
    res = Earshot().execute({"operation": "critique", "input_path": str(mix), "video_path": str(film), "fast": True})
    assert res.success, res.error
    assert fake_cli[-1][1:] == ["critique", str(mix), "--json", "--video", str(film), "--fast"]

    missing = Earshot().execute({"operation": "critique", "input_path": str(tmp_path / "nope.wav")})
    assert not missing.success  # rejected before the CLI runs


def test_critique_surfaces_cli_error(fake_cli, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "bad.wav").write_bytes(b"x")
    res = Earshot().execute({"operation": "critique", "input_path": "bad.wav"})
    assert not res.success
    assert "cannot read bad.wav" in res.error


def test_sfx_search_filters_bank(fake_cli):
    res = Earshot().execute({"operation": "sfx_search", "kind": "hit", "query": "SUB"})
    assert res.success, res.error
    assert fake_cli[-1][1:] == ["sfx", "list", "--json", "--kind", "hit"]
    assert [s["id"] for s in res.data["result"]["sounds"]] == ["cut_hit/sub"]


def test_unavailable_without_cli(monkeypatch):
    monkeypatch.setattr("tools.base_tool.shutil.which", lambda name: None)
    assert Earshot().get_status().value != "available"
