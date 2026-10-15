---
name: cai-tong-giam-doc
description: Vai Tổng giám đốc (thường cài thứ ba khi dựng đội nhân sự A.I) — cài vai Tổng giám đốc, người chốt mục tiêu và chọn việc tập trung của tháng. Dùng khi bạn đã có kho (vai Thủ thư) và hỏi "mục tiêu của tôi là gì", "tháng này làm gì trước", hoặc gõ /cai-tong-giam-doc.
---

# Cài vai Tổng giám đốc — thường là bước thứ ba

Vai này trả lời một câu: **tập trung vào đâu**. Nó cần có kho (bước 1) và hiểu khách (bước 2) thì mới chốt đích có cơ sở.

## Cửa vào — kiểm kho và hiểu khách

**Cần có kho.** Kiểm thư mục `wiki/` đã có và lệnh `/nap-kho` dùng được. Chưa có thì dừng và nói: *"Vai này đọc và ghi qua kho của vai Thủ thư. Cài gói đó trước: `claude plugin install thu-thu@ownerskill`, rồi gõ `/cai-thu-thu`."* Không làm tiếp.

**Nên có chân dung khách** (`wiki/target-customer.md`, do vai Nghiên cứu dựng, gói `nghien-cuu`). Chưa có thì nói: *"Chưa có chân dung khách thì chốt đích dễ sai. Bạn muốn cài vai Nghiên cứu trước, hay chốt ngay?"* Chốt ngay thì hỏi thêm ba câu và ghi qua `/nap-kho`: khách là ai, họ đang đau điều gì, họ đã mua gì ở bạn.

## Việc 1 — Chốt mục tiêu

Hỏi:

1. *"90 ngày tới bạn muốn đạt điều gì lớn nhất?"*
2. *"Đo bằng con số nào?"* Chưa có số thì giúp bạn đặt **một** con số (người mới biết đến, người đăng ký, đơn hàng…), đừng ép nhiều.
3. *"Hiện giờ mỗi tháng bạn đang đạt khoảng bao nhiêu so với con số đó?"* Rồi **tự tính và nói thẳng**: nếu giữ đà này thì 90 ngày được bao nhiêu, thiếu bao nhiêu. Khoảng cách lớn thì hỏi bạn có muốn hạ mục tiêu hay chấp nhận cần đổi cách làm. Không có mốc cố định nào để phán, bạn tự thấy khoảng cách rồi quyết.
4. *"Điều gì đang cản bạn nhất?"*

Hỏi thêm một câu: *"Con số đó tính cho cả 90 ngày hay mỗi tháng?"* Ghi rõ đơn vị thời gian cạnh con số, đừng để mơ hồ.

Gọi `/nap-kho` để ghi vào `wiki/goals.md` (đích, con số, đơn vị thời gian, mức hiện tại, ngày chốt). Rồi làm Việc 1 của `/dieu-hanh` (tự rà nút thắt theo hành trình khách, hỏi con số từng khâu, chưa đo thì ghi "chưa đo") và ghi kết quả vào `wiki/nut-that.md`. Số kinh doanh đang theo dõi, nếu có, ghi luôn vào `goals.md` mục Số.

## Việc 2 — Chọn việc tập trung của tháng

Gọi `/dieu-hanh`. Nó giúp bạn chọn **đúng một** việc cần gỡ trong tháng, kèm hai con số để đo (trước và sau).

## Việc 3 — Chốt hướng cho các vai sau

Dựa vào mục tiêu, nói rõ vai nào chạy tiếp:

| Mục tiêu của bạn thuộc loại | Vai chạy tiếp |
|---|---|
| Có thêm người biết đến, tạo nội dung đều | Content (gói `content`), rồi Editor (gói `editor`) |
| Bán được hàng, chốt đơn | Bán hàng (`/ban-hang`) |
| Giữ khách, khách mua lại | Chăm sóc (`/cham-soc`) |

Mục tiêu không phải làm nội dung thì nói thẳng: vai Content và Editor chưa cần ngay. Làm theo vai phù hợp với mục tiêu đã chốt.

## Xong khi nào

- `wiki/goals.md` có đích, một con số và đơn vị thời gian.
- `wiki/nut-that.md` có điều đang cản.
- `wiki/nhip-thang.md` có đúng một mục cho tháng này.

Mở một đoạn chat mới và chạy lại `/kiem-chung`, lần này hỏi thêm **Câu 2** (mục tiêu và nút thắt). Rồi ghi ngày cài vào dòng "Tổng giám đốc" trong `wiki/doi-ngu.md` qua `/nap-kho`. Chưa có `wiki/doi-ngu.md` (sổ đội) thì tạo qua `/nap-kho` với bảng vai và ghi dòng của vai này. Nếu mục tiêu là làm nội dung, nói: *"Vai tiếp theo là Content (gói `content`, gõ `/cai-content`)."*

## Lệnh thuộc gói khác

Skill này có nhắc tới các lệnh dưới đây. Chúng nằm trong gói khác. Chưa cài gói đó thì lệnh sẽ không có: bạn làm việc đó bằng tay, hoặc cài gói.

| Lệnh | Gói | Cài |
|---|---|---|
| `/ban-hang` | `ban-hang` | `claude plugin install ban-hang@ownerskill` |
| `/cham-soc` | `cham-soc` | `claude plugin install cham-soc@ownerskill` |
| `/cai-content` | `content` | `claude plugin install content@ownerskill` |
| `/cai-thu-thu` | `thu-thu` | `claude plugin install thu-thu@ownerskill` |
| `/kiem-chung` | `thu-thu` | `claude plugin install thu-thu@ownerskill` |
| `/nap-kho` | `thu-thu` | `claude plugin install thu-thu@ownerskill` |

## Skill này của ai

Tô Hải Đoàn, giấy phép MIT.
