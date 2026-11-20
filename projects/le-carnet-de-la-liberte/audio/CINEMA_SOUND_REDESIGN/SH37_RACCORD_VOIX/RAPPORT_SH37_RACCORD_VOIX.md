# SH37 — raccord voix / ambiance : diagnostic et correction (20/11/2026)
**Mesuré ≠ entendu.** Je n'ai rien écouté ; tout ce qui suit est mesuré. Votre écoute a raison : le grésillement persistait dans `SH37_C_selectif_265-275.wav`, et les mesures montrent pourquoi. Masters, SCOLAIRE, projet v2 : inchangés (SHA-256 `0f72fc9a…c029d`) ; fichiers nouveaux uniquement ; pas de rendu complet ; 0 crédit.

## 1. Fin de la voix de Younes (et une erreur de ma part corrigée)
Dernière parole audible : **267,61 s** (stem DX −40 dBFS) ; elle décroît à −45 dBFS à 267,69 s. Il reste ensuite une **queue du fichier vocal** de 267,70 à 267,88 s à −41…−49 dBFS (énergie 2–8 kHz : −83 dBFS, donc des basses/souffle, pas des aigus), puis silence numérique dès 267,92 s.
*Correction :* j'avais écrit « voix finie à 267,19 s » : mon détecteur avait coupé la phrase sur une pause entre deux mots et écarté le dernier mot (trop court). Les analyses précédentes de ce point de raccord étaient donc décalées de 0,4 s ; la zone du bruit de plume (268,0–270,3 s) reste exacte.

## 2. Les deux secondes avant, les quatre secondes après (master, mesuré)
| Intervalle | Constat |
|---|---|
| 265,6–267,6 s | voix de Younes (−15…−20 dBFS RMS) ; aucun bruit aigu autre que ses sifflantes |
| 267,62–268,00 s | **quasi-silence aiguë** : 2–8 kHz −62…−70 dBFS (reste : ton de pièce à −37 dBFS et queue basse de la voix) |
| **268,00 s** | **le crépitement démarre pile ici** : la plume de synthèse AMB passe de −37 à −30 dBFS (2–8 kHz) en 50 ms, alors que la musique MF entre en fondu |
| 268,0–270,3 s | plume de synthèse à −28…−33 dBFS (2–8 kHz), texture **bruitée** (planéité 0,40 ; kurtosis 4,9 ; centroïde 5,3 kHz) |
| 270,3–273 s | vent, « cahier se referme » (270,7 s) : propres |
Le défaut s'entend donc **0,4 s après la fin de la voix**, au premier instant où l'ambiance « s'ouvre », après un silence aigu net : il ressort davantage.

## 3. Pistes et automations (projet v2, SH37 : 267–271 s)
| Piste | Contenu mesuré |
|---|---|
| **DX** | voix jusqu'à 267,61 s, queue à 267,88 s ; **silence au-delà** ; aucune énergie aiguë après la parole |
| **AMB** | **seule source du bruit** : plume de synthèse (`sound_design_m4.py` l.122, `pen(2.6)` à 267,7 s) ; enveloppe 0,26 → 0,70 (268,9 s) → 0,92 (272 s) |
| **FOL** | pistes tests A/B muettes ; aucune contribution (dans la copie SH37C : 4 gestes de plume réelle à partir de 267,80 s, 2–8 kHz −71 dBFS) |
| **MUS** | MF entre à 268,0 s (fondu 1 s, −0,66 dB) ; sa bande 2–8 kHz (−31…−34 dBFS) est **tonale** (planéité 0,015) et au niveau habituel du morceau (médiane −34,4) : **ce n'est pas du bruit** |
| Transition / traitement | aucun effet actif, aucun artefact de traitement dans le master ou le projet : l'artefact est dans **ma** soustraction (§ 4) |

