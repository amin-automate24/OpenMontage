# film_ops — automatisation sûre d'un projet de film
Script : `scripts/film_ops.py` (tests : `tests/tools/test_film_ops.py`). N'écrase jamais : nouveaux fichiers en `_v2`, `_v3`; les CSV modifiés sont sauvegardés avant dans `<projet>/_backups/<date>/`.
- `contact-sheet OUT.jpg IMG... --cols 2` : planche numérotée.
- `ledger add --tool Magnific --credits 855 --item "..." [--balance N]` : ligne de BUDGET.csv avec solde chaîné ; `ledger show`.
- `shot set S1-02 --status VALIDE --video ID --cost N` : met à jour SHOT_LIST.csv.
- `status` : synthèse en lecture seule (plans, crédits, décisions en attente).
- `backup FILE...` ; `sync "message"` : commit + push (reprises 2/4/8/16 s) avec attribution.
Complète `film_studio.py` (non modifié).

## film_edit (montage par liste de décisions)
`scripts/film_edit.py plan|render EDL.json` : rend un montage à partir d'une EDL JSON (clip, in, out, transition cut/dissolve + durée), toujours en copie versionnée (`_v2`...), sources en lecture seule. Les EDL du projet sont dans `12_EDITING/`.

## film_mix (mixage audio)
`python3 scripts/film_mix.py plan|render MIX.json` : mixage pilote par un JSON de repères (pistes, début, durée, boucle, niveau `lufs`/`gain_db`, fondus). Sources en lecture seule ; sorties versionnées dans `12_EDITING/AUDIO/` (WAV + MP4 si `video`). Voir l'en-tête du script pour le format. Exemple : `films/LE_SECRET_BOITE_FER_BLANC/11_AUDIO/MIX_S1-S2_v2.json`.

## film_motion (calage son/geste)
`python3 scripts/film_motion.py env VIDEO T0 T1 [--roi x0,y0,x1,y1]` : profil de mouvement d'un plan. `gate SFX VIDEO T0 T1 OUT.wav [--roi ...] [--floor] [--power]` : produit un effet sonore MODULÉ par le mouvement réel (muet quand rien ne bouge) : synchronisation par construction pour pas, mains, portes, glissements. `film_mix` applique désormais un GAIN STATIQUE mesuré (pas de loudnorm dynamique qui écrase les nuances) + limiteur de crête.

Note film_mix (nov. 2026) : les pistes sont pré-rendues (découpe, boucle `-stream_loop`, lissage `smooth`) puis normalisées par GAIN STATIQUE mesuré (`lufs`, option `norm_whole` pour découper une musique sans aplatir son crescendo). Les mixages S1-S2 (v5) et S3 (v1), validés, ont été rendus avec la version précédente (loudnorm par piste) : ne pas les régénérer sans nouvelle validation. Attention : la mesure LUFS sous-estime les ambiances graves (vent, foule) ; à niveau LUFS égal elles « pèsent » davantage : les régler plus bas que la musique (≈ −55/−63 LUFS contre −35).
