#!/usr/bin/env bash
# Copies de relecture artistique 540p des masters NON FINAL v4 (lecture seule des masters ; refuse d'écraser).
set -euo pipefail
cd "$(dirname "$0")/../deliverables"
OUT=ARTISTIC_REVIEW_v4_NON_FINAL; mkdir -p $OUT/segments; W=$(mktemp -d)
TAGS="-colorspace smpte170m -color_primaries bt709 -color_trc bt709 -color_range tv"
VENC="-c:v libx264 -preset slow -b:v 750k -profile:v high -pix_fmt yuv420p -r 25 -g 50"
enc(){ # $1 src  $2 out  $3 start_frame  $4 end_frame(excl)
  [ -e "$2" ] && { echo "refus d'écraser $2"; exit 1; }
  F="[0:v]trim=start_frame=$3:end_frame=$4,setpts=PTS-STARTPTS,scale=960:540:flags=lanczos[v]"
  A="[0:a]atrim=start_sample=$(( $3*1920 )):end_sample=$(( $4*1920 )),asetpts=PTS-STARTPTS[a]"
  ffmpeg -nostdin -v error -y -i "$1" -filter_complex "$F" -map "[v]" $VENC -pass 1 -passlogfile $W/p -an -f null /dev/null
  ffmpeg -nostdin -v error -n -i "$1" -filter_complex "$F;$A" -map "[v]" -map "[a]" $VENC -pass 2 -passlogfile $W/p $TAGS \
    -c:a aac -b:a 128k -ar 48000 -ac 2 -movflags +faststart -metadata comment="NON FINAL — relecture artistique, image $3-$(( $4-1 ))" "$2"
  echo "écrit $2"; }
for K in CINEMA SCOLAIRE; do
  SRC=NON_FINAL_v4/LE_CARNET_DE_LA_LIBERTE_${K}_NON_FINAL_v4_1080p.mp4
  enc $SRC $OUT/${K}_v4_REVIEW_540p_NON_FINAL.mp4 0 7475
  i=1; for s in 0 1250 2500 3750 5000 6250; do e=$(( s+1250 > 7475 ? 7475 : s+1250 ))
    enc $SRC $(printf "$OUT/segments/${K}_v4_REVIEW_540p_NON_FINAL_seg%02d_f%04d-%04d.mp4" $i $s $((e-1))) $s $e; i=$((i+1)); done
done
