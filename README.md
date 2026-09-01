# Creator Skills

**51 skill cho người kinh doanh dựa trên thương hiệu cá nhân.** Cài vào Claude Code một lần, dùng mãi.

Gói này chia làm **hai nhóm tách bạch**, và sự tách bạch đó là cố ý:

| Nhóm | Số skill | Là gì | Ngôn ngữ |
|---|---|---|---|
| ⭐ **`cua-doan`** | 10 | Do **Tô Hải Đoàn** tự nghiên cứu, tự dùng cho công việc thật, rồi đóng gói lại | Tiếng Việt |
| **`tong-hop`** | 41 | Tuyển chọn từ nguồn mở MIT chất lượng cao, giữ nguyên không sửa | Tiếng Anh |

Bạn cài được một nhóm, hoặc cả hai.

---

## Cài trong 2 phút

```bash
claude plugin marketplace add creator-ceo/creator-skills
```

Rồi cài nhóm bạn muốn:

```bash
claude plugin install cua-doan@creator-skills
```

```bash
claude plugin install tong-hop@creator-skills
```

Mở Claude Code lên, gõ `/` — bạn sẽ thấy các skill mới trong danh sách.

> 💡 Chưa quen dùng dòng lệnh? Đọc [BAT-DAU-TU-DAY.md](BAT-DAU-TU-DAY.md) — từng bước một, có hình dung rõ chuyện gì đang xảy ra.

---

## ⭐ Nhóm 1 — 10 skill của Tô Hải Đoàn

Đây là phần không mua được ở đâu khác: quy trình thật, đã chạy thật, có ghi lại cả những chỗ từng làm sai.

### Dựng và nuôi bộ não thứ 2

| Skill | Làm gì |
|---|---|
| `/onboard` | Dựng bộ não thứ 2 lần đầu — thu tài liệu có sẵn, phỏng vấn lấp chỗ trống, dựng `wiki/` theo 3 vòng |
| `/nap-kho` | **Đường ghi DUY NHẤT vào `wiki/`.** Đọc → phân tích → soi trùng → mới ghi. Không sửa thẳng file `.md` |
| `/kiem-chung` | Kiểm chứng bộ não đã **lưu thật vào file** chưa, hay chỉ nằm trong trí nhớ của đoạn chat |
| `/banh-xe-cuoc-doi` | Bánh Xe Cuộc Đời 8 khía cạnh + kế hoạch 10 năm / 90 ngày. Công cụ Đoàn dùng từ 2015 |

### Làm ra thành phẩm

| Skill | Làm gì |
|---|---|
| `/viet-content` | Viết bài, hook, kịch bản video, email — đúng giọng bạn, chống văn AI. **Mang theo 4 trang luật nghề** |
| `/anh-quote` | Biến một câu thành ảnh đăng. Bộ render tự chứa, font nhúng sẵn, không cần cài gì |
| `/giai-thich-de-hieu` | Biến khái niệm khó thành **một trang có hình** — người chưa biết gì đọc 60 giây là hiểu |
| `/soi-ads` | Soi và tối ưu quảng cáo Meta + Google. Có lớp chặn cứng, **không tiêu tiền khi bạn chưa gật** |

### Nghiên cứu người khác — hai việc khác hẳn nhau

| Skill | Họ là ai với bạn | Câu hỏi lõi |
|---|---|---|
| `/soi-hinh-mau` | Người bạn **học theo** | *Lấy gì? Bỏ gì?* — 3 tầng luật, 359 dòng, rút sau 5+ vòng soi thật |
| `/soi-doi-thu` | Người **tranh khách** với bạn | *Khác biệt ở đâu? Họ hở chỗ nào?* |

Gộp hai việc này làm một là hỏng cả hai. Mỗi skill tự chỉ sang skill kia khi bị gọi nhầm.

**Thứ tự nên chạy:** `/banh-xe-cuoc-doi` → `/onboard` → `/kiem-chung` → rồi mới tới nhóm làm thành phẩm.

Lý do: các skill làm thành phẩm đều **đọc từ `wiki/` của bạn** — giọng của bạn, chuyện của bạn, khách của bạn. `wiki/` còn trống thì chúng không có gì để bám, và bài viết ra sẽ đúng nhưng không thật.

---

## Nhóm 2 — 41 skill marketing tổng hợp

