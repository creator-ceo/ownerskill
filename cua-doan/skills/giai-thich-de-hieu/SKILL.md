---
name: giai-thich-de-hieu
description: Dùng khi bạn muốn biến một thứ khó hiểu thành một TRANG GIẢI THÍCH BẰNG HÌNH — ít chữ, sơ đồ có cơ chế, người chưa biết gì cũng hiểu. Kể cả khi chỉ nói "giải thích cái này cho dễ hiểu", "vẽ ra cho tôi xem cơ chế của X", "dạy member cái này thế nào cho dễ", "làm sơ đồ cho khái niệm này", "biến bài giảng này thành hình", "cái này giải thích cho người mới sao đây". Cũng dùng khi bạn dán đường dẫn một trang trong wiki/teachings/, wiki/models/, wiki/learnings/ kèm câu "làm thành trang giải thích", hoặc gõ /giai-thich-de-hieu <chủ đề>.
---

> 🧩 **Vai trong đội nhân sự A.I: Thiết kế.** Tổng giám đốc giao việc *ảnh chữ, trang giải thích, slide* cho vai này. Vai không phải một skill riêng — nó là nhãn để `/tong-giam-doc` biết giao việc gì cho skill nào.

# Giải thích dễ hiểu — Tô Hải Đoàn

Biến một khái niệm khó thành **một trang có hình** mà người chưa biết gì đọc 60 giây là hiểu.

Ra hai thứ, tuỳ bạn cần cái nào:

| Đầu ra | Là gì | Dùng để |
|---|---|---|
| **Trang artifact** *(mặc định)* | trang HTML publish lên link riêng, gửi được | dạy member, gửi trong nhóm VIP, nhúng vào bài giảng |
| **Ảnh PNG** *(khi bạn xin)* | 1080×1350, render qua bộ máy của `anh-quote` | đăng Facebook, làm slide |

## ⛩ CÀI VAI NÀY

**Nền cố định:** mục nhận diện trong `wiki/systems-and-stack.md` · `wiki/target-customer.md` · `wiki/experiences-library.md` *(nguồn phép so sánh — thiếu nó là rơi vào ẩn dụ chung chung, đúng thứ skill này cấm)*.

**Biến thiên mỗi phiên:** giải thích cái gì · cho ai nghe · ra trang hay ra ảnh.

## Skill này chứa gì và KHÔNG chứa gì

Chứa **phương pháp giải thích** và **cách dựng trang**. Không chứa bảng màu, không chứa font, không chứa luật giọng văn.

Lý do y hệt `anh-quote` và `viet-content`: những thứ đó nằm trong `wiki/` và bạn sửa liên tục — bảng màu vừa đổi vai và tỷ lệ ngày 2026-08-16, grid paper vừa bị bỏ khỏi nhận diện. Chép vào đây là có hai bản, và bản trong skill sẽ âm thầm lạc hậu.

**Luôn mở file thật ra đọc, đừng viết từ trí nhớ** — kể cả khi thấy mình "đã biết rồi".

| Cần biết | Đọc file |
|---|---|
| Bảng màu (vai + tỷ lệ), font, cái gì đã bị bỏ khỏi nhận diện | `wiki/systems-and-stack.md` — mục *Brand & Poster Design Guidelines* |
| Chữ trên trang viết thế nào cho ra giọng bạn | `wiki/voice-profile.md` |
| **Người nghe là ai, họ đang mắc ở đâu** | `wiki/target-customer.md` — *Chân Dung "Sân Khấu 1 Người"* + *Nguyên Nhân Gốc* |
| Câu nào bạn hay dùng để mở | `viet-content/luat/hook.md` |
| Viết thế nào thì lộ ra là AI viết | `viet-content/luat/dau-hieu-ai-viet.md` |
| Chuyện thật của bạn để lấy làm phép so sánh | `wiki/experiences-library.md` |
| Xưng hô, khi nào hỏi khi nào tự làm | `wiki/ai-operating-preferences.md` |

Mọi đường dẫn tính từ gốc `SecondBrain/`.

## Chỗ để đồ

```
giai-thich/
  ra/<lượt>/   trang.html · noi-dung.json · anh.png (nếu có)
```

Một lượt một thư mục, đặt tên gợi nội dung (`tu-huyet-cam-xuc/`), không đặt `lan-3/`.

