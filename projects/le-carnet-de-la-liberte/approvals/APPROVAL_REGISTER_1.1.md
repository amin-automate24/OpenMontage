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
