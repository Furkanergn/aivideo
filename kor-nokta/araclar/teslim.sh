#!/bin/bash
# Kullanım: araclar/teslim.sh <ses.wav> <cikti-adi> <sure-saniye>   (kor-nokta klasöründen; index.html'i render eder)
# Render alır, sesi iki geçişli loudnorm ile -14 LUFS'a getirir, paylaşılabilir boyuta kodlar ve ../teslim/ altına koyar.
set -euo pipefail
W="$1"; AD="$2"; SURE="$3"
mkdir -p renders ../teslim
rm -f "renders/ham-$AD.mp4"
npx -y hyperframes@0.9.78 render -o "renders/ham-$AD.mp4" >/dev/null 2>&1
J=$(ffmpeg -hide_banner -nostats -i "$W" -af loudnorm=I=-14:TP=-3:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
al(){ echo "$J" | python3 -I -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
F=$(python3 -I -c "print($SURE-0.5)")
ffmpeg -y -v error -i "renders/ham-$AD.mp4" -i "$W" -map 0:v -map 1:a -c:v libx264 -preset medium -crf 21 -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-3:LRA=11:measured_I=$(al input_i):measured_TP=$(al input_tp):measured_LRA=$(al input_lra):measured_thresh=$(al input_thresh):offset=$(al target_offset):linear=true,afade=t=out:st=$F:d=0.5" \
  -ar 48000 -c:a aac -b:a 192k -movflags +faststart "../teslim/$AD.mp4"
rm -f "renders/ham-$AD.mp4"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt:format=duration,size -of default=nw=1 "../teslim/$AD.mp4" | tr '\n' ' '; echo
ffmpeg -hide_banner -nostats -i "../teslim/$AD.mp4" -af loudnorm=I=-14:TP=-2:print_format=summary -f null - 2>&1 | grep -E "Input (Integrated|True Peak)"
