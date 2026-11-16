# GENERATION PROMPT PACK 1.0 — PRÉPARATION UNIQUEMENT (aucune génération lancée)

> **Statut : rédigé, non exécuté.** Aucun appel payant n'a été fait. Chaque exécution exige l'approbation écrite de l'étape correspondante (voir `approvals/APPROVAL_REGISTER_1.0.md`).

## 1. Blocs réutilisables

**STYLE (à préfixer à tout prompt image)** :
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students
```

**NEGATIVE (à fournir quand le modèle accepte un negative prompt)** :
```
photorealistic photograph, fake archival photo, text, letters, captions, gibberish writing, watermark, logo, real person likeness, celebrity, king portrait, weapons, violence, blood, scary, distorted hands, extra fingers, modern objects in historical scenes, anachronistic clothing
```

**RÈGLE TEXTE** : Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.

**Modèle image proposé** : Google Nano Banana 2.1 (références personnage/style supportées), 16:9, 2k, 65 crédits/image (exact, simulé). Alternative bon marché pour tests de composition : flux-dev, 10 crédits. **Modèle vidéo proposé** : Kling 2.5, 1080p, 5 s, image de départ imposée, 325 crédits/clip (exact, simulé) — silencieux, donc son 100 % en post.

**Principe de continuité** : chaque génération de plan reçoit en références (1) le style board REF-00, (2) la fiche du ou des personnages, (3) le décor de référence. Toujours conserver le seed/ID de génération dans `approvals/generation_log.json`.

## 2. Blocs personnages

- **C-Younes** — YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile
- **C-Amina11** — AMINA aged 11 (1944): Moroccan girl, long dark braid, round face and the same warm brown eyes as Younes (family resemblance), simple ochre dress with a light cream headscarf [COSTUME TO VERIFY H5]
- **C-Amina20** — AMINA aged 20 (1953): same face and eyes, slimmer features, hair covered with a soft muted-blue headscarf, simple modest dress in muted tones, thoughtful gaze [COSTUME TO VERIFY H5]
- **C-Amina22** — AMINA aged 22-23 (1955-56): same face, radiant confident expression, warm coloured dress and light headscarf [COSTUME TO VERIFY H5]
- **C-Père** — AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person
- **C-Maîtresse** — THE TEACHER: woman in her 30s, warm smile, dark wavy shoulder-length hair, soft cardigan over a light blouse [headscarf choice = creative decision D6]
- **C-Mère** — YOUNES' MOTHER: woman in her mid 30s, gentle proud smile, casual modern home clothes, dark hair tied back

## 3. Images de référence (étape 1/2)

### REF-00 — Style board
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Single 16:9 style key image: stylized 3D look, warm classroom light blending into sepia notebook page edge. Used as STYLE reference for all later generations.
```

### REF-01 — Younes — character sheet
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Character sheet of YOUNES, front/3-quarter/profile + 3 expressions (curious, hesitant, proud), neutral background. YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile
```

### REF-02 — Amina — multi-age sheet
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Character sheet of ONE girl/woman at three ages on one sheet (11, 20, 23) with identical facial structure. AMINA aged 11 (1944): Moroccan girl, long dark braid, round face and the same warm brown eyes as Younes (family resemblance), simple ochre dress with a light cream headscarf [COSTUME TO VERIFY H5] | AMINA aged 20 (1953): same face and eyes, slimmer features, hair covered with a soft muted-blue headscarf, simple modest dress in muted tones, thoughtful gaze [COSTUME TO VERIFY H5] | AMINA aged 22-23 (1955-56): same face, radiant confident expression, warm coloured dress and light headscarf [COSTUME TO VERIFY H5]
```

### REF-03 — Le père — character sheet
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Character sheet, front/3-quarter/profile, two expressions (serious, tender). AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person
```

### REF-04 — La maîtresse — character sheet
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Character sheet, front/3-quarter, two expressions. THE TEACHER: woman in her 30s, warm smile, dark wavy shoulder-length hair, soft cardigan over a light blouse [headscarf choice = creative decision D6]
```

