# LE CARNET DE LA LIBERTÉ — Rendu du projet pour révision

*État au 17/11/2026 · livraison visée : vendredi 20/11/2026 · branche `claude/carnet-liberte-preproduction-b3y71m`, dossier `projects/le-carnet-de-la-liberte/`*

## 1. Le film
Court métrage éducatif d'animation 3D stylisée (France, public 9–12 ans, Maroc), **276 s (4 min 36)**, 1920×1080, H.264/AAC. Younes (10 ans) découvre le carnet de son arrière-grand-mère Amina et revit, par l'imagination, l'indépendance du Maroc (1944 → 1956). Six scènes, 38 plans (30 principaux + 8 secondaires), 5 plans en image→vidéo prévus, le reste en images fixes avec mouvements de caméra et graphiques locaux. Scénario de travail : `docs/LE_CARNET_DE_LA_LIBERTE_SCREENPLAY_DRAFT_1.2_FR.md` (le Draft 1.1 reste intact).

| Scène | Titre | Durée | Ambiance |
|---|---|---|---|
| 1 | LA QUESTION | 30 s | natural, welcoming classroom light |
| 2 | LE CARNET | 35 s | warm afternoon, natural |
| 3 | LE RÊVE DE LIBERTÉ | 55 s | warm ochre and sepia |
| 4 | LES JOURS DIFFICILES | 55 s | muted blue-gray, restrained contrast |
| 5 | LE RETOUR DE L'ESPOIR | 75 s | gradually warmer and brighter |
| 6 | L'HÉRITAGE | 26 s | natural, welcoming classroom light |

## 2. Livrables actuels
- **Animatic 2.0** : `animatic/ANIMATIC_2.0_276s.mp4` (local, ≈ 119 Mo, reconstruisible avec `scripts/build_animatic_v2.py`) et aperçu `animatic/ANIMATIC_2.0_preview_720p.mp4` (dans le dépôt). Images validées + compositions locales + voix de repère (espeak-ng, **non publiables**). Contrôle de livraison OK (`scripts/check_delivery.py`).
- Liste technique, prompts, références, plan sonore/Resolve, registre d'approbations : voir §8.

