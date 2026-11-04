# Registre des références approuvées — YASSINE

| ID | Statut | Midjourney | Seed | Fichier / Magnific | Notes |
|---|---|---|---|---|---|
| **YAS_01_MASTER** | ✅ VALIDÉ (2026-11-04) | grille task `7fee43a2-ca99-4786-a228-5c5cb18ec158` → U1 task `8f9c5094-ed1f-4cc7-a044-63686c6f9acc`, image_id `1567617911202250752`, V8.2 | 4033502968 | Magnific `lJXZ1eLgv9` · URL source `https://storage.fonedis.cc/e231b365-5d34-4682-b641-16b4e27157e3/0_0.png` (928×1232) · aperçu local `YAS_01_MASTER_preview.jpg` | Cicatrice : côté droit du front. Lumière fenêtre à gauche, fond sombre chaud |

| **YAS_02_3Q** | ✅ VALIDÉ (2026-11-04) — retouche du liseré à décider | grille v2 task `e0c927b7-1c59-4a5c-b9e3-d602a8b642b1` → U3 task `e3ac31cb-a67b-4012-87d0-e0403fc167ec`, image_id `1567623027032588288`, V8.2 | 572238788 | Magnific `rgM6NLZxtc` · URL source `https://platform2.cdn.acedata.cloud/midjourney/e3ac31cb-a67b-4012-87d0-e0403fc167ec.png` (928×1232) · aperçu `YAS_02_UPSCALE_preview.jpg` | Vrai trois-quarts, regard vers la droite du cadre. Défaut : liseré clair autour de l'oreille, de la joue et de la mâchoire |

---

## PROMPT YAS_02 — Portrait trois-quarts (en attente de validation)

**Rôle :** donner aux modèles vidéo l'angle le plus fréquent du film (Yassine qui regarde un objet ou une personne hors champ), en gardant l'identité de YAS_01_MASTER.

**Méthode :** même éclairage et même fond que la référence principale, pour isoler une seule variable : l'angle. Le cadrage est un peu plus large (jusqu'à la poitrine).

```
https://storage.fonedis.cc/e231b365-5d34-4682-b641-16b4e27157e3/0_0.png Photorealistic cinematic character reference portrait of Yassine, an 8-year-old Moroccan boy from Fez, slim build, oval face with soft round cheeks, warm light olive-brown skin, large dark-brown almond-shaped eyes with long lashes, thick dark slightly arched eyebrows, small straight nose, short slightly wavy black hair with one loose curl on his forehead, a small pale scar on the right side of his forehead above his right eyebrow, wearing a navy-blue cotton crewneck sweater with a thin cream trim at the collar. Three-quarter view, head and chest, head turned about 45 degrees to his left so the right side of his face is toward the camera, eyes looking just past the camera, calm attentive curious expression, mouth closed. Soft warm window light from the left of frame, gentle falloff into a dark warm-grey background. 85mm lens, f/4, natural skin texture, fine 35mm film grain, true-to-life color --ar 3:4 --style raw --s 50 --iw 1.5 --no smile with teeth, makeup, jewelry, hat, text, watermark, cartoon, illustration, plastic skin, extra fingers
```

| Paramètre | Valeur | Raison |
|---|---|---|
| Image prompt | URL de YAS_01_MASTER en tête de prompt | Le connecteur ne documente pas `--oref` ; l'image prompt est la méthode de référence confirmée |
| `--iw 1.5` | poids d'image élevé | Garde le visage, la coiffure et le pull ; au-delà de 2, Midjourney risque de recopier l'angle de face |
| Version | V8.2, mode fast | Identique à YAS_01 |
| `--ar 3:4 --style raw --s 50` | identiques à YAS_01 | Cohérence du rendu |
| Plan B | si la tête reste de face : `--iw 1.0` ; si l'identité dérive : `--iw 2` | — |

**Résultat attendu :** 4 portraits trois-quarts d'un garçon reconnaissable comme celui de YAS_01_MASTER, cicatrice visible côté caméra, même lumière dorée venant de la gauche.
**Coût estimé :** environ 0,4 crédit Midjourney, comme la grille YAS_01.

## PROMPT YAS_02 v2 (REFAIRE validé le 2026-11-04) — task `e0c927b7-1c59-4a5c-b9e3-d602a8b642b1`
Changements par rapport à v1 : `--iw 1.0` ; angle « three-quarter profile, face turned 45 degrees toward camera left, the right cheek and right ear clearly visible, eyes looking off-frame to the left » ; cicatrice « on the side of his forehead facing the camera » ; ajout de `front view, looking at camera` dans `--no`.
