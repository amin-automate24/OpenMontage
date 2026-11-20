-- EXPORT TEST COURT et non destructif : rend UNE fenêtre du MASTER dans exports/ (jamais le master FINAL).
-- Réglez WINDOW puis lancez. A = 30–65 s ; B = 160–190 s ; C = 268–299 s (générique, limiteur et fin). Le rendu se lance seul si REAPER l'accepte ;
-- sinon la boîte « Render » s'ouvre : vérifiez WAV 24 bits, 48 kHz, stéréo puis cliquez Render.
local WINDOW = "C"
local W = {A = {30.0, 65.0}, B = {160.0, 190.0}, C = {268.0, 299.0}}
local w = W[WINDOW]
reaper.GetSetProjectInfo(0, "RENDER_SETTINGS", 0, true)       -- 0 = mix MASTER
reaper.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 0, true)     -- 0 = bornes personnalisées
reaper.GetSetProjectInfo(0, "RENDER_STARTPOS", w[1], true)
reaper.GetSetProjectInfo(0, "RENDER_ENDPOS", w[2], true)
reaper.GetSetProjectInfo(0, "RENDER_SRATE", 48000, true)
reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 2, true)
reaper.GetSetProjectInfo_String(0, "RENDER_FILE", "exports", true)
reaper.GetSetProjectInfo_String(0, "RENDER_PATTERN", string.format("TEST_COURT_%s_%d-%d", WINDOW, w[1], w[2]), true)
reaper.GetSetProjectInfo_String(0, "RENDER_FORMAT", "ZXZhdxgAAAA=", true)   -- WAV 24 bits (valeur codée de REAPER ; à vérifier dans la boîte)
reaper.Main_OnCommand(42230, 0)   -- File: Render project, using the most recent render settings, auto-close render dialog
reaper.ShowMessageBox(string.format("Fenêtre %s (%.0f–%.0f s) rendue dans exports\\TEST_COURT_%s_%d-%d.wav.\nSi rien n'a été écrit : File > Render… (réglages déjà remplis), WAV 24 bits, Render.\nContrôle : glissez le WAV sur scripts\\03_controle_qc.bat", WINDOW, w[1], w[2], WINDOW, w[1], w[2]), "Carnet de la liberté", 0)
