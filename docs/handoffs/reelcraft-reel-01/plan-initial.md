# ReelCraftMaroc — Reel 30 s pour garages et vendeurs d'occasion à Salé
Plan de préparation (phase 1) — aucune génération lancée. En attente de votre validation.

## 0. Éléments manquants (à fournir avant production)
| Élément | État | Action |
|---|---|---|
| Logo ReelCraftMaroc | Manquant | Fournir un fichier PNG/SVG, sinon wordmark texte provisoire |
| Numéro WhatsApp de contact | Non disponible (eSIM en attente du ticket Meta) | Placeholder `[NUMÉRO WHATSAPP]` éditable |
| Site / Instagram / QR | Aucun | Placeholders, rien d'inventé |
| Palette et police de marque | Non définies | Proposition en section 3, à valider |
| Voix-off : darija ou français | À choisir | Recommandation : darija, sous-titres français |
| Capture réelle du bot « Auto Salé Occasion » | Existe (testé le 2 nov.) | Enregistrer l'écran, à utiliser en scène 3 |
| Statut légal (fonctionnaire) | Non vérifié | À régler avant de diffuser une offre commerciale |

## 1. Trois concepts
| | A — « Le message perdu » | B — « Le vendeur qui ne dort jamais » | C — « Le showroom dans la poche » |
|---|---|---|---|
| Idée | Un client écrit, personne ne répond ; il part chez le concurrent | Vue nocturne : le garage fermé, le bot répond à 23 h | Le client parcourt voitures, prix, photos dans WhatsApp |
| Émotion | Peur de perdre | Soulagement | Désir |
| Force | Problème très concret | Argument 24/7 fort | Visuel démonstratif |
| Risque | Négatif | Moins de démonstration | Peu de contexte métier |

## 2. Concept recommandé : A + extrait de B
Raison : le propriétaire de garage réagit d'abord à la perte (client non servi), puis à la solution. Le storyboard demandé suit déjà cette logique. On ajoute un plan nocturne en scène 4 pour l'argument « même quand vous ne répondez pas ».