## 3. Plan par plan (source utilisée dans l'animatic 2.0)
| Plan | TC | Durée | Cadre | Source | Réplique(s) |
|---|---|---|---|---|---|
| SH01 | 00:00.0 | 3.5 s | WS | `references/p1/SH01_classe_v001.png` | — |
| SH02 | 00:03.5 | 8.0 s | MS | `references/p4/post/SH02_composite_final.png` | La Maîtresse : Les enfants, pourquoi célébrons-nous cette journée ? |
| SH03 (v005 (en validation)) | 00:11.5 | 3.5 s | MCU | `references/p4/post/SH03_gaze_head_v005.png` | Younes : Parce que le Maroc est devenu indépendant ! |
| SH04 | 00:15.0 | 5.5 s | MS | recadrage de `references/p4/post/SH02_composite_final.png` | La Maîtresse : Très bien ! Mais comment notre pays a-t-il obtenu son indépe… |
| SH05 | 00:20.5 | 7.0 s | CU | recadrage de `references/p4/post/SH03_gaze_head_v005.png` | Younes : Je… je ne connais pas toute l'histoire. / La Maîtresse : Alors, découvre-la et raconte-la-nous demain ! |
| SH06 | 00:27.5 | 2.5 s | INSERT | transition locale (craie → page) | — |
| SH07 | 00:30.0 | 6.0 s | MS | `references/p4/SH07_younes_boite_v001.png` | — |
| SH08 | 00:36.0 | 3.5 s | CU | `references/p4/post/SH08_composite_final.png` | — |
| SH09 | 00:39.5 | 11.0 s | MS 2-shot | `references/p4/SH09_younes_mere_v001.png` | Younes : Maman ! À qui appartient ce carnet ? / La Mère : À Amina, ton arrière-grand-mère. Elle a vécu les années de l… |
| SH10 | 00:50.5 | 6.0 s | CU | clip `references/p1/post/SH10_master_1080p_v001.mp4` | — |
| SH11 | 00:56.5 | 5.0 s | CU | recadrage de `references/p1/post/SH10_composite_final.png` | — |
| SH12 | 01:01.5 | 3.5 s | TRAVELLING | transition locale (encre → rue 1944) | — |
| SH13 | 01:05.0 | 5.5 s | WS | `references/p2/SH13_rue1944_v001.png` | — |
| SH14 | 01:10.5 | 6.5 s | MS 2-shot | `references/p2/SH14_amina_pere_marche_v001.png` | Amina : Papa, pourquoi tout le monde parle-t-il de liberté ? |
| SH15 | 01:17.0 | 9.0 s | MS | `references/p2/SH15_pere_explique_v001.png` | Le Père : Parce que notre pays vit sous le protectorat. Beaucoup de Ma… |
| SH16 | 01:26.0 | 5.0 s | MS | clip `references/p2/post/SH16_composite_v001.mp4` | — |
| SH17 | 01:31.0 | 8.5 s | INSERT | `references/p3/post/SH17_composite_final.png` | Le Père : Aujourd'hui, des nationalistes marocains ont présenté un doc… |
| SH18 | 01:39.5 | 9.5 s | MS 2-shot | recadrage de `references/p2/SH16_table_feuille_v001.png` | Amina : Mais que signifie être indépendant ? / Le Père : C'est pouvoir décider de l'avenir de son pays, librement et … |
| SH19 | 01:49.0 | 6.5 s | CU | clip `references/p2/post/SH19_edit_6.50s.mp4` | — |
| SH20 | 01:55.5 | 4.5 s | INSERT | transition locale (→ 1953) | — |
| SH21 | 02:00.0 | 6.0 s | WS | `references/p2/SH21_maison1953_soir_v001.png` | — |
| SH22 | 02:06.0 | 8.0 s | CU | `references/p2/SH22_radio_v001.png` | Voix Radio : Le sultan Mohammed Ben Youssef a été déposé et contraint à l… |
| SH23 | 02:14.0 | 11.5 s | MS 2-shot | recadrage de `references/p2/SH21_maison1953_soir_v001.png` | Amina : Père… est-ce que notre rêve est terminé ? / Le Père : Non, Amina. Malgré les épreuves, beaucoup de Marocains pours… |
| SH24 | 02:25.5 | 6.0 s | CU | clip `references/p2/post/SH24_composite_v001.mp4` | — |
| SH25 | 02:31.5 | 12.0 s | MONTAGE | `references/p2/SH25_fenetre_v001.png` + saisons/années (local) | — |
| SH26 | 02:43.5 | 11.5 s | MS | `references/p1/SH26_fenetre_Amina_v001.png` | Voix Hors Champ : Amina ! Le sultan revient au Maroc ! |
| SH27 | 02:55.0 | 7.0 s | WS | `references/p3/SH27_foule_rabat1955_v001.png` | — |
| SH28 | 03:02.0 | 7.5 s | MS 2-shot | `references/p3/SH28_amina_pere_foule_v001.png` | Amina : Il est revenu ! Notre espoir renaît ! |
| SH29 | 03:09.5 | 9.0 s | INSERT | `references/p3/post/SH29_composite_final.png` | — |
| SH30 | 03:18.5 | 10.0 s | CU | clip `references/p3/post/SH30_composite_v001.mp4` | Amina : Le chemin a été long. Mais nous approchons enfin de notre rê… |
| SH31 | 03:28.5 | 8.0 s | INSERT | `references/p3/post/SH31_composite_final.png` | — |
| SH32 | 03:36.5 | 9.0 s | MS 2-shot | `references/p3/SH32_pere_amina_nouvelle_v001.png` | Le Père : Amina, la France vient de reconnaître officiellement l'indép… / Amina : Tant de personnes ont espéré ce jour… |
| SH33 | 03:45.5 | 14.0 s | INSERT | graphique local (ligne du temps) | — |
| SH34 | 03:59.5 | 10.5 s | CU | `references/p3/SH34_amina_ferme_carnet_v001.png` | Amina : J'espère que les enfants de demain se souviendront de notre … |
| SH35 | 04:10.0 | 3.5 s | WS | `references/p4/SH35_classe_presentation_v001.png` | La Maîtresse : Alors Younes, qu'as-tu appris ? |
| SH36 | 04:13.5 | 8.0 s | MCU | recadrage de `references/p4/SH35_classe_presentation_v001.png` | Younes : Que l'indépendance est le résultat de longues années de lutt… |
| SH37 | 04:21.5 | 9.0 s | MS | `references/p4/post/SH37_composite_final.png` | La Maîtresse : Comment ? / Younes : En étudiant, en respectant les autres et en construisant ens… |
| SH38 | 04:30.5 | 5.5 s | WS | `references/p1/SH38_cahier_final_v001.png` + drapeau vectoriel + titre (local) | — |