### REF-05 — La mère — character sheet
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Character sheet, front/3-quarter. YOUNES' MOTHER: woman in her mid 30s, gentle proud smile, casual modern home clothes, dark hair tied back
```

### REF-06 — Props sheet
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Props sheet on neutral background: old leather notebook (cover blank), faded sepia photograph (faces not legible), carved wooden box, 1950s tube radio (dial without text), school notebook (cahier). Blank surfaces.
```

### E1 — Environnement — classe 2026
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Wide shot of a bright Moroccan primary-school classroom, blackboard front, wooden desks, window light shaft, a small Moroccan flag corner (flag will be replaced by vector). Natural welcoming light. Empty of people.
```

### E2 — Environnement — maison familiale 2026
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Warm family living room, afternoon light, low sofa, window, Moroccan textiles, shelf; empty of people.
```

### E3 — Environnement — rue 1944
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Narrow old Moroccan medina street, 1944, warm ochre and sepia light, plastered walls, carved wooden doors, no modern objects, no signage text; empty of people. [ARCHITECTURE TO VERIFY H5]
```

### E4 — Environnement — intérieur 1940s
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Modest 1940s Moroccan home interior, low wooden table, carved window shutter, floor cushions, oil lamp; produce a DAY variant (warm ochre) and reuse with NIGHT blue-gray grade for 1953. Empty of people. [ARCHITECTURE TO VERIFY H5]
```

### E5 — Environnement — Rabat 1955
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Wide street and facades in Rabat, 1955, bright festive daylight, bunting poles (flags composited later), empty of people. [ARCHITECTURE TO VERIFY H5]
```

## 4. Prompts image par plan (étape 2)

Chaque prompt = `STYLE` + description ci-dessous + blocs personnages cités + `RÈGLE TEXTE`. Éclairage et étalonnage par époque : 1944 ocre/sépia chaud ; 1953 gris-bleu désaturé, contraste retenu ; 1955-56 de plus en plus chaud et lumineux ; 2026 lumière naturelle accueillante.

### SH01 — WS — Plan d'établissement de la classe, un rayon de soleil traverse la salle.
- Références à joindre : REF-00 (style), E1 classroom_2026, C-Younes, C-Maîtresse
- Revue historique requise avant génération : H10
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Wide establishing shot of a bright Moroccan primary-school classroom, a shaft of warm sunlight crossing the room, pupils seated at wooden desks seen from behind, a blackboard at the front, a small Moroccan flag in a corner, welcoming natural light. Lighting: natural welcoming light. Framing: WS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile | THE TEACHER: woman in her 30s, warm smile, dark wavy shoulder-length hair, soft cardigan over a light blouse [headscarf choice = creative decision D6].
```

### SH02 — MS — La maîtresse écrit la date au tableau puis pose sa question.
- Références à joindre : REF-00 (style), E1 classroom_2026, C-Maîtresse
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium shot of the kind young teacher at the blackboard, chalk in hand, turning slightly toward the class with a warm smile, board left empty (text will be composited later), soft window light. Lighting: natural welcoming light. Framing: MS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: THE TEACHER: woman in her 30s, warm smile, dark wavy shoulder-length hair, soft cardigan over a light blouse [headscarf choice = creative decision D6].
```

### SH03 — MCU — Younes lève la main, enthousiaste.
- Références à joindre : REF-00 (style), E1 classroom_2026, C-Younes
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium close-up of Younes (10) at his desk, hand raised high, eager open expression, classroom blurred behind. Lighting: natural welcoming light. Framing: MCU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile.
```

### SH04 — MS — La maîtresse félicite puis relance la question.
- Références à joindre : REF-00 (style), E1 classroom_2026, C-Maîtresse
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium shot of the teacher beside her desk, encouraging smile turning to a thoughtful, probing look. Lighting: natural welcoming light. Framing: MS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: THE TEACHER: woman in her 30s, warm smile, dark wavy shoulder-length hair, soft cardigan over a light blouse [headscarf choice = creative decision D6].
```

### SH05 — CU — Gros plan sur le regard intrigué de Younes (la maîtresse répond hors champ).
- Références à joindre : REF-00 (style), E1 classroom_2026, C-Younes
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Close-up on Younes' face, hesitant then intrigued, eyes slightly lifted, soft rim light, shallow depth of field. Lighting: natural welcoming light. Framing: CU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile.
```

