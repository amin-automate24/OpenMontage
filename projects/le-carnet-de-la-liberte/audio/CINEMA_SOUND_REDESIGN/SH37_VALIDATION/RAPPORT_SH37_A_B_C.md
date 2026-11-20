# SH37 — comparatif A / B / C : rapport technique concis (20/11/2026)
**But : choisir la meilleure solution artistique.** Aucune écoute de ma part : les chiffres sont des **mesures** ; le choix dépend de votre oreille. Master FINAL (SHA-256 `0f72fc9a…c029d`), mix source, projet REAPER et sources : **non modifiés** ; fichiers nouveaux uniquement ; aucun rendu complet ; 0 crédit.

## Le fichier
`audio/SH37_comparatif_A_B_C_267-273.wav` (22,58 s, 16 bits 48 kHz) · `SH37_comparatif_INDEX.txt`.
Repères : **A = 1 bip, B = 2 bips, C = 3 bips** (1 kHz, 0,12 s, −24 dBFS), puis 0,5 s de silence, puis la version (6,000 s chacune = **fenêtre du film 267,000–273,000 s, identique pour les trois**) ; **1,000 s de silence** entre une version et les bips de la suivante.
Repères temporels dans le fichier : A 0,62–6,62 s · B 8,48–14,48 s · C 16,58–22,58 s.

## Les trois versions
| | Contenu | Construction |
|---|---|---|
| **A** | bruitage de synthèse d'origine | mix du master (sans perte), **inchangé** |
| **B** | atténuation de **−20 dB** | contribution AMB × creux −20 dB entre 267,45 et 270,65 s (rampes cosinus 0,2 s et 0,3 s) |
| **C** | **plume réelle** Mixkit 2369 | contribution AMB × creux −60 dB (même zone, mêmes rampes) **+** 4 gestes de la plume réelle, **discrets** |
La contribution AMB est isolée par une décomposition mesurée : mix = reste + g·AMB, avec retard 47,7 échantillons et gain +14,6 dB ; en la retirant, l'énergie 4–8 kHz du mix baisse de 15,9 dB (la plume y est donc bien reconnue). Le « reste » (musique, voix, tout le reste du mix) n'est pas touché.

## Plume réelle de la version C
Le fichier Mixkit 2369 ne dure que **1,19 s, dont 0,55 s de geste actif** (spectre : 500–2 000 Hz dominant, 4–8 kHz à −29 dB relatif : très différent du bruit de synthèse). Il est utilisé en **4 gestes** : à 267,80 s (vitesse 1,00, 0 dB) · 268,50 s (0,97, −2 dB) · 269,20 s (1,04, −1 dB) · 269,85 s (0,99, −4 dB), fondus 20 ms/80 ms, centré. **Niveau :** −16,1 dB net sur la source (plus les gains par geste) → RMS des parties actives −42 dBFS, crête −23,1 dBFS, soit ≈ 23 dB sous le RMS de la musique (−19 dBFS) ; énergie 4–8 kHz de la plume seule −71 dBFS (contre −32 dBFS pour le bruit de synthèse). Ce niveau est un choix de « discrétion » à juger à l'oreille.

## Mesures (fenêtre 267–273 s)
| | A | B | C |
|---|---|---|---|
| Énergie 4–8 kHz à 268,0 / 268,5 / 269,0 / 269,5 / 270,0 s (dBFS) | −31,4 / −33,7 / −32,1 / −29,6 / −37,8 | −43,8 / −48,2 / −47,2 / −45,9 / −49,7 | −47,4 / −49,8 / −46,3 / −47,9 / −48,3 |
| Plancher HF hors rafale (267,0–267,9 s et ≥ 271 s) | ≈ −46…−47 | idem | idem |
| RMS 267,7–270,3 s | −19,2 dBFS | −19,5 | −19,5 |
| Sonie intégrée de la fenêtre | −15,9 LUFS | −16,0 | −16,0 |
| Crête vraie / crête échantillon | −3,1 dBTP / −3,12 dBFS | −3,1 / −3,08 | −3,0 / −3,05 |
| Écrêtage | 0 | 0 | 0 |
| Perte en mono dans la zone | −2,44 dB | −2,61 dB | −2,56 dB |
**Lecture :** B et C ramènent l'énergie 4–8 kHz **au plancher** de la fenêtre (≈ −46…−50 dBFS, donc plus aucune rafale ressortant de ce plancher) ; C n'ajoute pratiquement pas d'aigus (−71 dBFS), son apport est médium.

