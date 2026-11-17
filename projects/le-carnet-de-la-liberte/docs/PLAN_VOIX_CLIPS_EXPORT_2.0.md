# VOIX, CLIPS PRIORITAIRES, MONTAGE ET EXPORT — plan 2.0 (rien n'est lancé en payant)

## 1. Voix françaises (dialogues synchronisés)
- **Fichiers prêts** : `animatic/dialogue_sync_for_recording.csv` (25 répliques : plan, locuteur, départ, fenêtre disponible, texte) et `animatic/dialogue_sync.srt` ; voix de repère dans l'animatic 2.0.
- **Marge** : à ×1,2 de la durée synthétique, toutes les répliques tiennent dans leur plan sauf P4 (≈ −0,04 s, à compenser de 0,3 s au montage).
- **Option A — comédiens (recommandée Younes/Amina)** : 0 crédit ; WAV 48 kHz 24 bits, prise par réplique (`SH14_A1_take01.wav`) ; autorisation parentale/école ; contrat de cession de droits.
- **Option B — synthèse naturelle** : ElevenLabs v3 via Magnific ≈ **0,2 crédit/caractère** (1 539 car. ⇒ **≈ 308 cr** un passage complet ; test de 8 répliques / 596 car. ⇒ **≈ 119 cr** par voix candidate ; +50 % de reprises ⇒ ≈ 460 cr). Alternative : compte ElevenLabs direct (connecteur à reconnecter, permissions manquantes).
- **Droits** : usage commercial/éducatif **non vérifié** pour votre plan Magnific/ElevenLabs → lire les conditions avant publication ; pas de clonage ; **aucune voix de Mohammed V (réelle ou imitée)** ; la « voix radio » reste anonyme, filtrée en post.

## 2. Trois clips animés prioritaires (image→vidéo, Kling 2.5, 1080p, 5 s, silencieux)
| Clip | Plan | Image de départ | Mouvement (prompt) | Coût |
|---|---|---|---|---|
| 1 | **SH11** pages qui tournent (motif central) | `references/p1/post/SH10_composite_final.png` | « A gentle breeze flips the notebook pages one after another; warm golden light rises from the paper; tiny ink sparkles drift upward; slow push-in. » | 325 |
| 2 | **SH26** fenêtre et lumière (pivot émotionnel) | `references/p1/SH26_fenetre_Amina_v001.png` | « The window shutters swing open, warm golden daylight floods the room, Amina lifts her head toward the light, curtains stir; slow push-in; ends in a soft bloom of white light. » | 325 |
| 3 | **SH38** plan final (cahier + lumière) | `references/p1/SH38_cahier_final_v001.png` (drapeau vectoriel ajouté en post) | « The notebook closes softly, warm light blooms, very slow pull-out; no flag, no text. » | 325 |
**Total : 975 crédits** (+ 325 par reprise). Solde 7 818 → 6 843 ; réserve THE LAST OF MEN ≥ 4 643 respectée. Options hors liste (non recommandées) : SH07, SH27 (+325 chacun). **Aucune génération sans autorisation écrite** (« J'autorise les 3 clips, 975 cr maximum »). L'animatic 2.0 utilise des images fixes animées en caméra à leur place.

## 3. Montage final (DaVinci Resolve ou FFmpeg)
- **Resolve** : suivre `docs/SOUND_MUSIC_AND_RESOLVE_PLAN_1.0.md` ; sources = fichiers listés dans `scripts/build_animatic_v2.py` (images + clips) ; timecodes = `shotlist/TECHNICAL_SHOT_LIST_1.0.md` (276 s).
- **FFmpeg** : `scripts/build_animatic_v2.py` reconstruit toute la timeline en local ; remplacer `animatic/dialogue_mix.wav` par le mix final (voix + musique + SFX).

## 4. Livraison
1. `scripts/export_final.sh ANIMATIC_VIDEO.mp4 FINAL_MIX.wav OUT.mp4` → 1920×1080, H.264 High, AAC stéréo 48 kHz.
2. `scripts/check_delivery.py OUT.mp4` valide résolution, codecs, **durée < 300 s** (cible 276 s).
3. Mix final : −16 LUFS intégré, crête vraie ≤ −1 dBTP.

## 5. Ce qui reste à décider (blocages)
SH03 (65 cr) · voix (comédiens ou synthèse ≈ 308 cr) · musique (piste libre vérifiée ou Lyria 3 ≈ 80 cr/clip) · 3 clips (975 cr) · drapeau vectoriel : forme officielle à confirmer (H5) · revue historique finale (H1–H12).
