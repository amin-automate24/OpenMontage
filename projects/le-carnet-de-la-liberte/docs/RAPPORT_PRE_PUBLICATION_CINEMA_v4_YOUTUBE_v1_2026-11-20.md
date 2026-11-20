# LE CARNET DE LA LIBERTÉ — CINÉMA v4 — Rapport de pré-publication YouTube (v1, 20/11/2026)
**VERDICT : RELEASE BLOCKED — ACTION REQUIRED** · Statut du film : NON FINAL · Aucune publication, aucun envoi, aucun rendu, aucune dépense.

## 0. Source de référence (vérifiée)
`LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v4_1080p.mp4` — SHA-256 local `f619676bad01381460f20c2970f17297eb414a42cb5ace297b717a5b7dadb92b` = valeur attendue. Copie Dropbox : taille 209 678 194 octets identique ; empreinte Dropbox enregistrée à l'envoi (19/11) identique à celle du fichier local. Le jeton Dropbox d'envoi a expiré et son renouvellement a été refusé : la copie n'a pas été re-téléchargée pour un nouveau SHA-256 complet. SRT v4 : SHA-256 `2d9b2afa…` (copie octet pour octet du SRT v3).

**Mesuré vs regardé/écouté.** Tout ce qui suit est soit une *mesure automatique* (FFmpeg, scripts), soit une *inspection d'images fixes échantillonnées* (≈ 60 images sur 7 475). Je n'ai fait **aucun visionnage continu ni aucune écoute**. Seule la déclaration du responsable du projet (PV du 19/11) atteste une écoute/visionnage intégral — de **SCOLAIRE v4**, pas de CINÉMA v4.

