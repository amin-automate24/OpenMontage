#!/usr/bin/env python3
"""film_edit — render a cut from an edit decision list (EDL), never overwriting.

EDL (JSON): {"output": "S2_rough_cut_v2.mp4", "fade_in": 0.5, "fade_out": 1.0,
             "clips": [{"file": "path.mp4", "in": 0, "out": 7.0, "label": "S2-01"},
                       {"file": "...", "in": 0, "out": 5.5, "transition": "dissolve", "dur": 0.8, "label": "S2-02"}]}
`transition` describes the join with the PREVIOUS clip: "cut" (default) or "dissolve" (+ "dur").
Sources are read-only. Output gets a numbered suffix if it already exists.
Usage: film_edit.py plan EDL.json   (timecodes, no render)
       film_edit.py render EDL.json (render + junction contact sheet frames list)
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path


def versioned(p: Path) -> Path:
    if not p.exists():
        return p
    n = 2
    while p.with_name(f"{p.stem}_v{n}{p.suffix}").exists():
        n += 1
    return p.with_name(f"{p.stem}_v{n}{p.suffix}")


def build_filter(edl: dict):
    clips = edl["clips"]
    norm, durs = [], []
    for i, c in enumerate(clips):
        d = float(c["out"]) - float(c["in"])
        durs.append(d)
        norm.append(f"[{i}:v]trim={c['in']}:{c['out']},setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,fps=24,settb=AVTB[n{i}]")
    groups, cur = [], []
    for i, c in enumerate(clips):
        if i > 0 and c.get("transition", "cut") == "dissolve":
            groups.append(cur); cur = []
        cur.append(i)
    groups.append(cur)
    parts, glen, glabel, gdis = list(norm), [], [], []
    for k, g in enumerate(groups):
        ins = "".join(f"[n{i}]" for i in g)
        if len(g) == 1:
            parts.append(f"{ins}null[g{k}]")
        else:
            parts.append(f"{ins}concat=n={len(g)}:v=1:a=0[g{k}]")
        glen.append(sum(durs[i] for i in g)); glabel.append(f"g{k}")
        gdis.append(float(clips[g[0]].get("dur", 0.6)) if k > 0 else 0)
    label, total = glabel[0], glen[0]
    for k in range(1, len(groups)):
        d = gdis[k]
        parts.append(f"[{label}][{glabel[k]}]xfade=transition=fade:duration={d}:offset={total - d:.3f}[x{k}]")
        label, total = f"x{k}", total + glen[k] - d
    fi, fo = float(edl.get("fade_in", 0.5)), float(edl.get("fade_out", 0.5))
    parts.append(f"[{label}]fade=t=in:st=0:d={fi},fade=t=out:st={total - fo:.3f}:d={fo}[v]")
    return ";".join(parts), total


def timeline(edl: dict):
    """Start/end timecodes of each clip in the final cut."""
    out, t = [], 0.0
    for i, c in enumerate(edl["clips"]):
        d = float(c["out"]) - float(c["in"])
        if i > 0 and c.get("transition", "cut") == "dissolve":
            t -= float(c.get("dur", 0.6))
        out.append((c.get("label", f"clip{i}"), round(t, 2), round(t + d, 2)))
        t += d
    return out


def render(edl_path: Path, root: Path):
    edl = json.loads(edl_path.read_text())
    fc, total = build_filter(edl)
    out = versioned(root / "12_EDITING" / edl["output"])
    cmd = ["ffmpeg", "-v", "error", "-n"]
    for c in edl["clips"]:
        src = root / c["file"]
        if not src.exists():
            raise SystemExit(f"missing source: {src}")
        cmd += ["-i", str(src)]
    cmd += ["-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    return out, total


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("plan", "render"):
        raise SystemExit(__doc__)
    edl = json.loads(Path(sys.argv[2]).read_text())
    for lab, a, b in timeline(edl):
        print(f"{lab:8s} {a:7.2f} -> {b:7.2f}")
    print("total", round(build_filter(edl)[1], 2))
    if sys.argv[1] == "render":
        root = Path(sys.argv[2]).resolve().parents[1]
        print(render(Path(sys.argv[2]), root))
