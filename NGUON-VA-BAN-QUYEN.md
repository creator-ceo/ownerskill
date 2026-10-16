# Nguồn và bản quyền

Trang này ghi rõ cái nào của ai, để bạn dùng lại mà không sợ sai luật.

---

## Tám vai của Đoàn — 22 skill, mỗi vai một gói

**© Tô Hải Đoàn.** Giấy phép **MIT** (xem [LICENSE](LICENSE)).

**20 trong 22 skill** do Đoàn tự nghiên cứu và xây dựng, không lấy từ nguồn nào. Bạn được dùng, sửa, và phân phối lại — chỉ cần giữ dòng ghi công trong file `LICENSE`.

Hai skill còn lại là phái sinh hoặc áp dụng phương pháp của người khác: `/soi-doi-thu` (xem ngay dưới) và `/nghien-cuu-e5`, áp dụng phương pháp E5 của Todd Brown, đã ghi công ngay đầu và cuối file skill.

*(Thêm 2026-09-04: `/dieu-hanh` — vai điều phối đội nhân sự A.I. Tự viết, không lấy từ nguồn nào.)*

### ⚠️ `/soi-doi-thu` KHÔNG phải của Đoàn

`/soi-doi-thu` là **bản Việt hoá phái sinh** từ `competitor-profiling` của Corey Haines (MIT). Nó nằm cùng gói `nghien-cuu` với `/soi-hinh-mau` vì hai skill trỏ sang nhau để không giành nhau. Thông báo bản quyền MIT của bản gốc kèm theo tại `nghien-cuu/skills/soi-doi-thu/LICENSE-marketingskills`.

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

## Vai Editor (gói `editor`)

**© Tô Hải Đoàn.** Giấy phép **MIT**. Font Be Vietnam Pro kèm trong `editor/skills/dung-video/fonts/` theo giấy phép OFL (file giấy phép nằm cạnh font).

**Cố ý không đưa vào gói:** giọng đọc nhân bản, khuôn mặt và video mẫu, nhạc nền, bộ lọc màu theo máy quay, kho cảnh quay và nhãn cảnh, tài khoản và khoá đăng bài. Đây là tài sản riêng của từng người, mỗi người tự có của mình.
