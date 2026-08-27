# Hook — 8 kiểu và kỷ luật dùng hook

> 📎 **Đọc file này thế nào.** Đây là luật nghề của Tô Hải Đoàn, đóng gói nguyên văn để bạn dùng.
> Các liên kết dạng `[[tên-trang]]` trỏ tới những trang trong bộ não **của Đoàn**. Trang nào bộ não của bạn chưa có thì **bỏ qua liên kết đó** — đừng đoán nội dung của nó, và đừng bịa ra cho đủ. Muốn có trang tương đương thì tự dựng bằng `/nap-kho`.
> Các ví dụ, con số và tên người trong file là **của Đoàn**, dùng để minh hoạ luật. 🚫 Tuyệt đối không bê chúng vào bài của bạn — đó là vi phạm chính luật cấm bịa ở đây.


> **Nguồn:** rút từ `creator-dna/src/lib/hooks.ts` ngày 2026-07-29. Trước đó kiến thức này **chỉ tồn tại trong code** — `luat/loi-nghe.md` có nhắc "lớp hook đã có 8 kiểu với hướng dẫn nghề thật" nhưng không ai đọc được 8 kiểu đó ở đâu trong bộ não.
>
> Đây là tầng **nghề chung** (học được, không đổi theo ngách), cùng hạng với 10 luật ở `luat/loi-nghe.md`. Khác với `wiki/voice-profile.md` là tầng *giọng riêng*.

---

## Hook là gì — định nghĩa hẹp, cố ý

**Hook = dòng đầu tiên có chữ của bài.** Không phải một trường riêng, không phải metadata, không phải "đoạn mở đầu".

Vì sao hẹp như vậy là cố ý:

- Lưu hook tách khỏi bài thì hai thứ lệch nhau ngay lần sửa bài đầu tiên, và **không có cách nào biết cái nào mới đúng**.
- Thay hook = thay đúng một dòng, giữ nguyên phần còn lại. Nếu "thông minh" hơn — tự nhận ra hook là cả đoạn rồi thay cả đoạn — thì đoán sai một lần là nuốt mất một đoạn nội dung thật.

**Hook chịu trách nhiệm cho đúng MỘT việc: làm người ta dừng lại và đọc.** Người đọc xong có nhắn tin hay không là chuyện của thân bài và CTA. Nhớ ranh giới này, vì nó quyết định cách chọn hook mẫu ở mục cuối.

---

## 8 kiểu hook

Lấy từ chính **format hay dùng đã phân tích được ở hình mẫu của Đoàn** (xem [[content-modeling-playbook]] + phần `formats` trong phân tích hình mẫu 5 lớp) — **không phải** danh sách hook giật tít chung chung trên mạng.

| # | Kiểu | Cách làm cho đúng |
|---|---|---|
| 1 | **Lật ngược niềm tin** | Nói ngược lại điều số đông đang tin về chủ đề này. Chỉ dùng khi **thân bài thật sự chứng minh được** điều ngược đó — không lật ngược cho sốc. |
| 2 | **Con số / bằng chứng** | Mở bằng một con số hoặc bằng chứng **có thật lấy ra từ chính bài**. Tuyệt đối không bịa số, không làm tròn cho đẹp. |
| 3 | **Câu chuyện thật** | Mở bằng một khoảnh khắc cụ thể có trong bài: ai, lúc nào, đang làm gì. Cụ thể tới mức người đọc thấy được hình ảnh. |
| 4 | **Gọi đúng cơn đau** | Nói trúng thứ người đọc đang vướng, bằng **đúng chữ họ hay dùng khi than về nó** — không phải chữ của người bán hàng. |
| 5 | **Thú nhận sai lầm** | Kể cái mình từng làm sai và cái giá đã trả. Chỉ dùng khi bài có sai lầm thật **của chính người viết** — không mượn sai lầm của người khác. |
| 6 | **Trước / sau** | Đặt cạnh nhau hai trạng thái của cùng một người hoặc một việc. Sức nặng nằm ở **khoảng cách giữa hai vế**, không ở tính từ. |
| 7 | **Tuyên bố dứt khoát** | Một câu khẳng định ngắn, không rào đón, không "có lẽ / mình nghĩ là". Ngắn hơn thì mạnh hơn. |
| 8 | **Gọi đúng tên nhóm người** | Chỉ đích danh ai nên đọc tiếp, bằng **hoàn cảnh cụ thể** chứ không phải nhãn nghề nghiệp chung chung. |

