#!/usr/bin/env python3
"""SH27 v005 — QC correction only: right portrait card moved 110 px left (2610 -> 2500) so it stays inside the
SH27 camera frame (pull_out 1.08 -> 1.0 crops x > 2650 at shot start). Same archived photo (hash-checked in module C),
same size/rotation/height, left card unchanged. Geometric placement only, no AI. v003 (LOCKED) and v004 untouched."""
import compose_sh27_sh28_portraits as C
C.run(C.POST/"SH27_flags_v002.png", C.POST/"SH27_flags_portraits_v005.png",
      [(215, -3, 1050, 872, (1072, 878)), (215, 3, 2500, 742, (2522, 752))])
