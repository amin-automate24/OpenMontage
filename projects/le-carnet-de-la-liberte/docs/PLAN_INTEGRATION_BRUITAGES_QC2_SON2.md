# Plan d'intégration — bruitages candidats (QC2 SON2) — PLAN SEUL, NON EXÉCUTÉ
Statut : en attente de validation artistique écrite. Rien n'est modifié, rendu, généré ni dépensé. QC1, QC2, QC2 SON1, M9T.1, M9T.1_SH06_ATT10 et tous les mixes restent intacts ; les sorties auraient de nouveaux noms.

## Décisions retenues
SH06 = M9T.1 page −10 dB | SH12 = APRÈS | Rue 1944 = APRÈS (A1 inchangée) | Nuit 1953 = QC1 | SH26–29 = QC2 SON1 intégral.

## Base et sources
Base : `QC2_SON1/MIX_276s_QC2_SON1.wav` (= QC1 hors 163,5–193,0 s). Sources des zones : `M9T.1_SH06_ATT10/…att10.wav` (zone 1) et `M9T.1/…M9T.1.wav` (zone 2), alignées sur QC1 par le décalage constant de 47 échantillons (méthode SON1).

## Zones de raccord (temps du film)
| Zone | Contenu M9T.1 | Plein M9T.1 | Fondus (cos²/sin²) |
|---|---|---|---|
| Z1 SH06 | page Mixkit 1105 atténuée, posée 28,1–28,93 s (crête 28,446 s) | 28,10–28,93 | 27,90–28,10 et 28,93–29,13 (0,2 s) |
| Z2 SH12 + rue 1944 | brise 2427 (61,7–66,2) ; oiseaux 2472 (62,5–86,0) ; pas 1270 (65,3–77,0) ; fond −2 dB sous A1 (71,0–74,0) | 62,0–86,0 | 61,0–62,0 et 86,0–87,0 (1,0 s) |
SH12 et rue 1944 forment une seule zone car la brise (fin 66,2 s) chevauche les oiseaux (dès 62,5 s) et les pas (dès 65,3 s) : le raccord SH12 → rue 1944 (65,0 s) reste ainsi à l'intérieur de la zone, sans coupure. SH10–11 (51,3–61,5 s), SH16 (87,0 s) et le reste de 0–61 s et 87–163,5 s restent à l'identique de QC1.
Hors zones : Nuit 1953 (grillons 119–164 s) = QC1 ; 163,5–193,0 s = SON1 ; fin du film = QC1.

## Contrôles prévus (bloquants)
1. Hors Z1/Z2 : WAV identique à SON1 échantillon par échantillon.
2. Voix A1 (71–74 s) et musique B : stems inchangés (différence mesurée sur les pistes, pas seulement le mix) ; V1 et A5 à décalage 0.
3. Compensation de gain linéaire en dB après chaque zone si le loudnorm dynamique décale de ~0,4 dB (mesure sur voix/musique seules), comme pour SON1.
4. Niveaux : crête de page ≈ −11,4 dBFS ; mix global −16 LUFS ±0,3, crête ≤ −1 dBTP ; aucun clic/discontinuité aux 4 jonctions (27,90 / 29,13 / 61,0 / 87,0 s).
5. Vidéo QC2 inchangée (md5 vidéo `05f60f64…`) ; mux comme SON1 (AAC) ; sorties `QC2_SON2/MIX_276s_QC2_SON2.wav` et `MASTER_CANDIDATE_NON_FINAL_QC2_SON2_1080p.mp4` (nom neuf, rien d'écrasé).
6. Comparatif d'écoute SON1 / SON2 sur 26,5–31,5 s et 59,5–87 s, puis arrêt pour validation.

## Réserves
Éléments Mixkit non écoutés par moi (validation à l'oreille de l'utilisateur) ; licences archivées dans `approvals/licenses/SFX_LICENSES.json`, WAV non redistribués. Aucun FINAL, aucune génération, aucun crédit.
