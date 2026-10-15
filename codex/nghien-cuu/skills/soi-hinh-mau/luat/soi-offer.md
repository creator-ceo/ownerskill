# Modeling hệ thống chuyển đổi — soi offer và phễu của người khác

> 📎 **Đọc file này thế nào.** Liên kết `[[tên-trang]]` trỏ tới trang trong bộ não **của bạn** (thư mục `wiki/`). Trang nào bạn chưa có thì **bỏ qua** — đừng đoán nội dung, đừng bịa cho đủ. Muốn có trang tương đương thì dựng bằng `$nap-kho`.
> Tên người và con số trong file là **ví dụ minh hoạ** cách soi. 🚫 Đừng bê kết luận về họ thành kết luận của bạn — hình mẫu của bạn là người khác.


> Hệ thống chuyển đổi cũng cần có hình mẫu: thu hút có hình mẫu rồi, nhưng chuyển đổi cũng phải học từ người đi trước.
>
> Đọc `luat/loi-modeling.md` trước: 4 tiêu chí chọn hình mẫu và luật lọc theo bằng chứng nằm ở đó, áp cho mọi lĩnh vực. Trang này chỉ định nghĩa **soi cái gì** khi đối tượng là một hệ thống bán hàng.
>
> Chỗ đặt kết quả: `wiki/models-pheu/<slug>.md`. **Không đặt vào `wiki/models/`** — lý do kỹ thuật ở `luat/loi-modeling.md`.

---

## Lớp soi = chính Bản thiết kế offer mình đang dùng

Không nghĩ khuôn mới. Soi offer người khác bằng **đúng 12 mục** mình dùng để dựng offer mình (bản thiết kế offer của bạn; chưa có thì dựng bằng `$nap-kho`, loại thiết kế offer). Cùng một thước thì so được, và chỗ họ có mà mình trống thì lộ ra ngay.

| # | Mục | Câu hỏi khi soi người khác |
|---|---|---|
| 1 | Câu một dòng | Họ hứa **một** kết quả gì, cho ai, trong bao lâu? |
| 2 | Cơ chế | Cơ chế của họ **tên là gì**? Có tên riêng không? |
| 3 | Kết quả & thắng đầu tiên | Thắng đầu tiên họ cho khách là gì, sau bao lâu? |
| 4 | Các tầng offer | Lõi · Hỗ trợ · Giữ nhịp · Tài sản, đủ mấy tầng? |
| 5 | Quà kèm | Quà kèm phục vụ trụ nào của Phương trình giá trị? |
| 6 | Cam kết hoàn tiền | Họ **đảo rủi ro** bằng cách nào, hay không đảo? |
| 7 | Bản đồ lời từ chối | Lời từ chối nào họ xử bằng **thành phần** chứ không bằng câu chữ? |
| 8 | Giá | Bậc thang thế nào, giá nào **công khai** và giá nào **giấu**? |
| 9 | Lý do gấp & khan hiếm | Lý do gấp của họ **thật hay dựng**? |
| 10 | Đặt tên | Tên offer và tên framework đặt theo công thức gì? |
| 11 | Lời chào bán | Họ nói gọn cả offer trong mấy câu? |
| 12 | **Câu chào hai dòng** | Hai dòng đầu trang bán viết thế nào — dòng nào là kết quả, dòng nào là cơ chế, và **kết bằng cái gì**? |

> ⚡ **Mục 12 sinh ra từ chính việc soi.** Một trang bán nổi tiếng dùng đúng hai dòng đầu: một dòng nói kết quả, một dòng nói cơ chế. Nếu bản thiết kế offer của bạn không có ô nào cho lời chào đối ngoại, kết quả sẽ bị nhồi vào **tên sản phẩm**, và tên hết hạn ngay khi offer đổi hướng.

---

## Bốn lớp riêng, không có trong Bản thiết kế

Bản thiết kế dùng để **dựng** offer của bạn. Soi người khác thì cần thêm bốn lớp nữa:

### A. Thang bậc và vai trò từng bậc

Không chỉ ghi giá. Ghi **việc của mỗi bậc**: bậc nào để bắt chú ý, bậc nào để lọc người chịu móc ví, bậc nào để tạo thói quen mua, bậc nào là chỗ ra tiền thật.

Một thang 7 bậc từ 29 USD tới 68.000 USD không phải 7 sản phẩm. Nó là **một cái sàng có 7 mắt lưới**.

### B. Chặng phễu và cơ chế mỗi chặng

`người lạ chú ý → người quan tâm → chốt đơn → khách hàng → nâng bậc`

