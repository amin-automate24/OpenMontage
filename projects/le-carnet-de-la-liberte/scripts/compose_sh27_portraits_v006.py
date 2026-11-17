#!/usr/bin/env python3
"""SH27 v006 — QC correction: right portrait card moved 50 px left (2610 -> 2560) so it no longer hides the small flag
(v005 at 2500 hid half of it, rejected); combined with a +80 px horizontal camera centre for SH27 in build_animatic_v2.py,
the card stays fully inside the frame for the whole pull_out. Same archived photo (hash-checked), same size/rotation/height,
left card unchanged. Geometric placement only, no AI. v003 (LOCKED), v004, v005 untouched."""
import compose_sh27_sh28_portraits as C
C.run(C.POST/"SH27_flags_v002.png", C.POST/"SH27_flags_portraits_v006.png",
      [(215, -3, 1050, 872, (1072, 878)), (215, 3, 2560, 742, (2582, 752))])
