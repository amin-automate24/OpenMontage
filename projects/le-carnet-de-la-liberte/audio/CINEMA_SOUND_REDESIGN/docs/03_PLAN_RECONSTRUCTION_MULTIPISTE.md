# 3. Plan de reconstruction multipiste
## 3.1 Architecture (48 kHz / 24 bits, 299 s, calée sur l'image du master)
| Bus | Pistes | Contenu | Source |
|---|---|---|---|
| **DX — DIALOGUES** | DX1 Maîtresse · DX2 Younes · DX3 Amina · DX4 Père · DX5 Mère · DX6 Radio/voix hors champ | Répliques individuelles originales (32), corrections ciblées | `audio/voices_m2_lot/wav/*.wav` (24 bits, 48 kHz mono, une réplique par fichier), `audio/voices_younes_timothee/wav/`, `audio/voices_final/A7.wav`. **Aucune séparation IA nécessaire.** |
| **AMB — AMBIANCES** | AMB1 tons de pièce · AMB2 extérieurs (air, oiseaux, saisons) · AMB3 foules (rue, Rabat) | Fonds continus par lieu, transitions fondues sur les coupes | Mixkit 2427, 2472, 2475, 2658, 364, 437, 462 + synthèse locale M4–M7 (scripts reproductibles `sound_design_m*.py`, graine 1956) |
| **FX — FOLEY / SFX** | FX1 carnet & pages · FX2 écriture (stylo, craie) · FX3 pas & objets · FX4 transitions (encre, saisons, tampons) | Sons synchrones aux gestes visibles + marqueurs de dates | Mixkit 1101/1103/1104/1105, 1270, 2368, 2369 ; synthèse locale ; éventuels ajouts (§ 5) |
| **MX — MUSIQUE** | MX1 thème · MX2 variations · MX3 générique | Thème en 4 états + reprise au générique | Mixkit 599 (acquise, licence archivée) ; ajouts éventuels (§ 5) |
| **Retours** | REV classe · REV maison · REV rue · REV radio | Réverbérations de lieu | Traitement local ffmpeg ou Fairlight |
| **Sorties** | Print master stéréo ; **stems DX / AMB / FX / MX** ; **M&E** (sans dialogues, pour une version arabe/anglaise ultérieure) ; vérification mono | | |

## 3.2 Sources existantes — réalité vérifiée
* **Séparées et exploitables** : chaque réplique (fichiers 24 bits) ; les 14 sons Mixkit et 2 musiques ; les scripts de synthèse (reconstruction exacte des bruitages locaux).
* **Mélangées dans des stems** : `audio/stems/ambience_music_ducked.wav` (ambiance + musique) ; `audio/sfx_m6/ambience_foley_m6.wav` (ambiance + foley). Les pré-mix `audio/mixes/M9T_pre/ambience_ducked.wav` et `music_bed_ducked.wav` séparent musique et ambiance, mais ne couvrent que **276 s** (pas le générique) et ne sont peut-être pas identiques au mix du master final.
* **Séparation IA : non recommandée ici.** Elle serait nécessaire seulement pour récupérer des éléments d'un fichier déjà mixé ; ici on reconstruit depuis les sources. Limites si elle était employée (non installée : ni torch, ni demucs) : voix qui « bavent » sur la musique, résidus de réverbération, perte d'aigus ; inacceptable sur les voix d'enfants.
* Aucun fichier de **projet Fairlight** n'existe dans le dépôt ; le montage image existe en EDL/FCPXML (`timeline/`) et dans le master.

## 3.3 Méthode de travail
1. **Recaler** : exporter l'image de référence du master (aucune image modifiée) et la table de plans/timecodes ; créer les marqueurs (CSV/EDL) pour chaque réplique, geste, date et cue.
2. **Reconstruire** DX → AMB → FX → MX dans cet ordre ; contrôle à chaque étape par mesure (LUFS court terme, corrélation, intelligibilité = rapport voix/fond ≥ 15 dB sur les passages parlés).
3. **Mixer** avec ducking léger sur dialogues (−6 dB, 250 ms/600 ms), fondus de lieux, repli mono vérifié.
4. **Livrer** : candidat `CINEMA_SOUND_REDESIGN_v1` = **nouvelle vidéo mux image inchangée** (copie du flux vidéo du master FINAL sans réencodage, SHA-256 vérifié sur les 7 475 images) + audio nouveau ; masters stems et M&E à part.
5. **Valider** à l'écoute (vous) avant toute promotion ; le master FINAL reste intact.

## 3.4 Outils réellement disponibles (vérifié)
| Outil | Statut | Conséquence |
|---|---|---|
| ffmpeg (afftdn, arnndn, sidechaincompress, loudnorm, acompressor, alimiter, aecho, firequalizer…) + numpy | **Disponible ici** | Reconstruction et mixage **headless** possibles, reproductibles par script |
| DaVinci Resolve / Fairlight | **Absent du conteneur** ; aucun ordinateur n'est attaché à la session | Je ne peux **pas** piloter Fairlight. Je prépare un **paquet d'import** (stems WAV, EDL/FCPXML, marqueurs, image de référence) pour un finissage manuel sur votre PC, ou je produis le mixage complet en headless |
| ElevenLabs (via connecteur) | **Disponible** — forfait Starter, 1 604 / 40 000 caractères utilisés ce mois | Corrections de voix et éventuel Voice Design réalisables ; SFX/musique ElevenLabs passent aussi par Magnific (voir § 5) |
| Magnific Plus (audio : SFX ElevenLabs, musique Lyria) | **Disponible** — 7 818 crédits | Voir § 5 |
| Artlist | Essai gratuit, **0 crédit**, 2 images et 1 vidéo gratuites | Inutilisable pour la bande-son |
| Banques libres autorisées (Mixkit, Openverse, Freesound CDN) | Hôtes autorisés dans l'environnement | Musiques/SFX à licence vérifiable : **0 crédit**, licence à archiver pour chaque fichier |
| Séparation IA (demucs/torch) | Non installés | Non nécessaire |