### SH07 — MS — Younes ouvre une ancienne boîte en bois et découvre le carnet et une photographie.
- Références à joindre : REF-00 (style), E2 home_2026, C-Younes, P-boite_bois, P-carnet
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium shot, Younes kneeling in a warm family living room, lifting the lid of an old carved wooden box, afternoon light, a yellowed notebook and a faded photograph inside. Lighting: natural welcoming light. Framing: MS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile.
```

### SH08 — CU — Gros plan sur la couverture : « AMINA — MES SOUVENIRS » et la photographie.
- Références à joindre : REF-00 (style), P-carnet, P-photo_famille
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Close-up of an old leather notebook cover with worn corners, a faded sepia family photograph tucked beside it (face not legible), cover left blank - title composited later. Lighting: natural welcoming light. Framing: CU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.
```

### SH09 — MS 2-shot — Younes interroge sa mère, qui lui parle d'Amina.
- Références à joindre : REF-00 (style), E2 home_2026, C-Younes, C-Mère, P-carnet
- Revue historique requise avant génération : H1
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium two-shot in a family living room: Younes holding the notebook, his mother (mid 30s, warm) answering with a gentle proud smile. Lighting: natural welcoming light. Framing: MS 2-shot. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile | YOUNES' MOTHER: woman in her mid 30s, gentle proud smile, casual modern home clothes, dark hair tied back.
```

### SH10 — CU — Younes ouvre délicatement le carnet : première page « 11 JANVIER 1944 ».
- Références à joindre : REF-00 (style), P-carnet, C-Younes
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Over-the-shoulder close-up of Younes' hands opening the notebook to a yellowed first page, page left blank - date composited later in handwriting. Lighting: natural welcoming light. Framing: CU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile.
```

### SH11 — CU — Un souffle de vent fait tourner les pages ; les photographies s'animent dans l'imagination de Younes.
- Références à joindre : REF-00 (style), P-carnet
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Close-up of the open notebook, pages caught by a breeze, warm golden light spilling from the pages (imagination, not time travel). Lighting: natural welcoming light. Framing: CU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.
```

### SH13 — WS — Dans une rue ancienne, Amina (11 ans) marche avec son père ; des habitants discutent.
- Références à joindre : REF-00 (style), E3 street_1944, C-Amina11, C-Père
- Revue historique requise avant génération : H5, H11
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Wide shot of a narrow old Moroccan medina street in 1944, warm ochre light, Amina (11) walking beside her father, neighbours chatting in front of a house, no modern elements. Lighting: warm ochre and sepia light. Framing: WS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 11 (1944): Moroccan girl, long dark braid, round face and the same warm brown eyes as Younes (family resemblance), simple ochre dress with a light cream headscarf [COSTUME TO VERIFY H5] | AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person.
```

### SH14 — MS 2-shot — Amina interroge son père sur la liberté.
- Références à joindre : REF-00 (style), E3 street_1944, C-Amina11, C-Père
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium two-shot walking, Amina looking up at her father with curiosity. Lighting: warm ochre and sepia light. Framing: MS 2-shot. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 11 (1944): Moroccan girl, long dark braid, round face and the same warm brown eyes as Younes (family resemblance), simple ochre dress with a light cream headscarf [COSTUME TO VERIFY H5] | AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person.
```

### SH15 — MS — Le père explique le protectorat et le désir d'indépendance.
- Références à joindre : REF-00 (style), E3 street_1944, C-Père
- Revue historique requise avant génération : H6
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium shot of the father, calm and serious, explaining with a gentle gesture. Lighting: warm ochre and sepia light. Framing: MS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person.
```