## 1. Validation artistique ciblée
| Point | Constat | Nature |
|---|---|---|
| Lien CINÉMA ↔ SCOLAIRE | Audio décodé de CINÉMA v4 **identique** à celui de SCOLAIRE v4 (MD5 `d962bed6…` des deux). Image : hors fenêtres de sous-titres, écart = bruit de codage (PSNR ≥ 51,6 dB) ; générique identique (99 dB). | mesuré |
| SH21–SH23 (nuit 1953) | Planche examinée : ambiance froide cohérente sur SH21→SH23 ; fondu 1953→SH21 sans saut ; coupe SH23→SH24 vers la lampe chaude, motivée (saut de luminance 16 → 5). Aucun défaut perceptible sur les images vues. | images fixes + mesure |
| Ouverture | **Pas de carton-titre** : le film démarre à l'image 0 directement sur la classe, plein éclairage, sans fondu d'entrée ; le titre n'apparaît qu'au générique de fin. Pas un défaut, mais une présentation moins « professionnelle » pour YouTube. Amélioration **facultative** (carton 3–4 s ou fondu d'entrée) = nouveau rendu → autorisation requise. | images fixes |
| Générique | 3 cartons lisibles sur les images contrôlées ; crédits Anefo et BnF présents ; générique identique à celui validé. | images fixes |
| Son | Mesures seulement : −16,1 LUFS intégré, crête vraie −1,1 dBFS, LRA 15,8 LU (passages doux ≈ −30 LUFS). Intelligibilité des dialogues, équilibre voix/musique/bruitages, fin : **non vérifiés par moi** ; couverts uniquement par la déclaration d'écoute de SCOLAIRE v4 (même piste). | mesuré / déclaré |
| Sous-titres (SRT) | 32 répliques, UTF-8 sans BOM, numérotation continue, aucun chevauchement, durées 1,05–6,0 s, **aucune > 17 car/s**, orthographe relue (aucune faute), espaces insécables avant ? ! :. Réserve mineure : réplique 15, une ligne de 44 car. (> 42 recommandés), apostrophes droites partout (cohérent). Synchronisation mesurée contre le stem de dialogue : début de réplique médian −0,06 s, fin médiane +0,77 s ; 28/32 répliques à −0,66…+0,29 s ; les 4 autres sont des répliques de continuation d'une même phrase (artefact de mesure). | mesuré + relu |

## 2. Droits — porte obligatoire
### 2.1 SH08 — BnF / Agence Rol, réf. Rol 156948 : **BLOQUANT (conditions de réutilisation non établies)**
**Identification (source officielle, notice Gallica lue le 20/11/2026, https://gallica.bnf.fr/ark:/12148/btv1b53248904z)** : « 5-8-31, le sultan du Maroc et son fils Moulay Hassan : [photographie de presse] / [Agence Rol] » ; auteur : Agence Rol (commanditaire) ; couverture 5 août 1931 ; négatif verre 13 × 18 cm ; « Référence bibliographique : Rol, 156948 » ; source BnF, Estampes et photographie, EI-13 (1781) ; collection « Photographies de l'Agence Rol » ; mis en ligne 27/11/2022 ; notice catalogue cb47065604x ; champ **Droits : « domaine public »**.

**Conditions de réutilisation (textes officiels lus le 20/11/2026)** :
* Gallica, *Conditions d'utilisation* (mise à jour 13/12/2021) : réutilisation **non commerciale libre et gratuite** avec la mention « Source gallica.bnf.fr / Bibliothèque nationale de France » (ou « / BnF ») ; réutilisation **commerciale payante, sous licence** — définie comme « la revente de contenus sous forme de produits élaborés ou de fourniture de service ou toute autre réutilisation des contenus générant directement des revenus » ; pour un support de publication commercial : utilisation.commerciale@bnf.fr ; conditions régies par le droit français, vérification de conformité à la charge de l'utilisateur pour un autre pays.
* BnF, page *Reproduction of documents* : « **Commercial use** is deemed to mean **any use of documents conserved at the BnF, whether or not they are in the public domain**, in … an **audiovisual production**, a paying service or product … or a promotional or commercial medium » ⇒ autorisation et redevance ; « Non-commercial use … is free of charge, providing the source is acknowledged » ; **« The use of documents for publications for primary and secondary education … is not free of charge. »**
* Gallica, fenêtre de téléchargement : pour une image destinée à « une production audiovisuelle … ou support promotionnel ou commercial », consulter la page d'achat de reproduction.

**Analyse.** Le statut *de droit d'auteur* est cohérent avec le domaine public (photographie de presse d'agence de 1931 ; Gallica l'indique). Mais **la BnF distingue ce statut de ses conditions de réutilisation**, et ses deux textes divergent : la définition de Gallica (revenus directs) pourrait laisser une publication gratuite et non monétisée dans le « non commercial » ; la définition institutionnelle de la BnF classe toute « production audiovisuelle » comme usage commercial même pour un document du domaine public, et exclut de la gratuité les publications pour l'enseignement primaire/secondaire. Ce film est une production audiovisuelle éducative destinée à des élèves du primaire, diffusée sur une plateforme publique. **Je ne peux pas conclure à la gratuité ni à la suffisance de la seule mention de source.** Aucune confirmation écrite de la BnF n'existe au dossier. Incertitudes restantes : monétisation ou non de la chaîne ; qualification du film (audiovisuel/éducation) ; tarif éventuel ; périmètre exact de la « publication pour l'enseignement ». *(Une projection privée en classe n'est pas une publication en ligne, mais le même texte BnF est à signaler pour la séance du 20/11.)* Aucune conclusion juridique définitive n'est donnée ici.

**Alternatives licites (proposées, non appliquées — chacune est une décision créative/juridique du propriétaire)**
1. **Demande écrite à la BnF** (utilisation.commerciale@bnf.fr, copie reproduction@bnf.fr) : confirmer le régime pour (a) projection en classe, (b) publication YouTube gratuite non monétisée, et le crédit exact ; obtenir licence/exonération et tarif le cas échéant. *Brouillon en §6.*
2. **Version YouTube sans la photo BnF** : remettre dans SH08 l'ancienne photo fictive générée (celle d'avant v003b) ou un accessoire neutre ; supprimer la ligne de crédit BnF. Nouveau rendu du générique et de SH08 ⇒ autorisation requise.
3. **Photo Anefo CC0 seule** (déjà autorisée, SH27–28) recadrée dans le cadre de SH08, si le propos narratif le permet (recomposition à valider artistiquement).
4. *(Écartée)* Flouter les visages : cela reste une reproduction de l'image BnF et ne lève pas la question.

### 2.2 Autres matériaux protégés
| Élément | Preuve au dossier | Statut |
|---|---|---|
| Musique « Possible Dreams », Eugenio Mininni (Mixkit n° 599) | Licence « Mixkit Stock Music Free License » archivée (17/11) : vidéos YouTube, usage commercial et éducatif autorisés ; interdits : Content ID, redistribution seule de la piste ; attribution non exigée | **CLEARED** (risque résiduel : réclamation Content ID erronée → contester via team@mixkit.co avec la licence archivée) |
| 14 bruitages Mixkit | « Mixkit Sound Effects Free License » archivée ; YouTube/éducatif autorisés | **CLEARED** |
| Portraits Anefo 905-8914 (Nationaal Archief) | Fiche Commons archivée (oldid 1257609662) + copie + empreinte ; CC0 1.0 ; crédit présent | **CLEARED** |
| Polices du générique (Cinzel, Cormorant Garamond, Amiri) | Licences OFL archivées (`assets/fonts/ofl/`) | **CLEARED** |
| Drapeaux | Vectoriels dessinés localement | sans objet |
| **Voix des personnages (ElevenLabs)** | Journal : forfait « ElevenLabs Starter » ; page tarifs publique (20/11) : Starter inclut « Commercial License ». Mais le projet note lui-même « licence … des voix de la bibliothèque non vérifiés » ; **preuve du forfait actif au 17/11 et conditions des voix précises (ex. « Julia », « Timothée – Jeune Narrateur Calme ») non archivées** ; compteur d'un écart de 23 car. non expliqué | **UNVERIFIED** (documentaire) |
| **Images (Magnific, modèle « Nano Banana 2.1 »)** | Docs publiques Magnific : forfaits payants = licence commerciale pour contenus IA ; forfait « Plus » cité dans le projet ; **preuve du forfait/des conditions à la date de génération non archivée** | **UNVERIFIED** (documentaire) |
| Archives sonores, enregistrements tiers | Aucun identifié dans le film (ambiances = Mixkit/génération locale) | sans objet |

## 3. Adéquation technique à YouTube — **PASS**
H.264 High niveau 4.0, yuv420p, 1920×1080, 25 ips constant, GOP 2 s, 5,4 Mb/s (YouTube recommande ≈ 8 Mb/s en 1080p SDR : acceptable, YouTube ré-encode), AAC-LC stéréo 48 kHz 183 kb/s, atome `moov` en tête (faststart), 16:9 pixels carrés, 299 s. Couleur : primaires/transfert BT.709, matrice SMPTE 170M, plage limitée = encodage réel (décision documentée du 19/11). Sonie −16,1 LUFS : YouTube n'abaisse que les contenus plus forts (cible ≈ −14) → pas de modification. Réserve : contrôler l'aspect couleur sur la version traitée 1080p après envoi privé.

## 4. Paquet de publication (brouillons — rien publié)
**Titre** : *Le Carnet de la Liberté — Court-métrage d'animation sur l'indépendance du Maroc (1944–1956)*

**Description** : « Le 18 novembre, jour de la Fête de l'Indépendance, Younes découvre le carnet de son arrière-grand-mère Amina, témoin de la lutte pour l'indépendance du Maroc. Ce court-métrage d'animation éducatif (5 min) retrace des repères historiques : 11 janvier 1944 — Manifeste de l'indépendance ; 20 août 1953 — déposition et exil du sultan Mohammed Ben Youssef ; 16 novembre 1955 — son retour ; 18 novembre 1955 — Discours du Trône ; 2 mars 1956 — reconnaissance française de l'indépendance ; 7 avril 1956 — fin du protectorat espagnol dans le Nord. Le processus d'unification territoriale s'est poursuivi après 1956. Les personnages et les scènes sont une reconstitution pédagogique : ce ne sont pas des archives.
Écrit, réalisé et produit par Amin Benhida, enseignant à l'École communautaire de Tiddas. Sous-titres en français disponibles.
Crédits et sources : [**SOUS RÉSERVE DE LA DÉCISION SH08** — photographie : Mohammed V et son fils Moulay Hassan, Paris, 5 août 1931 — Agence Rol — Source : gallica.bnf.fr / Bibliothèque nationale de France] · Portraits historiques : photographie Anefo, 1953 — Nationaal Archief, La Haye — CC0 · Musique : « Possible Dreams » (Eugenio Mininni), Mixkit — Mixkit Stock Music Free License · Bruitages : Mixkit — Sound Effects Free License · [**À CONFIRMER SELON PREUVES** — voix de synthèse (ElevenLabs) ; illustrations réalisées avec l'aide de l'IA (Magnific)]. »

**Mots-clés** : Maroc, indépendance du Maroc, histoire du Maroc, Manifeste de l'indépendance, 11 janvier 1944, Mohammed V, Fête de l'indépendance, 18 novembre, court-métrage d'animation, film éducatif, histoire pour enfants, école primaire, protectorat. Hashtags : #Maroc #Histoire #FilmÉducatif.

**Sous-titres (YouTube Studio)** : Sous-titres → langue de la vidéo : français → Ajouter → *Importer un fichier* → « Avec minutage » (.srt) → fichier `…_FR.srt` (UTF-8) → vérifier l'aperçu → publier. Ne pas se fier aux sous-titres automatiques. *(Libellés de l'interface susceptibles de varier.)*

**Vignette (concept, non générée)** : image 3700 (Amina écrivant à la lampe, tons chauds, lisible en petit) ; titre « LE CARNET DE LA LIBERTÉ » en Cinzel or ; sous-titre discret « 1944 → 1956 · Maroc » ; 1280×720, marges de sécurité ; **aucun portrait de personne réelle** ; aucun slogan sensationnel.

**Public — recommandation : « conçu pour les enfants » = OUI.** Règle YouTube (aide officielle lue le 20/11) : le contenu est « made for kids » si les enfants sont le public principal ou si la vidéo vise les enfants (personnages animés, langage, sujets) ; « les contenus grand public » restent « pas conçus pour les enfants ». Le film cible explicitement des élèves de 9–12 ans (< 13 ans), avec des personnages d'enfants animés et un langage adapté : même si le public se veut « mixte », YouTube le range dans le contenu pour enfants. La désignation relève de la **responsabilité légale du créateur** (YouTube ne donne pas de conseil juridique) ; certaines fonctions de la chaîne sont limitées pour ces vidéos (à vérifier dans Studio). Pas de restriction d'âge. **Divulgation IA** : YouTube exempte l'animation manifestement non réaliste (exemple officiel : animation entièrement animée) ; les images et voix du film étant stylisées, la divulgation n'est probablement pas exigée, mais la transparence est recommandée dans la description ; l'option de cocher « oui » reste une décision du propriétaire.

## 5. Matrice de décision
| Domaine | Résultat | Action requise |
|---|---|---|
| Qualité artistique | **UNVERIFIED** (pour CINÉMA v4) | Visionnage/écoute de CINÉMA v4 par le responsable, ou confirmation écrite que la validation SCOLAIRE v4 vaut pour la piste (identique) et l'image (identique hors sous-titres) ; décider du carton-titre d'ouverture (facultatif) |
| Master technique | **PASS** | — |
| Son | **UNVERIFIED** (mesures conformes) | couvert par la déclaration d'écoute SCOLAIRE v4 si confirmée |
| Sous-titres | **PASS** | facultatif : reformater la réplique 15 (≤ 42 car.) |
| Droits | **BLOCKED** | SH08 (§2.1) ; preuves ElevenLabs et Magnific à archiver (§2.2) |
| Paquet YouTube | **READY** (brouillons) | finaliser les lignes de crédit entre crochets selon la décision de droits |

## 6. Brouillon d'e-mail à la BnF — **non envoyé**
À : utilisation.commerciale@bnf.fr · Cc : reproduction@bnf.fr
Objet : Demande de précision sur la réutilisation de la photographie Rol 156948 (Gallica, ark:/12148/btv1b53248904z)
« Madame, Monsieur, je réalise un court-métrage d'animation éducatif gratuit (5 min) sur l'histoire de l'indépendance du Maroc, destiné à des élèves du primaire. Il incorpore la photographie « 5-8-31, le sultan du Maroc et son fils Moulay Hassan » (Agence Rol, Rol 156948), indiquée « domaine public » sur Gallica, avec la mention « Source gallica.bnf.fr / Bibliothèque nationale de France ». Pouvez-vous me confirmer par écrit : (1) si la projection en classe, puis (2) la mise en ligne gratuite et non monétisée sur YouTube relèvent d'une réutilisation non commerciale libre avec cette mention, ou si une licence est requise (et son tarif) ; (3) la formulation de crédit attendue. Je vous remercie. [Nom, établissement, coordonnées] »

## 7. Actions restantes, par priorité
1. **Lever le blocage SH08** : envoyer la demande à la BnF (§6) *ou* choisir l'alternative 2/3 (nouveau rendu : autorisation requise). — *bloquant*
2. **Archiver les preuves** de forfait/licence : ElevenLabs Starter actif le 17/11 + conditions des voix utilisées ; Magnific « Plus » + conditions d'usage commercial des images. — *bloquant tant que non faites (preuve documentaire)*
3. **Confirmer l'artistique/son de CINÉMA v4** (visionnage/écoute ou confirmation d'héritage depuis SCOLAIRE v4).
4. **Décider** : « conçu pour les enfants » (recommandé : oui) et divulgation IA.
5. Facultatif : carton-titre/fondu d'ouverture, reformatage de la réplique 15.
6. Quand 1–4 sont réglés : autoriser expressément la copie FINAL (copie octet pour octet de v4 si rien ne change) et sa mise en ligne.

Fichiers non modifiés : CINÉMA v4, SCOLAIRE v4, SRT, quiz, registre d'approbation (aucune inscription faite).