## Hai cửa vào

**Cửa 1 — một khái niệm rời.** bạn gõ `/giai-thich-de-hieu phễu bán hàng` hoặc hỏi miệng.

**Cửa 2 — một trang có sẵn trong bộ não.** bạn dán đường dẫn `wiki/teachings/tu-huyet-cam-xuc.md` và bảo làm thành trang giải thích.

⚡ **Cửa 2 mới là cửa đáng dùng nhất, và hay bị bỏ quên.** Bộ não đang có 17 trang trong `wiki/teachings/`, 5 hình mẫu trong `wiki/models/`, 11 trang trong `wiki/learnings/` — toàn thứ bạn đã nghĩ kỹ, đã dạy thật, đã có ví dụ thật. Biến một trang trong đó thành hình thì **có nội dung gốc để bám**, khỏi phải bịa. Nếu bạn vào bằng Cửa 1 mà chủ đề trùng với một trang đang có, **nói ra và hỏi có muốn lấy trang đó làm gốc không** — đừng lặng lẽ viết lại từ đầu một thứ bộ não đã có.

---

## Bước 1 — Chốt NGƯỜI NGHE trước, chốt nội dung sau

Cùng một khái niệm, giải thích cho ba nhóm này ra ba trang khác hẳn nhau:

| Người nghe | Giải thích khác ở đâu |
|---|---|
| **Người lạ lướt Facebook** | phải tự đứng được, không giả định biết gì về bạn, mở bằng nỗi đau của họ |
| **Member đang học** | được phép dùng từ trong hệ thống, nối vào bài đã học |
| **Đội của bạn** | được dùng số thật, tên thật, chi tiết vận hành |

**Nếu bạn không nói rõ thì hỏi.** Một câu, hỏi luôn một lượt cùng Bước 3, đừng hỏi nhỏ giọt.

Không có thông tin gì thêm thì mặc định là **member đang học** — đó là chỗ skill này được dùng nhiều nhất.

## Bước 2 — Rút xuống ĐÚNG MỘT câu hỏi

Trước khi vẽ bất cứ thứ gì, viết ra một câu hỏi mà cả trang này trả lời. Trình cho bạn thấy câu đó.

- ✅ *"Vì sao khách gật đầu suốt buổi tư vấn rồi biến mất?"*
- ❌ *"Tổng quan về tâm lý khách hàng"*

⚠️ **Hai câu hỏi = hai trang.** Nhồi hai ý vào một trang là ra một trang không ai nhớ được gì. Thấy đang có hai thì tách và nói với bạn.

## Bước 3 — Tìm phép so sánh đời thường *(chỗ dễ hỏng nhất)*

Đây là toàn bộ khác biệt giữa một trang giải thích thật và một trang định nghĩa có màu.

**Luật:** khái niệm phải được neo vào **một thứ người nghe đã sờ tay vào rồi**.

Ba nguồn, xếp theo thứ tự ưu tiên:

1. ⭐ **Chuyện thật của bạn** — mở `wiki/experiences-library.md` tìm trước. Phép so sánh mạnh nhất là chuyện đã xảy ra với chính bạn, vì nó vừa giải thích vừa làm bằng chứng. Đây cũng là đúng thứ `wiki/voice-profile.md` PHẦN 4 đòi.
2. **Đời sống của người nghe** — với tệp của bạn (`wiki/target-customer.md`): quán ăn, xe máy hỏng, thợ thuyền, con cái, chợ búa, đội bóng, nhà cửa.
3. Cùng lắm mới tới ẩn dụ phổ thông.

⛔ **Cấm tuyệt đối mấy phép so sánh mặc định của AI:** pizza chia phần, robot, thư viện sách, nhà máy dây chuyền, "giống như khi bạn đặt Grab". Chúng nghe trơn tru vì chúng đã bị dùng cả triệu lần — và đó chính là lý do chúng không dạy được gì.

⛔ **Cấm bắt đầu bằng định nghĩa.** *"X là một phương pháp giúp..."* — đọc câu đó xong người nghe vẫn không biết gì. Bắt đầu bằng **tình huống họ đã gặp**, rồi mới gọi tên nó.

## Bước 4 — Dựng sơ đồ có CƠ CHẾ, không phải hình trang trí

