# Refonte sonore CINÉMA — projet REAPER v2 et générique v2 (rapport technique, 20/11/2026)
**Aucune écoute de ma part** (je n'entends pas l'audio) : tout ce qui suit est **mesuré** ; l'appréciation artistique vous revient. 0 crédit dépensé, aucune génération IA, aucune vidéo produite, aucune publication. Master FINAL intact (SHA-256 `0f72fc9a…c029d` revérifié). Fichiers précédents (tests A/B/C v1, paquet de la phase 2) conservés à l'identique.

## 1. Connexion à REAPER : choix et raison
| Option | Constat | Retenue |
|---|---|---|
| A. Claude Code sous Windows, accès direct aux fichiers REAPER | Cette session tourne dans un **conteneur Linux du cloud** ; aucun ordinateur n'est attaché (`list_computer_folders` : aucun dossier). Possible plus tard en lançant Claude Code **sur votre PC** (application de bureau ou terminal), sans installation de serveur tiers. | non (ici) |
| B. Connexion distante | Aucun accès entrant vers votre PC ; je n'installe aucun serveur MCP tiers non vérifié et ne demande aucun jeton. | non |
| **C. Projet portable + ReaScripts Lua + contrôle FFmpeg** | Aucune installation supplémentaire sur votre PC (REAPER + plugins fournis avec REAPER ; FFmpeg/Python facultatifs pour le contrôle). | **oui** |

