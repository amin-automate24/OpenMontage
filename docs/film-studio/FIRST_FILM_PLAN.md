# Plan — premier court-métrage (pilote)

> Statut : **proposition, mode 1 (planification)**. Rien n'a été généré et rien n'a été dépensé.

## Pourquoi un pilote

Le premier film doit éprouver toute la chaîne (bible, génération, continuité, son, montage, QC, export)
en jouant sur les points forts des générateurs actuels : décors, lumière, atmosphère, mouvements de
caméra lents. Il doit aussi éviter leurs points faibles : visages en gros plan répétés, mains, dialogues
synchronisés, foules.

## Proposition : **« Le Dernier Feu »**

| | |
|---|---|
| Genre | Court-métrage dramatique contemplatif, sans dialogue |
| Logline | La nuit où son phare doit être automatisé, un vieux gardien allume la lanterne une dernière fois, pour personne. |
| Durée | 60 à 75 s · 6 scènes · 12 à 14 plans de 4 à 6 s |
| Format | 16:9, 1920×1080, 24 fps, image en 2.39:1 avec letterbox |
| Direction artistique | Réalisme cinématographique, crépuscule bleu acier et lumière tungstène chaude, grain 35 mm léger, caméra lente sur dolly ou trépied |
| Personnage | Un seul : le gardien, presque toujours de dos, en silhouette ou de trois-quarts. Un unique gros plan (le regard), placé à la fin |
| Son | Vent, ressac, mécanisme de la lanterne, piano minimaliste et cordes qui montent, un silence complet avant la dernière image |
| Dernière image | Le faisceau balaie la mer une dernière fois. La fenêtre de la salle de veille s'éteint ; le phare reste allumé, automatique |

### Découpage indicatif

| Scène | Contenu | Plans | Risque |
|---|---|---|---|
| SC01 | Le phare au crépuscule, mer agitée (plan d'ensemble, lente approche) | 2 | faible |
| SC02 | Le gardien monte l'escalier en colimaçon, de dos | 2 | moyen (mouvement du corps) |
| SC03 | Mains sur le mécanisme, la lentille de Fresnel s'éclaire | 3 | moyen (mains → inserts courts) |
| SC04 | Le faisceau sur la mer, une lettre « Automatisation 1er novembre » sur la table | 2 | faible (texte → insert typographique en HyperFrames plutôt que généré) |
| SC05 | Le gardien regarde la mer, gros plan unique | 2 | **élevé** (visage → keyframe validée + image-to-video, mouvement minimal) |
| SC06 | Il éteint sa lampe de bureau ; le phare continue sans lui | 2 | faible |

## Les trois chemins de production

| Chemin | Ce qu'il faut | Coût indicatif du pilote | Qualité / limites |
|---|---|---|---|
| **A — Clé Gemini réelle** (recommandé) | Remplacer la `GEMINI_API_KEY` factice par une clé payante | Vidéo : ~70 s × 2 prises × ~0,10 $/s ≈ **14 $**. Keyframes et musique Lyria : quelques dollars de plus. **Plafond proposé : 25 $** | Pipeline 100 % natif (registre, coûts suivis, board), audio synchronisé natif. Une seule clé pour l'image, la vidéo, la musique et la voix |
| **B — Clé fal.ai** | Ajouter `FAL_KEY` | Selon le modèle (Seedance, Kling, Veo), annoncé avant chaque appel | Le plus grand choix de modèles vidéo et de meilleurs outils de cohérence par références |
| **C — Runway via MCP** | Recharger Runway (1 000 crédits = 10 $) | Le prix au crédit de chaque modèle est confirmé par l'outil avant l'appel. Prévoir 1 000 à 2 000 crédits | Fonctionne sans toucher à l'environnement, mais hors registre : provenance et coûts consignés à la main |
| **D — Zéro budget** | Rien | 0 $ | Pas de vidéo générée. Animatic sur stills ou monde Three.js stylisé : **ce n'est pas un film en prise de vues réelles**, à réserver pour valider la narration |

Ces chiffres sont des estimations. Le coût exact est annoncé outil par outil avant chaque appel, et le `cost_tracker` le suit en continu.

## Déroulé concret

| Étape | Livrable | Porte | Mode |
|---|---|---|---|
| 0 | `film_studio.py init le-dernier-feu`, board Backlot ouvert | — | 1 |
| 1 | research (références de lumière et d'ambiance) → `01_CONCEPT.md` + 3 directions | — | 1 |
| 2 | proposal : direction retenue, `03_VISUAL_BIBLE`, `04_CHARACTER_BIBLE`, runtime de composition (Remotion **et** HyperFrames présentés), plan musique, devis | **Porte 1** | 1 |
| 3 | `02_SCREENPLAY.md` | **Porte 2** | 1 |
| 4 | `05_STORYBOARD.md` + `06/08` prompts. Keyframes : 1 référence du gardien + 1 image par plan, **seul poste de dépense, environ 1 $** | **Porte 3** | 1 → 2 |
| 5 | Test : 2 plans (SC01 et SC05, le plus facile et le plus risqué) pour valider la cohérence avant de lancer le reste | accord | 2 |
| 6 | Génération des 12 à 14 plans, SFX, musique ; QC visuel plan par plan | **Porte 4** | 2 |
| 7 | Montage, étalonnage, mix -14 LUFS, titres et générique | — | 2 |
| 8 | `film_studio.py qc` → `11_QC_REPORT` ; corrections ; `export --master` | — | 2 |
| 9 | Livraison sur Dropbox ou Drive (avec accord) ; bilan dans `production_log.md` | accord | — |

## Ce que j'attends de toi

1. **Le chemin** (A, B, C ou D) et un **plafond de budget**.
2. **Garder « Le Dernier Feu » comme pilote** ou partir de ta propre idée. Dans ce cas, donne la logline et la durée ; je choisis le reste et je n'ajoute pas de questions inutiles.
