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

## Mise à jour 18/11 — maquettes définitives (décisions utilisateur)
- « FIN » conservé dans SH38 (plan inchangé). Générique 10 s muet, deux cartons.
- `GENERIQUE_FIN_v003.mp4` (avec crédit photo SH08) et `GENERIQUE_FIN_v003_sans_photo_SH08.mp4` (à utiliser tant que SH08 v003b n'est pas intégré) ; maquettes avec les 5 dernières secondes du film : `MAQUETTE_FIN_FILM_PLUS_GENERIQUE_v003*.mp4` ; planche `GENERIQUE_FIN_v003_planche.jpg`.
- Bloc « ARCHIVES PHOTOGRAPHIQUES » en bas du carton 2 (36 px, chiffres alignés, « CC0 » lisible) : 3 lignes avec la photo BnF, 1 ligne sans ; le carton n'est pas surchargé (titre et devise inchangés).
- Crédit Anefo vérifié sur la fiche Commons archivée (`references/p3/historical_sources/`, oldid 1257609662) : « Fotograaf Onbekend / Anefo », vers le 18 août 1953, Nationaal Archief, inv. 2.24.01.09, n° 905-8914, CC0 1.0. CC0 n'impose aucune attribution : le crédit est une courtoisie. La notice primaire du Nationaal Archief (handle) n'a pas été consultée depuis cette session.
- BnF : d'après des sources secondaires (réponse ministérielle 2013, extraits des conditions Gallica), la réutilisation non commerciale est libre avec mention de la source et la réutilisation commerciale relève d'une licence ; la page officielle des conditions n'a pas pu être lue ici. Aucune obligation de licence n'est affirmée : à vérifier sur gallica.bnf.fr avant toute diffusion monétisée.
- Sous-titres : v001 retenu. Réplique 10 (19,1 car/s, 2 lignes courtes de 24 et 21 car.) : vérifiée à l'image ; option `SUBTITLES_FR_QC3_v002_option_cue10.srt` = seule modification, début à 77,15 s (juste après la coupe SH14/SH15 à 77,08 s, 0,45 s avant la voix) → 17,0 car/s, sans désynchroniser la réplique suivante. Aperçu : `APERCU_SOUS_TITRES_v002_cue10_rue1944.mp4`.

## Contrôles ciblés avant intégration (18/11) — générique v004
- Carton 2 : crédits portés à 40 px (titre de bloc 28 px), opacité 92 %, visibles ≈ 3,0 s pleins (6,3–9,3 s) au lieu de ≈ 1,5 s en v003 (seul changement : calendrier et taille). Carton 1 avancé de 0,4–0,5 s : AMIN BENHIDA pleinement visible 2,2–5,2 s. Durée 10,0 s (250 images), muet.
- Raccord fin du film : SH38 (titre + « FIN ») → noir → générique ; aucune superposition, pas de son ajouté. À l'assemblage : compléter l'audio du master par 0,12 s de silence (vidéo 276,12 s / audio 276,00 s) avant le générique.
- Sous-titres v002 (option cue 10) : 32 répliques, UTF-8 sans BOM, numérotation continue, aucun chevauchement (écart minimal 80 ms), ≤ 2 lignes, dernière fin 269,0 s (aucun sous-titre dans SH38 ni le générique) ; cue 10 = 77,150–79,800 s (2,65 s, 17,0 car/s), 2,7 s après la fin de la cue 9, 80 ms avant la cue 11. ASS 1920×1080 identique (32 événements). Aucun décalage requis pour l'ajout du générique (ajouté après 276,12 s) : durée totale 286,12 s.

## Générique v005 (demande « v004 » de l'utilisateur ; v004 existait déjà, conservée) — 13,0 s, 3 cartons
`scripts/build_generique_fin_v005.py` (dérivé de v004, conservé) → `GENERIQUE_FIN_v005.mp4` / `_sans_photo_SH08.mp4` (325 images) ; maquettes avec les 5 dernières secondes du film : `MAQUETTE_FIN_FILM_PLUS_GENERIQUE_v005*.mp4` (18,01 s) ; planche `GENERIQUE_FIN_v005_planche.jpg`.
- Carton 1 (inchangé, 0,5–5,8 s) ; carton 2 devise 5,8–8,9 s (76 px / arabe Amiri 96 px, filet doré, pleinement lisible ≈ 1,7 s) ; carton 3 archives 8,8–13,0 s (titre Cinzel 36 px ; crédits 52 px + source 42 px, blocs espacés ; pleinement lisible ≈ 2,7 s) ; fondu au noir 12,3–13,0 s. Muet.
- Contrôles : arabe correct (liaisons, virgules arabes ; signe de « الله » dégagé du filet), marges ≥ 155 px (zone de sécurité ≥ 96 px), fondus sans saut (variation max 20/255 par image), fin du film → noir → carton 1 sans superposition.
- Crédit BnF uniquement dans la variante « avec BnF », à n'utiliser que si SH08 v003b est intégrée et ses conditions clarifiées.
