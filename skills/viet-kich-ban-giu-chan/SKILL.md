---
name: viet-kich-ban-giu-chan
description: Viết kịch bản tin tức 40–55 giây giữ chân người xem: hook, vòng mở, trả lời, mồi bình luận, kết vòng lặp, CTA.
---
# Viết kịch bản giữ chân

## Độ dài
- 40–55 giây, khoảng **130–170 chữ (âm tiết)**, 12–16 câu; mỗi câu một dòng trong `spec.json` (`segments[].line`).
- Câu ngắn, ≤ 20 âm tiết, dễ đọc liền một hơi.
- **Số viết bằng chữ** để giọng clone đọc đúng: "bảy trăm bảy mươi chín ca", không "779 ca". Tránh viết tắt, ký hiệu.

## Khung theo giây
| Giây | Nhiệm vụ |
|---|---|
| 0–2 | **HOOK**: câu < 12 chữ, nói ngay ở khung đầu, kèm chữ lớn trên hình |
| 2–6 | Khoá ngữ cảnh: ai, ở đâu, vì sao liên quan tới bạn |
| 6–25 | Thân: 3 ý, mỗi ý một hình thật + một số liệu có nguồn |
| ~17–20 | **Vòng mở**: "Nhưng điều đáng lo nhất lại không phải con số này." |
| 25–40 | **Trả lời** câu hỏi đã treo + ý nghĩa với người Việt; một cú lật/lưu ý trung thực |
| 40–48 | Lời khuyên hành động (checklist nếu là tin dịch vụ) |
| cuối | **Mồi bình luận** gắn trải nghiệm thật → **CTA** "Theo dõi để…" → câu cuối **nối về câu đầu** để video lặp tự nhiên |

## 5 công thức hook
1. Hệ quả với bạn: "[Sự kiện] có thể khiến [điều người Việt quan tâm] thay đổi".
2. Con số + so sánh: "Gấp sáu lần tốc độ âm thanh, nhưng…".
3. Câu hỏi mở: "Vì sao [nhân vật] lại [hành động bất ngờ]?".
4. Mâu thuẫn: "Ai cũng nghĩ X, hoá ra Y".
5. "Lần đầu tiên"/kỷ lục — **chỉ khi ≥ 2 nguồn xác nhận**.

## Kỹ thuật kể
- Mở bằng hệ quả, nói nguyên nhân sau. Dùng một nhân vật cụ thể ("ông cụ bảy mươi ba tuổi") thay số liệu trừu tượng.
- Mồi bình luận kiểu "Nhà bạn có ai đang bị…? Kể mình nghe ở phần bình luận." Không mồi kiểu "comment 1 nếu…".
- Không bịa; câu nào không có nguồn thì xoá. Tái hiện thì ghi "VÍ DỤ MINH HOẠ".
- Xem `examples/cum-a/spec.json` làm chuẩn.
