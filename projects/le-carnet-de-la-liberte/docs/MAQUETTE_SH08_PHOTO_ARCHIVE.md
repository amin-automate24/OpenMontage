# SH08 — remplacement de la photographie (MAQUETTE, NON INTÉGRÉE)
**Plan concerné** : SH08, 36,0–39,5 s dans QC3 SON2 (image affichée 36,04–39,56 s) ; gros plan carnet « AMINA — MES SOUVENIRS » + photo. Source actuelle : `references/p4/post/SH08_composite_final.png` (photo de famille **générée**, aucune archive). SH07 (30,0–36,0 s) montre la même photo en très petit, visages illisibles ; SH09 ne la montre pas.

## Photographie retenue (authentifiée)
- **Sujet** : le sultan Sidi Mohammed ben Youssef (Mohammed V) et son fils Moulay Hassan (futur Hassan II, environ 2 ans), Hôtel de Crillon, Paris.
- **Date** : 5 août 1931 (voyage officiel en France).
- **Auteur / fonds** : Agence Rol (agence de presse), n° de cliché **Rol 156948** (inscrit sur la plaque), négatif sur verre ; Bibliothèque nationale de France, département Estampes et photographie, ensemble Pho20Rol ; Gallica ark `btv1b53248904z`.
- **Fichier** : Wikimedia Commons « File:5-8-31, le sultan du Maroc et son fils Moulay Hassan - btv1b53248904z.jpg » (original 8502×6136, sha1 `b67e0103d6cd60db474a9aa974b7f9ba5deea6b3`) ; copie locale 1920 px : `references/p4/post/sh08_photo_archive/BnF_Rol_156948_btv1b53248904z_1920px.jpg` (sha1 `6b2093ed…`).
- **Droits** : domaine public (photographie de presse anonyme de 1931, mention Commons « Public domain », Copyrighted = False). Conditions BnF/Gallica : réutilisation non commerciale libre avec la mention « Source : gallica.bnf.fr / Bibliothèque nationale de France » ; une diffusion commerciale relève d'une licence BnF. Usage scolaire non commercial : conforme, crédit à prévoir au générique.

## Traitement (aucun visage généré ni retouché)
`scripts/mockup_sh08_photo_archive.py` : recadrage hors annotations d'inventaire, projection en perspective dans le tirage existant (coins 1852,726 / 2282,788 / 2108,1116 / 1502,1058 sur 2752×1536), tonalité sépia globale calée sur l'ancien tirage, vignette et grain légers. Bords déchirés, carnet, coffre et décor inchangés. Nouveau fichier : `SH08_composite_photo_BnF_Rol156948_v002.png` (l'original est conservé).
Rendu : `scripts/mockup_qc3_sh08_photo.py` (chaîne QC3, SH08 seul). Hors zone photo, image identique au master (écart moyen 1,2/255, bruit d'encodage).

## Candidats écartés
- « King of Morocco with members of his family » : scan de magazine, photographe inconnu, date contradictoire (« vers 1950 » vs visite aux États-Unis de 1957), justification de domaine public non vérifiable → provenance non authentifiée.
- « Sultan Muhammad V avec son fils Hassan II, Casablanca 1930 » : crédit AFP, domaine public revendiqué au titre du droit marocain, non vérifié.
- Anefo 904-2385 (11/10/1950, CC0) : authentique mais sans la famille.

## Points à arbitrer
1. **Époque** : 1931, antérieure au récit (1944–1956) ; aucune photo de famille des années 1950 à la provenance et aux droits vérifiés n'a été trouvée sur Commons.
2. **Récit** : le scénario décrit la photo de famille d'Amina ; un portrait du sultan gardé dans le coffre reste plausible (portraits répandus dans les foyers), mais change le sens du plan.
3. **Règle du projet** : seule l'Anefo 905-8914 était autorisée pour le visage de Mohammed V ; l'ajout de BnF Rol 156948 doit être inscrit au registre d'approbation après validation.
