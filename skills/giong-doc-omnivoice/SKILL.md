---
name: giong-doc-omnivoice
description: Lồng tiếng bằng giọng clone OmniVoice, tạo từng câu, kiểm bằng ASR và tạo lại câu lỗi.
---
# Giọng đọc OmniVoice

## Nguyên tắc
- Chỉ dùng giọng mẫu chủ cung cấp và xác nhận có quyền dùng (DỪNG 5 nếu cần giọng mới).
- **Không batch.** Tạo từng câu riêng (batch từng ra tiếng lảm nhảm và lặp vòng).
- Seed cố định (1234) cho lượt đầu; lỗi thì seed + 101×lần, step 16 → 32; tối đa 3 lần thử lại.
- Cắt lặng đầu/cuối, nén khoảng lặng trong câu ≤ 0,3 s, đệm 0,15 s giữa câu → đọc liền mạch.
- Kiểm ASR (faster-whisper `small`, tiếng Việt): đạt khi phủ ≥ 50% từ kịch bản và tỉ lệ độ dài 0,6–1,5. Số được bỏ qua khi so.
- Câu vẫn lỗi sau 3 lần: viết lại câu (đổi từ khó, ví dụ đổi tên riêng thành mô tả) rồi tạo lại. Nghe lại từ khó.

## Lệnh
```
python scripts/tts_lines.py --spec work/spec.json --out work --voice-prompt <voice_prompt.pt>
python scripts/concat_voice.py --dir work
python scripts/loudnorm.py work/vo.wav work/voN.wav
```
Thử đường ống không cần model: thêm `--dry-run`. Tạo `voice_prompt.pt` một lần từ giọng mẫu theo tài liệu OmniVoice, không đưa vào git.
