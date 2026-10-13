---
name: tai-len-drive
description: Tải video đã qua QC lên thư mục Drive riêng của chủ; video lỗi chuyển vào thư mục rác, không bao giờ xoá.
---
# Tải lên Drive

- Chỉ tải video **đã qua QC**, vào đúng thư mục chủ chỉ định. Đây là kho riêng, không phải đăng công khai (đăng công khai = DỪNG 2).
- ID thư mục lấy từ cấu hình/biến môi trường: `DRIVE_FOLDER_ID=<DRIVE_FOLDER_ID>`, `DRIVE_TRASH_FOLDER_ID=<TRASH_FOLDER_ID>`. Không ghi ID vào repo.
- Đặt tên `N###_chu-de-ngan.mp4`. File ≥ 100 MB thì nén lại trước.
- Trước khi tải, liệt kê thư mục đích để chắc không tải trùng (tìm kiếm Drive có thể chậm hiện file mới).
- Video lỗi/cũ/trùng: **chuyển** sang thư mục rác (hoặc thư mục con chủ đặt tên), **không xoá**.
- Nếu bot có connector Drive sẵn thì dùng connector; nếu không:
```
python scripts/drive_upload.py upload work/final.mp4 --name N002_ten.mp4
python scripts/drive_upload.py trash <FILE_ID>
```
(thêm `--dry-run` để thử). Ghi kết quả vào `manifest.csv`.
