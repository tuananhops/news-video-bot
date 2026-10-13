---
name: tim-chu-de-tin-tuc
description: Tìm và chấm điểm chủ đề tin tức cho video ngắn tiếng Việt; lọc tin cũ, tin một nguồn, tin trùng.
---
# Tìm chủ đề tin tức

## Bảng điểm (cần ≥ 6/10 mới làm)
| Tiêu chí | Điểm |
|---|---|
| Liên quan trực tiếp Việt Nam / túi tiền người Việt (xăng, vàng, tỷ giá, thời tiết, giao thông, việc làm, công nghệ đang dùng) | +3 |
| Sự kiện thế giới lớn đang nóng 24–48 giờ | +2 |
| Có hình thật mạnh và hợp pháp | +2 |
| Có yếu tố bất ngờ / kỷ lục / mâu thuẫn để làm hook | +2 |
| Có ≥ 2 nguồn uy tín | +1 |
| Khoa học hàn lâm hoặc thể thao xa lạ, không gắn được với người Việt | −3 |

Cơ cấu: ~40% Việt Nam và châu Á, ~40% thế giới đang nóng, ~20% khoa học/công nghệ dễ hiểu gây "wow". Ưu tiên tin "đáng gửi cho người thân" (sức khoẻ, giá cả, thời tiết, lừa đảo).

## Bắt buộc
1. **Độ mới ≤ 2 tuần**, mở bài gốc xem ngày đăng. Số liệu trùng với báo cáo năm trước → xác minh là bản mới.
2. **≥ 2 nguồn uy tín** độc lập (báo lớn, cơ quan chính thức, tạp chí khoa học). Chi tiết chỉ một nguồn yếu nói → bỏ hoặc nói nhẹ đi.
3. **Dedupe ngữ nghĩa** trước khi viết:
   ```
   python scripts/dedupe.py --manifest manifest.csv --id N002 --title "..." --url "..." --entities "tên;nơi;con số" --add
   ```
   Mã thoát 1 = nghi trùng → đọc lý do, nếu cùng sự kiện/ý chính thì bỏ. Không chỉ so tiêu đề.
4. Ghi lại nguồn (URL + ngày) cho bước credits.
