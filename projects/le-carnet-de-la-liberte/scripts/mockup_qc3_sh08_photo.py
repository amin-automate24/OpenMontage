#!/usr/bin/env python3
"""MAQUETTE SH08 sur la chaîne QC3 (NON FINAL, non intégrée) : seule l'image source de SH08 est remplacée par
SH08_composite_photo_BnF_Rol156948_v003b_genoux.png (photo d'archive BnF/Agence Rol 156948). Écrit un fichier neuf dans animatic/qc2/."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import mockup_qc2_sh06_sh33 as MQ        # chaîne QC3 (SH06 v2 + SH33 validés)
B = MQ.B
B.IMG[8] = B.P("references/p4/post/SH08_composite_photo_BnF_Rol156948_v003b_genoux.png") if hasattr(B, "P") else Path(__file__).resolve().parent.parent/"references/p4/post/SH08_composite_photo_BnF_Rol156948_v003b_genoux.png"
if __name__ == "__main__": MQ.Q2.main()
