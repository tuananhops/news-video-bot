# scripts/ — Công cụ dòng lệnh

## Cài đặt
```bash
sudo apt-get install -y ffmpeg fonts-dejavu-core      # ffmpeg >= 5, có loudnorm
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
# OmniVoice (venv riêng nếu muốn, CPU chạy được):
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install omnivoice            # hoặc cài từ mã nguồn k2-fsa/OmniVoice theo README của dự án
# Lần đầu chạy faster-whisper sẽ tự tải model "small".
```
Font tiếng Việt: tải Be Vietnam Pro (OFL) và khai báo đường dẫn ở `shots.json` → `font`.

## Các script (đều có `--help`)
| Script | Việc |
|---|---|
| `tts_lines.py` | Tạo giọng OmniVoice từng câu + kiểm ASR + thử lại (`--dry-run` để thử không cần model) |
| `asr_check.py` | So lời nhận dạng với kịch bản (`--hyp-json` để test không cần model) |
| `concat_voice.py` | Nối câu → `vo.wav` + `timeline.json` |
| `loudnorm.py` | Chuẩn hoá −14 LUFS / TP −1,5 dBTP (2 lượt) |
| `render.py` | Dựng video 9:16 từ `shots.json` (Ken Burns, thẻ số, phụ đề) |
| `make_sfx.py` | Tự tạo SFX whoosh/ding/hit/riser |
| `mix.py` | Trộn giọng + nhạc (ducking) + SFX, chuẩn hoá, ghép video |
| `qc.py` | QC loudness, TP, dung lượng, độ phân giải, thời lượng, ASR |
| `contact_sheet.py` | Lưới khung hình để soát bằng mắt |
| `dedupe.py` | Kiểm trùng chủ đề theo URL + thực thể + tiêu đề với `manifest.csv` |
| `drive_upload.py` | Tải lên / chuyển vào thư mục rác qua biến môi trường (`--dry-run`) |

## Chạy một video
```bash
W=work/N002; mkdir -p $W   # đặt spec.json, shots.json, mix.json, assets/ vào đây
python scripts/tts_lines.py --spec $W/spec.json --out $W --voice-prompt <voice_prompt.pt>
python scripts/concat_voice.py --dir $W && python scripts/loudnorm.py $W/vo.wav $W/voN.wav
python scripts/render.py --shots $W/shots.json --spec $W/spec.json --out $W/video.mp4
python scripts/mix.py --config $W/mix.json --video $W/video.mp4 --out $W/final.mp4
python scripts/qc.py $W/final.mp4 --asrqc $W/asrqc.json && python scripts/contact_sheet.py $W/final.mp4 --out $W/contact_sheet.jpg
```
Chỉ chạy một tác vụ nặng (TTS/render) tại một thời điểm.

## Thử nhanh không cần model
```bash
bash scripts/smoke_test.sh
```
