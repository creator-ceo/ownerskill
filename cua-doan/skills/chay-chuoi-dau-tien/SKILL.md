---
name: chay-chuoi-dau-tien
description: Dẫn bạn dựng đội nhân sự A.I theo đúng thứ tự (Thủ thư, Nghiên cứu, Tổng giám đốc, Content, Editor), rồi chạy trọn một vòng từ nguyên liệu thô tới video đầu tiên. Dùng khi bạn vừa cài bộ skill và hỏi "giờ làm gì trước", "bước tiếp theo là gì", "chạy thử cả quy trình giúp tôi", "tôi cài tới đâu rồi", hoặc gõ /chay-chuoi-dau-tien.
---

# Dựng đội và chạy chuỗi đầu tiên

Skill này **không tự làm việc nào**. Nó đọc sổ đội, cho bạn biết đang đứng ở bước nào và bước kế tiếp là gì.

## Phần 1 — Dựng đội, năm bước theo thứ tự

Mỗi bước là một vai. Vai sau đọc thứ vai trước dựng, nên **không nhảy cóc**.

| Bước | Vai | Gõ | Làm gì | Xong khi |
|---|---|---|---|---|
| 1 | 🗂️ Thủ thư | `/cai-thu-thu` | Dựng kho tài liệu, dạy cách nạp bằng `/nap-kho` | `/kiem-chung` đạt |
| 2 | 🔎 Nghiên cứu | `/cai-nghien-cuu` | Tìm hiểu khách và đối thủ, nạp kết quả vào kho | Có chân dung khách, có lời khách nói |
| 3 | 🧭 Tổng giám đốc | `/cai-tong-giam-doc` | Chốt mục tiêu 90 ngày và việc tập trung của tháng | Có đích kèm con số |
| 4 | ✍️ Content | `/cai-content` | Nạp giọng và chuyện, lập kế hoạch, viết bài đầu tiên | Một bài được bạn duyệt |
| 5 | 🎞️ Editor | `/cai-editor` | Cài công cụ, ghi cách bạn quay, dựng clip thử | Một video được bạn duyệt |

Bước 4 và 5 chỉ cần khi mục tiêu của bạn là làm nội dung. Mục tiêu khác (bán hàng, chăm sóc khách) thì Tổng giám đốc sẽ chỉ vai nào chạy tiếp.

### Cách tìm bạn đang ở bước nào

Mở `wiki/doi-ngu.md` (sổ đội). Dòng vai nào có ngày cài là đã xong. Dòng đầu tiên còn trống là bước kế tiếp. Chưa có file này nghĩa là chưa cài gì, bắt đầu từ `/cai-thu-thu`.

Nói với bạn đúng một câu: *"Bạn đang ở bước N. Gõ `/cai-...` để làm tiếp."*

## Phần 2 — Chạy trọn một vòng *(sau khi đã cài đủ đội)*

1. **Chốt việc của tháng:** `/dieu-hanh`.
2. **Lập kế hoạch:** `/viet-content`, nhờ lập kế hoạch content cho tuần hoặc tháng.
3. **Viết bài:** chọn một đề, nhờ `/viet-content` viết, đọc và sửa tay.
4. **Viết kịch bản video:** cũng với đề đó, nhờ `/viet-content` viết kịch bản kèm danh sách cảnh cần quay.
5. **Quay và dựng:** bạn quay theo kịch bản, rồi gọi `/dung-video`. Cần cảnh chèn thì dùng `/xuong-video`.
6. **Ghi lại điều học được:** bài nào ra kết quả, chuyện nào hay thì gọi `/nap-kho`. Vòng sau mọi vai đọc được thứ bạn vừa học.

## Nếu bạn kẹt

- Skill báo thiếu trang trong `wiki/` → làm theo gợi ý nạp ngay trong skill đó, rồi `/nap-kho`.
- Máy không phải Mac chip Apple → các vai trước vẫn dùng được; chỉ khâu dựng video của Editor chưa chạy.
- Không biết đang ở đâu → chạy lại `/chay-chuoi-dau-tien`.

## Skill này của ai

Tô Hải Đoàn, giấy phép MIT.
