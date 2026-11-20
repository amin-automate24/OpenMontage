-- LE CARNET DE LA LIBERTE — Phase 2 : prépare le rendu des stems (DX / AMB / FX / MX) en WAV 48 kHz.
-- NON EXÉCUTÉ par l'auteur du paquet. Ce script règle la portée et le nom des fichiers ; le FORMAT (WAV 24 bits) se choisit une fois dans
-- Fichier > Render... (case « WAV », profondeur 24 bits), puis relancer ce script. Les pistes dossiers (DX, AMB, FX, MX) sont rendues en « stems ».
local SR = 48000
reaper.GetSetProjectInfo(0, "RENDER_SETTINGS", 3, true)       -- 3 = stems (pistes sélectionnées)
reaper.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 1, true)      -- 1 = projet entier (régions de test : modifier à 3 pour « time selection »)
reaper.GetSetProjectInfo(0, "RENDER_SRATE", SR, true)
reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 2, true)
reaper.GetSetProjectInfo_String(0, "RENDER_PATTERN", "$track", true)
reaper.GetSetProjectInfo_String(0, "RENDER_FILE", "stems_export", true)  -- dossier relatif au projet
-- sélectionner uniquement les dossiers (bus) DX / AMB / FX / MX
reaper.Main_OnCommand(40297, 0)                                 -- désélectionner toutes les pistes
for i = 0, reaper.CountTracks(0) - 1 do
  local tr = reaper.GetTrack(0, i)
  local _, name = reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "", false)
  local depth = reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH")
  if depth == 1 and (name:match("^DX") or name:match("^AMB") or name:match("^FX") or name:match("^MX")) then reaper.SetTrackSelected(tr, true) end
end
reaper.ShowMessageBox("Rendu préparé : stems DX/AMB/FX/MX, 48 kHz, stéréo, dossier stems_export/.\nOuvrez Fichier > Render pour vérifier le format (WAV 24 bits) puis lancez « Render ».", "Carnet de la liberté", 0)
