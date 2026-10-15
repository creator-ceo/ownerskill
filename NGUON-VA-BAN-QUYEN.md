# Nguồn và bản quyền

Gói này gộp hai thứ có nguồn gốc khác nhau. Trang này ghi rõ cái nào của ai, để bạn dùng lại mà không sợ sai luật.

---

## Tám vai của Đoàn — 22 skill, mỗi vai một gói

**© Tô Hải Đoàn.** Giấy phép **MIT** (xem [LICENSE](LICENSE)).

**20 trong 22 skill** do Đoàn tự nghiên cứu và xây dựng, không lấy từ nguồn nào. Bạn được dùng, sửa, và phân phối lại — chỉ cần giữ dòng ghi công trong file `LICENSE`.

Hai skill còn lại là phái sinh hoặc áp dụng phương pháp của người khác: `/soi-doi-thu` (xem ngay dưới) và `/nghien-cuu-e5`, áp dụng phương pháp E5 của Todd Brown, đã ghi công ngay đầu và cuối file skill.

*(Thêm 2026-09-04: `/dieu-hanh` — vai điều phối đội nhân sự A.I. Tự viết, không lấy từ nguồn nào.)*

### ⚠️ `/soi-doi-thu` KHÔNG phải của Đoàn

`/soi-doi-thu` là **bản Việt hoá phái sinh** từ `competitor-profiling` của Corey Haines (MIT). Nó nằm ở nhóm `cua-doan/` vì cần đi cặp với `/soi-hinh-mau` — hai skill trỏ sang nhau để không giành trigger; tách ra hai nhóm thì cặp đó gãy khi học viên chỉ cài một nhóm.

Hai chỗ đổi thật so với bản gốc, không chỉ là dịch:
- **Chạy được không cần công cụ trả phí.** Bản gốc bắt buộc Firecrawl + DataForSEO và không có đường lui; bản này đọc trực tiếp, và chỉ ra rằng với mô hình nhân hiệu thì **bình luận và cộng đồng** mới là chỗ đáng đào — không công cụ SEO nào đọc hộ được.
- **Soi người làm nhân hiệu**, không soi công ty SaaS. Bỏ các ô Funding / HQ / Domain rank / Integrations; thêm mục **khe hở** (nhóm khách nào họ đang bỏ) và mục cách bán 1-1 / webinar / nhóm kín.

Ghi công đầy đủ ở cuối chính file `soi-doi-thu/SKILL.md`.

### Thứ đã CỐ Ý không đưa vào gói

Vài skill trong nhóm này ở bản gốc trỏ vào hạ tầng riêng của Đoàn. Những chỗ đó đã được gỡ hoặc thay, không phải bị bỏ sót:

| Đã gỡ | Vì sao |
|---|---|
| Toàn bộ tham chiếu tới `owner-os/` | Bảng điều khiển Creator OS — phần mềm riêng, không nằm trong gói |
| `content-voice-masterfile.md` (589 dòng) | **Giọng riêng của Đoàn.** Bạn cần giọng của chính bạn, không phải giọng anh ấy. `/viet-content` sẽ đọc `wiki/voice-profile.md` của bạn |
| Font nhận diện riêng | Bản quyền không thuộc gói này. `/giai-thich-de-hieu` mặc định dùng Be Vietnam Pro (Google Fonts, OFL) |
| Khoá API quảng cáo | Không bao giờ nằm trong repo. `/soi-ads` đi kèm `.khoa/mau.env` rỗng để bạn tự điền |
| Số liệu kinh doanh, tên khách, tệp khách hàng | Dữ liệu riêng |

### Thứ ĐÃ đưa vào — 4 trang luật nghề

`/viet-content` mang theo `luat/` gồm 832 dòng luật viết mà Đoàn rút ra từ công việc thật:

| File | Nội dung |
|---|---|
| `luat/loi-nghe.md` | 10 luật lõi nghề + 7 khung viết |
| `luat/dau-hieu-ai-viet.md` | 4 tầng dấu hiệu văn AI |
| `luat/hook.md` | 8 kiểu hook + kỷ luật dùng hook |
| `luat/cau-chu.md` | Khuôn cần tránh, luật câu chữ |

`/soi-hinh-mau` mang theo `luat/` gồm 359 dòng luật modeling, rút sau 5+ vòng soi thật:

