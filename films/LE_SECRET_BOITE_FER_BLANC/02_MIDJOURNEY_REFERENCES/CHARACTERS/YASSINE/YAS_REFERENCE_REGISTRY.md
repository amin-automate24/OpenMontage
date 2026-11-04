# Registre des références approuvées — YASSINE

| ID | Statut | Midjourney | Seed | Fichier / Magnific | Notes |
|---|---|---|---|---|---|
| **YAS_01_MASTER** | ✅ VALIDÉ (2026-11-04) | grille task `7fee43a2-ca99-4786-a228-5c5cb18ec158` → U1 task `8f9c5094-ed1f-4cc7-a044-63686c6f9acc`, image_id `1567617911202250752`, V8.2 | 4033502968 | Magnific `lJXZ1eLgv9` · URL source `https://storage.fonedis.cc/e231b365-5d34-4682-b641-16b4e27157e3/0_0.png` (928×1232) · aperçu local `YAS_01_MASTER_preview.jpg` | Cicatrice : côté droit du front. Lumière fenêtre à gauche, fond sombre chaud |

| **YAS_02_3Q** | ✅ VALIDÉ (2026-11-04) — **usage : référence d'identité uniquement (Kling character reference), jamais image de départ** | grille v2 task `e0c927b7-1c59-4a5c-b9e3-d602a8b642b1` → U3 task `e3ac31cb-a67b-4012-87d0-e0403fc167ec`, image_id `1567623027032588288`, V8.2 | 572238788 | Magnific `rgM6NLZxtc` · URL source `https://platform2.cdn.acedata.cloud/midjourney/e3ac31cb-a67b-4012-87d0-e0403fc167ec.png` (928×1232) · aperçu `YAS_02_UPSCALE_preview.jpg` | Vrai trois-quarts, regard vers la droite du cadre. Défaut : liseré clair autour de l'oreille, de la joue et de la mâchoire |

| ~~YAS_02b_3Q_CLEAN~~ | ❌ **RETIRÉE (2026-11-04)** — le réalisateur constate qu'elle ne ressemble pas au MASTER (visage plus rond et plus jeune, sourcils plus arqués). Ne pas utiliser | grille YAS_03 v1 task `14ad3568-6106-4783-890d-e8fea7f9e7ce` → U1 task `90882f88-2d85-480f-ab93-6d145109dee3`, image_id `1567631476046954496`, V8.2 | 2315460870 | Magnific `jUp3HnALD0` · URL source `https://platform2.cdn.acedata.cloud/midjourney/90882f88-2d85-480f-ab93-6d145109dee3.png` (928×1232) · aperçu `YAS_02b_3Q_CLEAN_preview.jpg` | Trois-quarts (~30°) vers la droite du cadre, regard à droite (axe de la bible), lumière venant de la droite, aucun liseré. Cicatrice non visible (côté opposé) |

| **YAS_04_FULLBODY** | ✅ VALIDÉ (2026-11-04) — référence costume complet et silhouette | Chaîne : MASTER → zoom ×2 (task `397e826a…`) v4 → U4 → zoom ×2 (task `cd0d8241…`) v3 → U3 → pan_down (task `d4ae321b…`) v1 → U1 → Vary Region rectangle (task `26deff0f…`) v1 → U1 (task `75f39014-6d4c-4585-82b5-899f234b4fd1`), image_id `1567636811583324160` | — | Magnific `ksTNOsY16B` · URL source `https://platform2.cdn.acedata.cloud/midjourney/75f39014-6d4c-4585-82b5-899f234b4fd1.png` (784×1552) · aperçu `YAS_04_FULLBODY_preview.jpg` | Visage identique au MASTER (non régénéré). Pantalon beige, baskets blanches usées. Fin cadre blanc extérieur à rogner avant usage comme image de départ |

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

### YAS_03 — Profil : PASSÉ (décision du réalisateur, 2026-11-04)
La v1 n'a pas donné de profil (trois-quarts 20–30°). Pas de nouvel essai : les modèles vidéo s'appuieront sur MASTER, YAS_02 et YAS_02b.

---

## PROMPT YAS_04 — Vue en pied (en attente de validation)

**Rôle :** verrouiller le **costume complet** (pull marine à liseré crème, pantalon de toile beige, baskets blanches usées), les proportions d'un enfant de 8 ans et la silhouette. Kling et Seedance en auront besoin pour tous les plans larges : escalier, grenier, marche dans la fresque.

**Méthode :**
- **Une seule référence (MASTER) avec `--iw 0.5`.** Leçon de YAS_02 et YAS_03 : une référence forte impose aussi le cadrage. Ici, elle tirerait l'image vers un portrait serré au lieu d'une vue en pied.
- **Le cadrage en pied est décrit explicitement** (« de la tête aux pieds, chaussures visibles ») et le portrait serré est exclu dans `--no`.
- **Même studio que le MASTER :** fond gris chaud, lumière de fenêtre venant de la gauche.
- Le descripteur canonique reste inchangé, cicatrice comprise, pour la cohérence, même si elle sera minuscule à cette échelle.

