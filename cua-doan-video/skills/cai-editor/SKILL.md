---
name: cai-editor
description: Bước 5 khi dựng đội nhân sự A.I — cài vai Editor, người dựng video. Kiểm máy bạn có chạy được không, cài công cụ cần thiết, ghi lại cách bạn quay, rồi dựng thử một clip ngắn. Dùng khi bạn đã cài Content và hỏi "làm video", "cài vai dựng video", hoặc gõ /cai-editor.
---

# Cài vai Editor — bước 5 trong 5

Vai này dựng clip bạn tự quay thành video hoàn chỉnh, và giữ kho cảnh quay để tra khi cần chèn.

## Cửa vào — kiểm máy và các bước trước

1. Mở `wiki/doi-ngu.md`. Content chưa có ngày cài thì dừng và chỉ về `/cai-content`.
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

Ghi ngày cài vào dòng "Editor" trong `wiki/doi-ngu.md` qua `/nap-kho`. Rồi nói: *"Đội nội dung của bạn đã đủ. Gõ `/chay-chuoi-dau-tien` để chạy trọn một vòng từ bài tới video."*

## Skill này của ai

Tô Hải Đoàn, giấy phép MIT.