**Bài kiểm một câu:** *mũi tên trong sơ đồ này đang nói "cái gì gây ra cái gì", hay chỉ nói "cái gì đứng cạnh cái gì"?*

Nếu là vế sau thì đó không phải sơ đồ, đó là bảng chia ô có màu.

| Hình dùng được | Hình giả vờ |
|---|---|
| Chuỗi nhân–quả có mũi tên, mỗi mũi tên gắn **động từ** (`làm cho`, `chặn`, `nuôi`) | Bốn cái hộp xếp ngang, không mũi tên |
| Trước ⟷ sau, sai ⟷ đúng đặt cạnh nhau để tự lộ khác biệt | Mấy emoji rải quanh chữ |
| Cái vòng lặp — chỉ ra chỗ nó tự quay lại | Icon minh hoạ chung chung cạnh mỗi gạch đầu dòng |
| Thanh/khối so tỷ lệ khi con số là điểm chốt | Ảnh nền đẹp không liên quan tới nội dung |

⛔ **Emoji không phải hình minh hoạ.** Rải emoji quanh chữ là cách rẻ nhất để một trang trông như đã được thiết kế mà thật ra chưa. Được dùng emoji làm **nhãn** (một cái, cạnh tiêu đề mục); không được dùng thay cho việc vẽ ra cơ chế.

Vẽ bằng **SVG viết tay trong trang** — không thư viện ngoài (artifact chặn hết). Cần biết vẽ sao cho đọc được ở cả nền sáng lẫn nền tối thì nạp skill `artifact-diagramming`.

## Bước 5 — Viết chữ

Đọc `wiki/voice-profile.md` trước khi đặt bút. Chữ trên trang giải thích cũng là content — luật giọng áp y như bài viết.

Thêm ràng buộc vật lý riêng của trang có hình:

- **Trần chữ: mỗi màn ≤ 30 chữ cho câu chính. Cả trang ≤ 250 chữ.** Vượt trần nghĩa là đang viết bài chứ không đang giải thích bằng hình — lúc đó tách bớt sang hình, hoặc chuyển sang `/viet-content`.
- **Một màn một ý.** Hai ý thì hai màn.
- **Câu ngắn, chủ ngữ là người nghe.** *"Khách gật đầu vì..."* chứ không phải *"Hiện tượng gật đầu được lý giải bởi..."* — cái sau đúng y dấu hiệu W1 trong `viet-content/luat/dau-hieu-ai-viet.md`.
- **Chốt bằng một câu dùng được ngay**, không phải một câu tổng kết. *"Lần tới, hỏi câu này trước khi báo giá: ..."* chứ không phải *"Tóm lại, thấu hiểu khách hàng là chìa khoá."*
- ⛔ **Không bịa số.** Luật cứng #5 trong `wiki/ai-operating-preferences.md`. Thiếu số thật thì để `[placeholder ngoặc vuông]` rồi hỏi bạn — trang giải thích còn nguy hơn bài viết vì nó bị chụp lại và lan đi.
- ⛔ **Không nêu doanh thu · SĐT · quy mô tài sản · chiến lược ngầm của member.** Tên gọi thường ngày thì được (luật đã nới 2026-08-19) — đọc kỹ bảng phân định trong `ai-operating-preferences.md` §2 trước khi nhắc tới ai.

## Bước 6 — Dựng trang

**Nạp skill `artifact-design` trước khi viết dòng HTML đầu tiên.** Bắt buộc, không bỏ qua vì thấy "trang này đơn giản".

Bố cục mặc định: **một màn dọc, cuộn xuống**, mỗi ý một khối chiếm gần hết bề ngang. Không làm tab, không làm accordion — giấu nội dung đi là đi ngược mục đích của skill này.

### Màu

Đọc bảng màu trong `wiki/systems-and-stack.md`. Khai thành token CSS theo đúng **vai**, đừng rắc hex khắp file:

```css
:root{
  --nen:    /* màu Chính — chiếm ~60% diện tích */;
  --chu:    /* màu Phụ */;
  --nhan:   /* màu Nhấn — ~10%, dùng cho ĐÚNG một thứ mỗi màn */;
  --chuc-nang: /* vàng — nhãn · highlight · pill. KHÔNG bao giờ làm nền */;
}
```

