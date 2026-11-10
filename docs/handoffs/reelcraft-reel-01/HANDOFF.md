# Transfert — Reel ReelCraftMaroc (30 s, garages d'occasion à Salé)

Document de reprise pour Claude Code sur ce dépôt. Auteur du projet : Amin (instituteur, Salé). Langue des échanges : français ou arabe ; documents longs en français ; réponses courtes, listes et tableaux ; signaler les pièges plutôt que féliciter.

## 1. Objectif

Reel vertical premium 9:16 (1080×1920), 30 s, pour la marque **ReelCraftMaroc**, destiné aux vendeurs de voitures d'occasion et garages de Salé. Concept validé : « Le message perdu » + « Le vendeur qui ne dort jamais ». Voix-off en darija, sous-titres français.

Règles du brief initial à respecter :
- Ne jamais écraser les originaux ; travailler dans un dossier projet séparé.
- Aucun numéro, site, réseau social ou QR inventé : placeholders éditables (`[NUMÉRO]`, `[À configurer]`).
- Présenter les fonctions comme des capacités du service proposé, pas comme déjà déployées. Pas de promesse de ventes garanties.
- Ne pas affirmer qu'une intégration existe sans vérification.
- Valider avec l'utilisateur seulement aux jalons créatifs majeurs.

## 2. Direction artistique

