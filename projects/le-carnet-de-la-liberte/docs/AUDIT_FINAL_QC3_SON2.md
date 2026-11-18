# AUDIT FINAL — MASTER CANDIDAT QC3 SON2 (NON FINAL)
Date : 18/11/2026. Inspection seule : aucun fichier modifié, aucun rendu, aucun crédit.

## 0. Fichier audité
`animatic/MASTER_CANDIDATE_NON_FINAL_QC3_SON2_1080p.mp4` — 124 381 498 o, sha256 `6f207586…`, identique au dépôt Dropbox `/LE_CARNET_DE_LA_LIBERTE/MASTER_CANDIDATE_NON_FINAL/` (content_hash vérifié). Distinct de QC1 / QC2 / QC2 SON2 (nom, hash, images SH06/SH33).
Le Bureau Windows (« Court métrage le carnet de la liberté ») n'était pas accessible depuis cette session (aucun dossier d'ordinateur partagé) : l'audit porte sur cette copie de référence.

## 1. Points conformes
**Technique**
- 1920×1080, 25 fps, H.264 High yuv420p, 6903 images ; AAC LC 48 kHz stéréo 198 kb/s. Vidéo 276,12 s, audio 276,00 s. `check_delivery.py` : tous critères vrais.
- Décodage intégral sans erreur ; aucune image noire hors fondu prévu ; aucun silence > 1 s (−50 dB).
- −16,1 LUFS intégré, crête vraie −1,1 dBTP, crête échantillon −1,25 dBFS, aucun écrêtage (flat factor 0), DC −0,00004.
- Synchronisation voix/mix : décalage 1 ms (enveloppe du stem dialogue vs mix final).
**SH06 (27,5–30,5 s)** : craie effacée 27,8–28,4 s, carton 28,4–28,7 s, « 18 novembre » pleinement lisible 28,7–30,0 s (1,3 s), aucune image avec craie et carton superposés ; fondu 0,5 s vers SH07 identique à QC2.
**SH33 (225,5–239,5 s)** : six dates + légendes + note finale ; frise complète figée 231,6–239,6 s (8,0 s mesurés) ; coupe franche vers SH34 sans saut.
**Histoire** : 11 janvier 1944 (Manifeste de l'indépendance), 20 août 1953 (exil du sultan), 16 novembre 1955 (retour), 18 novembre 1955 (discours du Trône), 2 mars 1956 (reconnaissance française), 7 avril 1956 (fin du protectorat espagnol au Nord) — dates exactes ; note « Le processus d'unification territoriale s'est poursuivi après 1956 » prudente et juste.
**Reconstitution vs archive** : mentions « ILLUSTRATION PÉDAGOGIQUE — non archive / reconstitution » (SH16, SH17), « Reconstitution fictive » (SH22), « ILLUSTRATION SYMBOLIQUE — non archive » (SH31). Portraits de Mohammed V (SH27–28) = photo d'archive Anefo 905-8914 (CC0) en pancartes ; aucun visage ni voix générés du souverain. Drapeaux vectoriels locaux (rouge 193/39/45, pentagramme vert).
**Dialogues** : 32 répliques ; rapport voix/fond (pré-mix) 24–47 dB, minimum 14,3 dB (V1, 166,5 s) et 15,3 dB (A5, 182,5 s, foule) ; niveau des répliques −12,8 à −17,0 dBFS RMS. SRT `SUBTITLES_FR_QC1.srt` : chaque voix démarre 0,06–0,17 s après le début du sous-titre (calage correct pour QC3, l'audio n'ayant pas bougé).
**Narration** : arc clair classe 2026 → carnet → 1944 → 1953 → 1955 → 1956 → classe ; cartons de date à chaque saut d'époque ; message final explicite (T5/Y5).

## 2. Défauts
**Critiques** : aucun.
**Importants** : aucun démontré par mesure.
**Mineurs**
1. Dérive images/son : les coupes tombent 0,02 à 0,10 s après leur position audio (arrondi des durées de plans à 25 fps ; ex. 70,60 / 180,60 / 239,60 / 270,60 s au lieu de 70,5 / 180,5 / 239,5 / 270,5 s). Plans sans mouvement de lèvres → impact faible ; existait depuis QC1.
2. Dynamique : LRA 15,8 LU ; passages calmes à −31…−36 LUFS (court terme) p. ex. 50,5, 109,6, 123,0, 212,6, 247,3 s, soit 13–15 LU sous les dialogues ; en classe bruyante, la musique/ambiance de ces passages peut se perdre (les voix restent claires).
3. Flash noir de 0,12 s à 208,60–208,72 s (entrée en fondu au noir de SH31, voulue dans le script) ; perceptible comme un clignement.
4. Plans entièrement fixes : SH04 15,0–20,6 s, SH13 65,1–70,6 s, SH15 77,1–86,1 s (9 s, choix validé), SH30 202,6–208,6 s, SH35 250,6–253,6 s ; rythme plus lent pour 9–12 ans.
5. Lisibilité en projection : légendes SH33 en 32 px (≈ 2,2 cm sur un écran de 1,1 m de haut, lisibles à 6–7 m environ) ; textes manuscrits SH19 « Un jour, mon pays sera libre » et SH24 « Nous garderons espoir » ≈ 30 px, non dits à voix haute.
6. SH38 : le drapeau est assombri de 31 % par le voile du titre (132/26/30 au lieu de 193/39/45), choix esthétique.
7. Sous-titres non intégrés au MP4 (fichier SRT séparé) ; 0,12 s finale d'image sans audio (fin de générique).

## 3. Corrections réellement indispensables
Aucune. Les points 1–7 sont des améliorations facultatives.

## 4. Limites de l'inspection
- **Aucune écoute perceptive et aucun visionnage en temps réel** : je ne peux pas entendre l'audio ni regarder la vidéo en lecture. Les conclusions sonores reposent sur des mesures (LUFS, crêtes, rapports voix/fond, synchro par enveloppes), pas sur une écoute ; le naturel des bruitages, des voix et de l'émotion n'est pas évalué.
- Le visuel a été vérifié sur images fixes : 38 images de milieu de plan, 74 images de raccords, détails SH06/SH19/SH24/SH27/SH33/SH38, plus détection automatique (coupes, noirs, gels) — pas sur la totalité des 6903 images à l'œil.
- Rapport voix/fond calculé sur les stems de pré-mix, pas sur le mix final traité.
- Lisibilité et compréhension par les élèves : estimations, non testées en classe.

## 5. Verdict
**PRÊT POUR VALIDATION FINALE** — sous réserve d'un visionnage et d'une écoute intégrales par un humain, que cet audit ne remplace pas. Aucune déclaration FINAL n'est faite ici.

Planches : `docs/audit_qc3_son2/` (milieux de plans, raccords, détails).
