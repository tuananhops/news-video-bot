# news-video-bot

Gói "bộ não" cho một bot AI sản xuất **video tin tức ngắn tiếng Việt khổ 9:16** (TikTok/Reels/Shorts), tập trung **giữ chân người xem**: cách chọn tin, viết kịch bản có hook và vòng mở, dựng hình hợp pháp, lồng giọng clone OmniVoice có kiểm ASR, QC âm thanh và tải lên Drive — kèm quy tắc, bài học từ lỗi cũ và script dòng lệnh.

## Giao cho bot mới
> **clone repo rồi bảo bot đọc AGENTS.md**

```bash
git clone <URL_REPO> && cd news-video-bot
```
Rồi nói với bot: "Đọc AGENTS.md và làm theo." Bot sẽ đọc `skills/`, `rules.md`, `examples/` và làm video mẫu đầu tiên để bạn duyệt trước khi làm hàng loạt.

Bạn cần tự cung cấp (không có trong repo): file giọng mẫu bạn có quyền dùng, ID thư mục Drive (biến môi trường), quyền truy cập Drive.

## Cấu trúc
```
.
├── AGENTS.md / CLAUDE.md    # chỉ dẫn cho bot (giống hệt nhau)
├── rules.md                 # quy tắc, cài đặt, lỗi & bài học, ghi chú công cụ
├── skills/                  # 6 skill: tìm chủ đề, kịch bản, dựng, giọng, QC, Drive
├── scripts/                 # CLI: tts_lines, asr_check, concat_voice, loudnorm, render, mix,
│                            #      make_sfx, qc, contact_sheet, dedupe, drive_upload, smoke_test.sh
├── examples/cum-a/          # video mẫu đã duyệt: kịch bản, shot list, mix, credits, tự đánh giá
├── requirements.txt
└── .gitignore
```
Cài đặt và chạy thử: xem `scripts/README.md` (`bash scripts/smoke_test.sh`).
