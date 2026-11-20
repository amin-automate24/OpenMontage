# CREDIT BUDGET AND PRODUCTION RISK REPORT 1.0

> **Aucun crédit consommé, aucun abonnement, aucune génération.** Les prix ci-dessous viennent de simulations **en lecture seule** (`simulate_cost` de Magnific, certitude « exact » sauf mention) et de lectures de solde. Le plafond de 2 000 crédits est un plafond de planification, **pas une autorisation de dépense**.

## 1. Soldes et limites des intégrations (lues le 16/11/2026)

| Intégration | État constaté | Conséquence |
|---|---|---|
| **Magnific** (plan Plus, crédits personnels) | **10 158 crédits disponibles** (73 070 au total, 62 912 dépensés ; « crédits supplémentaires » activés) — **partagés avec THE LAST OF MEN** | Réserve à définir pour THE LAST OF MEN (décision D2). Attention : les crédits supplémentaires peuvent signifier une consommation hors forfait — à ne pas déclencher. |
| Artlist | Essai gratuit, 0 crédit IA ; 2 images et 1 vidéo gratuites (non renouvelables) | Inutile pour la production ; pas de musique/génération sans abonnement. |
| Higgsfield | 0 crédit, plan gratuit | Inutilisable. |
| ElevenLabs (connecteur) | Lecture du solde refusée : « permissions supplémentaires requises, reconnecter le connecteur » | Voix finales non vérifiables ; le connecteur « restreint » n'offre ni musique ni vidéo. |
| Runway, Veo, Midjourney | Non interrogés (aucun besoin identifié, éviter toute dépense) | — |
| Firecrawl | Facturé à la requête : **non utilisé** (aucune vérification web) | Les vérifications historiques restent humaines. |
| Dropbox | Lecture seule ; aucune écriture, aucun fichier THE LAST OF MEN touché | — |

## 2. Prix unitaires (Magnific, 16:9)

| Poste | Modèle / réglage | Crédits | Certitude |
|---|---|---|---|
| Image finale | Google Nano Banana 2.1, 2k | **65** | exact |
| Image finale | GPT 2.6, 2k, qualité moyenne | 65 | exact |
| Image (brouillon 1k) | Nano Banana 2.1, 1k | 50 | exact |
| Image « esthétique » | Magnific One, 2k, qualité moyenne | 180 | exact |
| Image brouillon de composition | flux-dev | 10 | exact (qualité/consistance non testées) |
| Planche personnage | `images_character_sheet` | 145 | exact |
| **Vidéo image→vidéo 5 s, 1080p** | **Kling 2.5** (silencieux, image de départ + de fin) | **325** | exact |
| Vidéo 5 s, 720p | Seedance 2.0 Mini (audio natif) | 700 | exact |
| Vidéo 5 s, 720p | Seedance 2.0 Fast | 1 175 | exact |
| Vidéo 5 s, 1080p | Seedance 2.5 | 3 950 | exact |
| Voix (TTS) | ElevenLabs v3 via Magnific | 0,2 / caractère → **≈ 310** pour les 1 547 caractères de dialogue | extrapolé de 900 car. = 180 |
| Musique | Google Lyria 3 (par génération) | 80 | exact (durée du clip à confirmer) |
| Musique | ElevenLabs Music v2, 270 s | **5 400** | exact — écarté |
| Upscale image | selon taille source | 90 – 1 080 | variable — non prévu |

Remarque : les premières simulations avec `slug` retombaient sur le mode « Auto » (65 cr, « variable ») ; les valeurs ci-dessus sont celles obtenues avec le bon paramètre `mode` (« exact »).

## 3. Inventaire de génération (si tout est exécuté)