### SH16 — MS — À la maison, le père dépose une feuille sur la table.
- Références à joindre : REF-00 (style), E4 home_1940s, C-Père, C-Amina11
- Revue historique requise avant génération : H5
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Interior of a modest 1940s Moroccan home, father placing a single sheet of paper on a low wooden table, Amina watching, warm sepia light through a carved window. Lighting: warm ochre and sepia light. Framing: MS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person | AMINA aged 11 (1944): Moroccan girl, long dark braid, round face and the same warm brown eyes as Younes (family resemblance), simple ochre dress with a light cream headscarf [COSTUME TO VERIFY H5].
```

### SH17 — INSERT — Insert : illustration éducative du document, légende datée.
- Références à joindre : REF-00 (style)
- Revue historique requise avant génération : H3b, H5
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Illustrated educational document: aged paper with illegible stylised calligraphy lines, ornamental border, NO readable fake text, NOT an archival reproduction. Lighting: warm ochre and sepia light. Framing: INSERT. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.
```

### SH18 — MS 2-shot — Amina demande ce que signifie être indépendant ; le père répond.
- Références à joindre : REF-00 (style), E4 home_1940s, C-Amina11, C-Père
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium two-shot at the table, Amina questioning, father answering with quiet conviction. Lighting: warm ochre and sepia light. Framing: MS 2-shot. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 11 (1944): Moroccan girl, long dark braid, round face and the same warm brown eyes as Younes (family resemblance), simple ochre dress with a light cream headscarf [COSTUME TO VERIFY H5] | AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person.
```

### SH19 — CU — Amina sourit et écrit dans son carnet ; la caméra se rapproche des mots.
- Références à joindre : REF-00 (style), E4 home_1940s, C-Amina11, P-carnet
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Close-up of Amina smiling while writing in the notebook with a pencil, page area left clear for composited handwriting. Lighting: warm ochre and sepia light. Framing: CU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 11 (1944): Moroccan girl, long dark braid, round face and the same warm brown eyes as Younes (family resemblance), simple ochre dress with a light cream headscarf [COSTUME TO VERIFY H5].
```

### SH21 — WS — Neuf années ont passé : Amina est une jeune femme d'environ vingt ans.
- Références à joindre : REF-00 (style), E4 home_1940s (night), C-Amina20, C-Père
- Revue historique requise avant génération : H5
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Wide interior shot of the same home at dusk, muted blue-gray palette, Amina (20) and her father near an old radio on a shelf. Lighting: muted blue-gray evening light, restrained contrast. Framing: WS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 20 (1953): same face and eyes, slimmer features, hair covered with a soft muted-blue headscarf, simple modest dress in muted tones, thoughtful gaze [COSTUME TO VERIFY H5] | AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person.
```

### SH22 — CU — Une radio ancienne diffuse une annonce (reconstitution fictive).
- Références à joindre : REF-00 (style), E4 home_1940s (night), P-radio
- Revue historique requise avant génération : H8, H6
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Close-up of an old 1950s tube radio with glowing dial in a dim room, blue-gray tones, no text on dial. Lighting: muted blue-gray evening light, restrained contrast. Framing: CU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.
```

### SH23 — MS 2-shot — Silence, puis Amina interroge son père ; il l'encourage.
- Références à joindre : REF-00 (style), E4 home_1940s (night), C-Amina20, C-Père
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium two-shot, Amina anxious, father reassuring, low contrast blue-gray light. Lighting: muted blue-gray evening light, restrained contrast. Framing: MS 2-shot. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 20 (1953): same face and eyes, slimmer features, hair covered with a soft muted-blue headscarf, simple modest dress in muted tones, thoughtful gaze [COSTUME TO VERIFY H5] | AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person.
```

### SH24 — CU — Amina regarde son carnet et écrit.
- Références à joindre : REF-00 (style), E4 home_1940s (night), C-Amina20, P-carnet
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Close-up of Amina (20) writing in the notebook by lamplight, resolute expression, page area clear for composited handwriting. Lighting: muted blue-gray evening light, restrained contrast. Framing: CU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 20 (1953): same face and eyes, slimmer features, hair covered with a soft muted-blue headscarf, simple modest dress in muted tones, thoughtful gaze [COSTUME TO VERIFY H5].
```

