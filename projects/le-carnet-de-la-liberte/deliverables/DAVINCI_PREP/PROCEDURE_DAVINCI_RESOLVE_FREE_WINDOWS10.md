# LE CARNET DE LA LIBERTÉ — préparation DaVinci Resolve Free (Windows 10) — NON FINAL
Aucune de ces étapes n'a pu être testée depuis la session (pas d'accès au PC) : à exécuter et vérifier sur le poste.

## 1. Constats techniques
- **Couleur** : les images ont été encodées avec la matrice **BT.601** (vérifié : le rouge du drapeau 193/39/45 n'est exact qu'en décodage 601 ; en 709 il devient 203/53/40). Les masters **v3** portent désormais le balisage exact : primaires BT.709, transfert BT.709, matrice **SMPTE 170M (601)**, plage limitée. Images et son identiques aux v2 (MD5 vérifiés). Les baliser « Rec.709 » complet aurait faussé les couleurs.
- **Son** : seul le mix stéréo QC2 SON2 correspond au son validé ; aucune piste séparée fidèle. → ne pas remixer dans Fairlight.

## 2. Fichiers
| Fichier | Rôle |
|---|---|
| `LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v3_1080p.mp4` (206,5 Mo) | Source de la timeline légère (image + son validé) |
| `CARNET_TIMELINE_LEGERE_v3.fcpxml` (FCPXML 1.8) | 38 plans + générique = 39 clips coupés aux limites exactes (7475 images = 04:59:00), un marqueur par plan (transition, lieu) |
| `CARNET_TIMELINE_COMPLETE_PRORES_gabarit.fcpxml` | Gabarit pour clips ProRes par plan (non générés) + mix WAV |
| `NUIT1953_SH21-23_releve_doux.cube` | LUT 33³ = courbe du comparatif nocturne (écart ≤ 1/255 vérifié) |
| `LISTE_PLANS_38_PLUS_GENERIQUE.json` | Début/durée en images de chaque plan, transitions |
| `LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v3_FR.srt` | Sous-titres corrigés (cue 10 v2) |
Fondus 0,5 s intégrés à l'image (SH06, 07, 12, 17, 20, 21, 25, 27, 29, 33, 35) : ne pas ajouter de transitions dans Resolve.

## 3. Procédure (Resolve Free 18 ou plus récent)
1. Créer `C:\LE_CARNET_DE_LA_LIBERTE\MEDIA\` et y copier le MP4 CINÉMA v3 (chemin attendu par le FCPXML ; sinon « Relink » à l'étape 4).
2. Nouveau projet → Paramètres du projet : 1920×1080, **25 ips** (timeline et lecture), science couleur DaVinci YRGB, espace timeline Rec.709 Gamma 2.4.
3. Fichier → Importer → **Timeline…** → `CARNET_TIMELINE_LEGERE_v3.fcpxml` (laisser l'import automatique des sources).
4. Si un clip est « hors ligne » : clic droit dans la médiathèque → Relink → dossier MEDIA.
5. Contrôle : 39 clips, fin à **04:59:00**, marqueurs SH01…GENERIQUE ; lecture des raccords SH05/06 et SH32/33.
6. LUT nuit (seulement si validée) : copier le `.cube` dans `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\LUT\`, Paramètres du projet → Gestion des couleurs → Mettre à jour les listes ; page Couleur → clips SH21, SH22, SH23 uniquement → clic droit sur le nœud → LUT → `NUIT1953…`. Comparer au comparatif.
7. Étalonnage complémentaire facultatif : uniquement plan par plan, à l'œil, sans traitement automatique global.
8. Fairlight : ne rien modifier.
9. Export (Livraison) : MP4 H.264, 1920×1080, 25 ips, qualité élevée (≥ 20 Mb/s), audio AAC 48 kHz ; nom `…_DAVINCI_NON_FINAL.mp4`. Version scolaire : Fichier → Importer → Sous-titres (SRT), puis « Graver dans la vidéo » à l'export.
10. Me renvoyer le fichier : contrôle durée (299,000 s), images vs CINÉMA v3, son. Resolve réencode l'AAC : pour garder le son validé intact, je pourrai réassocier la piste audio d'origine sans réencodage.

## 4. Option ProRes par plan (non générée) — estimation
| Option | Stockage | Durée de préparation ici | Intérêt |
|---|---|---|---|
| A. Timeline légère (MP4 v3) | ≈ 0,21 Go | prête | étalonnage plan par plan suffisant ; une génération H.264 de plus à l'export |
| B. ProRes 422 LT par plan | ≈ 3,2 Go | ≈ 20–30 min + envoi | meilleure marge d'étalonnage |
| C. ProRes 422 | ≈ 4,6 Go | ≈ 20–30 min + envoi | idem, plus lourd |
| D. ProRes 422 HQ | ≈ 6,9 Go | ≈ 25–35 min + envoi | qualité maximale, lourd pour Dropbox |
| E. ProRes LT seulement SH21–SH23 | ≈ 0,3 Go | ≈ 5 min | utile si seule la nuit est étalonnée |
Recommandation : A (+ E si l'étalonnage de la nuit est retenu).
