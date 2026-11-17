#!/usr/bin/env python3
"""SH27/SH28 v004 — micro-adjustment of portrait position/size/perspective only (same archived Anefo 905-8914 photograph, geometric transforms only, no face edit).
Goal: fewer crowd faces hidden in SH27 (cards raised above the dense crowd, onto wall/background), slightly larger and clearer card in SH28.
Reads v002 (flags only) and writes v004 ; v003 and all earlier versions untouched. Never overwrites."""
import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import compose_sh27_sh28_portraits as C
POST = C.POST
if __name__ == "__main__":
    C.run(POST/"SH27_flags_v002.png", POST/"SH27_flags_portraits_v004.png", [(215, -3, 1000, 640, (1072, 868)), (215, 3, 2620, 660, (2632, 752))])
    C.run(POST/"SH28_flags_v002.png", POST/"SH28_flags_portraits_v004.png", [(140, 3, 2528, 792, (2490, 800))])
