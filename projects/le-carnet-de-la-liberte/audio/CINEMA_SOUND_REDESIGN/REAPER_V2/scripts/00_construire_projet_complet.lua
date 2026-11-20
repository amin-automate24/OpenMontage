-- Construit TOUT le projet dans un projet REAPER VIDE (Fichier > Nouveau projet, puis Enregistrer sous… dans ce dossier REAPER_V2).
-- Étapes : 48 kHz, pistes et bus, import et placement des médias, enveloppes de volume, marqueurs, traitements, envois.
local dir = debug.getinfo(1, "S").source:gsub("^@", ""):match("^(.*[/\\])")
local C = dofile(dir .. "lib_carnet.lua")
reaper.Undo_BeginBlock(); reaper.PreventUIRefresh(1)
C.set_project_48k(); C.create_tracks(); C.import_items(); C.apply_envelopes(); C.add_markers(); C.add_fx(); C.add_sends()
reaper.PreventUIRefresh(-1); reaper.UpdateArrange(); reaper.Undo_EndBlock("Carnet de la liberté : construire le projet", -1)
reaper.ShowMessageBox(table.concat(C.LOG, "\n"), "Carnet de la liberté — projet construit", 0)
