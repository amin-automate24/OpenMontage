-- DIAGNOSTIC — à lancer dans le VRAI REAPER après ouverture du projet (et script 01). Lecture seule : ne modifie rien.
-- Écrit diagnostic_reaper.txt à côté du .RPP, avec les valeurs ATTENDUES et le verdict OK/ÉCART pour chaque contrôle.
local OUT = {}
local function p(s) OUT[#OUT+1] = s end
local function chk(label, got, want, ok) p(string.format("[%s] %s : %s (attendu %s)", ok and "OK  " or "ÉCART", label, tostring(got), tostring(want))) end
local function exists(path) local f = io.open(path, "rb"); if f then f:close() return true end return false end
p("DIAGNOSTIC REAPER — LE CARNET DE LA LIBERTÉ v2")
p("REAPER " .. reaper.GetAppVersion() .. " | OS " .. reaper.GetOS())
local _, projfn = reaper.EnumProjects(-1, ""); p("Projet : " .. tostring(projfn))
local sr = reaper.GetSetProjectInfo(0, "PROJECT_SRATE", 0, false); chk("Fréquence d'échantillonnage projet (0 = réglage global du périphérique)", sr, "48000", sr == 48000)
local nt = reaper.CountTracks(0); chk("Nombre de pistes", nt, 17, nt == 17)
local depth = 0; local names = {}
for i = 0, nt - 1 do
  local tr = reaper.GetTrack(0, i); local _, n = reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "", false)
  depth = depth + reaper.GetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH"); names[i] = n
  local ni = reaper.CountTrackMediaItems(tr); local mute = reaper.GetMediaTrackInfo_Value(tr, "B_MUTE") == 1
  local env = reaper.GetTrackEnvelopeByName(tr, "Volume"); local pts = env and reaper.CountEnvelopePoints(env) or 0
  local fx = {}; for f = 0, reaper.TrackFX_GetCount(tr) - 1 do local _, fn = reaper.TrackFX_GetFXName(tr, f, ""); fx[#fx+1] = fn .. (reaper.TrackFX_GetEnabled(tr, f) and "" or " [désactivé]") end
  p(string.format("  piste %02d  %-42s items=%d  muette=%s  points_vol=%d  envois=%d  FX={%s}", i + 1, n, ni, tostring(mute), pts, reaper.GetTrackNumSends(tr, 0), table.concat(fx, "; ")))
end
chk("Somme des profondeurs de dossiers (doit revenir à 0)", depth, 0, depth == 0)
local nitems, offline, bad = 0, 0, {}
for i = 0, reaper.CountMediaItems(0) - 1 do
  local it = reaper.GetMediaItem(0, i); local tk = reaper.GetActiveTake(it); nitems = nitems + 1
  if tk then local src = reaper.GetMediaItemTake_Source(tk); local fn = reaper.GetMediaSourceFileName(src, ""); local len = reaper.GetMediaSourceLength(src)
    if not exists(fn) or len <= 0 then offline = offline + 1; bad[#bad+1] = fn end end
end
chk("Items", nitems, 12, nitems == 12); chk("Médias hors ligne (introuvables ou longueur nulle)", offline, 0, offline == 0); for _, b in ipairs(bad) do p("   manquant : " .. b) end
local _, nm, nr = reaper.CountProjectMarkers(0); chk("Marqueurs", nm, 73, nm == 73); chk("Régions (tests A/B/C)", nr, 3, nr == 3); chk("Total marqueurs + régions", nm + nr, 76, nm + nr == 76)
local function allitemsmuted(sub)
  for i = 0, nt - 1 do if names[i]:find(sub, 1, true) then local tr = reaper.GetTrack(0, i); local n = reaper.CountTrackMediaItems(tr)
    for k = 0, n - 1 do if reaper.GetMediaItemInfo_Value(reaper.GetTrackMediaItem(tr, k), "B_MUTE") ~= 1 then return false end end return n > 0 end end
end
for _, s in ipairs({"FOL test A", "FOL test B"}) do local m = allitemsmuted(s); chk("Test désactivé par défaut (item muet) : " .. s, m, "true", m == true) end
-- items muets des tests A/B/générique v2b (le mute est porté par l'item)
local muted = 0; for i = 0, reaper.CountMediaItems(0) - 1 do if reaper.GetMediaItemInfo_Value(reaper.GetMediaItem(0, i), "B_MUTE") == 1 then muted = muted + 1 end end
chk("Items muets (A, B, v2b, 2 REF)", muted, 5, muted == 5)
-- master
local mt = reaper.GetMasterTrack(0); local mf = {}
for f = 0, reaper.TrackFX_GetCount(mt) - 1 do local _, fn = reaper.TrackFX_GetFXName(mt, f, ""); mf[#mf+1] = fn
  for pi = 0, reaper.TrackFX_GetNumParams(mt, f) - 1 do local _, pn = reaper.TrackFX_GetParamName(mt, f, pi, ""); if fn:find("ReaLimit") and (pn:lower():find("threshold") or pn:lower():find("ceiling")) then local _, v = reaper.TrackFX_GetFormattedParamValue(mt, f, pi, ""); p("   ReaLimit " .. pn .. " = " .. v) end end
end
p("FX du MASTER : " .. table.concat(mf, "; ")); local hasLim = false; for _, f in ipairs(mf) do if f:find("ReaLimit") then hasLim = true end end; chk("Limiteur ReaLimit sur le MASTER", hasLim, "true", hasLim)
local hasMeter = false; for _, f in ipairs(mf) do if f:lower():find("loudness") then hasMeter = true end end; chk("Vumètre de sonie sur le MASTER (facultatif)", hasMeter, "true", hasMeter)
-- plugins natifs : disponibilité réelle (sans rien instancier de façon permanente)
for _, nm_ in ipairs({"ReaEQ (Cockos)", "ReaComp (Cockos)", "ReaVerbate (Cockos)", "ReaLimit (Cockos)"}) do
  local tr = reaper.GetTrack(0, 0); local idx = reaper.TrackFX_AddByName(tr, nm_, false, 0); chk("Plugin natif disponible : " .. nm_, idx >= 0 and "trouvé (déjà présent)" or "non instancié (voir pistes)", "trouvé ou présent sur une piste", true)
end
local path = (projfn and projfn:match("^(.*)[/\\]") or ".") .. "/diagnostic_reaper.txt"
local f = io.open(path, "w"); if f then f:write(table.concat(OUT, "\n")); f:close() end
local ecarts = 0; for _, l in ipairs(OUT) do if l:find("^%[ÉCART%]") then ecarts = ecarts + 1 end end
p("Rapport écrit : " .. path .. " | écarts : " .. ecarts)
reaper.ShowConsoleMsg(table.concat(OUT, "\n") .. "\n")
reaper.ShowMessageBox((ecarts == 0 and "Aucun écart.\n" or (ecarts .. " écart(s) — voir la console REAPER.\n")) .. "Rapport : " .. path .. "\nEnvoyez-moi ce fichier.", "Carnet de la liberté — diagnostic", 0)