## Les autres éléments sonores restent-ils inchangés ?
* **Hors zone 267,45–270,65 s : identiques à A** — écart maximal 3·10⁻¹⁰ (flottant) ; **0 échantillon différent** sur 16 bits dans le fichier livré, pour B et C.
* **Voix** : aucune dans la zone (la fin de Y5, avant 267,45 s, est identique) ; **musique** (50–2 000 Hz) : RMS −19,4 dBFS en A et en B, −19,3 en C, soit un écart ≤ 0,1 dB : inchangée.
* **Ce qui change réellement dans la zone** : tout ce que porte le bus AMB, pas seulement la plume. Énergie de la différence (A − version) : B = 50–1 000 Hz −39,8 / 2–4 kHz −38,5 / 4–8 kHz −34,3 dBFS ; C = −38,0 / −37,5 / −33,4 dBFS (C inclut l'ajout de la plume réelle). Le fond d'ambiance résiduel (ton de pièce, début du vent à 270,5 s dont la rampe de remontée finit à 270,65 s) est donc **aussi atténué**, à ≈ 20 dB sous la musique : probablement masqué, **mais à écouter**.

## La version C nécessite-t-elle une modification du bus AMB ou des médias sources ?
* **Bus AMB : oui.** Il faut automatiser son volume (creux à −60 dB entre 267,45 et 270,65 s, ou −20 dB pour B) : c'est une modification de l'**enveloppe de volume de la piste**, non destructive et réversible. Elle atténue aussi le reste de l'ambiance dans cette zone (voir ci-dessus). Une variante plus chirurgicale (couper seulement 2–8 kHz de la piste AMB par un égaliseur automatisé) conserverait mieux le fond : possible, plus complexe, non faite.
* **Médias sources : non.** Aucun fichier existant n'est modifié ni remplacé : la plume réelle est **déjà dans le projet** (`assets/sfx/mixkit/mixkit_2369_writing_scribble_on_paper.wav`). Il faut seulement l'ajouter au projet REAPER comme **4 items sur une piste FOL** (copie du média dans `media/`, longueur 0,6 s, positions 267,80 / 268,50 / 269,20 / 269,85 s, vitesses 1,00 / 0,97 / 1,04 / 0,99, gains −16,1 / −18,1 / −17,1 / −20,1 dB, fondus 20 et 80 ms). Alternative plus lourde, non nécessaire : régénérer la source d'ambiance sans le repère « plume » (nouveau fichier M7d, par `sound_design_m7c_test.py`), sans toucher à l'existant.
* **Le master FINAL** ne peut être concerné que par une décision ultérieure : nouvelle copie après votre choix, jamais d'écrasement.

## À écouter (non mesurable)
1. A : le crépitement est-il bien ce que vous avez entendu ? 2. B : suffisamment atténué, ou la plume manque-t-elle ? 3. C : la plume réelle est-elle naturelle et discrète (quatre gestes, un peu espacés), ou trop présente / trop sèche ? 4. Dans B et C, le fond d'ambiance paraît-il creusé pendant ces 3 secondes ? 5. Préférence finale A / B / C (ou C à un autre niveau).
Scripts : `scripts/build_sh37_comparatif.py` · mesures : `analysis/sh37_mesures.json`.
