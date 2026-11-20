# Plan d'intégration sonore dans QC2 — PLAN SEUL (rien n'est appliqué, aucun rendu) — 19/11/2026
Références sonores validées SH27–29 (figées, ne plus corriger) : mix `audio/mixes/M9T2.3/MIX_276s_M9T2.3.wav` (sha256 4eb881723bd48e53…) = entrée de foule M9T2.2 + raccord SH28→SH29 M9T2.3 ; scripts `sound_design_m7c_test.py`, `music_finish_m9t23.py`, `audio_qc_m9t23.py`. Base : mix QC1 `MIX_276s_M7B.2.wav` (sha256 a7a699b682d18cdb…), identique à la piste audio de QC2.

## Portion à remplacer : film 163,5–193,0 s (raccords de 1 s aux deux bouts), tout le reste = QC1 intact
| Élément approuvé | Temps (s) | Source |
|---|---|---|
| Rumeur réelle derrière la fenêtre (SH26), indissociable de V1 APRÈS — à confirmer | 164,5–175,5 | Mixkit 364 |
| V1 : musique et rumeur −3 dB | 166,3–169,6 | gain, voix inchangée |
| Entrée de foule adoucie (M9T2.2) | 174,0–175,4 | rampe lisse, niveau établi conservé |
| Foule réelle SH27–28, acclamations −8 dB filtrées 250–3200 Hz | 174,0–188,0 | Mixkit 364 ; 462 (176,0–182,0) ; 437 (179,6–184,1) |
| Raccord SH28→SH29 (M9T2.3) : queue (cos²)^0,45, fin 190,0 s | 188,0–190,0 | gain |

## Étapes (à exécuter seulement sur autorisation)
1. Aligner M9T2.3 de −47 échantillons (≈ 1 ms de retard introduit par le limiteur ajouté dans ses scripts ; sans cela le raccord ferait un filtre en peigne) ; vérifier une corrélation > 0,99 sur des passages inchangés.
2. Caler le niveau : M9T2.3 est +0,06 dB plus fort que QC1 hors zone → −0,06 dB sur le segment.
3. Raccords équipuissance 163,5–164,5 et 192,0–193,0 ; QC1 conservé à l'échantillon près partout ailleurs.
4. Un seul encodage AAC 192 kb/s, 48 kHz stéréo depuis ce WAV (comme QC1) ; vidéo de QC2 recopiée sans réencodage (images, drapeaux, portraits identiques) → fichier proposé `animatic/MASTER_CANDIDATE_NON_FINAL_QC2_SON1_1080p.mp4`.
5. Contrôles : −16,0 LUFS ±0,1, crête vraie ≤ −1,0 dBTP, durée audio 276,0 s, voix V1 (166,5) / A5 (182,5) à décalage 0, identité à QC1 hors 163,5–193,0, absence de clic aux raccords, empreinte vidéo = QC2, `check_delivery.py`.

## Non validé — reste QC1 (non intégré)
Rue 1944 (pas, oiseaux, −2 dB sous A1) ; grillons de la nuit 1953 ; page SH06 et brise SH12 ; tout autre bruitage M8.1/M9T.1 ; SH11/SH25 et réverbérations (écartés). Voix, musique B, silences : inchangés.

## Risques
Sons Mixkit non écoutés par l'assistant (licences archivées : 364, 462, 437) ; une écoute humaine de 163,5–193,0 s est requise après intégration ; léger écart AAC possible hors zone (second encodage depuis le WAV d'origine, pas depuis l'AAC de QC1).
