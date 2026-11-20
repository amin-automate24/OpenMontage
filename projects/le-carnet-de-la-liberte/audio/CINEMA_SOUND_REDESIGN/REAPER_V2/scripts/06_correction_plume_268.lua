-- CORRECTION MINIMALE du crépitement 268–270,3 s (bruitage de synthèse « plume », piste AMB). À lancer dans le projet déjà construit.
-- Réécrit UNIQUEMENT l'enveloppe de volume de la piste « AMB+FOLEY M7c » à partir de manifest/envelopes_correction_268.csv (creux de −20 dB entre 267,45 et 270,65 s).
-- Rien d'autre n'est touché (DX, MUS, items, FX, envois). Pour revenir en arrière : relancer scripts/01_completer_projet_rpp.lua (rétablit envelopes.csv).
local dir = debug.getinfo(1, "S").source:gsub("^@", ""):match("^(.*[/\\])")
local C = dofile(dir .. "lib_carnet.lua")
reaper.Undo_BeginBlock()
local n = C.apply_envelopes("envelopes_correction_268.csv")
reaper.UpdateArrange(); reaper.Undo_EndBlock("Carnet de la liberté : correction plume 268 s", -1)
reaper.ShowMessageBox(string.format("Correction appliquée : %d points d'enveloppe réécrits sur la piste AMB (creux −20 dB, 267,45–270,65 s).\nRelancez 05_export_test_court.lua (fenêtre C) pour mesurer.", n), "Carnet de la liberté", 0)
