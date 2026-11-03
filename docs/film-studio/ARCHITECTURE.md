# Architecture — Film Studio sur OpenMontage

Film Studio ne remplace pas OpenMontage : c'est une **couche film narratif** posée sur le pipeline
`cinematic`. Les décisions et les artefacts canoniques passent par le pipeline (checkpoints, board Backlot,
`decision_log`). La bible du film (01 → 11) est le miroir lisible et éditable de ces artefacts.

```
 IDÉE ──► research ──► proposal ──► script ──► scene_plan ──► assets ──► edit ──► compose ──► publish
            │            │  ▲          │           │             │         │         │
            │       [PORTE 1]     [PORTE 2]   [PORTE 3]     [PORTE 4]       │         │
            ▼            ▼             ▼           ▼             ▼          ▼         ▼
       01_CONCEPT   03_VISUAL    02_SCREENPLAY 05_STORYBOARD 06_VIDEO_   09_EDITING 11_QC_REPORT
                    04_CHARACTER               (+ keyframes)  PROMPTS     PLAN      10_output/
                                                              07/08_SOUND 10_TIMELINE
                         production_log.md  ◄── chaque opération, erreur, tentative, décision
```

## 1. Correspondance phases du cahier des charges → OpenMontage

| Phase du brief | Stage `cinematic` | Artefact canonique | Document bible | Outils |
|---|---|---|---|---|
| 1. Analyse / concept | `research` → `proposal` | `research_brief`, `proposal_packet`, `decision_log` | `01_CONCEPT.md` | web search, Claude |
| 3. Direction artistique | `proposal` | `proposal_packet` (taste_profile, render_runtime) | `03_VISUAL_BIBLE.md` | `skills/meta/taste-direction.md` |
| 4. Personnages | `proposal` → `scene_plan` | `scene_plan` (références) | `04_CHARACTER_BIBLE.md` | image gen (Imagen / Midjourney MCP), seeds |
| 2. Scénario | `script` | `script` | `02_SCREENPLAY.md` | Claude |
| 5. Storyboard | `scene_plan` | `scene_plan` | `05_STORYBOARD.md` | keyframes générées, `frame_sampler` |
| 6. Génération des plans | `assets` | `asset_manifest` | `06_VIDEO_PROMPTS.md` | `video_selector` → provider ; ou MCP (Runway, Veo) |
| 7. Animation des stills | `assets` | `asset_manifest` | `06_VIDEO_PROMPTS.md` | image-to-video ; parallax Remotion/HyperFrames en secours |
| 8. Musique / sound design | `assets` | `asset_manifest` | `07_SOUND_DESIGN.md`, `08_MUSIC_PROMPTS.md` | Lyria / Runway music / Pixabay ; SFX ElevenLabs MCP |
| 9. Montage | `edit` | `edit_decisions` | `09_EDITING_PLAN.md`, `10_TIMELINE/` | `video_compose`, `audio_mixer` |
| 10. Étalonnage / finition | `edit` → `compose` | `edit_decisions` | `03_VISUAL_BIBLE.md` §étalonnage | `color_grade` (LUT vérifié), `audio_enhance` |
| 11. Contrôle qualité | `compose` | `render_report` | `11_QC_REPORT.md` | `film_studio.py qc`, `visual_qa`, `frame_sampler` |
| 12. Export | `compose` → `publish` | `render_report` | `10_output/` | `film_studio.py export` |

## 2. Une fonction par outil

| Fonction | Outil principal | Secours | Statut aujourd'hui |
|---|---|---|---|
| Raisonnement, écriture, planification, scripts | Claude Code | — | ✅ |
| Références visuelles, keyframes, personnages | Imagen (`google_imagen`) | Midjourney MCP, Runway image | ⚠️ clé Gemini factice → Midjourney MCP (avec accord) |
| Plans vidéo | `video_selector` → Gemini Omni / Seedance / Kling / Veo | Runway MCP, Veo MCP | ⚠️ aucune clé valide ; MCP avec peu ou pas de crédits |
| Animation de stills | image-to-video du même provider | parallax / Ken Burns Remotion (signalé comme dégradé) | ✅ (secours) |
| Musique originale | Lyria (`google_music`) | Runway music (MCP), Pixabay (licence libre) | ⚠️ |
| SFX / ambiances | ElevenLabs MCP (SFX v2) | Runway SFX | ✅ (crédits ElevenLabs à confirmer) |
| Voix / voix off | Gemini TTS / Google TTS | ElevenLabs MCP (v3/v4) | ⚠️ / ✅ |
| Montage et composition | `video_compose` (FFmpeg · Remotion · HyperFrames) | — | ✅ |
| Étalonnage | `color_grade` + LUT FFmpeg | Magnific (0 crédit) | ✅ |
| QC et export | `scripts/film_studio.py` + `visual_qa` | — | ✅ |
| Finition pro (optionnelle) | DaVinci Resolve sur la machine de l'utilisateur | — | 👤 |
| Livraison | Dropbox / Google Drive MCP | téléchargement manuel | ✅ (avec accord) |

