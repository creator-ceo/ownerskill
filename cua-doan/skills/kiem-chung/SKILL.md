---
name: kiem-chung
description: Bài test Việc 6 — xác nhận bộ não thứ 2 đã LƯU THẬT vào file, không phải chỉ nằm trong trí nhớ của đoạn chat. Chạy sau khi dựng xong bộ não, và chạy lại mỗi lần nạp một khối dữ liệu lớn. Dùng khi người dùng nói "kiểm chứng", "test bộ não", "bộ não chạy chưa", "làm việc 6", hoặc gõ /kiem-chung.
---

# Bài kiểm chứng — bộ não đã lưu thật chưa

## Vì sao bài test này tồn tại

Cái bẫy phổ biến nhất khi dựng bộ não thứ 2 **không phải** là nạp thiếu. Là thế này:

> Người dùng ngồi cả buổi trả lời phỏng vấn. AI trả lời rất trúng, nhớ mọi thứ, gọi đúng tên, nhắc đúng mục tiêu. Người dùng thấy *"ổn rồi, nó hiểu mình rồi"*.
>
> Hôm sau mở đoạn chat mới. AI không biết họ là ai.

Vì toàn bộ thứ vừa rồi nằm trong **trí nhớ của đoạn chat đó**, không nằm trong file. Hết phiên là mất sạch.

Nguy hiểm ở chỗ **hai trường hợp trông giống hệt nhau từ phía người dùng**. Cách duy nhất phân biệt là mở một phiên hoàn toàn mới và hỏi lại.

Đây cũng là lý do bài test này là **nghiệm thu thật** của việc dựng bộ não — không phải một bước "cho chắc".

---

## Luật chạy bài test

⚠️ **Bắt buộc: mở ĐOẠN CHAT MỚI trên PROJECT MỚI.** Không chạy trong đoạn chat vừa dựng bộ não. Chạy trong đó thì AI vẫn nhớ mọi thứ từ ngữ cảnh phiên hiện tại, và bài test **luôn luôn đạt kể cả khi bộ não rỗng hoàn toàn** — một phép thử không thể trượt thì không chứng minh được gì.

Các bước:

1. Mở project mới / đoạn chat mới trong công cụ AI.
2. Cắm thư mục `SecondBrain` vào làm ngữ cảnh.
3. Hỏi lần lượt 5 câu dưới đây.
4. Đối chiếu câu trả lời với tiêu chí đạt.

---

## Câu 0 — hỏi TRƯỚC, để biết trượt là lỗi gì

> *"Đọc file `SecondBrain/wiki/goals.md` và cho tôi biết dòng đầu tiên của nó."*

Câu này không kiểm nội dung bộ não. Nó kiểm **công cụ có đọc được thư mục không** — và nó chia toàn bộ bài test thành hai nhánh chữa hoàn toàn khác nhau:

| Câu 0 | Nghĩa là | Mọi câu trượt sau đó là |
|---|---|---|
| ✅ đọc được | công cụ chạy tốt, file có thật trên đĩa | **lỗi NỘI DUNG** — trang chưa điền đủ. Ngồi điền tiếp, đừng đụng vào cài đặt |
| ❌ không đọc được | công cụ chưa thấy thư mục, hoặc file chưa từng được ghi ra | **lỗi CÔNG CỤ** — dừng bài test, đi sửa cài đặt trước |

⚠️ **Đừng bỏ câu này.** Không có nó, một bộ não lưu tốt nhưng mới điền được 2 trang sẽ ra điểm thấp giống hệt một bộ não chưa lưu được gì — hai vấn đề ngược nhau, hai cách chữa ngược nhau. Người gặp cảnh đó thường là người mới làm dở dang, tức người ít khả năng tự phân biệt nhất, và họ sẽ mất cả buổi đi sửa thứ không hỏng.

---

## 5 câu hỏi kiểm chứng

Hỏi **từng câu một**, không gộp. Sau mỗi câu, tự chấm đạt/không đạt trước khi đi tiếp.

### Câu 1 — Danh tính

> *"Tôi là ai, đang làm gì, cho ai?"*

| Đạt | Không đạt |
|---|---|
| Trả lời đúng tên, đúng nghề, đúng nhóm khách hàng bạn phục vụ | Trả lời chung chung kiểu "bạn là một người sáng tạo nội dung"; hoặc hỏi ngược lại "bạn có thể cho tôi biết thêm về bạn không" |

### Câu 2 — Mục tiêu và nút thắt

> *"Mục tiêu 90 ngày tới của tôi là gì, và nút thắt lớn nhất đang là gì?"*

| Đạt | Không đạt |
|---|---|
| Nêu đúng con số mục tiêu và đúng nút thắt bạn đã khai | Nói mục tiêu chung chung không có số; hoặc bịa ra một nút thắt bạn chưa từng nói |

### Câu 3 — Điều cấm ⚡

> *"Có điều gì bạn tuyệt đối không được làm thay tôi?"*

| Đạt | Không đạt |
|---|---|
| Đọc đúng các hard don'ts trong `ai-operating-preferences.md` | Trả lời đạo đức chung chung kiểu "tôi sẽ không làm điều gì gây hại" |

