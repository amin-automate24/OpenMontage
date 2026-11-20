-- DIAGNOSTIC SH37 version C (lecture seule) : vérifie dans le vrai REAPER les 2 pistes ajoutées, leurs 5 items (positions, vitesses, gains), les médias, l'état muet/actif,
-- et que l'existant n'a pas bougé (piste AMB d'origine : gain d'item et enveloppe). Écrit diagnostic_SH37C.txt à côté du .RPP.
local C = dofile((debug.getinfo(1, "S").source:gsub("^@", ""):match("^(.*[/\\])")) .. "lib_carnet.lua")
local OUT = {}; local function p(s) OUT[#OUT+1] = s end
local function chk(l, got, want, ok) p(string.format("[%s] %s : %s (attendu %s)", ok and "OK  " or "ÉCART", l, tostring(got), tostring(want))) end
local function near(a, b, tol) return math.abs(a - b) <= tol end
local function exists(f) local h = io.open(f, "rb"); if h then h:close() return true end return false end
p("DIAGNOSTIC SH37 version C — REAPER " .. reaper.GetAppVersion())
local amb = C.find_track("AMB SH37 — correction sélective >2,1 kHz (delta)"); local fol = C.find_track("FOL SH37 — plume réelle Mixkit 2369")
chk("Piste AMB SH37 (delta) présente", amb ~= nil, "true", amb ~= nil); chk("Piste FOL SH37 (plume réelle) présente", fol ~= nil, "true", fol ~= nil)
if amb and fol then
  local EXP = {{267.800, 1.00, -16.1}, {268.500, 0.97, -18.1}, {269.200, 1.04, -17.1}, {269.850, 0.99, -20.1}}
  chk("Items sur la piste FOL SH37", reaper.CountTrackMediaItems(fol), 4, reaper.CountTrackMediaItems(fol) == 4)
  local muted = 0
  for i = 0, reaper.CountTrackMediaItems(fol) - 1 do
    local it = reaper.GetTrackMediaItem(fol, i); local tk = reaper.GetActiveTake(it); local pos = reaper.GetMediaItemInfo_Value(it, "D_POSITION"); local e
    for _, x in ipairs(EXP) do if near(pos, x[1], 0.002) then e = x end end
    if not e then chk("Position du geste " .. i, pos, "267,80/268,50/269,20/269,85", false)
    else
      local rate = reaper.GetMediaItemTakeInfo_Value(tk, "D_PLAYRATE"); local vol = 20 * math.log(reaper.GetMediaItemInfo_Value(it, "D_VOL"), 10)
      chk(string.format("Geste à %.2f s : vitesse", pos), string.format("%.2f", rate), string.format("%.2f", e[2]), near(rate, e[2], 0.005))
      chk(string.format("Geste à %.2f s : gain d'item (dB)", pos), string.format("%.1f", vol), string.format("%.1f", e[3]), near(vol, e[3], 0.15))
      local fn = reaper.GetMediaSourceFileName(reaper.GetMediaItemTake_Source(tk), ""); chk(string.format("Geste à %.2f s : média en ligne", pos), exists(fn), "true", exists(fn))
    end
    if reaper.GetMediaItemInfo_Value(it, "B_MUTE") == 1 then muted = muted + 1 end
  end
  chk("Items AMB SH37 (delta)", reaper.CountTrackMediaItems(amb), 1, reaper.CountTrackMediaItems(amb) == 1)
  local d = reaper.GetTrackMediaItem(amb, 0); local fn = reaper.GetMediaSourceFileName(reaper.GetMediaItemTake_Source(reaper.GetActiveTake(d)), ""); chk("Delta : média en ligne", exists(fn), "true", exists(fn))
  chk("Delta : position (s)", reaper.GetMediaItemInfo_Value(d, "D_POSITION"), "267,000", near(reaper.GetMediaItemInfo_Value(d, "D_POSITION"), 267.0, 0.001))
  if reaper.GetMediaItemInfo_Value(d, "B_MUTE") == 1 then muted = muted + 1 end
  p(muted == 0 and "État : SH37 version C ACTIVE (aucun item muet)." or ("État : " .. muted .. " item(s) SH37 muet(s) = version précédente rétablie."))
end
local main = C.find_track("AMB+FOLEY M7c (source mélangée)")
if main then
  local it = reaper.GetTrackMediaItem(main, 0); local vol = 20 * math.log(reaper.GetMediaItemInfo_Value(it, "D_VOL"), 10); chk("Piste AMB d'origine : gain d'item inchangé (dB)", string.format("%.2f", vol), "16,49", near(vol, 16.49, 0.05))
  local env = reaper.GetTrackEnvelopeByName(main, "Volume"); local n = env and reaper.CountEnvelopePoints(env) or 0; chk("Piste AMB d'origine : points d'enveloppe inchangés", n, "≈ 2 760 (2 765 si 06_correction_plume_268 a été lancé)", n == 2760 or n == 2765)
end
local depth = 0; for i = 0, reaper.CountTracks(0) - 1 do depth = depth + reaper.GetMediaTrackInfo_Value(reaper.GetTrack(0, i), "I_FOLDERDEPTH") end; chk("Somme des profondeurs de dossiers", depth, 0, depth == 0)
local _, projfn = reaper.EnumProjects(-1, ""); local path = (projfn and projfn:match("^(.*)[/\\]") or ".") .. "/diagnostic_SH37C.txt"
local f = io.open(path, "w"); if f then f:write(table.concat(OUT, "\n")); f:close() end
local ec = 0; for _, l in ipairs(OUT) do if l:find("^%[ÉCART%]") then ec = ec + 1 end end
reaper.ShowConsoleMsg(table.concat(OUT, "\n") .. "\n"); reaper.ShowMessageBox((ec == 0 and "Aucun écart.\n" or (ec .. " écart(s) — voir la console.\n")) .. "Rapport : " .. path, "Carnet de la liberté — diagnostic SH37C", 0)
