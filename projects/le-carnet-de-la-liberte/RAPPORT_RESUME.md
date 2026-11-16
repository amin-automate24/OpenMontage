# LE CARNET DE LA LIBERTÉ — Rapport résumé de préproduction

**Date :** 16/11/2026 · **Livraison cible :** vendredi 20/11/2026 · **Durée :** 4 min 30 s (270 s), maximum absolu 5 min · **Format :** 1920×1080, H.264/AAC

## Statut en une ligne

Préproduction terminée et animatic local livré. **0 crédit dépensé, 0 appel payant.** THE LAST OF MEN n'a pas été touché. La production payante est bloquée en attente de vos décisions, surtout le budget.

## Ce qui a été produit

| Livrable | Détail |
|---|---|
| Scénario 1.1 | Texte conservé à l'identique, SHA-256 enregistré. Six scènes validées : 30+35+55+55+75+20 = 270 s. |
| Liste technique de plans | 38 plans (30 principaux, 8 secondaires), timecodés, 270,0 s. 5 plans en image→vidéo (SH07, 11, 26, 27, 38) ; le reste en images fixes avec caméra ou graphiques locaux. |
| Animatic 1.0 | MP4 1080p25, 270,0 s. Placeholders, cartons de dates, voix synthétiques espeak-ng **internes, non publiables**. |
| Références personnages et décors | Plan rédigé, rien généré. |
| Pack de prompts | 45 images et 5 clips image→vidéo, **rédigés, non exécutés**. |
| Budget et risques | Prix exacts simulés en lecture seule. |
| Plan sonore et DaVinci Resolve | Ambiances, repères musicaux, instructions de montage et d'export. |
| Registre d'approbations | 4 portes, **aucune accordée**. |

Tout est dans `projects/le-carnet-de-la-liberte/`, branche `claude/carnet-liberte-preproduction-b3y71m`. L'animatic se régénère en local avec `scripts/carnet_animatic.py`.

## Budget (Magnific, solde 10 158 crédits partagés avec THE LAST OF MEN)

| Scénario | Total | Contenu |
|---|---|---|
| **A — plafond 2 000** | 1 950 | 30 images, **aucun plan animé**, images très réutilisées |
| **B — recommandé** | **5 515** | 45 images + 20 % de reprises (3 510), 3 clips Kling 2.5 + 1 reprise (1 300), voix et musique (705) |
| **C — complet** | 6 490 | Comme B avec 5 clips animés |

Prix unitaires : image Nano Banana 2.1 à 65 crédits, clip Kling 2.5 de 5 s à 325 crédits, musique Lyria 3 à environ 80 crédits par clip. La musique ElevenLabs de 270 s (5 400) est écartée. **Le plafond de 2 000 crédits n'est tenable que pour le scénario A.**

## Points d'attention

1. **Scène 6 trop dense :** 20 s pour environ 15 s de dialogue naturel, plus écriture, plan final et titre. Recommandation : 26 s, soit un film de 276 s (< 300 s).
2. **Parenté :** Amina, née vers 1933, est « arrière-grand-mère », pas « arrière-arrière ». Texte non modifié.
3. **Vérification historique :** aucune source externe consultée. Dates et détails (18/11/1955, 02/03 et 07/04/1956, costumes, drapeau) à faire confirmer par un humain. Aucun visage, aucune voix, aucun discours de Mohammed V. Drapeaux, dates et calligraphie sont composités, jamais générés par l'IA.
4. **`carnet.py` introuvable** sur la machine ; remplacé par `scripts/carnet_animatic.py`.
5. **Intégrations :** Artlist en essai sans crédits, Higgsfield à 0, connecteur ElevenLabs à reconnecter.
6. **Moteurs de composition :** seul FFmpeg est utilisable. Remotion et HyperFrames ne sont pas installés.
7. **Voix et musique :** aucune voix finale, aucune piste libre de droits.

## Décisions à prendre

| ID | Décision | Recommandation |
|---|---|---|
| **D2** | Plafond de crédits et réserve pour THE LAST OF MEN | Scénario B, ou A sans plans animés |
| **D1** | Scène 6 à 26 s | Oui |
| **D11** | Corriger en « arrière-grand-mère » | Oui |
| **D10** | Voix finales | Comédiens humains, ou synthèse testée sur 2 répliques |
| **D12** | Source de la musique | Piste libre de droits fournie, sinon Lyria 3 |
| **D9** | Moteur de composition | DaVinci Resolve, cartons en FFmpeg ou Remotion |
| D3 à D5 | Mentions « illustration pédagogique », « reconstitution », note territoriale | Oui |
| D6 à D8 | Design de la maîtresse, langue du carnet, phrases d'Amina écrites mais non dites | Votre choix créatif |

## Calendrier

| Jour | Action |
|---|---|
| Lun 16 | Vos décisions D1, D2, D10 ; je mets à jour la liste de plans et l'animatic |
| Mar 17 | Porte 2 : échantillon (style, Younes, Amina = 195 crédits), puis fiches, décors, images de plans |
| Mer 18 | Porte 3 : clips animés ; voix ; cartons et drapeaux en local |
| Jeu 19 | Montage, étalonnage, musique, mixage ; contrôle historique plan par plan |
| Ven 20 | Export final et vérification (< 5 min, 1080p, H.264/AAC) |

Toute décision qui glisse au 17 met la génération et l'enregistrement des voix en conflit.

## Pour continuer

Répondez par exemple : « J'approuve la porte 2, scénario B, plafond X, échantillon d'abord. » Aucune étape suivante ne sera lancée sans approbation écrite.

Détails complets : `docs/PRODUCTION_READINESS_SUMMARY_1.0.md`, `docs/CREDIT_BUDGET_AND_PRODUCTION_RISK_REPORT_1.0.md`, `docs/HISTORICAL_AND_TIMING_FLAGS_1.0.md`, `approvals/APPROVAL_REGISTER_1.0.md`.
