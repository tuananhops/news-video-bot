#!/usr/bin/env bash
# Thử toàn bộ script không cần OmniVoice/whisper: tiếng bíp thay giọng, ảnh test thay ảnh thật.
set -euo pipefail
cd "$(dirname "$0")"; PY=${PYTHON:-python3}; T=$(mktemp -d)
for s in *.py; do [ "$s" = common.py ] || $PY "$s" --help >/dev/null; done; echo "--help: OK"
printf '{"segments":[{"line":"Chỉ năm tuần, số ca tăng hơn bảy lần."},{"line":"Nhưng điều đáng lo nhất lại không phải con số này."},{"line":"Theo dõi để cập nhật tiếp."}]}' > $T/spec.json
$PY tts_lines.py --spec $T/spec.json --out $T --dry-run
$PY concat_voice.py --dir $T
ffmpeg -v error -y -f lavfi -i "sine=frequency=440:duration=5" -ar 48000 $T/tone.wav
$PY loudnorm.py $T/tone.wav $T/tone_n.wav && $PY qc.py $T/tone_n.wav --size none
ffmpeg -v error -y -f lavfi -i "testsrc=size=1600x1000:rate=1" -frames:v 1 $T/img.jpg
printf '{"timeline":"timeline.json","shots":[{"type":"image","src":"img.jpg","seg":0,"text":"TĂNG ×7","credit":"Ảnh: test"},{"type":"stat","seg":1,"big":"779 CA","sub":"tuần 40"},{"type":"image","src":"img.jpg","seg":2,"fx0":0.2,"fx1":0.8}]}' > $T/shots.json
$PY render.py --shots $T/shots.json --spec $T/spec.json --out $T/video.mp4
$PY make_sfx.py --out $T/assets
ffmpeg -v error -y -f lavfi -i "sine=frequency=220:duration=30" $T/assets/music.wav
printf '{"voice":"vo.wav","music":"assets/music.wav","sfx":[{"file":"assets/hit.wav","t":0},{"file":"assets/whoosh.wav","t":1.5}]}' > $T/mix.json
$PY mix.py --config $T/mix.json --video $T/video.mp4 --out $T/final.mp4
$PY qc.py $T/final.mp4 --asrqc $T/asrqc.json
$PY contact_sheet.py $T/final.mp4 --out $T/cs.jpg --cols 3 --rows 2
$PY dedupe.py --manifest $T/m.csv --id N001 --title "Cúm A tăng 7 lần ở Hà Nội" --entities "cúm A;Hà Nội" --add
if $PY dedupe.py --manifest $T/m.csv --title "Cúm A ở Hà Nội tăng mạnh" --entities "Hà Nội;cúm A"; then echo "dedupe FAIL"; exit 1; fi
$PY drive_upload.py --dry-run upload $T/final.mp4
printf '{"0":"chỉ năm tuần số ca tăng hơn bảy lần","1":"nhưng","2":"theo dõi để cập nhật tiếp"}' > $T/hyp.json
$PY asr_check.py --spec $T/spec.json --hyp-json $T/hyp.json
echo "SMOKE TEST: ALL OK ($T)"
