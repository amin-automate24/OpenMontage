# S3 — LE SABLE : découpage (03:00 → 04:30 du film)

> Statut : **PROPOSITION, en attente de validation.** Aucune image ni vidéo générée.
> 10 plans x 9 s = 90 s. 16:9 plein cadre. Séquence silencieuse (sans dialogue). Réalisme magique : c'est la transformation.

## Intention
Yassine touche le sable : les grains s'élèvent en particules dorées et les murs du grenier deviennent une **fresque vivante** qui s'anime. Une respiration avant la transformation (bible G), puis une montée lente vers le désert de 1975 (S4). La magie reste douce, sacrée, jamais spectaculaire.

## Règles de séquence
- Palette magie (bible F) : or chaud `#F2C14E`, or blanc `#FFE9A8`, halos sur fond sombre ; le rouge et le vert du drapeau restent les seules couleurs saturées.
- Le sable au repos est ocre naturel (PRP_05) ; **l'or n'apparaît qu'à partir du plan S3-03**.
- La fresque est **peinte** (pigments terre, accents d'or), dans le style des références ENV_03 (désert) et ENV_04 (foule vue de dos) pour que S4 la prolonge. **Aucun texte, aucune calligraphie, aucun portrait de personne réelle** (ni Hassan II).
- Yassine : pull bleu marine, pantalon beige. Visage de dos, de loin ou hors cadre (sauf mention).
- Mouvements lents (bible E) : push-in, dolly circulaire lent. Prompts « locked-off ... identique » sauf pour la transformation.

## Découpage
| Plan | Temps | Valeur | Action | Image de départ | Références |
|---|---|---|---|---|---|
| **S3-01** | 0:00-0:09 | Insert mains | Les doigts de Yassine dénouent le tissu blanc du sable (sable ocre naturel) | À créer | PRP_05, PRP_02, YAS_04 |
| **S3-02** | 0:09-0:18 | Macro | Les grains de sable dans sa paume ; un seul grain brille doucement (la respiration avant la transformation) | À créer | PRP_05 |
| **S3-03** | 0:18-0:27 | Insert | Les grains s'élèvent lentement de la paume en particules dorées | À créer | PRP_05 |
| **S3-04** | 0:27-0:36 | Moyen, de dos | Yassine agenouillé, les particules d'or tourbillonnent autour de lui, la lumière devient dorée | À créer | ENV_01, YAS_04 |
| **S3-05** | 0:36-0:45 | Large | Le grenier se remplit de particules d'or en spirale lente, les poutres s'éclairent | À créer | ENV_01 |
| **S3-06** | 0:45-0:54 | Large, mur | Sur le mur nu à la chaux, des traits d'or se dessinent (dunes, silhouettes, drapeaux) | À créer | ENV_01c |
| **S3-07** | 0:54-1:03 | Large, mur | La fresque se colore : désert, foule vue de dos, drapeaux peints ; léger push-in | À créer | ENV_01c, ENV_03, ENV_04 |
| **S3-08** | 1:03-1:12 | Large | La fresque s'anime : la foule peinte marche, les drapeaux flottent ; Yassine minuscule de dos au premier plan | À créer | ENV_01c, ENV_04, YAS_04 |
| **S3-09** | 1:12-1:21 | Insert | Yassine, de dos, tend la main vers la fresque ; les particules d'or le relient au mur | À créer | ENV_01c, YAS_04 |
| **S3-10** | 1:21-1:30 | Large | Le mur se dilate : le désert envahit le cadre, lumière crue, fondu vers S4 | À créer | ENV_03, ENV_04 |

## Sons (bible G)
L'ambiance du grenier s'efface ; crissement du sable, souffle, scintillement granulaire ; textures de cordes en harmoniques, voix lointaine sans paroles ; une respiration (silence) avant la transformation (S3-02).

## Coût estimé (Kling 3.0 Omni 1080p, rien de lancé)
- 10 plans x 920 (image 65 + vidéo 855) = **9 200 en une passe** ; avec 30 % de reprises **≈ 12 000** ; scénario prudent (50 %) **≈ 13 800**.
- Solde réel au dernier relevé : 42 755 crédits : la séquence est financée avec de la marge.

## Risques
- **S3-07 à S3-10 (fresque animée, transformation) :** les plus difficiles pour Kling : déformations, foules étranges, morphing du mur. Je les attends avec le plus de reprises.
- **L'or généré par l'IA :** il peut sembler trop « paillettes » (déjà vu en S2-02). Parade : « poussière dorée fine et chaude, pas de scintillement ni de bokeh » ; correction en étalonnage au montage.
- **S3-01/02/03 :** mains qui se déforment, grains en trop grand nombre.
- **Fresque :** ne jamais montrer de texte ni de portrait ; ne jamais la présenter comme une archive (bible H).

## Décisions demandées
1. Valider le découpage (ou modifier plan par plan).
2. Autorisation de génération : séparée (file `QUEUE.csv`, rien d'approuvé).
3. **Question de fond :** l'or est généré directement par le modèle (plus simple, risque « paillettes ») ou on le garde pour l'étalonnage au montage (plus propre, plus de travail) ? Par défaut : généré, corrigé à l'étalonnage.