### SH25 — MONTAGE — Les saisons défilent ; les feuilles du carnet portent 1953, 1954, 1955.
- Références à joindre : REF-00 (style), E4 window_seasons x3, P-carnet pages
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Three seasonal window views (autumn, winter, spring) as keyframes behind notebook pages dated 1953/1954/1955. Lighting: muted blue-gray light, restrained contrast. Framing: MONTAGE. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.
```

### SH26 — MS — Une fenêtre s'ouvre, la lumière revient ; voix hors champ ; Amina lève les yeux ; grande lumière.
- Références à joindre : REF-00 (style), E4 home_1940s (day, warm), C-Amina22
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium shot of Amina (22) as a window shutter swings open and warm light floods in, her face lifting with hope. Lighting: warm, bright, hopeful light. Framing: MS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 22-23 (1955-56): same face, radiant confident expression, warm coloured dress and light headscarf [COSTUME TO VERIFY H5].
```

### SH27 — WS — Une foule joyeuse accueille le retour du souverain ; drapeaux marocains.
- Références à joindre : REF-00 (style), E5 rabat_1955
- Revue historique requise avant génération : H5, H6, H7
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Wide shot of a joyful crowd in Rabat, families, children on shoulders, Moroccan flags waving (flags will be replaced by composited vector flags), warm bright light, the sovereign NOT shown. Lighting: warm, bright, hopeful light. Framing: WS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.
```

### SH28 — MS 2-shot — Amina rejoint son père dans la foule ; il lui serre la main.
- Références à joindre : REF-00 (style), E5 rabat_1955, C-Amina22, C-Père
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium two-shot in the crowd, Amina radiant, father gently squeezing her hand. Lighting: warm, bright, hopeful light. Framing: MS 2-shot. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 22-23 (1955-56): same face, radiant confident expression, warm coloured dress and light headscarf [COSTUME TO VERIFY H5] | AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person.
```

### SH29 — INSERT — Page « 18 NOVEMBRE 1955 » : illustration historique du discours du Trône + texte pédagogique.
- Références à joindre : REF-00 (style), P-carnet page
- Revue historique requise avant génération : H3, H6
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Symbolic educational illustration of a throne-day ceremony: empty ornate throne, palace architecture, crowd silhouettes; NO portrait of the sovereign, NO quote. Lighting: warm, bright, hopeful light. Framing: INSERT. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.
```

### SH30 — CU — Amina écrit dans son carnet.
- Références à joindre : REF-00 (style), E4 home_1940s (day, warm), C-Amina22, P-carnet
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Close-up of Amina (22) writing, hopeful, bright warm light. Lighting: warm, bright, hopeful light. Framing: CU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 22-23 (1955-56): same face, radiant confident expression, warm coloured dress and light headscarf [COSTUME TO VERIFY H5].
```

### SH31 — INSERT — Page « 2 MARS 1956 » : illustration symbolique des négociations et d'un document officiel.
- Références à joindre : REF-00 (style), P-carnet page
- Revue historique requise avant génération : H4, H5
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Symbolic illustration: two abstract delegations at a table with an official document, flags as vector overlays; no recognisable real person. Lighting: warm, bright, hopeful light. Framing: INSERT. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.
```

### SH32 — MS 2-shot — Le père annonce la reconnaissance ; Amina ferme les yeux, émue, serre son carnet.
- Références à joindre : REF-00 (style), E4 home_1940s (day, warm), C-Amina23, C-Père
- Revue historique requise avant génération : H4
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium two-shot, father delivering news with joy, Amina closing her eyes, hugging the notebook to her chest. Lighting: warm, bright, hopeful light. Framing: MS 2-shot. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 22-23 (1955-56): same face, radiant confident expression, warm coloured dress and light headscarf [COSTUME TO VERIFY H5] | AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person.
```

### SH34 — CU — Amina, doucement ; le carnet se referme.
- Références à joindre : REF-00 (style), E4 home_1940s (day, warm), C-Amina23, P-carnet
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Close-up of Amina (23), serene, gently closing the notebook, warm bright light. Lighting: warm, bright, hopeful light. Framing: CU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: AMINA aged 22-23 (1955-56): same face, radiant confident expression, warm coloured dress and light headscarf [COSTUME TO VERIFY H5].
```

### SH35 — WS — Younes devant ses camarades, il présente le carnet d'Amina.
- Références à joindre : REF-00 (style), E1 classroom_2026, C-Younes, C-Maîtresse, P-carnet
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Wide classroom shot, Younes standing at the front holding the notebook, classmates attentive, teacher at the side. Lighting: natural welcoming light. Framing: WS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile | THE TEACHER: woman in her 30s, warm smile, dark wavy shoulder-length hair, soft cardigan over a light blouse [headscarf choice = creative decision D6].
```

