# Film Studio — Meta Skill

## When to Use

The user wants a **narrative short film** (drama, thriller, sci-fi, horror, music-video narrative,
historical, experimental) built from an idea: characters, a screenplay, continuity between shots,
original score. This is an overlay on the **`cinematic` pipeline**, not a separate pipeline: every rule
in `AGENT_GUIDE.md` (Rule Zero, preflight, decision communication, gates, motion-required) still applies.

Docs: `docs/film-studio/ARCHITECTURE.md` (phase ↔ stage map), `docs/film-studio/ENVIRONMENT_AUDIT.md`
(last audit), `docs/film-studio/FIRST_FILM_PLAN.md` (pilot plan).

## Protocol

1. **Preflight, then verify keys for real.** `provider_menu_summary()` only checks that env vars exist.
   Before promising a provider, make one free, read-only call (e.g. list models) or confirm a sane
   key length. A placeholder key is a blocker: report it per "Escalate Blockers Explicitly".
2. **Scaffold:** `python scripts/film_studio.py init <kebab-id> --title "<Title>"`, then
   `python -m backlot open <id>`. This writes the canonical OpenMontage layout plus the film bible
   (`01_CONCEPT` … `11_QC_REPORT`) and `production_log.md`.
3. **Run `cinematic` stage by stage**, reading each director skill first. Keep the bible docs in sync
   with the canonical artifacts — the JSON artifact is the contract, the `.md` is the human mirror:
   - research/proposal → `01_CONCEPT.md`, `03_VISUAL_BIBLE.md`, `04_CHARACTER_BIBLE.md`
   - script → `02_SCREENPLAY.md` (professional format, scene IDs `SC01`…)
   - scene_plan → `05_STORYBOARD.md` (shot IDs `SC01_SH001`, one main action per shot)
   - assets → `06_VIDEO_PROMPTS.md`, `07_SOUND_DESIGN.md`, `08_MUSIC_PROMPTS.md`
   - edit → `09_EDITING_PLAN.md`; compose → `11_QC_REPORT.md` + `10_output/`
4. **Log everything** with `python scripts/film_studio.py log <id> "<entry>" --kind <op|file|error|retry|tool|decision|todo>`.

## Continuity Rules (binding)

- Write one **canonical character descriptor** and one **style block** (English) in the bibles; paste
  them verbatim into every prompt. Never paraphrase them between shots.
- Generate and get approval for a **character reference image** before any shot featuring that
  character. Prefer image-to-video from an approved keyframe over text-to-video for character shots.
  Record seeds when the tool supports them.
- Limit face close-ups; favour backs, silhouettes, wide shots and inserts. Each close-up shot is a
  flagged risk in `05_STORYBOARD.md` with a pre-agreed plan B.
- No costume, prop, light-direction or time-of-day change between consecutive shots unless the
  screenplay motivates it — write the motivation in the log.
- Readable text inside a shot (letters, signs) is composed as a typographic insert (Remotion /
  HyperFrames), not generated.

## Sampling Before Batching

Generate the **easiest and the riskiest shot first** (2-shot sample). Show both, get approval, then
batch. Never batch-generate a whole film from untested prompts.

## Failed Shots

Max two prompt-corrected retries per shot, each logged. Then propose (do not apply) a simpler
alternative. Still-image or parallax substitution for a motion shot is a downgrade that requires
approval (AGENT_GUIDE → Motion-Required). Never block the whole film on one shot.

## External MCP Connectors

Session MCP connectors (Runway, Veo, Midjourney, ElevenLabs SFX…) are outside the registry. Use them
only with explicit approval; announce tool + model + cost first; log a `provider_selection` decision;
save outputs under `projects/<id>/assets/...` and record provenance (tool, model, prompt, seed, cost) in
the `asset_manifest`. Check the connector's credit balance before the first paid call.

## QC and Delivery

1. Visual QC per shot: sample frames (`frame_sampler`), look at them, fill the table in
   `11_QC_REPORT.md` (faces, costume continuity, objects, motion, artifacts, light).
2. Technical QC: `python scripts/film_studio.py qc <id> projects/<id>/renders/final.mp4 --preset youtube`
   (exit 1 = critical issue: resolution, fps, A/V drift, silent audio, true peak).
3. Export: `python scripts/film_studio.py export <id> <render> --preset youtube --master [--srt …]`.
   It refuses an aspect-ratio change unless `--fit pad|crop` is passed — check the framing first.
4. The container is ephemeral and `projects/` is gitignored: offer delivery to Dropbox/Google Drive
   (requires approval) before declaring the film delivered.

Never report a file as generated, animated, edited or exported unless the file exists and passed QC.
