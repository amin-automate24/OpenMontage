# Vignette YouTube — LE CARNET DE LA LIBERTÉ (CINÉMA FINAL) — rapport de sélection artistique (20/11/2026)
**Trois propositions, aucune validée.** Le propriétaire choisit la vignette officielle ; rien n'est téléversé ni publié. Master FINAL non modifié (SHA-256 `0f72fc9ad6f82526…`).

## Méthode (fidélité avant tout)
* Les anciennes miniatures ne sont pas utilisées. Référence = le master FINAL : les plans SH24, SH10 et SH26 y ont été revus (images de référence extraites dans `references_master_frames/`).
* **Aucune image générée, aucun crédit dépensé** : les plans du film existent en 2752×1536 (versions composites utilisées pour le montage, textes d'écran compris). Les recomposer garantit la fidélité exacte des personnages, costumes, décors, étalonnage et textes du film ; une nouvelle génération IA aurait risqué de les déformer et aurait coûté des crédits. Retouches : recadrage 16:9, mise à l'échelle 3840×2160, courbe de contraste douce, vignettage, voile sombre derrière le titre, titre en Cinzel (police du générique) avec contour et ombre. Aucun personnage, costume ni événement ajouté.
* Aucun portrait ni photo d'archive de personne réelle ; aucun nom de personne ni d'établissement ; seul texte ajouté : « LE CARNET DE LA LIBERTÉ ».

## Plans du film utilisés
| Plan | Fichier source (identique au plan du master) | SHA-256 |
|---|---|---|
| SH24 (images 3639–3788) | `references/p2/post/SH24_composite_final.png` | `fa24a4e4495801fa…` |
| SH10 (images 1264–1413) | `references/p1/post/SH10_composite_final.png` | `6b5fb88a117e61ed…` |
| SH26 (images 4089–4376) | `references/p1/SH26_fenetre_Amina_v001.png` | `5fce16b73fe6d3b5…` |

Références dans le master FINAL : image 3700 (SH24), 1330 (SH10), 4150 (SH26).

## Propositions et évaluation (1 = faible, 5 = excellent)
| Critère | A — La lueur du carnet (SH24) | B — Le carnet d'Amina (SH10) | C — Le regard d'Amina (SH26) |
|---|---|---|---|
| Fidélité aux personnages | 5 | 5 | 5 |
| Cohérence avec le master FINAL | 5 | 5 | 5 |
| Exactitude historique et symbolique | 5 (Amina en 1953, écrit « Nous garderons espoir. ») | 5 (« 11 janvier 1944 — Nous rêvions d'un Maroc libre. ») | 4 (Amina en 1955, espoir : sans repère historique explicite) |
| Impact visuel et émotionnel | 5 (lampe, visage, geste d'écriture) | 5 (découverte d'un enfant, message lisible) | 4 |
| Lisibilité mobile (360 px et 168 px) | 5 (grand titre, visage lisible) | 4 (titre plus petit ; texte du carnet lisible à 360 px) | 3 (personnage petit, titre moyen) |
| Composition et typographie | 5 | 5 | 4 |
| Absence d'éléments trompeurs | 5 | 5 | 5 |
| **Verdict** | Retenue | Retenue (recommandée) | Retenue, 3e choix |
Contrôles faits : visages, mains, costumes, objets et texte examinés à pleine taille et en simulation mobile (badge de durée YouTube en bas à droite laissé libre) ; aucune incohérence majeure ; orthographe du titre vérifiée (« LE CARNET DE LA LIBERTÉ »). Les textes manuscrits à l'écran viennent du film (« NOUS GARDERONS ESPOIR. » ; « AMINA — MES SOUVENIRS » ; « 11 JANVIER 1944 — NOUS RÊVIONS D'UN MAROC LIBRE. »).

## Recommandation argumentée
1. **B — Le carnet d'Amina (recommandée).** Elle résume le film : un enfant découvre le carnet d'Amina, « 11 janvier 1944 — Nous rêvions d'un Maroc libre ». Elle parle au public visé (élèves de 9–12 ans), annonce le sujet (l'indépendance) sans archive ni sensationnalisme, et son texte reste lisible sur mobile.
2. **A — La lueur du carnet.** La plus lisible en miniature (titre dominant, visage complet) et la plus cinématographique ; choix alternatif si la priorité est le clic en petite taille.
3. **C — Le regard d'Amina.** Image d'espoir, très fidèle, mais moins forte à petite taille.

## Spécifications
JPEG 1280×720 (16:9, qualité 93, 247–345 Ko, bien sous la limite de 2 Mo de YouTube) + version de travail PNG 3840×2160 pour chaque proposition. Script : `scripts/build_thumbnails_cinema_final.py`.

## Fichiers
`A_la_lueur_du_carnet_YOUTUBE_1280x720.jpg`, `B_le_carnet_d_Amina_YOUTUBE_1280x720.jpg`, `C_le_regard_d_Amina_YOUTUBE_1280x720.jpg` (+ versions 3840×2160 PNG), `PLANCHE_COMPARATIVE_VIGNETTES.jpg`, `references_master_frames/`, `SHA256SUMS_VIGNETTES.txt`, ce rapport.
