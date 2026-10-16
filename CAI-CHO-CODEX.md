# Cài cho Codex

Trang này dành cho người dùng **Codex** (công cụ lập trình A.I của OpenAI), viết cho người **chưa quen dòng lệnh**. Dùng Claude Code thì đọc [CAI-CHO-CLAUDE-CODE.md](CAI-CHO-CLAUDE-CODE.md).

Bản Codex có nội dung giống bản Claude Code. Khác ở cách gọi skill và cách cài, nên có file riêng.

---

## Bước 1 — Cài Codex (bỏ qua nếu đã có)

Làm theo hướng dẫn chính thức của OpenAI: [developers.openai.com/codex](https://developers.openai.com/codex). Cài xong, mở Terminal (máy Mac: bấm `Cmd + dấu cách`, gõ "Terminal", Enter) rồi gõ `codex`. Thấy Codex mở lên là được.

---

## Bước 2 — Thêm kho skill

Dán dòng này vào Terminal:

```bash
codex plugin marketplace add creator-ceo/ownerskill
```

Nó chỉ **thêm địa chỉ kho** vào máy bạn, chưa cài gì cả.

---

## Bước 3 — Cài vai bạn cần

Mỗi vai là một gói riêng. **Vai Thủ thư cài trước**, vì các vai khác đọc và ghi vào kho của nó.

1. Mở Codex (gõ `codex` trong Terminal).
2. Gõ `/plugins`. Một danh sách hiện ra.
3. Chọn kho **Ownerskill**, rồi chọn gói **thu-thu** và cài.
4. Làm tương tự cho vai khác bạn cần.
5. **Thoát Codex và mở lại một phiên mới.** Skill của gói chỉ dùng được từ phiên mới.

Bạn dùng ứng dụng Codex trên máy tính thay vì Terminal thì mở mục **Plugins Directory**, chọn kho Ownerskill, cài gói như trên rồi khởi động lại ứng dụng.

| Gói | Vai |
|---|---|
| `thu-thu` | Giữ kho tài liệu (cài đầu tiên) |
| `nghien-cuu` | Hiểu khách, đối thủ |
| `tong-giam-doc` | Chốt mục tiêu, việc của tháng |
| `content` | Viết bài, kịch bản, kế hoạch tháng |
| `editor` | Dựng video, ảnh (cần ffmpeg; dựng video chỉ chạy trên Mac chip Apple) |
| `ban-hang` | Offer, phễu, quảng cáo |
| `cham-soc` | Chăm sóc người đã mua |
| `phat-trien-san-pham` | Bài giảng, trang giải thích |

> **Đừng cài hết một lần.** Codex chỉ dành một phần nhỏ bộ nhớ làm việc để liệt kê skill. Cài quá nhiều thì mô tả bị rút gọn hoặc bỏ bớt, và Codex chọn sai skill. Chỉ cài vai bạn dùng.

---

## Bước 4 — Gọi skill

Trong Codex, skill gọi bằng dấu **`$`**, không phải dấu `/`:

```
$cai-thu-thu
```

Hoặc gõ `/skills` để chọn từ danh sách. Không nhớ tên cũng không sao, cứ nói bằng lời thường, Codex tự chọn skill hợp. Gọi bằng `$` thì chắc chắn.

---

## Bước 5 — Chạy đúng thứ tự

Mỗi vai cài xong thì gọi một lần lệnh thiết lập của nó:

```
vai Thủ thư        → $cai-thu-thu         dựng kho tài liệu, dạy cách nạp
vai Nghiên cứu     → $cai-nghien-cuu      hiểu khách và đối thủ
vai Tổng giám đốc  → $cai-tong-giam-doc   chốt mục tiêu và việc của tháng
vai Content        → $cai-content         giọng của bạn, kế hoạch, bài đầu tiên
vai Editor         → $cai-editor          dựng video (cần Mac chip Apple)
```

**Mở Codex trong một thư mục riêng** dành cho bộ não của bạn. Đó là nơi vai Thủ thư dựng kho (`raw/`, `wiki/`, `index.md`, `log.md`).

Thứ tự gợi ý là từ trên xuống, vì mỗi vai đọc thứ vai trước dựng. Bạn không cần có đủ vai, nhưng **Thủ thư luôn cần có trước**. Không biết đang ở bước nào thì gọi `$chay-chuoi-dau-tien`.

Sau đó dùng hằng ngày:

| Muốn gì | Gọi |
|---|---|
| Lưu một chuyện, một insight vào bộ não | `$nap-kho` |
| Viết bài, hook, kịch bản video | `$viet-content` |
| Biến một câu thành ảnh đăng | `$anh-quote` |
| Dựng clip ngồi nói thành video | `$dung-video` |
| Soi **đối thủ** | `$soi-doi-thu` |

---

## Vài điều khác với bản Claude Code

- Gọi skill bằng `$tên-skill` thay vì `/tên-skill`.
- Chỗ nào skill nói "chạy theo lịch hằng ngày" (ví dụ theo dõi một hình mẫu), bản Claude Code dùng nhiệm vụ theo lịch của nó. Với Codex bạn dùng tính năng chạy theo lịch của Codex nếu bản bạn dùng có, hoặc bỏ qua phần đó.
- Muốn tắt một skill mà không xoá, khai trong file cấu hình `~/.codex/config.toml` mục skill, đặt `enabled = false`.

## Vài điều nên biết trước

**Bộ não của bạn nằm trong file, không nằm trong chat.** Nó là thư mục `wiki/` gồm các file `.md` bạn mở ra đọc được bằng mắt.

**Chỉ có một đường ghi vào bộ não: `$nap-kho`.** Sửa thẳng file `.md` thì nhanh hơn, nhưng sau vài tuần sẽ có hai trang nói ngược nhau mà không ai biết.

**`$soi-ads` mặc định bị khoá.** Nó tiêu tiền quảng cáo thật, nên cài xong là khoá cứng cho tới khi bạn tự điền tài khoản và hạn mức.

**Bản Codex là bản mới.** Nó được sinh tự động từ bản Claude Code và chưa có nhiều người dùng thử. Gặp chỗ lạ thì nhắn tác giả ở cuối trang.

---

## Gỡ ra

```bash
codex plugin marketplace remove ownerskill
```

Gỡ skill **không xoá bộ não của bạn**. `wiki/` là file của bạn, nằm trong thư mục của bạn.

---

## Kẹt thì nhắn tôi

Cài không được, chạy ra kết quả lạ, hoặc muốn được hướng dẫn dùng cho đúng việc của bạn: **[facebook.com/tohaidoan](https://www.facebook.com/tohaidoan/)**
