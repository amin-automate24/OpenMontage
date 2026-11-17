# Préparation du master (base M5) — 17/11/2026 — NON FINAL

## Décisions artistiques retenues
- Younes = Timothée (validation d'écoute finale à confirmer). Version principale **sans sous-titres incrustés** ; SRT français facultatif **sans noms de personnages** : `animatic/SUBTITLES_FR_M5_sans_noms.srt` (25 sous-titres calés sur M5, ponctuation française insécable).
- Bandeaux techniques et préfixes de personnages supprimés du rendu propre (`build_animatic_v2.py --clean`).
- Musique : instrumentale sobre, thème récurrent, sans paroles ; **aucune musique sur SH22 (2:06–2:14) ni SH33 (3:45.5–3:59.5)**.

## Rendu propre 1080p
`animatic/MASTER_CLEAN_1080p_video_prep.mp4` : vidéo seule 1920×1080, 25 i/s, toutes les images/clips/cartons validés : SH03 v006 verrouillée, SH17 et SH31 avec mentions « non archive », SH22 « Reconstitution fictive », SH27/SH29, ligne du temps SH33 avec note H4, titre SH38. Les cartons pédagogiques font partie de l'image (conservés) ; ni heure/plan en haut à gauche, ni sous-titres. Pas d'audio dans ce fichier (assemblage ultérieur).

## Source musicale
Recherche limitée aux ressources déjà disponibles : `projects/.../assets/music/` vide ; aucun dossier `music_library/` ; seuls des effets sonores (sans licence documentée) dans les compétences de l'outil. **Aucune piste musicale avec licence documentée n'est disponible : version SANS MUSIQUE conservée.** Rien n'a été téléchargé, acheté ni généré.

## Finition audio (candidat M6, local, `audio/mixes/M6/`)
Même mix que M5 (voix, ambiances, bruitages, radio v2, A2/A4) avec chaîne « salle de classe » : passe-haut 70 Hz, compression douce du bus (seuil −27 dB, 2,4:1), normalisation −16 LUFS, plafond de crête −1,0 dBTP (limiteur à −1,5 dBFS d'échantillon). M5 non modifié.

## Fairlight (travail humain sur la base M6)
1. Import : piste vidéo = `MASTER_CLEAN_1080p_video_prep.mp4` ; pistes audio = stems M6 (`stems/dialogue.wav`, `stems/ambience_music_ducked.wav`) ; piste guide = `MIX_276s_M6.wav`.
2. Dialogues : ±2 dB entre personnages, coupe-bas 80 Hz, de-esser léger ; Timothée sans pitch/formant ; radio inchangée.
3. Bus ambiances : −9 dB sous voix ; fondus aux changements de scène ; musique (si ajoutée plus tard) coupée sur SH22 et SH33.
4. Bus maître : compresseur doux (≈ 2:1) + limiteur −1 dBTP ; vérifier au Loudness Meter **−16 LUFS intégrés**, LRA ≤ 8–10 LU.
5. Écoute de contrôle : haut-parleur de classe et repli mono ; pas de voix masquée par ambiance.
6. Livraison (non autorisée à ce jour) : MP4 H.264/AAC 48 kHz stéréo, `scripts/check_delivery.py`.
