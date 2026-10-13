# rules.md — Quy tắc công việc, cài đặt, bài học

## 1. Quy tắc bắt buộc
1. **Giọng đọc:** giọng nam clone (OmniVoice) từ file giọng chủ cung cấp và đã xác nhận có quyền dùng. Trong trẻo, rõ chữ, đọc liền mạch không ngắt vụn. Dùng xuyên suốt mọi video.
2. **Mỗi video một chủ đề riêng**, không trùng nội dung với bất kỳ video nào đã làm (kiểm theo URL, thực thể, ý chính — không chỉ tiêu đề).
3. **Không bịa sự thật.** Mọi số liệu, trích dẫn phải có nguồn. Cảnh tái hiện/minh hoạ phải ghi rõ chữ **"VÍ DỤ MINH HOẠ"** trên khung.
4. **Chỉ học phong cách** của kênh tham khảo. Không dùng cảnh quay, nhạc, giọng, logo, khuôn mặt của họ; không reupload.
5. **Không đăng ở đâu** (mạng xã hội, công khai) khi chưa được chủ duyệt. Tải lên thư mục Drive riêng chủ đã chỉ định thì được.
6. **Chỉ một tác vụ render/TTS nặng tại một thời điểm.** Chỉ một tiến trình sản xuất chạy; dùng file khoá (lock).
7. **Âm thanh:** −14 LUFS (±0,5), true peak ≤ −1 dBTP; nhạc nền khoảng −24 đến −28 LUFS dưới giọng, có ducking.
8. **Video:** 720×1280, 40–55 giây (kiểu mới), file < 100 MB.
9. **Video hỏng/cũ: chuyển vào thư mục rác**, không xoá.
10. **Dừng ở ngưỡng mức sử dụng chủ đặt**; khi chủ bảo dừng thì dừng ngay (tạo file `STOP`).
11. **Câu yếu hoặc chỉ một nguồn:** cắt hoặc viết lại cho đúng với nguồn uy tín ("lần đầu tiên", "kỷ lục" chỉ dùng khi ≥ 2 nguồn xác nhận).
12. **Kiểm tra ngày đăng** của nguồn: tin ≤ 2 tuần; con số trùng với báo cáo cũ thì phải xác minh là bản mới.
13. Ảnh thật phải đúng chủ đề; không dùng ảnh stock lạc đề. Không có hình hợp pháp → bỏ tin.
14. Thẻ nền đen ô đỏ tối đa 3 lần mỗi video; không để 2 cảnh liền nhau cùng loại.
15. Không đưa thông tin cá nhân, mật khẩu, khoá truy cập, link riêng vào repo hay video.

## 2. Cài đặt bắt buộc
- ffmpeg/ffprobe (có loudnorm, sidechaincompress, zoompan).
- Python 3.10+, `requirements.txt`; OmniVoice (torch, CPU chạy được) trong venv riêng; faster-whisper model `small`, int8.
- Font tiếng Việt đủ dấu (ví dụ Be Vietnam Pro, OFL) — khai báo đường dẫn trong `shots.json`.
- Dữ liệu bản đồ Natural Earth (public domain).

## 3. Lỗi đã mắc và bài học
| Lỗi | Bài học |
|---|---|
| Tạo giọng OmniVoice cả loạt câu một lần → ra tiếng lảm nhảm, lặp vòng | Tạo **từng câu riêng**, seed cố định, kiểm ASR từng câu, tạo lại tối đa 3 lần với seed khác/nhiều step hơn |
| Giọng gTTS, Piper, MMS bị chủ chê | Dùng giọng clone chủ duyệt; không tự đổi giọng |
| edge-tts trả 403 từ server | Không phụ thuộc dịch vụ TTS online không chính thức |
| File video đầu tiên > 200 MB | Nén CRF 21–23, 720p; kiểm < 100 MB trước khi tải |
| Chủ đề trùng lọt qua (v37/v120/v294, v122/v287, v118/v270, v153/v272) | Dedupe theo **URL + thực thể** (tên, nơi, con số), không chỉ tiêu đề; soát lại cả kho định kỳ |
| Nghi tin cũ (WWF 73%, LUNAR) | Luôn mở nguồn xem **ngày đăng**; con số giống báo cáo cũ phải xác minh |
| Câu "danh hiệu quốc tế đầu tiên" (Hồng Kông) chỉ một trang yếu nói | Cắt hoặc viết lại theo nguồn uy tín, thay video, bản cũ vào rác |
| Hai lượt chạy song song tranh nhau → tải trùng | Một tiến trình sản xuất duy nhất + file khoá; kiểm thư mục đích trước khi tải |
| Mẫu thẻ đen chỉ có chữ bị chủ gọi là "chết não", chán | **Giữ chân trước tiên**: hình thật, chuyển động, hook, vòng mở, nhịp đa dạng |
| Ảnh stock lạc đề (ảnh tiêm phòng hải quân Mỹ cho tin Hà Nội) | Hình phải khớp nội dung câu đang đọc |
| ASR nghe "cúm A" thành "cung à", "co giật" thành "có dật" | Đổi seed tạo lại; nếu vẫn lỗi thì đổi cách viết/câu |

## 4. Ghi chú công cụ và web
- **Google Drive:** mỗi file tải lên < 100 MB (giới hạn của công cụ tải đang dùng). Thư mục đích lấy từ cấu hình (`<DRIVE_FOLDER_ID>`), không gõ cứng. Tìm kiếm Drive có thể chậm hiện file mới — kiểm trực tiếp bằng liệt kê thư mục.
- **Pixabay, Freesound:** trả 403 khi truy cập từ server → dùng Wikimedia Commons hoặc SFX tự tổng hợp (`scripts/make_sfx.py`).
- **YouTube Audio Library:** cần đăng nhập → không tự động được; nhờ chủ tải nếu muốn.
- **Wikimedia Commons:** mỗi file một giấy phép. PD dùng tự do; CC BY/BY-SA phải ghi tác giả + giấy phép (trên khung và caption); tránh NC/ND. Ảnh chính phủ Mỹ (CDC, NASA, DoD) là public domain, nhưng không dùng logo để ngụ ý bảo trợ.
- **Ảnh báo chí (AP, Reuters, Getty):** có bản quyền; chỉ xuất hiện trong ảnh chụp trang báo kèm "Nguồn".
- **Nhạc TikTok thương mại:** chỉ cho tài khoản cá nhân, không cho tài khoản doanh nghiệp.
