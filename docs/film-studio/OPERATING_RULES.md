# Règles d'exploitation (contexte, appels MCP, erreurs)
- **Contexte :** ne pas relire les fichiers déjà lus ; lire PROJECT_CONTEXT.md + PRODUCTION_STATUS_AUTO.md au début d'une session. Les résultats `midjourney_get_task` sont volumineux : un seul appel une fois la tâche terminée (attendre, ne pas boucler). `creations_wait` côté Magnific attend lui-même.
- **Appels MCP :** Midjourney lancé avec `split_images` désactivé + `images_split_grid` Magnific (gratuit) revient moins cher que 4 imports. Vérifier le solde réel (`account_balance`, gratuit) seulement avant un lot, pas à chaque plan.
- **Erreurs connues :** Kling 3.0 Omni élargit le cadrage ; jets d'eau et décor dérivent sans « locked-off, architecture identique » ; identité du grand-père fiable seulement en plan large ; les CDN d'images sont bloqués (importer via Magnific) ; `creations_read` n'accepte que hq low/medium.
- **Pas de boucle de reprise :** une vidéo qui échoue deux fois s'arrête et remonte au réalisateur.
- **Fichiers :** jamais d'écrasement ; versions numérotées ; images et vidéos hors git (sauvegarde externe sur autorisation).
