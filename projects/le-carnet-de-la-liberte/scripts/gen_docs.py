#!/usr/bin/env python3
"""Generate shot list (md/csv/json) and prompt pack (md/json) from shots_data.py. Local only."""
import csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from shots_data import SHOTS, SCENES, LINES, TOTAL, validate

ROOT = Path(__file__).resolve().parent.parent
timing = json.loads((ROOT / "animatic" / "dialogue_timing.json").read_text()) if (ROOT / "animatic" / "dialogue_timing.json").exists() else None


def tc(t):
    fr = int(round((t - int(t)) * 25)) % 25
    return f"{int(t)//60:02d}:{int(t)%60:02d}:{fr:02d}"


METHOD_FR = {"STILL_CAM": "Image fixe + mouvement caméra (local)", "I2V": "Image→vidéo (clip animé)",
             "CARD_COMP": "Carton / graphique composité (local)", "TRANSITION": "Transition composité (local)"}

# ------------------------------------------------------------------ shot list
assert not validate()
rows = []
for s in SHOTS:
    rows.append(dict(
        id=f"SH{s['n']:02d}", scene=s["scene"], kind="principal" if s["kind"] == "P" else "secondaire",
        tc_in=tc(s["start"]), tc_out=tc(s["start"] + s["dur"]), start_s=s["start"], dur_s=s["dur"],
        location=s["loc"], framing=s["framing"], camera=s["cam"], method=s["method"],
        dialogue=" | ".join(f"{LINES[k][0]}: {LINES[k][1]}" for k, _ in s["lines"]),
        on_screen=json.dumps(s.get("overlay"), ensure_ascii=False) if s.get("overlay") else "",
        assets=", ".join(s["assets"]), history_flags=",".join(s["flags"]), description=s["desc"]))
