# Writing Craft Core — lõi nghề viết dùng chung

> 📎 **Đọc file này thế nào.** Đây là luật nghề của Tô Hải Đoàn, đóng gói nguyên văn để bạn dùng.
> Các liên kết dạng `[[tên-trang]]` trỏ tới những trang trong bộ não **của Đoàn**. Trang nào bộ não của bạn chưa có thì **bỏ qua liên kết đó** — đừng đoán nội dung của nó, và đừng bịa ra cho đủ. Muốn có trang tương đương thì tự dựng bằng `/nap-kho`.
> Các ví dụ, con số và tên người trong file là **của Đoàn**, dùng để minh hoạ luật. 🚫 Tuyệt đối không bê chúng vào bài của bạn — đó là vi phạm chính luật cấm bịa ở đây.


> **Đây KHÔNG phải quy tắc riêng của Đoàn.** Đây là lớp luật viết phổ quát áp cho **mọi user** của [[projects/creator-os]], bất kể ngách. Bản cá nhân của Đoàn nằm ở `luat/vi-du-luat-rieng.md` (phát kèm làm **ví dụ**, không phải luật bạn phải theo) và `wiki/voice-profile.md`.
> Chốt: 2026-07-29, qua một phiên phản biện đối chiếu với [[personal-mission]] · [[values-and-principles]] · [[contrarian-beliefs]] · [[target-customer]] · [[goals]].
> Trạng thái: **đang thử nghiệm** — Đoàn duyệt để thử, chưa qua kiểm chứng bằng bài thật.


## Vì sao cần lớp này

Trước 2026-07-29, tool Creator OS có 13 ô nhập ở `/write` thì **11 ô lo nội dung** (viết cái gì, chứng minh bằng chuyện nào, cho ai) và chỉ **2 ô lo cách viết** — cả hai đều mặc định rỗng. Riêng Story bank được cấp ngân sách 120.000 ký tự trong prompt, còn kỹ thuật viết được cấp 0 ký tự.

Hệ quả: chất lượng câu chữ phó mặc cho model nền. Mà văn mặc định của model đúng là thứ lớp luật này đang cấm. Triệu chứng dễ thấy nhất trong tool: **hook sắc, thân bài nhạt** — vì lớp hook đã có 8 kiểu với hướng dẫn nghề thật (`lib/hooks.ts`), còn thân bài thì không có gì.

---

## Kiến trúc 4 tầng và thứ tự thắng

```
Lõi nghề  >  Khung viết  >  Giọng cá nhân  >  Đặc trưng hình mẫu
```

| Tầng | Là gì | Ai quyết | Có mặt khi nào | Dùng ở |
|---|---|---|---|---|
| **1. Lõi nghề** | 10 luật bắt buộc | Tool, duyệt sẵn | Luôn luôn | `/write` + `/review` |
| **2. Khung viết** | 7 khung, mỗi khung có mạch + hướng dẫn | User chọn, hoặc AI chọn trong 7 | Luôn có | `/write` + `/review` |
| **3. Giọng cá nhân** | `VoiceProfile` — 7 dòng đã có sẵn | Từng user | Khi đã dựng hồ sơ | `/write` + `/review` |
| **4. Đặc trưng hình mẫu** | `Analysis.formats[].howTo` | Bản phân tích | Chỉ khi chọn hình mẫu | `/write` |

**Vì sao thứ tự đó:**
- Khung thắng giọng vì khung là lựa chọn cho riêng bài này, còn giọng là hồ sơ đứng sẵn.
- Giọng thắng đặc trưng hình mẫu vì mục tiêu là viết giọng mình, không phải nhái người ta.

Trước khi có file này, **không có luật phân xử nào** — prompt viết bài có cả `Format hay dùng: [...]` (từ hình mẫu) lẫn `Khung viết (framework): ...` (từ user), hai dòng nói về cùng một thứ mà không ai thắng ai.

---

## ⚡ Trước cả 4 tầng — quy trình xác định NÓI GÌ, nạp 2026-08-22

> Bốn tầng trên quyết định **VIẾT THẾ NÀO** (cấu trúc/giọng/hình mẫu). Không tầng nào trả lời câu hỏi đến trước: viết bài này **để làm gì**, và **lấy gì để chứng minh**. Đoàn mô tả quy trình thật khi được hỏi cơ chế Nhân Hiệu Thực Chứng ([[offer-ladder]] V2) chạy qua mấy bước cụ thể trong Creator OS — câu trả lời hoá ra là lớp nằm TRƯỚC cả 4 tầng, không phải một chi tiết của Tầng 2.

**7 bước, đúng thứ tự — mỗi bước là input của bước sau:**

1. **Mục tiêu bài viết** — bài này để làm gì
2. **Hành vi mục tiêu** — muốn người đọc làm gì sau khi đọc xong (kêu gọi hành động)
3. **Thông điệp** — từ hành vi mục tiêu suy ra thông điệp cần truyền tải
4. **Luận điểm / bằng chứng** — câu chuyện (của mình hoặc sưu tầm) hoặc số liệu/nghiên cứu/phân tích để chứng minh thông điệp
5. **Cấu trúc** — chọn từ hình mẫu, học cấu trúc của người đang làm tốt → nối thẳng vào **Tầng 2** ở trên
6. **Giọng điệu** — giọng thật của chính mình, phân tích ra chứ không "diễn" → nối thẳng vào **Tầng 3**
7. **Viết**

