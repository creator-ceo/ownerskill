---
name: cai-editor
description: Vai Editor (thường cài thứ năm khi dựng đội nhân sự A.I) — cài vai Editor, người dựng video. Kiểm máy bạn có chạy được không, cài công cụ cần thiết, ghi lại cách bạn quay, rồi dựng thử một clip ngắn. Dùng khi bạn đã có kho (vai Thủ thư) và hỏi "làm video", "cài vai dựng video", hoặc gõ /cai-editor.
---

# Cài vai Editor — thường là bước thứ năm

Vai này dựng clip bạn tự quay thành video hoàn chỉnh, và giữ kho cảnh quay để tra khi cần chèn.

## Cửa vào — kiểm máy và các bước trước

1. **Cần có kho.** Kiểm thư mục `wiki/` đã có và lệnh `/nap-kho` dùng được. Chưa có thì dừng và nói: *"Vai này đọc và ghi qua kho của vai Thủ thư. Cài gói đó trước: `claude plugin install thu-thu@creator-skills`, rồi gõ `/cai-thu-thu`."* Không làm tiếp. Vai Content (gói `content`) là nơi viết kịch bản. Chưa có thì vẫn cài được, nhưng bạn sẽ tự mang kịch bản của mình vào.
2. **Kiểm máy:** vai này hiện **chỉ chạy trên Mac chip Apple (M1 trở lên)**, vì bước nghe lời nói dùng công cụ riêng của chip này. Máy khác thì nói thẳng: *"Máy này chưa dựng được video bằng bộ skill này. Bạn vẫn dùng được các vai trước, và có thể dựng video bằng phần mềm khác từ kịch bản Content viết."* Rồi dừng.

## Việc 1 — Cài công cụ

Chạy lệnh kiểm trong skill `/dung-video` (`dv.py kiem`). Thiếu gì thì cài theo hướng dẫn nó in ra: FFmpeg (phần mềm xử lý video, miễn phí) và vài gói Python. Lần nghe đầu tiên máy tự tải một mô hình khoảng 1,6 GB, chỉ một lần.

## Việc 2 — Ghi lại cách bạn quay

Hỏi lần lượt: *"Bạn quay bằng gì (điện thoại hay máy quay)?"*, *"Có micro riêng không?"*, *"Có chân máy hay gimbal (tay cầm chống rung) không?"*, *"Quay ở đâu, ánh sáng thế nào, có đèn riêng không?"*, *"Quay một mình hay có người giúp?"*, *"Bạn có sẵn cảnh quay phụ (B-roll) không?"*, *"Phần hậu kỳ bạn tự làm hay muốn máy dựng?"* Gọi `/nap-kho` ghi vào `wiki/video-production-setup.md`. Nhờ vậy kịch bản Content viết ra chỉ chứa thứ bạn quay được thật.

## Việc 3 — Kho cảnh quay *(tuỳ chọn)*

Bạn có sẵn footage cũ thì gọi `/xuong-video` lập kho một lần để tra cảnh chèn. Chưa có thì bỏ qua, làm lần sau.

## Việc 4 — Dựng thử một clip

Bảo bạn quay hoặc chọn một clip ngồi nói ngắn (30 đến 60 giây). Gọi `/dung-video`. Skill sẽ trình **bảng dựng** cho bạn duyệt trước khi dựng bản cuối. Đừng bỏ bước duyệt.

## Xong khi nào

- Lệnh kiểm máy báo sẵn sàng.
- `wiki/video-production-setup.md` có nội dung thật.
- Có một video dựng thử đã được bạn duyệt.

Ghi ngày cài vào dòng "Editor" trong `wiki/doi-ngu.md` qua `/nap-kho`. Chưa có `wiki/doi-ngu.md` (sổ đội) thì tạo qua `/nap-kho` với bảng vai và ghi dòng của vai này. Rồi nói: *"Vai Editor đã sẵn. Có đủ vai thì gõ `/chay-chuoi-dau-tien` (gói `thu-thu`) để chạy trọn một vòng từ bài tới video."*

## Lệnh thuộc gói khác

Skill này có nhắc tới các lệnh dưới đây. Chúng nằm trong gói khác. Chưa cài gói đó thì lệnh sẽ không có: bạn làm việc đó bằng tay, hoặc cài gói.

| Lệnh | Gói | Cài |
|---|---|---|
| `/cai-thu-thu` | `thu-thu` | `claude plugin install thu-thu@creator-skills` |
| `/chay-chuoi-dau-tien` | `thu-thu` | `claude plugin install thu-thu@creator-skills` |
| `/nap-kho` | `thu-thu` | `claude plugin install thu-thu@creator-skills` |

## Skill này của ai

Tô Hải Đoàn, giấy phép MIT.
