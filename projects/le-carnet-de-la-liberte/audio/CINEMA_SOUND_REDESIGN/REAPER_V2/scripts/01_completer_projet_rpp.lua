-- À lancer après l'ouverture de LE_CARNET_SOUND_V2.RPP : ajoute ce que le fichier .RPP ne porte pas
-- (enveloppes de volume, traitements, envois) et les marqueurs manquants. Réexécutable sans doublon.
local dir = debug.getinfo(1, "S").source:gsub("^@", ""):match("^(.*[/\\])")
local C = dofile(dir .. "lib_carnet.lua")
reaper.Undo_BeginBlock(); reaper.PreventUIRefresh(1)
C.set_project_48k(); C.apply_envelopes(); C.add_markers(); C.add_fx(); C.add_sends()
reaper.PreventUIRefresh(-1); reaper.UpdateArrange(); reaper.Undo_EndBlock("Carnet de la liberté : automatisations et traitements", -1)
reaper.ShowMessageBox(table.concat(C.LOG, "\n"), "Carnet de la liberté — projet complété", 0)
