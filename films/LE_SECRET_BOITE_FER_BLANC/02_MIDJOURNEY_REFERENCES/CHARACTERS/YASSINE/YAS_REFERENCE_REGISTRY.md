# Registre des références approuvées — YASSINE

| ID | Statut | Midjourney | Seed | Fichier / Magnific | Notes |
|---|---|---|---|---|---|
| **YAS_01_MASTER** | ✅ VALIDÉ (2026-11-04) | grille task `7fee43a2-ca99-4786-a228-5c5cb18ec158` → U1 task `8f9c5094-ed1f-4cc7-a044-63686c6f9acc`, image_id `1567617911202250752`, V8.2 | 4033502968 | Magnific `lJXZ1eLgv9` · URL source `https://storage.fonedis.cc/e231b365-5d34-4682-b641-16b4e27157e3/0_0.png` (928×1232) · aperçu local `YAS_01_MASTER_preview.jpg` | Cicatrice : côté droit du front. Lumière fenêtre à gauche, fond sombre chaud |

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
