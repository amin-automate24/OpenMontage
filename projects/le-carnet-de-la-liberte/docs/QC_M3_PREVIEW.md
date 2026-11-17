# QC ciblé — aperçu M3 (NON FINAL), 17/11/2026

Contrôles faits : 25 répliques toutes dans leur plan prévu, aucun chevauchement ; aucun silence numérique > 0,7 s (−45 dB) ; niveaux par réplique ≈ −15,7 LUFS sauf R1 ; avertissements historiques vérifiés sur images (SH22, SH27, SH29, SH33 + mention H4, SH38). SH03 : NON VALIDÉ, aucune conclusion sur le regard depuis un aperçu 360p.

| # | Gravité | Timecode | Problème | Correction proposée (locale, sans IA) |
|---|---|---|---|---|
| 1 | BLOQUANT | 1:31–1:39.5 (SH17), 3:28.5–3:36.5 (SH31) | Mentions « ILLUSTRATION PÉDAGOGIQUE — non archive » (SH17) et « ILLUSTRATION SYMBOLIQUE — non archive » (SH31) prévues dans shots_data mais absentes de l'image ; la feuille de SH31 porte en plus un pseudo-texte flou | Incruster la mention (sous-titre `sub`) par rendu partiel `build_animatic_v2.py --shots 17,31` + patch FFmpeg ; aucune image régénérée |
| 2 | IMPORTANT | 0:11.8, 0:20.8, 0:39.8, 4:13.7, 4:22.9 | Younes Y1–Y5 encore en voix de repère espeak (robotique) | Enregistrement humain (kit prêt) avant le 20/11 ; à défaut, livrer avec mention « voix provisoire » : décision à prendre |
| 3 | IMPORTANT | 2:06.5–2:11.6 (SH22) | R1 radio ≈ 4 dB sous les autres répliques (−19,7 vs ≈ −15,7 LUFS), filtre radio en plus | +3 dB sur R1 dans le prochain mix versionné (M4), filtre conservé |
| 4 | MINEUR | 3:41.5–3:41.7 (SH32) | P5 → A7 : 0,21 s seulement entre les deux répliques | Décider à l'écoute ; option A7 à 221,95 s |
| 5 | MINEUR | global | Mix à −17,3 LUFS (cible finale −16) | Réglage final dans Fairlight, pas avant |
