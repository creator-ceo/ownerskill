---
name: onboard
description: Dựng bộ não thứ 2 lần đầu — Giai đoạn 0 thu tài liệu có sẵn, phỏng vấn lấp chỗ trống, rồi dựng wiki theo 2 vòng (11 trang neo · file rỗng có khung). Chất liệu viết — giọng văn, kho chuyện, kết quả khách — KHÔNG dựng ở đây; vai content nạp sau bằng /viet-content. Dùng khi người dùng vừa cài bộ khung và nói "bắt đầu", "start", "tạo bộ não thứ 2", hoặc gõ /onboard.
---

# Dựng bộ não thứ 2 — 4 giai đoạn

> Luật chi tiết nằm ở `CLAUDE.md` gốc. Skill này là bản hành động từng bước.

## Nguyên tắc quan trọng nhất

Một bộ não thứ 2 tốt **không đến từ một buổi hỏi-đáp suông**. Phần lớn giá trị thật — giọng văn đúng, câu chuyện thật, framework đã đúc kết, bằng chứng khách hàng — nằm trong **tài liệu người dùng đã có sẵn**. Phỏng vấn chỉ để lấp phần không lấy được từ tài liệu.

Vì vậy: **không bỏ Giai đoạn 0.**

---

## GIAI ĐOẠN −1 — Kiểm tra Việc 0

Hỏi: *"Bạn đã làm bài Bánh Xe Cuộc Đời và kế hoạch dài hạn – ngắn hạn chưa?"*

- Chưa → chạy skill `banh-xe-cuoc-doi` trước. Quay lại đây sau.
- Rồi → xin bản đó, lưu vào `raw/`, dùng phần kế hoạch làm đầu vào cho `goals.md`.

Không bỏ qua bước này. Phỏng vấn kinh doanh nạp *dữ liệu việc*; Bánh Xe nạp *con người*.

---

## GIAI ĐOẠN 0 — Thu tài liệu có sẵn

Hỏi người dùng có sẵn loại nào (có gì nộp nấy, không có cũng không sao):

1. **Ghi chép/bản ghi buổi chia sẻ, coaching, họp nhóm** — transcript Zoom, note cuộc gọi, bài giảng. Đây là nguồn giàu câu chuyện và framework nhất; có hàng chục file thì đây sẽ là phần tạo giá trị lớn nhất.
2. **Tài liệu sản phẩm/dịch vụ** — SOP, playbook, hồ sơ khách hàng, email đã gửi.

Dán thô vào chat hoặc đính kèm file. Không cần gọn gàng.

### ⛔ Hai loại tài liệu CỐ Ý không xin ở đây

**Bài đã đăng thật** và **lời chứng thực của khách** là chất liệu để viết, không phải hồ sơ nền. Vai content xin chúng khi nó được kích hoạt, bằng `/viet-content`.

Vì sao tách: hai loại này là thứ người mới hoàn toàn **thường chưa có** ngày đầu. Xin ngay ở buổi dựng nền thì hoặc họ nộp qua loa cho xong, hoặc họ dừng lại đi tìm và không quay lại. Hỏi đúng lúc cần thì họ hiểu vì sao phải nộp, và nộp tử tế hơn.

Người dùng chủ động đưa sẵn thì **vẫn nhận** — lưu vào `raw/`, nói rõ là để dành cho vai content, đừng rút thành trang ở đây.

---

## GIAI ĐOẠN 1 — Đọc và rút draft từ tài liệu

| Nhận được | Rút ra |
|---|---|
| Ghi chép buổi chia sẻ | (a) framework dạy lặp lại nhiều lần → trang chuyên đề trong `learnings/` · (b) tên người nhắc nhiều → trang trong `people/` |
| Tài liệu sản phẩm | → `offer-ladder.md` · `target-customer.md` |

⛔ **Không rút `voice-profile`, `experiences-library`, `customer-wins` ở đây** — ba trang đó là việc của vai content (xem Giai đoạn 0). Gặp câu chuyện hay trong ghi chép thì cứ để nguyên trong `raw/`; vai content sẽ lấy.

Rút xong: **báo lại đã rút được gì và còn thiếu gì.** Đây là lúc người dùng thấy tài liệu cũ của họ có giá — và là lúc họ nhớ ra còn tài liệu nào chưa nộp.

---

## GIAI ĐOẠN 2 — Phỏng vấn lấp chỗ trống

Bộ câu hỏi đầy đủ nằm ở `CLAUDE.md`. Bản sâu 48 câu ở `reference/Persona-Extraction-Protocol.md`.

