# QC — YAS_02 v1 (portrait trois-quarts)

- Midjourney V8.2 fast, image prompt YAS_01_MASTER + `--iw 1.5` — task `d1b43b57-4a7f-4e3f-9b6d-efa2f7c1ed3f`, image_id `1567619452424421376`, 0,401 crédit
- Magnific : v1_1 `bxWyxqU5Y2` · v1_2 `iGQez2l3uK` · v1_3 `eIwHtmUdqL` · v1_4 `bxWyjgi5Y2`

| Critère | v1_1 | v1_2 | v1_3 | v1_4 |
|---|---|---|---|---|
| Ressemblance avec YAS_01_MASTER | ✅ très bonne | ✅ bonne (plus grave) | ✅ très bonne | ⚠️ visage plus large, plus âgé |
| **Angle trois-quarts (~45°)** | ❌ presque de face | ❌ de face | ❌ très léger quart de tour | ❌ de face |
| **Cicatrice côté droit du front (descripteur)** | ❌ côté gauche | ❌ côté gauche, très marquée | ❌ côté gauche | ⚠️ à peine visible, côté gauche |
| Mèche, pull, liseré | ✅ | ✅ | ✅ | ✅ |
| Lumière fenêtre à gauche, fond sombre chaud | ✅ | ✅ | ✅ | ✅ |
| Expression curieuse et attentive | ⚠️ neutre | ⚠️ grave | ✅ | ⚠️ neutre |

**Diagnostic :** l'identité tient, mais l'objectif de YAS_02 (l'angle) n'est pas atteint. Avec `--iw 1.5`, la référence impose la pose de face et Midjourney a inversé la cicatrice.
**Recommandation : REFAIRE** avec le plan B prévu : `--iw 1.0`, un angle formulé plus fortement, et la cicatrice décrite par rapport à la caméra.

---

# QC — YAS_02 v2 (plan B : --iw 1.0, angle renforcé)

- task `e0c927b7-1c59-4a5c-b9e3-d602a8b642b1`, image_id `1567622146685927424`, 0,401 crédit
- Magnific : v2_1 `P3aTYWH42C` · v2_2 `CqZgjgCEEy` · v2_3 `lJX2in2gv9` · v2_4 `u5AUs9AQLD`

| Critère | v2_1 | v2_2 | v2_3 | v2_4 |
|---|---|---|---|---|
| Angle trois-quarts | ❌ presque de face, regard caméra | ⚠️ ~20°, regard hors champ | ✅ **vrai trois-quarts (~40°)**, côté droit du visage et oreille droite vers la caméra | ⚠️ ~20° |
| Cicatrice côté droit du front | ❌ côté gauche | ⚠️ bon côté mais énorme, centrale | ✅ bon côté, discrète (près de la mèche) | ❌ côté gauche |
| Ressemblance avec le MASTER | ✅ | ✅ | ✅ (paraît ~10 ans, comme le MASTER) | ✅ très bonne |
| Axe du regard (bible : gauche → droite vers le passé) | — | ❌ regarde à gauche | ✅ regarde vers la droite du cadre | ❌ regarde à gauche |
| Artefacts | ✅ | ⚠️ cicatrice « patch » | ⚠️ **liseré clair autour de l'oreille et de la joue** (effet de détourage) | ✅ |
| Lumière | ✅ | ✅ | ✅ contre-jour doré, très cinéma | ✅ |

**Recommandation : v2_3**, la seule qui remplit l'objectif (angle). Il faut d'abord corriger le liseré clair du contour (retouche Magnific ou Vary Region Midjourney ciblée), puis l'upscaler.
