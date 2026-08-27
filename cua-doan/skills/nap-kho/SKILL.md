---
name: nap-kho
description: Đường ghi DUY NHẤT vào wiki/ của bộ não thứ 2. Nạp nguyên liệu mới — câu chuyện, insight, tài liệu, bài học, hình mẫu — bằng cách ĐỌC và PHÂN TÍCH trước, soi trùng với kho đang có, rồi mới ghi và append log.md. Dùng khi người dùng kể một chuyện mới, nói một điều vừa nhận ra, đưa một tài liệu, hoặc chỉ nói "lưu cái này vào não", "ghi lại insight này", "nạp vào kho", hoặc gõ /nap-kho.
---

# Nạp vào kho — có soi, không chép thẳng

## Vì sao chỉ còn một đường ghi

Sửa thẳng file `.md` thì nhanh hơn — và đó chính là vấn đề. Sau vài tuần sửa tay, bộ não sẽ có: cùng một câu chuyện nằm ở ba trang, hai trang nói ngược nhau mà không ai biết trang nào mới, và `log.md` không phản ánh thứ gì đã thật sự đổi.

Đi qua skill này thì **mỗi lần ghi đều bắt buộc qua bốn cửa**: soi trùng · rút bài học đúng luật · chọn đúng chỗ đặt · nối liên kết. Chậm hơn vài phút, đổi lại bộ não sáu tháng sau vẫn dùng được.

⚠️ **Luật:** không sửa thẳng file trong `wiki/`, kể cả sửa một lỗi chính tả. Mọi thay đổi đi qua đây.

---

## Bước 1 — Đọc và phân loại

Đọc kỹ nguyên liệu người dùng đưa. Xác định nó là loại gì:

| Loại | Dấu hiệu | Đích đến |
|---|---|---|
| **Câu chuyện** | có mốc thời gian, có chuyện xảy ra với chính người dùng | `experiences-library.md` |
| **Insight khách hàng** | lời khách nói, điều quan sát được từ khách thật | `audience-insights.md` |
| **Bài học / nguyên lý** | một điều vừa nhận ra, áp dụng được nhiều lần | trang chuyên đề trong `learnings/` |
| **Hình mẫu** | một người/thương hiệu đang học theo | `models/<tên>.md` |
| **Kết quả khách** | có con số, có bằng chứng | `customer-wins.md` |
| **Quyết định dự án** | chốt một hướng đi, đổi phạm vi | `projects/<tên>.md` |
| **Tài liệu dài** | transcript, bài viết, khoá học | lưu `raw/` trước, rồi rút ra các trang trên |

Không rõ loại → **hỏi người dùng**, đừng đoán rồi đặt bừa.

---

## Bước 2 — Lưu nguyên bản vào `raw/` trước

Nếu nguyên liệu là tài liệu dài (transcript, bài viết, ghi chép buổi họp):

```
raw/<loại>-<YYYY-MM-DD>-<mô tả ngắn>.md
```

**Không bao giờ sửa file trong `raw/` về sau.** Đây là bản gốc để đối chiếu khi nghi ngờ.

---

## Bước 3 — Soi trùng ⚠️ *(bước hay bị bỏ nhất)*

**Trước khi viết một dòng nào vào `wiki/`**, tìm trong kho xem thứ này đã có chưa:

1. Tìm theo **từ khoá chính** của nguyên liệu.
2. Tìm theo **thông điệp** — cùng một bài học có thể đã được ghi bằng câu chữ khác hẳn.
3. Đọc lướt trang đích để xem có mục nào đang nói cùng chuyện.

Kết quả có ba khả năng:

| Tình huống | Làm gì |
|---|---|
| **Chưa có** | Thêm mục mới |
| **Đã có, cái mới đầy đủ hơn** | **Cập nhật mục cũ**, không tạo mục thứ hai. Giữ chi tiết cũ nếu nó vẫn đúng |
| **Đã có, mâu thuẫn với cái mới** | ⚠️ Dừng lại, **hỏi người dùng cái nào đúng**. Không tự chọn. Rồi ghi rõ *"sửa ngày X, thay cho bản trước"* — giữ dấu vết, đừng xoá lịch sử |

---

## Bước 4 — Rút bài học đúng luật

Với câu chuyện và tài liệu, luôn rút ra một dòng **Bài học**.

**Luật: rút ra, không nghĩ hộ.**

| ✅ Rút ra | ❌ Nghĩ hộ |
|---|---|
| Bài học nằm sẵn trong lời kể, chỉ gọi tên nó ra | Bài học do bạn suy ra vì "nghe hợp lý" |
| Dùng chính chữ của người dùng khi họ đã nói ra | Viết lại thành câu châm ngôn cho hay |
| Không có bài học rõ → ghi *"chưa rút được — cần hỏi thêm"* | Bịa một bài học chung chung để lấp chỗ trống |

Một câu chuyện = **một** thông điệp. Hai thông điệp trở lên thì tách thành hai mục.

---

## Bước 5 — Ghi vào wiki + nối liên kết

- Ghi vào đúng trang đã chọn ở Bước 1.
- **Bắt buộc nối `[[liên kết]]`** tới ít nhất 2 trang liên quan. Trang không có liên kết nào là một thất bại — sáu tháng sau không ai tìm ra nó.
- Nếu tạo trang mới: thêm ngay một dòng vào `index.md`.
- Giữ nguyên chữ của người dùng ở phần trích dẫn. Chỉ dọn câu chữ ở phần đúc kết.

**Không bịa.** Thiếu dữ liệu (con số, tên, ngày) → để `[trong ngoặc vuông]` hoặc hỏi. Một bộ não có chỗ trống thì sửa được; một bộ não có chỗ bịa thì hỏng mà không ai biết.

---

## Bước 6 — Append `log.md`

Luôn ghi thêm vào cuối, **không bao giờ viết đè**:

```
## [YYYY-MM-DD] Nạp <loại> | <tiêu đề ngắn>
<Một–hai câu: nạp gì, vào trang nào, có trùng với cái cũ không>
```

---

## Bước 7 — Báo lại người dùng

Nói gọn ba ý:

1. **Đã ghi gì, vào trang nào**
2. **Có trùng/mâu thuẫn gì với kho cũ không** — đây là phần có giá trị nhất, đừng bỏ
3. **Còn thiếu gì** để mục này dùng được (thiếu bằng chứng? thiếu con số? thiếu bài học?)

---

## Ghi chú cho AI chạy skill này

- **Bạn là chỗ duy nhất ghi vào bộ não.** Không có đường nào khác để chữa nếu bạn ghi sai. Chậm và đúng hơn là nhanh và bừa.
- **Đừng xu nịnh.** Người dùng đưa một insight nhạt thì nói thẳng là nó chưa đủ cụ thể để lưu, và hỏi thêm — đừng khen rồi lưu bừa. Kho đầy thứ nhạt còn tệ hơn kho rỗng, vì nó làm loãng thứ đáng giá.
- **Nghi ngờ trước khi tin.** Nếu người dùng nói *"cái này tôi lưu rồi"* — kiểm tra file thật rồi hãy tin. Trí nhớ về việc đã lưu là thứ sai thường xuyên nhất.
