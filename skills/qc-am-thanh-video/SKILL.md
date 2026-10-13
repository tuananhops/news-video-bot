---
name: qc-am-thanh-video
description: QC kỹ thuật và nội dung trước khi tải lên: loudness, true peak, dung lượng, contact sheet, tự đánh giá.
---
# QC âm thanh và video

## Kỹ thuật (`scripts/qc.py`, thoát 0 = đạt)
```
python scripts/qc.py work/final.mp4 --asrqc work/asrqc.json --min-sec 40 --max-sec 55
```
- −14 ±0,5 LUFS, true peak ≤ −1 dBTP, < 100 MB, 720×1280, không còn câu ASR lỗi.

## Bằng mắt
```
python scripts/contact_sheet.py work/final.mp4 --out work/contact_sheet.jpg
```
Mở ảnh và kiểm: hook ≤ 2 s có chữ lớn; không 2 cảnh liền cùng loại; ≥ 60% hình thật/chuyển động; chữ không che nhau, không lệch highlight; hình khớp nội dung; có vòng mở, CTA, ghi công giấy phép; không có "chết" khung tĩnh > 3 s ngoài chủ ý.

## Tự đánh giá
Viết `SELF_REVIEW.md` (mẫu `examples/cum-a/SELF_REVIEW.md`): thông số, những gì đã sửa, những gì còn yếu so với video mẫu — nói thật. Không đạt → sửa, không tải lên.
