# Plan audio v1 (proposition, en attente d'autorisation) — rien généré

Durées des montages actuels : S1+S2 140,4 s · S3 68,9 s · S4 83,2 s · S5 77,0 s · S6 77,7 s → **≈ 447 s (7 min 27)** avant raccords. Film silencieux (pas de dialogue).

## Tarifs mesurés (Magnific, simulate_cost, exacts)
- Musique **Lyria 3 Pro** : 160 cr par morceau (30–180 s) · Lyria 3 : 80 cr (30 s) · ElevenLabs Music : 20 cr/s (2 400 pour 120 s) → **Lyria 3 Pro retenu**.
- Effets sonores et ambiances (ElevenLabs SFX) : ≈ 5 cr/s (40 cr pour 8 s ; 150 cr pour 30 s en boucle).

## Musique (5 morceaux, original, licence commerciale ; aucun chant existant)
| Morceau | Sert | Contenu | Coût |
|---|---|---|---|
| M1 Thème de Yassine | S1, S2, reprise S6 | oud solo, notes rares, intime, lent | 160 |
| M2 Bourdon / grenier | S2, S6 | bourdon grave très bas, cordes frottées | 160 |
| M3 Textures de sable | S3 | cordes en harmoniques, voix lointaine sans paroles, granulaire | 160 |
| M4 Thème principal 1975 | S4 (+ S5 début) | cordes, oud, bendir, montée ample | 160 |
| M5 Thème de transmission | S5 fin, S6 | oud + violoncelle, résolution, dernière note tenue | 160 |
Marge : 2 régénérations par morceau si besoin ≈ +1 600.

## Ambiances (boucles) et effets (à partir des fiches de repérage S1-S6)
- Ambiances ≈ 10 : médina lointaine + oiseaux, patio + fontaine, grenier (vent léger, craquements), désert (vent), foule immense générique **inintelligible**, tissu de drapeaux, pas sur le sable… ≈ 10 × 100 = 1 000.
- Effets ponctuels ≈ 45 (pas sur zellige, perles de bois, craquement de marche, grincement de porte, glissement de boîte, couvercle métallique ouvert/fermé, froissement du drapeau, crissement du sable, grain qui tombe, souffle…) ≈ 45 × 35 = 1 600.
- Appel à la prière très lointain (validé « oui » par le réalisateur) : généré, inintelligible, mixé à très bas niveau ; **retiré si le rendu sonne caricatural ou irrespectueux**.

## Total estimé : ≈ 3 400 (+ marge) → **plafond proposé 5 000** (solde actuel 22 275).

## Méthode de mixage (gratuit, local)
- Pistes : ambiance / effets / musique, niveaux (musique −18 dB sous effets), silences exacts (S2-08, S5-05/07, S6-08), fondus croisés aux raccords.
- Script `film_mix` (ffmpeg adelay/amix/afade) lisant un JSON de repères (temps, fichier, gain) ; rendu versionné `12_EDITING/AUDIO/`, sources jamais modifiées ; mixage sur copies du montage vidéo muet (`FILM_*_cut_*.mp4`).
- Contrôle : niveaux (LUFS cible −16), absence de clipping, synchronisation aux images repères.

## Ordre d'exécution
1. M1 + ambiances S1-S2 + effets S1-S2 → mixage S1-S2 → validation.
2. S3 (M3 + effets) → S4 (M4 + foule) → S5 (M5 + silence) → S6 (reprises M1/M5 + couvercle) → validation séquence par séquence.
3. Assemblage final des pistes sur le film complet.
