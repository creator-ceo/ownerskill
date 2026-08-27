---
name: onboard
description: Dựng bộ não thứ 2 lần đầu — Giai đoạn 0 thu tài liệu có sẵn, phỏng vấn lấp chỗ trống, rồi dựng wiki theo 3 vòng (11 trang neo · trang cần tài liệu · file rỗng có khung). Dùng khi người dùng vừa cài bộ khung và nói "bắt đầu", "start", "tạo bộ não thứ 2", hoặc gõ /onboard.
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

1. **10–20 bài đã đăng thật** (Facebook/blog/email) hoặc transcript video/script đã quay. Cần bản **thật đã công khai**, không phải nháp.
2. **Ghi chép/bản ghi buổi chia sẻ, coaching, họp nhóm** — transcript Zoom, note cuộc gọi, bài giảng. Đây là nguồn giàu câu chuyện và framework nhất; có hàng chục file thì đây sẽ là phần tạo giá trị lớn nhất.
3. **Tài liệu sản phẩm/dịch vụ** — SOP, playbook, hồ sơ khách hàng, email đã gửi.
4. **Feedback/testimonial/case study khách cũ** — số liệu kết quả thật, lời chứng thực.

Dán thô vào chat hoặc đính kèm file. Không cần gọn gàng.

---

## GIAI ĐOẠN 1 — Đọc và rút draft từ tài liệu

| Nhận được | Rút ra |
|---|---|
| Bài đã đăng | pattern giọng văn: đại từ · tông giọng · kiểu mở bài · câu cửa miệng · ẩn dụ đặc trưng · cách dùng số liệu → draft `voice-profile.md` |
| Ghi chép buổi chia sẻ | (a) câu chuyện cá nhân ngôi thứ nhất → `experiences-library.md` · (b) framework dạy lặp lại nhiều lần → trang chuyên đề trong `learnings/` · (c) tên người nhắc nhiều → trang trong `people/` |
| Tài liệu sản phẩm | → `offer-ladder.md` · `target-customer.md` |
| Feedback khách | → `customer-wins.md`, **giữ nguyên trích dẫn** |

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

## GIAI ĐOẠN 3 — Dựng wiki theo 3 vòng

Dùng khung trong `templates/`, giữ nguyên heading, chỉ thay `[...]`. **Không bịa** — thiếu thì để nguyên placeholder hoặc ghi *"chưa có thông tin"*.

**Vòng 1 — 11 trang neo, luôn tạo:**
`about-me` · `goals` · `offer-ladder` · `target-customer` · `values-and-principles` · `contrarian-beliefs` · `ai-operating-preferences` · `systems-and-stack` · `decision-style` · `network` · `customers`

**Vòng 2 — chỉ tạo khi có tài liệu:**
`voice-profile` (cần ≥10 bài thật) · `experiences-library` · `customer-wins` · `expertise`

Chưa đủ điều kiện → **tạo file với đúng một dòng ghi rõ vì sao trống**, ví dụ: `> Chưa dựng — cần ít nhất 10 bài đã đăng thật.` Đừng dựng `voice-profile` bằng cách hỏi suông: cái người ta *nghĩ* mình viết thường khác hẳn cái họ *thật sự* viết.

**Vòng 3 — tạo file rỗng có khung, KHÔNG điền:**
`audience-insights` · `business-metrics` · `content-library` · `hook-library` · `competitors` · thư mục `models/` `learnings/` `projects/` `people/`

Mỗi file mở đầu đúng một dòng: `> Chưa có dữ liệu. Trang này sinh ra từ [việc X] — không điền bằng trí nhớ.`

Tạo sẵn dù rỗng vì: không có chỗ đúng thì nội dung sẽ bị nhét bừa vào trang khác, và bộ não loạn từ tuần thứ ba.

---

## Kết thúc

1. Cập nhật `index.md` — mọi trang + một dòng tóm tắt.
2. Lưu nguyên văn buổi phỏng vấn vào `raw/onboarding-<ngày>.md` — **bất biến**.
3. Append `log.md`.
4. Báo người dùng đã dựng được gì, trang nào còn trống và vì sao.
5. ⚡ **Nhắc chạy Việc 6** — skill `kiem-chung`, trên **đoạn chat mới, project mới**. Chưa chạy bài đó thì chưa biết bộ não có lưu thật hay chỉ đang nằm trong trí nhớ của phiên này.
