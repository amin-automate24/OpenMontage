# Fiche décor : LE PATIO DE LA MAISON (ENV_02)

> Statut : **PROPOSITION, en attente de validation du prompt.** Aucune génération lancée.

## Rôle dans le film
Décor de la séquence 1 (la maison de Fès, lumière d'après-midi : le grand-père âgé sommeille ou prie, Yassine monte l'escalier vers le grenier) et du retour en séquence 6. Il doit être **réel** (dar traditionnel, type architectural de Fès) et **chaleureux**, en contraste doux avec le grenier poussiéreux.

## Description (bible C : patio, zellige vert et blanc, gebs, cèdre, fontaine)
| Élément | Description |
|---|---|
| Cour | Patio carré, dallage de terre cuite et marbre blanc usé, petite fontaine centrale en zellige vert et blanc, eau claire |
| Murs | Arcs, plâtre sculpté (gebs) blanc cassé, frises de zellige vert et blanc à hauteur d'homme, sans inscription |
| Boiseries | Portes, volets et galerie à l'étage en cèdre, patine brune |
| Escalier | Escalier de bois étroit montant vers l'étage et la terrasse (celui de Yassine), visible dans un angle |
| Ciel | Ouverture carrée vers le ciel, lumière d'après-midi qui frappe un côté de la cour, l'autre en ombre |
| Mobilier | Un banc bas à coussins de laine, un tapis, une plante en pot ; **un seul** fauteuil ou banc pour le grand-père, à l'ombre |
| Ambiance | Calme, novembre, lumière dorée douce, intemporel |

**Règles de continuité :** aucun texte ni calligraphie (zellige géométrique seulement) ; aucun objet moderne, câble, antenne, plastique ; la lumière vient de la **gauche** (comme partout dans le film) ; l'escalier de bois reste du côté droit du cadre, pour que Yassine monte vers le grenier.

**Palette (bible F) :** chaux `#E8DCC4`, cèdre `#3B2A1E`, lumière ambrée `#E3A857`, avec le vert zellige comme seul accent froid.

## Prompt Midjourney ENV_02 : plan large de référence
```
Photorealistic cinematic establishing photograph of the central courtyard of a traditional dar house in the medina of Fez, empty of people, late afternoon in November. Square patio with worn terracotta and white marble paving, a small central fountain tiled in green and white geometric zellige with clear water, carved off-white plaster arches, green and white zellige tile bands at human height, dark cedar wood doors, shutters and an upper gallery railing. A narrow wooden staircase rising in the right corner towards the upper floor. A square opening to the sky, warm golden sunlight from the left striking one side of the courtyard while the other side stays in soft shadow. A low bench with wool cushions in the shade, a rug, a potted plant. Quiet, suspended in time. 35mm lens, f/5.6, wide static composition with depth, rich plaster, tile and wood textures, fine 35mm film grain, true-to-life color --ar 16:9 --style raw --s 50 --no people, text, letters, calligraphy, signs, electric cable, antenna, plastic, modern objects, cartoon, illustration, watermark
```

| Paramètre | Valeur | Raison |
|---|---|---|
| `--ar 16:9` | — | Format du film |
| Lumière de gauche, escalier à droite | — | Continuité de la bible et trajet de Yassine vers le grenier |
| `--no calligraphy, text…` | — | Midjourney invente des inscriptions dans les zelliges |
| Version / mode | V8.2, fast | Comme pour le grenier |
| Coût estimé | environ 0,4 crédit Midjourney | — |

**Résultat attendu :** 4 patios crédibles, fontaine en zellige vert et blanc, arcs en plâtre, cèdre, escalier de bois à droite, lumière dorée de gauche, aucun texte.

## Ensuite (après validation du plan large)
- **ENV_02b** : coin d'ombre avec le banc, pour le grand-père (plan de lui assis, dérivé de ENV_02).
- **ENV_02c** : le pied de l'escalier, pour le départ de Yassine (dérivé de ENV_02).

## Registre
| ID | Statut | Midjourney | Magnific | Notes |
|---|---|---|---|---|
| **ENV_02_MASTER** | ✅ VALIDÉ (2026-11-05), choix 2 | grille task `17cb0454-5a5b-4698-b7d3-d9af9b64af33` (image_id `1567997803047682048`) → U2 task `1f870c31-e8bd-4256-81b7-9ef675320ccf` (image_id `1567998181042552832`), 1456×816, 0,12 crédit | `lJXareYgv9` (tuile non agrandie : `rgMIq2axtc`) | Fontaine en zellige vert et blanc (grand bassin surélevé), arcs en plâtre sculpté, banc à coussins à gauche, escalier de bois à droite, lumière chaude de gauche, aucune inscription |
