-- RETOUR IMMÉDIAT à la version précédente de SH37 : coupe (mute) les items des deux pistes SH37 (plume réelle + delta sélectif). Rien n'est supprimé ni modifié d'autre ;
-- le bruitage de synthèse d'origine revient tel quel. Relancer 08_activer_SH37_version_C.lua pour réactiver.
local dir = debug.getinfo(1, "S").source:gsub("^@", ""):match("^(.*[/\\])")
local C = dofile(dir .. "lib_carnet.lua"); local n = 0
for _, name in ipairs({"AMB SH37 — correction sélective >2,1 kHz (delta)", "FOL SH37 — plume réelle Mixkit 2369"}) do
  local tr = C.find_track(name)
  if tr then for i = 0, reaper.CountTrackMediaItems(tr) - 1 do reaper.SetMediaItemInfo_Value(reaper.GetTrackMediaItem(tr, i), "B_MUTE", 1); n = n + 1 end end
end
reaper.UpdateArrange()
reaper.ShowMessageBox(n .. " item(s) SH37 coupé(s) : version précédente rétablie (bruitage de synthèse d'origine).", "Carnet de la liberté", 0)
