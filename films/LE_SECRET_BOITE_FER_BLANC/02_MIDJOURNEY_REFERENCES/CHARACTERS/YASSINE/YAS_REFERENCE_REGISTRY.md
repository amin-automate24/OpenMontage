# Registre des références approuvées — YASSINE

| ID | Statut | Midjourney | Seed | Fichier / Magnific | Notes |
|---|---|---|---|---|---|
| **YAS_01_MASTER** | ✅ VALIDÉ (2026-11-04) | grille task `7fee43a2-ca99-4786-a228-5c5cb18ec158` → U1 task `8f9c5094-ed1f-4cc7-a044-63686c6f9acc`, image_id `1567617911202250752`, V8.2 | 4033502968 | Magnific `lJXZ1eLgv9` · URL source `https://storage.fonedis.cc/e231b365-5d34-4682-b641-16b4e27157e3/0_0.png` (928×1232) · aperçu local `YAS_01_MASTER_preview.jpg` | Cicatrice : côté droit du front. Lumière fenêtre à gauche, fond sombre chaud |

| **YAS_02_3Q** | ✅ VALIDÉ (2026-11-04) — **usage : référence d'identité uniquement (Kling character reference), jamais image de départ** | grille v2 task `e0c927b7-1c59-4a5c-b9e3-d602a8b642b1` → U3 task `e3ac31cb-a67b-4012-87d0-e0403fc167ec`, image_id `1567623027032588288`, V8.2 | 572238788 | Magnific `rgM6NLZxtc` · URL source `https://platform2.cdn.acedata.cloud/midjourney/e3ac31cb-a67b-4012-87d0-e0403fc167ec.png` (928×1232) · aperçu `YAS_02_UPSCALE_preview.jpg` | Vrai trois-quarts, regard vers la droite du cadre. Défaut : liseré clair autour de l'oreille, de la joue et de la mâchoire |

| **YAS_02b_3Q_CLEAN** | ✅ VALIDÉ (2026-11-04) — **référence d'identité ET image de départ possible** | grille YAS_03 v1 task `14ad3568-6106-4783-890d-e8fea7f9e7ce` → U1 task `90882f88-2d85-480f-ab93-6d145109dee3`, image_id `1567631476046954496`, V8.2 | 2315460870 | Magnific `jUp3HnALD0` · URL source `https://platform2.cdn.acedata.cloud/midjourney/90882f88-2d85-480f-ab93-6d145109dee3.png` (928×1232) · aperçu `YAS_02b_3Q_CLEAN_preview.jpg` | Trois-quarts (~30°) vers la droite du cadre, regard à droite (axe de la bible), lumière venant de la droite, aucun liseré. Cicatrice non visible (côté opposé) |

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

### Règle d'usage YAS_02_3Q (décision du réalisateur, option C)
Le liseré clair (oreille → cou) n'a pas pu être corrigé : un essai Midjourney Vary Region a échoué (masque illisible), puis une retouche Magnific (110 crédits) n'a pas eu d'effet. L'image sert **uniquement** de référence d'identité. Les images de départ des plans seront de nouvelles images Midjourney composées dans les décors du film.

---

## PROMPT YAS_03 — Profil (en attente de validation)

**Rôle :** fournir aux modèles vidéo le profil de Yassine. C'est l'angle des plans où il marche, monte l'escalier ou se penche sur la boîte. Le profil est tourné **vers la droite du cadre**, conformément à l'axe de regard de la bible (de gauche à droite, vers le passé).

**Méthode :** deux images de référence (MASTER et YAS_02_3Q) pour verrouiller l'identité sous deux angles, avec `--iw 1.0`, le réglage qui a fonctionné pour YAS_02. La lumière vient de l'avant du visage (droite du cadre), sinon un profil à contre-jour serait illisible. Le liseré de détourage est exclu dans `--no`.
**Note :** de profil vers la droite, c'est le côté gauche du visage qui fait face à la caméra. La cicatrice, côté droit, ne sera donc **pas visible**, et c'est voulu.

```
https://storage.fonedis.cc/e231b365-5d34-4682-b641-16b4e27157e3/0_0.png https://platform2.cdn.acedata.cloud/midjourney/e3ac31cb-a67b-4012-87d0-e0403fc167ec.png Photorealistic cinematic character reference portrait of Yassine, an 8-year-old Moroccan boy from Fez, slim build, oval face with soft round cheeks, warm light olive-brown skin, large dark-brown almond-shaped eyes with long lashes, thick dark slightly arched eyebrows, small straight nose, short slightly wavy black hair with one loose curl on his forehead, wearing a navy-blue cotton crewneck sweater with a thin cream trim at the collar. Strict side profile facing right of frame, head and chest, the left side of his face toward the camera, looking straight ahead to the right, calm curious expression, mouth closed. Soft warm window light from the right of frame falling on his face, gentle falloff into a dark warm-grey background. 85mm lens, f/4, natural skin texture, fine 35mm film grain, true-to-life color --ar 3:4 --style raw --s 50 --iw 1.0 --no smile with teeth, makeup, jewelry, hat, text, watermark, cartoon, illustration, plastic skin, extra fingers, front view, three-quarter view, looking at camera, light outline, halo, cutout edge
```

| Paramètre | Valeur | Raison |
|---|---|---|
| Images de référence | MASTER + YAS_02_3Q (URL source Midjourney) | L'identité est verrouillée sous deux angles |
| `--iw 1.0` | — | Réglage validé sur YAS_02 v2 (assez de liberté pour tourner la tête) |
| `--no ... light outline, halo, cutout edge` | — | Évite de reproduire le défaut de YAS_02 |
| Version / mode | V8.2, fast | Identiques |
| Coût estimé | environ 0,4 crédit Midjourney | — |
