# Générique de fin et sous-titres — QC3 SON2 (MAQUETTES, NON INTÉGRÉES)
## Générique (10,0 s, après 276,12 s → durée totale prévue 286,12 s)
`scripts/build_generique_fin.py` → `animatic/qc2/GENERIQUE_FIN_v002.mp4` ; maquette avec les 5 dernières secondes du film : `MAQUETTE_FIN_FILM_PLUS_GENERIQUE_v002.mp4`.
- 0–0,6 s ouverture au noir ; carton 1 (0,9–6,2 s) : titre (Cinzel or 62 px), « Court-métrage écrit, réalisé et produit par » (Cormorant 46 px), **AMIN BENHIDA** (Cinzel 116 px ivoire, élément dominant), « Enseignant à l’École communautaire de Tiddas » (44 px) ; carton 2 (6,3–9,9 s) : « Dieu, la Patrie, le Roi » + « الله، الوطن، الملك » (Amiri, mise en forme arabe vérifiée) en or, crédit photo (36 px) ; fondu au noir 9,3–10 s.
- Fond sombre à vignettage et grain léger (pas de banding au projecteur). Polices OFL (licences dans `assets/fonts/ofl/`).
- Audio : silence (aucune nouvelle musique). Le film se termine déjà sur le fondu de la musique B (MF, 271–276 s).
- Le crédit photo n'est affiché que si SH08 v003b est intégré (option `--sans-credit-photo` sinon).
## Sous-titres
`animatic/SUBTITLES_FR_QC3_v001.srt` (nouveau ; QC1 conservé) + style `SUBTITLES_FR_QC3_v001_style1080.ass` (Inter SemiBold 52 px, blanc, contour 2,6 px sombre, ombre légère, marge basse 62 px, 2 lignes max).
- Texte : identique au script des dialogues (32 répliques, vérifié automatiquement) ; seules modifications : coupure « décider de l'avenir / de son pays » (au lieu de « de son / pays »), « Non, Amina. » isolé, espaces insécables avant ? ! : ;
- Synchronisation recalée sur les pauses mesurées dans le stem voix : 10/11 (la 2e phrase était affichée 0,6 s après le début de la voix), 19/20 (« Malgré les épreuves » affiché trop tôt), 28/29, 30/31, 24/25, 14/15 ; écarts entre sous-titres ≥ 2 images (5 écarts d'1 image corrigés) ; aucun chevauchement ; apparition 0,05–0,25 s avant la voix.
- Lignes ≤ 42 caractères sauf cue 15 ligne 2 (44, coupure sémantique). Vitesse ≤ 15 car/s pour 22 cues ; 15,0–16,6 pour 9 cues (débit de voix) ; cue 10 « Parce que notre pays vit sous le protectorat. » 19,1 car/s (phrase dite en 2,2 s, impossible à rallonger sans désynchroniser).
- Aucun masquage : cartons (dates, mentions « non archive », « Reconstitution fictive ») en haut ou hors des répliques ; vérifié sur 14 images. Aucun sous-titre pendant SH38 ni le générique.
- Aperçu incrusté (7 scènes, 126 s) : `animatic/qc2/APERCU_SOUS_TITRES_QC3_v001.mp4` + planche.
## Livrables prévus après autorisation
A (scolaire) : QC3 SON2 + générique, sous-titres incrustés (ASS ci-dessus). B (cinéma/YouTube) : QC3 SON2 + générique, sans incrustation + SRT séparé. 1920×1080, 25 fps ; 276,12 s + 10,0 s.