📌 Câu này quan trọng nhất trong năm câu. Nó kiểm hai thứ cùng lúc: bộ não có lưu thật không, **và** trang `ai-operating-preferences` có được đọc không. Trang đó là trang duy nhất cả hệ thống yêu cầu đọc đầu mỗi phiên.

### Câu 4 — Chi tiết chỉ mình bạn biết

> *"[Một chi tiết cụ thể bạn vừa nạp — tên một khách hàng, một con số, một câu chuyện]. Kể lại cho tôi nghe."*

Tự chọn một chi tiết **cụ thể, không đoán được từ ngoài**. Ví dụ: *"Khách tên X đang ở tình trạng nào?"* hoặc *"Bước ngoặt lớn nhất trong hành trình của tôi là gì?"*

| Đạt | Không đạt |
|---|---|
| Kể đúng chi tiết, đúng tên, đúng số | Kể một phiên bản na ná nhưng sai chi tiết → **đây là bịa, không phải nhớ** |

⚠️ Sai ở câu này nguy hiểm hơn không trả lời được. Không trả lời được = biết là thiếu. Trả lời sai mà nghe hợp lý = bạn sẽ tin và dùng luôn.

### Câu 5 — Giọng văn

> *"Viết cho tôi 3 câu mở đầu một bài đăng, theo đúng giọng của tôi."*

| Đạt | Không đạt |
|---|---|
| Dùng đúng đại từ bạn đã khai, tránh đúng những cụm bạn đã cấm | Dùng sai đại từ, hoặc dùng ngay một cụm nằm trong danh sách cấm |

*(Chưa dựng `voice-profile` vì chưa đủ 10 bài thì bỏ qua câu này — nhưng phải ghi rõ là bỏ qua, không tính là đạt.)*

---

## Chấm kết quả

**Đọc bảng này theo Câu 0 trước, rồi mới đếm điểm.**

### Nhánh A — Câu 0 ✅ (công cụ chạy tốt)

| Số câu đạt | Kết luận | Làm gì tiếp |
|---|---|---|
| **5/5** | Bộ não đã lưu thật, chạy được | Sang Việc 7 |
| **3–4/5** | Có lưu, thiếu nội dung ở vài trang | Xem câu nào trượt → mở đúng trang tương ứng → bổ sung → chạy lại **từ đầu, trên phiên mới** |
| **0–2/5** | ⚠️ **Không phải bộ não hỏng — là bạn mới điền được rất ít.** Đây là chuyện bình thường của người vừa bắt đầu | Quay lại **Việc 4**, điền cho đủ 11 trang neo. **Đừng đụng vào cài đặt, công cụ không hỏng** — Câu 0 vừa chứng minh điều đó |

### Nhánh B — Câu 0 ❌ (công cụ chưa đọc được)

Dừng bài test, **không cần hỏi 5 câu kia** — chúng sẽ trượt hết vì cùng một nguyên nhân. Kiểm theo thứ tự:

1. Thư mục `SecondBrain/wiki/` có file `.md` thật không? *(mở bằng trình quản lý file, nhìn bằng mắt)*
2. Có file mà AI không đọc được → **lỗi cắm ngữ cảnh**: workspace đang trỏ sai thư mục.
3. Không có file nào → bộ não **chưa bao giờ được ghi ra đĩa**. Đây mới đúng là cái bẫy mà bài test này sinh ra để bắt: buổi phỏng vấn hôm trước chỉ nằm trong trí nhớ đoạn chat. Quay lại **Việc 2 và Việc 3**, làm lại trên công cụ bậc 2.

**Trượt câu nào thì trang nào phải sửa:**

| Câu trượt | Mở trang |
|---|---|
| 1 | `about-me.md` |
| 2 | `goals.md` |
| 3 | `ai-operating-preferences.md` |
| 4 | trang chứa chi tiết đó (`customers.md`, `experiences-library.md`…) |
| 5 | `voice-profile.md` |

---

## Sau khi đạt

Ghi một dòng vào `log.md`:

```
## [YYYY-MM-DD] Kiểm chứng Việc 6 | 5/5 đạt — bộ não đã lưu thật
```

Rồi nói với người dùng đúng một ý: từ giờ mỗi lần nạp một khối dữ liệu lớn, chạy lại bài này. Nó rẻ (5 phút) và nó là thứ duy nhất phân biệt được *"AI đang nhớ"* với *"bộ não đang lưu"*.

---

## Ghi chú cho AI chạy skill này

- **Không tự chấm hộ người dùng.** Đưa câu hỏi, để họ tự đọc câu trả lời và tự đối chiếu. Bài test này chỉ có giá trị khi chính chủ nhìn thấy kết quả bằng mắt mình.
- Nếu người dùng đang chạy bài test **trong chính đoạn chat vừa dựng bộ não** — dừng lại, nói rõ vì sao không hợp lệ, yêu cầu mở phiên mới. Đây là lỗi hay gặp nhất và nó làm bài test mất sạch giá trị.
- Không an ủi khi trượt. Trượt ở đây là tin tốt: nó lộ ra vấn đề lúc còn dễ sửa, thay vì ba tháng sau.
