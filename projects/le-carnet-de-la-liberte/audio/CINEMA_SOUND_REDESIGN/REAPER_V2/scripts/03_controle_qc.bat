@echo off
REM Contrôle FFmpeg d un export : 03_controle_qc.bat exports\fichier.wav
cd /d "%~dp0.."
python scripts\03_controle_qc.py %1 media\REF_master_FINAL_audio_299s_AAC_decode.flac
pause
