# APPROVAL REGISTER 1.1 — LE CARNET DE LA LIBERTÉ (mise à jour 16/11/2026)

Règles inchangées : une approbation écrite par étape ; l'une n'autorise jamais la suivante ; une notification automatique n'est jamais une approbation.

## Décisions approuvées (message utilisateur du 16/11/2026)
| ID | Décision | Appliquée |
|---|---|---|
| D1 | Film à 276 s (scène 6 = 26 s) | ✅ liste de plans, animatic 1.1, scénario 1.2 |
| D3 | Mention « illustration pédagogique — non archive » | ✅ (SH17, 29, 31) |
| D4 | Note « processus territorial poursuivi après 1956 » | ✅ pied de la ligne du temps (SH33) |
| D5 | Mention « Reconstitution fictive » sur l'annonce radio | ✅ SH22 |
| D6 | Maîtresse marocaine contemporaine | ✅ fiche/prompts à valider en GATE 2 suivante |
| D7 | Carnet en français | ✅ |
| D8 | Phrases d'Amina écrites mais non dites | ✅ (silencieuses) |
| D9 | Montage Resolve ; cartons en FFmpeg/Remotion (selon recommandation) | ✅ pas d'installation lancée |
| D11 | Généalogie harmonisée : « arrière-grand-mère » | ✅ Draft 1.2 (le 1.1 reste intact, SHA inchangé) |
| D2 | Scénario B (5 515 cr) = **référence budgétaire seulement**, pas une autorisation globale. **Réserve THE LAST OF MEN ≥ 4 643 cr** | ✅ enregistrée |
| D10/D12 | Préparer test de voix et musique sous licence **sans dépense** | ✅ `docs/VOICE_TEST_PLAN_1.0.md`, `docs/MUSIC_LICENSE_PLAN_1.0.md` |

## Portes
| Porte | Statut | Détail |
|---|---|---|
| GATE 1 Références historiques/visuelles | Décisions approuvées ; références historiques humaines (H5) toujours à fournir | — |
| **GATE 2 Images** | **Partiellement accordée : échantillon de 3 images, plafond 195 cr** — **exécutée et épuisée** | REF-00 style, REF-01 Younes, REF-02 Amina ; 3 × 65 = **195 cr** ; en attente de **validation visuelle** |
| GATE 2 suite (autres images) | ⏳ Non accordée | — |
| GATE 3 Image→vidéo | ⏳ Non accordée | — |
| GATE 4 Audio final et post | ⏳ Non accordée | — |

## Registre des dépenses
| Date | Poste | Crédits | Solde Magnific |
|---|---|---|---|
| 16/11 avant | — | 0 | 10 158 |
| 16/11 | REF-00 style board (Nano Banana 2.1, 2k, 16:9) | 65 | — |
| 16/11 | REF-01 Younes | 65 | — |
| 16/11 | REF-02 Amina | 65 | **9 963** (vérifié) |
| **Total projet** | | **195 / 195 autorisés** | Réserve THE LAST OF MEN : 9 963 disponibles, ≥ 4 643 intouchables |

Aucune marge de reprise : toute régénération d'une référence exige une nouvelle autorisation.

## Mise à jour — correction REF-01
| Date | Autorisation | Poste | Crédits | Solde |
|---|---|---|---|---|
| 16/11 | AUTH-03 : correction de REF-01 (tenue de Younes) uniquement | REF-01 v002 | 65 | **9 898** (calculé : 9 963 − 65) |
Total projet : **260 cr**. REF-00 et REF-02 non touchées. Aucune autre génération autorisée.

## Validation — REF-01 v002 VERROUILLÉE (16/11)
Référence officielle de Younes pour tous les futurs plans (visage, coiffure, expressions, proportions, tenue). SHA-256 `0a5f8b74532b10bf…`. v001 conservée, remplacée. 0 génération, 0 crédit.

## Amina — sélections présentées (non verrouillées)
REF-02 examinée seule : enfant 11 ans (A) et adulte 20–23 ans (B : 1953 gris-bleu / 1955-56 chaud) extraits sans régénération (`references/gate2_sample/selections/`). En attente de validation ; 0 crédit.