⚠️ **Tỷ lệ 60-30-10 là quyết định có lý do, không phải gợi ý thẩm mỹ.** `systems-and-stack.md` ghi rõ: 90% diện tích màu nhạt để chở *bình tâm · bình thản*, 10% đỏ chở năng lượng. Tô đỏ cả nền là đi ngược từ khoá thương hiệu. Thấy trang mình vừa dựng nhiều đỏ quá thì đó là lỗi, không phải phong cách.

Trang phải chạy đúng ở **cả nền sáng lẫn nền tối** — người xem đang để chế độ nào là artifact hiện theo chế độ đó. Định nghĩa đủ bộ token ở `:root` trần, rồi định nghĩa lại trong `@media (prefers-color-scheme: dark)` bọc `:root:not([data-theme="light"])`, và một lần nữa trong `:root[data-theme="dark"]`. `body` phải có nền tô bằng token, đừng để trong suốt.

### Font

Artifact chặn mọi host ngoài, **trừ Google Fonts**. Nên chọn font từ đó, hoặc nhúng base64 font của chính bạn.

| Cửa | Làm sao | Khi nào |
|---|---|---|
| ⭐ **Be Vietnam Pro** | link thẳng từ Google Fonts | mặc định — dựng nhanh, dấu tiếng Việt vẽ đúng, miễn phí OFL |
| **Font nhận diện của bạn** | base64 file `.woff2` vào `@font-face` dạng `data:` | khi thương hiệu của bạn đã có font riêng |

```bash
# in ra chuỗi data: để dán vào @font-face
printf 'url(data:font/woff2;base64,%s)' "$(base64 -i <đường-dẫn-font>.woff2 | tr -d '\n')"
```

Một weight đã subset thường ~12KB, base64 lên ~16KB — nhúng `regular` + `medium` hết ~33KB, không đáng kể so với trần 16MB của Artifact.

⚠️ **Kiểm weight tối đa của font trước khi dùng.** Đặt `font-weight: 600` hay `700` cho một font chỉ có tới 500 thì trình duyệt tự bôi đậm giả — chữ dày ra và **dính dấu tiếng Việt**. Muốn tiêu đề nặng hơn thì tăng cỡ chữ, đừng tăng độ đậm.

⚠️ **Nhiều font Latin nổi tiếng vẽ sai dấu tiếng Việt** — nhất là dấu nặng và dấu hỏi ở chữ HOA (Poppins bản gốc của Google là một ví dụ đã xác nhận tận mắt). Trước khi chốt font, gõ thử `ữ ự ệ ặ ộ ỗ ẫ ở Đ` ở cả chữ thường lẫn chữ HOA rồi **nhìn bằng mắt**.

Lưu bản HTML vào `giai-thich/ra/<lượt>/trang.html` **trước khi** publish, rồi mới gọi Artifact với đường dẫn đó.

## Bước 7 — TỰ KIỂM trước khi đưa bạn

⚠️ **Artifact là trang riêng tư, trình duyệt trong app KHÔNG mở được link đó.** Muốn nhìn tận mắt thì xem bản local:

```
preview_start { name: "xem-trang-giai-thich" }
→ http://localhost:8765/ra/<lượt>/trang.html?v=2
```

Cấu hình đã có sẵn trong `.claude/launch.json`, chạy `xem.py` nằm cùng thư mục skill này. **Đừng thay bằng `python3 -m http.server`** — lý do ghi ở *Bẫy đã gặp thật* §2. Đổi file rồi thì phải đổi luôn `?v=` trên URL, không thì trình duyệt trả bản cache cũ và mình ngồi sửa một thứ đã sửa rồi.

Nhìn ở **cả hai nền**: `resize_window { colorScheme: "light" }` rồi `"dark"`. Bỏ một nền là bỏ đúng chỗ bẫy §1 nấp.

Rồi chạy đủ bốn bài kiểm:

