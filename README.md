# Ownerskill

**63 skill cho người làm thương hiệu cá nhân, chia theo từng vai trong một đội nhân sự A.I.** Mỗi vai là một gói riêng, bạn chọn vai cần và cài riêng từng vai.

Gói chia làm hai nhóm tách bạch, và sự tách bạch đó là cố ý:

| Nhóm | Số skill | Là gì | Ngôn ngữ |
|---|---|---|---|
| ⭐ **Tám vai của Tô Hải Đoàn** | 22 | Do **Tô Hải Đoàn** tự nghiên cứu, tự dùng cho công việc thật, rồi đóng gói lại. Mỗi vai một gói | Tiếng Việt |
| **`tong-hop`** | 41 | Tuyển chọn từ nguồn mở MIT chất lượng cao, giữ nguyên không sửa | Tiếng Anh |

## Cài trong 2 phút

Thêm kho một lần:

```bash
claude plugin marketplace add creator-ceo/ownerskill
```

Rồi cài **đúng vai bạn cần**, mỗi vai một dòng. Vai Thủ thư cài trước, vì các vai khác đọc và ghi vào kho của nó:

```bash
claude plugin install thu-thu@ownerskill
```

```bash
claude plugin install content@ownerskill
```

Mỗi vai có một lệnh thiết lập riêng (`/cai-thu-thu`, `/cai-content`…). Gõ lệnh đó một lần sau khi cài để vai biết về bạn. Rồi dùng skill của vai hằng ngày.

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

> 💡 Chưa quen dòng lệnh? Đọc [BAT-DAU-TU-DAY.md](BAT-DAU-TU-DAY.md) — từng bước một.

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
- **Tám vai của Đoàn** lo phần **bạn là ai**: giọng của bạn, chuyện thật của bạn, khách của bạn, và luật để bài viết ra không nghe như AI viết.

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
3. **`/soi-ads` tiêu tiền thật.** Đây là rủi ro lớn nhất trong cả gói, và nó nằm ở gói `ban-hang` của Đoàn chứ không phải nhóm `tong-hop`. Nó khoá cứng cho tới khi bạn tự điền `luat.json`, và không bao giờ áp thay đổi nếu bạn chưa gật **trong chính cuộc hội thoại đó**.

## Bản quyền

- **Tám vai của Đoàn** — © Tô Hải Đoàn, giấy phép [MIT](LICENSE).
- **Nhóm `tong-hop`** — © Corey Haines, giấy phép MIT, giữ nguyên bản gốc kèm [file giấy phép](tong-hop/LICENSE-marketingskills).

Chi tiết đầy đủ và cách cập nhật từ nguồn gốc: [NGUON-VA-BAN-QUYEN.md](NGUON-VA-BAN-QUYEN.md).
