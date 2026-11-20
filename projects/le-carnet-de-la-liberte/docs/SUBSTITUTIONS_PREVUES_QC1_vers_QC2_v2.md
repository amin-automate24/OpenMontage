# Substitutions QC1 → QC2 — liste CORRIGÉE v2 (clarification utilisateur 18/11/2026) — rien n'est appliqué, aucun rendu
Remplace la v1 (`SUBSTITUTIONS_PREVUES_QC1_vers_QC2.md`, conservée). Base : `animatic/MASTER_CANDIDATE_NON_FINAL_QC1_1080p.mp4` (intact). Mix conservé : **M7B.2 (QC1)** ; M8.1 non validé, hors périmètre.

| # | Plan | QC1 | QC2 prévu | Source |
|---|---|---|---|---|
| 1 | SH13 (65,0–70,5) | fondu 0,5 s | coupe franche | `DISSOLVE` v3 |
| 2 | SH14 (70,5–77,0) | push_in_slow | travelling latéral zoom 1,06 (x 1300→1452) | `CAM[14]` v3 |
| 3 | SH15 (77,0–86,0) | push_in_slow | plan fixe zoom 1,03 | `CAM[15]` v3 |
| 4 | SH16 (86,0–91,0) | mention 30 px | mention 38 px, même texte | `make_overlay` v3 (n==16) |
| 5 | SH33 (225,5–239,5) | **durée QC1 14 s conservée** ; frise 28/44 px, apparition 1,2 s/entrée, tenue ≈ 8 s | frise v3c (dates 42 px, légendes 32 px à x=960, note 34 px) ; **apparition 1,5 s/entrée** (entrée n°6 à 8,3 s, note à 9,0 s) → vue complète stable **5 s** (9,0–14,0 s) ; textes/dates inchangés ; aucune réplique dans SH33 | `draw_overlay` v3 + pas d'apparition 1,5 s (à ajouter au script) |
| 6 | SH34 (239,5–250,0) | 10,5 s | **QC1 inchangé** (239,5–250,0) ; A8 240,5 | — |
| 7 | SH27 (175,0–180,5) | 7,0 s | **−1,5 s → 5,5 s** ; v006 + caméra recentrée + carton 42 pt (déjà QC1) | `--shot 27 175.0 5.5` |
| 8 | SH28 (180,5–189,5) | 182,0–189,5 | **début 1,5 s plus tôt → 9,0 s** (fin 189,5 inchangée) ; image LOCKED v003 ; recul 1,05→1,0 (maquette P3) | `--shot 28 180.5 9.0`, `CAM[28]` v3 |
| — | SH25 / SH26 | 151,5→163,5 / 163,5→175,0 | **QC1 intégral**, y compris caméra push_in de SH26 (pas de `CAM[26]`) ; raccord sonore : aucune correction | — |

Tous les autres plans et effets v3 (SH1, 7, 9, 18, 32 ; coupes SH7, 17, 21, 29, 31 ; autres fondus) : **QC1, non retenus**.

## Cohérence temporelle (vérifiée par calcul sur `shots_data.py` + `dialogue_timing.json`)
- 38 plans contigus, sans trou ni chevauchement ; total **276,0 s** inchangé.
- Seuls SH27 (175,0 / 5,5 s) et SH28 (180,5 / 9,0 s) changent ; SH33 14 s, SH34 10,5 s, SH25, SH26 = QC1.
- 0 réplique hors de la fenêtre de son plan ; A5 (182,5–185,2) tombe à +2,0 s dans SH28 (au lieu de +0,5 s) ; V1 166,5, A6 199,5, A8 240,5 inchangées.
- Audio M7B.2 en temps absolu : aucun recalage ; sons de foule SH27–28 (174,0–192,1 ; 176,0–183,1) restent couverts.
- Seul ajout de script requis avant rendu : pas d'apparition de la frise 1,2 → 1,5 s (SH33) ; tout le reste = paramètres existants de `build_animatic_v3.py`.
