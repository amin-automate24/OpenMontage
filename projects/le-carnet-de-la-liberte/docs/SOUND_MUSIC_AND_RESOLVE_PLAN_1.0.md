# SOUND DESIGN, MUSIC, LICENSING AND DAVINCI RESOLVE PLAN 1.0 (préparation uniquement)

## 1. Voix

- **État** : voix de prévisualisation `espeak-ng` seulement (`animatic/voices/`, `animatic/dialogue_mix.wav`) — usage interne, **ne pas publier**.
- **Casting à prévoir** : Younes (garçon ≈ 10 ans), Amina (une voix ou deux : fillette 11 ans / jeune femme), le père, la maîtresse, la mère, voix de la radio (reconstitution, anonyme), voix hors champ. Enfants : autorisation parentale / de l'école.
- **Interdits** : cloner ou imiter la voix de Mohammed V ; ajouter une narration explicative.
- **Spécifications d'enregistrement** : WAV 48 kHz 24 bits mono, une prise par réplique, nom `SH14_A1_take01.wav`, 1 s de silence de tête, accent français neutre ; marge de durée demandée : voir `docs/HISTORICAL_AND_TIMING_FLAGS_1.0.md` (T2).
- **Option TTS** (si approuvée) : ≈ 310 crédits Magnific pour un passage complet ; test préalable sur 2 répliques ; vérifier la licence.

## 2. Plan sonore par scène (ambiances et bruitages, sans musique)

| Scène | Ambiance | Bruitages clés |
|---|---|---|
| 1 (2026) | Salle de classe, murmures, cour au loin | Craie sur tableau (SH02), main levée, chaises |
| 2 | Salon calme, horloge discrète | Couvercle de boîte (SH07), papier ancien, souffle de vent (SH11), « souffle d'encre » en transition |
| 3 (1944) | Rue de médina : voix lointaines, pas, artisans | Feuille posée sur table, crayon sur papier (SH19) |
| 4 (1953) | Maison silencieuse, nuit tombante | **Radio à lampes** (grésillement, filtre téléphonique), silence après l'annonce, pages qui défilent, fenêtre qui s'ouvre (SH26), oiseaux et rues revenant |
| 5 (1955-56) | Grande foule festive à Rabat, enfants, vent dans les drapeaux | Pages, crayon, carnet qui se referme (SH34) |
| 6 (2026) | Classe attentive | Cahier qui se ferme, drapeau dans le vent (SH38) |

Banques d'effets : à fournir libres de droits (ou génération approuvée) ; **aucun SFX n'est généré à ce jour** (le modèle vidéo proposé est silencieux).

## 3. Musique — fiche de repères (cue sheet)

Brief : instrumentation chaleureuse (oud, qanun, nay discrets, cordes douces, percussions légères), thème du carnet simple et mémorisable, **sans imiter un hymne ni une pièce existante**. Mixage sous les dialogues (−18 à −22 LU relatif).

| Repère | Plans | Timecode | Intention |
|---|---|---|---|
| M1 Curiosité | SH05 → SH06 | 0:20 → 0:30 | Entrée discrète du thème quand Younes réfléchit |
| M2 Thème du carnet | SH07 → SH12 | 0:30 → 1:05 | Merveille douce ; magie = imagination |
| M3 Ocre 1944 | SH13 → SH20 | 1:05 → 2:00 | Espoir, rythme marché léger |
| M4 Silence / tension | SH21 → SH25 | 2:00 → 2:43 | Presque silence, nappe grave ; **aucune musique pendant la radio (SH22)** |
| M5 Lumière | SH26 → SH27 | 2:43 → 3:05 | Montée vers la lumière ; « la musique accompagne la joie populaire » |
| M6 Joie populaire | SH27 → SH28 | 2:55 → 3:09 | Célébration, tempo plus vif |
| M7 Mémoire | SH29 → SH34 | 3:09 → 4:10 | Retour calme du thème ; **ligne du temps (SH33) quasi sans musique pour la lisibilité** |
| M8 Héritage | SH35 → SH38 | 4:10 → 4:30 | Résolution du thème ; fin tenue sur le plan du drapeau |

**Disponibilité** : aucune piste fournie ; Artlist sans crédits ; Lyria 3 = 80 cr/clip (≈ 240 pour 3 clips) ; ElevenLabs Music 270 s = 5 400 cr (écarté). Option gratuite : piste libre de droits déposée dans `music_library/` avec preuve de licence.

**Licences** : conserver licence/preuve d'achat par piste dans `approvals/licenses/` ; vérifier l'usage éducatif et la diffusion en ligne.

## 4. DaVinci Resolve — instructions de montage

**Projet** : 1920×1080, **25 i/s**, espace colorimétrique Rec.709 gamma 2.4, timeline 1 920×1 080.

**Pistes** : V1 plans / V2 cartons & dates (PNG avec alpha, ou Fusion) / V3 drapeau vectoriel et surimpressions / V4 grain & vignette ; A1 dialogues / A2 ambiances / A3 bruitages / A4 musique / A5 sous-titres éventuels.

**Import** : importer `shotlist/shot_list.csv` comme référence ; créer un marqueur par plan (nom `SHxx`, durée de la liste). Respecter les timecodes de `TECHNICAL_SHOT_LIST_1.0.md` (la timeline démarre à 00:00:00:00).

**Plans fixes** : appliquer les mouvements de `camera` (push-in lent ≈ +4 %, push-in +8 %, push-in fort +20 %, pull-out, pan) via Transform en images clés avec courbe ease-in-out ; **ne jamais animer sur plus de 20 % de zoom** sans régénération 2k→4k.

**Transitions page de carnet** : fondu enchaîné 15 images pour SH06/12/17/20/25/29/31/33 ; effet « encre » = calque de texture papier + masque animé (Fusion) ; **éclair blanc** à la fin de SH26 (≈ 1,5 s).

**Étalonnage (color script)** : 1944 ocre/sépia chaud (T° ≈ 3 800 K, contraste moyen) ; 1953 gris-bleu désaturé (sat. −25 %, contraste retenu) ; 1955-56 progressivement plus chaud et lumineux ; 2026 naturel. Un seul nœud de base par époque + ajustement par plan.

**Cartons & texte** : dates, légendes, ligne du temps, titre en post (police lisible, ≥ 48 px, contraste fort) ; ligne du temps ≥ 5 s avec toutes les dates visibles ; mentions « ILLUSTRATION PÉDAGOGIQUE — non archive » (D3) en bas de SH17, SH29, SH31.

**Audio** : dialogues −16 LUFS court terme ; musique sous dialogue ; mix final **−16 LUFS intégré, true peak ≤ −1 dBTP**, stéréo 48 kHz.

**Export** : H.264 (profil High), 1920×1080 25p, ≈ 12–16 Mb/s, AAC stéréo 48 kHz 256 kb/s, `.mp4`, nom `LE_CARNET_DE_LA_LIBERTE_v001_FINAL.mp4`. **Durée à vérifier : 4:30 (ou 4:36 si D1 accepté) — jamais > 5:00.**

**Livrables de contrôle** : export de contrôle 720p + capture des 38 plans + checklist (texte lisible, dates correctes, aucune archive fabriquée, drapeau conforme).
