---
name: dung-video-giu-chan
description: Dựng video 9:16 có nhịp giữ chân: hỗn hợp cảnh, nguồn hình hợp pháp, Ken Burns, bản đồ, biểu đồ, phụ đề, SFX, nhạc.
---
# Dựng video giữ chân

## Hỗn hợp cảnh (đổi cảnh ~1,6–2,2 s; hook 0,5–1 s/cảnh; đoạn kể 3–4 s cho "thở")
- A. Ảnh/video thật của sự kiện, toàn màn hình, Ken Burns (zoom 1,0→1,12 hoặc lia) — ~40%.
- B. Trang báo (ưu tiên báo Việt) chụp tiêu đề + đoạn ngắn, highlight vàng, thẻ "Nguồn: … · ngày" — ~15%.
- C. Bản đồ động (Natural Earth PD, hoặc OSM ghi "© OpenStreetMap contributors") — ~10%.
- D. Biểu đồ/so sánh động, số chạy đếm — ~10%.
- E. Thẻ nền đen ô đỏ số lớn — tối đa 3 lần/video.
- F. Stock minh hoạ chung (Pexels/Pixabay), không giả làm ảnh sự kiện — ~15%.
- Không 2 cảnh liền cùng loại. ≥ 60% thời lượng là hình thật hoặc chuyển động.

## Nguồn hình hợp pháp
- Wikimedia Commons: đọc giấy phép từng file; PD dùng tự do; CC BY/BY-SA ghi tác giả + giấy phép trên khung; tránh NC/ND.
- NASA, NOAA, USGS, CDC, DoD/DVIDS, White House: thường public domain (không dùng logo để ngụ ý bảo trợ; ảnh bên thứ ba thì không).
- Press kit công ty: đọc điều khoản, ghi nguồn.
- Ảnh hãng tin (AP, Reuters, Getty): chỉ trong ảnh chụp trang báo kèm nguồn.
- Ghi mọi hình/nhạc vào `CREDITS_LICENSES.md` (mẫu: `examples/cum-a/CREDITS_LICENSES.md`). Hình phải khớp câu đang đọc.

## Chữ và phụ đề
- Phụ đề 1–3 chữ, trắng đậm viền đen, trong vùng an toàn (trên 20% đáy, tránh cột icon bên phải); từ khoá tô vàng, hiệu ứng nảy; 5–10 từ/giây.
- Khung đầu = ảnh bìa: hình thật + 2–5 chữ lớn + con số; không flash trắng.

## Âm thanh
- Nhạc nền tin tức/hồi hộp, ducking dưới giọng (sidechain). Nguồn: Wikimedia (CC BY, ghi công), Pixabay/YouTube Audio Library (chủ tự tải nếu server bị chặn).
- SFX: whoosh khi chuyển cảnh, ding khi số hiện, hit ở hook, riser trước vòng mở. Tự tạo bằng `scripts/make_sfx.py`.

## Lệnh
```
python scripts/concat_voice.py --dir work/          # vo.wav + timeline.json
python scripts/render.py --shots work/shots.json --spec work/spec.json --out work/video.mp4
python scripts/mix.py --config work/mix.json --video work/video.mp4 --out work/final.mp4
```
`render.py` là khung cơ bản (Ken Burns, thẻ số, phụ đề); bản đồ/biểu đồ/trang báo có thể dựng thành ảnh hoặc clip rồi đưa vào `shots.json`.