## Validation — Amina VERROUILLÉE (16/11), 3 apparences
- 1944 enfant 11 ans, robe ocre, foulard crème — `references/locked/AMINA_1944_enfant_v001.png` — SHA-256 `2f8b8712991a063c9561a578691197faedb20ce1a228c37d803a6e248cd99d2e`
- 1953 adulte, robe gris foncé, foulard bleu-gris — `references/locked/AMINA_1953_adulte_v001.png` — SHA-256 `ff935ef0f95383e833f30e22f5e0fb1e5a2c5e3e9cd0b59d763d700dab57712d`
- 1955-56 adulte, tenue ocre à motifs, foulard crème — `references/locked/AMINA_1955-56_adulte_v001.png` — SHA-256 `d70efc6d3651502f667e8037bdc8bdbf1be654fc40a816ea16aa8651a148bd98`
- Source REF-02 intacte — SHA-256 `e27572942ae2c3f5dc8a65520f870b2195a18096a282ae999fcf85562500add7`
Usage final des costumes **soumis à revue historique H12** (voir docs/HISTORICAL_AND_TIMING_FLAGS_1.0.md). 0 génération, 0 crédit.

## AUTH-04 — Lot P1 (16/11) : 7 images × 65 = **455 / 455 cr**, aucune reprise
REF-03 père, REF-04 maîtresse, E4 intérieur 1940s, SH01, SH10, SH26, SH38 (`references/p1/`, ids dans `generation_log.json`). Références utilisées : Younes REF-01 v002, Amina 1955-56 verrouillée, REF-00 style. Statut : **en attente de validation visuelle**. Total projet : 715 cr ; solde attendu 9 443 (à vérifier). P2–P4, clips, audio : non autorisés.

## SH10 VERROUILLÉ (16/11) — composition et inscriptions validées
- base_image: `references/p1/SH10_carnet_Younes_v001.png` SHA-256 `6644309ff5348d56…`
- composite_final: `references/p1/post/SH10_composite_final.png` SHA-256 `6b5fb88a117e61ed…`
- text_layer: `references/p1/post/SH10_text_layer_final.png` SHA-256 `136f6e094aff7b21…`
- composite_clip: `references/p1/post/SH10_composite_v001.mp4` SHA-256 `9b3cddca847436d4…`
- master_1080p: `references/p1/post/SH10_master_1080p_v001.mp4` SHA-256 `2f14f92463a20a17…`
Recomposition finale : `scripts/compose_sh10.py --master` (1080p depuis la source 2752×1536, lecture stable 1,8 s). 0 génération, 0 crédit.

## AUTH-05 — Lot P2 (16/11) : 9 images × 65 = **585 / 585 cr**, aucune reprise
- SH13_rue1944_v001 — `references/p2/SH13_rue1944_v001.png` — SHA-256 `bcc61d956b76cdf8…`
- SH14_amina_pere_marche_v001 — `references/p2/SH14_amina_pere_marche_v001.png` — SHA-256 `95ee6a0cd25f522c…`
- SH15_pere_explique_v001 — `references/p2/SH15_pere_explique_v001.png` — SHA-256 `c2a0326d4854a3e3…`
- SH16_table_feuille_v001 — `references/p2/SH16_table_feuille_v001.png` — SHA-256 `37a7a829929027c7…`
- SH19_amina11_ecrit_v001 — `references/p2/SH19_amina11_ecrit_v001.png` — SHA-256 `9a9643c1e041a62a…`
- SH21_maison1953_soir_v001 — `references/p2/SH21_maison1953_soir_v001.png` — SHA-256 `ea3d760592243438…`
- SH22_radio_v001 — `references/p2/SH22_radio_v001.png` — SHA-256 `07724d672a418aa4…`
- SH24_amina20_ecrit_v001 — `references/p2/SH24_amina20_ecrit_v001.png` — SHA-256 `b59fce091dae64b0…`
- SH25_fenetre_v001 — `references/p2/SH25_fenetre_v001.png` — SHA-256 `7e7a855d6bdfebc3…`
Références : REF-00 style, Amina 1944 / 1953 verrouillées, père REF-03, E4. SH14–15 ont SH13 pour décor. Statut : **en attente de validation groupée**. Total projet : 1 300 cr ; solde attendu 8 858 (à vérifier). Rue et djellaba d'extérieur = reconstitution fictive à confirmer (H12), non authentifiée. P3/P4, clips, audio : non autorisés.

## P2 VERROUILLÉ artistiquement (16/11), sous réserve du contrôle historique final
Images P2 : empreintes dans `generation_log.json` et `approval_register.json`. Inscriptions locales (SH16 manifeste en illustration pédagogique, SH19, SH24) : `references/p2/post/` (clips, calques, SHA-256 enregistrés). Originaux intacts. **P3 préparé** (`prompts/P3_PREPARED_NOT_EXECUTED.md`, 520 cr), non autorisé. 0 génération, 0 crédit.

## P2 — correction typographique SH16/SH19 (16/11)
Textes redessinés à la résolution 1080p (nets, en perspective, hors reliure/bords) ; SH24 inchangé ; empreintes mises à jour dans `approval_register.json`. 0 génération, 0 crédit.

