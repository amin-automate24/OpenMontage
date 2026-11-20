-- Prépare le rendu (non destructif) : mix complet du MASTER 0–299 s, WAV 48 kHz stéréo, dans le sous-dossier exports/.
-- Choisir une seule fois le format WAV 24 bits dans Fichier > Render…, puis « Render ». Pour les stems, mettre STEMS = true.
local STEMS = false
reaper.GetSetProjectInfo(0, "RENDER_SETTINGS", STEMS and 2 or 0, true)   -- 0 = master ; 2 = stems des pistes sélectionnées uniquement
reaper.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 0, true)                 -- 0 = bornes personnalisées ci-dessous
reaper.GetSetProjectInfo(0, "RENDER_STARTPOS", 0, true)
reaper.GetSetProjectInfo(0, "RENDER_ENDPOS", 299.0, true)
reaper.GetSetProjectInfo(0, "RENDER_SRATE", 48000, true)
reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 2, true)
reaper.GetSetProjectInfo_String(0, "RENDER_FILE", "exports", true)
reaper.GetSetProjectInfo_String(0, "RENDER_PATTERN", STEMS and "STEM_$track" or "LE_CARNET_MIX_V2_$project", true)
if STEMS then
  reaper.Main_OnCommand(40297, 0)   -- désélectionner toutes les pistes
  for i = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, i); local _, n = reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "", false)
    if n:match("^DX —") or n:match("^AMB —") or n:match("^FOL —") or n:match("^MUS —") or n:match("^AUX —") then reaper.SetTrackSelected(tr, true) end
  end
end
reaper.ShowMessageBox("Rendu préparé : " .. (STEMS and "stems DX/AMB/FOL/MUS/AUX" or "mix MASTER") .. ", 0–299 s, 48 kHz, stéréo, dossier exports/.\nOuvrez Fichier > Render… : vérifiez WAV 24 bits, puis Render.\nContrôle ensuite : scripts\\03_controle_qc.bat exports\\<fichier>.wav", "Carnet de la liberté", 0)
