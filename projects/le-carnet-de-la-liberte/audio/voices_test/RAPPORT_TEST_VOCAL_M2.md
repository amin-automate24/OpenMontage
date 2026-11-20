# LE CARNET DE LA LIBERTÉ — Rapport test vocal ElevenLabs (17/11/2026)

**Statut : EN ATTENTE DE VALIDATION** — aucune autre réplique générée.

| Réplique | Personnage | Voix (Voice Library) | Texte | Fichier | Durée | Fenêtre dispo | Coût |
|---|---|---|---|---|---|---|---|
| Y3 (SH09) | Younes, 10 ans | Jules – Warm French Storyteller | « Maman ! À qui appartient ce carnet ? » | Y3_jules_m2_take1.mp3 | 2,27 s | 10,7 s | 36 car. |
| A7 (SH32) | Amina adulte | Julia – Warm French Narrator | « Tant de personnes ont espéré ce jour... » | A7_julia_m2_take1.mp3 | 2,95 s | 3,8 s | 39 car. |

- **Modèle** : ElevenLabs Multilingual v2, compte Starter actif.
- **Coût total** : 75 caractères sur un plafond autorisé de 146. Aucun achat ni dépassement ; quota mensuel de 40 000 caractères.
- **Prises** : 1 par réplique. Deux prises auraient coûté 150 caractères, au-dessus du plafond.
- **Écart** : le connecteur ne transmet pas les réglages du casting (stabilité, style, vitesse). Les voix sont donc jouées avec leurs réglages par défaut.
- **Points d'analyse** :
  - Y3 : Jules est une voix de jeune adulte, la bibliothèque n'ayant aucune voix d'enfant française. Il faut juger la crédibilité d'un garçon de 10 ans ; sinon, prévoir la conception d'une voix (Voice Design) ou un jeune comédien.
  - A7 : 2,95 s pour une fenêtre de 3,8 s, la réplique tient.
- **Droits** : voix de bibliothèque, ni clonées ni imitées. La licence commerciale du plan Starter reste à confirmer dans les conditions d'utilisation d'ElevenLabs.
- **Intégration** : une fois validés, les fichiers sont copiés vers `audio/voices_final/<KEY>.wav` puis assemblés par `assemble_audio.py` (FFmpeg, EDL DaVinci Resolve inchangés).
- **Traçabilité** : `approvals/generation_log.json` (lot VOICE_TEST_M2), Git `claude/carnet-liberte-preproduction-b3y71m`.
