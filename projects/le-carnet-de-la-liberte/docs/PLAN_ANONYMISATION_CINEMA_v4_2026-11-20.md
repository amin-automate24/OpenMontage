# CINÉMA v4 — Plan d'anonymisation de l'édition YouTube (INTERNE — ne pas publier) — 20/11/2026
**Statut : DÉCISION CRÉATIVE APPROUVÉE — RENDU EN ATTENTE D'AUTORISATION.** Aucun fichier vidéo créé ou modifié. Édition CINÉMA uniquement ; SCOLAIRE v4, quiz, SRT, registres et master CINÉMA v4 inchangés.

## 1. Références personnelles et scolaires trouvées (inventaire)
| # | Où | Texte exact | Minutage (master CINÉMA v4, 25 ips) |
|---|---|---|---|
| 1 | Carton 1 du générique, ligne d'attribution | « Court-métrage écrit, réalisé et produit par » | entrée 0,30 s après le début du générique ≈ image 6910 ; plein de ≈ 6915 à ≈ 7033 ; sortie jusqu'à ≈ 7048 |
| 2 | Carton 1, nom | « AMIN BENHIDA » (Cinzel 700, 116 px, nom du propriétaire) | entrée 0,40 s ≈ image 6913 ; même sortie |
| 3 | Carton 1, fonction/établissement | « Enseignant à l’École communautaire de Tiddas » (nom de l'école) | entrée 0,50 s ≈ image 6915 ; même sortie |
| 4 | Métadonnées incorporées du master | titre « LE CARNET DE LA LIBERTÉ — NON FINAL (contrôle interne) » ; commentaire « NON FINAL — diffusion non autorisée » ; tags logiciels `Lavf60.16.100` / `Lavc60.31.102 libx264` | aucun nom ni école ; les mentions « NON FINAL » devront disparaître de la copie publique |
| — | Film (images, dialogues), SRT, quiz | « Amina » (SRT) = personnage fictif ; aucun autre nom du propriétaire ou de l'école trouvé (recherche textuelle de tous les scripts, SRT, ASS, quiz ; échantillon d'images revu) | — |
| — | Documentation interne | `docs/GENERIQUE_SOUS_TITRES_QC3.md`, ancien rapport de pré-publication (brouillon de description) | **conservés** (dossiers internes) ; le brouillon de description est remplacé par le paquet anonyme |
*Limite : aucune lecture automatique du texte (OCR) n'est disponible ; l'absence de texte parasite dans les images générées repose sur la revue d'images échantillonnées et l'historique de production.*

## 2. Suppressions exactes proposées
Retirer du carton 1 les lignes 1, 2 et 3 ci-dessus et rien d'autre. Le titre, la devise (carton 2), les crédits d'archives (carton 3 : Anefo ; BnF **sous réserve de la décision SH08**) et « FIN » (SH38) restent identiques. Aucun réalisateur, aucune société, aucun pseudonyme ajouté.

## 3. Texte du générique révisé (carton 1)
* **Proposition A (recommandée)** : « LE CARNET DE LA LIBERTÉ » (Cinzel 500, 100 px, espacement 8 → 1 497 px de large, limite 1 640 px) · filet doré · « Court-métrage d’animation » (Cormorant Garamond 500, 46 px, ivoire ; 495 px). Descripteur de genre, pas une attribution.
* Variante B : titre seul + filet (le plus sobre).
* Mise en page A : titre centré vertical à y ≈ 480 (au lieu de 300), filet à y ≈ 548 (demi-largeur 260 px, comme aujourd'hui), descripteur à y ≈ 610. Polices, couleurs (or / ivoire), fond sombre et grain inchangés. Le carton garde la composition centrée des cartons 2 et 3.

## 4. Impact sur durée, transitions, mise en page
* **Durée et images inchangées** : générique 572 images (22,88 s) ; film 7 475 images, 299,000 s ; mêmes balises couleur.
* **Transitions inchangées** : fondu depuis le noir de 0,6 s au début du générique (image 6903) ; carton 1 → carton 2 → carton 3 avec les mêmes fondus (carton 1 jusqu'à ≈ 5,8 s, carton 2 ≈ 5,8–8,9 s, carton 3 plein ≈ 9,6–22,18 s puis fondu au noir).
* **Rythme du carton 1** : mêmes entrées/sorties ; titre à 0,20 s, filet à 0,30 s, descripteur à 0,60 s ; le carton, plus léger, reste lisible 4,6 s (aucune lecture à garantir au-delà du titre).
* **Audio** : aucune modification ; le générique est muet.

## 5. Opérations de rendu requises (rien lancé)
1. **R1 — Nouveau carton** (≈ 1 min, local) : script dérivé `build_generique_fin_v006_anonyme.py` (v005 conservé) → `GENERIQUE_FIN_v006_anonyme_c3_12s6.mp4` (572 images, muet) ; contrôle d'une image du carton 1 (aucun nom, marges, lisibilité).
2. **R2 — Assemblage « CINÉMA v5 — NON FINAL »** (≈ 2–3 min) : copie sans réencodage des images 0–6864 de CINÉMA v4 (dernière image clé avant 6903 = image 6865) ; réencodage seulement des images 6865–7474 (images 6865–6902 du film + nouveau générique) avec les mêmes réglages x264 (High 4.0, CRF 17, GOP 50, BT.709/170M) ; **piste audio AAC d'origine recopiée telle quelle** ; fichier neuf, v4 conservé. *Repli si la jonction n'est pas propre : ré-exécuter le pipeline complet (≈ 10 min) avec le nouveau générique.*
3. **R3 — QC ciblé** : 7 475 images, 25 ips, 299,000 s ; images 0–6864 identiques à v4 (comparaison de paquets) ; images 6865–6902 ≥ 45 dB vs v4 ; audio identique (MD5) ; aucune chaîne du nom ou de l'école dans le fichier (recherche binaire) ; carton 1 contrôlé à l'image ; empreintes SHA-256 ; envoi Dropbox. Aucune étiquette FINAL.
4. **R4 — Copie de diffusion** (seulement après votre autorisation « FINAL » et la levée des blocages de droits) : remuxage sans réencodage, noms publics neutres, métadonnées nettoyées (§ paquet anonyme).
*Facultatif avant R1 : une image-maquette du carton 1 (un seul PNG) pour validation visuelle.*

## 6. Points d'attention
* L'anonymat à l'écran **n'empêche pas** d'identifier le demandeur dans la demande de licence BnF (échange privé, nécessaire) ; la mention publique de la BnF reste obligatoire.
* L'identité du compte YouTube, les liens Dropbox et le nom de la chaîne relèvent du propriétaire (hors périmètre).
* Les blocages de droits du rapport de pré-publication (SH08, preuves ElevenLabs/Magnific) restent **inchangés** par cette décision.