```
https://storage.fonedis.cc/e231b365-5d34-4682-b641-16b4e27157e3/0_0.png Photorealistic cinematic full-body character reference of Yassine, an 8-year-old Moroccan boy from Fez, slim build, average height for his age, oval face with soft round cheeks, warm light olive-brown skin, large dark-brown almond-shaped eyes with long lashes, thick dark slightly arched eyebrows, small straight nose, short slightly wavy black hair with one loose curl on his forehead, a small pale scar on the right side of his forehead above his right eyebrow, wearing a navy-blue cotton crewneck sweater with a thin cream trim at the collar, beige cotton canvas trousers, worn white sneakers. Full body from head to toe, shoes fully visible with floor space below, standing naturally facing the camera, weight slightly on one leg, arms relaxed at his sides, calm curious expression. Soft warm window light from the left, plain warm-grey studio backdrop and floor, soft contact shadow. 50mm lens, f/5.6, natural skin and fabric texture, fine 35mm film grain, true-to-life color --ar 2:3 --style raw --s 50 --iw 0.5 --no close-up, portrait crop, cropped feet, cropped head, smile with teeth, makeup, jewelry, hat, text, watermark, cartoon, illustration, plastic skin, extra fingers, light outline, halo, cutout edge
```

| Paramètre | Valeur | Raison |
|---|---|---|
| Référence | MASTER seule, `--iw 0.5` | Identité sans imposer le cadrage du portrait |
| `--ar 2:3` | vertical | Format naturel d'une silhouette debout |
| 50 mm, f/5.6 | — | Peu de déformation, silhouette nette de la tête aux pieds |
| `--no close-up, portrait crop, cropped feet...` | — | Force un cadrage complet |
| Version / mode | V8.2, fast | Identiques |
| Coût estimé | environ 0,4 crédit Midjourney | — |

**Résultat attendu :** 4 vues en pied du même garçon, chaussures visibles, costume complet lisible, proportions crédibles pour un enfant de 8 ans.
**Point de vigilance :** à `--iw 0.5`, la ressemblance du visage peut baisser. Elle sera vérifiée en priorité face au MASTER.

| **YAS_05_TURNAROUND_SHEET** | ✅ **VALIDÉ v2** (2026-11-04) | Montage local, sans génération : YAS_04 (cadre blanc rogné) + MASTER + YAS_02 (v2, YAS_02b retirée) | — | `YAS_05_TURNAROUND_SHEET.jpg` (2601×1060, assemblé à partir des aperçus 1024 px) — non versionné | Document de référence humain (bible, continuité). Pour Kling, les références restent passées séparément (jusqu'à 3 références personnage). L'envoi vers Magnific est impossible tant que ak-data.magnific.com est bloqué |

---

## PROPOSITION YAS_06 — Expressions (en attente de validation)

**Rôle :** fixer les 5 émotions clés de Yassine dans le film, sur **son visage exact**.

| ID | Expression | Séquence | Consigne (anglais) |
|---|---|---|---|
| YAS_06a | Émerveillement | S3–S4 (le sable, la fresque) | eyes wide open with wonder, lips slightly parted, eyebrows raised, soft golden light reflected in his eyes |
| YAS_06b | Curiosité | S1–S2 (le grenier) | intrigued look, one eyebrow slightly raised, head subtly tilted, lips closed |
| YAS_06c | Inquiétude légère | S3 (la transformation) | slightly worried, brows drawn together, lips pressed, eyes searching |
| YAS_06d | Fierté | S4–S5 (le grand-père jeune) | proud gentle closed-mouth smile, chin slightly up, shining eyes |
| YAS_06e | Émotion retenue | S6 (la transmission) | moved, glistening eyes holding back tears, trembling faint smile |

**Méthode :** même technique qui a réussi pour YAS_04, à savoir une **retouche de zone (Vary Region) sur YAS_01_MASTER**. On garde intacts les cheveux, le pull, la lumière et le fond, et seule la zone des traits du visage (yeux, sourcils, bouche) est régénérée selon la consigne. Le masque est un rectangle 1 bit (environ 500 caractères, transmission fiable). Les 4 propositions par expression permettent de choisir celle qui ressemble le plus.
**Limite assumée :** contrairement à YAS_04, le visage est ici redessiné, donc une légère dérive d'identité est possible. Elle sera contrôlée face au MASTER à chaque fois.
**Déroulé :** 1 expression test (YAS_06a, émerveillement, l'émotion centrale du film) → validation → les 4 autres.
**Coût :** upscale du MASTER déjà fait ; environ 0,4 crédit par expression, soit environ 2 crédits Midjourney pour les 5.
