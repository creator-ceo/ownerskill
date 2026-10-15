---
name: cai-content
description: Vai Content (thường cài thứ tư khi dựng đội nhân sự A.I) — cài vai Content, người viết bài, lập kế hoạch tháng và viết kịch bản video theo giọng của bạn. Dùng khi bạn đã có kho (vai Thủ thư) và hỏi "cài vai viết bài", "viết đúng giọng tôi", hoặc gõ $cai-content.
---

# Cài vai Content — thường là bước thứ tư

Vai này viết bài, lập kế hoạch tháng và viết kịch bản video. Nó chỉ viết **đúng giọng bạn** khi có hai thứ: bài bạn đã đăng thật và chuyện thật của bạn.

## Cửa vào — kiểm kho, khách và mục tiêu

**Cần có kho.** Kiểm thư mục `wiki/` đã có và lệnh `$nap-kho` dùng được. Chưa có thì dừng và nói: *"Vai này đọc và ghi qua kho của vai Thủ thư. Cài gói đó trước: gói `thu-thu` (trong Codex gõ `/plugins`, chọn kho ownerskill, cài gói đó), rồi gõ `$cai-thu-thu`."* Không làm tiếp.

**Nên có chân dung khách** (`wiki/target-customer.md`) **và mục tiêu** (`wiki/goals.md`), do vai Nghiên cứu và Tổng giám đốc dựng. Thiếu thì không dừng, nhưng nói rõ bài ra sẽ chung chung hơn, rồi hỏi tối thiểu: *"Bài này viết cho ai?"* và *"Bạn muốn người đọc làm gì sau khi đọc?"* Ghi hai câu trả lời qua `$nap-kho` vào hai trang trên. Mục tiêu đã chốt không liên quan nội dung thì hỏi bạn có thật sự muốn cài vai này lúc này không.

## Việc 1 — Nạp giọng và chuyện

1. *"Dán vào đây 5 tới 10 bài bạn đã đăng thật."* Gọi `$nap-kho` rút hồ sơ giọng của bạn. Không hỏi suông "giọng bạn thế nào", vì cái bạn nghĩ mình viết thường khác cái bạn thật sự viết.
2. *"Kể ít nhất 3 chuyện thật của bạn, mỗi chuyện có cảnh, có người, có con số."* Gọi `$nap-kho` ghi vào kho chuyện (`wiki/experiences-library.md`).
3. Xin thêm **một đoạn bạn nói thật** (một đoạn ghi âm gõ lại, hoặc tin nhắn thoại chép ra) để tách giọng nói với giọng viết. Kịch bản video cần giọng nói, không dùng giọng viết. Chưa có thì bỏ qua, đánh dấu cần bổ sung. Hỏi hai câu về giọng, ghi bổ sung vào `wiki/voice-profile.md`: *"Có từ, cụm hay kiểu nói nào bạn ghét, không bao giờ dùng?"* và *"Có câu cửa miệng nào của bạn không?"*
4. Hỏi hai câu về quan điểm: *"Có điều gì bạn tin là đúng trong nghề mà số đông không đồng ý?"* và *"Vì sao bạn tin vậy?"* Gọi `$nap-kho` ghi vào `wiki/contrarian-beliefs.md`. `$viet-content` cần đủ bốn trang này (giọng, chuyện, khách, quan điểm) mới coi là kho đầy đủ.

Chưa có bài đã đăng thì nói thẳng: chưa viết được bài nghe ra bạn. Gợi ý bạn kể bằng lời, rồi viết thử và sửa.

## Việc 2 — Chạy thử một kế hoạch nhỏ

Gọi `$viet-content` loại **kế hoạch content một tháng** nhưng chỉ cho **một tuần**. Nó hỏi nhịp đăng thật của bạn, số giờ mỗi tuần bạn có, một bài thường mất bao lâu, rồi chia số bài, và ra danh sách đề bài có giải thích vì sao.

## Việc 3 — Viết bài đầu tiên

Chọn một đề trong kế hoạch, gọi `$viet-content` viết thành bài. Đọc bài và hỏi bạn: *"Nghe ra bạn chưa?"* Chỗ nào chưa giống thì sửa, rồi hỏi nguyên nhân. Nếu là một luật viết riêng của bạn, gọi `$nap-kho` ghi lại để lần sau bài ra đúng ngay.

## Xong khi nào

- Có đủ bốn trang: giọng, chuyện, khách (từ bước 2), quan điểm; trang nào còn mỏng thì nói thẳng.
- Có một kế hoạch một tuần và một bài đã được bạn duyệt.

Mở một đoạn chat mới và chạy lại `$kiem-chung`, lần này hỏi thêm **Câu 5** (giọng văn). Rồi ghi ngày cài vào dòng "Content" trong `wiki/doi-ngu.md` qua `$nap-kho`. Chưa có `wiki/doi-ngu.md` (sổ đội) thì tạo qua `$nap-kho` với bảng vai và ghi dòng của vai này. Rồi nói: *"Muốn làm video thì cài gói `editor` (gõ `$cai-editor`). Lưu ý Editor chỉ chạy trên Mac chip Apple."*

## Lệnh thuộc gói khác

Skill này có nhắc tới các lệnh dưới đây. Chúng nằm trong gói khác. Chưa cài gói đó thì lệnh sẽ không có: bạn làm việc đó bằng tay, hoặc cài gói.

| Lệnh | Gói | Cài |
|---|---|---|
| `$cai-editor` | `editor` | gói `editor` (trong Codex gõ `/plugins`, chọn kho ownerskill, cài gói đó) |
| `$cai-thu-thu` | `thu-thu` | gói `thu-thu` (trong Codex gõ `/plugins`, chọn kho ownerskill, cài gói đó) |
| `$kiem-chung` | `thu-thu` | gói `thu-thu` (trong Codex gõ `/plugins`, chọn kho ownerskill, cài gói đó) |
| `$nap-kho` | `thu-thu` | gói `thu-thu` (trong Codex gõ `/plugins`, chọn kho ownerskill, cài gói đó) |

## Skill này của ai

Tô Hải Đoàn, giấy phép MIT.
