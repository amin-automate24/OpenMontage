# S1 — Fiches de plan

## S1-01 — patio vide (test 1)
| Champ | Valeur |
|---|---|
| Image de référence | ENV_02_MASTER (Magnific `lJXareYgv9`) |
| Prompt Midjourney | grille task `17cb0454-5a5b-4698-b7d3-d9af9b64af33`, U2 task `1f870c31-e8bd-4256-81b7-9ef675320ccf` |
| Prompt vidéo | voir 06_VIDEO_PROMPTS.md (S1-01) |
| Modèle / paramètres | Kling 3.0 Omni `kling-omni3`, 9 s, 16:9, 1080p, image de départ, sans son généré |
| Coût | 855 crédits Magnific |
| Vidéo | Magnific `If4GFLQtvE` (v1) |
| Remarques QC v1 | Push-in correct mais trop marqué (la fontaine grossit d'environ 1,6×), pas d'oiseau. Le décor dérive : dès 0,3 s le cadrage est plus large que le MASTER et les arcs, l'escalier et le banc changent de place ; le jet de la fontaine apparaît puis devient une colonne blanche en fin de plan. Pas de personne, texte ou artefact grave. Continuité du décor insuffisante pour un plan d'ouverture |
| Statut v1 | ❌ non retenue (dérive du décor) |

### v2 (reprise 1080p, prompt resserré)
| Champ | Valeur |
|---|---|
| Prompt | « Locked-off static camera… architecture strictly identical… push-in of about 3 percent… single small low spray unchanged… no people, no birds » |
| Vidéo | Magnific `dt73qaYXSL`, 855 crédits |
| Remarques QC v2 | Architecture stable sur 9 s (arcs, escalier à droite, banc, fontaine), jet d'eau minime, pas de colonne blanche, push-in très léger, pas d'oiseau (retiré volontairement). Réserve : le cadrage est plus large que le MASTER dès la première image (le modèle recompose légèrement) ; lumière et ambiance conservées |
| Statut | ✅ **VALIDÉ v2** (2026-11-05), écart de cadrage accepté |

## S1-03 — le grand-père sur le banc
### Image de départ v1
| Champ | Valeur |
|---|---|
| Références | ENV_02b `KL0BHjPkqp`, GPA_01 `N2EeRSy6D9`, PRP_06 `u5AVLoyQLD` |
| Méthode | Nano Banana 2.1, 16:9, 65 crédits |
| Image | Magnific `tC9zsgymZJ` (aperçu `S1-03_start_v1_preview.jpg`) |
| QC | Alcôve fidèle à ENV_02b ; djellaba brun grisé, chemise blanche, sans taqiya, cheveux gris argenté, moustache claire, chapelet long tenu à deux mains. Visage petit à cette distance : identité plausible mais grain de beauté non vérifiable. Écart : yeux ouverts, regard vers la gauche (pas encore assoupi), visage éclairé et non dans l'ombre. Fontaine visible en bas à droite (plus proche que dans le MASTER) |
| Statut v1 | ↪ remplacée par v2 sur demande (MODIFIER IMAGE) |

### Image de départ v2
| Champ | Valeur |
|---|---|
| Méthode | Nano Banana 2.1 sur v1 `tC9zsgymZJ` + GPA_01, 65 crédits |
| Image | Magnific `P3a5d9542C` (aperçu `S1-03_start_v2_preview.jpg`) |
| QC | Composition, vêtements, chapelet et décor identiques à la v1. Tête un peu baissée, paupières mi-closes, expression calme. Éclairage du visage peu modifié (changement subtil). Grain de beauté non vérifiable à cette distance |
| Statut | ✅ **VALIDÉE** (2026-11-05) |

### Vidéo v1
| Champ | Valeur |
|---|---|
| Modèle / paramètres | Kling 3.0 Omni, 9 s, 16:9, 1080p, image de départ `P3a5d9542C`, sans son |
| Vidéo | Magnific `YMr7QgGWeC`, 855 crédits |
| QC | Pose, vêtements, banc et alcôve stables sur 9 s, aucune dérive visible de silhouette, mouvement très discret (pas de saut). Écart : le cadre est beaucoup plus large que l'image de départ (plan moyen devenu plan large : le grand-père occupe environ un sixième de la hauteur), donc visage trop petit pour vérifier l'identité et la respiration/les paupières ; la fontaine est plus présente. Même recomposition que S1-01 |
| Statut | ✅ **VALIDÉE comme plan large** (2026-11-05) : le visage est trop petit pour que l'écart d'identité se voie |

### Image de départ v3 (plus serrée, pour reprise)
| Champ | Valeur |
|---|---|
| Méthode | Nano Banana 2.1 sur v2 `P3a5d9542C` + GPA_01, 65 crédits |
| Image | Magnific `gOBCdN9SXO` (aperçu `S1-03_start_v3_tight_preview.jpg`) |
| QC | Plan taille-haut, trois-quarts, yeux fermés, expression paisible, chapelet entre les mains, alcôve floutée. Djellaba brun grisé avec capuche, chemise blanche, sans calotte. Ressemblance avec GPA_01 : approximative (cheveux gris courts, moustache blanche, visage maigre et ridé) mais le grain de beauté sous l'œil gauche est absent, la ligne de cheveux moins dégarnie et le nez moins aquilin. Identité non garantie |
| Statut | ❌ non utilisée (identité approximative) ; la vidéo plan large `YMr7QgGWeC` est conservée pour S1-03 |

## S1-02 — fontaine, insert
### Image de départ v1
| Champ | Valeur |
|---|---|
| Référence | ENV_02_MASTER `lJXareYgv9` |
| Méthode | Nano Banana 2.1, 16:9, 65 crédits |
| Image | Magnific `w4IQt107EI` (aperçu `S1-02_start_v1_preview.jpg`) |
| QC | Même patio reconnaissable (arcs, escalier à droite, banc à coussins à gauche, plante). Gouttes tombant dans le bassin, éclaboussures, reflets chauds sur l'eau, profondeur de champ faible. Aucun texte. Écarts : bassin plus large que dans le MASTER, quelques carreaux bleu marine dans la bordure au premier plan, gouttes qui tombent d'une source hors cadre |
| Statut | ✅ **VALIDÉE** (2026-11-05) |

### Vidéo v1
| Champ | Valeur |
|---|---|
| Modèle / paramètres | Kling 3.0 Omni, 9 s, 16:9, 1080p, image de départ `w4IQt107EI`, sans son |
| Vidéo | Magnific `jUphXBNLD0`, 855 crédits |
| QC | Plan stable sur 9 s : ondulations et cercles dans l'eau verte, reflets chauds qui tremblent, quelques gouttes visibles en haut du cadre, aucun saut ni artefact, pas de texte. Écart : dès la première image, la caméra est plus basse et plus proche de l'eau que l'image de départ, le fond d'arcades est simplifié (moins de détails d'escalier et de banc) ; gouttes plus discrètes que prévu |
| Statut | ✅ **VALIDÉ v1** (2026-11-05), écart de cadrage accepté |

## S1-04 — mains et chapelet
### Image de départ v1
| Champ | Valeur |
|---|---|
| Références | PRP_06 `u5AVLoyQLD`, ENV_02b `KL0BHjPkqp` |
| Méthode | Nano Banana 2.1, 16:9, 65 crédits |
| Image | Magnific `ksT85Ch16B` (aperçu `S1-04_start_v1_preview.jpg`) |
| QC | Deux mains âgées (5 doigts chacune, anatomie plausible, taches de vieillesse), l'une égrène le chapelet en bois sombre avec gland, l'autre posée sur la djellaba brun grisé. Alcôve en zellige vert et blanc floue à gauche. Pas de visage, bague, montre ni texte. Mains plus grandes dans le cadre que prévu (plan serré, bon pour un insert) |
| Statut | ⏳ en attente de validation du réalisateur |
| Statut image v1 | ✅ **VALIDÉE** (2026-11-05) |

### S1-04 Vidéo v1
| Champ | Valeur |
|---|---|
| Modèle / paramètres | Kling 3.0 Omni, 9 s, 16:9, 1080p, image de départ `ksT85Ch16B`, sans son |
| Vidéo | Magnific `yiv54N8PW9`, 855 crédits (solde ≈ 14 575, calcul) |
| QC | De 0 à 7,6 s : les perles glissent entre les doigts de façon crédible, la main au repos garde cinq doigts et sa forme, alcôve stable, aucun visage ni texte. Défauts : cadrage plus large que l'image de départ (on voit davantage le genou) ; dans la dernière seconde (8,2 à 8,8 s) la main qui tient le chapelet se lève et s'ouvre, geste non demandé, avec doigts un peu allongés. Utilisable en coupant la fin vers 8 s (ou en gardant le geste comme image de l'assoupissement) |
| Statut | ⏳ en attente de décision du réalisateur |
