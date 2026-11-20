# SH37 — version C retenue : intégration (copie de travail) — rapport synthétique (20/11/2026)
**Limites d'abord.** Je n'ai rien écouté : tout ce qui suit est **mesuré**. Le projet REAPER n'a **pas été ouvert dans le vrai REAPER** (scripts vérifiés par syntaxe Lua et par une API REAPER simulée). Le rendu d'intégration doit être **écouté avant toute validation définitive**.
**Protection :** master FINAL (SHA-256 `0f72fc9a…c029d`), SCOLAIRE, `LE_CARNET_SOUND_V2.RPP`, `lib_carnet.lua` et tous les médias existants : **inchangés** (git : aucune différence). Fichiers **nouveaux uniquement** ; aucun rendu complet ; autres scènes non touchées ; 0 crédit, aucune génération.

## 1. Intégration préparée (copie de travail du projet v2)
Nouveaux fichiers dans `REAPER_V2/` : `LE_CARNET_SOUND_V2_SH37C.RPP` (copie du .RPP v2 + 2 pistes, 19 pistes, 18 items, dossiers équilibrés, 0 média manquant) · `media/SH37_plume_reelle_mixkit_2369.wav` (copie du média Mixkit) · `media/PH3_SH37_AMB_selectif_delta_pos267.00s.flac` · `manifest_sh37c/` · scripts `08` (ajoute/active), `09` (retour), `10` (diagnostic dans REAPER).
* **Piste « FOL SH37 — plume réelle »** : les 4 gestes de la version C choisie, niveau discret inchangé (tableau ci-dessous).
* **Piste « AMB SH37 — correction sélective »** : une couche *delta* qui, additionnée à la piste AMB d'origine, retire **seulement la bande > 2,1 kHz** de l'ambiance entre 267,45 et 270,50 s. La piste AMB d'origine (gain d'item, enveloppe) n'est pas touchée.
* **Retour immédiat** : `09_retour_version_precedente_SH37.lua` coupe les 5 items SH37 (le bruitage de synthèse d'origine revient tel quel) ; ou rouvrir `LE_CARNET_SOUND_V2.RPP`. `08` les réactive.
| Geste | Position | Vitesse | Gain d'item | Durée |
|---|---|---|---|---|
| 1 | 267,80 s | 1,00 | −16,1 dB | 0,600 s |
| 2 | 268,50 s | 0,97 | −18,1 dB | 0,619 s |
| 3 | 269,20 s | 1,04 | −17,1 dB | 0,577 s |
| 4 | 269,85 s | 0,99 | −20,1 dB | 0,606 s |
Niveau : RMS des parties actives −42 dBFS, crête −23,1 dBFS (≈ 23 dB sous la musique), énergie 4–8 kHz de la plume −71 dBFS. Fondus 20 ms/80 ms.

## 2. Correction plus sélective que −20 dB / −60 dB sur tout le bus
**Étude (mesures, contribution AMB à l'échelle du mix, dBFS) :**
| Bande | avant la plume (266,0–267,4 s) | **pendant (268,0–270,2 s)** | après : vent + cahier (270,8–273 s) |
|---|---|---|---|
| 30–150 Hz | −44,2 | −44,3 | −56,9 |
| 150–500 Hz | −39,9 | −40,3 | −41,7 |
| 500–1 000 Hz | −43,4 | −50,3 | −39,6 |
| 1–1,5 kHz | −48,4 | −57,9 | −39,6 |
| 1,5–2,1 kHz | −60,5 | −72,5 | −73,4 |
| **2,1–4 kHz** | −83,9 | **−36,2** | −85,0 |
| **4–8 kHz** | −83,8 | **−32,0** | −84,6 |
| 8–16 kHz | −90,4 | −66,6 | −89,0 |
**Conclusion :** le bruit de synthèse n'existe qu'entre **2,1 et 8 kHz** (+48 dB au-dessus du niveau de fond de ces bandes) ; le fond d'ambiance (ton de pièce, puis vent) vit sous 2,1 kHz et est **identique avant/pendant/après**. Une coupure limitée à la bande > 2,1 kHz retire donc le bruit sans toucher au fond.
**Réglage retenu :** séparation complémentaire (AMB = bas + haut, somme exacte) avec transition 1,8–2,1 kHz ; seul le « haut » est abaissé de −60 dB de 267,45 à 270,50 s (rampes cosinus de 0,2 s) ; la remontée finit à 270,50 s, l'instant où le vent démarre.
| Mesure (fenêtre 265–275 s) | A master | C approuvée (atténuation globale) | **C sélective** |
|---|---|---|---|
| Fond AMB 30–2 100 Hz modifié dans la zone (A : −38,4 dBFS) | — | **−38,4** (fond entièrement retiré) | **−104,3 (aucune modification)** |
| Écart maximal après 270,52 s (début du vent) | — | 0,031 (vent entamé) | **1·10⁻¹⁶ (intact)** |
| Énergie 4–8 kHz, 268,0 → 270,0 s (dBFS) | −31,4 / −33,7 / −32,1 / −29,6 / −37,8 | −47,4 / −49,8 / −46,3 / −47,9 / −48,3 | **identique à C approuvée** (plancher du fond) |

## 3. Raccords avant, pendant, après SH37 (mesurés)
* **Avant** : voix de Younes (Y5, fin à 267,19 s) et tout ce qui précède 267,40 s : **identiques au master** (écart ≤ 2·10⁻¹⁶). La correction commence à 267,45 s ; la 1re plume réelle à 267,80 s ; la musique MF entre à 268,0 s (inchangée).
* **Pendant** : l'écriture est visible en continu à l'image de 266,8 à 270,4 s (images vérifiées) ; les 4 gestes couvrent 267,80 → 270,46 s, séparés de 0,07 à 0,10 s.
* **Après** : le plan SH38 (drapeau, titre) arrive à **270,60 s** (mesuré par détection de coupe) ; la remontée du haut finit à 270,50 s, le vent (270,5 s) et le « cahier se referme » (270,7 s) sont **intacts**.
* **Pas de clic ajouté** : saut maximal d'échantillon local, master / C approuvée / **C sélective** — entrée (267,35–267,80) 0,0542 / 0,0545 / **0,0542** ; pendant (268,0–270,2) 0,1436 / 0,0670 / **0,0671** ; sortie (270,25–270,70) 0,0740 / 0,0499 / **0,0501** ; avant (266,0–267,3) et après (270,7–273,0) identiques.

## 4. Export de test 265–275 s (10,000 s = 250 images)
Fichiers (`audio/`) : **`SH37_C_selectif_265-275.wav`** (version à valider) · `SH37_comparatif_integration_265-275.wav` + `_INDEX.txt` (1 bip = master actuel, 2 bips = C approuvée, 3 bips = C sélective ; 1 s de silence entre versions) · `SH37_C_integration_projet_REAPER_simule_265-275.wav` et `SH37_AVANT_projet_REAPER_simule_265-275.wav` (simulation de ce que le projet REAPER doit produire).
| | A master | C approuvée | **C sélective** |
|---|---|---|---|
| Sonie intégrée / LRA | −15,6 LUFS / 4,0 | −15,6 / 3,8 | **−15,6 / 3,8** |
| Court terme max | −14,9 LUFS | −15,1 | **−15,1** |
| Crête vraie / échantillon | −2,9 dBTP / −2,89 dBFS | −2,9 / −2,89 | **−2,9 / −2,89** |
| Écrêtage | 0 | 0 | **0** |
| Perte en mono (zone) | −2,35 dB | −2,55 | **−2,56** |
| 30–2 100 Hz, zone (dBFS) | −19,7 | −19,7 | **−19,7** |
| 16 bits différents du master hors [267,40 ; 270,55] s | — | 9 187 (rampe jusqu'à 270,65 s) | **0** |
**Simulation du projet REAPER (avant → après intégration) :** couche delta RMS −35,0 dBFS, crête −16,3 dBFS ; écart AVANT/APRÈS hors zone **0,0** ; énergie 4–8 kHz 267→271 s : −43…−31 → −68…−50 dBFS ; bas 30–2 100 Hz modifié (hors plume) −106,7 dBFS ; crête après −3,49 dBFS, 0 écrêtage.

## 5. Ce qui n'a pas été vérifié
* **Écoute** : naturel et discrétion des 4 gestes, absence de « trou » dans l'ambiance, fluidité de la sortie vers SH38.
* **Vrai REAPER** : chargement du .RPP, lecture de la vitesse de geste (hauteur non préservée, comme dans mon test), exécution de `08`/`09`/`10`. Le script `10_verifier_SH37C.lua` écrit `diagnostic_SH37C.txt` : envoyez-le-moi.
* **Dépendance de la couche delta** : elle est calculée avec le gain (+16,49 dB) et l'enveloppe actuels de la piste AMB entre 267 et 271 s ; si vous les modifiez dans cet intervalle, la couche doit être recalculée (je le ferai).
* **Master FINAL** : non modifié ; l'inclusion de la version C dans une nouvelle copie du master est une décision séparée.

## 6. Appliquer sur votre PC
Dézippez `LE_CARNET_REAPER_V2_PATCH_SH37C.zip` **dans `Documents\`** (il fusionne avec `REAPER_V2\`, sans remplacer de fichier existant). Ouvrez `LE_CARNET_SOUND_V2_SH37C.RPP`, lancez `scripts\10_verifier_SH37C.lua` (diagnostic), puis écoutez 265–275 s. Pour revenir en arrière : `scripts\09_…lua` ou ouvrir `LE_CARNET_SOUND_V2.RPP`.
Scripts de calcul : `scripts/study_amb_bands.py`, `scripts/build_sh37_integration.py`, `scripts/build_reaper_sh37c.py` · mesures : `analysis/`.