## 2. Générique 276–299 s : nouvelle proposition
**Cause du niveau trop faible de la v1** : j'avais pris l'introduction très douce de la piste (−33 dBFS RMS) avec −24,5 dB supplémentaires, soit −47 à −56 dBFS, alors que MF dans le film est à ≈ −17 dBFS RMS. Une première tentative de v2 (fin d'éditeur de la piste, décroissance de 18 dB/s) a été rejetée avant livraison.
**v2 retenue** : Mixkit 599, **corps de la piste** (offset 118,7 → 144,7 s ; la décroissance d'éditeur commence à 144,8 s, mesuré), entrée à **273,0 s en fondu enchaîné** avec la queue de MF (qui s'éteint de 273 à 276 s), plateau sur les cartons 1–2, **descente lente et continue** sur le carton 3 jusqu'à 299,0 s ; gain statique (dynamiques internes de la musique conservées) × enveloppe lente ; stéréo 60 % à sonie conservée. **v2b** : même musique, « respiration » d'environ 1 s avant l'entrée à 275,0 s.

| Mesure (fenêtre 268–299 s) | AVANT | v1 | **v2** | v2b |
|---|---|---|---|---|
| Court terme carton 1 (277–282 s), LUFS min/max | silence | −67,2 / −36,0 | **−25,2 / −19,4** | −32,3 / −20,0 |
| Carton 2 (282–285,5 s) | silence | −54,7 / −50,6 | **−20,1 / −18,5** | −20,1 / −18,5 |
| Carton 3 (285,5–295 s) | silence | −57,1 / −41,9 | **−23,7 / −18,4** | −23,7 / −18,4 |
| 296–298 s, min | silence | −56,9 | **−30,7** (descente finale) | −30,8 |
| Couche ajoutée, RMS 277–295 s | — | −49,1 dBFS | **−22,3 dBFS** | −22,6 dBFS |
| Perte en mono de la couche | — | −1,75 dB | **−1,35 dB** | −1,33 dB |
| Silences < −60 dBFS | 275,7–298,9 s | 275,7–298,9 s (morcelés) | **298,6–298,9 s seulement (fin du fondu)** | idem |
| Crête vraie / écrêtage | −3,1 dBTP / 0 | −3,1 / 0 | **−3,1 dBTP / 0** | −3,1 / 0 |
| Plus grand saut RMS après 276 s | — | 15,7 dB/s | **9,2 dB/s** (dernière seconde, à −36→−46 dBFS) | 9,2 |
| Identique à l'AVANT avant 272,9 s | — | oui | **oui** | oui |
Repère : les dialogues du film sont vers −16/−17 LUFS court terme ; MF monte à −15 LUFS. Le plateau v2 (−18,5 à −20 LUFS) est donc nettement audible, un peu sous la parole ; le niveau se règle d'un seul paramètre (`PLATEAU_DB`) si l'écoute le juge trop présent.
**À écouter (non mesurable)** : naturel du fondu enchaîné MF → v2 (deux passages de la même œuvre se superposent ~2 s) ; préférence v2 / v2b ; émotion de la reprise ; fin de la descente.

## 3. Projet REAPER v2 (`REAPER_V2/`, 91 Mo de médias)
* **Structure** : MIX BUS ⊃ DX (stem des voix originales), AMB (ambiance+foley M7c, source mélangée), FOL (tests A et B, **muets par défaut**), MUS (thème 599 en 4 repères + générique v2 ; v2b muet), AUX (réverbérations intérieur/extérieur, ReaVerbate) ; REF muettes (mix actuel sans perte, master FINAL) ; MASTER avec ReaLimit (−1 dB, réglé par nom de paramètre) et vumètre JS de sonie. 48 kHz, stéréo, 76 marqueurs/régions (plans, répliques, cartons, coupes mesurées, régions des tests).
* **Non destructif** : volumes d'items, fondus, enveloppes de volume (5 580 points : gain par réplique DX ; gain par plan + ducking −9/−12 dB AMB et MUS), envois ; EQ/compresseurs ajoutés **désactivés** (à régler à l'écoute) ; aucun plugin payant.
* **Reconstruction calibrée** contre le mix final (moindres carrés par blocs de 4 s) : écart **−6,5 dB** (de −5,7 à −8,1 dB selon les sections) → **base de travail fidèle à ~80 % en amplitude, pas une copie** (le mix final assemble plusieurs versions et passe par une compression/limitation non reconstituées). Gains musicaux trouvés : MA ×1,21, MB ×0,85, MC/MD ×0,46, MF ×0,93.
* **Simulation de la somme du projet** (sans plugins) : 299,000 s ; −17,2 LUFS ; **crête +2,3 dBFS / +0,1 dBTP avant limiteur** → le limiteur MASTER est **indispensable** (prévu à −1 dB) ; perte mono −0,78 dB ; aucun silence > 0,5 s ; synchronisation avec le master : décalage 1–11 échantillons (< 0,25 ms) et corrélation 0,83–0,90 (écarts dus à la reconstruction, pas au placement) ; dialogues : écart médian −0,9 dB vs master (max 2,7 dB), étendue 4,6 dB contre 3,2 dB (la compression d'origine n'est pas reproduite).
* **Vérifications faites ici** : structure du .RPP (42 blocs ouverts/fermés, profondeur de dossiers équilibrée, 9 médias référencés présents) ; syntaxe Lua 5.4 des 4 scripts ; exécution des scripts avec une **API REAPER simulée** (17 pistes, 12 items, 5 580 points ≤ +6 dB, 76 marqueurs, 9 traitements, 3 envois, seconde exécution sans doublon, limiteur réglé à −1,1 dB). **Non vérifié : le comportement dans le vrai REAPER.**

## 4. Tests A et B dans le projet
Intégrés comme pistes **FOL test A** (froissement à 36,20 s, air d'encre 60,7–65,9 s) et **FOL test B** (oiseau à 164,10 s), **muettes** en attendant votre décision, avec envois vers les réverbérations. Non intégrés automatiquement : le +1,5 dB des répliques V1/A5 (test B) et la réduction de largeur des fonds (SH10–12, SH27), car ils modifient l'équilibre existant : à faire dans REAPER par enveloppe de volume DX et enveloppe de largeur (*width*) sur AMB si vous les retenez. Les ajustements « présence du carnet » et « profondeur des ambiances » sont préparés (pistes FOL, envois AUX, EQ désactivés) mais **non réglés**, car leur dosage dépend de l'écoute.

## 5. Décisions attendues
1. Générique : **v2**, **v2b** ou ajustement du plateau (plus bas / plus haut) ?
2. Test A et test B : activer, ajuster ou abandonner ?
3. Après ouverture réelle dans REAPER : messages d'erreur éventuels (je corrige), puis feu vert pour le mixage complet des 299 s.
