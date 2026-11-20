# Substitutions prévues QC1 → QC2 (LISTE SEULE — rien n'est appliqué, aucun rendu) — 18/11/2026
Base : `animatic/MASTER_CANDIDATE_NON_FINAL_QC1_1080p.mp4` (intact). Script de rendu futur : `scripts/build_animatic_v3.py` (paramètres ci-dessous). Durée totale inchangée : 276 s.

| # | Plan | QC1 | À substituer | Source / paramètre |
|---|---|---|---|---|
| 1 | SH13 (65,0–70,5) | fondu 0,5 s depuis SH12 | coupe franche | `DISSOLVE` v3 (13 absent) |
| 2 | SH14 (70,5–77,0) | push_in_slow | travelling latéral lent zoom 1,06, centre x 1300→1452 | `CAM[14]` v3 |
| 3 | SH15 (77,0–86,0) | push_in_slow | plan fixe zoom 1,03 centré | `CAM[15]` v3 |
| 4 | SH16 (86,0–91,0) | mention « non archive » 30 px | mention 38 px, même texte, bandeau 962–1052 | `make_overlay` v3 (n==16) |
| 5 | SH33 (225,5–236,5, 11,0 s) | 14,0 s, frise 28/44 px | frise v3c : dates 42 px, légendes 32 px à x=960, note 34 px ; **−3,0 s** | `draw_overlay` v3 (n==33) + `--shot 33 225.5 11.0` |
| 6 | SH34 (236,5–250,0, 13,5 s) | 239,5–250,0 (10,5 s) | début 3,0 s plus tôt, fin inchangée (250,0) ; A8 (240,5) et carnet refermé (248,3) restent en place | `--shot 34 236.5 13.5` |
| 7 | SH27 (175,0–180,5, 5,5 s) | 7,0 s | **−1,5 s** ; v006 (portrait droit) + caméra recentrée conservés ; carton 42 pt | `--shot 27 175.0 5.5` |
| 8 | SH28 (180,5–189,5, 9,0 s) | 182,0–189,5 (7,5 s) | début 1,5 s plus tôt, fin 189,5 inchangée ; image LOCKED v003 ; recul 1,05→1,0 | `--shot 28 180.5 9.0`, `CAM[28]` v3 |
| — | SH25 / SH26 | 151,5→163,5 / 163,5→175,0 | **AUCUNE** (P4 rejetée) : durées et images QC1, y compris caméra push_in de SH26 (ne pas appliquer `CAM[26]`) | — |

Inchangés (non examinés, non approuvés) — rester QC1 : tous les autres plans et les autres effets v3 (`CAM` SH1, 7, 9, 18, 32 ; coupes à la place des fondus des SH7, 17, 21, 29, 31 ; fondus conservés SH6, 12, 20, 25, 27, 35).
Audio : M7B.2 (QC1) inchangé ; M8.1 (sons Mixkit) non décidé, hors substitutions. Les repères audio sont en temps absolu : aucune réplique ne bouge (V1 166,5 ; A5 182,5 ; A6 199,5 ; A8 240,5).
Points à confirmer avant rendu : (a) P2 inclut le raccourcissement de SH33 (−3 s) ; (b) la maquette P3 montrait SH26 avec un recul de caméra, non retenu ici (SH26 = QC1).