### ⚡ Ép mỗi kiểu đúng 1 hook — đây mới là điểm

Xin 8 hook "tuỳ ý" thì nhận về **8 biến thể của cùng một ý, khác nhau vài chữ**. Ép theo kiểu là ép ra góc *thật sự* khác — đó là toàn bộ lý do sinh nhiều hook thay vì một.

Cùng một cơ chế với 7 khung viết ở `luat/loi-nghe.md`: cho tự do thì nhận về cái trung bình của mọi lựa chọn.

### 5/7 khung viết chính là kiểu hook được nâng lên thành khung cả bài

Truy nguyên 2026-07-30, khi Đoàn hỏi 7 khung ở `luat/loi-nghe.md` lấy từ đâu:

| Khung viết | Kiểu hook gốc ở trang này |
|---|---|
| Lật ngược niềm tin | #1 Lật ngược niềm tin |
| Bằng chứng dẫn đường | #2 Con số / bằng chứng |
| Một sai lầm đắt giá | #5 Thú nhận sai lầm |
| Trước / sau của người khác | #6 Trước / sau |
| Kể thẳng một chuyện | #3 Câu chuyện thật |

Hai khung còn lại: **Chuyển hoá 5 bước** = công thức 5 bước của Đoàn ở `wiki/voice-profile.md` PHẦN 2. **Bóc một câu hỏi** — ⚠️ **không có nguồn nào trong bộ não**, không có trong 8 kiểu hook, không có trong `formats` của cả 4 hình mẫu ở [[models/matt-gray]] · [[models/nguyen-quang-khai]] · [[models/thao-tran]] · [[models/tran-manh-duc]]. Khung này là **nghĩ ra, không phải rút ra** — chờ Đoàn quyết giữ hay bỏ.

Chuỗi truy nguyên đầy đủ vì vậy là: **bài thật của 4 hình mẫu → phân tích `formats` → 8 kiểu hook → 5 khung viết.** Đây chính là bằng chứng cho đính chính ở `luat/loi-nghe.md`: khung và `formats` là cùng một loại, ranh giới là tần suất chứ không phải loại.

⚠️ Còn một khoản nợ nữa: phần `guide` (hướng dẫn nghề) của **6/7 khung** không lấy từ nguồn nào — viết ra trong lúc code ngày 2026-07-29, chưa qua kiểm chứng bằng bài thật. Spec chỉ chốt cột *mạch*, và chỉ viết ra `guide` cho đúng khung 7. Đừng coi 6 `guide` kia là luật đã duyệt.

### Kiểm chéo với luật lõi nghề

Ba kiểu có điều kiện, và điều kiện đều là **luật B1 (cấm bịa)** ở `luat/loi-nghe.md`:

- Kiểu 2 cần số thật → không có số thật thì đổi kiểu, đừng bịa.
- Kiểu 5 cần sai lầm của chính mình → mượn sai lầm người khác là hỏng cả bài, không riêng hook.
- Kiểu 1 cần thân bài đỡ được → xem luật **B2 (trả nợ cho thứ đã hứa)**.

Kiểu 4 và 8 đòi **chữ của người đọc** — lấy ở [[target-customer]] và [[audience-insights]], không tự nghĩ ra.

---

## Vì sao KHÔNG chấm điểm hook bằng AI

Đoàn đã chốt (2026-07-25): *"không chấm điểm giọng văn, nhưng chấm hook thì được"*.

