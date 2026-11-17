import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("film_edit", Path(__file__).resolve().parents[2] / "scripts" / "film_edit.py")
fe = importlib.util.module_from_spec(spec); sys.modules["film_edit"] = fe; spec.loader.exec_module(fe)

EDL = {"output": "x.mp4", "fade_in": 0.5, "fade_out": 1.0, "clips": [
    {"file": "a.mp4", "in": 0, "out": 6, "label": "A"},
    {"file": "b.mp4", "in": 0, "out": 5, "transition": "dissolve", "dur": 1.0, "label": "B"},
    {"file": "c.mp4", "in": 1, "out": 4, "label": "C"}]}


def test_total_and_timeline():
    fc, total = fe.build_filter(EDL)
    assert abs(total - 13.0) < 1e-6          # 6 + 5 + 3 - 1 dissolve
    assert fe.timeline(EDL) == [("A", 0.0, 6.0), ("B", 5.0, 10.0), ("C", 10.0, 13.0)]
    assert "xfade" in fc and "concat=n=2" in fc


def test_versioned(tmp_path):
    p = tmp_path / "o.mp4"; p.write_text("x")
    assert fe.versioned(p).name == "o_v2.mp4"
