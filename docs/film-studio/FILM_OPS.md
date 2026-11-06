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
