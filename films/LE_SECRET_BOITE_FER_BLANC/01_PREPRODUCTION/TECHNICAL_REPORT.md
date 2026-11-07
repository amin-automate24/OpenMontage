# Rapport technique — LE SECRET DE LA BOÎTE EN FER BLANC

> Audit du 4 novembre 2026. Tout a été vérifié en lecture seule : **aucune génération, aucun crédit dépensé.**

## 1. Serveurs MCP disponibles pour ce film

| Serveur | État | Rôle prévu |
|---|---|---|
| **Magnific** | ✅ connecté · **plan gratuit, 0 crédit** | Animation (Kling, Seedance), upscale, VFX, étalonnage, **audio** |
| **Midjourney** | ✅ connecté (statut officiel à confirmer, voir §3) · solde non exposé | Références visuelles |
| ElevenLabs (restreint) | ✅ connecté | Voix, SFX, design de voix |
| Runway | ✅ connecté · 8 crédits | Secours |
| Dropbox / Google Drive | ✅ connectés | Échange de fichiers avec toi, livraison |
| Higgsfield | ❌ échec de connexion (404) | — |

## 2. Magnific — ce qui est réellement accessible

### Modèles vidéo (catalogue `video_models_list`)

| Modèle | Durée 9 s native | Résolution | Références | Points forts | Coût exact d'un plan 9 s 16:9 1080p |
|---|---|---|---|---|---|
| **Kling 3.0 Omni** (`kling-omni3`, non bêta) | ✅ (3–15 s) | 720p / 1080p / 4K | start frame + end frame, **jusqu'à 3 références personnage**, images, vidéo | Continuité des personnages, keyframes | **855 crédits** |
| Kling 3.0 (`kling-30`, bêta) | ✅ | 720p / 1080p / 4K | start/end frame, 3 réf. personnage | Même famille, un peu moins cher | 810 crédits |
| Seedance 2.5 (`bytedance-seedance-pro-2.5`, bêta, « SOTA » selon Magnific) | ✅ (4–30 s) | jusqu'à 1080p | jusqu'à 30 réf. personnage, réf. style et couleur, **52 mouvements caméra nommés** | Meilleure qualité, mouvements complexes | **7 110 crédits** |
| Seedance 2.0 (`bytedance-seedance-pro-2.0`, bêta) | ✅ | jusqu'à 4K | idem 2.0 | 4K | 6 300 crédits |
| Seedance 2.0 Mini (bêta) | ✅ | 480p / 720p | idem | Brouillons | 1 260 crédits (720p) |

**Limites importantes :**
- Chez Seedance, les **keyframes (start/end) sont incompatibles avec les références** : il faut choisir entre partir d'une image Midjourney exacte et guider par références personnage.
- Kling 3.0 Omni accepte les deux : une start frame plus des références personnage. C'est l'atout clé pour la continuité.
- Kling 4.0 / 4.0 Omni existent (jusqu'à 30 s) mais sont en bêta ; non retenus pour l'instant.

### Distinction Magnific / modèle (règle demandée)
- **Magnific** fournit : l'interface, le stockage (« creations »), l'upscale, le relight, le color grade, les VFX, l'extension de vidéo, l'estimation des coûts.
- **Kling / Seedance** fournissent : le rendu du mouvement, les durées, les références acceptées et les mouvements caméra.

### Audio via Magnific (confirmé dans l'outil, pas supposé)
| Fonction | Modèle | Coût mesuré |
|---|---|---|
| Musique | Google Lyria 3 (30 s fixes) · Lyria 3 Pro (30–180 s) · ElevenLabs Music v1/v2 (10–300 s) | ElevenLabs v2, 90 s : **1 800 crédits** |
| Effets sonores | ElevenLabs SFX (1–30 s, boucles) | 3 s : **15 crédits** |
| Voix, isolation, nettoyage | TTS, voice change, isolate, clean speech | non estimé |

## 3. Midjourney — intégration réelle

- Un connecteur « Midjourney » est installé dans la session. Il permet : imagine (V5.2 → **V8.2**), modes fast/relax/turbo, HD, upscale et variations, blend, édition, describe, récupération du seed, génération vidéo.
- **Réserve importante :** à ma connaissance, Midjourney ne publie **pas d'API publique officielle**. Ce connecteur passe donc très probablement par un service tiers que je ne peux pas vérifier. Cela correspond à la catégorie « non officielle ou fragile » que tu as exclue.
- Son outil d'aide ne documente ni `--oref` / `--cref` (Omni / Character Reference), ni `--sref`, ni `--cw` / `--ow`. Seule la référence image avec `--iw` est confirmée.

**Recommandation : procédure manuelle par défaut.**
1. Je rédige le prompt et ses paramètres.
2. Tu valides.
3. Tu lances la génération sur midjourney.com (ou Discord) avec ton compte, et tu y vérifies les paramètres disponibles dans ta version (`--oref`, `--sref`, `--seed`).
4. Tu déposes les images retenues dans un dossier Dropbox ou Drive : je les récupère, je les renomme et je les contrôle.

Si tu préfères malgré tout utiliser le connecteur, c'est ta décision : je l'utiliserai seulement sur ton accord explicite, image par image.

## 4. Récupération et organisation des fichiers

- **Toi → moi :** Dropbox ou Google Drive (lecture via MCP), ou fichiers ajoutés au dépôt Git.
- **Magnific → projet :** chaque génération est une « creation » avec une URL ; je la télécharge dans `09_MAGNIFIC_GENERATIONS/`, puis je la range dans le dossier de la séquence.
- **Images Midjourney → Magnific :** je les importe avec `creations_upload_image` pour les utiliser comme start frame ou référence.
- Les médias ne sont pas versionnés dans Git (`.gitignore`), car le conteneur est éphémère. Les prompts, fiches et rapports le sont.

## 5. Budget — le point bloquant

Magnific affiche **0 crédit**. Aucune animation ne peut être lancée sans achat de crédits.

Estimation pour 60 plans de 9 s (coûts exacts mesurés par Magnific, hors Midjourney) :

| Scénario | Calcul | Crédits |
|---|---|---|
| Tout en Kling 3.0 Omni 1080p | 60 × 855 | 51 300 |
| + marge de reprises (×1,6, réaliste en IA) | | ≈ 82 000 |
| + 6 plans héros en Seedance 2.5 au lieu de Kling | 6 × (7 110 − 855) | + 37 500 |
| Audio : 6 musiques de 90 s + ~120 SFX | 6 × 1 800 + 120 × 15 | ≈ 12 600 |
| **Total recommandé** | | **≈ 130 000 crédits** |

Le prix en euros dépend de l'offre Magnific choisie : je ne l'invente pas, il est à vérifier sur la page de tarifs. Tout en Seedance 2.5 coûterait environ 430 000 crédits avant reprises : ce n'est pas recommandé.

## 6. Ce qui reste local et gratuit
Montage, étalonnage final, mixage (−14 LUFS), titres, sous-titres, contrôle technique et export via FFmpeg, Remotion et `scripts/film_studio.py`.
