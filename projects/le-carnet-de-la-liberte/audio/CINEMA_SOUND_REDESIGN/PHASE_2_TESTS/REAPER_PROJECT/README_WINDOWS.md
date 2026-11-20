# Paquet REAPER — Phase 2 sonore (préparatoire) — Windows
**Statut honnête : ce projet a été généré par script. REAPER n'existe pas dans l'environnement de préparation : il n'a jamais été ouvert ni exécuté.** Le format `.RPP` suit la spécification texte de REAPER ; si une ligne est refusée, REAPER l'ignore ou affiche une erreur : dans ce cas, créez les pistes à la main (voir tableau) et exécutez `01_setup_markers_et_pistes.lua`.

## Installation
1. Dézippez **le dossier entier** n'importe où (garder `media/`, `scripts/`, `markers.csv` à côté du `.RPP`) : les médias sont référencés par chemins **relatifs** (`media/…`), donc aucun lecteur ni nom d'utilisateur n'est écrit en dur.
2. Double-cliquez sur `LE_CARNET_SOUND_PHASE2.RPP` (REAPER 6.x ou 7.x). Si REAPER demande des fichiers manquants : *Browse* → dossier `media/`.
3. Images : *Insert > Media file* → `LE_CARNET_DE_LA_LIBERTE_CINEMA_FINAL_1080p.mp4` (jamais fourni ici, jamais modifié) sur une piste vidéo, début à 0 s, pour vérifier la synchro. Les pistes `REF` (muettes) contiennent le son actuel pour comparer.
4. Scripts : *Actions > Show action list > New action > Load ReaScript…* → `scripts/01_setup_markers_et_pistes.lua` (marqueurs depuis `markers.csv`), puis `02_rendre_stems_et_test.lua` (préparation des stems). `03_mesures_ffmpeg.py` mesure un export (ffmpeg requis, `python 03_mesures_ffmpeg.py export.wav`).

## Pistes (4 bus dossier)
| Bus | Piste | Média | Remarque |
|---|---|---|---|
| DX | DX stem M6 | `DX_dialogue_stem_M6_276s.flac` | posé à +0,00098 s (47 échantillons) pour caler le stem sur le mix final |
| AMB | AMB+FOLEY M7c | `AMB_FOLEY_M7c_276s_melange.flac` | ambiance et foley **mélangés** dans la source ; séparation possible seulement en régénérant avec `scripts/sound_design_m*.py` du dépôt |
| FX | PH2-A, PH2-B | couches ajoutées aux tests A et B | positions 36,00 s et 163,90 s |
| MX | thème Mixkit 599 (4 cues M9T), PH2-C | `mixkit_599_possible_dreams.mp3` + reprise du générique à 274,60 s | niveaux des cues = ceux du rapport M9T (pré-mastering) |
| REF | mix actuel sans perte ; master FINAL décodé | muets | comparaison A/B |

**Limite importante :** la somme DX + AMB + MX de ce projet n'est **pas garantie identique** au mix final (le mix final provient de plusieurs versions assemblées : voir `PHASE_2_TESTS/RAPPORT_COMPARATIF_PHASE2.md`). Pour A/B fiable, utiliser les pistes `REF` et les WAV AVANT/APRÈS fournis.

## Ce que les trois tests ont fait, et comment le refaire dans REAPER
* **Test A** : foley de couverture à 36,20 s et souffle d'air filtré 60,7–65,9 s = pistes PH2-A ; fond SH10–12 (50,5–65,0 s) à 60 % de largeur stéréo à sonie conservée = plug-in de largeur (JS: *Stereo width* ou *Mid/Side*) sur la piste AMB, avec compensation de gain.
* **Test B** : oiseau 164,1 s (PH2-B) ; voix +1,5 dB sur V1 (166,5 s) et A5 (182,5 s) = enveloppe de volume sur la piste DX ; fond SH27 (175–182 s) à 60 % de largeur.
* **Test C** : reprise du thème = PH2-C (déjà préparée, piste MX).
