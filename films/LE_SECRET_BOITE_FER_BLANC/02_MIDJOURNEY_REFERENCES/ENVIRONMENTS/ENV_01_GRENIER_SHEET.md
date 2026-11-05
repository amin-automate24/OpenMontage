# Fiche décor : LE GRENIER (ENV_01)

> Statut : **PROPOSITION, en attente de validation du prompt.** Aucune génération lancée.

## Rôle dans le film
C'est le décor central des séquences 2 (la découverte de la boîte) et 3 (la transformation : les murs deviennent la fresque). Il faut donc un lieu à la fois **réaliste** (une vraie pièce de rangement de Fès, aujourd'hui) et **riche en surfaces calmes** (les murs à la chaux) sur lesquelles la fresque pourra apparaître.

## Description verrouillée (bible C, section validée)
Pièce de rangement haute, sous la terrasse d'un dar de la médina de Fès, accessible par un escalier étroit. On garde le mot « grenier » dans le film.

| Élément | Description |
|---|---|
| Plafond | Poutres de cèdre sombres, apparentes, solives rapprochées |
| Murs | Chaux blanc cassé, écaillée par endroits, laissant voir l'enduit ocre dessous |
| Sol | Terre cuite ancienne ou carreaux de ciment usés, couverts d'une fine poussière |
| Fenêtre | **Une seule**, petite, en bois de cèdre à volets ajourés, **à gauche du cadre** (règle de continuité de la bible) |
| Lumière | Un seul rai de soleil d'après-midi, ambre, entrant par la fenêtre ; poussière en suspension dans le faisceau |
| Objets | Malles en bois, tapis roulés, cuivres ternis, une vieille chaise paillée, un coffre de cèdre bas dans un coin (là où sera trouvée la boîte) |
| Accès | Une porte basse en bois, au fond, sur un escalier étroit |
| Ambiance | Silence, temps suspendu, mémoire |

**Palette (bible F) :** ombres brun cèdre `#3B2A1E`, chaux `#E8DCC4`, lumière ambrée `#E3A857`, poussière `#C9B79C`.

**Règles de continuité :** fenêtre à gauche du cadre ; pas de prise électrique, ni de câble, ni d'objet en plastique ; aucun texte ni inscription ; le coffre de cèdre reste dans le coin droit.

## Prompt Midjourney ENV_01 : plan large de référence

```
Photorealistic cinematic establishing photograph of an old storage attic room under the roof terrace of a traditional house in the medina of Fez, empty of people. Dark cedar wood ceiling beams with closely spaced joists, whitewashed lime plaster walls flaking in places to reveal ochre plaster beneath, worn old terracotta floor under a fine layer of dust. A single small cedar wood window with lattice shutters on the left of frame lets in one beam of warm amber afternoon sunlight, with dust particles floating in the beam. Old wooden trunks, rolled rugs, tarnished copper pots and a worn straw-seated chair along the walls, a low cedar wood chest in the right corner, a low wooden door at the far end leading to a narrow staircase. Quiet, suspended in time. 35mm lens, f/5.6, wide static composition with depth, rich dust and wood textures, fine 35mm film grain, true-to-life color --ar 16:9 --style raw --s 50 --no people, text, letters, signs, electric cable, plastic, modern objects, cartoon, illustration, watermark
```

| Paramètre | Valeur | Raison |
|---|---|---|
| `--ar 16:9` | — | Format du film : cette image pourra servir directement d'image de départ |
| Fenêtre à gauche | — | Règle de continuité de la bible (lumière venant de la gauche, comme pour les personnages et les objets) |
| `--no people, text…` | — | Aucun personnage (ils s'ajouteront à partir des références validées) ni écriture |
| Version / mode | Midjourney V8.2, fast | Comme pour les personnages |
| Coût estimé | environ 0,4 crédit Midjourney | — |

**Résultat attendu :** 4 greniers crédibles, lumière ambrée par la fenêtre de gauche, poutres de cèdre, chaux écaillée, un coffre bas dans un coin, aucun texte.

## Ensuite (après validation de ce plan large)
- **ENV_01b** : le coin du coffre, plus serré, pour le plan où Yassine découvre la boîte (dérivé de ENV_01 pour garder le même lieu).
- **ENV_01c** : le mur à la chaux vu de face, nu, support de la fresque (séquence 3).

## Registre
| ID | Statut | Midjourney | Magnific | Notes |
|---|---|---|---|---|
| **ENV_01_MASTER** | ✅ VALIDÉ (2026-11-05), choix 1 | grille task `381ab97a-334a-4505-b2ed-ba4bac27c4bc` (image_id `1567994756577886208`) → U1 task `b4aa874a-a95a-418f-86bf-1c7c41d76e1e` (image_id `1567996397930676224`), 1456×816, 0,12 crédit | `JNmF1txOq4` (recadrage non agrandi : `p8UN3Fzehw`) | Fenêtre à gauche, rai ambré avec poussière, poutres de cèdre, chaux écaillée, coffre bas au coin droit, porte et escalier au fond. Réserve : sol plutôt terre battue que terracotta |
| **ENV_01b_CHEST** | ⏳ en attente de validation | — | `hu6nDG3vqL` (Nano Banana 2.1 sur ENV_01_MASTER, 16:9, 65 crédits) | Coin du coffre : même pièce, poutres, chaux écaillée, porte et escalier à gauche, lumière ambrée du bas-gauche. Réserve : coffre plus clair et plus neuf que dans le MASTER |
| **ENV_01c_WALL** | ⏳ en attente de validation | — | `ksToCwi16B` (Nano Banana 2.1 sur ENV_01_MASTER, 16:9, 65 crédits) | Mur nu frontal, chaux blanc cassé écaillée, aucun objet ni texte. Réserve : plafond réduit à une fine bande, éclairage plus frontal que rasant |
