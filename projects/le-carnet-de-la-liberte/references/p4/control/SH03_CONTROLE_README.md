# SH03 — éléments de validation (NON VALIDÉ, 17/11/2026)

Fichiers : `SH03_control_hr_v001_v002_v005.png` (recadrages natifs 2752×1536 : plan large avec rayon pupille→visage de la maîtresse, yeux ×3, tête), `SH03_control_measures.json`, `SH03_frame_1080p_animatic2.1_t13.0.png` (le plan tel que livré en 1080p), preuve précédente `references/p4/post/SH03_gaze_proof_rays_v005.jpg`. Script : `scripts/sh03_control_sheet.py` (lecture seule).

Constats (mesure + recadrages) :
- **Cible** : yeux de la maîtresse (flou de profondeur de champ) vers (925, 452) ; direction pupille→cible : v002 13,1°, v005 12,7°. Regard mesuré précédemment : v005 14,0° (écart ≈ 1,3°, à comparer à 18,6° pour v002).
- **Yeux** : v005 iris en bord gauche de l'ouverture, sclère visible à droite, reflets cohérents, identité (couleur, forme, sourcil) inchangée vs v002.
- **Tête** : inclinée de 4° ; sourire et oreille cohérents.
- **Défauts visibles en zoom (et un peu en 1080p)** : (1) léger éclat/bavure au bout du nez, autour de (1700, 710) ±25 px ; (2) fine ligne verticale de raccord à gauche du front, x≈1755–1765, y≈560–700.
- v001 est un cadrage face caméra (regard à l'objectif) : pas comparable.

Correction locale possible (non appliquée) : retouche v006 = réparation du bout du nez et de la ligne de raccord par reconstruction d'arrière-plan/peau (même méthode `cv2.inpaint` + fondu), sur une copie, sans toucher aux yeux ni à l'identité. Coût 0 crédit, ≈ 30 min. Le regard lui-même n'a pas besoin d'être modifié d'après la mesure ; la validation reste visuelle, à votre charge.