Mỗi chặng hỏi đúng hai câu: **cơ chế nào đẩy người ta sang chặng sau**, và **tài sản thật nào đang gánh chặng đó**. Chặng nào không chỉ ra được tài sản thì đó là chặng đứt.

### C. Cách lọc khách — ai bị loại, loại bằng gì

Chỗ này hay bị bỏ qua mà lại là chỗ khác biệt lớn nhất giữa một offer khoẻ và một offer chạy theo số lượng.

Lọc bằng **giá** · bằng **ngưỡng điều kiện** (*"chỉ nhận người đã 30K USD/tháng"*) · bằng **nội quy** · bằng **câu chào** viết thẳng ra ngưỡng.

⚡ Đối chiếu với [[target-customer]]: nếu bạn có nội quy nghiêm, nó **vừa là rào cản vừa là bộ lọc**. Xem người khác lọc thế nào để biết mình đang lọc quá tay hay chưa đủ.

### D. Cái gì họ giấu, cái gì họ công khai

Giá công khai tới bậc nào rồi bắt đặt lịch? Cơ chế nói ra tới đâu? Bằng chứng cho xem loại nào?

Đây là lớp trả lời trực tiếp câu bạn phải quyết mỗi lần viết một trang bán hàng: nói ra tới đâu thì đủ tin, giấu tới đâu thì còn lý do để họ liên hệ.

---

## ⛔ Ba thứ soi xong thì GHI LẠI ĐỂ BỎ, không mang về

`luat/loi-modeling.md` ghi luật *"lấy phần này bỏ phần kia"*. Với hệ thống chuyển đổi, ba thứ dưới đây gần như chắc chắn sẽ gặp và gần như chắc chắn phải bỏ:

1. **Khan hiếm dựng lên.** Đếm ngược giả, "còn 3 suất" nói mãi, hạn chót gia hạn. Loại này ai cũng nhận ra là giả; nếu bạn có `wiki/objections-library.md` thì đối chiếu ở đó.
2. **Tín hiệu bơm.** Engagement pod, mua tương tác, và mọi thao tác **né phát hiện** (gỡ tham số theo dõi, sửa bài sau khi đã lên). Đây là ranh giới cứng.
3. **Mượn hào quang.** Đặt một con số lớn cạnh tên mình mà con số đó không thuộc về mình.

📌 Ba thứ này bỏ **không phải vì không hiệu quả**. Bỏ vì chúng va vào nguyên tắc làm nghề trung thực của bạn, và vì khách của bạn có thể sợ nhất là bị gọi *"lùa gà"* (xem `wiki/customer-voice.md` nếu có). Cái gì hiệu quả với người khác mà bật đúng nỗi sợ đó thì với bạn là lỗ, không phải lãi.

---

## Kết quả soi ghi ra sao

Mỗi hình mẫu một file `wiki/models-pheu/<slug>.md` trong bộ não của bạn, theo khuôn:

```markdown
# Hình mẫu chuyển đổi — <Tên>

## Hồ sơ
| Khoá | Giá trị |            ← ngách · quy mô · nguồn · ngày soi

## ⚠️ Đọc trước: cái gì kiểm chứng được, cái gì chỉ là lời họ nói

## Thang bậc                  ← lớp A
## Phễu — các chặng           ← lớp B
## Cách lọc khách             ← lớp C
## Giấu gì, công khai gì      ← lớp D
## Soi theo Bản thiết kế 12 mục  ← bảng 12 dòng
## ⛔ Va chạm giá trị — phần KHÔNG được chép
## Lấy gì · Bỏ gì
## Đối chiếu với offer của bạn

```

Mục **Đối chiếu với offer của bạn** là mục bắt buộc, và là lý do cả trang tồn tại. Soi xong mà không nói được *chỗ này họ có mình trống* thì mới chỉ là đọc, chưa phải modeling.

---

## Hình mẫu nên soi trước

Chọn 2–3 người theo 4 tiêu chí ở `luat/loi-modeling.md`. Gợi ý nhóm đáng soi: người có thang bậc sản phẩm rõ (từ rẻ tới đắt), người bán membership/cộng đồng, người chạy phễu theo đợt. Với mỗi người, nếu phân tích chuyển đổi đang nằm lẫn trong trang hình mẫu **nội dung**, hãy **chuyển** sang trang riêng ở `wiki/models-pheu/` rồi để lại một dòng trỏ — **không chép thành bản thứ hai**.

---

## Links

`luat/loi-modeling.md` · [[offer-ladder]] · [[objections-library]] · [[target-customer]] · `luat/soi-noi-dung.md` · [[competitors]]
