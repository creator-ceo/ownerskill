# Ownerskill

**22 skill cho người làm thương hiệu cá nhân, chia theo từng vai trong một đội nhân sự A.I.** Mỗi vai là một gói riêng, bạn chọn vai cần và cài riêng từng vai.

Tất cả do **Tô Hải Đoàn** tự nghiên cứu, tự dùng cho công việc thật, rồi đóng gói lại. Tiếng Việt.

## Cài trong 2 phút

Bộ này chạy được trên **hai công cụ**, mỗi công cụ một cách cài và một file hướng dẫn riêng:

| Bạn dùng | Đọc hướng dẫn | Gọi skill bằng |
|---|---|---|
| **Claude Code** | [CAI-CHO-CLAUDE-CODE.md](CAI-CHO-CLAUDE-CODE.md) | `/tên-skill` |
| **Codex** | [CAI-CHO-CODEX.md](CAI-CHO-CODEX.md) | `$tên-skill` |

**Claude Code**: thêm kho một lần, rồi cài đúng vai bạn cần, mỗi vai một dòng.

```bash
claude plugin marketplace add creator-ceo/ownerskill
```
```bash
claude plugin install thu-thu@ownerskill
```

**Codex**: thêm kho một lần, rồi cài vai trong `/plugins`.

```bash
codex plugin marketplace add creator-ceo/ownerskill
```

Vai Thủ thư cài trước, vì các vai khác đọc và ghi vào kho của nó. Mỗi vai có một lệnh thiết lập riêng (`/cai-thu-thu`, `/cai-content`… hoặc `$cai-thu-thu`… trên Codex). Gọi lệnh đó một lần sau khi cài để vai biết về bạn. Bảng dưới ghi tên lệnh theo kiểu Claude Code.

| Gói | Vai | Skill | Làm gì |
|---|---|---|---|
| `thu-thu` | 🗂️ Thủ thư | `/cai-thu-thu` · `/nap-kho` · `/kiem-chung` · `/chay-chuoi-dau-tien` | Dựng và giữ kho tài liệu. **Cài đầu tiên**, các vai khác đọc từ kho này |
| `nghien-cuu` | 🔎 Nghiên cứu | `/cai-nghien-cuu` · `/nghien-cuu-e5` · `/tim-tam-guong` · `/soi-hinh-mau` · `/soi-doi-thu` | Hiểu khách, đối thủ, hình mẫu |
| `tong-giam-doc` | 🧭 Tổng giám đốc | `/cai-tong-giam-doc` · `/dieu-hanh` | Chốt mục tiêu 90 ngày, nút thắt, việc của tháng |
| `content` | ✍️ Content | `/cai-content` · `/viet-content` | Bài, hook, kịch bản, email, kế hoạch content một tháng đúng giọng bạn |
| `editor` | 🎞️ Editor | `/cai-editor` · `/dung-video` · `/xuong-video` · `/anh-quote` | Dựng video, kho cảnh quay, ảnh đăng. Dựng video chỉ chạy trên Mac chip Apple, cần ffmpeg |
| `ban-hang` | 💰 Bán hàng | `/ban-hang` · `/soi-ads` | Offer, trang bán, email bán, phễu, quảng cáo |
| `cham-soc` | 🤝 Chăm sóc | `/cham-soc` | Lo người đã trả tiền tới khi ra kết quả |
| `phat-trien-san-pham` | 📦 Phát triển sản phẩm | `/lam-khoa-hoc` · `/giai-thich-de-hieu` | Bài giảng, slide, bài tập, trang giải thích bằng hình |

> 💡 Chưa quen dòng lệnh? Mỗi file hướng dẫn ở trên đi từng bước một.

---

## Ai viết bộ này, và nhắn ở đâu khi kẹt

Tám vai do **Tô Hải Đoàn** viết — người làm nội dung và xây thương hiệu cá nhân tại Việt Nam.

Đây là quy trình tôi dùng cho công việc của chính mình mỗi ngày, không phải bộ skill dựng ra để phát. Vì thế nó có nhiều luật trông kỳ cục cho tới khi bạn gặp đúng tình huống nó sinh ra để chặn — phần lớn được rút từ chỗ tôi đã làm hỏng một lần.