**Chỗ rất dễ hiểu nhầm:** cho phép chấm **không có nghĩa** là để AI tự chấm bài của chính nó. AI chấm hook nó vừa viết ra chỉ là một con số tự khen — đúng loại *chính xác giả* mà quy trình soi bài đã cố ý bỏ đi.

**Cái chấm được là THỰC TẾ:** bài nào đăng ra kéo được người đọc thì hook bài đó thắng. Có số liệu thật, không cần ai cho điểm.

> Đây là một ca nữa của cùng một cơ chế đã ghi ở `log.md`: một câu chốt gọn ("chấm hook thì được") đọc rời ngữ cảnh sẽ dẫn tới đúng cái tác giả không định.

---

## Thư viện hook đã thắng

Hook thắng lấy từ bài thật đã đăng, đưa ngược vào prompt làm **ví dụ thật của chính mình** — thay vì ví dụ vay mượn.

### Lấy theo trục lan toả, KHÔNG lấy theo điểm tổng

Đây là chỗ dễ làm sai nhất của cả tính năng.

Theo ma trận 2 trục ở [[post-performance-framework]], hook thắng gồm **cả 🏆 Nhân bản LẪN ⚠️ Viral rỗng**:

- 🏆 Nhân bản — lan toả tốt, chuyển đổi tốt.
- ⚠️ Viral rỗng — lan toả tốt, chuyển đổi kém. **Hook vẫn thắng**, vì hook chỉ chịu trách nhiệm kéo người vào. Chính lời khuyên của ô này đã nói: *"GIỮ NGUYÊN hook (nó đang chạy tốt), sửa phần sau"*.

Lọc theo *điểm tổng* thay vì theo *trục lan toả* sẽ **vứt mất đúng một nửa số hook đã được thực tế chứng minh**.

### Khi nào được nói "kiểu X đang thắng ở tài khoản này"

Ba chốt chặn, cả ba đều để tránh biến vài bài lẻ thành "quy luật":

1. Cần ít nhất **3 hook thắng có ghi kiểu**. Dưới ngưỡng đó chỉ là mô tả lại một hai bài.
2. Kiểu dẫn đầu phải xuất hiện **từ 2 lần trở lên**. Mỗi kiểu đúng 1 lần = không kiểu nào thắng.
3. **Hoà nhau thì không kết luận gì.** Câu "3 trong 6 hook thắng là kiểu X" vẫn đúng số học khi kiểu Y cũng có 3 — nhưng người đọc sẽ hiểu X hơn Y rồi viết theo X. *Nói một sự thật theo cách dẫn tới kết luận sai thì cũng là nói sai.*

⚠️ Kiểu hook chỉ được ghi lại khi hook do tool sinh ra và người dùng bấm áp vào bài. Bài viết tay hoặc bài cũ hơn tính năng thì **không suy ngược ra được**. Nên rất lâu lúc đầu sẽ không có kết luận nào — **và như vậy là đúng**.

---

## Vay từ hình mẫu — ba kỹ thuật đo được, không phải cảm nhận

> Nạp 2026-08-08 từ [[models/matt-gray]]. **Đây là KỸ THUẬT, không phải hook để chép.** Câu chữ, con số, chuyện phải là của Đoàn — luật **B1** và **C5** ở `luat/loi-nghe.md`.

### 1. Viết 5 tiêu đề cho MỘT nội dung, theo 5 trục kéo khác nhau, rồi mới chọn

Matt Gray để lộ nguyên khối *"Video title ideas (for the algo)"* trong **75/165** mô tả podcast công khai. Ví dụ, cùng một tập về deep work:

| Trục kéo | Tiêu đề |
|---|---|
| Sở hữu | *My Deep Work Routine* |
| Đánh đổi | *My Deep Work Protocol (More Output, Less Time)* |
| Con số gây sốc | *How I Work 20 Hours a Week* |
| Quyền lực | *The 4-Hour Deep Work System That Runs My Empire* |
| So sánh | *How to Get More Done in 4 Hours Than Most Do in 4 Days* |