| File | Nội dung |
|---|---|
| `luat/loi-modeling.md` | Lõi phổ quát — 4 tiêu chí chọn, luật lọc theo bằng chứng |
| `luat/soi-noi-dung.md` | Soi thu hút — 5 lớp, 7 loại bằng chứng |
| `luat/soi-offer.md` | Soi chuyển đổi — 12 mục offer + 4 lớp phễu |

Nhân vật trong `khuon/hinh-mau-mau.md` là **hư cấu** — kết quả nghiên cứu thật của Đoàn (`wiki/models/`, 390KB) **không** nằm trong gói.

⚠️ Trong các file này có **ví dụ, con số và tên người của Đoàn** — chúng ở đó để minh hoạ luật. Đừng bê chúng vào bài của bạn: đó là vi phạm chính luật cấm bịa mà chúng đang dạy.

---

## Nhóm `tong-hop/` — 41 skill

**© Corey Haines.** Giấy phép **MIT** — bản gốc kèm theo tại [`tong-hop/LICENSE-marketingskills`](tong-hop/LICENSE-marketingskills).

| | |
|---|---|
| **Nguồn** | https://github.com/coreyhaines31/marketingskills |
| **Số sao lúc đóng gói** | 45.826 ⭐ |
| **Phiên bản gốc** | 2.11.0 |
| **Ngày lấy về** | 2026-08-27 |
| **Đã sửa gì** | Không sửa một chữ nào trong nội dung skill |
| **Đã bỏ gì** | 9 skill thuần SaaS/app; thư mục `evals/` của mỗi skill (chỉ dùng để chạy test nội bộ) |

MIT cho phép phân phối lại kèm sửa đổi, với điều kiện giữ nguyên thông báo bản quyền — file `LICENSE-marketingskills` chính là thông báo đó.

### Cập nhật từ nguồn gốc

Repo gốc cập nhật thường xuyên. Lấy bản mới:

```bash
./scripts/cap-nhat-nguon.sh
```

Script tải bản mới nhất về, thay đúng 41 skill đã chọn, giữ nguyên tám gói vai. Xem `git diff` trước khi commit.

---

## Nguồn ĐÃ XÉT nhưng KHÔNG đưa vào

Ghi lại để bạn biết đã cân nhắc gì, và vì sao loại.

| Nguồn | ⭐ | Vì sao không đưa vào |
|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 171.972 | ⚠️ **Không có file LICENSE** → mặc định là giữ toàn quyền, phân phối lại là sai luật. Cài trực tiếp từ nguồn (xem dưới) |
| [obra/superpowers](https://github.com/obra/superpowers) | 278.391 | MIT, chất lượng cao — nhưng thiên về quy trình lập trình, không phục vụ mô hình thương hiệu cá nhân |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 25.061 | MIT, ~388 skill — nhiều nhưng chất lượng không đều. Nhồi hết vào làm Claude chọn nhầm skill |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 73.424 | Là **danh mục liệt kê**, không phải skill dùng được |

### Muốn thêm bộ skill chính chủ của Anthropic

Xử lý tài liệu (Word, Excel, PowerPoint, PDF), thiết kế, tạo skill mới:

```bash
claude plugin marketplace add anthropics/skills
```

Cài thẳng từ nguồn nên luôn đúng bản quyền và luôn là bản mới nhất.

---

## Một lưu ý về số lượng

Claude chọn skill bằng cách đọc **mô tả của mọi skill đang bật**. Bật càng nhiều thì càng dễ chọn nhầm.

51 skill là con số đã cân nhắc, không phải giới hạn kỹ thuật. Nếu bạn thấy Claude hay chọn sai, hãy tắt bớt nhóm bạn ít dùng:

```bash
claude plugin disable tong-hop
```

---

## Vai Editor (gói `editor`)

**© Tô Hải Đoàn.** Giấy phép **MIT**. Font Be Vietnam Pro kèm trong `editor/skills/dung-video/fonts/` theo giấy phép OFL (file giấy phép nằm cạnh font).

**Cố ý không đưa vào gói:** giọng đọc nhân bản, khuôn mặt và video mẫu, nhạc nền, bộ lọc màu theo máy quay, kho cảnh quay và nhãn cảnh, tài khoản và khoá đăng bài. Đây là tài sản riêng của từng người, mỗi người tự có của mình.
