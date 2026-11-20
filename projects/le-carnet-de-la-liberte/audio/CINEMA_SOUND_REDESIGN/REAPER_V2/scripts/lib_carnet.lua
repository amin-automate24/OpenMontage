-- LE CARNET DE LA LIBERTÉ — bibliothèque commune des ReaScripts (REAPER 6/7, Windows). Aucune action destructive :
-- jamais de suppression de piste, d'item ou de fichier ; seules les enveloppes de volume des pistes du projet sont réécrites (DX, AMB, MUS).
-- Les fichiers du paquet sont lus depuis le dossier parent de « scripts/ » (chemins relatifs : media/, manifest/).
local C = {}
local src = debug.getinfo(1, "S").source:gsub("^@", "")
C.SCRIPTS = src:match("^(.*[/\\])") or ""
C.ROOT = C.SCRIPTS:gsub("[/\\]scripts[/\\]$", "/")
C.MEDIA = C.ROOT .. "media/"
C.MAN = C.ROOT .. "manifest/"
C.LOG = {}
function C.log(s) C.LOG[#C.LOG+1] = s; reaper.ShowConsoleMsg(s .. "\n") end

-- Organisation des pistes (clé, nom, profondeur de dossier REAPER : 1 ouvre, 0 normal, -1/-2 ferme 1/2 niveaux)
C.LAYOUT = {
  {"MIXBUS",  "MIX BUS",                                   1},
  {"DXF",     "DX — Dialogues et voix",                    1},
  {"DX",      "DX stem (voix originales)",                -1},
  {"AMBF",    "AMB — Ambiances",                           1},
  {"AMB",     "AMB+FOLEY M7c (source mélangée)",          -1},
  {"FOLF",    "FOL — Foley et bruitages",                  1},
  {"FOL_A",   "FOL test A — carnet + air d'encre",         0},
  {"FOL_B",   "FOL test B — oiseau fenêtre",              -1},
  {"MUSF",    "MUS — Musique",                             1},
  {"MUS",     "MUS thème 599 + générique v2",              0},
  {"MUS_ALT", "MUS générique v2b (respiration)",          -1},
  {"AUXF",    "AUX — Réverbérations",                      1},
  {"AUX_INT", "AUX réverbération intérieur",               0},
  {"AUX_EXT", "AUX réverbération extérieur",              -2},
  {"REFF",    "REF — Références (muettes)",                1},
  {"REF_MIX", "REF mix actuel sans perte",                 0},
  {"REF_MST", "REF master FINAL (audio)",                 -1},
}
C.MUTED_TRACKS = {REFF = true}

-- Traitements (plugins fournis avec REAPER uniquement). bypass=true : ajoutés mais désactivés (à activer et régler à l'écoute).
C.FX = {
  {"DX",      "ReaEQ (Cockos)",    true},
  {"DX",      "ReaComp (Cockos)",  true},
  {"AMB",     "ReaEQ (Cockos)",    true},
  {"MUS",     "ReaEQ (Cockos)",    true},
  {"AUX_INT", "ReaVerbate (Cockos)", false},
  {"AUX_EXT", "ReaVerbate (Cockos)", false},
  {"MIXBUS",  "ReaEQ (Cockos)",    true},
  {"MASTER",  "ReaLimit (Cockos)", false},
  {"MASTER",  "JS: Loudness Meter Peak/RMS/LUFS (Cockos)", false},
}
-- Envois vers les réverbérations (niveau d'envoi en dB ; départs discrets)
C.SENDS = { {"DX", "AUX_INT", -24.0}, {"FOL_A", "AUX_INT", -18.0}, {"FOL_B", "AUX_EXT", -18.0} }

function C.db2lin(d) return 10 ^ (d / 20) end

-- Lecteur CSV minimal (gère les champs entre guillemets contenant des virgules)
function C.parse_line(line)
  local out, field, inq, i = {}, "", false, 1
  while i <= #line do
    local ch = line:sub(i, i)
    if inq then
      if ch == '"' then
        if line:sub(i+1, i+1) == '"' then field = field .. '"'; i = i + 1 else inq = false end
      else field = field .. ch end
    else
      if ch == '"' then inq = true
      elseif ch == "," then out[#out+1] = field; field = ""
      elseif ch ~= "\r" then field = field .. ch end
    end
    i = i + 1
  end
  out[#out+1] = field
  return out
end
function C.read_csv(path)
  local f = io.open(path, "r"); if not f then error("Fichier introuvable : " .. path) end
  local head = C.parse_line(f:read("*l")); local rows = {}
  for line in f:lines() do
    if line:match("%S") then
      local v = C.parse_line(line); local r = {}
      for k, h in ipairs(head) do r[h] = v[k] end
      rows[#rows+1] = r
    end
  end
  f:close(); return rows
end

function C.find_track(name)
  for i = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, i); local _, n = reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "", false)
    if n == name then return tr end
  end
end
function C.track_by_key(key)
  if key == "MASTER" then return reaper.GetMasterTrack(0) end
  for _, L in ipairs(C.LAYOUT) do if L[1] == key then return C.find_track(L[2]) end end
end
-- pistes du manifeste -> clé de piste
C.ITEM_TRACK = {DX="DX", AMB="AMB", MUS="MUS", MUS_ALT="MUS_ALT", FOL_A="FOL_A", FOL_B="FOL_B", REF_MIX="REF_MIX", REF_MST="REF_MST"}

function C.set_project_48k()
  reaper.GetSetProjectInfo(0, "PROJECT_SRATE", 48000, true)
  reaper.GetSetProjectInfo(0, "PROJECT_SRATE_USE", 1, true)
end

function C.create_tracks()
  if reaper.CountTracks(0) > 0 then error("Le projet contient déjà des pistes : ouvrez un projet VIDE (Fichier > Nouveau projet) pour ce script.") end
  for i, L in ipairs(C.LAYOUT) do
    reaper.InsertTrackAtIndex(i - 1, true)
    local tr = reaper.GetTrack(0, i - 1)
    reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", L[2], true)
    reaper.SetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH", L[3])
    if C.MUTED_TRACKS[L[1]] then reaper.SetMediaTrackInfo_Value(tr, "B_MUTE", 1) end
  end
  C.log(string.format("%d pistes créées (DX, AMB, FOL, MUS, AUX dans MIX BUS ; REF muettes hors MIX BUS).", #C.LAYOUT))
end

function C.import_items()
  local n, miss = 0, 0
  for _, r in ipairs(C.read_csv(C.MAN .. "items.csv")) do
    local tr = C.track_by_key(C.ITEM_TRACK[r.track] or r.track)
    local path = C.MEDIA .. r.file
    if not tr then C.log("Piste absente pour " .. r.track) miss = miss + 1
    elseif not reaper.file_exists(path) then C.log("Média manquant : " .. path) miss = miss + 1
    else
      local it = reaper.AddMediaItemToTrack(tr); local tk = reaper.AddTakeToMediaItem(it)
      reaper.SetMediaItemTake_Source(tk, reaper.PCM_Source_CreateFromFile(path))
      reaper.SetMediaItemTakeInfo_Value(tk, "D_STARTOFFS", tonumber(r.source_offset_s))
      reaper.GetSetMediaItemTakeInfo_String(tk, "P_NAME", r.name, true)
      reaper.SetMediaItemInfo_Value(it, "D_POSITION", tonumber(r.position_s))
      reaper.SetMediaItemInfo_Value(it, "D_LENGTH", tonumber(r.length_s))
      reaper.SetMediaItemInfo_Value(it, "D_VOL", C.db2lin(tonumber(r.volume_db)))
      reaper.SetMediaItemInfo_Value(it, "D_FADEINLEN", tonumber(r.fade_in_s))
      reaper.SetMediaItemInfo_Value(it, "D_FADEOUTLEN", tonumber(r.fade_out_s))
      reaper.SetMediaItemInfo_Value(it, "C_FADEINSHAPE", 1); reaper.SetMediaItemInfo_Value(it, "C_FADEOUTSHAPE", 1)
      reaper.SetMediaItemInfo_Value(it, "B_LOOPSRC", 0)
      reaper.SetMediaItemInfo_Value(it, "B_MUTE", tonumber(r.mute))
      n = n + 1
    end
  end
  reaper.Main_OnCommand(40047, 0) -- Peaks: build any missing peaks
  C.log(string.format("%d items importés, %d problème(s).", n, miss))
  return n, miss
end

function C.volume_envelope(tr)
  local env = reaper.GetTrackEnvelopeByName(tr, "Volume")
  if not env then
    reaper.SetOnlyTrackSelected(tr); reaper.Main_OnCommand(40406, 0)  -- Track: Toggle track volume envelope visible (la crée)
    env = reaper.GetTrackEnvelopeByName(tr, "Volume")
  end
  return env
end
function C.apply_envelopes()
  local by = {}
  for _, r in ipairs(C.read_csv(C.MAN .. "envelopes.csv")) do by[r.track] = by[r.track] or {}; table.insert(by[r.track], r) end
  local total = 0
  for key, pts in pairs(by) do
    local tr = C.track_by_key(key)
    if tr then
      local env = C.volume_envelope(tr)
      if env then
        reaper.DeleteEnvelopePointRange(env, -1, 1e9)            -- remplace uniquement les points de CETTE enveloppe (réexécution sans doublon)
        local mode = reaper.GetEnvelopeScalingMode(env)
        for _, p in ipairs(pts) do
          reaper.InsertEnvelopePoint(env, tonumber(p.time_s), reaper.ScaleToEnvelopeMode(mode, tonumber(p.value_linear)), 0, 0, false, true)
        end
        reaper.Envelope_SortPoints(env); total = total + #pts
      else C.log("Enveloppe de volume indisponible pour " .. key) end
    end
  end
  C.log(string.format("%d points d'enveloppe de volume écrits (DX gain par réplique ; AMB gain par plan + ducking ; MUS gain + ducking).", total))
  return total
end

function C.add_markers()
  local have = {}
  local _, nm, nr = reaper.CountProjectMarkers(0)
  for i = 0, nm + nr - 1 do local _, isr, pos, _, name = reaper.EnumProjectMarkers(i); have[string.format("%s|%.3f", name, pos)] = true end
  local added = 0
  for _, r in ipairs(C.read_csv(C.MAN .. "markers.csv")) do
    local s = tonumber(r.Start); local e = tonumber(r.End or "")
    if s and not have[string.format("%s|%.3f", r.Name, s)] then
      reaper.AddProjectMarker2(0, e ~= nil, s, e or 0, r.Name, -1, 0); added = added + 1
    end
  end
  C.log(string.format("%d marqueurs/régions ajoutés (plans, répliques, cartons, régions des tests A/B/C).", added))
  return added
end

-- Règle un paramètre par son NOM (pas d'index supposé) : recherche dichotomique sur la valeur normalisée jusqu'à afficher la valeur voulue (en dB).
function C.set_param_db(tr, fx, pattern, target)
  for p = 0, reaper.TrackFX_GetNumParams(tr, fx) - 1 do
    local _, pname = reaper.TrackFX_GetParamName(tr, fx, p, "")
    if pname:lower():match(pattern) then
      local lo, hi = 0.0, 1.0
      for _ = 1, 40 do
        local mid = (lo + hi) / 2; reaper.TrackFX_SetParamNormalized(tr, fx, p, mid)
        local _, s = reaper.TrackFX_GetFormattedParamValue(tr, fx, p, ""); local v = tonumber((s:gsub(",", ".")):match("-?[%d%.]+"))
        if not v then break end
        if v < target then lo = mid else hi = mid end
      end
      local _, s = reaper.TrackFX_GetFormattedParamValue(tr, fx, p, ""); C.log(string.format("  %s réglé à %s (visé %.1f dB)", pname, s, target)); return true
    end
  end
  C.log("  paramètre « " .. pattern .. " » introuvable : à régler à la main"); return false
end
function C.add_fx()
  local ok, ko = 0, 0
  for _, F in ipairs(C.FX) do
    local tr = C.track_by_key(F[1])
    if tr then
      local names = {F[2]}
      if F[2]:match("^JS: Loudness") then names = {F[2], "JS: Loudness Meter Peak/RMS/LUFS", "loudness_meter"} end
      local idx = -1
      for _, nm in ipairs(names) do if idx < 0 then idx = reaper.TrackFX_AddByName(tr, nm, false, 1) end end   -- 1 = ajoute seulement s'il n'est pas déjà présent
      if idx >= 0 then ok = ok + 1; if F[3] then reaper.TrackFX_SetEnabled(tr, idx, false) end
        if F[2] == "ReaLimit (Cockos)" then C.set_param_db(tr, idx, "threshold", -1.0); C.set_param_db(tr, idx, "ceiling", -1.0) end
      else ko = ko + 1; C.log("Plugin introuvable (ignoré) : " .. F[2]) end
    end
  end
  C.log(string.format("%d traitements en place (EQ/compresseur désactivés par défaut, réverbérations et limiteur actifs), %d introuvable(s).", ok, ko))
  return ok, ko
end

function C.add_sends()
  local n = 0
  for _, S in ipairs(C.SENDS) do
    local a, b = C.track_by_key(S[1]), C.track_by_key(S[2])
    if a and b then
      local exists = false
      for i = 0, reaper.GetTrackNumSends(a, 0) - 1 do
        if reaper.GetTrackSendInfo_Value(a, 0, i, "P_DESTTRACK") == b then exists = true end
      end
      if not exists then local i = reaper.CreateTrackSend(a, b); reaper.SetTrackSendInfo_Value(a, 0, i, "D_VOL", C.db2lin(S[3])); n = n + 1 end
    end
  end
  C.log(string.format("%d envois de réverbération créés.", n))
  return n
end
return C
