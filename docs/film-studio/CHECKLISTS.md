# Checklists de production (film_ops)
## Avant toute génération payante
1. `film_ops guard <plan> <image|video> --est <crédits>` doit répondre OK (plan non déjà validé, budget suffisant, élément approuvé dans QUEUE.csv).
2. Prompt et références repris de 06_VIDEO_PROMPTS*.md ; image de départ au cadrage voulu.
3. Autorisation du réalisateur (explicite ou plafond groupé) dans DECISIONS_LOG.md.
## Après chaque génération
1. Regarder le résultat (vidéo : 16 images) et noter identité, décor, mouvement, texte, artefacts.
2. `film_ops ledger add ...` puis `film_ops shot set ...` ; `film_ops check` ; `film_ops status --write`.
3. `film_ops sync "message"` (commit + push). Planche : `film_ops contact-sheet`.
4. Journal : une entrée courte dans production_log.md.
## Fin de séquence
Rapport unique : plans validés, crédits, problèmes, décisions en attente.