## 4. Décisions validées
D1 film à 276 s · D3 mention « illustration pédagogique — non archive » · D4 note « processus territorial poursuivi après 1956 » · D5 « Reconstitution fictive » sur l'annonce radio · D6 maîtresse marocaine contemporaine · D7 carnet en français · D8 phrases d'Amina écrites, non dites · D9 montage DaVinci Resolve + cartons FFmpeg · D11 « arrière-grand-mère ». Références verrouillées : Younes (REF-01 v002), Amina (3 apparences : 1944, 1953, 1955–56), SH10, SH17, SH19, SH24, SH16, P2, P3.

## 5. Points d'attention historiques (à confirmer par un relecteur humain — aucune source externe consultée)
- Costumes d'Amina : 1944 et 1955–56 plausibles ; **1953 : foulard proche d'un hijab contemporain** (choix artistique, intérieur uniquement) ; couches de sortie (haïk/djellaba) ajoutées aux extérieurs 1944 et 1955.
- Mohammed V : aucun visage, aucune voix, aucun discours ; SH29 = trône vide symbolique ; SH31 = négociations symboliques ; mentions « reconstitution symbolique / illustration pédagogique — non archive » (SH16, SH17, SH29, SH31) ; drapeau toujours en **vecteur local**, jamais généré.
- Dates : 11/01/1944, 20/08/1953, 16/11/1955, 18/11/1955, 02/03/1956, 07/04/1956 ; la distinction 16/11 – 18/11 – 02/03 est respectée ; note territoriale ajoutée à la ligne du temps.

## 6. Budget Magnific
- **Dépensé : 2340 crédits** (36 générations d'images, dont 1 régénération SH03) ; **solde 7 818** (au 17/11) ; réserve THE LAST OF MEN ≥ 4 643 respectée ; aucun achat ni abonnement.
- Lots : échantillon 195 · correction REF-01 65 · P1 455 · P2 585 · P3 520 · P4 455 · SH03 v002 65.
- **À venir (non autorisé)** : édition IA SH03 **65** · 3 clips Kling 2.5 (SH11, SH26, SH38) **975** · voix de synthèse ≈ **308** (test ≈ 119) ou comédiens **0** · musique : piste libre vérifiée **0** ou Lyria 3 ≈ 80/clip.

## 7. Points ouverts
1. **SH03** : v005 (corrigée en local, regard mesuré à 14,0° pour une cible de 12,1°) en attente de validation visuelle ; sinon édition IA 65 crédits. **P4 reste ouvert** tant que SH03 n'est pas validé.
2. Voix françaises (choix comédiens / synthèse, droits d'usage à vérifier).
3. Trois clips animés prioritaires (975 crédits).
4. Musique licenciée et mixage final (−16 LUFS).
5. Revue historique finale ; forme officielle du drapeau.
6. Montage Resolve et export `scripts/export_final.sh` (1080p, H.264/AAC, < 5 min).

## 8. Index des fichiers
| Sujet | Fichier |
|---|---|
| Scénario | `docs/LE_CARNET_DE_LA_LIBERTE_SCREENPLAY_DRAFT_1.2_FR.md` |
| Liste technique (md/csv/json) | `shotlist/` |
| Prompts et propositions | `prompts/GENERATION_PROMPT_PACK_1.0.md`, `prompts/SH03_AI_EDIT_PROPOSAL.md` |
| Références validées | `references/` (`locked/`, `gate2_sample/`, `p1`…`p4`, `post/`) |
| Plan voix / clips / export | `docs/PLAN_VOIX_CLIPS_EXPORT_2.0.md` |
| Plan sonore et Resolve | `docs/SOUND_MUSIC_AND_RESOLVE_PLAN_1.0.md` |
| Points historiques et rythme | `docs/HISTORICAL_AND_TIMING_FLAGS_1.0.md` |
| Budget et risques | `docs/CREDIT_BUDGET_AND_PRODUCTION_RISK_REPORT_1.0.md` |
| Autorisations et dépenses | `approvals/APPROVAL_REGISTER_1.1.md`, `approval_register.json`, `generation_log.json` |
| Voix de repère / sous-titres | `animatic/dialogue_sync_for_recording.csv`, `dialogue_sync.srt` |
| Scripts | `scripts/` (`build_animatic_v2.py`, `compose_*.py`, `export_final.sh`, `check_delivery.py`) |