1. 🖼 **Bài kiểm che chữ.** Che hết phần chữ, chỉ nhìn hình — còn hiểu được đại ý không? Không hiểu nghĩa là hình đang trang trí chứ không đang giải thích. Sửa hình, đừng thêm chữ.
2. 📖 **Bài kiểm người lạ.** Đọc lại như người chưa biết gì: có chỗ nào giả định sẵn kiến thức không? Từ nào chưa được giải thích mà đã dùng?
3. 🤖 **Bài kiểm AI.** Soi theo `viet-content/luat/dau-hieu-ai-viet.md` — song song phủ định, mệnh đề rỗng cuối câu, né động từ "là", câu nào cũng dài đều tăm tắp.
4. 🎨 **Bài kiểm màu.** Đếm nhanh: nền có đang là màu Chính không, đỏ có đang chỉ chiếm điểm nhấn không, vàng có bị dùng làm nền không.

Theo luật bằng chứng trong `ai-operating-preferences.md`: **cấm nói "xong" khi chưa trình bằng chứng.** Với skill này, bằng chứng là link artifact + nói rõ đã chạy bốn bài kiểm trên và thấy gì.

## Bước 8 — Muốn ra ảnh đăng Facebook thì nối sang `anh-quote`

**Không dựng bộ máy render mới.** `anh-quote` đã có sẵn, đã nhúng font, đã xử lý xong cả tá bẫy.

Sơ đồ 3–5 bước thì dùng thẳng kiểu `so-do-vang-chanh.html`, JSON dạng:

```json
{
  "nhan": "Cơ chế",
  "tieuDe": "Vì sao khách gật đầu rồi biến mất",
  "phuDe": "Dòng một.\nDòng hai.",
  "cacBuoc": [
    { "ten": "gật đầu", "chuThich": "Gật cho xong buổi, không phải vì đã tin", "phia": "tren" },
    { "ten": "về nhà",  "chuThich": "Không còn ai giữ nhiệt, nỗi sợ quay lại", "phia": "duoi" }
  ]
}
```

```bash
node .claude/skills/anh-quote/dung.mjs \
  --kieu anh-quote/kieu/so-do-vang-chanh.html \
  --noi-dung giai-thich/ra/<lượt>/noi-dung.json \
  --ra giai-thich/ra/<lượt>/anh.png
```

Rồi làm đủ **Bước 6 của `anh-quote`**: mở file PNG ra nhìn tận mắt. Ở đó đã ghi một ca render báo thành công, ảnh đủ dung lượng, mà mảng vàng và lưới giấy **không hề xuất hiện**.

Quá 5 bước thì tách hai tấm. Cần kiểu ảnh khác thì đọc `anh-quote/SKILL.md` — đừng tự chế kiểu mới ở đây.

## Bước 9 — Ghi log, KHÔNG tự ghi `wiki/`

