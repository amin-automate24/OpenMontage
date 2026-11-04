# Fiche personnage — YASSINE

> Statut : **VALIDÉE.** Référence maîtresse : YAS_01 v1_1 (seed 4033502968).
> Le prompt YAS_01 ci-dessous est conservé tel qu'il a été généré (cicatrice à gauche) ; le descripteur canonique fait foi pour la suite.

## Rôle dans le film
Yassine est le regard du film : le spectateur découvre la boîte, la magie et 1975 à travers lui. Il est présent dans les 6 séquences, dans des plans larges comme en gros plans. **C'est le personnage dont la cohérence compte le plus.** Sa référence doit être solide avant toute autre création.

## Identité visuelle verrouillée

| Attribut | Description |
|---|---|
| Âge | 8 ans |
| Origine | Garçon marocain de Fès |
| Morphologie | Mince, taille moyenne pour son âge, épaules étroites |
| Visage | Ovale aux joues encore rondes, menton fin |
| Peau | Mate, brun olive clair, chaleureuse |
| Yeux | Grands, en amande, brun foncé, longs cils |
| Sourcils | Épais, foncés, légèrement arqués |
| Nez | Petit, arête droite |
| Bouche | Lèvres pleines ; sourire timide, souvent bouche fermée |
| Cheveux | Noirs, courts, légèrement ondulés, une mèche rebelle sur le front |
| **Signe distinctif** | **Petite cicatrice claire sur le côté droit du front, au-dessus du sourcil droit** (ancre de continuité — alignée sur YAS_01 v1_1, validé le 2026-11-04) |
| Costume (verrouillé pour tout le film) | Pull ras du cou en coton bleu marine avec un fin liseré crème au col, pantalon en toile beige, baskets blanches usées |
| Accessoire | Aucun (le sable, plus tard, deviendra « son » objet) |

## Jeu et comportement
- **Personnalité :** curieux, observateur, plus silencieux que bavard, courageux sans être téméraire.
- **Posture :** se penche en avant pour regarder ; s'accroupit pour examiner les objets.
- **Gestes :** touche les choses du bout des doigts, avec précaution.
- **Expressions à créer :**
  1. neutre attentive ;
  2. curiosité (sourcils relevés) ;
  3. émerveillement (bouche entrouverte, yeux grands) ;
  4. légère inquiétude ;
  5. sourire de fierté ;
  6. émotion retenue (yeux brillants).

## Descripteur canonique (anglais, copié tel quel dans chaque prompt)
```
Yassine, an 8-year-old Moroccan boy from Fez, slim build, oval face with soft round cheeks, warm light olive-brown skin, large dark-brown almond-shaped eyes with long lashes, thick dark slightly arched eyebrows, small straight nose, short slightly wavy black hair with one loose curl on his forehead, a small pale scar on the right side of his forehead above his right eyebrow, wearing a navy-blue cotton crewneck sweater with a thin cream trim at the collar
```

## Plan des références à produire

| ID | Référence | Format | Ordre |
|---|---|---|---|
| YAS_01 | Portrait de face (**référence maîtresse**) | 3:4 | 1 |
| YAS_02 | Portrait trois-quarts | 3:4 | 2, à partir de YAS_01 |
| YAS_03 | Profil | 3:4 | 3, à partir de YAS_01 |
| YAS_04 | Vue en pied (costume complet) | 2:3 | 4 |
| YAS_05 | Fiche multi-angle (turnaround) | 16:9 | 5 |
| YAS_06 | Planche d'expressions (6 expressions) | 16:9 | 6 |

Méthode : YAS_01 est généré seul. Une fois validé, il sert de **référence de personnage** (Omni Reference ou image prompt, selon ce que propose ta version de Midjourney) et son seed est noté, pour YAS_02 à YAS_06.

---

## PROMPT MIDJOURNEY YAS_01 — Portrait de face (référence maîtresse)

**Rôle :** fixer l'identité faciale de Yassine pour tout le film. Le fond est volontairement neutre : c'est une référence, pas un plan du film. Un fond neutre évite que le décor « contamine » les générations suivantes.

```
Photorealistic cinematic character reference portrait of Yassine, an 8-year-old Moroccan boy from Fez, slim build, oval face with soft round cheeks, warm light olive-brown skin, large dark-brown almond-shaped eyes with long lashes, thick dark slightly arched eyebrows, small straight nose, short slightly wavy black hair with one loose curl on his forehead, a small pale scar above his left eyebrow, wearing a navy-blue cotton crewneck sweater with a thin cream trim at the collar. Front view, head and shoulders, centered, looking straight into the lens, calm curious expression with a faint closed-mouth smile. Soft warm window light from the left, gentle fill, plain warm-grey studio backdrop. 85mm lens, f/4, natural skin texture, fine 35mm film grain, true-to-life color --ar 3:4 --style raw --s 50 --no smile with teeth, makeup, jewelry, hat, text, watermark, cartoon, illustration, plastic skin, extra fingers
```

### Paramètres
| Paramètre | Valeur | Raison |
|---|---|---|
| Version | V8.2 si disponible dans ton compte, sinon V7 | Meilleur photoréalisme |
| `--ar 3:4` | portrait | Cadre une tête et des épaules sans recadrage |
| `--style raw` | — | Réduit l'embellissement automatique et garde un rendu photographique naturel |
| `--s 50` | stylisation basse | Fidélité au prompt plutôt qu'interprétation artistique |
| `--no …` | exclusions | Évite les sourires dentés « publicitaires », le maquillage, le rendu illustration |
| Mode | fast | Une grille de 4 propositions |
| Après génération | upscale de la meilleure image, puis récupération du `seed` | Le seed servira aux variations |

À vérifier dans ton interface au moment de lancer : disponibilité de `--style raw` et de `--oref` dans ta version. Si un paramètre est refusé, retire-le sans changer le reste du prompt et indique-le-moi.

### Résultat attendu
- Une grille de 4 portraits de face d'un garçon de 8 ans crédible, au visage enfantin (pas d'air adulte), au regard droit et à la lumière douce venant de la gauche.
- Pull bleu marine bien lisible, fond gris chaud uni.

**Critères de choix :**
1. regard vivant et naturel ;
2. cicatrice au sourcil gauche visible mais discrète ;
3. âge crédible ;
4. pas de déformation (oreilles, dents, symétrie) ;
5. peau texturée, non lissée.

Si la cicatrice n'apparaît sur aucune image, on la corrigera par une retouche ciblée (édition Midjourney), sans régénérer tout le portrait.

### Contrôle à réception
Je vérifierai la conformité au descripteur, le réalisme, l'âge apparent, la lumière, les artefacts et la compatibilité avec la palette (le bleu marine doit se détacher sur l'ambre du grenier). Je te présenterai mes observations ; la décision te revient.