| Élément | Valeur |
|---|---|
| Fond | navy `#031430` (celui du logo) |
| Accent | orange `#FF5A0A` |
| Texte | blanc ; bulles : gris `#1f2a3a` (client), vert `#0b5a4a` (assistant) |
| Police visée | Montserrat ExtraBold (titres) + Inter (texte). Montserrat n'est pas installée dans l'environnement de rendu actuel : Inter est utilisée à la place |
| Logo | `assets/logo-original.png` (fichier original fourni par l'utilisateur, 1080×1080, fond navy) |
| Zone de sécurité | 170 px haut, 230 px bas |

## 3. Storyboard et minutage

| Scène | Temps | Contenu | Voix darija (écriture arabe) | Sous-titre FR |
|---|---|---|---|---|
| 1 | 0–5 s | Client écrit, aucune réponse | كاين كليان كايصيفط ليك ميساج... وانتا مشغول. | Un client vous écrit… vous êtes occupé. |
| 2 | 5–10 s | Assistant WhatsApp IA répond | دابا، المساعد ديالك فواتساب كايجاوب فثانية. | Votre assistant WhatsApp répond en une seconde. |
| 3 | 10–20 s | Fiche voiture, essai samedi, essai confirmé | الثمن، الكيلوميتراج، الصور، وطلب التجربة... كلشي أوتوماتيك. | Prix, kilométrage, photos, demandes d'essai : tout est automatique. |
| 4 | 20–25 s | Garage fermé, l'assistant répond | حتى فاش الكراج كايكون مسدود، كايبقى كايجاوب. | Même fermé, votre garage répond. |
| 5 | 25–30 s | Logo, tagline, CTA, contact | ريل كرافت. أتمتة الكراج ديالك، من اليوم. | CTA + `[NUMÉRO]` |

Clips de voix placés 0,3 s après le début de chaque scène : 0,3 / 5,3 / 10,3 / 20,3 / 25,3 s. Chaque clip dure environ 3 s. Musique sur 30 s, environ −14 dB sous la voix.

À faire relire par un locuteur natif avant diffusion (voix générée par IA, texte darija non validé).

## 4. État d'avancement

| Livrable | État |
|---|---|
| Plan de préparation | Fait (`plan-initial.md`, palette verte WhatsApp dépassée : voir section 2) |
| Images de référence, vidéos IA S1/S2/S4, voix, musique | Générés sur Magnific (identifiants section 6) |
| **v1** : montage HyperFrames (photos + vidéo IA) + voix + musique, exporté via Reel Studio | **Défectueux** : textes qui se superposent en scène 3, bouton CTA coupé en scène 5 |
| v2 : correction demandée à HyperFrames | **Échec** : scène 2 quasi vide à ~6 s, scène 3 inchangée, superpositions aux transitions |
| **v3** : scènes refaites en HTML, rendues localement (`src/`) | **Propre**, vérifié sur les images aux transitions. **Muet**, sans photos de voitures (🚗 émoji) |
| Version finale avec voix + musique + images | **À faire** (c'est le travail transféré) |

Défauts de v3 à connaître : pas de vraies photos ni de vidéo IA ; scène 1 en texte + émoji ; police Inter au lieu de Montserrat.

## 5. Ce qu'il reste à faire (travail transféré)

1. Choisir le pipeline OpenMontage adapté (voir `AGENT_GUIDE.md` : Rule Zero, pipeline, preflight) et créer le projet sous `projects/reelcraft-reel-01/` (dossier ignoré par git).
2. Reprendre `src/reel_v3.html` comme base de composition (ou la recomposer avec le moteur du pipeline) : conserver la mise en page en flux, sans chevauchement, et les transitions successives (fondu sortant terminé avant le fondu entrant).
3. Réintroduire les visuels : photos de voitures (images IA du projet Magnific, ou nouvelles) dans leur propre zone, jamais sous du texte ; éventuellement les vidéos IA des scènes 1, 2 et 4.
4. Régénérer ou récupérer la voix darija par scène (5 clips) et la musique ; caler comme en section 3 ; mixer voix 0 dB, musique −12 à −15 dB ; viser −14 LUFS.
5. Rendre en H.264, 1080×1920, 30 fps.
6. Contrôle qualité : extraire des images à 2, 4.9, 5.1, 9.9, 10.1, 14, 17, 19.9, 20.1, 24.9, 25.1, 28 s ; vérifier qu'aucun texte n'est chevauché, coupé, ni qu'aucune scène n'est vide.

## 6. Ressources externes (références sans lien signé)

| Ressource | Identifiant |
|---|---|
| Projet Magnific | `ReelCraft-Reel-01`, réf. `9744b211-9912-4928-a63d-7a376c876351` |
| Images retenues | `tCNchifmZJ` (parking), `p8wZdiXehw` (téléphone), `8a4YtctIrU` (nuit) ; autres : `79m5OhKJAL`, `0esNVPFTfW`, `xSpfLE6jfW` |
| Vidéos IA (Kling 2.5, 5 s) | `P3fr6jl42C` (S1), `VXgidpOMMU` (S2), `ksVhLOs16B` (S4) |
| Voix par scène (voix « Tariq Nasser », eleven_v4) | `VXgiFAhMMU` (0 s), `YMxPf3hWeC` (5 s), `u5GdJmyQLD` (10 s), `JNhKTlbOq4` (20 s), `aFRMSIhfSh` (25 s) ; voix complète `0esNpl8TfW` |
| Musique (google-lyria-3) | `Sy8HOqVUb8` |
| Film Reel Studio | slug `reelcraftmaroc-reel-garages-sale`, shot `reel-complet-30s` |
| Projet HyperFrames | `a71e79b3-9641-422c-9568-06e6310b8606` (quota gratuit épuisé ce mois-ci) |

Les liens de téléchargement de ces services sont signés et expirent : ne pas les enregistrer ici, les redemander au service.

## 7. Pièges connus

- **HyperFrames** : refuse tout nouveau rendu tant que le quota gratuit du mois est épuisé ; ignore l'audio externe ; son agent a ignoré des consignes de mise en page précises. Préférer une composition maîtrisée localement.
- **Reel Studio** : plan gratuit = filigrane « Reel/Studio » en bas à droite sur les exports ; peu de crédits.
- **Réseau de l'environnement cloud** : les hôtes des CDN Magnific et Reel Studio ne sont pas accessibles depuis le shell (erreur 403 « CONNECT tunnel failed »). Ne pas insister avec d'autres commandes. Dans un environnement local avec accès normal, télécharger les clips depuis les services.
- **Polices et émojis** : vérifier que Montserrat est installée ; les émojis passent par Noto Color Emoji.
- **Statut légal** : l'utilisateur est fonctionnaire ; vérifier la compatibilité avant toute offre commerciale publique.
- **Numéro WhatsApp** : en attente (eSIM / validation Meta) ; garder `[NUMÉRO]`.

## 8. Rendre v3 localement

```bash
pip install playwright && playwright install chromium
# depuis la racine du dépôt
python3 docs/handoffs/reelcraft-reel-01/src/render_video.py   # → assets/reelcraft_reel_v3_silencieux.mp4 (30 s, 900 images, ffmpeg requis)
python3 docs/handoffs/reelcraft-reel-01/src/render_frames.py <dossier> 4.9 5.1 14   # images de contrôle
```

`reel_v3.html` expose `setTime(t)` : chaque image est rendue de façon déterministe à l'instant `t`.

## 9. Version finale (session du 2026-11-10)

| Élément | Valeur |
|---|---|
| Vidéo | `assets/reelcraft_reel_final.mp4` (H.264 1080×1920, 30 fps, 30 s, AAC stéréo) |
| Composition | `final/reel_final.html` (v3 + photos Magnific en cadres dédiés, zoom lent) |
| Rendu | `final/render.js` (Node Playwright → ffmpeg) ; contrôle : `final/qc.js` |
| Projet OpenMontage | `projects/reelcraft-reel-01/` (pipeline `animation`, runtime `ffmpeg`, non versionné) |
| Voix | 5 clips Magnific normalisés à −20 LUFS, débuts mesurés 0,33 / 5,33 / 10,33 / 20,33 / 25,33 s |
| Musique | `Sy8HOqVUb8` étirée à 30 s (atempo 0,915), 12,7 à 13,5 dB sous la voix, remontée progressive après 25 s |
| Master | −14,4 LUFS intégré, crête −1,3 dBFS |

Changements par rapport à v3 :
- Fondus : sortie sur [b−0,15 ; b], entrée sur [a+0,02 ; a+0,10]. En v3, l'écran était entièrement vide à 4,9 / 9,9 / 19,9 / 24,9 s.
- Logo S5 visible dès 25,0 s (en v3, écran vide à 25,1 s).
- Émojis 😬 (S1) et 🚗 (S3) remplacés par les photos `tCNchifmZJ` et `79m5OhKJAL` ; photos `p8wZdiXehw` (S2) et `8a4YtctIrU` (S4) ajoutées.

`reel_final.html` attend les images dans `../assets/images/` (`parking_tCNchifmZJ.png`, `phone_p8wZdiXehw.png`, `parking2_79m5OhKJAL.png`, `night_8a4YtctIrU.png`, `logo.png`) : les retélécharger via Magnific, sans écrire les liens signés dans le dépôt.

## 10. Mise à jour : clips Kling intégrés (session du 2026-11-10)

| Élément | Valeur |
|---|---|
| Vidéo | `assets/reelcraft_reel_final.mp4` (clips Kling en S1, S2, S4 ; S3 reste une photo) |
| Version précédente | `assets/reelcraft_reel_final_photos_seules.mp4` |
| Audio | Inchangé (−14,4 LUFS, crête −1,3 dBFS, voix à 0,3 / 5,3 / 10,3 / 20,3 / 25,3 s) |

Pour rendre `final/reel_final.html`, il faut des séquences d'images extraites des clips Kling : `ffmpeg -i <clip>.mp4 -vf "fps=30,scale=960:-2" -q:v 3 assets/video/frames/<s1|s2|s4>/%04d.jpg`, avec les clips `P3fr6jl42C` (S1), `VXgidpOMMU` (S2), `ksVhLOs16B` (S4) retéléchargés depuis Magnific. `render.js` et `qc.js` appellent `setTimeAsync(t)`, qui attend le décodage de l'image.

Vérifié : les voix et la musique de Reel Studio sont identiques octet pour octet à celles de Magnific. La « musique 30 s » de Reel Studio fait en réalité 27,45 s.
