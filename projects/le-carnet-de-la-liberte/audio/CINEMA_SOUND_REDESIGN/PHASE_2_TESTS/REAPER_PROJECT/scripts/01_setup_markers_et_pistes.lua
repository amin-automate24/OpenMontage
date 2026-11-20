-- LE CARNET DE LA LIBERTE — Phase 2 : (re)crée les marqueurs/régions depuis markers.csv et vérifie les pistes.
-- NON EXÉCUTÉ par l'auteur du paquet (REAPER absent de l'environnement de préparation). Idempotent : ne duplique pas un marqueur de même nom et même position.
-- Usage : Actions > Show action list > New action > Load ReaScript... puis exécuter. Le projet doit être enregistré dans ce dossier.
local _, projfn = reaper.EnumProjects(-1, "")
local dir = projfn and projfn:match("^(.*)[/\\]") or ""
local path = dir .. "/markers.csv"
local f = io.open(path, "r")
if not f then reaper.ShowMessageBox("markers.csv introuvable à côté du projet :\n" .. path, "Carnet de la liberté", 0) return end
local existing = {}
local _, nm, nr = reaper.CountProjectMarkers(0)
for i = 0, nm + nr - 1 do
  local _, isrgn, pos, rgnend, name = reaper.EnumProjectMarkers(i)
  existing[string.format("%s|%.3f|%s", name, pos, tostring(isrgn))] = true
end
local added = 0
f:read("*l") -- en-tête
for line in f:lines() do
  local id, name, s, e = line:match('^([^,]*),"?(.-)"?,([%d%.]+),([%d%.]*),')
  if id and name and s then
    local isrgn = (e ~= nil and e ~= "")
    local key = string.format("%s|%.3f|%s", name, tonumber(s), tostring(isrgn))
    if not existing[key] then reaper.AddProjectMarker2(0, isrgn, tonumber(s), isrgn and tonumber(e) or 0, name, -1, 0) added = added + 1 end
  end
end
f:close()
reaper.UpdateTimeline()
reaper.ShowMessageBox(string.format("%d marqueurs/régions ajoutés.\nPistes : %d.", added, reaper.CountTracks(0)), "Carnet de la liberté", 0)