⚡ Đây là **bài tập đặt hook có sẵn đáp án**: một nội dung, năm cách kéo. Áp được ngay vào tính năng sinh 8 hook ở [[projects/creator-os]]. Kho đầy đủ 50 khối / 238 dòng nằm ở `raw/matt-gray-rss-165-tap-2026-08-08.md`.

### 2. Công thức ngoặc đơn + dấu hai chấm (dạng ảnh bìa / carousel)

Ngoặc đơn nói rõ **phần thưởng** hoặc **điều kiện**; dấu hai chấm là lời hứa *"nội dung ở slide sau"*:

> *…in 30 days **(if I lost it all tomorrow)**:* · *…personal brand **(find your level in 30 seconds)**:* · *…**(and the one belief that separates them)**:* · *…**(in 5 simple steps)*** · ***(Steal my structure)***

Khác vai với hook bài viết: hook bài viết giữ người **đọc tiếp**; hook ảnh bìa giữ người **vuốt tiếp**. Đoàn đang làm carousel qua skill `anh-quote` — đây là khuôn cho dòng đầu.

### 3. Công thức mở bài mạnh nhất đo được: **"Số đông nghĩ X. Không phải."**

Đọc tận nơi 10 bài LinkedIn gần nhất (2026-08-08): **4/10 = 40%** mở bằng đúng khuôn này.

> *"**Most founders think** clarity comes from more planning. It doesn't. It comes from fewer questions, asked better."*
> *"**Most people don't have** a focus problem. They have a direction problem."*
> *"**Most people wake up and ask,** 'What should I do today?'"*

Khuôn ba nhịp: **nêu niềm tin số đông → phủ nhận cụt lủn → thay bằng cái đúng.** Nhịp giữa (*"It doesn't."* / *"They have a…"*) là chỗ tạo lực — càng cụt càng mạnh.

Họ hàng gần với *"It's not X, it's Y"* (33% theo MagicPost) — cùng một động tác, khác cách xuống dòng.

⚠️ **Chỗ phải cẩn thận với Đoàn:** khuôn này chỉ đúng khi **cái "số đông nghĩ" là thật**. Bịa một niềm tin số đông để phủ nhận cho oai là rơi vào đúng thứ [[contrarian-beliefs]] cảnh báo — trái chiều rỗng. Phải rút từ [[objections-library]] hoặc ghi chép 1-1 thật.

**Và 7/10 dòng mở kết bằng DẤU HAI CHẤM** — giống hệt công thức ảnh bìa Instagram ở mục 2. Trên hai kênh khác nhau, cùng một thủ pháp: **câu đầu không nói gì trọn vẹn, nó chỉ mở cửa.**

### 4. Số đo văn phong để chấm hook — có mốc so sánh

| Chỉ số | Matt Gray | Mặt bằng creator |
|---|---|---|
| Mở bài bằng CON SỐ | **40%** | 22% |
| Công thức "It's not X, it's Y" | 33% | — |
| Từ mỗi câu · mỗi đoạn | **8 · 9** | — |
| Hashtag · dấu chấm than | **0 · 0** | — |
| Tiêu đề mở bằng "how" (165 tập) | **41%** | — |

⚡ **Nghịch lý đáng chép nhất:** bài dài **gấp đôi** mặt bằng (402 từ vs 185) nhưng đọc thấy nhanh, vì câu 8 từ. **Dài mà lướt được** — không phải chọn giữa dài và dễ đọc.

⚠️ Ba bảng trên là **số của người khác đo** (MagicPost quét 758 bài), trừ dòng "how" là em tự đếm. Dùng làm **mốc so sánh**, đừng dùng làm mục tiêu — [[contrarian-beliefs]] belief số 6.

---

## Links
`luat/loi-nghe.md` · `luat/cau-chu.md` · `wiki/voice-profile.md` · [[post-performance-framework]] · [[story-selection-protocol]] · [[content-modeling-playbook]] · [[target-customer]] · [[audience-insights]] · [[projects/creator-os]] · [[models/matt-gray]]
