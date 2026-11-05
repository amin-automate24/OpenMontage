# Fiche des objets narratifs

> Statut : **PROPOSITION, en attente de validation.** Les objets suivent la bible de production (section D).

## Ordre de production

| ID | Objet | Rôle | Méthode |
|---|---|---|---|
| PRP_01 | **Boîte en fer blanc fermée** | Le seuil du film | Génération (référence principale de l'objet) |
| PRP_02 | Boîte ouverte, avec les 3 objets | La révélation (S2) | Élargissement ou retouche à partir de PRP_01, pour garder exactement la même boîte |
| PRP_03 | Drapeau marocain plié, décoloré | La nation | Génération |
| PRP_04 | Coran de poche | La foi (traité avec respect) | Génération |
| PRP_05 | Sable doré (dans un petit tissu noué) | Le déclencheur magique | Génération |
| PRP_06 | Chapelet en bois du grand-père | S1 | Génération |

**Principe de cohérence :**
- Tous les objets sont photographiés **dans la même lumière** : fenêtre chaude à gauche, fond sombre brun cèdre, l'univers du grenier.
- Tous sont cadrés **à une échelle lisible**, avec la même optique macro.
- La boîte ouverte (PRP_02) est **dérivée de la boîte fermée**. On ne régénère jamais une autre boîte.

---

## PRP_01 : boîte en fer blanc fermée

**Description verrouillée (bible D) :**
- boîte rectangulaire d'environ 25 × 18 × 8 cm, couvercle à charnière ;
- fer blanc lithographié délavé : motif floral ancien vert et bordeaux, **sans aucune marque ni texte lisible** ;
- rouille aux angles et le long des arêtes, rayures, petites bosses ;
- une fine couche de poussière sur le couvercle, avec des traces de doigts discrètes (signe qu'on l'a déjà ouverte, il y a longtemps).

**Descripteur canonique (anglais) :**
```
an old rectangular tin box about 25 by 18 by 8 centimeters with a hinged lid, faded lithographed tinplate with a vintage floral pattern in muted green and burgundy, no brand and no readable text, rust spots on the corners and along the edges, small dents and fine scratches, a thin layer of dust on the lid
```

**Prompt Midjourney :**
```
Photorealistic cinematic prop reference photograph of an old rectangular tin box about 25 by 18 by 8 centimeters with a hinged lid, closed, faded lithographed tinplate with a vintage floral pattern in muted green and burgundy, no brand and no readable text, rust spots on the corners and along the edges, small dents and fine scratches, a thin layer of dust on the lid with faint old fingerprints. Three-quarter top view, the box resting on an old cedar wood plank, centered, the whole box in frame. Soft warm window light from the left with gentle dust particles in the beam, dark warm brown background falling into shadow. 100mm macro lens, f/5.6, rich metal and dust texture, fine 35mm film grain, true-to-life color --ar 4:3 --style raw --s 50 --no text, letters, logo, brand, label, writing, numbers, watermark, cartoon, illustration, plastic, new shiny metal
```

| Paramètre | Valeur | Raison |
|---|---|---|
| `--ar 4:3` | — | Format naturel d'un objet rectangulaire vu de trois-quarts |
| Planche de cèdre | — | Ancre l'objet dans l'univers du grenier sans créer de décor complet |
| `--no text, letters, logo…` | — | Les boîtes anciennes portent souvent des inscriptions, que Midjourney invente et déforme |
| Version / mode | V8.2, fast | Comme pour les personnages |
| Coût estimé | environ 0,4 crédit Midjourney | — |

**Résultat attendu :** 4 boîtes anciennes crédibles, motif floral vert et bordeaux délavé, rouille aux angles, poussière visible dans un rai de lumière, sans aucun texte.

---

## Registre
| ID | Statut | Midjourney | Seed | Magnific | Notes |
|---|---|---|---|---|---|
| **PRP_01_MASTER** | ✅ VALIDÉ (2026-11-04) | task `8ab3756e…` v1 → U1 (task `78f9c3a8-0a41-460a-809e-eb3cf7f2abd5`), image_id `1567652509986586624` | 3943399178 | `MBgFtiCDCm` (1232×928) · aperçu `PRP_01_MASTER_preview.jpg` | Motif floral vert/bordeaux lisible, rouille aux arêtes, trace de doigt dans la poussière, aucun texte |

| **PRP_02_OPEN** | ✅ VALIDÉ v2 (2026-11-05) — sable corrigé | — (Midjourney Vary Region refusé : taille de canevas paysage) | — | **`cpj7UuQ0eP`** (Nano Banana 2.1, correction du sable sur la v1 `iGQ1qrd3uK`, 65 + 65 crédits Magnific) · aperçu `PRP_02_OPEN_v2_preview.jpg` | Même boîte que PRP_01. Drapeau, Coran (fermé, sans texte lisible), sable fin et granuleux dans un tissu blanc noué, quelques grains échappés jusqu'à la planche. Réserve mineure acceptée : tache de poussière répétée à l'intérieur du couvercle. v1 `iGQ1qrd3uK` remplacée |

---

## PRP_02 : boîte ouverte avec les trois objets (proposition)

**Méthode :** retouche par zone sur **PRP_01_MASTER**. Le masque couvre le couvercle et l'espace au-dessus de la boîte, où le couvercle relevé va se dessiner. Le corps de la boîte (flancs et motif) **reste identique, pixel pour pixel**. Le masque est un rectangle 1 bit, transmissible sans erreur. Aperçu : `PRP_02_mask_overlay.jpg`.

**Contenu (bible D) :** drapeau marocain plié en triangle, rouge passé, étoile verte visible ; petit Coran de poche à couverture verte usée, posé avec soin, fermé ; petit tissu de coton noué contenant du sable doré, légèrement entrouvert.

**Prompt de retouche :**
```
the same old tin box now with its hinged lid opened upright at the back, showing the matching faded green and burgundy floral pattern on the inside of the lid, inside the box: a folded faded red Moroccan flag with its green star visible, a small closed pocket Quran with a worn green cover placed with care, and a small knotted cotton cloth bundle slightly open revealing fine glowing golden sand, soft warm window light from the left, dust particles in the beam, photorealistic, no text
```
**Coût :** environ 0,4 crédit Midjourney.
