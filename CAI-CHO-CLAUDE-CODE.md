# Cài cho Claude Code

Trang này dành cho người dùng **Claude Code**, viết cho người **chưa quen dòng lệnh**. Dùng Codex thì đọc [CAI-CHO-CODEX.md](CAI-CHO-CODEX.md). Làm theo từng bước, không cần hiểu gì thêm.

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
claude plugin marketplace add creator-ceo/ownerskill
```

Nó chỉ **thêm địa chỉ kho** vào máy bạn, chưa cài gì cả.

---

## Bước 3 — Cài vai bạn cần

Mỗi vai là một gói riêng. **Vai Thủ thư cài trước**, vì các vai khác đọc và ghi vào kho của nó:

```bash
claude plugin install thu-thu@ownerskill
```

Rồi cài thêm vai bạn cần, mỗi vai một dòng. Ví dụ vai Content:

```bash
claude plugin install content@ownerskill
```

Các vai khác: `nghien-cuu` · `tong-giam-doc` · `editor` · `ban-hang` · `cham-soc` · `phat-trien-san-pham`. Thay tên vai vào dòng lệnh trên.

> Vai Editor cần cài ffmpeg trước và chỉ dựng được video trên Mac chip Apple. Đổi ý lúc nào cũng cài thêm vai được.

---

## Bước 4 — Kiểm tra

```bash
claude plugin list
```

Thấy các vai bạn vừa cài (ví dụ `thu-thu`, `content`) trong danh sách là xong.

Giờ mở Claude Code ở thư mục bạn muốn làm việc, gõ dấu `/` — danh sách skill sẽ hiện ra.

---

## Bước 5 — Chạy đúng thứ tự

Đây là phần quan trọng nhất, và cũng là chỗ nhiều người làm ngược rồi thất vọng.

### Không biết bắt đầu từ đâu?

Gõ `/chay-chuoi-dau-tien`. Nó đọc sổ đội, cho bạn biết đang ở bước nào và bước kế tiếp là gì.

### Mỗi vai cài xong thì gõ một lệnh thiết lập

```
vai Thủ thư        → /cai-thu-thu         dựng kho tài liệu, dạy cách nạp
vai Nghiên cứu     → /cai-nghien-cuu      hiểu khách và đối thủ
vai Tổng giám đốc  → /cai-tong-giam-doc   chốt mục tiêu và việc của tháng
vai Content        → /cai-content         giọng của bạn, kế hoạch, bài đầu tiên
vai Editor         → /cai-editor          dựng video (cần Mac chip Apple)
```

**Thứ tự gợi ý** là từ trên xuống, vì mỗi vai đọc thứ vai trước dựng. Bạn không cần có đủ vai: mỗi lệnh thiết lập sẽ nói vai nào bắt buộc (luôn là Thủ thư), vai nào nên có, và hỏi bù phần còn thiếu nếu bạn bỏ qua. Nhưng đội càng đủ thì bài ra càng sát bạn.

Thủ thư kết thúc bằng `/kiem-chung`, sinh ra vì một cái bẫy có thật: bạn ngồi kể chuyện cả buổi, AI trả lời rất hay, bạn tưởng nó đã nhớ, nhưng thật ra chưa lưu vào file nào. Mở một đoạn chat mới là mất sạch. `/kiem-chung` bắt bạn kiểm điều đó ngay.

Không biết đang ở bước nào thì gõ `/chay-chuoi-dau-tien`.

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
| Dựng clip ngồi nói thành video | `/dung-video` |
| Lập kho cảnh quay để tra B-roll | `/xuong-video` |
| Nghiên cứu khách và đối thủ | `/nghien-cuu-e5` |
| Lập kế hoạch content một tháng | `/viet-content` |

Không nhớ tên skill cũng không sao — **cứ nói bằng lời thường**. Nói *"viết giúp tôi bài về lần tôi mất khách lớn nhất"* thì Claude tự gọi `/viet-content`.

---

## Vài điều nên biết trước

**Bộ não của bạn nằm trong file, không nằm trong chat.** Nó là thư mục `wiki/` gồm các file `.md` bạn mở ra đọc được bằng mắt. Không có tài khoản, không có đám mây, không ai khác đọc được.

**Chỉ có một đường ghi vào bộ não: `/nap-kho`.** Nghe thì phiền, nhưng đây là thứ giữ cho bộ não không mục sau vài tháng. Sửa thẳng file `.md` thì nhanh hơn — và sau vài tuần bạn sẽ có cùng một chuyện nằm ở ba trang, hai trang nói ngược nhau, không biết trang nào mới.

**`/soi-ads` mặc định bị khoá.** Nó tiêu tiền quảng cáo thật, nên cài xong là khoá cứng cho tới khi bạn tự điền tài khoản và hạn mức vào `luat.json`. Chạy `node bo-may/kiem.mjs` để xem còn thiếu ô nào.

---

## Khi thấy Claude chọn nhầm skill

Bật nhiều skill quá thì Claude dễ chọn nhầm. Gỡ bớt vai ít dùng:

```bash
claude plugin uninstall <tên vai>@ownerskill
```

Cài lại lúc nào cũng được:

```bash
claude plugin install <tên vai>@ownerskill
```

---

## Gỡ ra

```bash
claude plugin uninstall content
```

Gỡ skill **không xoá bộ não của bạn** — `wiki/` là file của bạn, nằm trong thư mục của bạn.

---

## Kẹt thì nhắn tôi

Hướng dẫn trên viết cho người chưa quen dòng lệnh, nhưng máy mỗi người một khác nên vẫn có thể vướng.

Vướng ở bước nào, hoặc cài xong mà không biết dùng vào việc gì của mình, thì nhắn thẳng cho tôi — **[facebook.com/tohaidoan](https://www.facebook.com/tohaidoan/)**. Chụp màn hình chỗ báo lỗi kèm theo là nhanh nhất.

— Tô Hải Đoàn