## P2 CLOS (16/11) après contrôle technique
9/9 empreintes d'images conformes ; clips SH16/SH19/SH24 en 1920×1080 25 i/s ; SH16 et SH24 conservés ; SH19 : texte replacé (ancienne version gardée). **P3 préparé** (520 cr, `prompts/P3_PREPARED_NOT_EXECUTED.md`), non autorisé. Total projet : 1 300 cr, solde 8 858.

## SH19 — correction finale (16/11)
Texte relevé et recentré ; marge basse mesurée ≥ 15.3 % et haute ≥ 21.2 % de la hauteur utile sur toute la vidéo (108 images, contrôle automatique + vérification visuelle à 2,0/3,0/4,5/6,4 s, 1920×1080). Versions précédentes préservées. 0 génération, 0 crédit.

## SH19 VALIDÉ DÉFINITIVEMENT (16/11)
Apparition partielle de « SERA LIBRE. » = balayage d'écriture gauche→droite intentionnel (2,4→3,4 s) ; phrase complète et non déformée dès 3,4 s ; lisible 3,08 s (≥ 2 s). P2 reste clôturé. 0 génération, 0 crédit.

## SH19 / P2 CLÔTURÉS DÉFINITIVEMENT (16/11)
Montage : `SH19_edit_6.50s.mp4` (case 109,0–115,5 s remplie exactement), phrase complète maintenue 3,1 s (≥ 2 s). Fichiers d'origine conservés. **P3 prêt** : 8 images, 520 cr, solde après P3 = 8 338 (réserve THE LAST OF MEN ≥ 4 643 respectée). Non autorisé, non lancé.

## AUTH-06 — Lot P3 (16/11) : 8 images × 65 = **520 / 520 cr**, aucune reprise
- SH17_document_illustre_v001 — `references/p3/SH17_document_illustre_v001.png` — SHA-256 `499cdb3f4253fd09…`
- SH27_foule_rabat1955_v001 — `references/p3/SH27_foule_rabat1955_v001.png` — SHA-256 `6a602c3e57ebd03a…`
- SH28_amina_pere_foule_v001 — `references/p3/SH28_amina_pere_foule_v001.png` — SHA-256 `11a1a9c907036636…`
- SH29_trone_symbolique_v001 — `references/p3/SH29_trone_symbolique_v001.png` — SHA-256 `cedc13365acc9ad2…`
- SH30_amina_ecrit_1955_v001 — `references/p3/SH30_amina_ecrit_1955_v001.png` — SHA-256 `02c661c9a4617e62…`
- SH31_negociations_symboliques_v001 — `references/p3/SH31_negociations_symboliques_v001.png` — SHA-256 `958c57822b9a0d18…`
- SH32_pere_amina_nouvelle_v001 — `references/p3/SH32_pere_amina_nouvelle_v001.png` — SHA-256 `820f22ee0e952cd0…`
- SH34_amina_ferme_carnet_v001 — `references/p3/SH34_amina_ferme_carnet_v001.png` — SHA-256 `351fd5aa9781638d…`
Aucun drapeau généré (mâts vides, vectoriel en post) ; aucun visage du souverain ; SH17/29/31 = illustrations pédagogiques, non archives. Statut : **en attente de validation groupée**. Total projet : 1 820 cr ; solde attendu 8 338 (à vérifier). P4, clips, audio : non autorisés.

## P3 — validation artistique + corrections locales (16/11)
Validés : SH27, SH28, SH30, SH32, SH34. SH29/SH31 : mention « RECONSTITUTION SYMBOLIQUE — sans valeur documentaire » (SH31 : pseudo-texte et fausse signature IA masqués). SH17 : pseudo-texte IA masqué ; inscription « PARTI DE L'ISTIQLAL » + « Demande d'indépendance du Maroc » (description, pas une citation ; pas de date pour éviter la répétition avec SH16) ; mention illustration pédagogique. SH30 : « Le chemin a été long. » (clip 10 s). Originaux intacts ; empreintes dans `approval_register.json`. 0 génération, 0 crédit. En attente de validation groupée.

## P3 — contrôle (16/11)
SH29/SH31 validés. SH17 : inscription pédagogique « Manifeste de l'indépendance — 11 janvier 1944 » + mention de reconstitution (version Istiqlal conservée). SH30 : cohérent avec le scénario et le minutage, inchangé. 0 génération, 0 crédit.