Bạn dùng và sửa thoải mái, giấy phép MIT.

**Cài không được, chạy ra kết quả lạ, hoặc muốn được hướng dẫn dùng cho đúng việc của bạn** thì nhắn tôi ở đây: **[facebook.com/tohaidoan](https://www.facebook.com/tohaidoan/)**

---

## ⭐ Tám vai của Tô Hải Đoàn

Đây là phần không mua được ở đâu khác: quy trình thật, đã chạy thật, có ghi lại cả những chỗ từng làm sai.

**Thứ tự gợi ý khi dựng đội:** Thủ thư → Nghiên cứu → Tổng giám đốc → Content → Editor. Mỗi vai đọc thứ vai trước dựng, nhưng bạn không bắt buộc có đủ: mỗi lệnh `/cai-...` nói rõ vai nào cần, vai nào nên có, và hỏi bù phần còn thiếu. Riêng **Thủ thư luôn cần có trước**. Gõ `/chay-chuoi-dau-tien` để biết đang ở đâu.

**Nghiên cứu người khác — hai việc khác hẳn nhau** (trong gói `nghien-cuu`):

| Skill | Họ là ai với bạn | Câu hỏi lõi |
|---|---|---|
| `/soi-hinh-mau` | Người bạn **học theo** | *Lấy gì? Bỏ gì?* |
| `/soi-doi-thu` | Người **tranh khách** với bạn | *Khác biệt ở đâu? Họ hở chỗ nào?* |

Gộp hai việc làm một là hỏng cả hai. Mỗi skill tự chỉ sang skill kia khi bị gọi nhầm.

**Vai Editor:** cần cài [ffmpeg](https://ffmpeg.org) trước. Khâu dựng người ngồi nói hiện **chỉ chạy trên Mac chip Apple (M1 trở lên)**. Gói chỉ gồm công cụ dùng chung. Giọng đọc, khuôn mặt, nhạc nền, bộ lọc màu và kho cảnh quay là của riêng mỗi người nên không kèm theo.

---

## An toàn

**Skill không phải phần mềm thường. Nó là văn bản ra lệnh cho AI**, và con AI đó đang ngồi trong máy bạn với quyền đọc file và chạy lệnh. Cài skill của ai cũng nên đọc qua trước.

Với bộ này, bạn cần biết:

- **Một số skill có kèm file chạy được** (Python, JavaScript): `dung-video`, `xuong-video`, `anh-quote`, `soi-ads`, `giai-thich-de-hieu`. Chúng chỉ chạy khi bạn gọi skill, nằm trong thư mục `bo-may/` hoặc cạnh `SKILL.md`, và đọc được trước khi cài.
- **`/soi-ads` tiêu tiền thật.** Nó khoá cứng cho tới khi bạn tự điền tài khoản và hạn mức vào `luat.json`, và không thay đổi gì trong tài khoản quảng cáo khi bạn chưa gật.
- **Khoá và mật khẩu của bạn không bao giờ nằm trong repo.** Các skill cần khoá (Gemini, quảng cáo) đọc từ biến môi trường hoặc file riêng trên máy bạn.

Tự soi lại được, đừng tin lời tôi:

```bash
./scripts/soi-an-toan.sh
```

Máy quét sẽ liệt kê các file chạy được ở trên (cùng chỗ gọi mạng và chỗ đọc khoá của các skill đó). Đó là chủ ý, bạn đọc từng cái. Chạy được trên bất kỳ thư mục skill nào, kể cả skill bạn tải từ nơi khác. Sạch theo máy quét không có nghĩa là an toàn tuyệt đối, vì skill vẫn là chỉ thị cho AI. Không gì thay được việc đọc `SKILL.md`.

## Bản quyền

- **Tám vai của Đoàn** — © Tô Hải Đoàn, giấy phép [MIT](LICENSE).
- Riêng `/soi-doi-thu` phái sinh từ skill của Corey Haines (MIT), thông báo bản quyền kèm trong [thư mục skill](nghien-cuu/skills/soi-doi-thu/LICENSE-marketingskills).

Chi tiết đầy đủ: [NGUON-VA-BAN-QUYEN.md](NGUON-VA-BAN-QUYEN.md).