### SH36 — MCU — Younes répond avec gravité.
- Références à joindre : REF-00 (style), E1 classroom_2026, C-Younes, P-carnet
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium close-up of Younes, earnest, proud, notebook in hands. Lighting: natural welcoming light. Framing: MCU. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile.
```

### SH37 — MS — « Comment ? » ; Younes répond, puis écrit dans son cahier.
- Références à joindre : REF-00 (style), E1 classroom_2026, C-Younes, C-Maîtresse
- Revue historique requise avant génération : aucune
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Medium shot, teacher and Younes, Younes then writing in his school notebook at his desk (cahier open, text composited). Lighting: natural welcoming light. Framing: MS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later. Characters: YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, white collared shirt, navy knitted sweater vest, navy trousers, school backpack [LOCKED REF-01 v002; attach REF-01_Younes_v002 as character reference], small gap-toothed curious smile | THE TEACHER: woman in her 30s, warm smile, dark wavy shoulder-length hair, soft cardigan over a light blouse [headscarf choice = creative decision D6].
```

### SH38 — WS — Le cahier se referme ; un drapeau marocain flotte dans la lumière ; titre.
- Références à joindre : REF-00 (style), E1 classroom_2026, P-cahier
- Revue historique requise avant génération : H5
```
Cinematic stylized 3D animated film, original character design (not copying any existing studio character), expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, 16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students. Closing school notebook in foreground, soft blurred Moroccan flag drifting in warm light behind (flag replaced by composited vector flag). Lighting: natural welcoming light. Framing: WS. Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later.
```

## 5. Prompts image→vidéo (étape 3 — uniquement les 5 plans animés)

Départ = image de départ validée (start frame). Durée de génération 5 s. Pas de dialogue ni de musique générés (Kling 2.5 est silencieux).

### SH07 (écran 6.0 s)
```
Younes slowly lifts the wooden lid, curious, his face lit by a soft glow from the box; dust motes drift in sunlight; subtle push-in. Keep character identity and costume exactly as in the start frame. Stylized 3D look unchanged. No text, no new objects.
```

### SH11 (écran 5.0 s)
```
A gentle breeze flips the notebook pages one after another; warm golden light rises from the paper; tiny ink sparkles drift upward; slow push-in. Keep character identity and costume exactly as in the start frame. Stylized 3D look unchanged. No text, no new objects.
```

### SH26 (écran 11.5 s)
```
The window shutters swing open, warm golden daylight floods the room, Amina lifts her head toward the light, curtains stir; slow push-in; ends in a soft bloom of white light. Keep character identity and costume exactly as in the start frame. Stylized 3D look unchanged. No text, no new objects.
```

### SH27 (écran 7.0 s)
```
The crowd cheers and waves, flags ripple in a breeze, children bounce on shoulders, slow pull-out reveal; no individual is identifiable. Keep character identity and costume exactly as in the start frame. Stylized 3D look unchanged. No text, no new objects.
```

### SH38 (écran 5.5 s)
```
The notebook closes softly, warm light blooms, a flag ripples gently in the background, very slow pull-out. Keep character identity and costume exactly as in the start frame. Stylized 3D look unchanged. No text, no new objects.
```

## 6. Ce qui n'est PAS généré
- Dates, cartons, légendes, ligne du temps, titre : composités (Remotion/HyperFrames/DaVinci).
- Drapeaux marocains : vecteur dessiné localement (étoile verte à cinq branches, rouge officiel) et incrusté ; jamais généré par IA.
- Calligraphie arabe et textes de documents : jamais générés.
- Archives : aucune « archive » fabriquée ; les inserts historiques portent la mention « ILLUSTRATION PÉDAGOGIQUE — non archive ».
- Mohammed V : aucun visage, aucune voix, aucun discours inventé.
