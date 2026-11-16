# CHARACTER AND ENVIRONMENT REFERENCE PLAN 1.0

Statut : **plan uniquement** — aucune image générée. Les prompts correspondants sont dans `prompts/GENERATION_PROMPT_PACK_1.0.md` (REF-00 à REF-06, E1 à E5).

## 1. Principes

1. **Un seul style** : 3D stylisée cinématographique, personnages originaux (aucune ressemblance avec un personnage de studio existant), visages expressifs, proportions crédibles.
2. **Références d'abord, plans ensuite** : aucun plan n'est généré avant validation humaine des fiches REF-01 à REF-05 et du style board REF-00.
3. **Famille reconnaissable** : Younes et Amina partagent la forme du visage et les yeux (regard brun chaud) pour matérialiser la transmission.
4. **Éléments sensibles jamais générés** : drapeaux, texte, calligraphie, dates → composités en post ; personnes historiques réelles → non représentées.
5. **Nommage fichiers** : `REF-01_Younes_v001.png`, `E3_rue1944_v001.png`, `SH14_kf_v001.png` ; chaque génération consigne modèle, seed, prompt, date, coût dans `approvals/generation_log.json` (créé à la première génération approuvée).

## 2. Personnages

| ID | Personnage | Âge / époque | Plans | Conception | Points d'attention |
|---|---|---|---|---|---|
| C-Younes | Younes | 10 ans, 2026 | SH01, 03, 05, 07, 09, 10, 35–37 | **VERROUILLÉ — REF-01 v002 (16/11)** : cheveux bruns bouclés courts, grands yeux bruns, visage rond ; chemise blanche à col, pull sans manches bleu marine, pantalon marine, baskets, cartable (plus de blouse) | Tenue validée ; ne plus modifier |
| C-Amina11 | Amina | 11 ans, 1944 | SH13, 14, 16, 18, 19 | Longue tresse brune, robe ocre simple, foulard crème léger | Costume féminin urbain 1944 à vérifier (H5) |
| C-Amina20 | Amina | ≈ 20 ans, 1953 | SH21, 23, 24 | Même visage, traits affinés, foulard bleu-gris, tenue sobre | Teintes sourdes imposées par l'étalonnage |
| C-Amina22/23 | Amina | ≈ 22–23 ans, 1955-56 | SH26, 28, 30, 32, 34 | Même visage, expression rayonnante, tenue plus claire et colorée | Progression chaleureuse vers 1956 |
| C-Père | Père d'Amina (fictif) | ≈ 40–50 ans | SH13–19, 21–23, 28, 32 | Barbe courte grisonnante, djellaba de laine brune, tarbouche rouge | Ne représente aucune personne réelle ; costume à vérifier (H5) |
| C-Maîtresse | La maîtresse | ≈ 30–35 ans | SH01, 02, 04, 35, 37 | Cheveux ondulés mi-longs, gilet clair | Décision D6 (foulard ou non) |
| C-Mère | Mère de Younes | ≈ 35 ans | SH09 | Tenue d'intérieur moderne, chignon | Apparition brève : réutiliser REF-05 sans planche élaborée |
| Figurants | Élèves, habitants, foule | — | SH01, 13, 27, 35 | Silhouettes non identifiables | Aucun visage « historique » identifiable |

**Interdits** : portrait de Mohammed V, d'un souverain actuel, de figures politiques réelles ; voix imitées ; fausses photographies d'archive.

## 3. Progression d'âge d'Amina (contrôle de continuité)

| Date (carnet) | Âge | Version | Lumière dominante |
|---|---|---|---|
| 11 janv. 1944 | ≈ 10–11 ans (née vers 1933) | C-Amina11 | Ocre et sépia chauds |
| 20 août 1953 | ≈ 20 ans | C-Amina20 | Gris-bleu sourd, contraste retenu |
| 16–18 nov. 1955 | ≈ 22 ans | C-Amina22 | Plus chaud, plus lumineux |
| 2 mars 1956 | ≈ 22–23 ans | C-Amina23 (= 22) | Chaud, lumineux |

## 4. Décors

| ID | Décor | Époque | Plans | Remarques |
|---|---|---|---|---|
| E1 | Classe d'école primaire | 2026 | SH01–06, 35–38 | Lumière naturelle accueillante ; tableau vide (texte composité) ; **aucun portrait officiel dessiné** (H10) |
| E2 | Maison familiale / salon | 2026 | SH07–11 | Lumière d'après-midi |
| E3 | Rue de médina | 1944 | SH12–15 | Ocre/sépia ; sans enseignes ni objets modernes ; architecture à vérifier (H5) |
| E4 | Intérieur modeste 1940s (jour / soir / saisons) | 1944–1956 | SH16–26, 30, 32, 34 | **Un seul décor, trois étalonnages** (ocre, bleu-gris, chaud) = économie + continuité ; fenêtre récurrente |
| E5 | Rue de Rabat en fête | 1955 | SH27–28 | Drapeaux incrustés en vecteur ; souverain jamais montré |

## 5. Accessoires récurrents (REF-06)

Carnet de cuir (couverture vierge → titre composité), photographie sépia (visages non lisibles), boîte en bois sculpté, radio à lampes années 1950 (cadran sans texte), cahier d'école de Younes.

## 6. Références historiques à fournir ou valider par un humain (avant l'étape images)

- Drapeau marocain : proportions et étoile verte à cinq branches (source officielle) → je dessine ensuite le vecteur.
- Costumes civils urbains 1944–1956 (hommes et femmes), couvre-chefs.
- Architecture de médina, intérieurs modestes, mobilier ; rues de Rabat en 1955.
- Radio domestique des années 1950 (type, ordre de grandeur).
- Aucune photographie d'archive ne sera insérée sans identification de la source et vérification des droits.

## 7. Check-list de validation d'une fiche (humaine, avant approbation d'étape)

- [ ] Visage cohérent sur toutes les vues ; yeux de la « famille » respectés
- [ ] Costume plausible pour l'époque (revue H5)
- [ ] Aucune ressemblance avec une personne réelle ou un personnage de franchise
- [ ] Mains et proportions correctes ; pas de texte parasite
- [ ] Palette conforme à l'époque (ocre / gris-bleu / chaud / naturel)