(ROOT / "shotlist").mkdir(exist_ok=True)
with open(ROOT / "shotlist" / "shot_list.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
(ROOT / "shotlist" / "shots.json").write_text(json.dumps(dict(total_s=TOTAL, fps=25, shots=SHOTS, scenes=SCENES, lines=LINES), ensure_ascii=False, indent=2))

P = [s for s in SHOTS if s["kind"] == "P"]
S = [s for s in SHOTS if s["kind"] == "S"]
i2v = [s for s in SHOTS if s["method"] == "I2V"]
still = [s for s in SHOTS if s["method"] == "STILL_CAM"]
card = [s for s in SHOTS if s["method"] in ("CARD_COMP", "TRANSITION")]
md = []
md.append("# TECHNICAL SHOT LIST 1.0 — LE CARNET DE LA LIBERTÉ\n")
md.append(f"Source : Screenplay Draft 1.1 (FR). Durée totale planifiée : **{sum(s['dur'] for s in SHOTS):.1f} s = 4 min 30 s** (maximum absolu 300 s). Format 1920×1080, 25 i/s, 16:9.\n")
md.append(f"**{len(SHOTS)} plans** : {len(P)} principaux (cible 20–30 respectée) + {len(S)} secondaires (inserts, cartons, transitions locales, sans génération).\n")
md.append(f"**Méthodes de production** : {len(still)} plans « image fixe + caméra », **{len(i2v)} plans image→vidéo** (SH{', SH'.join(f'{s['n']:02d}' for s in i2v)} = {sum(s['dur'] for s in i2v):.1f} s à l'écran, clips générés de 5 s), {len(card)} cartons/transitions composités localement.\n")
md.append("Légende : **P** principal, **S** secondaire. Les timecodes sont `mm:ss:ff` (25 i/s). Les textes à l'écran (dates, cartons, drapeaux, calligraphie) sont **toujours composités en post-production**, jamais générés par l'IA.\n")
for sc, info in SCENES.items():
    ss = [s for s in SHOTS if s["scene"] == sc]
    md.append(f"\n## SCÈNE {sc} — {info['title']}  ({tc(info['start'])} → {tc(info['end'])}, {info['end']-info['start']:.0f} s) — ambiance : {info['palette']}\n")
    md.append("| ID | K | TC in | TC out | Durée | Cadre | Caméra | Méthode | Contenu / dialogue | Assets | Revue |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for s in ss:
        dlg = "<br>".join(f"**{LINES[k][0]}** : « {LINES[k][1]} »" for k, _ in s["lines"])
        ov = s.get("overlay")
        extra = ""
        if ov and ov.get("text"): extra = f"<br>*À l'écran :* {ov['text']}"
        md.append(f"| SH{s['n']:02d} | {s['kind']} | {tc(s['start'])} | {tc(s['start']+s['dur'])} | {s['dur']:.1f} s | {s['framing']} | {s['cam']} | {METHOD_FR[s['method']]} | {s['desc']}{('<br>'+dlg) if dlg else ''}{extra} | {', '.join(s['assets'])} | {', '.join(s['flags']) or '—'} |")
md.append("\n## Continuité (personnages et décors récurrents)\n")
md.append("| Élément | Plans |\n|---|---|")
track = {}
for s in SHOTS:
    for a in s["assets"]:
        track.setdefault(a.split(" (")[0], []).append(s["n"])
for a, ns in sorted(track.items()):
    md.append(f"| {a} | {', '.join(f'SH{n:02d}' for n in ns)} |")
md.append("\n## Plans nécessitant une vraie animation image→vidéo\n")
for s in i2v:
    md.append(f"- **SH{s['n']:02d}** ({s['dur']:.1f} s à l'écran, clip généré de 5 s{', prolongé par maintien/ralenti local' if s['dur']>5 else ''}) — {s['desc']}")
md.append("\nTous les autres plans sont des images fixes avec mouvements de caméra contrôlés (push-in, pull-out, pan) ou des graphiques locaux : pas de génération vidéo.\n")
md.append("## Contrôles de durée\n")
md.append(f"- Somme des plans : {sum(s['dur'] for s in SHOTS):.1f} s ; scènes : 30 + 35 + 55 + 55 + 75 + 20 = 270 s ✔ (les bornes de scène du scénario sont respectées au plan près).\n- Voir `docs/HISTORICAL_AND_TIMING_FLAGS_1.0.md` pour l'analyse de rythme (la scène 6 est trop dense).\n")
(ROOT / "shotlist" / "TECHNICAL_SHOT_LIST_1.0.md").write_text("\n".join(md), encoding="utf-8")

# ------------------------------------------------------------------ prompt pack
STYLE = ("Cinematic stylized 3D animated film, original character design (not copying any existing studio character), "
         "expressive faces, credible proportions, painterly PBR materials, soft volumetric light, shallow depth of field, "
         "16:9, clean composition with safe margins, family-friendly, for Moroccan primary-school students")
NEG = ("photorealistic photograph, fake archival photo, text, letters, captions, gibberish writing, watermark, logo, "
       "real person likeness, celebrity, king portrait, weapons, violence, blood, scary, distorted hands, extra fingers, "
       "modern objects in historical scenes, anachronistic clothing")
CHAR = {
    "C-Younes": "YOUNES: Moroccan boy, 10 years old, short dark curly hair, warm brown eyes, round friendly face, expressive eyebrows, light-blue shirt and navy trousers (white school smock in class), small gap-toothed curious smile",
    "C-Amina11": "AMINA aged 11 (1944): Moroccan girl, long dark braid, round face and the same warm brown eyes as Younes (family resemblance), simple ochre dress with a light cream headscarf [COSTUME TO VERIFY H5]",
    "C-Amina20": "AMINA aged 20 (1953): same face and eyes, slimmer features, hair covered with a soft muted-blue headscarf, simple modest dress in muted tones, thoughtful gaze [COSTUME TO VERIFY H5]",
    "C-Amina22": "AMINA aged 22-23 (1955-56): same face, radiant confident expression, warm coloured dress and light headscarf [COSTUME TO VERIFY H5]",
    "C-Amina23": "AMINA aged 22-23 (1955-56): same face, radiant confident expression, warm coloured dress and light headscarf [COSTUME TO VERIFY H5]",
    "C-Père": "AMINA'S FATHER (fictional): Moroccan man in his 40s, kind lined face, short greying beard, brown wool djellaba, red tarbouche/fez [COSTUME TO VERIFY H5], calm dignified posture; NOT a depiction of any historical person",
    "C-Maîtresse": "THE TEACHER: woman in her 30s, warm smile, dark wavy shoulder-length hair, soft cardigan over a light blouse [headscarf choice = creative decision D6]",
    "C-Mère": "YOUNES' MOTHER: woman in her mid 30s, gentle proud smile, casual modern home clothes, dark hair tied back",
}
TXT_RULE = "Leave all writing surfaces (blackboard, notebook pages, documents, flags) EMPTY or neutral: text, dates and flags are composited later."
pack = []
jpack = {"style": STYLE, "negative": NEG, "characters": CHAR, "rule": TXT_RULE, "refs": [], "shots": []}

REFS = [
    ("REF-00", "Style board", "Single 16:9 style key image: stylized 3D look, warm classroom light blending into sepia notebook page edge. Used as STYLE reference for all later generations."),
    ("REF-01", "Younes — character sheet", "Character sheet of YOUNES, front/3-quarter/profile + 3 expressions (curious, hesitant, proud), neutral background. " + CHAR["C-Younes"]),
    ("REF-02", "Amina — multi-age sheet", "Character sheet of ONE girl/woman at three ages on one sheet (11, 20, 23) with identical facial structure. " + CHAR["C-Amina11"] + " | " + CHAR["C-Amina20"] + " | " + CHAR["C-Amina22"]),
    ("REF-03", "Le père — character sheet", "Character sheet, front/3-quarter/profile, two expressions (serious, tender). " + CHAR["C-Père"]),
    ("REF-04", "La maîtresse — character sheet", "Character sheet, front/3-quarter, two expressions. " + CHAR["C-Maîtresse"]),
    ("REF-05", "La mère — character sheet", "Character sheet, front/3-quarter. " + CHAR["C-Mère"]),
    ("REF-06", "Props sheet", "Props sheet on neutral background: old leather notebook (cover blank), faded sepia photograph (faces not legible), carved wooden box, 1950s tube radio (dial without text), school notebook (cahier). Blank surfaces."),
    ("E1", "Environnement — classe 2026", "Wide shot of a bright Moroccan primary-school classroom, blackboard front, wooden desks, window light shaft, a small Moroccan flag corner (flag will be replaced by vector). Natural welcoming light. Empty of people."),
    ("E2", "Environnement — maison familiale 2026", "Warm family living room, afternoon light, low sofa, window, Moroccan textiles, shelf; empty of people."),
    ("E3", "Environnement — rue 1944", "Narrow old Moroccan medina street, 1944, warm ochre and sepia light, plastered walls, carved wooden doors, no modern objects, no signage text; empty of people. [ARCHITECTURE TO VERIFY H5]"),
    ("E4", "Environnement — intérieur 1940s", "Modest 1940s Moroccan home interior, low wooden table, carved window shutter, floor cushions, oil lamp; produce a DAY variant (warm ochre) and reuse with NIGHT blue-gray grade for 1953. Empty of people. [ARCHITECTURE TO VERIFY H5]"),
    ("E5", "Environnement — Rabat 1955", "Wide street and facades in Rabat, 1955, bright festive daylight, bunting poles (flags composited later), empty of people. [ARCHITECTURE TO VERIFY H5]"),
]
for r in REFS:
    jpack["refs"].append(dict(id=r[0], title=r[1], prompt=r[2]))
pk = ["# GENERATION PROMPT PACK 1.0 — PRÉPARATION UNIQUEMENT (aucune génération lancée)\n",
      "> **Statut : rédigé, non exécuté.** Aucun appel payant n'a été fait. Chaque exécution exige l'approbation écrite de l'étape correspondante (voir `approvals/APPROVAL_REGISTER_1.0.md`).\n",
      "## 1. Blocs réutilisables\n",
      f"**STYLE (à préfixer à tout prompt image)** :\n```\n{STYLE}\n```\n",
      f"**NEGATIVE (à fournir quand le modèle accepte un negative prompt)** :\n```\n{NEG}\n```\n",
      f"**RÈGLE TEXTE** : {TXT_RULE}\n",
      "**Modèle image proposé** : Google Nano Banana 2.1 (références personnage/style supportées), 16:9, 2k, 65 crédits/image (exact, simulé). Alternative bon marché pour tests de composition : flux-dev, 10 crédits. **Modèle vidéo proposé** : Kling 2.5, 1080p, 5 s, image de départ imposée, 325 crédits/clip (exact, simulé) — silencieux, donc son 100 % en post.\n",
      "**Principe de continuité** : chaque génération de plan reçoit en références (1) le style board REF-00, (2) la fiche du ou des personnages, (3) le décor de référence. Toujours conserver le seed/ID de génération dans `approvals/generation_log.json`.\n",
      "## 2. Blocs personnages\n"]
for k, v in CHAR.items():
    if k == "C-Amina23": continue
    pk.append(f"- **{k}** — {v}")
pk.append("\n## 3. Images de référence (étape 1/2)\n")
for r in REFS:
    pk.append(f"### {r[0]} — {r[1]}\n```\n{STYLE}. {r[2]}\n```\n")

pk.append("## 4. Prompts image par plan (étape 2)\n")
pk.append("Chaque prompt = `STYLE` + description ci-dessous + blocs personnages cités + `RÈGLE TEXTE`. Éclairage et étalonnage par époque : 1944 ocre/sépia chaud ; 1953 gris-bleu désaturé, contraste retenu ; 1955-56 de plus en plus chaud et lumineux ; 2026 lumière naturelle accueillante.\n")
for s in SHOTS:
    if s["method"] in ("TRANSITION",) or (s["method"] == "CARD_COMP" and s["n"] in (33,)):
        continue
    chars = [a for a in s["assets"] if a.startswith("C-")]
    cblocks = " | ".join(CHAR[c] for c in chars if c in CHAR)
    light = {"1944": "warm ochre and sepia light", "1953": "muted blue-gray light, restrained contrast", "1955-56": "warm bright hopeful light", "2026": "natural welcoming light"}[SCENES[s["scene"]]["era"]]
    if s["n"] in (26, 27, 28, 29, 30, 31, 32, 34): light = "warm, bright, hopeful light"
    if s["n"] in (21, 22, 23, 24): light = "muted blue-gray evening light, restrained contrast"
    prompt = f"{STYLE}. {s['kf']}. Lighting: {light}. Framing: {s['framing']}. {TXT_RULE}"
    if cblocks: prompt += f" Characters: {cblocks}."
    refs = ["REF-00 (style)"] + [c for c in s["assets"] if c.startswith(("C-", "E", "P-"))]
    entry = dict(shot=f"SH{s['n']:02d}", method=s["method"], prompt=prompt, negative=NEG, references=refs, history_flags=s["flags"])
    jpack["shots"].append(entry)
    pk.append(f"### SH{s['n']:02d} — {s['framing']} — {s['desc']}\n- Références à joindre : {', '.join(refs)}\n- Revue historique requise avant génération : {', '.join(s['flags']) or 'aucune'}\n```\n{prompt}\n```\n")

pk.append("## 5. Prompts image→vidéo (étape 3 — uniquement les 5 plans animés)\n")
pk.append("Départ = image de départ validée (start frame). Durée de génération 5 s. Pas de dialogue ni de musique générés (Kling 2.5 est silencieux).\n")
for s in i2v:
    mp = f"{s['motion']} Keep character identity and costume exactly as in the start frame. Stylized 3D look unchanged. No text, no new objects."
    jpack["shots"].append(dict(shot=f"SH{s['n']:02d}", method="I2V_MOTION", prompt=mp, duration=5, resolution="1080p", model="kling-25", start_frame=f"keyframe SH{s['n']:02d}"))
    pk.append(f"### SH{s['n']:02d} (écran {s['dur']:.1f} s)\n```\n{mp}\n```\n")
pk.append("## 6. Ce qui n'est PAS généré\n- Dates, cartons, légendes, ligne du temps, titre : composités (Remotion/HyperFrames/DaVinci).\n- Drapeaux marocains : vecteur dessiné localement (étoile verte à cinq branches, rouge officiel) et incrusté ; jamais généré par IA.\n- Calligraphie arabe et textes de documents : jamais générés.\n- Archives : aucune « archive » fabriquée ; les inserts historiques portent la mention « ILLUSTRATION PÉDAGOGIQUE — non archive ».\n- Mohammed V : aucun visage, aucune voix, aucun discours inventé.\n")
(ROOT / "prompts").mkdir(exist_ok=True)
(ROOT / "prompts" / "GENERATION_PROMPT_PACK_1.0.md").write_text("\n".join(pk), encoding="utf-8")
(ROOT / "prompts" / "prompt_pack.json").write_text(json.dumps(jpack, ensure_ascii=False, indent=2))
print("ok", len(jpack["shots"]), "prompt entries;", len(rows), "rows")
