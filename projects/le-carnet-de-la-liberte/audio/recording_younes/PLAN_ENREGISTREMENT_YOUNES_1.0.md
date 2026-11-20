# Enregistrement humain — Younes (LE CARNET DE LA LIBERTÉ)

Statut : **PRÉPARÉ, non exécuté**. Aucune dépense. Scénario inchangé (textes identiques à `elevenlabs_script_multilingual_v2.json`).

## 1. Texte regroupé et durées
| Clé | Plan | Réplique | Fenêtre dispo | Car./s |
|---|---|---|---|---|
| Y1 | SH03 | Parce que le Maroc est devenu indépendant ! | 3.2 s (11.8→15.0 s) | 13.4 |
| Y2 | SH05 | Je... je ne connais pas toute l'histoire. | 6.7 s (20.8→27.5 s) | 5.8 |
| Y3 | SH09 | Maman ! À qui appartient ce carnet ? | 10.7 s (39.8→50.5 s) | 3.4 |
| Y4 | SH36 | Que l'indépendance est le résultat de longues années de lutte et de sacrifices. Et que nous devons en être dignes ! | 7.8 s (253.7→261.5 s) | 14.7 |
| Y5 | SH37 | En étudiant, en respectant les autres et en construisant ensemble l'avenir de notre pays ! | 7.6 s (262.9→270.5 s) | 11.8 |

Lecture : Y4 (≈14,7 car./s) est serrée pour un enfant ; la dire naturellement, quitte à garder une version un peu plus lente pour permettre un léger recalage en montage (pas de raccourcissement du texte). Y1 (≈13,4 car./s) aussi.

## 2. Consignes de jeu
- **Y1** : Fier, spontané, un peu vif : il répond tout de suite, sûr de lui.
- **Y2** : Hésitant, honnête, voix qui baisse : il avoue ne pas tout savoir. Les « Je... je » se disent vraiment, sans théâtre.
- **Y3** : Curieux, surpris, légèrement essoufflé : il vient de trouver le carnet et appelle sa mère. Pas de cri.
- **Y4** : Posé, sérieux, plus mûr : il a compris. Deux phrases, respirer au point. Ni solennel ni récité.
- **Y5** : Sincère, énergique, tourné vers l'avenir : il énumère trois idées, légère montée sur « construisant ».
- Général : voix d'enfant naturelle, parler comme à la maison, pas de voix « de dessin animé », pas d'accent forcé, pas d'imitation. Lire une fois à blanc, puis 3 prises par réplique (dont une un peu plus lente).

## 3. Procédure d'enregistrement WAV 48 kHz
1. Pièce calme et sourde (rideaux, coussins) ; couper ventilation, notifications, appareils bruyants.
2. Téléphone ou micro à ~20 cm, légèrement de côté (anti-plosives), jamais face à la bouche ; filtre anti-pop si possible.
3. Application d'enregistrement en **WAV 48 kHz, 24 bits (ou 16), mono**, sans réduction de bruit ni compression automatique. Si seul le M4A est possible : prendre la meilleure qualité, conversion locale ensuite.
4. Silence de 5 s en début de fichier (bruit de pièce), puis les répliques ; 1 s de silence entre chaque prise ; claquer un clap ou dire « prise 1, Y3 » au début de chaque prise.
5. Niveau d'entrée : crêtes vers −12 dBFS, jamais d'écrêtage ; ne pas toucher au gain en cours de session.
6. Nommage : `Y1_t1.wav`, `Y1_t2.wav`… ; dépôt dans `audio/recording_younes/prises/` (originaux jamais modifiés).
7. Traitement local (sans IA) : coupe, éventuel filtre passe-haut 80 Hz, égalisation du niveau dialogues (cf. plan Fairlight) ; version retenue copiée vers `audio/voices_final/<CLÉ>.wav`, lue par `assemble_audio.py`.

## 4. Audition courte (≈ 5 min)
- Candidats : une voix de l'équipe ou un jeune comédien de 9–12 ans, francophone, naturel.
- Texte d'audition : Y3 (« Maman ! À qui appartient ce carnet ? ») et Y1 (« Parce que le Maroc est devenu indépendant ! »), 2 prises chacune ; ajouter Y5 si le temps le permet.
- Critères : timbre enfantin naturel, curiosité, spontanéité, articulation, tient dans la fenêtre, constance entre prises ; comparaison avec le test refusé (Y3 Jules).
- Autorisations **obligatoires avant tout enregistrement** (mineur) : consentement écrit d'un parent/tuteur (enregistrement, usage de la voix dans le film pédagogique, durée, diffusion prévue, droit de retrait) ; cession/licence de la voix pour ce projet uniquement ; rémunération ou gratuité convenue par écrit ; aucune utilisation pour clonage ou entraînement IA sans accord séparé. Modèle de formulaire à rédiger/faire valider avant l'audition ; rien n'est signé ni envoyé.

## 5. Intégration
Voix de Younes humaine ; autres personnages restent sur le casting ElevenLabs Multilingual v2 (aucune génération sans accord), Amina adulte : Julia (A7 provisoire déjà convertie en `voices_final/A7.wav`, 48 kHz).
