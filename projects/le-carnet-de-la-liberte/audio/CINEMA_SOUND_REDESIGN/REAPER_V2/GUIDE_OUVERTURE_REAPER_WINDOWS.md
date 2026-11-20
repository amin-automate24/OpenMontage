# Ouvrir le projet REAPER v2 sur Windows 10 — guide court
**À savoir :** ce projet a été préparé dans un environnement cloud Linux, sans REAPER. Il n'a **jamais été ouvert dans REAPER** ; les scripts Lua ont passé une vérification de syntaxe (Lua 5.4) et un test avec une API REAPER **simulée**, pas le vrai logiciel. Signalez-moi tout message d'erreur.

## 1. Installer le dossier (2 min)
1. Dézippez **les 6 archives** `LE_CARNET_REAPER_V2_<n>sur6_*.zip`, chacune par *Extraire tout…* dans `Documents\` (elles fusionnent dans `Documents\REAPER_V2\`). **Gardez la structure** : `LE_CARNET_SOUND_V2.RPP`, `media\`, `manifest\`, `scripts\`, `exports\` côte à côte (chemins relatifs, aucun chemin personnel écrit en dur).
2. Facultatif pour le contrôle : FFmpeg et Python 3 installés et accessibles dans le PATH.

## 2. Ouvrir — voie A (recommandée) : fichier .RPP
1. Double-cliquez sur `LE_CARNET_SOUND_V2.RPP`. Si REAPER demande des fichiers manquants : *Browse…* → dossier `media\`.
2. *Actions → Show action list → New action → Load ReaScript…* → `scripts\01_completer_projet_rpp.lua` → *Run*. Le script ajoute les enveloppes de volume (5 580 points), les traitements (plugins fournis avec REAPER uniquement), les envois de réverbération, le limiteur du MASTER réglé à −1 dB, et les marqueurs manquants. Il peut être relancé sans créer de doublon.
3. *File → Save*.

## 2 bis. Voie B (si le .RPP pose problème) : construction par script
*File → New project* (vide) → *Save as…* dans le dossier `LE_CARNET_REAPER_V2\` → lancer `scripts\00_construire_projet_complet.lua`. Le script refuse de s'exécuter si le projet contient déjà des pistes (aucune destruction).

## 3. Image de référence
*Insert → Media file…* → `LE_CARNET_DE_LA_LIBERTE_CINEMA_FINAL_1080p.mp4` (le master, **non fourni dans le paquet, jamais modifié**) sur une piste vidéo, à 0 s, son coupé. *View → Video*. Affichage en images : *Options → Project settings → Video → frame rate 25*, puis règle de temps en *Hours:Minutes:Seconds:Frames*.

## 4. Écoute A/B
* Pistes **REF** (muettes) : mix actuel sans perte et master FINAL. Pour comparer, solo sur REF, puis solo sur MIX BUS.
* **Générique** : `MUS thème 599 + générique v2` (actif) ; alternative `MUS générique v2b (respiration)` (muette).
* **Tests A et B** : pistes `FOL test A` et `FOL test B` muettes par défaut → les activer après votre décision.
* Mono : *View → Mixer*, puis le bouton mono de la piste MASTER (ou contrôle chiffré au § 5).

## 5. Exporter et contrôler
1. Lancer `scripts\02_preparer_exports.lua` (mix MASTER 0–299 s, 48 kHz stéréo, dossier `exports\`). *File → Render…* : vérifier **WAV 24 bits**, puis *Render*.
2. Double-cliquer `scripts\03_controle_qc.bat` en glissant le WAV exporté dessus : durée, écrêtage, crête vraie (≤ −1 dBTP), sonie, LRA, perte en mono, silences, niveau de chaque réplique et synchronisation contre le master FINAL.
