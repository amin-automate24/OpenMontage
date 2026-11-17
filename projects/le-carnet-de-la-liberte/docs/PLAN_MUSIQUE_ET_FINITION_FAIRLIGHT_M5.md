# Plan de musique et de finition Fairlight — base M5 (préparation uniquement, 17/11/2026)

Rien n'est acheté, généré ni téléchargé. Ce plan met à jour la fiche de repères de `docs/SOUND_MUSIC_AND_RESOLVE_PLAN_1.0.md` aux timecodes du film de 276 s.

## 1. Fiche de repères musicaux (276 s)
| Repère | Plans | Timecode | Intention / règle |
|---|---|---|---|
| M1 Curiosité | SH05–06 | 0:20.5 → 0:30 | Entrée très discrète du thème |
| M2 Thème du carnet | SH07–12 | 0:30 → 1:05 | Merveille douce ; sous les voix de Y3/M1 |
| M3 Ocre 1944 | SH13–20 | 1:05 → 2:00 | Espoir, rythme léger |
| M4 Silence / tension | SH21–25 | 2:00 → 2:43.5 | Presque silence ; **aucune musique pendant la radio SH22 (2:06–2:14)** ni le silence SH23 |
| M5 Lumière | SH26 | 2:43.5 → 2:55 | Montée vers la lumière |
| M6 Joie populaire | SH27–28 | 2:55 → 3:09.5 | Célébration, tempo plus vif, sous les dialogues V1/A5 |
| M7 Mémoire | SH29–34 | 3:09.5 → 4:10 | Retour calme ; **SH33 (3:45.5–3:59.5) quasi sans musique** pour lire la ligne du temps |
| M8 Héritage | SH35–38 | 4:10 → 4:36 | Résolution du thème ; fin tenue sur le drapeau ; voix de Younes sur Y4/Y5 sans musique dense |
Brief : oud, qanun, nay discrets, cordes douces, percussions légères ; thème simple ; sans imiter un hymne ni une pièce existante. Niveau cible : −18 à −22 LU sous les dialogues.

## 2. Sources possibles (aucune acquise)
1. **Gratuite avec preuve de licence (recommandée)** : piste libre de droits (CC0 / licence autorisant l'usage éducatif et la diffusion en ligne) déposée dans `music_library/` avec la licence archivée dans `approvals/licenses/`. Pas d'achat.
2. Génération locale (ACE-Step) : seulement si une machine adaptée est disponible ; sinon non faisable ici. À autoriser séparément.
3. Génération payante (Lyria ≈ 80 cr/clip, ElevenLabs Music écarté : trop cher) : **uniquement sur votre autorisation chiffrée**.
4. Repli sans musique : film livrable avec ambiances et bruitages seuls (M4.1/M5) ; la musique est un plus, pas un prérequis du calendrier.
Décision requise : choisir 1, 2, 3 ou 4 ; si 1, fournir ou valider les fichiers.

## 3. Finition Fairlight (DaVinci Resolve Free) — ordre de travail
1. Import : dialogues (une piste par personnage : Younes/Timothée, Amina, Père, Maîtresse, Mère, Radio, Voix hors champ), `ambience_foley_m4.wav` (ambiances/bruitages), musique si disponible, mix M5 en piste guide.
2. Dialogues : égaliser les écarts perçus à ±2 dB (Younes/Timothée ≈ 4 dB sous le Père dans les originaux) ; coupe-bas 80 Hz ; de-esser léger si sibilances ; pas de pitch/formant sur Timothée.
3. Radio : conserver la chaîne R1 v2 (passe-bande 320–3 300 Hz, compression, grain) ; contrôler l'intelligibilité au casque et sur petit haut-parleur.
4. Ambiances/musique : bus séparés, ducking −9 dB sous les voix (sidechain), fondus aux changements de scène.
5. Bus maître : limiteur true peak −1,5 dBTP ; **mesure −16 LUFS intégrés sur le film complet** (réglage final à −1 dB près), LRA surveillée.
6. Contrôles de projection : écoute sur haut-parleur de classe (mono de repli : vérifier qu'aucune voix ne disparaît) ; comparer avec M5.
7. Export (non autorisé à ce jour) : WAV 48 kHz stéréo + AAC dans le MP4 final 1080p, `check_delivery.py`.

## 4. Points liés à la projection scolaire
- Mono de repli : les voix sont centrées/peu panoramiquées, sans risque d'annulation de phase.
- La dynamique actuelle (LRA ≈ 22 LU) est élevée pour une salle de classe : prévoir une compression douce du bus maître ou un relèvement des passages calmes (nuit 1953) avant l'export.