**Règle sur les connecteurs MCP.** Ils sont hors du registre OpenMontage. On ne s'en sert qu'avec un accord explicite. On annonce l'outil, le modèle, le coût et la raison avant l'appel, on consigne le choix dans le `decision_log` (`category: provider_selection`), puis on télécharge le fichier sous `projects/<id>/assets/video/scene_XX/shot_XXX.mp4` et on l'inscrit dans l'`asset_manifest` avec sa provenance (outil, modèle, prompt, seed, coût).

## 3. Structure d'un projet

`python scripts/film_studio.py init <id> --title "<Titre>"` crée :

```
projects/<id>/
├── project.json · checkpoint_*.json · artifacts/   ← OpenMontage (board Backlot)
├── assets/ (= 06_assets/)                          ← médias, une seule source de vérité
│   ├── images/characters/<nom>/ · images/storyboard/
│   ├── video/scene_01/shot_001.mp4 …
│   ├── audio/{dialogue,sfx,ambience}/ · music/
├── renders/final.mp4                               ← sortie de compose
├── 01_concept/01_CONCEPT.md
├── 02_screenplay/02_SCREENPLAY.md
├── 03_visual_bible/03_VISUAL_BIBLE.md · 04_CHARACTER_BIBLE.md
├── 04_storyboard/05_STORYBOARD.md
├── 05_prompts/06_VIDEO_PROMPTS.md · 08_MUSIC_PROMPTS.md
├── 07_editing/07_SOUND_DESIGN.md · 09_EDITING_PLAN.md · 10_TIMELINE/
├── 08_subtitles/
├── 09_quality_control/11_QC_REPORT.md · 11_QC_REPORT_auto.{md,json}
├── 10_output/final_film.mp4 · final_film_master.mov · final_film_subtitles.srt
└── production_log.md
```

Le master est un fichier **ProRes 422 HQ en `.mov`**. Le brief demandait `final_film_master.mp4`, mais le ProRes n'est pas un codec valide dans un conteneur MP4 ; le `.mov` est le standard des étalonneurs et monteurs.

## 4. Modes d'autonomie

| Mode | Ce que fait l'agent | Ce qui exige ton accord |
|---|---|---|
| **1 — Planification** (par défaut) | research, proposal, script, scene_plan, bible complète, prompts, devis | rien n'est dépensé |
| **2 — Production** | génération des keyframes, plans, musique, SFX ; montage ; QC ; export | porte assets, chaque changement de provider ou de modèle |
| **3 — Autonomie contrôlée** | enchaîne tout, régénère les plans ratés dans un budget plafond | une autorisation globale **écrite** (`decision_log`, `category: approval_policy`) avec un plafond en $ ; toute dépense au-delà du plafond, toute publication publique, tout envoi vers Dropbox/Drive |

## 5. Gestion des erreurs plan par plan

1. Un plan échoue : on diagnostique (déformation, dérive du visage, mouvement incohérent, refus de modération, erreur API) et on le consigne dans `production_log.md` (`--kind error`).
2. On corrige le prompt : une seule action, mouvement plus simple, keyframe image-to-video. On retente, deux fois au maximum (`--kind retry`), sans toucher aux autres plans.
3. Après deux échecs, on **propose** une alternative (still + animation légère, cadrage plus large, plan de coupe, plan supprimé) **sans l'appliquer sans accord**. C'est un passage du video-led au still-led : règle « Motion-Required » de l'AGENT_GUIDE.
4. La production n'est jamais bloquée par un seul plan : le montage continue avec un placeholder signalé.

## 6. Backlog (pas encore construit)

- Export de timeline **FCPXML / EDL** depuis `edit_decisions.json` pour reprendre le montage dans DaVinci Resolve.
- Vérification réelle des clés au preflight (un appel `list models` gratuit), pour que le registre cesse de marquer « available » des clés factices.
- Tableau de continuité automatique : comparer les frames échantillonnées aux références des personnages via `visual_qa`.