⚡ **Nguyên văn quan trọng nhất — mở rộng khái niệm "chất liệu của mình" ở bước 4:** *"kể cả là những câu chuyện mình đi đọc của người ta... thì vẫn là câu chuyện của mình... hay những phân tích, nghiên cứu mà mình đọc được thì cũng là trải nghiệm của mình... vẫn là câu chuyện cá nhân hết, không cần lo."* Không giới hạn ở chuyện đời thật xảy ra với chính mình — **đọc/tìm thấy một điều gì đó cũng là một trải nghiệm thật**, đủ tư cách làm luận điểm. Đây là câu trả lời trực tiếp cho nỗi sợ *"tôi không có gì để kể"* ([[objections-library]] #16).

📌 **Bước 5 và 6 là chỗ nối vào hệ đã có** — không đẻ khung song song. Bước 5 = việc chọn 1 trong **Tầng 2 — 7 khung viết**. Bước 6 = **Tầng 3 — Giọng cá nhân** (`VoiceProfile`). Bốn bước đầu (1–4) là lớp hoàn toàn mới, quyết định NỘI DUNG trước khi bốn tầng cũ quyết định HÌNH THỨC.

---

## Tầng 1 — Lõi nghề: 10 luật

Nguyên văn dạng đi vào system prompt:

```
NGƯỜI ĐỌC ĐANG BẬN NGHĨ CHUYỆN KHÁC.

Trước khi đọc câu đầu tiên của bài, tâm trí họ đã kín chỗ bởi một mối
bận tâm không liên quan gì tới bài. Đừng viết cho một người đang chờ
đọc bài của bạn — không có người đó. Bài phải tự giành lấy chỗ, và
giành bằng cách nối được điều mình nói với thứ đang có sẵn trong họ.

Mười luật dưới đây áp trên giả định đó.

NHÓM A — BÀI PHẢI ĐỌNG LẠI GÌ

A1. PHẢI CÓ MỘT THÔNG ĐIỆP, VÀ NGƯỜI ĐỌC PHẢI NHẬN RA ĐƯỢC NÓ.
    Đọc xong, người đọc phải THẤY được, NHẬN RA được, hoặc CẢM NHẬN
    được một điều gì đó.

    Nói thẳng thông điệp ra hay để nó ẩn trong câu chuyện — CẢ HAI
    ĐỀU ĐÚNG. Chọn theo bài, không có kiểu nào là mặc định. Khi cần
    nói rõ thì nói rõ, kể cả giảng giải vì sao điều đó quan trọng.

    Cái bị cấm chỉ có một: bài kể xong mà không đọng lại gì.

A2. CHẠM NGUYÊN NHÂN, VÀ TRẢ LỜI ĐIỀU NGƯỜI ĐỌC ĐANG CÃI.
    Nếu bài có chỉ cách làm thì phải cho thấy nguyên lý đằng sau —
    cho thấy bằng chuyện và bằng hệ quả thật, không chỉ bằng một đoạn
    phân tích.
    Và bài phải NÓI RA được điều người đọc đang phản bác trong đầu,
    rồi trả lời nó. Nêu một quan điểm xong bỏ mặc người đọc với sự
    nghi ngờ của họ là bài mới xong một nửa.
    Cách làm: liệt kê HẾT lý do người đọc có thể nói "không" với
    điều bạn đang nói, rồi dọn từng cái theo đúng thứ tự nó nảy ra
    trong đầu họ. Đọc xong không còn chỗ nào để cãi nữa mới là xong.

NHÓM B — BÀI PHẢI THẬT

B1. CỤ THỂ HOÁ. Thay mọi thứ mơ hồ bằng thứ nhìn thấy được: không
    "nhiều năm" mà "12 năm"; không "một người bạn" mà tên thật; không
    "kiếm được nhiều" mà con số. Con số không cần lớn, cần thật.
    CẤM TUYỆT ĐỐI BỊA SỐ, bịa tên, bịa kết quả để cho tròn luật này.
    Không có số thật thì kể chi tiết thật, hoặc để trống.

B2. TRẢ NỢ CHO THỨ ĐÃ HỨA. Câu mở hứa gì, thông điệp khai gì, thì thân
    bài phải chứng minh đúng cái đó. Cấm mở bằng một chuyện rồi giữa
    bài rẽ sang chuyện khác.

B3. MỘT BÀI MỘT THÔNG ĐIỆP. Đi sâu một ý. Thà bỏ ba ý hay còn hơn nhồi
    bốn ý nửa vời.

NHÓM C — CÂU CHỮ KHÔNG ĐƯỢC SẶC MÙI AI

C1. VIẾT NHƯ NGƯỜI THẬT ĐANG NÓI. Văn nói có nhịp, không phải văn báo
    cáo. Không để cả bài cùng một độ dài câu, và cũng không xếp ba câu
    ngắn cùng kiểu liên tiếp. Danh sách tối đa 3-4 điểm.
    CÂU CHỦ ĐỘNG, không bị động. Soi các từ "bị", "được", "do", "là"
    để tìm câu bị động rồi lật lại.
    Gặp câu nhiều dấu phẩy, thử tách thành mấy câu ngắn.

C2. ẨN DỤ PHẢI SỜ ĐƯỢC. Chỉ dùng hình ảnh người đọc hình dung ngay
    ("sợi dây thun đã nhão"). Cấm ẩn dụ trừu tượng: "trên một mặt
    phẳng", "lệch nhịp", "lệch pha", "cùng đứng", "một khung sẵn".

C3. CẤM CÁC KHUÔN ĐÃ MÒN: "X nghe có vẻ tốt. Nhưng thực ra...", mở câu
    bằng "Bạn không cần...", lặp "không phải... mà là" quá một lần,
    chuỗi phủ định kép liên tiếp.
    CẤM CÂU HỎI ĐÓNG làm câu mở — câu hỏi mà người đọc trả lời được
    bằng "có" hoặc "không" thì họ gạt đi ngay và không đọc tiếp.
    Câu hỏi mở bài phải là câu chưa trả lời ngay được.
    NGOẠI LỆ có điều kiện — khuôn "Hầu hết mọi người nghĩ X, nhưng với
    tôi Y" ĐƯỢC PHÉP khi Y là một lập trường cụ thể của người viết và
    bài có chứng minh Y. Cấm khi nó chỉ là câu mở chung chung rồi bài
    đi chỗ khác.

C4. ĐƯỢC PHÉP GIẬT TÍT. Được dùng ngôn từ đánh trúng tâm lý người đọc.
    Điều kiện duy nhất: thân bài phải chứng minh được (xem B2).
    NHƯNG tránh giật bằng khoe khoang, phóng đại, con số gây sốc —
    không phải vì sai, mà vì kiểu đó đã quá phổ biến nên hết tác dụng,
    người đọc lướt qua.
    Giật bằng chất liệu đời thường, chân thực, giản dị. Cùng một sức
    kéo, nhưng đến từ chỗ người đọc tin được.

C5. KHÔNG AI KHÁC VIẾT ĐƯỢC BÀI NÀY. Thử đổi tên người viết sang một
    người cùng ngành. Bài vẫn đúng, vẫn dùng được? Vậy thì bài chưa
    có gì là của mình — mới chỉ đúng, chưa thật.
    Thứ không thay được: chuyện đã sống, số đã đo, người đã gặp,
    giá đã trả.
```

### Nguồn từng luật

Không luật nào là suy đoán. Bảng này để phiên sau kiểm lại được:

| Luật | Nguồn |
|---|---|
| Lời mở "người đọc đang bận nghĩ chuyện khác" | [[teachings/tu-huyet-cam-xuc]] (Roy Garn) — thứ **duy nhất** trong cả cuốn qua được bộ lọc hai tầng. Cố ý để dạng lời mở chứ không thành một luật riêng: nó không bảo phải làm gì, nó đổi giả định mà cả mười luật kia đứng lên |
| A1 | Đoàn trả lời trực tiếp 2026-07-29 · khớp `wiki/voice-profile.md` PHẦN 8 *"Bài có đang khuyên hay đang kể?"* (dạng câu hỏi, không phải lệnh cấm) |
| A2 | `luat/vi-du-luat-rieng.md` nguyên tắc gốc 3 · [[values-and-principles]] mục *"Tư Duy Nguyên Nhân Gốc Rễ"*. **Vế "trả lời điều người đọc đang cãi" bổ sung 2026-07-29** từ [[teachings/thoi-mien-bang-ngon-tu]] — bản rút đầu tiên chỉ lấy nửa sau của nguyên tắc gốc 3 (*bám vào lý do đằng sau*) và bỏ mất nửa trước (*đa chiều, có phản biện*) |
| B1 | Masterfile PHẦN 4 *"Số liệu thật"* + *"Nhân vật phụ gọi tên"* · vế cấm bịa từ [[ai-operating-preferences]] Hard Don't số 5 |
| B2 | [[values-and-principles]] nguyên tắc bất biến 1 *"Làm điều mình nói"*, hạ xuống cấp độ bài viết · Đoàn xác nhận 2026-07-29 là điều kiện để cho phép giật tít |
| B3 | Guidelines nguyên tắc gốc 2 · khớp *"Định (Tĩnh tâm): tập trung sâu vào ít"* |
| C1 | Guidelines nguyên tắc gốc 1 · Masterfile PHẦN 4 *"Nhịp câu"* — viết theo hướng cấm thay vì hướng ép, để chính nó không thành khuôn mòn · **vế câu chủ động và vế dấu phẩy** bổ sung 2026-07-29 từ [[teachings/thoi-mien-bang-ngon-tu]] ch.51, cả hai đều **soi được bằng máy** nên dùng được cho `/review` |
| C2 | Masterfile PHẦN 4 *"Ẩn dụ vật lý"* · danh sách cấm từ PHẦN 6 · khớp SOP Cậu Hai *"không dùng ngôn ngữ tâm linh sáo rỗng"* ở [[target-customer]] |
| C3 | Guidelines mục *"Khuôn cần tránh"* · **ngoại lệ** do Đoàn phân xử 2026-07-29, vì [[contrarian-beliefs]] ghi khuôn này là *"pattern sắc bén nhất"* — hai file vốn đang cãi nhau · **vế cấm câu hỏi đóng** bổ sung từ [[teachings/thoi-mien-bang-ngon-tu]] ch.45: Guidelines vốn cấm *"câu hỏi chung chung"* nhưng chữ đó khó kiểm, còn "trả lời được bằng có/không" thì kiểm được ngay |
| C4 | Đoàn trả lời trực tiếp 2026-07-29 · khớp [[contrarian-beliefs]] belief 6 đã làm rõ (*"vẫn cần viral, vẫn cần tương tác"*) và [[goals]] nút thắt *"thiếu Thu hút"* |
| C5 | [[teachings/thoi-mien-bang-ngon-tu]] — Vitale nêu ở hai cấp: tiêu đề (*"tiêu đề này có áp vào quảng cáo của đối thủ được không?"*) và toàn bài (*"đối thủ có sao chép bản thảo này dùng cho sản phẩm của họ được không?"*). Đoàn duyệt 2026-07-29. Là luật khớp chặt nhất với định vị **nhân hiệu thực chứng**: thứ đối thủ không chép được chính là bằng chứng đã sống |

### ⚡ B2 và B3 đang đẩy bài về phía văn AI (phát hiện 2026-08-05)

Cả hai luật đều bảo: cắt mọi thứ không phục vụ thông điệp. Làm đúng tuyệt đối thì ra một bài **không còn chi tiết thừa nào** — mà chi tiết thừa lại chính là thứ chứng minh chuyện có thật (không ai bịa ra chi tiết chẳng để làm gì).

Không phải lỗi của B2/B3. Nhưng chúng cần một đối trọng, và hiện không có. Nháp **luật C6 "Để lại dấu tay"** ở `luat/dau-hieu-ai-viet.md` — **chưa duyệt**.

### Ba thứ CỐ Ý không đưa vào lõi nghề

Vì thuộc lớp giọng cá nhân, ép cho mọi user là sai:

- **Cấm "tụi mình", "ảnh"** — gu vùng miền của Đoàn. User ngách khác dùng bình thường.
- **Xưng "tôi", gọi "bạn"** — ngôi xưng là giọng, không phải nghề.
- **6 trục tư tưởng** (giá trị thật > tiền nhanh · trải nghiệm > lý thuyết · cho đi → nhận lại · môi trường & người dẫn đường > nỗ lực cá nhân · tự do bên trong > tự do vật chất · phát triển liên tục > thành tựu đứng yên) — niềm tin của Đoàn, không phải kỹ thuật viết. Bản đầy đủ ở `wiki/voice-profile.md` PHẦN 3.

### Ba chỗ suýt sai, ghi lại để không lặp

1. **A1 từng bị viết quá chặt.** Bản đầu ép "kể, không khuyên, cấm giảng giải" — bê từ skill `viet-content` Bước 4. Đoàn bác: *"đôi khi vẫn có, chứ không phải lúc nào cũng không... Mình sẽ có cả hai kiểu."* Bộ não bản gốc (masterfile PHẦN 8) vốn ghi dạng **câu hỏi tự soi**, skill mới là chỗ hoá nó thành luật cấm. Skill đang chạy chặt hơn ý Đoàn → cần sửa riêng.
2. **Bộ luật từng nghiêng về "nhũn".** Bản đầu có ba luật kéo về tiết chế, không luật nào cấp phép cho sức kéo. Đây đúng cái nghiêng đã gây sự cố ghi ở [[contrarian-beliefs]] dòng 16 (một phiên đọc file đó rồi đề xuất **cắt sạch tính năng viral khỏi tool**, Đoàn phải chỉnh lại). C4 sinh ra để chặn đúng lỗi đó ở tầng câu chữ.
3. ⚡ **B1/C5 bị đọc rộng thành "cấm dùng chuyện của người khác"** (Đoàn chỉ ra 2026-08-10). Hai luật này cấm **nhận vơ**, không cấm **trích dẫn**:
   - **B1** cấm *bịa* số/tên/kết quả. Trích một con số **có nguồn, ghi rõ nguồn** không phải bịa.
   - **C5** hỏi *"đổi tên người viết sang người cùng ngành thì bài còn là của mình không"* — nó áp cho **lõi phân biệt** của bài (chuyện đã sống, số đã đo, người đã gặp, giá đã trả), **không** áp cho bằng chứng phụ trợ có dẫn nguồn.

   Trích dẫn thẩm quyền là **Loại 5** trong 7 loại bằng chứng ở [[content-modeling-playbook]] — bằng chứng **hợp lệ**, không phải khoản phải trừ. Ranh giới đã khai sẵn ở đó: ***kiểm chứng được hay không***, không phải *có phải chuyện của mình không*.

   Đã mắc thật: [[models/tran-manh-duc]] gọi đúng tên *"khung mượn có tên (Loại 5)"* rồi vẫn kết luận *"đây đúng chỗ Đoàn phải thay"*, và xếp việc mượn khung Hormozi/Munger/Harari vào mục **Va chạm giá trị**. Trong khi [[models/matt-gray]] cùng bộ luật lại ghi đúng: *"Loại 2 và Loại 5 — mạch **không cần câu chuyện của mình**, hợp lúc kho chuyện chưa dày."* Hai trang, hai kết luận trái nhau.

   **Cách nhớ:** mượn **có ghi nguồn** = bằng chứng · mượn **rồi kể như của mình** = vi phạm. Kho trích dẫn dùng lại được ở [[quoted-authority]].

---

## Tầng 2 — 7 khung viết

Dựng theo đúng cách `HOOK_ANGLES` đã làm ở `lib/hooks.ts`: mỗi khung một hướng dẫn nghề riêng, không phải nhãn suông. Lý lẽ giống hệt — cho AI tự do thì nhận về bảy biến thể của cùng một mạch; ép theo khung mới ra mạch thật sự khác.

| Khung | `key` | Mạch | Thông điệp | Hợp tuyến |
|---|---|---|---|---|
| **Chuyển hoá 5 bước** | `transformation` | Hook → tôi từng sai thế này → cho đến khi → kết quả và bài học → mời | Nói ra | Thương hiệu |
| **Bằng chứng dẫn đường** | `evidence_led` | Kết quả thật đã có → bóc từng bước đã làm → điều kiện để lặp lại được → mời | Nói ra | Bán hàng |
| **Lật ngược niềm tin** | `belief_flip` | Điều số đông đang tin → chỗ nó hỏng → cái thay thế → chuyện thật chứng minh | Nói ra | Thu hút |
| **Một sai lầm đắt giá** | `costly_mistake` | Thú nhận việc mình làm sai → cái giá đã trả → vì sao lúc đó tin là đúng → điều đã đổi | Nói ra | Thương hiệu |
| **Bóc một câu hỏi** | `one_question` | Câu hỏi thật khách hay hỏi → trả lời thẳng trong 2 câu → vì sao đa số trả lời sai → ví dụ | Nói ra | Nuôi tệp |
| **Trước / sau của người khác** | `client_before_after` | Tình trạng ban đầu của học viên → thứ đã thay đổi → mình đã làm gì trong đó → mời | Nói ra | Bán hàng |
| **Kể thẳng một chuyện** | `plain_story` | Một khoảnh khắc thật, kể từ đầu đến cuối, không rút bài học ra thành lời | **Ẩn** | Thương hiệu |

Cột `key` là chuỗi thật đi vào dòng `> Khung:` ở đầu `ket-qua.md`. Bảng này là **nguồn duy nhất** của cả tên lẫn khoá.

### Hướng dẫn nghề của từng khung

⚡ **Đây mới là phần có giá trị.** Cột "Mạch" ở trên chỉ là cái tên gọi của chuỗi chặng — ai đọc cũng đoán được. Phần dưới đây là chỗ nói ra **thứ nhìn bài không tự thấy**: chặng nào chịu sức nặng, chỗ nào hay bị bỏ, và mỗi khung hỏng theo kiểu gì.

Bổ sung 2026-08-04. Trước đó bảy đoạn này **chỉ tồn tại trong `creator-dna/src/lib/writing-craft.ts`**, không có trong bộ não — nên skill `viet-content` đọc file này thì chỉ nhận được nhãn và mạch, đúng thứ mà câu mở đầu mục này gọi là *"nhãn suông"*.

| Khung | Cách làm cho đúng |
|---|---|
| **Chuyển hoá 5 bước** | Sức nặng nằm ở đoạn *"tôi từng sai"*, không ở đoạn kết quả. Kể cái sai đủ cụ thể để người đọc thấy mình trong đó, rồi mới được quyền kể cái đúng. Đoạn *"cho đến khi"* phải là một thời điểm có thật, không phải một quá trình mơ hồ. |
| **Bằng chứng dẫn đường** | Mở bằng kết quả thì phải là kết quả **đo được, có thật**. Phần *"điều kiện để lặp lại"* là phần hay bị bỏ và là phần khiến bài khác một bài khoe: nói thẳng ai làm được, ai chưa nên làm, cần có sẵn gì. |
| **Lật ngược niềm tin** | Chỉ lật khi có chuyện thật đỡ phía sau — lật cho sốc là hỏng. Phải nêu điều số đông tin bằng **phiên bản mạnh nhất** của nó (không dựng bù nhìn dễ đánh), rồi mới chỉ chỗ nó hỏng. |
| **Một sai lầm đắt giá** | Đoạn *"vì sao lúc đó tin là đúng"* là đoạn quyết định. Thiếu nó, bài thành tự trách; có nó, người đọc nhận ra chính mình đang tin điều đó. Cái giá phải nói bằng con số hoặc bằng thứ mất đi cụ thể, không nói bằng tính từ. ⚡ **Thêm 2026-08-19:** Và phần *sai lầm + cái giá* phải **nặng hơn** phần *điều đã đổi* — đếm đoạn cũng được. Kể giải pháp dài hơn kể sai lầm là bài trượt thành quảng cáo cho giải pháp, dù không có một câu bán nào. Đây là luật đối xứng của khung *Trước/sau của người khác* (phần mình làm phải nhỏ hơn phần họ thay đổi). |
| **Bóc một câu hỏi** | Trả lời **thẳng trong 2 câu đầu**, không vòng vo lấy đà — người đọc có câu trả lời rồi mới chịu đọc phần giải thích. Câu hỏi phải là câu khách thật sự hỏi, bằng đúng chữ họ dùng. |
| **Trước / sau của người khác** | Phần *"mình đã làm gì"* phải **nhỏ hơn** phần *"họ đã thay đổi thế nào"* — kể ngược lại là bài khoe công. Tình trạng ban đầu càng cụ thể thì khoảng cách càng thật. |
| **Kể thẳng một chuyện** | ⚠️ **ĐÂY LÀ KHUNG DỄ HỎNG NHẤT.** Sức nặng nằm ở chi tiết và ở chỗ **DỪNG LẠI** — dừng đúng lúc thì người đọc tự rút ra, dừng sai thì thành bài kể lể. Chỉ dùng khi chuyện đủ mạnh để tự đứng một mình. Tuyệt đối không thêm câu *"qua đó tôi nhận ra..."* ở cuối; nếu thấy cần thêm câu đó thì chuyện chưa đủ mạnh, hãy đổi khung khác. |

Bảy đoạn trên chép **nguyên văn** từ `WRITING_FRAMES[].guide` trong bản code, cố ý — [[#⚠️ Ràng buộc hai chiều với code]] đòi hai bản khớp nhau, diễn đạt lại cho "hay hơn" là làm hai bản lệch ngay tại lúc chép. Cùng lý do đã áp cho khối 10 luật.

Khung 1 chính là công thức 5 bước của Đoàn ở `wiki/voice-profile.md` PHẦN 2, giờ là một lựa chọn có tên thay vì nằm mờ trong placeholder.

Cột "Thông điệp" tồn tại vì đây chính là chỗ quyết định nói ra hay để ẩn — và đó là **quyết định theo từng bài**, nên nó thuộc tầng khung chứ không thuộc tầng luật. Luật áp cho mọi bài thì không được chọn hộ.

**"Để AI tự chọn" vẫn giữ**, nhưng bị ép chọn đúng 1 trong 7 và phải nói ra chọn khung nào.

Tên khung là bản v1, đổi được sau khi dùng thật.

### ⚡ Luật kể chuyện — CHI TIẾT PHẢI CHẠM ĐƯỢC GIÁC QUAN *(nạp 2026-08-22)*

> Đoàn nêu trực tiếp: *"nếu đã kể câu chuyện, thì tôi muốn bổ sung thêm một quy tắc kể chuyện ở đây là kể chi tiết, sử dụng những ngôn từ như là tượng hình và tượng thanh. Kể chi tiết hình ảnh, cảm xúc, cảm giác theo công thức kể chuyện theo frame mà tôi đã có."*

**Lỗ hổng có thật, đã kiểm.** Trước hôm nay, chữ *"tượng hình"* và *"tượng thanh"* **không xuất hiện một lần nào** trong `wiki/`, Bảy hướng dẫn khung ở trên có nhắc "chi tiết" (`plain_story`: *"sức nặng nằm ở chi tiết"*; **B1**: *"kể chi tiết thật"*) nhưng **không chỗ nào nói chi tiết LOẠI GÌ**. Nên "chi tiết" bị thi hành thành *chi tiết thông tin* — ngày tháng, con số, tên riêng. Đúng luật B1, mà vẫn ra một câu chuyện **không ai nhìn thấy được**.

⚡ **B1 lo chi tiết ĐÚNG. Luật này lo chi tiết THẤY ĐƯỢC.** Hai việc khác nhau, và một câu chuyện cần cả hai.

#### Bốn neo, cắm vào đúng chặng mà khung đã có

Không đẻ thêm chặng nào — Đoàn nói rõ *"theo công thức kể chuyện theo frame mà tôi đã có"*. Khung nào có chặng kể chuyện thì cắm neo vào đúng chặng đó.

| Neo | Là gì | Ví dụ có thật trong bài của Đoàn |
|---|---|---|
| **Hình** *(tượng hình)* | Thứ mắt nhìn thấy, kể bằng **động tác** chứ không bằng tính từ | *"tôi ngồi nhìn màn hình, refresh liên tục"* · *"viết từng câu chữ, sắp từng khung hình"* |
| **Tiếng** *(tượng thanh)* | Âm thanh thật trong cảnh đó | *"tim tôi đập **thình thịch**"* |
| **Cảm xúc** | Gọi tên thẳng, không né | *"cảm giác vừa sững sờ, vừa nhẹ nhõm"* |
| **Cảm giác cơ thể** | Chỗ cảm xúc đó **nằm trên người** | *"như có ai nhấc hẳn tảng đá ra khỏi ngực mình"* · *"Tôi thở phào"* |

⚡ **Đúng ba câu liền nhau trong bài #3 làm đủ cả bốn neo.** Đó là đoạn cao trào, và nó là **mẫu chuẩn** của luật này — không phải bốn neo rải đều cả bài.

#### Đo được: 5 dòng, trên 19 bài, tất cả nằm trong MỘT bài

Quét 19 bài nguyên văn (`raw/kho-bai-viet-facebook-NGUYEN-VAN-2026-08-09.md`) bằng từ điển tượng thanh + tượng hình + cảm giác cơ thể:

| | Con số |
|---|---|
| Dòng có neo giác quan | **5** |
| Bài chứa chúng | **1** — bài #3 *"Đánh cược toàn bộ số tiền cuối cùng"* |
| Các bài kể chuyện còn lại | **7 bài — 0 dòng** |

🔴 **Đây KHÔNG phải vân tay giọng văn. Đây là thứ Đoàn muốn thêm.** Phân biệt này quan trọng và đừng để phiên sau xoá mất nó: `wiki/voice-profile.md` PHẦN 4B ghi thứ Đoàn **đang làm** (đo được, lặp lại trên nhiều bài); luật này ghi thứ Đoàn **muốn làm từ nay** (mới xảy ra 1/19 lần). Nhét nó vào PHẦN 4B là làm hỏng đúng nền bằng chứng của phần đó. **Bài #3 là tiền lệ, không phải thói quen.**

#### ⛔ Ranh giới — chỗ luật này tự hỏng

Chi tiết giác quan viết quá tay là **văn AI**, không phải văn hay. Bốn chốt chặn:

1. **Neo phải có thật.** Không nhớ hôm đó nghe thấy gì thì **để trống**. `CRAFT_NO_FABRICATION` áp nguyên: bịa ra một cơn mưa cho có hình ảnh là vi phạm **B1**, và B1 thắng.
2. **Cấm giọng brochure.** *"nắng vàng trải dài"*, *"không gian ấm cúng"*, *"bầu không khí sôi động"* — đó là **W4 (ngôn từ quảng cáo du lịch)** ở `luat/dau-hieu-ai-viet.md`, một **dấu hiệu AI**, không phải tượng hình.
3. **Ẩn dụ phải sờ được — C2 vẫn áp.** *"tảng đá trên ngực"* đạt. *"một khoảng lặng trong tâm hồn"* trượt.
4. **Chỉ cắm ở cảnh cao trào.** Rải giác quan lên mọi đoạn là làm **phẳng** bài — mà `luat/dau-hieu-ai-viet.md` Tầng 4 gọi đúng cái phẳng đó là dấu hiệu AI: *"bài AI đều một mức 'hay'"*.

📌 **Chỉnh một chỗ ở bản nháp C6** *(ở `luat/dau-hieu-ai-viet.md`, vẫn CHƯA DUYỆT)*. C6 viết *"cảm xúc thì BỘC LỘ, đừng mô tả — đừng viết 'tôi đã rất sốc'"*. Nhưng bài #3 **gọi thẳng tên cảm xúc** (*"sững sờ"*, *"nhẹ nhõm"*) rồi **mới** neo vào thân thể. Khuôn thật của Đoàn là **gọi tên + neo thân thể**, không phải "cấm gọi tên". Nếu về sau duyệt C6 thì phải sửa vế đó theo đây.


---

## Tầng 4 — Đặc trưng hình mẫu

`Analysis.formats` hiện là `[{ name, structure }]` và đi vào prompt viết bài dưới dạng `JSON.stringify()` thô, **không kèm lệnh nào** — nằm ngang hàng với dòng `Ngôn ngữ: vi`.

Đổi thành `[{ name, structure, howTo }]`:

- `howTo` là 2-3 câu dạy cách làm được mạch đó.
- Prompt phân tích phải chặn đúng cái bẫy dễ mắc: **cấm mô tả lại `structure` bằng chữ khác**. Phải nói ra thứ người đọc nhìn bài không tự thấy — chỗ nào là điểm lật, cái gì nói sớm và cái gì giữ tới cuối, đoạn nào cố tình ngắn.
- `howTo` để **optional** cho tương thích ngược. Bản phân tích cũ thiếu thì chạy bình thường. Hiện nhãn "phân tích lại để có hướng dẫn cách viết" trên trang hình mẫu, **không tự chạy lại** — đó là credit của user.

Phân biệt với tầng 2: khung trả lời *"bài này đi theo mạch nào"* (thuộc **nghề**, học được, không đổi theo ngách); `formats` trả lời *"người này có thói quen viết gì riêng"* (thuộc **cá tính** hình mẫu, phải rút từ bài thật mới có).

### ⚠️ Đính chính 2026-07-30 — hai tầng này KHÔNG phải hai loại khác nhau

Đoàn đọc lại và chỉ ra: khung viết và `formats` là **cùng một loại đồ vật** — đều là chuỗi chặng của một bài. Đúng. Đặt cạnh nhau thì thấy ngay:

| | Nội dung |
|---|---|
| Khung "Chuyển hoá 5 bước" | Hook → tôi từng sai thế này → cho đến khi → kết quả và bài học → mời |
| Format của Nguyễn Quang Khải | Hook bằng mốc thời gian cụ thể (2014 vỡ nợ) → mô tả chi tiết hoàn cảnh tệ hại → khoảnh khắc giác ngộ → đúc kết thành nguyên lý có tên riêng → framework 3 bước → câu hỏi phản tư → CTA để lại từ khoá |

Ranh giới thật là **tần suất, không phải loại**: mạch lặp lại ở NHIỀU người thì gọi là nghề và đóng sẵn thành khung; mạch của MỘT người thì để nguyên là cá tính của họ. Bằng chứng: 5/7 khung chính là rút ra từ chỗ này — xem bảng đối chiếu ở `luat/hook.md`.

Và mạch của hình mẫu thường **chi tiết hơn** khung (7 chặng có ví dụ thật, so với 5 chặng gọn). Nên câu *"khung thắng hình mẫu"* trong mọi trường hợp là vứt đi phần chi tiết hơn.

**Quyết định của Đoàn:** ô "Khung viết" chứa **cả hai nhóm** — 7 khung của mình, và các mạch của hình mẫu đang chọn. Người viết tuỳ bài mà chọn bên nào. Khi chủ động chọn mạch hình mẫu thì mạch đó **là** khung, không còn là tham khảo. Kèm một ranh giới cứng trong prompt: chọn mạch hình mẫu là mượn **cách kể**, không mượn chất liệu — chuyện, số liệu, tên người vẫn phải của người viết (luật B1 và C5).

Thứ tự thắng ở đầu trang **không đổi**: khung vẫn thắng đặc trưng hình mẫu. Chỉ khác ở chỗ giờ khung *có thể chính là* một mạch của hình mẫu, do người viết chọn. Không ai chọn thì AI chọn 1 trong (7 khung + các mạch hình mẫu) và phải nói ra chọn cái nào.

### Hình mẫu vào cả ba màn hình viết — mỗi chỗ một kiểu (2026-07-30)

| Màn hình | Hình mẫu cho gì | Ghi chú |
|---|---|---|
| Viết bài | Thông điệp cốt lõi + mạch bài | Hình mẫu là *nguyên liệu*, nên chọn trước |
| Soi bài | Chỉ mạch bài, để đối chiếu | Một ô duy nhất, không cần chọn hình mẫu trước — bài đã tồn tại rồi |
| Viết hook | **Hook THẬT**, bóc từ tối đa 12 bài mẫu | Chỗ duy nhất hình mẫu cho dữ liệu thật thay vì bản phân tích cô lại |

⚡ **Luật C5 tới đây mới chạy đủ hai cấp như nguồn gốc.** [[teachings/thoi-mien-bang-ngon-tu]] ghi Vitale nêu phép thử này ở **cả tiêu đề và toàn bài**; bản bake 2026-07-29 chỉ áp được cấp toàn bài. Tính năng hook giờ áp cấp tiêu đề: *"hook này đem áp thẳng vào một bài của hình mẫu có dùng được luôn không? Nếu được thì nó chưa phải hook của bài này."*

⚠️ **Hook là chỗ dễ trượt sang nhái nhất trong cả tool**, và lý do cụ thể: một *mạch bài* đủ trừu tượng để "mượn cách kể" vẫn an toàn, còn một *hook* chỉ dài 1-3 câu — khoảng cách từ "bắt chiếc" tới bản sao gần như bằng không. Ba lớp chặn ghi ở `api/posts/hooks/route.ts`; đừng gỡ lớp nào mà không đọc chú thích ở đó trước.

---

## Quan hệ với các trang khác

- `luat/vi-du-luat-rieng.md` — bản **cá nhân của Đoàn**, phát kèm làm **ví dụ mẫu**. Lõi nghề rút từ đây và đã lọc bỏ phần chỉ thuộc về Đoàn, nên file đó **không còn nằm trong danh sách đọc bắt buộc** *(gỡ 2026-09-06)*: để nguyên trong danh sách là phát giọng của Đoàn kèm nghề, đúng thứ dòng đầu skill cấm.
- `wiki/voice-profile.md` PHẦN 8 — danh sách kiểm 7 điểm trước khi publish, **của riêng Đoàn** (có mục đại từ "tôi/bạn"). Trùng khoảng 5/10 luật. Giữ nguyên, chỉ thêm dòng trỏ qua đây.
- [[content-modeling-playbook]] — tiêu chí chọn bài mẫu. Không đụng nhau: playbook lo *chọn nguyên liệu*, file này lo *cách viết*.
- `.claude/skills/viet-content/SKILL.md` — quy trình viết bài cho Đoàn. Đọc file này thay vì chép.

### Ba trang cùng tầng "nghề chung" — bổ sung 2026-07-29

File này lo phần **thân bài**. Ba trang dưới lo ba khâu còn lại, cùng rút từ code `creator-dna` cùng ngày:

- `luat/hook.md` — **8 kiểu hook**. Giải cho câu ở mục "Triệu chứng" phía trên (*hook sắc, thân bài nhạt — vì lớp hook đã có 8 kiểu với hướng dẫn nghề thật, còn thân bài thì không có gì*): 8 kiểu đó nay đã có trong bộ não, không còn chỉ nằm trong `lib/hooks.ts`.
- [[story-selection-protocol]] — chọn **chuyện nào** để chứng minh thông điệp. Đứng TRƯỚC file này trong quy trình: chọn sai nguyên liệu thì viết đúng luật vẫn ra bài rỗng.
- [[post-performance-framework]] — đo bài SAU khi đăng. Đóng vòng lặp: bài 💎 *Mỏ vàng bị chôn* quay lại `luat/hook.md`, bài ⚠️ *Viral rỗng* quay lại file này.
- [[tuyen-noi-dung]] *(thêm 2026-08-13)* — ba tuyến **viral · brand · sales**, tức bài đang tối ưu cho trục đo nào. Liên quan trực tiếp tới file này ở hai chỗ: cột **Hợp tuyến** của bảng 7 khung là thứ nối khung với tuyến, và luật **C4** (được phép giật tít) là luật mà tuyến `viral` dựa vào — **C4 không nới ra theo tuyến**, điều kiện **B2** vẫn nguyên.

## Links

`luat/vi-du-luat-rieng.md` · `wiki/voice-profile.md` · `luat/hook.md` · [[story-selection-protocol]] · [[post-performance-framework]] · [[voice-profile]] · [[projects/creator-os]] · [[content-modeling-playbook]] · [[contrarian-beliefs]] · [[values-and-principles]] · [[target-customer]] · [[personal-mission]] · [[goals]]