Tuyển từ [marketingskills](https://github.com/coreyhaines31/marketingskills) của Corey Haines — **45.800 sao trên GitHub**, giấy phép MIT, cập nhật liên tục.

Đã bỏ 9 skill thuần SaaS/app (`aso`, `paywalls`, `signup`, `programmatic-seo`, `schema`, `site-architecture`, `directory-submissions`, `revops`, `sms`) vì không hợp mô hình cá nhân.

<details>
<summary><b>Xem đủ 41 skill</b></summary>

**Offer & tiền:** `offers` · `pricing` · `lead-magnets` · `launch` · `free-tools`

**Viết & nội dung:** `copywriting` · `copy-editing` · `content-strategy` · `emails` · `cold-email` · `social` · `video` · `image`

**Khách hàng:** `customer-research` · `marketing-psychology` · `onboarding` · `churn-prevention` · `referrals` · `community-marketing`

**Đối thủ & định vị:** `competitors` · `competitor-profiling` · `product-marketing`

**Quảng cáo & chuyển đổi:** `ads` · `ad-creative` · `cro` · `ab-testing` · `popups`

**Đo lường:** `analytics` · `attribution`

**Tìm khách & bán:** `prospecting` · `sales-enablement`

**Lan toả:** `public-relations` · `influencer-marketing` · `co-marketing` · `events`

**SEO:** `seo-audit` · `ai-seo`

**Chiến lược:** `marketing-plan` · `marketing-ideas` · `marketing-loops` · `marketing-council`

</details>

---

## Hai nhóm này ăn khớp với nhau thế nào

Chúng không giẫm chân nhau — chúng làm hai việc khác nhau:

- **`tong-hop`** dạy bạn **kỹ thuật marketing**: cấu trúc một offer, đặt giá thế nào, chuỗi email gồm mấy bức.
- **`cua-doan`** lo phần **bạn là ai**: giọng của bạn, chuyện thật của bạn, khách của bạn, và luật để bài viết ra không nghe như AI viết.

Ví dụ một lượt làm việc thật:

```
/offers            → dựng cấu trúc offer (kỹ thuật, tiếng Anh)
/nap-kho           → nạp offer vừa dựng vào bộ não
/viet-content      → viết bài bán offer đó, bằng giọng của bạn
/anh-quote         → cắt câu chốt thành ảnh đăng
```

---

## An toàn — vì sao cài skill lạ là chuyện đáng cân nhắc

**Skill không phải phần mềm. Nó là văn bản ra lệnh cho AI** — và con AI đó đang ngồi trong máy bạn với quyền đọc file, chạy lệnh, gọi API. Cài skill của người lạ nghĩa là để họ viết chỉ thị cho nó.

41 skill nhóm `tong-hop` đã được soi trước khi đưa vào gói:

| Soi gì | Kết quả |
|---|---|
| File chạy được (`.sh`, `.py`, `.js`…) | **0** — toàn bộ chỉ là `.md` |
| Hook · MCP server · LSP *(thứ tự chạy, không cần bạn gõ gì)* | **0** |
| Lệnh phá hoại, leo quyền, tải-rồi-chạy | **0** |
| Endpoint gửi dữ liệu ra ngoài | **0** |
| Lệnh đọc `~/.ssh`, `.aws/credentials`, keychain | **0** |
| Chỉ thị ngầm (prompt injection) | 1 chỗ khớp mẫu — đã đọc tận nơi, là skill **dạy cách CHỐNG** injection |
| Đối chiếu với bản gốc trên GitHub | **41/41 khớp bit-for-bit** |

Bạn tự soi lại được, đừng tin lời tôi:

```bash
./scripts/soi-an-toan.sh tong-hop
```

Chạy được trên **bất kỳ** thư mục skill nào — kể cả skill bạn tải từ nơi khác.

### Ba điều máy quét KHÔNG che được

1. **Sạch theo máy quét ≠ an toàn tuyệt đối.** Skill vẫn là chỉ thị cho AI. Một skill hoàn toàn "sạch" vẫn có thể dạy AI làm việc theo cách bạn không muốn. Không gì thay được việc đọc `SKILL.md` của skill bạn dùng nhiều nhất.
2. **Bản cập nhật tương lai là bản chưa ai soi.** Repo bên thứ ba có thể đổi chủ hoặc bị chiếm. Vì thế skill được **chép cứng vào repo này** thay vì tải lúc chạy — và `cap-nhat-nguon.sh` **tự soi rồi dừng** nếu bản mới có gì đáng ngờ.
3. **`/soi-ads` tiêu tiền thật.** Đây là rủi ro lớn nhất trong cả gói, và nó nằm ở nhóm `cua-doan` chứ không phải nhóm người ngoài. Nó khoá cứng cho tới khi bạn tự điền `luat.json`, và không bao giờ áp thay đổi nếu bạn chưa gật **trong chính cuộc hội thoại đó**.

## Bản quyền

- **Nhóm `cua-doan`** — © Tô Hải Đoàn, giấy phép [MIT](LICENSE).
- **Nhóm `tong-hop`** — © Corey Haines, giấy phép MIT, giữ nguyên bản gốc kèm [file giấy phép](tong-hop/LICENSE-marketingskills).

Chi tiết đầy đủ và cách cập nhật từ nguồn gốc: [NGUON-VA-BAN-QUYEN.md](NGUON-VA-BAN-QUYEN.md).
