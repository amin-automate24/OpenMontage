# Diagnostic du grésillement à 268 s — résultats (20/11/2026)
**Distinction :** tout ce qui suit est **mesuré** (aucune écoute de ma part). Ce que vous entendez (désagrément, « télé sans signal ») est une perception humaine que je ne peux pas confirmer ni infirmer ; les mesures montrent seulement ce qui existe dans le signal et d'où cela vient.
**Limite importante :** votre `TEST_COURT_C_268-299.wav` exporté par REAPER **n'est pas dans cette session** (le fichier de ce nom présent dans mon dossier temporaire est une copie de ma v2, utilisée pour tester le script de contrôle). J'ai donc mesuré la **lecture simulée du projet REAPER v2** (mêmes médias, mêmes gains d'items, mêmes enveloppes, mêmes fondus), pas votre export réel.

## 1. Les secondes 268–273 : master original contre reconstruction
Énergie aiguë (6–16 kHz), RMS par seconde (dBFS) :
| s | master FINAL | mix sans perte | **somme REAPER simulée** | bus AMB | bus MUS | bus DX |
|---|---|---|---|---|---|---|
| 267 | −49,1 | −48,9 | −55,3 | −100,6 | silence | −55,3 (fin de Y5) |
| **268** | **−34,2** | −34,1 | **−42,4** | −42,4 | −64,7 | silence |
| **269** | **−32,0** | −31,9 | **−33,5** | −33,6 | −62,0 | silence |
| 270 | −45,9 | −45,8 | −45,2 | −45,4 | −58,3 | silence |
| 271 | −54,9 | −54,7 | −56,8 | −91,5 | −56,8 | silence |
| 272 | −64,4 | −64,5 | −65,1 | −89,1 | −65,1 | silence |
Par 0,25 s au-dessus de 4 kHz, le master passe de −64,7 dBFS (267,75 s) à **−30,1 dBFS dès 268,00 s**, reste entre **−26 et −33 dBFS jusqu'à ≈ 270,25 s**, puis retombe sous −38 puis −48 dBFS : **un événement aigu de 2,6 s qui commence exactement à 268,0 s**, comme votre écoute.

## 2. Déjà présent dans la référence ou introduit par la reconstruction ?
**Déjà présent dans le master original** (et à l'identique dans le mix sans perte QC2_SON2, écart ≤ 0,3 dB). La reconstruction REAPER **le reproduit** avec des niveaux voisins (−42/−33,5 contre −34/−32 dBFS) ; elle ne l'ajoute pas.
Signature mesurée de l'événement (4–20 kHz) : pic à 5 713 Hz, centroïde 6 000 Hz, kurtosis 5,8 (un bruit gaussien donne 3 ; un bruit en impulsions donne davantage) : c'est du **bruit en rafales**, pas une note de musique.

## 3. Bus par bus (268–278 s)
| Bus | Contribution mesurée |
|---|---|
| **AMB** (ambiance+foley M7c) | **seule source du bruit aigu** : HF −42,4 / −33,6 / −45,4 dBFS à 268/269/270 s ; la source brute présente la même rafale entre 268,0 et 270,3 s |
| MUS (MF + générique v2) | propre : HF −65…−57 dBFS, planéité spectrale 0,15 (tonale, non bruitée) ; le générique v2 (273–299 s) : HF −62…−77 dBFS |
| DX | silence de 268 à 278 s (−240 dBFS) |
| FOL | pistes tests A/B muettes : aucune contribution |
| AUX | aucune entrée : les envois partent de DX (silence) et de FOL (muet) |
**Origine dans les fichiers de conception :** `scripts/sound_design_m4.py`, ligne 122 : `put(pen(2.6), 267.7, -40, …, "Younes écrit dans son cahier (SH37, écrit — non dit)")` — **bruitage de synthèse « plume »**, durée 2,6 s à 267,7 s, présent à l'identique dans les versions M4, M6, M7, M7c (même profil HF) ; la version M5 utilisait un enregistrement réel (Mixkit), très différent (kurtosis 25, énergie aiguë bien plus faible).

## 4. Effets, gains, automations, envois, superpositions (dans le projet v2)
* Items actifs entre 268 et 278 s : DX (silence), **AMB** (volume d'item +16,49 dB, enveloppe de 0,25 à 0,92), **MUS** : MF (−0,66 dB) et générique v2 (0 dB) qui **se superposent volontairement** de 273 à 276 s (fondu enchaîné, sans bruit : HF −62…−77 dBFS).
* Aucun traitement actif : EQ et compresseurs sont **désactivés**, ReaVerbate (AUX) n'a pas d'entrée, ReaLimit au MASTER ne fait que limiter la crête.
* **Pas de défaut d'automation ni de superposition de médias** : la sommation reproduit le master à ±8 dB près en HF à 268 s (plus bas, jamais plus haut) et à ±2 dB ensuite.
* Si votre export réel est plus bruyant que cette simulation, il y aurait une différence propre à REAPER que je ne peux pas voir d'ici (par exemple une enveloppe non appliquée, un plugin actif non prévu) : voir § 7.

## 5. Correction minimale (copie de travail ; master FINAL et projet d'origine non modifiés)
**Un seul geste :** creux de **−20 dB** sur l'**enveloppe de volume de la piste AMB**, entre **267,45 et 270,65 s** (rampes cosinus 0,2 s puis 0,3 s). Ni filtre, ni réduction de bruit générale, ni modification de DX ou MUS. Elle est portée par `manifest/envelopes_correction_268.csv` et le script `scripts/06_correction_plume_268.lua` (ne réécrit que l'enveloppe AMB ; retour arrière = relancer `01_…lua`).
Effet **mesuré** (énergie >4 kHz par 0,5 s à partir de 268,0 s) :
| | 268,0 | 268,5 | 269,0 | 269,5 | 270,0 | 270,5 |
|---|---|---|---|---|---|---|
| master | −31,6 | −33,9 | −32,4 | −29,8 | −38,1 | −50,6 |
| AVANT (projet simulé) | −43,0 | −35,5 | −32,7 | −30,9 | −37,9 | −50,7 |
| **APRÈS** | **−62,6** | **−52,0** | **−49,3** | **−49,8** | **−51,7** | −50,7 |
Hors de la zone 267,4–270,7 s, **APRÈS − AVANT = 0,0** (écart maximal) ; RMS 268–273 s : −19,3 → −19,4 dBFS ; crête −3,49 dBFS, 0 écrêtage ; perte mono −3,4 → −3,5 dB (la musique domine, inchangée).
**Prix à payer (à écouter) :** le bruitage de plume de SH37 est quasi supprimé pendant ces 2,8 s ; Younes « écrit — non dit », ce n'est pas un son narratif essentiel, mais c'est un choix artistique qui vous revient. Alternative sans le perdre : remplacer par l'enregistrement réel (Mixkit 2369, déjà dans le projet), à bas niveau : non appliqué.

## 6. Fichiers comparatifs 268–278 s (250 images, exportés depuis la copie de travail)
`audio/268-278_MASTER_original.wav` · `268-278_AVANT_projet_REAPER_simule.wav` · `268-278_APRES_correction_plume.wav` · `268-278_AB_master_avant_apres.wav` (master, 1 s de silence, AVANT, 1 s de silence, APRÈS). À écouter : le crépitement est-il celui entendu ? Est-il atténué à votre goût ?

## 7. Ce qui reste à confirmer, et par qui
1. **Confirmation par vous** : les 2 premières secondes de `268-278_MASTER_original.wav` contiennent-elles bien ce crépitement ? Si oui, il fait partie du master actuel, pas de la reconstruction. Si vous ne l'entendiez pas dans le master, dites-le-moi : cela signalerait une différence propre à votre export REAPER.
2. **Votre export réel** : exécutez `scripts\07_mesure_hf.py exports\TEST_COURT_C_268-299.wav` (ou envoyez-moi le fichier) : attendu autour de −35/−30 dBFS en 268–270,5 s si c'est la même rafale ; nettement plus haut ou plus long = autre cause.
3. **Même défaut ailleurs (mesuré, non corrigé)** : le même générateur de plume de synthèse produit des rafales aiguës dans le master à 109,6–114,6 s (SH19 : −29,9 dBFS pendant, contre −43,7 avant), 146,3–149,9 s (SH24 : −27,8 contre −32,7) et 267,7–270,3 s (−32,6 contre −35,7). Ce sont des candidats à vérifier à l'écoute ; je n'y ai pas touché.
4. **Master FINAL** : inchangé (SHA-256 `0f72fc9a…c029d`). Si le crépitement est confirmé et que vous voulez le corriger dans le master, ce sera une décision séparée (nouvelle copie, pas d'écrasement).
