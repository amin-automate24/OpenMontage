import importlib.util
import json
import subprocess
import sys
from pathlib import Path

spec_ = importlib.util.spec_from_file_location("film_mix", Path(__file__).resolve().parents[2] / "scripts" / "film_mix.py")
fm = importlib.util.module_from_spec(spec_)
sys.modules["film_mix"] = fm
spec_.loader.exec_module(fm)


def tone(path, freq=440, dur=2):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    f"sine=frequency={freq}:duration={dur}", str(path)], check=True)


def test_versioned(tmp_path):
    f = tmp_path / "a.wav"
    f.write_text("x")
    assert fm.versioned(f).name == "a_v2.wav"


def test_render_never_overwrites_and_duration(tmp_path):
    (tmp_path / "11_AUDIO").mkdir()
    tone(tmp_path / "11_AUDIO" / "a.wav")
    mix = {"project": str(tmp_path), "output": "MIX", "duration": 5,
           "tracks": [{"file": "11_AUDIO/a.wav", "start": 1.0, "label": "a", "fade_in": 0.2, "fade_out": 0.2}]}
    mp = tmp_path / "mix.json"
    mp.write_text(json.dumps(mix))
    out1 = fm.render(mp)[0]
    out2 = fm.render(mp)[0]
    assert out1.name == "MIX.wav" and out2.name == "MIX_v2.wav"
    assert abs(fm.probe_duration(out1) - 5.0) < 0.2


def test_loop_track_fills_duration(tmp_path):
    (tmp_path / "s").mkdir()
    tone(tmp_path / "s" / "l.wav", dur=1)
    mix = {"project": str(tmp_path), "output": "L", "duration": 4,
           "tracks": [{"file": "s/l.wav", "loop": True, "dur": 4}]}
    mp = tmp_path / "m.json"
    mp.write_text(json.dumps(mix))
    assert abs(fm.probe_duration(fm.render(mp)[0]) - 4.0) < 0.2


def test_missing_source_is_reported(tmp_path):
    import pytest
    mix = {"project": str(tmp_path), "output": "X", "duration": 2, "tracks": [{"file": "nope.wav"}]}
    mp = tmp_path / "m.json"
    mp.write_text(json.dumps(mix))
    with pytest.raises(SystemExit):
        fm.render(mp)
