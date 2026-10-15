---
name: cai-nghien-cuu
description: Bước 2 khi dựng đội nhân sự A.I — cài vai Nghiên cứu thị trường. Tìm hiểu khách của bạn đang muốn gì, bực gì, đối thủ đang hứa gì, rồi nạp kết quả vào kho. Dùng khi bạn đã cài Thủ thư và hỏi "bước tiếp theo", "nghiên cứu khách giúp tôi", hoặc gõ /cai-nghien-cuu.
---

# Cài vai Nghiên cứu — bước 2 trong 5

Vai này làm hai việc: hiểu khách thật của bạn, và lấp các trang đầu tiên trong kho bằng thứ tìm ra. Kết quả nghiên cứu là nền cho các vai sau.

## Cửa vào — kiểm bước 1

Mở `wiki/doi-ngu.md`. Dòng "Thủ thư" chưa có ngày cài thì dừng và nói: *"Cần cài Thủ thư trước. Gõ `/cai-thu-thu`."* Không làm tiếp.

## Việc 1 — Chọn một nhóm khách

Hỏi trước hai điều: *"Bạn muốn phục vụ nhóm khách nào nhất, mô tả bằng một câu?"* và *"Bạn đang bán gì cho họ?"* Các điều còn lại `/nghien-cuu-e5` sẽ tự hỏi khi cần, bạn chỉ trả lời phần chưa nói.

Chỉ **một** nhóm cho lần cài này. Nhiều nhóm thì làm lần sau.

## Việc 2 — Chạy nghiên cứu

1. Gọi `/nghien-cuu-e5` cho nhóm khách đó, **chọn mức Nhanh**. Khi nó hỏi lại những điều bạn đã nói ở Việc 1, dùng câu trả lời đã có, đừng bắt bạn nói lại. Nó cần lời khách thật, nên hỏi bạn có tin nhắn, bình luận hay ghi chép nào chưa lưu không. Nó đi tìm khách muốn gì, tin gì, đã thử gì, bực gì (bằng lời của chính họ, có nguồn), và đối thủ đang hứa gì.
2. Nếu bạn có một vài đối thủ rõ ràng: gọi `/soi-doi-thu`. Nếu có người bạn muốn học theo: gọi `/soi-hinh-mau`.
3. Cần một người thật để chứng minh một ý nào đó: gọi `/tim-tam-guong`.

## Việc 3 — Nạp kết quả vào kho

Cho bạn xem tóm tắt. Bạn gõ "ok" thì gọi `/nap-kho` để ghi vào kho. Các trang thường được dựng ở bước này: chân dung khách, lời khách tự nói, đối thủ, vì sao chọn bạn, các lời từ chối hay gặp. Trang nào nghiên cứu không tìm ra gì thì **không dựng**.

## Xong khi nào

- Báo cáo nghiên cứu đã lưu, và bạn đã gõ "ok" để nạp.
- Có trang chân dung khách và trang lời khách tự nói, đều có nội dung thật trong `wiki/`.

**Mức Nhanh của `/nghien-cuu-e5` đòi từ 15 câu khách nói, 5 nguồn, 3 đối thủ.** Khách mới thường chưa đủ. Chưa đủ thì làm đúng ba việc, không hạ chuẩn ngầm:
1. Nói thẳng thiếu ở đâu (còn bao nhiêu câu, nguồn, đối thủ so với mức đòi).
2. Vẫn nạp phần đã có, nhưng ghi **"mỏng"** vào cột Ghi chú của dòng Nghiên cứu trong sổ đội.
3. Hẹn bổ sung dần: mỗi tuần dán thêm tin nhắn, bình luận mới của khách và nạp bằng `/nap-kho` vào trang lời khách.

Mỏng vẫn được đi tiếp sang bước 3. Chỉ dừng khi hoàn toàn không có lời khách nào để nạp.

Ghi ngày cài vào dòng "Nghiên cứu" trong `wiki/doi-ngu.md` qua `/nap-kho`. Rồi nói: *"Bước 3 là cài Tổng giám đốc, người chốt mục tiêu. Gõ `/cai-tong-giam-doc`."*

## Skill này của ai

Tô Hải Đoàn, giấy phép MIT.
