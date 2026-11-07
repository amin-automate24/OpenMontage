# S2 — LE GRENIER : découpage (01:30 → 03:00 du film)

> Statut : ✅ **VALIDÉ (2026-11-05).** Aucune image ni vidéo générée (autorisation de génération à donner séparément).
> 10 plans x 9 s = 90 s. 16:9 plein cadre. Séquence silencieuse (comme S1). Présent, grenier.

## Intention
Poussière dans les rais de lumière, objets oubliés, le coffre de cèdre, la boîte en fer blanc : ouverture, puis découverte des trois objets. Le **silence avant l'ouverture** est le point d'orgue (bible G) : presque aucune musique, un bourdon grave.

## Règles de séquence
- Fenêtre à **gauche** du cadre, un seul rai ambré ; coffre de cèdre au **coin droit** ; aucun texte, câble, plastique.
- Yassine : pull bleu marine, pantalon beige, baskets blanches usées. Visage **de dos, de loin ou en plan large** sauf S2-10 (test d'identité).
- Boîte en fer blanc : toujours dérivée de PRP_01 / PRP_02 ; Coran sans écriture (médaillon géométrique).
- Prompts « locked-off, architecture strictement identique » ; Kling élargit le cadrage.

## Découpage
| Plan | Temps | Valeur | Action | Caméra | Image de départ | Références |
|---|---|---|---|---|---|---|
| **S2-01** | 0:00-0:09 | Très large | Grenier vide, un rai ambré, poussière en suspension | Static, push-in très léger | **ENV_01_MASTER** (existante, sans nouvelle image) | ENV_01 |
| **S2-02** | 0:09-0:18 | Insert | Poussière qui flotte dans le rai de lumière | Static, macro | À créer | ENV_01 |
| **S2-03** | 0:18-0:27 | Large | Yassine entre par la porte basse du fond, de dos, petit dans le grenier | Static | À créer | ENV_01, YAS_04 |
| **S2-04** | 0:27-0:36 | Moyen, de dos | Il avance dans le rai, regarde malles, tapis roulés, cuivres | Léger tracking | À créer | ENV_01, YAS_04 |
| **S2-05** | 0:36-0:45 | Insert mains | Sa main passe sur un tapis roulé, la poussière se soulève | Static, 85 mm | À créer | ENV_01, YAS_04 |
| **S2-06** | 0:45-0:54 | Moyen | Il s'agenouille devant le coffre de cèdre du coin droit, de dos | Static | À créer | ENV_01b, YAS_04 |
| **S2-07** | 0:54-1:03 | Insert | La boîte en fer blanc dans le coffre, poussière et traces de doigts | Static, macro | À créer (PRP_01) | PRP_01, ENV_01b |
| **S2-08** | 1:03-1:12 | Gros plan mains | Ses mains sortent la boîte et la posent dans le rai de lumière (silence) | Static | À créer | PRP_01, ENV_01 |
| **S2-09** | 1:12-1:21 | Insert | Le couvercle s'ouvre : drapeau plié, Coran, tissu de sable | Static, très léger push-in | À créer (PRP_02) | PRP_02, PRP_03, PRP_04, PRP_05 |
| **S2-10** | 1:21-1:30 | Moyen, de trois-quarts | Yassine, éclairé par la boîte, regard d'émerveillement discret | Static | À créer ⚠ test d'identité | YAS_06, YAS_01, ENV_01 |

## Sons (bible G)
Vent léger, craquements du bois ; glissement de la boîte, couvercle métallique, tissu du drapeau ; presque pas de musique, bourdon grave ; **silence avant l'ouverture (S2-08 à S2-09)**.

## Coût estimé (Kling 3.0 Omni 1080p, rien de lancé)
- 1 vidéo sans image (S2-01) : 855 ; 9 plans à 920 : 8 280 → **≈ 9 135 en une passe** ; avec 30 % de reprises **≈ 11 900**.
- Solde au moment de la rédaction : 8 070 → il manque **≈ 3 800** pour finir S2 avec reprises.

## Risques
- **S2-10 :** seul plan avec visage ; identité à vérifier face à YAS_01/YAS_06 avant la vidéo ; repli : plan de dos ou de profil lointain.
- **S2-09 :** les trois objets doivent rester ceux de PRP_02 (Coran sans écriture).
- **S2-05/08 :** mains qui se déforment en bougeant.

## Décisions demandées
1. Valider le découpage (ou modifier plan par plan).
2. Autorisation de génération : séparée (voir QUEUE.csv, tout est non approuvé).