## 3. Direction artistique
- Palette : noir profond, anthracite, accent vert WhatsApp (#25D366) pour l'interface, blanc cassé pour le texte (à valider).
- Typo : sans-serif grasse (Montserrat ExtraBold titres, Inter sous-titres).
- Étalonnage : contraste élevé, ombres froides, reflets carrosserie chauds.
- Règle : mêmes voitures, même lumière, même interface dans toutes les scènes (image de référence fixée en premier).

## 4. Storyboard 30 s (1080×1920, 9:16)
| Temps | Scène | Visuel | Texte écran |
|---|---|---|---|
| 0–5 s | 1 Problème | Parking d'occasion, vendeur occupé avec un client, téléphone sur le capot qui vibre ; message « Salam, wach had tomobil mazala disponible? » resté « lu » sans réponse | « Combien de clients perdez-vous pendant que vous êtes occupé ? » |
| 5–11 s | 2 Solution | Zoom dans l'écran, interface type WhatsApp, réponse instantanée en darija | « Votre assistant WhatsApp IA. » |
| 11–19 s | 3 Automatisation | Gros plans UI : fiche voiture + photo, prix/kilométrage, demande d'essai, ligne de lead rangée dans un tableau | « Réponses instantanées. Leads qualifiés. » |
| 19–25 s | 4 Transformation | Écran partagé : clients qui écrivent / réponses + leads ; plan nuit du garage fermé, téléphone qui répond | « Votre garage répond. Même quand vous ne pouvez pas. » |
| 25–30 s | 5 Marque | Fond sombre, logo, tagline, CTA | « REELCRAFTMAROC — Votre WhatsApp. Votre assistant commercial IA. » / « Automatisez votre garage dès aujourd'hui. » / « Contactez-nous sur WhatsApp : [NUMÉRO] » |

Les fonctionnalités sont présentées comme capacités du service, sous réserve de configuration. Aucune promesse de ventes garanties.

## 5. Prompts image (Midjourney, 9:16, `--ar 9:16`)
1. Référence de marque : « Modern used car lot in Salé, Morocco, golden hour, three clean cars (compact hatchback, sedan, SUV), Moroccan salesperson in shirt speaking with customers, premium commercial photography, shallow depth of field, cinematic grade, no text, no logos »
2. Gros plan téléphone : « Smartphone lying on a car hood, screen lit with an unanswered WhatsApp-style chat, blurred dealership background, macro, premium advertising »
3. Écran de conversation propre (à refaire en HTML/Canva pour un texte lisible, la génération IA déforme le texte) : thème vert/noir, bulles client/assistant.
4. Plan nocturne : « Closed car dealership at night, neon-lit cars, a single phone glowing on the counter, blue-teal cinematic lighting »
5. Fond de marque : dégradé noir/anthracite, léger grain, espace central pour logo.
Les textes d'interface et le logo sont montés au montage, jamais générés.

## 6. Prompts vidéo (Higgsfield / Veo / Runway, 5–6 s par plan)
| Plan | Prompt |
|---|---|
| S1 | « Slow push-in on salesperson busy with customers, phone vibrating on the hood in foreground sharp focus, golden hour, 9:16, no on-screen text » |
| S2 | « Smooth dolly into smartphone screen, light flare, clean transition » |
| S3 | Éviter la vidéo IA : animer les écrans réels/HTML (capture du bot démo), meilleure lisibilité |
| S4 | « Night dealership exterior, slow orbit, phone glow, rain reflections on cars » |
| S5 | Animation de logo en montage |
Ne jamais montrer un vrai plaque d'immatriculation ni une marque identifiable de façon trompeuse.

## 7. Voix-off (darija, ≈ 28 s) et sous-titres FR
| Temps | Darija (latin) | Sous-titre FR |
|---|---|---|
| 0–5 | « Klient kaysift lik message… w ntouma mchghoulin. » | « Un client vous écrit… vous êtes occupé. » |
| 5–11 | « Daba, l'assistant dyalk f WhatsApp kayjaweb f tanya. » | « Votre assistant WhatsApp répond en une seconde. » |
| 11–19 | « Taman, kilométrage, tsawer, w talab dyal essai : kolchi automatique. » | « Prix, kilométrage, photos, demandes d'essai. » |
| 19–25 | « Hta mni katkoun msakker, l'garage dyalk kayb9a kaygawb. » | « Même fermé, votre garage répond. » |
| 25–30 | « ReelCraftMaroc. Automatisez votre garage. » | CTA + numéro placeholder |
À faire relire par un locuteur natif avant génération vocale.

## 8. Musique et sons
- Électro corporate, 110–120 BPM, montée à 0:19, coupure nette à 0:25 pour le logo.
- SFX : notification WhatsApp-like (son générique, pas l'original), whoosh de transition, clic UI, swell final.
- Sources : Artlist (recherche musique/SFX), alternative Magnific audio.

## 9. Montage et transitions
- Cut sur mouvement S1→S2 (zoom dans l'écran), match-cut écran→interface.
- Sous-titres : 2 lignes max, zone sûre 150 px haut/bas (UI Reels).
- Étalonnage unique appliqué à tous les plans, grain léger.
- Export H.264, 1080×1920, 30 fps, −14 LUFS.

## 10. Chaîne de production et outils
| Étape | Outil visé | Vérification |
|---|---|---|
| Images | Midjourney | Connecteur présent dans la liste, à tester |
| Vidéo | Higgsfield / Veo / Runway | Présents, crédits à vérifier |
| Amélioration | Magnific | Présent |
| Musique/SFX | Artlist | Présent |
| Voix | ElevenLabs / Artlist | Darija à tester |
| Montage | **DaVinci Resolve : aucun connecteur** | Remplacer par Reel Studio / Magnific vidéo / Canva, ou montage manuel de votre côté |

Estimation : coûts en crédits à obtenir via get_generation_cost avant tout lancement.

## 11. Checklist de production
1. □ Valider concept, palette, langue de voix
2. □ Fournir logo et placeholder CTA
3. □ Enregistrer l'écran du bot démo « Auto Salé Occasion »
4. □ Créer le dossier projet `ReelCraft-Reel-01/` (originaux préservés, rien écrasé)
5. □ Générer images de référence (jalon de validation 1)
6. □ Générer plans vidéo S1, S2, S4 (jalon 2 : choix des prises)
7. □ Voix-off + musique (jalon 3 : écoute)
8. □ Montage, sous-titres, étalonnage
9. □ Export et relecture finale
10. □ Vérifier statut légal avant diffusion

## Approbation
Répondez « approuvé » (avec vos choix : concept, voix, langue) pour lancer. Validations demandées uniquement aux jalons 5, 6 et 7.
