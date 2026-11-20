# Phase 2 — trois tests AVANT/APRÈS : rapport comparatif (20/11/2026)
**Rien n'a été écouté** (je ne peux pas entendre l'audio) : les chiffres ci-dessous sont des **mesures techniques** ; aucune amélioration audible n'est affirmée. Chaque test est une **proposition à juger par votre écoute**. 0 crédit, aucune génération, aucun master modifié (SHA-256 `0f72fc9a…c029d` revérifié), aucune vidéo produite.

## Base et méthode
* AVANT = `audio/mixes/QC2_SON2/MIX_276s_QC2_SON2.wav` : la source sans perte du master (le master AAC = ce WAV, gain 0,996, retard 0, écart −29,9 dB = bruit AAC) ; générique = silence. Fenêtres calées sur des **images entières à 25 ips** (30,00–65,00 s ; 160,00–190,00 s ; 268,00–299,00 s).
* AVANT et APRÈS sont **identiques au bit près hors des zones modifiées** (écart max 0,0 mesuré sur 47 %, 39 %, 19 % des échantillons des trois fenêtres) : aucune dérive, aucun retard introduit.
* Couches ajoutées : uniquement des sons **déjà dans le projet** (Mixkit 1103, 2427, 2472, 599). Voix de Younes non modifiées.
* **Limite de séparation** : le mix final ne se décompose pas proprement en dialogue / musique / ambiance (les stems de pré-mix expliquent le mix à seulement −7…−9 dB près, la composante « voix » estimée garde des résidus). J'ai donc **écarté** un test d'abaissement du fond sous la voix (impossible à mesurer honnêtement) et gardé des traitements locaux et vérifiables.

## Les trois tests (fichiers dans chaque dossier : `…_AVANT.wav`, `…_APRES.wav`, `…_AB_AVANT_puis_APRES.wav` = AVANT, 1 s de silence, APRÈS ; `MODIFICATIONS.txt`)
| | A — ouverture du carnet (30–65 s, SH07–12) | B — séquence 1955 (160–190 s, SH26–28) | C — générique (268–299 s) |
|---|---|---|---|
| **Ce qui change** | froissement doux de la couverture à 36,20 s (SH08 débute à 36,04 s, mesuré) ; souffle d'air filtré 60,7–65,9 s menant à l'entrée dans l'encre ; fond de SH10–12 resserré à 60 % de largeur, sonie conservée | oiseau à 164,10 s à l'ouverture de la fenêtre (SH26 débute à 163,56 s, mesuré) ; voix V1 (166,5 s) et A5 (182,5 s) **+1,5 dB** sur leur composante ; fond de SH27 (175–182 s) resserré à 60 % | reprise progressive du thème (Mixkit 599, début de piste) de 274,6 s à 299,0 s, entrée sous la fin de MF, montée jusqu'à ~292,6 s puis sortie ; stéréo 60 % pour le mono |
| Sonie intégrée (LUFS) | −17,3 → −17,4 | −16,7 → −16,3 | −16,2 → −16,7 |
| Crête vraie (dBTP) | −2,7 → −2,7 | −2,5 → **−1,2** (marge réduite) | −3,1 → −3,1 |
| Écrêtage | 0 → 0 | 0 → 0 | 0 → 0 |
| Court terme max / P10 (LUFS) | −14,7/−30,0 → −14,7/−29,9 | −14,0/−18,7 → −12,8/−18,7 | −14,9/−47,8 → −14,9/−61,8 |
| Compatibilité mono (perte, fenêtre ciblée) | **−3,59 → −1,75 dB** (SH10–12) | **−2,92 → −1,51 dB** (SH27) | musique ajoutée seule : −3,76 → −1,75 dB |
| Niveau des dialogues (mix entendu, RMS des répliques) | **0,0 dB** (3 répliques inchangées) | **+1,12 dB** (V1), **+1,26 dB** (A5) — volontaire | sans objet |
| Synchronisation | écart nul hors zones ; ancrage SH08 à +0,16 s de la coupe | écart nul hors zones ; oiseau à +0,54 s de la coupe | début de musique 1,5 s **avant** le carton 1 (276,12 s) |

## Questions artistiques (c'est vous qui décidez, à l'écoute)
1. **A** : le froissement et l'air d'encre soutiennent-ils l'entrée dans le carnet sans « effet » ? Le resserrement du fond change-t-il le caractère de SH10–12 (plus central, moins enveloppant) ?
2. **B** : +1,5 dB sur les deux répliques aide-t-il, ou la voix était-elle déjà assez présente ? L'oiseau est-il perçu comme un signe de lumière ou comme un ajout ?
3. **C** : la reprise du thème sous le générique apporte-t-elle l'émotion attendue ? L'entrée sous la queue de MF (274,6 s) est-elle fluide, ou faut-il un silence d'une seconde avant ? Les enchaînements harmoniques (fin de MF puis début de piste) sont **à écouter**.
Option sûre si l'écoute déçoit : garder le silence du générique (D1 de la phase 1).

## Contrôles non faits ou limites
* Synchronisation vérifiée par **détection de coupes sur l'image** (36,04 ; 39,56 ; 163,56 ; 180,60 ; 276,12 s) et identité sample par sample hors zones ; **aucun visionnage** du rendu avec image (aucune vidéo produite).
* Dialogues : niveaux mesurés dans le mix entendu ; le rapport voix/fond isolé n'est pas fiable (résidus de voix dans le fond estimé) : non utilisé comme preuve.
* Sources de test : le « fond » n'a pas été reconstruit depuis les stems (cf. séparation) ; le projet REAPER est une base de travail, pas un équivalent prouvé du mix final.

## REAPER
* **Disponibilité** : REAPER n'est pas installé dans l'environnement cloud, son site n'est pas joignable (aucune installation tentée), aucun ordinateur n'est attaché : je n'ai **ni ouvert ni exécuté** le projet.
* **Livré** : `REAPER_PROJECT/` (89 Mo) — `LE_CARNET_SOUND_PHASE2.RPP` (pistes en 4 bus, 76 marqueurs/régions, médias en chemins relatifs, 8 références vérifiées présentes), `markers.csv`, 2 ReaScripts Lua (marqueurs ; préparation des stems), 1 script de mesures FFmpeg, `README_WINDOWS.md`. Le fichier RPP est écrit selon le format texte, **non validé par le logiciel** ; les scripts Lua n'ont pas été analysés syntaxiquement (Lua absent).

## Historique de ce qui a été corrigé en cours de route (transparence)
Version 1 : réduction de largeur sans compensation → sonie du test A −1,5 LU (rejeté) ; version 2–3 : abaisser le fond de 3 dB sous la voix modifiait aussi la voix (résidus dans le fond estimé, −0,3 à −0,7 dB) → remplacé par un relèvement de la voix ; musique du générique d'abord large en stéréo (−3,76 dB en mono) → resserrée. Les mesures des versions rejetées sont dans `qc/versions_precedentes_rejetees/`.

Scripts : `scripts/build_phase2_tests.py`, `scripts/qc_phase2_tests.py`, `scripts/build_reaper_package.py`. Mesures : `qc/QC_PHASE2_MESURES.json`, `qc/decomposition_lignes.json`, `qc/voix_fond.json`.
