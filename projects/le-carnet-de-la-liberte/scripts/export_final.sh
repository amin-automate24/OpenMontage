#!/usr/bin/env bash
# Final export: 1920x1080, H.264 (High) + AAC stereo 48 kHz, < 300 s. Usage: export_final.sh VIDEO.mp4 FINAL_MIX.wav OUT.mp4
set -euo pipefail
V="${1:?video}"; A="${2:?audio mix wav}"; O="${3:-LE_CARNET_DE_LA_LIBERTE_FINAL.mp4}"
ffmpeg -y -v error -i "$V" -i "$A" -map 0:v:0 -map 1:a:0 -c:v libx264 -profile:v high -preset slow -crf 16 -pix_fmt yuv420p -r 25 \
  -vf "scale=1920:1080:flags=lanczos,format=yuv420p" -c:a aac -b:a 256k -ar 48000 -ac 2 -shortest -movflags +faststart "$O"
python3 "$(dirname "$0")/check_delivery.py" "$O"
