# Phong cách: chuyên gia ngồi nói

Một người nói thẳng vào máy, cận ngực, trong nhà hay ngoài trời đều được. Cả phong cách xoay quanh một ý: **mắt người xem không bao giờ phải nhìn một khung hình đứng yên quá vài giây, trong khi lời nói vẫn liền mạch.**

## Nhịp cần đạt

| | Mục tiêu khi dựng |
|---|---|
| Đổi hình | khoảng 2–3,5 giây một lần (`nhip_muc_tieu` trong bảng dựng, mặc định 3,1) |
| Quãng hình đứng yên dài nhất | không quá 6 giây |
| Phụ đề | 2–5 chữ mỗi lần hiện — vừa với người nói nhanh |

"Đổi hình" gồm: mỗi vết cắt, mỗi lần đổi khung (phóng to/thu nhỏ) và mỗi lần một cảnh chèn hiện lên hay rút đi.

## Năm lớp hiệu ứng

1. **Cắt nhảy** — bỏ hết khoảng ngập ngừng và câu nói lại, lời nói liền mạch. Đoạn nói dài thì đổi khung (phóng vào/thu ra) để hình không đứng yên.
2. **Phụ đề hai tầng, ngay dưới cằm** (khoảng 66–72% chiều cao khung). Dòng nhỏ viết thường, gõ ra từng chữ có con trỏ. Cụm nhấn to gấp đôi, đậm, nghiêng, hiện mờ rồi rõ dần trong khoảng 0,2 giây. Chữ trắng, bóng đổ mềm, không viền.
3. **Thẻ chữ toàn màn hình** — nền đen hoặc nền trắng ngà xen kẽ. Đầu mục to ở giữa, chữ nhỏ bên dưới hiện từng từ theo lời. Đây là bộ khung của bài: bài nói "5 bước" thì có 5 thẻ. Mỗi thẻ 2–4 giây.
4. **Thẻ danh sách / con số** — tiêu đề rồi từng dòng gõ ra đúng lúc người nói nhắc tới ý đó.
5. **Ảnh bằng chứng và cảnh minh hoạ (B-roll)** — ảnh chụp màn hình bo góc, hơi nghiêng, 1–3 tấm hiện lần lượt, phụ đề nhảy lên trên đầu ảnh. Cảnh minh hoạ chèn đúng lúc câu nói tả cảnh hay hành động, phụ đề vẫn chạy trên đó.

## Kiểu chữ và màu

- Font **Be Vietnam Pro** (đã kèm sẵn trong `fonts/`, viết tiếng Việt có dấu đúng ở cả chữ HOA).
- Phụ đề **chỉ màu trắng**, không tô màu cụm nhấn. Ngoại lệ: phụ đề nằm trên thẻ ảnh nền trắng ngà thì tự đổi sang chữ tối, vì chữ trắng trên nền trắng là mất chữ.
- Thẻ chữ: nền `"den"` (đen) hoặc `"trang"` (trắng ngà `#faf9f6`).

## Skill làm được đến đâu

| | |
|---|---|
| ✅ làm được | cả năm lớp; gõ chữ có con trỏ; cụm nhấn hiện mờ-rõ; thẻ nền đen/trắng ngà; ảnh bo góc nghiêng; cảnh minh hoạ từ thư mục `broll/` của dự án; chuyển cảnh vào/ra |
| ⬜ chưa làm | cụm nhấn **nằm trên** dòng nhỏ (hiện chỉ có kiểu dòng nhỏ ở trên) · hiệu ứng âm thanh (tiếng "vút", "bụp") khi chuyển cảnh |
