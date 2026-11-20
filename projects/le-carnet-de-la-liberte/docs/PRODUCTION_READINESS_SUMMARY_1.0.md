# PRODUCTION READINESS SUMMARY 1.0 — LE CARNET DE LA LIBERTÉ

Date : 16/11/2026 · Livraison cible : **vendredi 20/11/2026** (J-4) · Durée : 270 s (max 300 s)

## Verdict : préproduction prête, production payante **bloquée sur des décisions**, pas sur la technique

| Domaine | État |
|---|---|
| Scénario 1.1 (texte exact, SHA-256 enregistré) | ✅ sauvegardé, six scènes et durées validées (30+35+55+55+75+20 = 270 s) |
| Liste technique de plans 1.0 | ✅ 38 plans (30 principaux + 8 secondaires), timecodés, 270,0 s |
| Animatic 1.0 local | ✅ MP4 1080p25 H.264/AAC, 270,0 s, voix synthétiques internes (non publiables) |
| Plan des références personnages/décors | ✅ rédigé, non exécuté |
| Pack de prompts (image, image→vidéo) | ✅ rédigé, non exécuté (45 images + 5 clips) |
| Budget et risques | ✅ chiffré avec prix exacts ; **plafond 2 000 cr incompatible** avec le périmètre propre |
| Registre d'approbations | ✅ 4 portes, **aucune accordée** |
| Isolation de THE LAST OF MEN | ✅ aucune écriture, aucun crédit partagé consommé |
| Crédits dépensés / appels payants | **0 / 0** |

## Ce qui a été découvert (important)

1. **Plafond de 2 000 crédits** : seul le scénario A (images fixes très réutilisées, **aucun plan animé**) y tient (1 950). Le scénario recommandé B coûte ≈ **5 515** (dont 705 d'audio) ; le solde Magnific partagé est de **10 158**.
2. **Scène 6 trop dense** : 20 s pour ~15 s de dialogue naturel + écriture + plan final + titre. Recommandation : +6 s (film de 276 s).
3. **« arrière-arrière-grand-mère »** : la généalogie donne « arrière-grand-mère » (Amina née vers 1933).
4. **`carnet.py` introuvable** sur la machine ; remplacé par `scripts/carnet_animatic.py`.
5. **Voix, musique, droits** : aucune voix finale, aucune musique licenciée ; connecteur ElevenLabs à reconnecter ; Artlist et Higgsfield sans crédits.
6. **Moteurs de composition** : seul FFmpeg est utilisable aujourd'hui ; Remotion (dépendances `node_modules` manquantes) et HyperFrames (paquet non installé) demandent une installation gratuite mais à décider (D9).

## Décisions indispensables (voir `approvals/APPROVAL_REGISTER_1.0.md` §4)

D1 durée scène 6 · **D2 plafond/réserve de crédits** · D3–D5 mentions pédagogiques · D6 design de la maîtresse · D7 langue du carnet · D8 phrases écrites murmurées ou non · **D9 moteur de composition** · D10 voix finales · D11 correction de parenté · D12 musique.

### D9 — Moteurs de composition (présentation obligatoire avant verrouillage)
- **FFmpeg** (disponible) — fiable, simple ; limité pour cartons animés. *Contre-indication :* rendu plus sec.
- **Remotion** (nécessite installation locale gratuite) — idéal pour cartons de dates, ligne du temps, titres déjà modélisés ; *contre :* installation + mode « templated » = look générique si on ne personnalise pas.
- **HyperFrames** (nécessite installation) — idéal pour l'effet « encre » et la typographie animée ; *contre :* plus expérimental, plus de temps.
- **Recommandation** : montage final dans **DaVinci Resolve** (déjà prévu), avec cartons/graphiques produits localement en **FFmpeg/Remotion** ; HyperFrames seulement si le temps le permet. À valider — je n'ai rien verrouillé.

## Prochaines actions (ordre conseillé, planning J-4)

| Jour | Action | Dépend de |
|---|---|---|
| **Lun 16 (aujourd'hui)** | Vous : trancher D1, D2, D6, D9–D12 ; fournir/valider références historiques (H5). Moi : appliquer D1/D11 à la liste de plans, ré-exporter l'animatic 1.1 | Vos réponses |
| **Mar 17** | GATE 2 (échantillon d'abord : REF-00/01/02), puis fiches et décors, puis images de plans | Approbation GATE 2 + budget |
| **Mer 18** | GATE 3 (3 clips I2V) ; enregistrement des voix ; composition locale des cartons, drapeaux, ligne du temps | GATE 3 ; D10 |
| **Jeu 19** | Montage Resolve, étalonnage, musique, mixage, contrôle historique plan par plan | GATE 4 ; D12 |
| **Ven 20** | Export final + vérification (durée < 5 min, 1080p, H.264/AAC) | — |

**Alerte planning** : toute décision qui glisse au 17 mettra les gates 2–3 en conflit avec l'enregistrement des voix et les retakes. Recommandation : décisions D1–D2–D10 **aujourd'hui**.

## Fichiers livrés (dans `projects/le-carnet-de-la-liberte/`)

- `docs/LE_CARNET_DE_LA_LIBERTE_SCREENPLAY_DRAFT_1.1_FR.md`
- `shotlist/TECHNICAL_SHOT_LIST_1.0.md`, `shot_list.csv`, `shots.json`
- `animatic/ANIMATIC_1.0_LOCAL_PLACEHOLDER.mp4`, `contact_sheet.png`, `dialogue_timing.json`
- `references/CHARACTER_AND_ENVIRONMENT_REFERENCE_PLAN_1.0.md`
- `prompts/GENERATION_PROMPT_PACK_1.0.md`, `prompt_pack.json`
- `docs/CREDIT_BUDGET_AND_PRODUCTION_RISK_REPORT_1.0.md`
- `docs/HISTORICAL_AND_TIMING_FLAGS_1.0.md`
- `docs/SOUND_MUSIC_AND_RESOLVE_PLAN_1.0.md`
- `approvals/APPROVAL_REGISTER_1.0.md`, `approval_register.json`
- `scripts/` (`shots_data.py`, `carnet_animatic.py`, `gen_docs.py`) — l'animatic se régénère localement en une commande.

## Limites connues de l'animatic

Silhouettes placeholders ; voix espeak-ng robotiques ; pas de musique ni de SFX ; petits débordements cosmétiques (texte du tableau SH02, dernière ligne de la ligne du temps SH33, titre sur le drapeau SH38). Le minutage, lui, est exact et sert de référence.
