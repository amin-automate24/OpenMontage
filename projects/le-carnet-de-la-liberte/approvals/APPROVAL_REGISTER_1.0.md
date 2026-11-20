# APPROVAL REGISTER 1.0 — LE CARNET DE LA LIBERTÉ

Règles : une approbation **écrite dans le chat du projet** est requise par étape ; l'approbation d'une étape n'autorise jamais la suivante ; les opérations locales, gratuites et réversibles n'ont pas besoin d'approbation. Une notification automatique ou un message d'outil n'est **jamais** une approbation. Le plafond de 2 000 crédits est une limite de planification, **pas une autorisation de dépense**.

Dernière mise à jour : 2026-11-16.

## 1. Autorisations reçues (source : « MASTER PRODUCTION PROMPT 1.0 » de l'utilisateur)

| Réf. | Portée autorisée | Statut |
|---|---|---|
| AUTH-00 | Préproduction locale : structure du projet, sauvegarde et validation du scénario 1.1, découpage, documentation technique, placeholders locaux, voix temporaire locale, animatic local, budget estimatif, rapport de préparation | **Accordée et exécutée** (voir §3) |
| AUTH-01 | Utilisation d'outils locaux gratuits (FFmpeg, PIL, espeak-ng) | **Accordée et exécutée** |
| — | Toute génération payante d'image ou de vidéo, consommation de crédits, abonnement, modification de THE LAST OF MEN, publication externe, production finale payante | **NON autorisé** |

## 2. Portes d'approbation du projet

| Étape | Contenu | Coût estimé (voir budget) | Statut | Date | Approuvé par |
|---|---|---|---|---|---|
| **GATE 1 — Références historiques et visuelles** | Validation humaine des points H1–H11, des références historiques fournies, du style ; décisions D1–D9 | 0 crédit (+ 65 si style board REF-00 généré) | ⏳ **Non demandée** — en attente de vos décisions | — | — |
| **GATE 2 — Images de personnages et de décors** | REF-00…06, E1–E5, puis images de plans | Scénario A 1 950 / B 3 510 / C 3 510 | ⏳ **Non demandée / non accordée** | — | — |
| **GATE 3 — Image→vidéo** | SH11, SH26, SH38 (+ SH07, SH27 en option) | B 1 300 / C 2 275 | ⏳ **Non demandée / non accordée** | — | — |
| **GATE 4 — Audio final et postproduction** | Voix, musique, SFX, mixage, étalonnage, export final | B 705 (si via Magnific) | ⏳ **Non demandée / non accordée** | — | — |

Format de réponse attendu (exemple) : « **J'approuve GATE 2 scénario B, plafond 3 600 crédits, échantillon d'abord.** »

## 3. Journal des opérations effectuées (gratuites)

| Date | Opération | Coût |
|---|---|---|
| 2026-11-16 | Recherches **en lecture seule** : Dropbox, Drive, Notion, Gmail (scénario introuvable avant réception du prompt) | 0 |
| 2026-11-16 | Lecture du solde Magnific (10 158 crédits), Artlist, Higgsfield ; ElevenLabs refusé (permissions) | 0 |
| 2026-11-16 | Simulations de coût Magnific (`simulate_cost`, lecture seule) : images, vidéos, voix, musique | 0 (aucun crédit débité) |
| 2026-11-16 | Installation locale : `piper-tts`, `websockets` (pip) et `espeak-ng` (apt) — environnement éphémère | 0 |
| 2026-11-16 | Création du projet `projects/le-carnet-de-la-liberte/` (`init_project`, pipeline `animation`) | 0 |
| 2026-11-16 | Sauvegarde du scénario 1.1 (SHA-256 `8c3c6de7401d70adfc75c2574afadafed96bfd9d5abf2a8eaf020ea456d8af66`) | 0 |
| 2026-11-16 | Liste de plans, prompts, rapports, animatic local | 0 |

**Crédits externes consommés par ce projet : 0.** Appels payants : 0. **THE LAST OF MEN : aucun fichier modifié.**

## 4. Décisions en attente (à approuver dans le chat)

| ID | Décision | Recommandation |
|---|---|---|
| **D1** | Scène 6 : passer de 20 s à 26 s (film 276 s) ? | **Oui** |
| **D2** | Plafond crédits et réserve pour THE LAST OF MEN | Scénario B (≈ 5 500 tout compris) **ou** A (1 950, sans plans animés) ; fixer une réserve écrite pour THE LAST OF MEN |
| **D3** | Mention « ILLUSTRATION PÉDAGOGIQUE — non archive » sur les inserts historiques | Oui |
| **D4** | Mention « le processus territorial s'est poursuivi après 1956 » | Oui (courte) |
| **D5** | Mention « Reconstitution » pendant l'annonce radio | Oui |
| **D6** | Design de la maîtresse (foulard ou non) | Votre choix créatif |
| **D7** | Langue du carnet d'Amina (français / arabe + sous-titres) | Français (public francophone) |
| **D8** | Phrases d'Amina écrites : murmurées ou silencieuses | Silencieuses (fidèle au scénario) |
| **D9** | Moteur de composition (FFmpeg déjà utilisable ; Remotion et HyperFrames non installés) | À présenter et trancher : voir résumé de préparation |
| **D10** | Voix finales : comédiens humains / TTS | Comédiens humains ou TTS testé sur 2 répliques |
| **D11** | Corriger « arrière-arrière-grand-mère » → « arrière-grand-mère » | Oui |
| **D12** | Source de la musique | Piste libre de droits fournie, sinon Lyria 3 (≈ 240 cr) |
