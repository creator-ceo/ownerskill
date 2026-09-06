# Bắt đầu từ đây

Trang này viết cho người **chưa quen dòng lệnh**. Làm theo từng bước, không cần hiểu gì thêm.

---

## Bước 1 — Cài Claude Code (bỏ qua nếu đã có)

Mở **Terminal** (máy Mac: bấm `Cmd + dấu cách`, gõ "Terminal", Enter) rồi dán dòng này:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Xong thì gõ `claude` để kiểm tra. Thấy Claude chào là được.

---

## Bước 2 — Thêm kho skill

Dán dòng này vào Terminal:

```bash
claude plugin marketplace add creator-ceo/creator-skills
```

Nó chỉ **thêm địa chỉ kho** vào máy bạn, chưa cài gì cả.

---

## Bước 3 — Cài skill

Dán dòng này để cài 10 skill của Tô Hải Đoàn:

```bash
claude plugin install cua-doan@creator-skills
```

Và dòng này để cài 41 skill marketing:

```bash
claude plugin install tong-hop@creator-skills
```

> Cài một nhóm trước cũng được. Đổi ý lúc nào cũng cài thêm được.

---

## Bước 4 — Kiểm tra

```bash
claude plugin list
```

Thấy `cua-doan` và `tong-hop` trong danh sách là xong.

Giờ mở Claude Code ở thư mục bạn muốn làm việc, gõ dấu `/` — danh sách skill sẽ hiện ra.

---

## Bước 5 — Chạy đúng thứ tự

Đây là phần quan trọng nhất, và cũng là chỗ nhiều người làm ngược rồi thất vọng.

### Ba việc đầu tiên, làm theo đúng thứ tự này

```
1. /banh-xe-cuoc-doi     ← nhìn lại cuộc sống, đặt mục tiêu 10 năm / 90 ngày
2. /onboard              ← dựng bộ não thứ 2 của bạn
3. /kiem-chung           ← kiểm tra bộ não đã lưu THẬT vào file chưa
```

**Vì sao phải theo thứ tự này:** các skill làm thành phẩm (`/viet-content`, `/anh-quote`, `/giai-thich-de-hieu`) đều **đọc từ bộ não của bạn** — giọng của bạn, chuyện thật của bạn, khách của bạn. Bộ não còn trống thì chúng không có gì để bám, và bài viết ra sẽ **đúng nhưng không thật** — nghe như ai cũng viết được.

Đây không phải lời khuyên cho vui. Bước `/kiem-chung` sinh ra vì một cái bẫy có thật: bạn ngồi kể chuyện cả buổi, AI trả lời rất hay, bạn tưởng nó đã nhớ — nhưng thật ra **chưa có dòng nào được ghi vào file**. Đóng chat là mất sạch.

### Sau đó, dùng hằng ngày

| Muốn gì | Gõ |
|---|---|
| Lưu một chuyện, một insight vào bộ não | `/nap-kho` |
| Viết bài, hook, kịch bản video | `/viet-content` |
| Biến một câu thành ảnh đăng | `/anh-quote` |
| Giải thích một thứ khó bằng hình | `/giai-thich-de-hieu` |
| Soi quảng cáo Facebook / Google | `/soi-ads` |
| Soi một người đi trước để **học theo** | `/soi-hinh-mau` |
| Soi **đối thủ** đang tranh khách với mình | `/soi-doi-thu` |

Không nhớ tên skill cũng không sao — **cứ nói bằng lời thường**. Nói *"viết giúp tôi bài về lần tôi mất khách lớn nhất"* thì Claude tự gọi `/viet-content`.

---

## Vài điều nên biết trước

**Bộ não của bạn nằm trong file, không nằm trong chat.** Nó là thư mục `wiki/` gồm các file `.md` bạn mở ra đọc được bằng mắt. Không có tài khoản, không có đám mây, không ai khác đọc được.

**Chỉ có một đường ghi vào bộ não: `/nap-kho`.** Nghe thì phiền, nhưng đây là thứ giữ cho bộ não không mục sau vài tháng. Sửa thẳng file `.md` thì nhanh hơn — và sau vài tuần bạn sẽ có cùng một chuyện nằm ở ba trang, hai trang nói ngược nhau, không biết trang nào mới.

**`/soi-ads` mặc định bị khoá.** Nó tiêu tiền quảng cáo thật, nên cài xong là khoá cứng cho tới khi bạn tự điền tài khoản và hạn mức vào `luat.json`. Chạy `node bo-may/kiem.mjs` để xem còn thiếu ô nào.

**Skill nhóm `tong-hop` viết bằng tiếng Anh.** Không sao — bạn cứ hỏi bằng tiếng Việt, Claude trả lời bằng tiếng Việt. Tiếng Anh chỉ là ngôn ngữ của tài liệu bên trong.

---

## Khi thấy Claude chọn nhầm skill

Bật nhiều skill quá thì Claude dễ chọn nhầm. Tắt bớt nhóm ít dùng:

```bash
claude plugin disable tong-hop
```

Bật lại:

```bash
claude plugin enable tong-hop
```

---

## Gỡ ra

```bash
claude plugin uninstall cua-doan
```

Gỡ skill **không xoá bộ não của bạn** — `wiki/` là file của bạn, nằm trong thư mục của bạn.

---

## Kẹt thì nhắn tôi

Hướng dẫn trên viết cho người chưa quen dòng lệnh, nhưng máy mỗi người một khác nên vẫn có thể vướng.

Vướng ở bước nào, hoặc cài xong mà không biết dùng vào việc gì của mình, thì nhắn thẳng cho tôi — **[facebook.com/tohaidoan](https://www.facebook.com/tohaidoan/)**. Chụp màn hình chỗ báo lỗi kèm theo là nhanh nhất.

— Tô Hải Đoàn