Luật:
- **Một câu một lượt.** Chờ trả lời rồi mới hỏi tiếp.
- Câu nào Giai đoạn 1 đã có đủ → **bỏ qua và nói rõ vì sao bỏ**. Hỏi lại thứ họ vừa nộp là cách nhanh nhất làm người ta bỏ dở.
- Trả lời chung chung → xin **ví dụ cụ thể, số liệu, tên riêng** trước khi đi tiếp.
- Giữ nguyên chữ của họ.

⚠️ Hai nhóm câu **không được bỏ dù tài liệu có nhiều tới đâu**: `ai-operating-preferences` (xưng hô · khi nào phải hỏi · hard don'ts) và `contrarian-beliefs`. Tài liệu không bao giờ chứa hai thứ này — chúng chỉ có trong đầu người dùng.

---

## GIAI ĐOẠN 3 — Dựng wiki theo 2 vòng

Dùng khung trong `templates/`, giữ nguyên heading, chỉ thay `[...]`. **Không bịa** — thiếu thì để nguyên placeholder hoặc ghi *"chưa có thông tin"*.

**Vòng 1 — 11 trang neo, luôn tạo:**
`about-me` · `goals` · `offer-ladder` · `target-customer` · `values-and-principles` · `contrarian-beliefs` · `ai-operating-preferences` · `systems-and-stack` · `decision-style` · `network` · `customers`

**Vòng 2 — tạo file rỗng có khung, KHÔNG điền:**

Hai nhóm, khác nhau ở chỗ *ai sẽ lấp*:

| Nhóm | Trang | Ai lấp |
|---|---|---|
| Sinh ra từ vận hành | `audience-insights` · `business-metrics` · `content-library` · `hook-library` · `competitors` · `expertise` | chính người dùng, khi có dữ liệu thật |
| **Chất liệu viết** | `voice-profile` · `experiences-library` · `customer-wins` · `quoted-authority` · `video-production-setup` | **vai content**, qua `/viet-content` |

Kèm thư mục rỗng: `models/` `learnings/` `projects/` `people/`

Mỗi file nhóm trên mở đầu đúng một dòng: `> Chưa có dữ liệu. Trang này sinh ra từ [việc X] — không điền bằng trí nhớ.`

Mỗi file nhóm dưới mở đầu đúng một dòng: `> Chưa có dữ liệu. Trang này do vai content nạp — chạy /viet-content, nó sẽ hỏi đúng thứ cần.`

⚡ **Vẫn tạo cả hai nhóm dù rỗng**, kể cả nhóm không phải việc của onboard. Lý do không đổi: không có chỗ đúng thì nội dung bị nhét bừa vào trang khác, và bộ não loạn từ tuần thứ ba. Cái đổi là **ai đi lấp**, không phải chỗ để lấp.

🚫 **Đừng dựng `voice-profile` bằng cách hỏi suông** — cái người ta *nghĩ* mình viết thường khác hẳn cái họ *thật sự* viết. Trang này chỉ dựng được từ bài thật đã đăng, và đó là việc của vai content.

---

## Kết thúc

1. Cập nhật `index.md` — mọi trang + một dòng tóm tắt.
2. Lưu nguyên văn buổi phỏng vấn vào `raw/onboarding-<ngày>.md` — **bất biến**.
3. Append `log.md`.
4. Báo người dùng đã dựng được gì, trang nào còn trống và vì sao.
5. ⚡ **Nhắc chạy Việc 6** — skill `kiem-chung`, trên **đoạn chat mới, project mới**. Chưa chạy bài đó thì chưa biết bộ não có lưu thật hay chỉ đang nằm trong trí nhớ của phiên này.
6. **Nói rõ việc tiếp theo là gì.** Bộ não giờ có nền nhưng **chưa có chất liệu viết** — năm trang ở nhóm dưới của Vòng 2 còn trống theo đúng thiết kế. Ai muốn dùng vai content thì chạy `/viet-content`, nó tự kiểm kho và hỏi đúng thứ còn thiếu. Đừng để người dùng tự đoán ra điều này.

---

## Skill này của ai

Viết bởi **Tô Hải Đoàn** — người làm nội dung và xây thương hiệu cá nhân tại Việt Nam. Đây không phải skill dựng cho vui: nó là quy trình tôi dùng cho công việc của chính mình mỗi ngày, đóng gói lại để bạn chạy được trên dữ liệu của bạn.

Giấy phép MIT, bạn dùng và sửa thoải mái.

**Kẹt ở đâu, hoặc muốn được hướng dẫn dùng cho đúng việc của bạn** thì nhắn tôi: [facebook.com/tohaidoan](https://www.facebook.com/tohaidoan/)