## 4. Cause du bruit persistant dans C sélectif v1 — contrôle direct du rendu
La plume est bien présente dans le mix avec un **gain variable** (×6,36 à 268,0–268,5 s, puis ×4,3 à ×6,0). Ma v1 soustrayait un gain **unique** (×5,40). Mesure du gain de plume qui reste dans chaque rendu (0 = absente ; A = master) :
| Fenêtre 100 ms | A master | **C v1 (livré)** | **C v2** |
|---|---|---|---|
| 268,0–268,4 s | 6,36 | **0,97 (≈ 15 % restent)** | **0,01** |
| 268,5 s | 6,28 | 0,89 | −0,01 |
| 269,0–269,1 s | 4,78 / 4,38 | **−0,60 / −1,00** (sur-soustraction, plume en opposition de phase) | 0,00 / −0,02 |
| 269,5–269,6 s | 5,73 / 5,83 | 0,34 / 0,44 | 0,01 / −0,01 |
| 269,8–270,2 s | 4,78…4,31 | −0,61…−1,07 | ≤ 0,11 (0,33 sur une fenêtre à 270,1 s) |
Dans la v1, **10 à 17 % de la plume** (bruit large, dans un sens ou dans l'autre) restaient sur toute la zone : planéité 2–8 kHz **0,071** (la musique seule : 0,015). C'est le « grésillement » que vous entendez ; le reste est plus audible juste après la voix car il surgit d'un silence aigu.

## 5. Correction localisée (v2)
* **Cause traitée, pas de réduction de bruit générale** : on soustrait uniquement la **composante > 2,1 kHz de la plume connue** (source AMB M7c), avec son **gain temporel mesuré** (fenêtres de 50 ms, bande 4–8 kHz, 81 fenêtres, de ×4,27 à ×6,39), au lieu d'un gain unique.
* **Voix et reste du mix intacts** : seule cette composante est retirée ; rampe d'entrée **267,80–267,95 s** (après la fin de la voix), sortie 270,30–270,50 s. Le ton de pièce, le vent et la musique ne sont pas modifiés (bande 30–2 100 Hz modifiée : −104,6 dBFS = nulle). Les 4 gestes de plume réelle (version C choisie, même niveau) sont conservés.
| Mesure (8 s : 265–273 s) | A master | C v1 (livré) | **C v2** |
|---|---|---|---|
| Écart avec le master avant 267,78 s (voix de Younes incluse) | — | 2,4·10⁻⁴ | **0,0 (identique au bit près)** |
| Écart avec le master après 270,52 s (vent, cahier) | — | ≈ 0 | **0,0** |
| Énergie 4–8 kHz à 268,0 / 268,5 / 269,0 / 269,5 / 270,0 s (dBFS) | −31,4 / −33,7 / −32,1 / −29,6 / −37,8 | −47,4 / −49,8 / −46,3 / −47,9 / −48,3 | **−59,5 / −50,3 / −48,8 / −52,4 / −50,7** |
| **Planéité 2–8 kHz, 268,0–270,3 s** (bruit = élevé) | 0,399 | 0,071 | **0,022** |
| Sonie intégrée / crête vraie | −15,2 LUFS / −2,9 dBTP | idem | **−15,2 / −2,9** |
| Écrêtage / perte en mono (zone) | 0 / −2,35 dB | 0 / −2,56 | **0 / −2,56** |
| Sauts d'échantillon max locaux (fin de voix / 268–270,2 / sortie) | 0,0542 / 0,1436 / 0,0740 | 0,0542 / 0,0671 / 0,0501 | **0,0542 / 0,0592 / 0,0501** (aucun clic ajouté) |
**Projet REAPER :** non concerné par ce défaut. La couche *delta* de SH37C est calculée à partir de l'ambiance telle que REAPER la joue (exacte par construction) : reste de plume mesuré **≤ 0,62 %**. Aucune modification du projet n'est nécessaire.

## 6. Comparatif (fenêtre 265–273 s, 2,6 s de contexte avant la fin de voix, 2,7 s après la plume)
`audio/SH37_raccord_voix_comparatif_265-273.wav` (+ `_INDEX.txt`) : **1 bip** = master actuel · **2 bips** = C sélectif v1 (livré, non validé : AVANT) · **3 bips** = **C sélectif v2** (APRÈS) · **4 bips** = *contrôle* : v2 **sans** la plume réelle (pour isoler la cause : si un grésillement subsiste encore en 4 bips, il ne vient pas de la plume de synthèse). Même fenêtre pour toutes, 1,000 s de silence entre les versions. `SH37_C2_correction_265-273.wav` : la v2 seule.

## 7. Ce qui reste à confirmer à l'écoute
1. 3 bips : le grésillement a-t-il disparu juste après la voix ? 2. 4 bips (sans plume réelle) : s'il reste un bruit, dites-moi à quel instant ; sinon les gestes de plume réelle sont-ils eux-mêmes perçus comme un grésillement (texture rugueuse, kurtosis 9,6) ? 3. La **queue du fichier vocal** (267,70–267,88 s, basse fréquence, voix non modifiée) vous gêne-t-elle ? Je ne l'ai pas touchée, par respect de la voix.
Scripts : `scripts/diag_fin_voix.py`, `scripts/build_correction_fin_voix.py` · mesures : `analysis/`.
