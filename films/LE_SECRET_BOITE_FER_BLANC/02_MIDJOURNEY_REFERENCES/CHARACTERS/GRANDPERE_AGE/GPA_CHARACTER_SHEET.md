# Fiche personnage : LE GRAND-PÈRE ÂGÉ (aujourd'hui, Fès)

> Statut : **PROPOSITION, en attente de validation.** Personnage fictif.

## Rôle dans le film
Il apparaît en S1 (la maison) et en S6 (la transmission) : le gardien de la mémoire. Le spectateur doit **reconnaître immédiatement** en lui le jeune homme de 1975 (GPJ_01_MASTER), 51 ans plus tard.

## Ce qui ne change pas (ancres d'identité héritées de GPJ_01_MASTER)
- Visage allongé, pommettes hautes, nez légèrement aquilin.
- Yeux brun foncé en amande, profondément enfoncés.
- **Grain de beauté sous l'œil gauche.**
- Moustache, portée de la même façon (fine, soignée).
- Même structure d'oreilles et de mâchoire.

## Ce qui change avec l'âge (73 ans)

| Attribut | Description |
|---|---|
| Cheveux | Gris argenté, plus clairsemés, front légèrement dégarni, coupés court |
| Moustache | **Blanche**, fine, toujours soignée |
| Peau | Rides profondes au front et autour des yeux (pattes d'oie du sourire), sillons nasogéniens marqués, taches de vieillesse discrètes, peau hâlée |
| Yeux | Paupières un peu tombantes, regard doux et vif |
| Silhouette 💡 | Toujours mince, épaules légèrement voûtées |
| Costume 💡 | Djellaba de laine **brun grisé** (tenue d'intérieur d'hiver, novembre à Fès), chemise blanche dessous, **petite calotte blanche (taqiya)** en option |
| Accessoire 💡 | Chapelet (tasbih) en bois, en option, pour la scène S1 |

*Points 💡 à valider : costume, taqiya, chapelet.*

## Descripteur canonique (anglais)
```
a 73-year-old Moroccan man from Fez, the same man as the young man in the reference photo 51 years later, lean build with slightly stooped shoulders, long face with high cheekbones, slightly aquiline nose, deep-set dark-brown almond-shaped eyes with gentle drooping eyelids, a small mole under his left eye, short thinning silver-grey hair with a slightly receding hairline, a neat thin white mustache, deep forehead lines and crow's feet, pronounced smile lines, warm sun-tanned olive skin with faint age spots, kind and lively expression
```

---

## MÉTHODE DE VIEILLISSEMENT PROPOSÉE

**Méthode recommandée : image de référence forte depuis GPJ_01_MASTER.**
- Le portrait âgé utilise **le même cadrage** (face, tête et épaules, même lumière, même fond).
- Contrairement à YAS_02 et YAS_03, la tendance de la référence à imposer la pose **joue ici en notre faveur** : on veut justement la même pose.
- Un poids de référence élevé (`--iw 1.5`) garde la structure du visage. Le texte décrit le vieillissement.

**Pourquoi pas une retouche par zone :** vieillir demande de changer la peau, les cheveux, la moustache et le contour des yeux, donc presque toute la tête. Avec un masque aussi grand, on régénère le visage presque entier, et on perd l'avantage de la retouche.

## PROMPT MIDJOURNEY GPA_01 : portrait de face (référence principale)

```
https://platform2.cdn.acedata.cloud/midjourney/da3a9e54-c753-4529-bf6e-4e61d16a8e6d.png Photorealistic cinematic character reference portrait of a 73-year-old Moroccan man from Fez, the same man as the young man in the reference photo 51 years later, lean build with slightly stooped shoulders, long face with high cheekbones, slightly aquiline nose, deep-set dark-brown almond-shaped eyes with gentle drooping eyelids, a small mole under his left eye, short thinning silver-grey hair with a slightly receding hairline, a neat thin white mustache, deep forehead lines and crow's feet, pronounced smile lines, warm sun-tanned olive skin with faint age spots, wearing a grey-brown wool djellaba over a white shirt. Front view, head and shoulders, centered, looking straight into the lens, kind calm expression with a faint warm smile. Soft warm window light from the left, plain warm-grey studio backdrop. 85mm lens, f/4, natural skin texture, fine 35mm film grain, true-to-life color --ar 3:4 --style raw --s 50 --iw 1.5 --no beard, glasses, jewelry, young face, black hair, text, watermark, cartoon, illustration, plastic skin, light outline, halo
```

| Paramètre | Valeur | Raison |
|---|---|---|
| Image de référence | GPJ_01_MASTER (URL source Midjourney) | Structure du visage et pose identiques |
| `--iw 1.5` | élevé | Garde l'ossature ; si le résultat reste trop jeune, on baisse à 1.0 |
| `--no young face, black hair` | — | Empêche Midjourney de recopier la jeunesse de la référence |
| Version / mode | V8.2, fast | Identiques |
| Coût estimé | environ 0,4 crédit Midjourney | — |

**Contrôle prévu :** comparaison à trois, côte à côte et à la même échelle : GPJ_01_MASTER, la proposition âgée, et Yassine (pour l'air de famille).
