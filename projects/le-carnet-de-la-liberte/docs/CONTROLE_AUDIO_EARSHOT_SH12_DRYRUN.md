# CONTRÔLE AUDIO — SH12 — ESSAI À BLANC EARSHOT (NON FINAL)
Date : 19/11/2026. Inspection seule : aucun master, mix, sous-titre, asset ni registre modifié ; aucun rendu ; aucun crédit.

## 0. Source
`LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v3_1080p.mp4` (Dropbox `FINITION_DAVINCI_2026-11-19/`, téléchargé en lecture seule, content_hash vérifié `8ab0a78e…`). Extraits décodés (AAC → PCM 24 bits), hors projet :
- SH12 seul : 61,56–65,08 s (images 1539–1627).
- Contexte SH11–SH13 : 56,56–70,60 s (coupe SH12→SH13 détectée à 65,08 s).
Mix aplati : pas de stems ; dialogue, musique et SFX ne sont pas séparables ici.

## 1. Mesures (objectives, sans modèle)
| Mesure | SH12 | SH11–13 | Film entier |
|---|---|---|---|
| Loudness intégrée (ffmpeg EBU R128 = Earshot) | −15,7 LUFS | −18,3 LUFS | −16,1 LUFS |
| Crête vraie | −4,4 dBTP | −2,9 dBTP | (−1,1 dBTP, audit QC3) |
| LRA | 0,8 LU | 5,8 LU | — |
| Écrêtage | aucun (crête −4,4 dBFS) | aucun | — |
| Silences > 0,3 s à −50 dB | 0 | 0 | — |
| Réduction mono (L+R)/2 | −22,4 LUFS (**−6,7 LU**) | −24,1 LUFS (−5,8 LU) | −19,6 LUFS (−3,5 LU) |
| Corrélation L/R moyenne | **−0,12** (72 % des trames < 0) | +0,06 | 70 fenêtres de 1 s sur 276 < 0 |
| Plancher de bruit (Earshot) | −37,3 dBFS | −33,2 dBFS | — |
| Graves 20–60 Hz (part, Earshot) | −40,1 dB | −38,5 dB | — |

Plages anti-corrélées les plus longues (s) : 60–66 (SH11–SH12), 154–159, 168–174, 270–276.

## 2. Lectures du modèle (Earshot : CLAP / AudioSet — analyse machine, PAS une écoute)
- SH12 : « musique » (AudioSet 0,54), humeur « mélancolique » (z +2,9, indicatif) ; oiseaux 0,14 ; lecture d'effets faible (z ≤ 2,0).
- SH11–13 : musique jusqu'à ~67,6 s puis section « oiseaux » ; accents forts à 62,2 s (+17 dB, note type glockenspiel) et 68,6 s (+24 dB, « pas »).
- Raccord SH12→SH13 (65,08 s) : aucun attaque sonore dans ±100 ms de la coupe (mesure de synchronisation) — constat, pas un défaut en soi pour une transition en fondu.
- Étiquettes « VOICE » sur SH12 = respirations/notes probables : SH12 n'a pas de réplique (liste des plans) ; non fiables.
- `critique` : « launch-grade », 15/17 métriques dans les plages — **référence inadaptée** (7 films de lancement commerciaux) ; ses suggestions (couche sub, élargir les graves) ne s'appliquent pas à ce film.

## 3. Propositions (non appliquées)
1. **Compatibilité mono (important à vérifier)** : SH12 perd 6,7 LU en mono et sa corrélation est négative ; le film perd 3,5 LU. Sur une enceinte mono de classe, la musique/ambiance de ces plages peut s'effacer. Vérifier à l'écoute sur une enceinte mono ; si confirmé, réduire la largeur stéréo des pistes musique/ambiance concernées dans le projet Fairlight (pas sur le master).
2. Aucune correction de niveau, d'écrêtage ni de silence nécessaire sur SH12 (mesures dans les tolérances de l'audit QC3).
3. Dialogue : non évaluable sur SH12 (aucune réplique) ; le rapport voix/fond reste celui de l'audit QC3 (stems pré-mix).

## 4. Limites
Aucune écoute perceptive : je n'entends pas l'audio. Les étiquettes du modèle sont des indices (≈ 1 erreur sur 5 pour l'humeur). Mesures faites sur l'AAC décodé du master, pas sur les stems.
