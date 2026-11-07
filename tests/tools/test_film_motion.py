import importlib.util
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location("film_motion", Path(__file__).resolve().parents[2] / "scripts" / "film_motion.py")
fmo = importlib.util.module_from_spec(spec)
sys.modules["film_motion"] = fmo
spec.loader.exec_module(fmo)


def moving_video(path):
    # 1 s fixe, 1 s tres anime (bruit temporel), 2 s fixe
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-f", "lavfi", "-i", "color=c=gray:s=320x180:r=24:d=1",
                    "-f", "lavfi", "-i", "color=c=gray:s=320x180:r=24:d=1,noise=alls=90:allf=t",
                    "-f", "lavfi", "-i", "color=c=gray:s=320x180:r=24:d=2",
                    "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0,format=yuv420p[v]", "-map", "[v]", str(path)], check=True)


def tone(path):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "sine=frequency=300:duration=1", str(path)], check=True)


def test_envelope_follows_motion(tmp_path):
    v = tmp_path / "v.mp4"
    moving_video(v)
    env = fmo.envelope(v, 0, 4)
    t = np.linspace(0, 4, len(env))
    assert env[(t > 1.2) & (t < 1.8)].mean() > 0.5
    assert env[(t > 2.6) & (t < 3.8)].mean() < 0.2


def test_gate_is_silent_when_still_and_refuses_overwrite(tmp_path):
    v, s, o = tmp_path / "v.mp4", tmp_path / "s.wav", tmp_path / "o.wav"
    moving_video(v)
    tone(s)
    fmo.gate(s, v, 0, 4, o)
    with wave.open(str(o)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float)
    sr = fmo.SR
    still = np.abs(x[int(3 * sr): int(3.8 * sr)]).mean()
    moving = np.abs(x[int(1.2 * sr): int(1.8 * sr)]).mean()
    assert moving > 20 * (still + 1)
    import pytest
    with pytest.raises(SystemExit):
        fmo.gate(s, v, 0, 4, o)
