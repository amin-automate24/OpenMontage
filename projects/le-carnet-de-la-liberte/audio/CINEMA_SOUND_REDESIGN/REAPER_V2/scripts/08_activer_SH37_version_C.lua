-- SH37 VERSION C (choix artistique) — ajoute ou ACTIVE : 1) piste « FOL SH37 — plume réelle » (4 gestes Mixkit 2369) ; 2) piste « AMB SH37 — correction sélective » (couche delta qui retire seulement la bande > 2,1 kHz de l'ambiance, 267,45–270,50 s).
-- N'altère aucun item, aucune enveloppe, aucun gain existants. Idempotent. Si vous avez ouvert LE_CARNET_SOUND_V2_SH37C.RPP, les pistes existent déjà : ce script ne fait que les DÉMUTER.
-- Retour immédiat à la version précédente : scripts/09_retour_version_precedente_SH37.lua (mute) ou ouvrir LE_CARNET_SOUND_V2.RPP (inchangé).
local dir = debug.getinfo(1, "S").source:gsub("^@", ""):match("^(.*[/\\])")
local C = dofile(dir .. "lib_carnet.lua")
local AMB_NAME, FOLB_NAME = "AMB+FOLEY M7c (source mélangée)", "FOL test B — oiseau fenêtre"
local NEW = {AMB_SH37 = {"AMB SH37 — correction sélective >2,1 kHz (delta)", AMB_NAME}, FOL_SH37 = {"FOL SH37 — plume réelle Mixkit 2369", FOLB_NAME}}
local function ensure_track(key)
  local name, after_name = NEW[key][1], NEW[key][2]
  local tr = C.find_track(name); if tr then return tr, false end
  local after = C.find_track(after_name); if not after then error("Piste introuvable : " .. after_name .. " (ouvrez le projet v2)") end
  local idx = math.floor(reaper.GetMediaTrackInfo_Value(after, "IP_TRACKNUMBER"))          -- numéro 1-based de la piste « après » = index 0-based de l'insertion
  local d = reaper.GetMediaTrackInfo_Value(after, "I_FOLDERDEPTH")
  reaper.InsertTrackAtIndex(idx, true); tr = reaper.GetTrack(0, idx)
  reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", name, true)
  reaper.SetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH", d)                                   -- la nouvelle piste devient la dernière du dossier
  if d < 0 then reaper.SetMediaTrackInfo_Value(after, "I_FOLDERDEPTH", 0) end
  return tr, true
end
local function has_item(tr, nm) for i = 0, reaper.CountTrackMediaItems(tr) - 1 do local it = reaper.GetTrackMediaItem(tr, i); local tk = reaper.GetActiveTake(it); if tk then local _, n = reaper.GetSetMediaItemTakeInfo_String(tk, "P_NAME", "", false); if n == nm then return it end end end end
reaper.Undo_BeginBlock(); reaper.PreventUIRefresh(1)
local added, unmuted, miss = 0, 0, 0
local tracks = {AMB_SH37 = ensure_track("AMB_SH37"), FOL_SH37 = ensure_track("FOL_SH37")}
for _, r in ipairs(C.read_csv(C.MAN:gsub("manifest[/\\]$", "manifest_sh37c/") .. "items_sh37c.csv")) do
  local tr = tracks[r.track_key]; local path = C.MEDIA .. r.file; local it = has_item(tr, r.name)
  if not it then
    if not reaper.file_exists(path) then C.log("Média manquant : " .. path); miss = miss + 1
    else
      it = reaper.AddMediaItemToTrack(tr); local tk = reaper.AddTakeToMediaItem(it)
      reaper.SetMediaItemTake_Source(tk, reaper.PCM_Source_CreateFromFile(path))
      reaper.SetMediaItemTakeInfo_Value(tk, "D_STARTOFFS", tonumber(r.source_offset_s)); reaper.SetMediaItemTakeInfo_Value(tk, "D_PLAYRATE", tonumber(r.playrate)); reaper.SetMediaItemTakeInfo_Value(tk, "B_PPITCH", 0)
      reaper.GetSetMediaItemTakeInfo_String(tk, "P_NAME", r.name, true)
      reaper.SetMediaItemInfo_Value(it, "D_POSITION", tonumber(r.position_s)); reaper.SetMediaItemInfo_Value(it, "D_LENGTH", tonumber(r.length_s)); reaper.SetMediaItemInfo_Value(it, "D_VOL", C.db2lin(tonumber(r.volume_db)))
      reaper.SetMediaItemInfo_Value(it, "D_FADEINLEN", tonumber(r.fade_in_s)); reaper.SetMediaItemInfo_Value(it, "D_FADEOUTLEN", tonumber(r.fade_out_s)); reaper.SetMediaItemInfo_Value(it, "C_FADEINSHAPE", 1); reaper.SetMediaItemInfo_Value(it, "C_FADEOUTSHAPE", 1); reaper.SetMediaItemInfo_Value(it, "B_LOOPSRC", 0)
      added = added + 1
    end
  end
  if it and reaper.GetMediaItemInfo_Value(it, "B_MUTE") == 1 then reaper.SetMediaItemInfo_Value(it, "B_MUTE", 0); unmuted = unmuted + 1 end
end
reaper.Main_OnCommand(40047, 0); reaper.PreventUIRefresh(-1); reaper.UpdateArrange(); reaper.Undo_EndBlock("Carnet de la liberté : SH37 version C", -1)
reaper.ShowMessageBox(string.format("SH37 version C active : %d item(s) ajouté(s), %d démuté(s), %d problème(s).\nRetour immédiat : scripts\\09_retour_version_precedente_SH37.lua", added, unmuted, miss), "Carnet de la liberté", 0)
