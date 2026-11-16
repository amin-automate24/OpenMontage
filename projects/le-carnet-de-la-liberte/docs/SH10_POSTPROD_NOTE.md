# SH10 — inscriptions du carnet (post-production locale, 0 crédit)

Image originale **inchangée** : `references/p1/SH10_carnet_Younes_v001.png`. Texte composité, police manuscrite Amatic SC (licence OFL), encre sépia en multiplication (ombrage du papier conservé), légère irrégularité des lettres.
Textes : page gauche « Amina — Mes souvenirs » · page droite « 11 janvier 1944 » / « Nous rêvions d'un Maroc libre. » (la seconde phrase vient de l'utilisateur ; elle n'est pas dans le Draft 1.2).

## Fichiers (`references/p1/post/`)
`SH10_composite_final.png` (état final) · `SH10_text_layer_final.png` (calque RGBA transparent pour Resolve) · `SH10_composite_v001.mp4` (6 s, 1080p25, écriture progressive 0,3 → 4,2 s puis lecture stable ≥ 1,8 s, zoom 1,00 → 1,06) · `animatic/ANIMATIC_1.1b_SH10_composite.mp4` (animatic 1.1 avec SH10 remplacé à 50,5–56,5 s ; son identique).
Script : `scripts/compose_sh10.py` (régénère tout en local).

## DaVinci Resolve (équivalent)
Importer l'image + `SH10_text_layer_final.png` sur V2 (même résolution 2752×1536, mise à l'échelle « Fit »). Pour l'écriture progressive : Fusion → Corner Pin sur un texte, coins (px d'origine) page gauche TL(560,700) TR(950,722) BR(1280,1280) BL(745,1225) ; page droite TL(1090,700) TR(1480,615) BR(1650,1000) BL(1310,1130) ; révélation par Rectangle Mask animé gauche→droite, ligne par ligne, mode de fusion Multiply. Zoom lent 100 % → 106 % sur 6 s.

## Lisibilité (vérifiée dans l'animatic 1.1b, image à 56,4 s)
Tout le texte est lisible et complet avant la coupe ; la date est la ligne la plus petite (≈ 26 px de haut en 1080p) : acceptable en plein écran, à confirmer sur petit écran.