1. **Append `log.md`** một dòng — không rewrite (luật sắt #4).
2. ⛔ **Không tự sửa file nào trong `wiki/`.** Đoàn chốt 2026-07-30: chỉ còn một đường ghi vào `wiki/` là `/nap-kho`. Trong lúc làm mà rút ra được một phép so sánh hay, một cách diễn đạt ăn tiền → **đề xuất bạn chạy `/nap-kho`**, đừng tự tay ghi.
3. Trang nào bạn duyệt là dùng tốt thì giữ nguyên thư mục `giai-thich/ra/<lượt>/` làm mẫu cho lượt sau.

---

## Bẫy đã gặp thật

> Rút từ **lượt chạy đầu tiên**, 2026-08-26, trang `tu-huyet-cam-xuc`. Bốn cái dưới đây đều hỏng thật trong lượt đó, không phải đoán.

**1. ⚠️ Trong SVG, `class` THẮNG thuộc tính `fill=` — và nền sáng không lộ ra.**
Viết `<text class="svg-chu" fill="var(--chuc-nang-chu)">` thì `fill=` bị `.svg-chu` đè, chữ lấy màu `--chu`. Ở nền sáng `--chu` là gần đen nên nằm trên ô vàng vẫn đọc được, **trông y như đúng**. Sang nền tối `--chu` là màu kem, chữ trên ô vàng gần như tàng hình. Muốn đổi màu một chữ đã có class thì phải **khai một class khác, đặt SAU trong khối `<style>`** (`.svg-tren-vang{fill:var(--chuc-nang-chu)}`), hoặc dùng `style=` inline. Thuộc tính `fill=` chỉ ăn khi thẻ đó **không có class nào**.
📌 Chỗ đáng nhớ: **lỗi này chỉ hiện ở một nền.** Kiểm mỗi nền sáng là không bao giờ thấy.

**2. `python3 -m http.server` làm vỡ hết tiếng Việt.**
Ra `VÃ¬ sao nÃ³i Ä'Ãºng`. Nguyên nhân: nó trả `text/html` **không kèm charset**, mà `trang.html` cố tình không có `<head>`/`<meta charset>` (Artifact tự bọc khi publish). Trình duyệt không có gì để bám nên đoán Latin-1. **Trang không sai, chỗ xem sai** — suýt ngồi sửa nhầm trang. Đã viết `xem.py` cạnh skill này để ép `charset=utf-8`; `launch.json` đã trỏ sang nó.

**3. Trình duyệt giữ cache, sửa xong nhìn vẫn thấy bản cũ.**
Sửa header server rồi mà màn hình vẫn vỡ chữ, tưởng chưa ăn. Thật ra là cache. **Luôn đổi `?v=` mỗi lần nạp lại**, và khi nghi thì `curl -sI` xem header thật thay vì tin mắt.

**4. Trần "250 chữ cả trang" ở Bước 5 chưa nói rõ đếm cái gì.**
Lượt đầu đo ra 320 chữ và tưởng vượt; tách ra mới thấy **văn xuôi chỉ 230**, phần dôi là 69 chữ nhãn trong sơ đồ + 21 chữ dòng nguồn.
✅ **Chốt cách đếm:** trần 250 tính **văn xuôi thôi** (`<h1>`/`<h2>`/`<p>`), **không tính** nhãn trong SVG và dòng nguồn ở chân trang. Trần 30 chữ mỗi màn tính **câu chính**, phần bổ trợ để ở `<p class="phu">` thì tính riêng. Không có luật này thì lượt sau lại cắt nhầm vào chữ đang cần.

---

## Chỗ nghi, CHƯA gặp

**5. `so-do-vang-chanh.html` đang dùng vàng `#dcfa7a`, không phải vàng nhận diện `#fff777`.** Đếm trực tiếp trong file. Ảnh render ra sẽ lệch màu so với trang artifact dựng đúng bảng màu. Chưa rõ cố ý hay sót — **hỏi bạn trước khi tự sửa**, vì sửa file kiểu là đổi mọi ảnh đã dùng kiểu đó. *(Lượt 1 chưa render ảnh nên chưa đụng tới.)*

**6. `giay-grid-brand.html` vẫn dùng nền giấy kẻ ô — thứ bạn đã bỏ khỏi nhận diện 2026-08-16.** `systems-and-stack.md` tự ghi đây là việc còn phải làm. Đừng chọn kiểu này cho trang giải thích mới.

**7. Bộ dấu tiếng Việt của bản woff2 đã subset: lượt 1 nhìn tận mắt thấy ĐỦ** (`ữ ự ệ ặ ộ ỗ ẫ ở Đ` đều hiện đúng trên FZ Poppins nhúng base64). Vẫn chưa kiểm được bằng máy (máy không có `fontTools`), nên vẫn phải nhìn, đừng bỏ qua.


## Links
`wiki/systems-and-stack.md` · `wiki/voice-profile.md` · `wiki/target-customer.md` · `viet-content/luat/dau-hieu-ai-viet.md` · `wiki/experiences-library.md` · `viet-content/luat/hook.md` · `wiki/ai-operating-preferences.md` · skill `anh-quote` (render ảnh) · skill `viet-content` (khi chữ vượt trần) · skill `nap-kho` (đường duy nhất ghi vào `wiki/`) · skill `artifact-design` + `artifact-diagramming` (nạp trước khi dựng trang)

---

## Skill này của ai

Viết bởi **Tô Hải Đoàn** — người làm nội dung và xây thương hiệu cá nhân tại Việt Nam. Đây không phải skill dựng cho vui: nó là quy trình tôi dùng cho công việc của chính mình mỗi ngày, đóng gói lại để bạn chạy được trên dữ liệu của bạn.

Giấy phép MIT, bạn dùng và sửa thoải mái.

**Kẹt ở đâu, hoặc muốn được hướng dẫn dùng cho đúng việc của bạn** thì nhắn tôi: [facebook.com/tohaidoan](https://www.facebook.com/tohaidoan/)
