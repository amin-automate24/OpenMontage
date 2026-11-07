# Audit de l'environnement — Film Studio

> Instantané du **3 novembre 2026**, session cloud Claude Code.
> Il s'agit d'une photo d'un moment : relancer le preflight au début de chaque production
> (`registry.provider_menu_summary()`, voir `AGENT_GUIDE.md` → Mandatory Preflight).

## 1. Machine

| Élément | Valeur | Conséquence |
|---|---|---|
| OS | Ubuntu 24.04.5 LTS (conteneur cloud **éphémère**) | Tout ce qui n'est pas poussé ou exporté est perdu à la fin de la session. `projects/` est gitignoré. |
| CPU / RAM | 4 cœurs · 15 Go | Suffisant pour FFmpeg, Remotion, HyperFrames en 1080p. |
| GPU | **Aucun** | Pas de génération vidéo/image locale (WAN, LTX, ComfyUI, SadTalker…). Toute génération passe par API. |
| Disque | ~30 Go d'allocation | ~60 à 90 min de rushes 1080p + intermédiaires ; nettoyer entre deux projets. |
| Claude Code | 2.1.317 | — |
| Python / Node | 3.13 · Node 22.23 (npx 10.9) | Node ≥ 22 : HyperFrames OK. |
| FFmpeg / FFprobe | 6.1.1 — libx264, ProRes (`prores_ks`), DNxHD, AAC, `ebur128`, `loudnorm`, `lut3d`, `blackdetect`, `freezedetect` | Montage, étalonnage par LUT, normalisation loudness, QC et master ProRes possibles en local. |
| DaVinci Resolve / Premiere | **Non installés** (Linux sans interface graphique) | Le montage se fait en FFmpeg/Remotion/HyperFrames ; pour finir sous Resolve, il faut l'exporter sur la machine de l'utilisateur (voir §5). |

## 2. Moteurs de composition (OpenMontage `video_compose`)

| Runtime | État | Rôle dans un film |
|---|---|---|
| FFmpeg | ✅ opérationnel | Coupes, concat, trim, LUT, titres simples, mix, export |
| Remotion | ✅ opérationnel (`node_modules` installé pendant cet audit) | Titres et génériques animés, sous-titres mot à mot, transitions précises |
| HyperFrames | ✅ opérationnel (v0.9.9) | Typographie cinétique, cartons-titres HTML/GSAP, mondes Three.js |

## 3. Capacités de génération — état réel

### Ce que le registre annonce et ce qui marche vraiment

Le registre marque `google_imagen`, `gemini_omni_video`, `google_music` (Lyria), `gemini_tts`, `google_tts`
et `pexels_*` comme **available**. **C'est inexact** : le registre ne vérifie que la *présence* des variables
d'environnement. Vérification faite :

| Variable | Longueur | Test réel | Verdict |
|---|---|---|---|
| `GEMINI_API_KEY` | 6 caractères | `400 API_KEY_INVALID` (Generative Language API) | ❌ valeur factice, pas une vraie clé |
| `PEXELS_API_KEY` | 6 caractères | `401` (api.pexels.com) | ❌ valeur factice, pas une vraie clé |

**Aucune clé API de génération valide n'est donc configurée dans le conteneur.** Tous les outils natifs
d'OpenMontage qui dépendent de ces clés échoueront à l'appel.

### Connecteurs MCP de la session (hors registre OpenMontage)

| Connecteur | Statut vérifié | Capacités utiles | Solde |
|---|---|---|---|
| Runway | ✅ connecté (plan Standard) | text/image-to-video, multishot, images, musique, SFX, voix, upscale 4K | **8 crédits**, moins d'un plan vidéo. Recharge : 1 000 crédits = 10 $ |
| Reel Studio | ✅ connecté | Film/scènes/plans/cast/lieux, timeline, review, export | **6 crédits** |
| Veo (MCP) | ✅ connecté | veo3, veo3-fast, veo31, veo31-fast, ingredients (multi-image) · 16:9/9:16 · 1080p/4K | solde non exposé par l'outil, à vérifier avant le premier appel |
| Midjourney (MCP) | ✅ connecté | Images de référence, personnages, storyboard, vidéo | solde non exposé |
| ElevenLabs (MCP restreint) | ✅ connecté | Voix (v3/v4), **SFX** (≤ 30 s, boucles), design de voix, effets audio, transcription | pas de musique ni d'image ni de vidéo dans ce connecteur |
| Magnific | ✅ connecté | Upscale, relight, étalonnage vidéo, SFX/musique | **0 crédit** (plan gratuit) |
| Canva, Gamma, HyperFrames (HeyGen) | ✅ connectés | Affiches, dossiers de présentation | — |
| Dropbox, Google Drive | ✅ connectés | **Livraison des fichiers finaux hors du conteneur éphémère** | — |
| Higgsfield | ❌ échec de connexion (404) | — | à reconnecter côté réglages |