- **12 images de référence** : style board, 5 fiches personnages (Younes, Amina multi-âge, père, maîtresse, mère), fiche accessoires, 5 décors (E1–E5).
- **≈ 33 images de plans** (30 plans principaux – 3 qui réutilisent un décor + 3 illustrations d'inserts + 3 vues de fenêtre pour le montage des saisons).
- **Total premier jet : 45 images.**
- **5 plans image→vidéo** possibles (SH07, SH11, SH26, SH27, SH38) ; **3 prioritaires** : SH11 (pages qui tournent — le motif central), SH26 (fenêtre/lumière — pivot émotionnel), SH38 (plan final).

## 4. Trois scénarios budgétaires (planification)

| | **A — Plafond 2 000** | **B — Recommandé** | **C — Complet** |
|---|---|---|---|
| Images (premier jet) | 24 (16 plans + 8 réfs) | 45 × 65 = **2 925** | 45 × 65 = **2 925** |
| Re-générations | 6 × 65 = 390 | 9 (20 %) × 65 = **585** | 585 |
| Sous-total images | **1 950** (30 images) | **3 510** | **3 510** |
| Image→vidéo (Kling 2.5, 5 s) | **0** | 3 clips × 325 = 975 + 1 reprise 325 = **1 300** | 5 clips × 325 = 1 625 + 2 reprises 650 = **2 275** |
| Voix finales (Magnific TTS) | hors plan (voix humaines ou autre outil) | 310 + 50 % de reprises = **465** | 465 |
| Musique (Lyria 3 × 3 clips) | hors plan (musique libre de droits) | **240** | 240 |
| **TOTAL** | **1 950** | **5 515** (4 810 sans audio) | **6 490** (5 785 sans audio) |
| Reste sur 10 158 | 8 208 | 4 643 | 3 668 |
| Qualité attendue | Réutilisation forte des mêmes images (≈ 2,4 plans/image), **aucun plan animé** : mouvements 2,5D locaux seulement ; risque de répétitivité | Un visuel propre par plan, 3 moments animés clés | Tous les moments animés |
| Respecte le plafond de 2 000 ? | **Oui** | **Non (×2,8)** | Non (×3,2) |

**Lecture** : le plafond de 2 000 crédits ne permet qu'un film en images fixes très réutilisées. Dès qu'on veut des plans propres + quelques plans animés, il faut environ **5 000–5 500 crédits**. Ce n'est pas une surprise cachée : c'est la décision financière centrale (D2).

**Leviers d'économie** (cumulables) : brouillons de composition en flux-dev (10 cr) avant tout rendu final à 65 cr ; planches personnages réduites à 3 (Younes, Amina, père) ; réutiliser E1 pour 6 plans de classe ; clips I2V limités à SH11 et SH26 (économie 325) ; voix humaines enregistrées en dehors des crédits ; musique issue d'une bibliothèque libre de droits vérifiée.

**Ordre d'engagement conseillé** : approuver d'abord un **échantillon** (REF-00 + REF-01 + REF-02 = 195 crédits, ou 30 en flux-dev) pour valider le style avant d'engager le reste ; ne jamais enchaîner l'étape suivante automatiquement.

## 5. Droits et licences (à régler avant publication)

| Élément | État | Action |
|---|---|---|
| Images / vidéos générées (Magnific) | Droits d'usage commercial et éducatif **non vérifiés** dans cette session | Lire les conditions du plan Plus (usage commercial, mentions IA obligatoires) avant publication |
| Voix finales | Aucune voix finale. Voix synthétiques actuelles = **internes**, non publiables ; **ne jamais cloner ou imiter la voix de Mohammed V** | Choisir : comédiens humains (enfants 9–12 ans → autorisation parentale/école) ou TTS autorisé ; vérifier la licence |
| Musique | **Aucune piste disponible** (`music_library/` vide ; Artlist sans crédit ; Lyria 3 payant) | Fournir une piste libre de droits (ex. bibliothèque audio YouTube, Jamendo) avec preuve de licence, ou approuver une génération Lyria 3 |
| Documents/illustrations historiques | Aucune archive utilisée ni fabriquée | Mention « illustration pédagogique — non archive » (D3) ; si de vraies archives sont ajoutées, vérifier leur statut juridique |
| Drapeau, symboles nationaux | Dessinés en vecteur, forme officielle à vérifier | Contrôle humain (H5) |
| Diffusion en milieu scolaire marocain | Conformité programme / autorisation de diffusion non vérifiées | À confirmer par le commanditaire |

## 6. Risques de production

| # | Risque | Probabilité | Impact | Parade |
|---|---|---|---|---|
| R1 | **Plafond 2 000 crédits incompatible** avec le périmètre visuel | Certaine | Élevé | Décision D2 (scénario A ou relèvement) |
| R2 | Délai : 4 jours (16 → 20 nov.), dont génération, retakes, voix, montage, étalonnage | Élevée | Élevé | Figer les décisions D1–D9 aujourd'hui ; limiter I2V ; montage local |
| R3 | Cohérence des personnages (Amina sur trois âges, 38 plans) | Moyenne | Élevé | Fiches + références obligatoires, un seul modèle image, seeds journalisés |
| R4 | Erreurs historiques de l'IA (drapeau, costumes, architecture, calligraphie) | Élevée | Élevé | Éléments sensibles composités en vecteur/post ; revue humaine par plan flaggé |
| R5 | Scène 6 trop dense (20 s) | Certaine | Moyen | Décision D1 (+6 s) |
| R6 | Voix finales d'enfants/adultes de qualité française native | Moyenne | Élevé | Plan voix (D10) ; test sur 2 répliques avant de tout commander |
| R7 | Pas de musique licenciée | Certaine | Moyen | Fournir une piste ou approuver Lyria 3 |
| R8 | Consommation des crédits partagés avec THE LAST OF MEN | Moyenne | Élevé | Réserve écrite (D2) + registre des dépenses |
| R9 | Rendu final : moteur de composition non choisi | Faible | Moyen | Décision D9 |
| R10 | Fichiers fragiles : conteneur éphémère | Moyenne | Moyen | Tout est commité dans la branche `claude/carnet-liberte-preproduction-b3y71m` |

## 7. Garantie d'isolation de THE LAST OF MEN

- Aucune écriture : seules des recherches Dropbox **en lecture** ont été faites (dossiers `THE_LAST_OF_MEN_*` repérés, non ouverts, non modifiés).
- Le projet vit dans `projects/le-carnet-de-la-liberte/` (espace séparé) ; aucun fichier existant n'a été écrasé.
- Dernier backup repéré (non touché) : `THE_LAST_OF_MEN_BACKUP_20261114_2036_v001.zip` ; derniers rapports du 15–16/11/2026.
- Aucun crédit partagé consommé ; ses portes d'approbation ne sont pas altérées.
