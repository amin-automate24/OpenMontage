# Normalisation des niveaux vocaux — DaVinci Resolve Free / Fairlight (plan, non appliqué)

Objectif : voix homogènes entre personnages (Younes, Amina, père, maîtresse, mère) avant mixage ; cible livraison cohérente avec le mix local FFmpeg (−16 LUFS intégrés, crête ≤ −1,5 dBFS).

1. **Import** : un fichier par réplique (`audio/voices_final/<KEY>.wav`) sur pistes dialogue séparées par personnage. Originaux jamais écrasés.
2. **Par clip** : Clip Attributes > Normalize Audio Levels, mode loudness (ITU-R BS.1770 / EBU R128 si proposé, sinon True Peak), cible −23 LUFS ou −18 dBFS crête de travail, pour égaliser avant bus. Ensuite ajustement manuel ±2 dB à l'écoute (voix d'enfant plus aiguë).
3. **Par piste** : gain de piste par personnage (Y vs A) pour que Younes et Amina soient perçus au même niveau ; EQ léger (coupe-bas 80 Hz) et de-esser si besoin.
4. **Bus Dialogues** : Loudness Meter (Fairlight > Meters) sur le bus ; limiteur −1,5 dBTP ; viser −16 LUFS intégrés sur le film complet 276 s.
5. **Ambiances/musique** : ducking −9 dB sous les dialogues (comme `assemble_audio.py`), bus séparé.
6. **Contrôle final** : lecture complète, puis comparaison avec `audio/MIX_276s.wav` (−16,9 LUFS / −1,5 dBFS mesurés sur le mix test). Fichiers et EDL existants inchangés.