## SH17 VERROUILLÉ — P3 CLOS (16/11)
SH17 (Manifeste de l'indépendance — 11 janvier 1944 + mention pédagogique) validé ; original conservé. Contrôle technique : 8/8 images, 520 cr, empreintes OK, sorties 1080p, SH30 ['1920,1080,25/1,250', '10.000000']. SH29/SH30/SH31 conformes. Total projet 1 820 cr, solde 8 338. P4, clips, audio : non autorisés.

## AUTH-07 — Lot P4 (17/11) : 7 images × 65 = **455 / 455 cr**, aucune reprise
- SH02_maitresse_tableau_v001 — `references/p4/SH02_maitresse_tableau_v001.png` — SHA-256 `0ccaca3781fe712f…`
- SH03_younes_main_levee_v001 — `references/p4/SH03_younes_main_levee_v001.png` — SHA-256 `347cd8afe41fbe79…`
- SH07_younes_boite_v001 — `references/p4/SH07_younes_boite_v001.png` — SHA-256 `0d433d6d7d31534f…`
- SH08_carnet_couverture_v001 — `references/p4/SH08_carnet_couverture_v001.png` — SHA-256 `ce5fa0640ea9c7a8…`
- SH09_younes_mere_v001 — `references/p4/SH09_younes_mere_v001.png` — SHA-256 `ef8775ee0bd30c6b…`
- SH35_classe_presentation_v001 — `references/p4/SH35_classe_presentation_v001.png` — SHA-256 `302fec6117746000…`
- SH37_maitresse_younes_cahier_v001 — `references/p4/SH37_maitresse_younes_cahier_v001.png` — SHA-256 `1ffd610f3979b40d…`
Références : style REF-00, Younes REF-01 v002, maîtresse REF-04, classe SH01, carnet SH10 ; la mère est créée dans SH09 (fictive). SH07 sert de décor à SH08/SH09. Tableau et couverture du carnet laissés vierges (textes en post). Statut : **en attente de validation groupée**. Total projet : 2 275 cr ; solde attendu 7 883 (à vérifier). Clips, audio : non autorisés.

## P4 — validation artistique + corrections locales (17/11)
SH02 : inscription à la craie ; SH08 : titre sur la couverture ; SH37 : gros plan local (classe en profondeur de champ, cartable hors focus) pour la continuité avec SH35 (classe pleine, inchangé). Originaux intacts, empreintes dans `approval_register.json`. 0 génération, 0 crédit. En attente de validation et clôture.

## AUTH-08 — SH03 v002 (17/11) : 1 régénération × 65 = **65 cr** (aucune reprise)
Correction locale impossible (Younes face caméra, tableau derrière lui). v002 : regard et visage vers le tableau/la maîtresse ; v001 conservée ; SHA-256 `f56c8a350aa01fb9…`. Total projet : 2 340 cr ; solde attendu 7 818 (à vérifier). En attente de validation.

## SH03 — correction locale du regard v003 (17/11)
Iris de l'œil proche déplacé vers le haut-gauche (vers le visage de la maîtresse), ancienne zone reconstruite, paupières respectées ; identité, tenue, main levée, cadrage et décor inchangés ; v001 et v002 conservées. 0 génération, 0 crédit (total projet 2 340, solde 7 818). En attente de validation.

## SH03 — v004 (17/11) : inclinaison locale de la tête + regard
Tête et cheveux pivotés de 6° (menton vers le haut, vers la maîtresse), fond reconstruit, iris déjà décalés (v003). Limites : inclinaison dans le plan uniquement ; fine ligne de raccord à gauche du front et minuscule éclat au bout du nez visibles seulement en zoom. v001/v002/v003 conservées. 0 génération, 0 crédit. En attente de validation.

## Reprise prioritaire (17/11)
Animatic 2.0 (276,0 s, 1080p H.264/AAC, contrôle de livraison OK) : toutes les images et compositions validées intégrées ; voix de repère. P4 clos sauf SH03 (édition IA 65 cr proposée, non lancée). Voix, 3 clips (975 cr), musique : plan et coûts dans `docs/PLAN_VOIX_CLIPS_EXPORT_2.0.md` ; rien n'est lancé. 0 crédit dépensé dans cette étape (total projet 2 340, solde 7 818).

## SH03 v005 (17/11) — correction locale calibrée par mesure
Regard mesuré : v002 18,6° / v004 35,8° (dépassement) / **v005 14,0° pour une cible de 12,1°** (direction pupille→visage de la maîtresse). Tête inclinée de 4°, paupière restaurée. v001 = original conservé (non modifié par conception). Animatic 2.0 mis à jour (SH03/SH05). P4 reste **ouvert** jusqu'à validation visuelle. 0 génération, 0 crédit ; édition IA (65 cr) toujours proposée, non autorisée.

## Audio 2.0 (17/11) — préparation
Casting FR, script ElevenLabs Multilingual v2 par réplique, 2 répliques test (Y3, A7), EDL/repères Resolve, assemblage FFmpeg (test −16,9 LUFS). Solde ElevenLabs non vérifiable (permissions) ; Multilingual v2 absent de Magnific. **0 génération, 0 crédit.** Prochaine autorisation : test voix (voir `docs/AUDIO_CASTING_ET_MIX_2.0.md` §7).

## SH03 v006 (17/11) — préparée, NON VALIDÉE
Retouche locale de v005 (script `scripts/fix_sh03_v006.py`, 0 crédit, 0 génération) : bavure du bout du nez et raccord du mur à gauche du front uniquement ; yeux, sourcil, peau, bouche, cheveux vérifiés identiques (écart 0). Fichiers : `references/p4/post/SH03_gaze_head_v006.png` (+ `_1080p`), comparaison `references/p4/control/SH03_compare_v005_v006.png`. v005 intacte. En attente de votre validation visuelle. Voix de Younes : audition Y1/Y3 et kit d'intégration préparés ; repli Gaspard Chevallier non généré.

## SH03 v006 — VERROUILLÉE (17/11)
Décision de l'utilisateur : v006 retenue comme version candidate finale ; contrôle 1080p (planche `SH03_preview_1080p_v005_v006_face.png` + plan complet) : retouche discrète, regard vers la maîtresse visuellement acceptable. **Référence retenue pour le montage final** : `references/p4/post/SH03_gaze_head_v006.png` — SHA-256 `6420f9c99267a5f04b8f3617bc1280ec175c4f1f9c8965118fcd163e5f2f3e4a`. Préservées : v005 `9a4fdd3dd4d5ffb9…`, v001 `347cd8afe41fbe79…` (inchangées). P4 clos. 0 crédit. Animatic existant non re-rendu (SH03 v006 sera intégrée au prochain rendu demandé).

## Musique (17/11) — candidate B, NON VALIDÉE
Option B « Possible Dreams » (Eugenio Mininni, Mixkit) = candidate prioritaire, non validée ; option A « A Peaceful World » et M6.1 (sans musique) conservés. Repères MA, MB, MC→MD (prise continue), MF ; **ME supprimé** ; aucune musique sur SH22, SH23, SH29–33 (vérifié : niveau musical nul sur ces zones). Licence : Mixkit Stock Music Free License, texte + page archivés (`approvals/licenses/`), SHA-256 des fichiers vérifiés. **Restrictions** : projection scolaire et diffusion en ligne autorisées ; DVD/CD, TV/radio, Content ID interdits. 0 € dépensé. Aucun master FINAL avant validation artistique et écoute complète (aperçu `audio/mixes/M7B/ECOUTE_COMPLETE_M7B_NON_FINAL_360p.mp4`).

## Musique B — candidat M7B.1 (17/11), NON FINAL
Décision utilisateur : option B retenue comme base de finition (MA, MB, MC→MD, MF ; ME supprimé). M7B.1 = transitions électroniques atténuées, foule/musique/dialogues rééquilibrés (SH27–28), sortie musicale du titre adoucie (cos² 5 s). Détails : `audio/mixes/M7B.1/NOTES_M7B.1.md`. M6.1 sans musique, M7A, M7B et licence Mixkit archivée préservés. 0 € ; aucun master FINAL ni publication avant validation.

## SH27/SH28 v002 — drapeaux (17/11), préparation locale, NON VALIDÉE
Sur copies (`references/p3/post/SH27_flags_v002.png`, `SH28_flags_v002.png` ; originaux v001 inchangés, SHA-256 vérifiés) : 5 drapeaux vectoriels sur les perches existantes de SH27, 3 en arrière-plan de SH28 (`scripts/compose_sh27_sh28_flags.py`). Comparaisons 1080p : `references/p3/control/COMPARAISON_SH2*_*.jpg`. 0 crédit, aucune génération. **Portraits** : maquette SH27 avec 2 cartes à panneaux gris neutres (aucun visage), `SH27_maquette_portraits_PLACEHOLDER_v002.png` ; la photographie de Mohammed V (≈1953, Commons/Nationaal Archief-Anefo, CC0 annoncée) n'est PAS utilisée : provenance et licence non vérifiées (Wikimedia 429), voir `references/p3/historical_sources/MOHAMMED_V_1953_PROVENANCE_STATUS.md`. La règle « aucun visage de Mohammed V » est levée par l'utilisateur uniquement pour une photographie authentique vérifiée. Aucun remplacement dans le montage.

## SH27/SH28 v003 — portraits photographiques authentiques (17/11), préparation locale, NON VALIDÉE
Photo : Nationaal Archief / Anefo, bestanddeelnummer 905-8914 (≈ 18/08/1953), CC0 1.0 (fiche Commons archivée, JPG archivé et empreinte SHA-256 vérifiée par le script) — `references/p3/historical_sources/`. Compositing local sur copies : `references/p3/post/SH27_flags_portraits_v003.png` (2 portraits) et `SH28_flags_portraits_v003.png` (1 portrait en arrière-plan), drapeaux v002 conservés ; v001, v002 et le master inchangés ; transformations géométriques seules sur la photo (aucune génération ni retouche du visage). Comparaisons 1080p : `references/p3/control/COMPARAISON_SH2*_v003_1080p.jpg`. Les portraits apparaissent comme des photographies dans une reconstitution fictive, non comme une archive de la foule. 0 crédit. Aucune intégration au master avant nouvelle validation.

## 2026-11-17 — SH27/SH28 micro-ajustement v004 (portraits) — NON VALIDÉ
- Source : v002 drapeaux + photo archivée Anefo 905-8914 (CC0), transformations géométriques seules ; visage non modifié ; aucun crédit IA.
- SH27 v004 : cartes relevées sur murs/arrière-plan (pixels modifiés dans la zone foule : 123 977 → 49 996) ; visages de la foule dégagés ; drapeaux intacts.
- SH28 v004 : portrait élargi 105→140 px, reste en arrière-plan.
- v003 conservée (non écrasée). Comparaisons : references/p3/control/COMPARAISON_SH27_v003_v004_1080p.jpg, COMPARAISON_SH28_v003_v004_1080p.jpg.
- Recommandation : valider v004 (en attente de l'accord écrit). Aucune intégration au master, aucun export final.

## 2026-11-17 — SH27/SH28 v003 VALIDÉES par l'utilisateur (verrouillage)
- Validé : SH27_flags_portraits_v003.png, SH28_flags_portraits_v003.png (v004 non retenue, conservée).
- Verrouillées : references/locked/SH27_flags_portraits_v003_LOCKED.png (sha256 be6abc15…), SH28_flags_portraits_v003_LOCKED.png (sha256 877d5b38…), lecture seule, copies identiques aux v003.
- scripts/build_animatic_v2.py : SH27/SH28 pointent vers les LOCKED ; options --out-name/--report-name (refus si fichier existant).
- Rendu de contrôle NON FINAL en cours (nouveaux noms, aucun écrasement). 0 € ; aucune IA ; aucun export final sans accord explicite.

## 2026-11-17 — Master candidat M7B.1 + SH27/SH28 v003 — NON FINAL
- Local : animatic/MASTER_CANDIDATE_NON_FINAL_M7B.1_SH27-28_v003_1080p.mp4 (127 892 399 o, SHA-256 1988fc0da018ac4f…b5fca) + MASTER_CLEAN_1080p_video_prep_SH27_28_v003.mp4 ; anciens masters intacts. QC : docs/QC_MASTER_CANDIDATE_M7B.1_SH27-28_v003.md.
- Dropbox (déposé sur demande, vérifié par content_hash + SHA-256 après re-téléchargement) : /LE_CARNET_DE_LA_LIBERTE/MASTER_CANDIDATE/{MASTER_CANDIDATE_NON_FINAL.mp4, MASTER_CANDIDATE_NON_FINAL_FR.srt, QC_MASTER_CANDIDATE_NON_FINAL.md}.
- 0 € ; aucune IA ; aucun FINAL ni publication. Validation explicite requise.

## 2026-11-17 — Corrections QC1 (autorisées) — MASTER_CANDIDATE_NON_FINAL_QC1 — NON FINAL
- SH27 : SH27_flags_portraits_v006.png (portrait droit −50 px, même photo d'archive, aucun visage modifié ; v005 écartée car elle masquait un drapeau) + caméra SH27 recentrée +80 px ; carton ajusté à 42 pt (tient dans son bandeau). SH28 v003 LOCKED inchangée.
- SH29 : guillemets retirés, texte identique.
- Audio M7B.2 (depuis M7B.1, automation de gain uniquement) : 169–182 s −2,3 dB ; passages calmes SH10–12 et SH33 relevés (min −36,5→−31,5 et −39,0→−33,7 LUFS). Master : −16,0 LUFS, crête −1,1 dBTP, LRA 15,8 LU.
- SRT : animatic/SUBTITLES_FR_QC1.srt (32 sous-titres, ≤ 41 car./ligne, 0 chevauchement, fin ≤ voix +0,8 s, texte identique ; 3 sous-titres > 17 car./s, imposés par le débit de la voix).
- Fichier : animatic/MASTER_CANDIDATE_NON_FINAL_QC1_1080p.mp4 (SHA-256 dc63810a…8023), check_delivery OK. Masters précédents préservés. 0 € ; aucune IA ; aucun FINAL.

## 2026-11-18 — Révision Work : maquettes P2–P4 (NON FINALES, non appliquées)
- SH12–16 APRÈS (v3) : retenu comme candidat approuvé visuellement (décision utilisateur) ; préservé.
- P2 SH33–34 : frise v3c (dates 42 px / légendes 32 px à x 960, aucun contact, 2 mars 1956 dans le cadre), textes et dates inchangés ; SH33 225,5–236,5 (11 s), SH34 236,5–250,0 ; A8 inchangée (240,5).
- P3 SH27 raccourci de 1,5 s : SH27 175,0–180,5 ; SH28 180,5–189,5 ; V1 (166,5) et A5 (182,5) inchangés ; portraits (photo archivée Anefo 905-8914), drapeaux et carton intacts.
- P4 SH25 sortie 1,5 s plus tôt : SH25 151,5–162,0 ; SH26 162,0–175,0 ; V1 (166,5) inchangée ; musique MC→MD inchangée ; dernière page sonore de SH25 (162,3 s) déborde de 0,3 s sur SH26, à recaler si validé.
- Durée totale 276 s inchangée ; QC1 et références verrouillées intacts ; 0 € ; aucune IA.

## 2026-11-18 — Décisions Work : P2/P3 retenues, P4 non validée
- P2 SH33–34 (frise corrigée v3c) : RETENUE, candidate visuellement validée ; frise figée (plus de modification).
- P3 SH27/28 : RETENUE comme candidate visuelle. Traçabilité vérifiée sans recherche : photo Anefo 905-8914 (SHA-256 3f2c5ece…d48d31, CC0 1.0, oldid 1257609662) archivée dans references/p3/historical_sources/ ; script compose_sh27_sh28_portraits.py contrôle l'empreinte.
- P4 SH25/26 : NON VALIDÉE. Extrait complet SH25 (fin) / SH26 / SH27 (début), film 156–181 s : animatic/remontage_v3/COMPARAISON_P4_SH25-27_extrait_complet.mp4 (AVANT QC1 + son M7B.2 puis APRÈS P4 + son M8.1). Durées : AVANT SH25 12,0 s / SH26 11,5 s ; APRÈS SH25 10,5 s / SH26 13,0 s (sortie −1,5 s, SH26 +1,5 s) ; SH27 175,0 et totaux inchangés. Raccord sonore mesuré : musique MC→MD (−20 dBFS) masque les bruitages (≈ −42 dB) ; page SH25 de 161,8 (0,2 s avant la coupe 162,0) jusqu'à 163,4 ; écart M8.1/M7B.2 ≤ 1 dB, saut d'échantillon maximal 0,025 (pas de clic) -> NON gênant, conservé pour écoute humaine ; aucun changement audio. Écart pages/changements de carte : QC1 +0,6/+0,4 s ; P4 −0,8/−0,5 s.
- QC1, références verrouillées, anciens extraits : intacts ; 0 € ; aucune IA ; aucune intégration au master.

## 2026-11-18 — Décisions utilisateur après révision ChatGPT Work (maquettes)
- SH12–16 : RETENIR l'APRÈS. P2 SH33/34 : RETENIR la frise corrigée v3c (frise figée). P3 SH27/28 : RETENIR la variante visuelle raccourcie (portraits et drapeaux préservés). P4 SH25/26 : REJETÉE (durées et images QC1 : SH25 jusqu'à 02:43,5 ; SH26 jusqu'à 02:55,0).
- Liste exacte des substitutions préparée, NON appliquée : docs/SUBSTITUTIONS_PREVUES_QC1_vers_QC2.md. Aucun rendu, aucune intégration au master ; QC1, originaux et références verrouillées intacts ; 0 € ; aucune IA ; aucun FINAL.
- Raccord audio « 0,3 s » : vérifié par calcul sur les repères — il ne concerne que la variante P4 rejetée (coupure à 162,0 s, page 161,8–163,4). En QC1/M8.1 (coupure 163,5 s) la dernière page finit à 163,4 (M8.1) / 162,25 (M7B.2) : aucun son ne traverse la coupe ; le seul « +0,3 s » est le grincement de fenêtre SH26 à 163,8, voulu.

## 2026-11-18 — Clarification QC2 (utilisateur) — liste v2 des substitutions, NON appliquée
- P2 : frise v3c retenue, durées QC1 conservées (SH33 14 s, SH34 10,5 s), tenue finale adaptée (apparition 1,5 s/entrée, vue complète stable 5 s, sans réplique dans SH33). P3 : SH27 −1,5 s, SH28 avancé (maquette validée). SH26 : QC1 intégral, sans recul. SH12–16 : améliorations visuelles retenues uniquement. SH25/26 : QC1, raccord sonore sans correction. Mix QC1 (M7B.2) conservé ; M8.1 non validé.
- Liste : docs/SUBSTITUTIONS_PREVUES_QC1_vers_QC2_v2.md (v1 conservée). Cohérence : 38 plans contigus, 276,0 s, 0 réplique hors plan. Intégration au master : en attente d'autorisation explicite ; aucun rendu ; 0 € ; aucune IA ; aucun FINAL.

## 2026-11-18 — Intégration autorisée : MASTER_CANDIDATE_NON_FINAL_QC2 (NON FINAL)
- Fichier : animatic/MASTER_CANDIDATE_NON_FINAL_QC2_1080p.mp4 (vidéo animatic/qc2/MASTER_CLEAN_1080p_video_QC2.mp4, script scripts/build_qc2.py) ; substitutions = docs/SUBSTITUTIONS_PREVUES_QC1_vers_QC2_v2.md uniquement.
- Audio : piste AAC de QC1 recopiée sans réencodage (MD5 audio identique). check_delivery : OK (1920x1080, H.264/AAC stéréo, 276,1 s).
- Contrôle image par plan (différence QC1/QC2) : seuls SH13–16, SH27, SH28, SH33 changent (+ 0,5 s de fondu d'entrée SH29 qui hérite de la dernière image de SH28) ; 30 autres plans identiques ; SH25/26/34 = QC1. 38 plans, 6903 images.
- A5 (182,5) dans SH28 (180,5–189,5) ; portraits Anefo, drapeaux et carton SH27 visibles ; frise SH33 v3c complète de 9,0 à 14,0 s (titre seul 0–1,5 s).
- QC1, références verrouillées, anciennes versions intacts ; 0 € ; aucune IA ; aucun FINAL ni publication.

## 2026-11-18 — QC2 enregistré comme RÉFÉRENCE VISUELLE CANDIDATE (NON FINALE)
- Conformité visuelle SH33, SH27/28, SH25/26 confirmée (révision ChatGPT Work, décision utilisateur). Plans validés figés ; QC1, références historiques archivées et originaux conservés. Aucun remontage, aucune IA, aucun nouvel export.
- Comparaison mix QC1 / M8.1 (mesures, rien appliqué) : docs/COMPARAISON_MIX_QC1_vs_M8.1.md.

## 2026-11-18 — Test sonore ciblé QC2 (NON FINAL, non appliqué)
- Lit M6 test (scripts/sound_design_m6_test.py : SH06 page, SH12 brise, rue 1944 pas + oiseaux, nuit 1953 grillons, foule 1955 ; sans réverbération ; SH11/SH25 = QC1) ; mix M9T → M9T.1 (scripts/music_finish_m9_test.py, audio_qc_m9t.py) : −16,0 LUFS, −1,2 dBTP.
- MP3 AVANT/APRÈS : audio/mixes/M9T.1/TEST_SONORE_QC2_AVANT-QC1_APRES-M9T.mp3 ; index : docs/TEST_SONORE_QC2_INDEX.md. QC1/QC2 et leur mix inchangés ; 0 € ; aucune IA.

## 2026-11-19 — Décisions audio M9T.1 (utilisateur) — extrait SH27/28 corrigé, NON FINAL
- Retenu : V1 APRÈS (musique et rumeur −3 dB sous 166,3–169,6 s). Foule réelle SH27/28 conservée comme candidate, acclamations atténuées. Autres bruitages M9T.1 (rue 1944, grillons, SH06/SH12, −2 dB sous A1) NON appliqués. Dialogues, musique B, silences préservés ; QC1, QC2, M9T.1 intacts.
- M9T2.1 (sound_design_m7_test.py, music_finish_m9t2.py, audio_qc_m9t2.py) : −16,0 LUFS, −1,2 dBTP ; acclamations −8 dB, filtrées 250–3200 Hz ; énergie 3–8 kHz (176–181 s) : QC1 −37,4 / M9T.1 −43,1 / M9T2.1 −48,3 dB ; fenêtre des acclamations −1,4 dB vs M9T.1 ; A5 inchangée.
- Extraits : audio/mixes/M9T2.1/extrait_SH27-28/ (MP3 comparatif 3 versions ; MP4 image QC2 + son M9T2.1, 174–190 s). 0 € ; aucune IA ; aucun FINAL.
