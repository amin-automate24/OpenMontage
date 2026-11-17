# Plan musical minimal — base M6.1 (préparation seulement, 17/11/2026)

M6.1 reste le master candidat **sans musique** (NON FINAL) et sert de repli ; il n'est pas modifié. Aucune piste n'est téléchargée ni générée.

## Où la musique apporte réellement de l'émotion (≈ 82 s, 30 % du film)
| Repère | Plans | In → Out | Rôle | Gain bus |
|---|---|---|---|---|
| MA | SH10–12 | 0:50.5 → 1:06 | Exposition du thème du carnet (ouverture, pages, encre) | −23 |
| MB | SH19–20 | 1:49 → 2:01 | Amina écrit son espoir, pages vers 1953 (solo chaud) | −24 |
| MC | SH25–26 | 2:31.5 → 2:58 | Retour de la lumière ; V1 sous la musique | −24 |
| MD | SH27–28 | 2:55 → 3:09.5 | Joie populaire ; A5 sous la musique | −26 |
| ME | SH34 | 4:04.8 → 4:10 | Le carnet se referme (après A8) | −25 |
| MF | SH38 | 4:28 → 4:36 | Résolution du thème sur le drapeau et le titre, fin tenue | −22 |
**Aucune musique** : SH01–09 (classe, Y3/M1), SH13–18 (rue 1944, père), **SH22** (radio), SH23, **SH29–33** (cartons historiques, A6/P5/A7, ligne du temps), SH35–37 (Younes). Détails et recouvrements : `audio/music_plan/cues_music_minimal.json`.

## Paramètres de mixage
- Bus musique séparé, niveau ≈ 8 LU sous les dialogues ; ducking −9 dB (attaque 250 ms, relâche 600 ms) sur le bus dialogues ; coupe-bas 90 Hz, creux −2 dB à 2–3 kHz ; vérifier le repli mono.
- Musique mixée **avant** la chaîne de finition (`scripts/finish_master_audio.py` : −16 LUFS, −1 dBTP) ; contrôle de non-régression : voix intelligibles, aucune musique sur SH22 et SH33.

## Source possible et coût
1. **Piste gratuite avec licence vérifiable (recommandée) — 0 €.** Banque à licence commerciale sans attribution (par ex. Mixkit : « Mixkit License », déjà prise en charge par l'outil de recherche du projet) ou domaine public/CC0. Condition : le fichier et la page de licence sont archivés dans `approvals/licenses/` au moment du téléchargement. Nécessite votre autorisation de télécharger 1 à 2 pistes (non fait) ; je ne peux pas garantir à l'avance qu'une piste convienne (oud/cordes douces, thème mémorisable).
2. **Génération IA via Magnific (simulation de coût, exacte, rien lancé)** : Lyria 3, 30 s fixes = **80 crédits** (suffit pour un motif répété en boucle et variations) ; Lyria 3 Pro = 160 crédits ; ElevenLabs Music 60 s = 1 200 crédits (écarté). Licence d'usage = conditions de votre plan Magnific, non vérifiables par mes outils. Les crédits restent loin de la réserve de 4 643 pour THE LAST OF MEN.
3. **Repli** : aucune musique (M6.1 tel quel).

## Décisions nécessaires
- Choisir : (1) téléchargement gratuit avec archivage de licence, (2) Lyria 3 à 80 crédits, ou (3) rester sans musique.
- Valider les 6 repères ci-dessus (ou en retirer, par exemple ME).
