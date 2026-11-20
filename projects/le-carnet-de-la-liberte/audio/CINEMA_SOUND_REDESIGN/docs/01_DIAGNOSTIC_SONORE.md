# 1. Diagnostic sonore — master CINÉMA FINAL (phase 1, 20/11/2026)
**Source mesurée** : `deliverables/FINAL_CINEMA/LE_CARNET_DE_LA_LIBERTE_CINEMA_FINAL_1080p.mp4` (SHA-256 `0f72fc9a…c029d`, non modifié). Mesures : `analysis/mesures_master_audio.json`, `analysis/loudness_par_plan.csv`, `analysis/voix_sources_mesures.json` ; script `scripts/measure_master_audio.py`.

## Ce que ce diagnostic est — et n'est pas
* **MESURÉ** = calculé par programme (LUFS, crêtes, spectre, corrélation stéréo, enveloppes, hauteur f0 par autocorrélation). Fiable pour les niveaux ; la hauteur f0 peut comporter des erreurs d'octave.
* **À ÉCOUTER** = hypothèse tirée des mesures, **non vérifiée à l'oreille**. **Je n'ai écouté aucun passage** (je ne peux pas entendre l'audio). Aucune appréciation de naturel, d'émotion, de diction ou de justesse des bruitages n'est donnée ici ; elles restent à votre écoute.
* Non re-mesuré ici : calage image/son (audit QC3 du 18/11 : coupes 0,02–0,10 s après leur position audio ; voix 0,06–0,17 s après le sous-titre).

## Chiffres globaux (MESURÉ)
Durée 299,000 s ; AAC stéréo 48 kHz ; −16,1 LUFS intégré ; LRA 15,8 LU ; crête vraie −1,1 dBTP ; crête échantillon −1,25 dBFS ; 0 écrêtage ; corrélation stéréo globale 0,71. Énergie par bandes (relative) : <100 Hz −19,4 dB ; 100–500 Hz −1,4 ; 500–2 k −7,0 ; 2–6 k −13,3 ; >6 k −19,5.
Sources du mix actuel : stems 276 s (dialogue mono, ambiance, musique) ; 1 seule musique (Mixkit n° 599) ; bruitages = synthèse locale (M4.1) + 9 sons Mixkit ; voix ElevenLabs (lot M2, 17/11) + Younes (« Timothée », validation provisoire).

## Constats classés
| Prio | Timecode | Constat | Nature |
|---|---|---|---|
| **P1** | **276,0 → 299,0 s** (générique) | **23 s de silence numérique** (−91 dBFS) ; la bande-son s'éteint vers 275,7 s après un fondu depuis 274 s. 7,7 % du film sans aucun son sous les cartons 1–3. | MESURÉ ; effet voulu ou non : à trancher |
| **P1** | 0–50 s, 189–239 s | Aucune musique dans l'ouverture (SH01–09), ni dans les cartons historiques/ligne du temps (SH29–33), par choix du plan « musique minimale ». Musique réellement présente (stem pré-mix) : 51–66, 109–121, 153–190, 268–275 s ≈ 71 s (24 % du film). Le repère ME (SH34, 244,8–250 s) prévu au plan est **absent** du stem mesuré (à confirmer sur le mix final). | MESURÉ ; effet émotionnel : À ÉCOUTER |
| **P1** | Plans SH01 (0–3,5), SH08 (36–39,5), SH21 (120–126), SH29 (189,5–198,5), SH31 (208,5–216,5), SH33 (225,5–239,5) | Passages sans voix à −30…−34 LUFS court terme (médiane/plan), soit **13–17 LU sous les dialogues** (≈ −16/−17 LUFS). En classe ou sur haut-parleur de téléphone, ils risquent de disparaître. | MESURÉ ; audibilité réelle : À ÉCOUTER |
| P1 | Voix de Younes (Y1–Y5 : 11,8 ; 20,8 ; 39,8 ; 253,7 ; 262,9 s) | f0 médiane mesurée **122–131 Hz**, proche des voix d'homme adulte (père 116–125 Hz) ; un enfant de 10 ans se situe d'ordinaire vers 230–300 Hz. Possible octave faussée par la mesure, **à confirmer à l'écoute**. Y3 est aussi nettement plus sombre (centroïde 1 299 Hz contre 2 000–3 500 Hz ailleurs). | MESURÉ (f0, spectre) ; crédibilité : À ÉCOUTER |
| P2 | Amina enfant vs adulte (A1/A2 vs A4–A8) | Même voix (Julia), f0 274/254 Hz (enfant) vs 225–264 Hz (adulte) : peu de différence mesurée entre 11 ans et 23 ans. A1 est plus sombre qu'A2 (centroïde 1 795 vs 2 890 Hz). | MESURÉ ; ressenti : À ÉCOUTER |
| P2 | Dialogues, tout le film | Voix **toutes mono, au centre** (corrélation 0,97–1,00 sur les plans parlés) : pas de placement ni d'espace propre à chaque lieu. Crêtes normalisées à −6,0 dBFS pour presque toutes les répliques ; niveau efficace très variable : **−20,8 à −28,2 dBFS RMS (7,4 dB d'écart)**, ex. SH15 père −25,5/−25,7 vs SH14 Amina −21,3 ; radio SH22 −28,2 ; V1 (166,5 s) −23,5/−25,9. La normalisation par crête, et non par sonie, est probablement à l'origine des écarts perçus. | MESURÉ ; réverbération/lieux : À ÉCOUTER |
| P2 | SH10–SH12 (50,5–65 s), SH20 (115,5–120 s), SH38 (270,5–276 s), SH08 | Corrélation stéréo **proche de 0 ou négative** (SH10 −0,11 ; SH11 −0,09 ; SH12 −0,18 ; SH20 −0,10 ; SH38 −0,22 ; SH08 −0,01) : risque d'affaiblissement/creux de phase en écoute **mono** (projecteur unique, téléphone). | MESURÉ ; gravité réelle : À ÉCOUTER en mono |
| P2 | Ensemble | Dynamique large : LRA 15,8 LU ; niveau court terme par plan de −34 à −15 LUFS. L'écart médian entre plans parlés et plans sans voix n'est que de 6,5 LU, mais avec des creux isolés à −30 LUFS (voir P1). | MESURÉ |
| P2 | Ambiances | Ambiances continues à −33…−45 dBFS (pré-mix), quasi inaudibles sous les voix ; presque rien à 96–100 s (−56) et 137–139 s (−58, choix « silence » de SH23). Ambiance 168–200 s plus forte (−33, foule) : cohérent avec Rabat 1955. | MESURÉ ; réalisme : À ÉCOUTER |
| P3 | Bruitages | Synthèse locale + 9 Mixkit (pages 1101–1105, pas 1270, brise 2427, oiseaux 2472, foule 364/437/462, stylo 2368/2369). Cohérence et synchro des gestes (craie 4,3 s, charnière 30,8 s, pages 56,5 s, stylo…) : **non écoutées**. Risque d'effets « synthétiques répétitifs » à vérifier. | À ÉCOUTER |
| P3 | Fin 270,5–276 s | Résolution musicale MF (268–275 s) présente puis coupure sèche à ~275,7 s vers le silence. | MESURÉ ; ressenti : À ÉCOUTER |
| P3 | Conformité technique | −16,1 LUFS, crête vraie −1,1 dBTP, aucun écrêtage : conforme YouTube/projection scolaire. Pour une salle de cinéma, le niveau intégré de −16 LUFS et les 15,8 LU de LRA ne suivent pas la pratique EBU R128 (−23 LUFS) : question de livrable, pas de défaut. | MESURÉ |

## Bilan
Aucun défaut technique « cassé » (pas d'écrêtage, pas de trou non voulu hors générique). Les vrais chantiers sont **artistiques** : musique rare et plate d'architecture (une seule piste), générique muet, passages calmes trop bas, voix sans espace et à niveaux hétérogènes, doute sur le timbre de Younes, repli mono. Ils justifient la refonte, mais l'écoute reste indispensable pour les confirmer.
