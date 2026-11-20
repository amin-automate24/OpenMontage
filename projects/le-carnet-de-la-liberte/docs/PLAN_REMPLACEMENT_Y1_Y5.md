# Plan concret de remplacement de Y1–Y5 (voix de Younes) — 17/11/2026

Statut : préparé, rien exécuté, aucune dépense. Voix de repère (espeak) conservées dans M4.1 jusqu'à validation.

## A. Réalisation (priorité 1 : interprète humain)
- Candidat : enfant de 9–12 ans de l'équipe/entourage ou jeune comédien. **Avant toute prise** : consentement écrit d'un parent (usage de la voix dans le film pédagogique, durée, diffusion, droit de retrait), cession limitée au projet, rémunération/gratuité écrite. Aucun clonage ni entraînement IA.
- Audition 5 min : Y3 + Y1 (2 prises chacune). Séance retenue : 323 caractères au total, 3 prises par réplique, ≈ 20 min avec pauses (kit : `audio/recording_younes/`).
- Délai réaliste : audition mercredi 18/11, séance jeudi 19/11 matin, intégration l'après-midi, livraison vendredi 20/11. Si l'audition échoue mercredi, passer au repli B dès jeudi.

## B. Replis réalistes, par ordre (chacun nécessite votre accord)
1. **Adulte au timbre jeune + pitch/formant léger, local, gratuit** : une voix de l'équipe (idéalement jeune, aiguë) enregistrée selon le même kit, puis transposée de +2 à +3 demi-tons avec formants préservés (FFmpeg `rubberband`, disponible ici). Compromis créatif : à valider à l'écoute, limite ≈ +3 demi-tons sinon voix artificielle.
2. **Voix ElevenLabs la plus jeune du casting FR existant** (Gaspard Chevallier, « jeune, posé, curieux », déjà repérée, non cloné) : 323 caractères pour 1 prise de Y1–Y5, soit 0,8 % du quota restant ; **aucun Voice Design** (bloqué, non relancé). Accord + plafond écrits requis ; rendu « jeune adulte », pas enfant.
3. **Dernier recours** : livrer avec la mention « voix provisoire » : à éviter pour un film destiné à des élèves.

## C. Intégration immédiate (dès que les WAV arrivent)
1. Déposer les prises dans `audio/recording_younes/prises/` (`Y1_t1.wav`…).
2. Contrôle automatique, sans écriture : `python3 scripts/integrate_younes_voices.py --pick Y1=t1,Y2=t2,Y3=t1,Y4=t3,Y5=t1` (durée vs fenêtre, crêtes, bruit de pièce, écrêtage). Le test à blanc sur prises synthétiques a fonctionné.
3. Si tout est OK : même commande avec `--apply` -> copies 48 kHz mono 24 bits dans `retenues/` (passe-haut 80 Hz uniquement, aucun changement de niveau, aucun écrasement).
4. Après votre validation, copie manuelle vers `audio/voices_final/<CLÉ>.wav` (priorité sur toute voix de repère) puis mix versionné M5 : `assemble_audio_versioned.py M5 …` (mêmes options que M4.1 + `--rhythm` pour Y1/Y4 si nécessaire : Y1 début 11,6 s, Y4 début 253,6 s, T5 à 262,1 s).
5. Équilibrage Fairlight des dialogues (écart ≤ 2 dB entre personnages) ; −16 LUFS réservé au mix final.
6. Contrôle visuel/sonore des 5 plans (SH03, SH05, SH09, SH36, SH37) sur aperçu M5 NON FINAL.
