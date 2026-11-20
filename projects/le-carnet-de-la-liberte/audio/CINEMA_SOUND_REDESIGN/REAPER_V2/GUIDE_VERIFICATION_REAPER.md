# Vérification de REAPER v2 sur votre PC Windows — pas à pas
**Limite honnête :** je travaille dans un conteneur cloud sans REAPER ; je ne peux donc ni ouvrir le projet, ni constater le chargement des médias, des pistes, des marqueurs, des scripts ou des plugins. Vous allez les exécuter, et **vous me renvoyez deux fichiers** (rapport de diagnostic + export test). Je corrige ensuite uniquement ce qui est en écart. Rien n'est modifié sur le master CINÉMA FINAL, les tests A et B restent muets, aucune voix et aucun équilibre ne sont touchés.

## 1. Télécharger les 6 archives `LE_CARNET_REAPER_V2_<n>sur6_*.zip` (14 à 25 Mo chacune) depuis cette conversation
* Ouvrez la conversation dans le navigateur (claude.ai) sur le PC, pas dans l'application mobile : cliquez la pièce jointe `LE_CARNET_REAPER_V2.zip` → **Télécharger**.
* Si le bouton manque ou si le fichier est tronqué : dites-le-moi, je le dépose sur votre Dropbox (un jeton valide est nécessaire) ou je le découpe en parties.
* Vérification d'intégrité facultative (PowerShell) : `Get-FileHash .\LE_CARNET_REAPER_V2.zip -Algorithm SHA256` ; taille attendue **95 229 295 octets**.

## 2. Installer (3 min)
1. Clic droit sur le zip → *Extraire tout…* dans `Documents\` → vous obtenez `Documents\REAPER_V2\`. **Ne déplacez pas** les dossiers `media`, `manifest`, `scripts`, `exports` : ils doivent rester à côté du `.RPP`.
2. Les scripts de vérification (`04_…`, `05_…`, `03_…` corrigé) et ce guide sont déjà dans l'archive n°1.

## 3. Ouvrir et construire le projet
1. Double-clic sur `LE_CARNET_SOUND_V2.RPP`. Si REAPER signale des fichiers introuvables : *Browse…* → `REAPER_V2\media`.
2. *Actions → Show action list… → New action → Load ReaScript…* → `scripts\01_completer_projet_rpp.lua` → *Run*. **Copiez le texte de la console REAPER** (View → Show console, ou la boîte de dialogue qui s'affiche).
3. *File → Save project*.
4. **Voie B si le RPP échoue** : *File → New project*, *Save as…* dans `REAPER_V2\`, puis lancer `scripts\00_construire_projet_complet.lua` (il refuse de tourner si le projet contient déjà des pistes).

## 4. Diagnostic automatique (30 s)
*Load ReaScript…* → `scripts\04_verifier_environnement.lua` → *Run*. Le script ne modifie rien ; il compare 17 contrôles aux valeurs attendues et écrit `REAPER_V2\diagnostic_reaper.txt`.
**Attendu :** 17 pistes · somme des dossiers 0 · 13 items · 0 média hors ligne · 73 marqueurs + 3 régions = 76 · tests A et B muets · 6 items muets (A, B, v2b, REF mix, REF master 1/2 et 2/2) · ReaLimit sur le MASTER (seuil et plafond −1,0 dB) · ReaEQ, ReaComp, ReaVerbate, ReaLimit disponibles · points de volume sur DX, AMB, MUS. *(Une fréquence d'échantillonnage projet affichée à 0 signale seulement qu'elle suit le périphérique audio : réglez 48000 dans Options → Preferences → Audio → Device ou dans Project settings.)*
→ **Envoyez-moi `diagnostic_reaper.txt`** (glisser dans la conversation).

## 5. Export test court et non destructif
1. Ouvrez `scripts\05_export_test_court.lua`, vérifiez `local WINDOW = "C"` (C = 268–299 s : générique, limiteur, fin ; A et B = autres fenêtres, à faire ensuite si vous voulez), *Run*. Le fichier arrive dans `REAPER_V2\exports\TEST_COURT_C_268-299.wav` (rien d'autre n'est écrit).
2. Si rien n'apparaît : *File → Render…*, les bornes personnalisées sont déjà remplies ; format **WAV 24 bits, 48 kHz, stéréo** ; *Render*.
3. Glissez le WAV sur `scripts\03_controle_qc.bat` (Python + FFmpeg dans le PATH). Sinon **envoyez-moi directement le WAV** (≈ 9 Mo) dans la conversation : je lance les mêmes mesures ici.
**Valeurs attendues pour la fenêtre C :** durée 31,000 s ; **aucun écrêtage** ; **crête vraie ≤ −1 dBTP** (la somme simulée du projet sans limiteur monte à +0,1 dBTP : si la crête vraie dépasse −1 dBTP, le limiteur n'agit pas) ; sonie intégrée de l'ordre de −19 LUFS (reconstruction, pas le master) ; synchronisation : décalage 0 à quelques échantillons dans la première partie (jusqu'à ~275 s) ; au-delà, « non applicable » car le master est silencieux à cet endroit.

## 6. Si une erreur apparaît : correction ciblée (sans reconstruire le projet)
| Symptôme | Cause probable | Correction ciblée |
|---|---|---|
| « Fichiers introuvables » à l'ouverture | dossier déplacé ou renommé | *Browse…* vers `media\` ; ne rien reconstruire |
| Pistes ou dossiers de travers, items mal placés | `.RPP` partiellement lu | Voie B (script 00 dans un projet vide) ; les médias ne sont pas régénérés |
| Console : `attempt to call a nil value (field 'X')` | fonction absente de votre version de REAPER | Envoyez-moi la ligne exacte : je remplace cet appel seul (versions < 6.x : mettre REAPER à jour) |
| « Enveloppe de volume indisponible » | création automatique de l'enveloppe refusée | Clic droit sur le potentiomètre de volume de DX, AMB et MUS → *Show track volume envelope*, puis relancer `01_…lua` |
| « Plugin introuvable : ReaVerbate/ReaLimit… » | nom différent dans votre installation | Notez le nom exact dans le navigateur d'effets (FX → Add) : je corrige la liste dans `lib_carnet.lua` |
| Limiteur non réglé à −1 dB | paramètres nommés autrement | Réglez *Threshold* et *Brickwall ceiling* à −1,0 dB à la main ; je corrigerai les noms recherchés |
| Export absent ou en 16 bits | commande de rendu non acceptée | Passer par *File → Render…* comme au § 5.2 |
| Crête vraie > −1 dBTP | limiteur absent ou contourné | Vérifiez qu'il est actif sur le MASTER et après tous les traitements |
| Synchronisation décalée > 100 échantillons | item DX déplacé | DX doit commencer à 0,000979 s ; ne pas le faire glisser |