Les soldes de Veo et de Midjourney ne s'affichent pas avec les outils de lecture : je les vérifie juste avant tout appel payant, et toujours avec ton accord.

## 4. Matrice : opérationnel / à configurer / intervention humaine

### ✅ Opérationnel maintenant (automatisable sans intervention)
- Développement : concept, scénario, bible visuelle, bible personnages, storyboard, prompts (Claude).
- Structure de projet, journal de production, checkpoints, board Backlot.
- Montage, transitions, titres, sous-titres SRT, étalonnage par LUT/courbes, mixage, loudness EBU R128.
- QC technique (`scripts/film_studio.py qc`) : résolution, fps, codecs, dérive A/V, LUFS, true peak, noirs, gels, silences.
- Export H.264/AAC 1080p24 + master ProRes 422 HQ + SRT (`scripts/film_studio.py export`).
- Échantillonnage de frames et analyse de scènes (`frame_sampler`, `scene_detect`, `video_analyzer`) pour le QC visuel.
- Animation 2.5D sur stills (parallax, Ken Burns, Remotion), mondes Three.js (HyperFrames).

### 🔧 Nécessite une configuration (≈ 1 minute, côté réglages de l'environnement)
- **Une vraie `GEMINI_API_KEY`** (palier payant) remplace la valeur factice et débloque d'un coup Gemini Omni (vidéo avec audio synchronisé, ~0,10 $/s), Imagen (images), Lyria (musique) et Gemini TTS, tous dans le pipeline natif.
- **`FAL_KEY`** débloque la plus large palette vidéo du registre (Seedance, Kling, Veo, MiniMax, WAN…), plus FLUX et la musique ElevenLabs via fal.
- **`PEXELS_API_KEY` réelle** (gratuite) pour les plans d'archive et de stock.
- Recharge Runway (MCP) : c'est l'alternative si tu préfères ne pas ajouter de clé.

Les clés s'ajoutent dans les réglages de l'environnement cloud (menu de l'environnement dans la barre de titre de la session → Edit → *Network secrets* / variables d'environnement). Une nouvelle session les prend en compte. **Ne jamais coller une clé dans la conversation.**

### 👤 Nécessite une intervention humaine
- Validation à chaque porte (concept, scénario, storyboard, assets) et accord avant toute dépense.
- Achat de crédits et choix des abonnements.
- Visionnage final : le QC automatique ne remplace pas l'œil d'un réalisateur.
- Finition dans DaVinci Resolve, si tu le souhaites, sur ta machine.
- Reconnexion de Higgsfield.

## 5. Limites à connaître

1. **Cohérence des personnages.** Aucun outil ne garantit un visage identique d'un plan à l'autre. On limite le risque avec des images de référence (Midjourney/Imagen), l'image-to-video depuis une keyframe validée, des plans larges ou de dos, et peu de gros plans.
2. **Lip-sync.** Aucun outil d'avatar ou de lip-sync n'est configuré (HeyGen et Kling ne sont pas configurés, et il n'y a pas de GPU pour Wav2Lip). Pour un premier film, mieux vaut ne pas avoir de dialogue synchronisé à l'image, ou n'en avoir qu'en voix off.
3. **Durée par plan.** Les générateurs produisent des plans de 4 à 10 s : un film se construit plan par plan, jamais en un seul prompt.
4. **Timeline pour Resolve/Premiere.** OpenMontage produit `edit_decisions.json`, pas encore d'export FCPXML ou EDL. C'est une étape à construire (voir ARCHITECTURE.md, backlog).
5. **Persistance.** Les médias générés vivent dans `projects/` (gitignoré) sur un conteneur éphémère. Livraison via Dropbox ou Google Drive, avec ton accord.
