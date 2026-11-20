# AUDIO — casting ElevenLabs Multilingual v2, vérifications, assemblage et finition (2.0) — rien de payant lancé

## 1. Casting (voix FR de la bibliothèque, lues en lecture seule ; script par réplique : `audio/elevenlabs_script_multilingual_v2.json`)
| Personnage | Voix proposée | Réglages (stab./sim./style/vitesse) | Remarque |
|---|---|---|---|
| Younes (10 ans) | **aucune voix d'enfant FR dans la liste** → *Voice Design* (garçon ~10 ans) ou jeune comédien ; repli : Jules – Warm French Storyteller | 0,35 / 0,80 / 0,45 / 1,05 | cohérence maximale : une seule voix pour tout le film |
| Amina 11 → 23 ans | Julia – Warm French Narrator (jeune, chaude) | 0,45 / 0,80 / 0,40 / 1,0 | enfant : diction légère ; adulte : posée, émotion contenue |
| Le père | Christophe – warm mature narration | 0,60 / 0,80 / 0,25 / 0,95 | rassurant, sans « voix de pub » |
| La maîtresse | Marine – Warm and Captivating | 0,50 / 0,80 / 0,30 / 1,0 | |
| La mère | Dahlia – Podcasts et livres audio | 0,55 / 0,80 / 0,30 / 1,0 | une seule apparition (SH09) |
| Voix radio (reconstitution fictive) | Damien Doré – Deep Narrator + filtre radio en post | 0,70 / 0,75 / 0,10 / 0,95 | anonyme ; **jamais** une imitation de Mohammed V |
| Voix hors champ | Dorian – Parisian | 0,35 / 0,80 / 0,50 / 1,05 | |
Multilingual v2 n'a **pas** de balises audio (réservées à v3/v4) : émotion par ponctuation, points de suspension et `<break time="0.5s" />`.

## 2. Deux répliques test (73 caractères au total)
- **Younes — curiosité (Y3, SH09)** : « Maman ! À qui appartient ce carnet ? » (36 car.)
- **Amina adulte — émotion (A7, SH32)** : « Tant de personnes ont espéré ce jour… » (37 car.)

## 3. Crédits, coût, licences, intégration (vérifié le 17/11)
- **Connecteur ElevenLabs** : lecture des voix et du guide de modèle OK ; **solde/forfait refusés** (« permissions supplémentaires : reconnecter le connecteur ») → crédits ElevenLabs **non vérifiables**. Connecteur « restreint » : voix/parole seulement. Aucun accès supposé.
- **Multilingual v2 n'est pas proposé via Magnific** (modèle refusé par `audio_tts`) : il faut passer par le connecteur ElevenLabs et ses crédits propres.
- **Coût** : Multilingual v2 ≈ 1 crédit ElevenLabs par caractère (barème public usuel, **à confirmer** sur votre forfait) → test ≈ **73 crédits ElevenLabs** ; film complet 1 539 car. ≈ 1 540 (+ reprises). Alternative Magnific (ElevenLabs v3, 0,2 cr/car., prix simulé) : test ≈ **15 crédits Magnific** ; film ≈ 308.
- **Licences** : usage commercial/diffusion dépend du forfait ElevenLabs et des conditions de chaque voix de la bibliothèque (non vérifiés) ; interdits : clonage/imitation de personnes réelles, voix du souverain. Voix d'enfant : Voice Design ou comédien avec autorisation parentale.

## 4. Fichiers de dialogue et synchronisation (animatic 2.0)
`audio/elevenlabs_script_multilingual_v2.json` (texte, voix, réglages, départ, fenêtre, fichier cible `audio/voices_final/<CLÉ>.wav`) · `animatic/dialogue_sync_for_recording.csv` · `animatic/dialogue_sync.srt` · `timeline/LE_CARNET_276s_V1.edl` + `markers.csv` (repères de plans, base 01:00:00:00, 25 i/s). Marges : toutes les répliques tiennent dans leur plan à ×1,2 sauf P4 (−0,04 s, à compenser de 0,3 s).

## 5. Assemblage automatisé (FFmpeg) — `scripts/assemble_audio.py`
Placement des répliques (finales si présentes, sinon voix de repère), ambiances par scène (génération locale de qualité repère), musique (premier fichier de `music_library/` s'il existe), **ducking −9 dB sous la parole**, panoramique léger, normalisation −16 LUFS. Test sur voix de repère : **−16,9 LUFS intégré, crête −1,5 dBFS** (276,0 s ; `audio/MIX_276s.wav`, non versionné car lourd). Ensuite : `scripts/export_final.sh VIDEO.mp4 audio/MIX_276s.wav OUT.mp4` puis `scripts/check_delivery.py`.

## 6. Finition DaVinci Resolve Free / Fairlight (sans supposer d'accès MCP)
1. Nouveau projet 1920×1080, 25 i/s ; importer les médias (`references/**`) puis la timeline via **File → Import → Timeline → EDL** (`timeline/LE_CARNET_276s_V1.edl`) ; relier les plans par nom `SHxx` ; remplacer les images par les clips composités (SH10, SH16, SH19, SH24, SH30).
2. Page **Fairlight** : pistes **DIA** (une piste par personnage), **AMB**, **MUS**, **SFX**, bus *Dialogue* / *Ambiances+Musique* / *Master*.
3. Dialogues : EQ (coupe-bas 80 Hz, +2 dB vers 3 kHz), compresseur doux (≈ 3:1), de-esser léger ; voix radio : passe-bande 450–3 000 Hz + grain. *(Certains outils IA — isolation vocale, nivelage de dialogue — peuvent être réservés à Studio : à vérifier sur votre version.)*
4. Ambiances/musique : −30 à −22 LU sous les dialogues, **ducking** par automation ou sidechain ; silence autour de la radio (SH22) et lisibilité de la ligne du temps (SH33) ; cue sheet : `docs/SOUND_MUSIC_AND_RESOLVE_PLAN_1.0.md`.
5. Contrôle : Loudness meter −16 LUFS intégré, True Peak ≤ −1 dBTP ; écoute casque + enceinte portable ; priorité absolue à l'intelligibilité des répliques d'enfants.
6. Export : H.264 1080p25 + AAC 256 kb/s stéréo 48 kHz, < 300 s.

## 7. Prochaine autorisation à donner (non lancée)
« J'autorise le test voix : ElevenLabs Multilingual v2, répliques Y3 et A7 (73 caractères), plafond N crédits ElevenLabs » **ou** « ElevenLabs v3 via Magnific, ≤ 15 crédits Magnific ». Avant : reconnecter le connecteur ElevenLabs (solde) et confirmer le forfait commercial.
