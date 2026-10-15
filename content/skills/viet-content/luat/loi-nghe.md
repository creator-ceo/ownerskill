# Writing Craft Core — lõi nghề viết dùng chung

> 📎 **Đọc file này thế nào.** Đây là luật nghề viết dùng chung, đóng gói nguyên văn để bạn dùng.
> Các ví dụ, con số và tên người (nếu có) trong file chỉ để minh hoạ luật. 🚫 Tuyệt đối không bê chúng vào bài của bạn — đó là vi phạm chính luật cấm bịa ở đây.

> **Đây là lớp luật viết phổ quát**, áp cho mọi người viết bất kể ngách. Giọng riêng của bạn nằm ở `wiki/voice-profile.md`; `luat/vi-du-luat-rieng.md` chỉ là **ví dụ** một bộ luật riêng trông thế nào, không phải luật bạn phải theo.
> Trạng thái: **đang thử nghiệm** — chưa qua kiểm chứng bằng nhiều bài thật, hãy chỉnh khi dùng.


## Vì sao cần lớp này

Phần lớn hướng dẫn viết bài chỉ lo **nội dung** (viết cái gì, chứng minh bằng chuyện nào, cho ai) mà bỏ trống **cách viết**. Khi đó chất lượng câu chữ phó mặc cho model nền — mà văn mặc định của model đúng là thứ lớp luật này đang cấm.

Triệu chứng dễ thấy nhất: **hook sắc, thân bài nhạt** — vì hook đã có 8 kiểu với hướng dẫn nghề thật (`luat/hook.md`), còn thân bài thì không có gì.

---

## Kiến trúc 4 tầng và thứ tự thắng

```
Lõi nghề  >  Khung viết  >  Giọng cá nhân  >  Đặc trưng hình mẫu
```

| Tầng | Là gì | Ai quyết | Có mặt khi nào | Dùng ở |
|---|---|---|---|---|
| **1. Lõi nghề** | 10 luật bắt buộc | Cố định, duyệt sẵn | Luôn luôn | Viết bài + soi bài |
| **2. Khung viết** | 7 khung, mỗi khung có mạch + hướng dẫn | Bạn chọn, hoặc AI chọn trong 7 | Luôn có | Viết bài + soi bài |
| **3. Giọng cá nhân** | Hồ sơ giọng ở `wiki/voice-profile.md` | Từng người viết | Khi đã dựng hồ sơ | Viết bài + soi bài |
| **4. Đặc trưng hình mẫu** | Cách làm của hình mẫu đã phân tích | Bản phân tích | Chỉ khi chọn hình mẫu | Viết bài |

**Vì sao thứ tự đó:**
- Khung thắng giọng vì khung là lựa chọn cho riêng bài này, còn giọng là hồ sơ đứng sẵn.
- Giọng thắng đặc trưng hình mẫu vì mục tiêu là viết giọng mình, không phải nhái người ta.

Không có thứ tự này thì prompt viết bài có hai dòng nói về cùng một thứ (format hay dùng của hình mẫu, và khung viết do bạn chọn) mà không ai thắng ai.

---

## ⚡ Trước cả 4 tầng — quy trình xác định NÓI GÌ

> Bốn tầng trên quyết định **VIẾT THẾ NÀO** (cấu trúc/giọng/hình mẫu). Không tầng nào trả lời câu hỏi đến trước: viết bài này **để làm gì**, và **lấy gì để chứng minh**. Quy trình dưới đây nằm TRƯỚC cả 4 tầng.

**7 bước, đúng thứ tự — mỗi bước là input của bước sau:**

1. **Mục tiêu bài viết** — bài này để làm gì
2. **Hành vi mục tiêu** — muốn người đọc làm gì sau khi đọc xong (kêu gọi hành động)
3. **Thông điệp** — từ hành vi mục tiêu suy ra thông điệp cần truyền tải
4. **Luận điểm / bằng chứng** — câu chuyện (của mình hoặc sưu tầm) hoặc số liệu/nghiên cứu/phân tích để chứng minh thông điệp
5. **Cấu trúc** — chọn từ hình mẫu, học cấu trúc của người đang làm tốt → nối thẳng vào **Tầng 2** ở trên
6. **Giọng điệu** — giọng thật của chính mình, phân tích ra chứ không "diễn" → nối thẳng vào **Tầng 3**
7. **Viết**

⚡ **Mở rộng khái niệm "chất liệu của mình" ở bước 4:** những câu chuyện mình đã đọc của người khác, hay những phân tích, nghiên cứu mình đọc được, cũng có thể là trải nghiệm của mình, miễn là ghi rõ nguồn. Không giới hạn ở chuyện đời thật xảy ra với chính mình — **đọc/tìm thấy một điều gì đó cũng là một trải nghiệm thật**, đủ tư cách làm luận điểm. Đây là câu trả lời trực tiếp cho nỗi sợ *"tôi không có gì để kể"*.

📌 **Bước 5 và 6 là chỗ nối vào hệ đã có** — không đẻ khung song song. Bước 5 = việc chọn 1 trong **Tầng 2 — 7 khung viết**. Bước 6 = **Tầng 3 — Giọng cá nhân** (hồ sơ giọng). Bốn bước đầu (1–4) quyết định NỘI DUNG trước khi bốn tầng quyết định HÌNH THỨC.

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

### Gốc của một số luật

Không luật nào là suy đoán. Một vài luật có gốc công khai:

- **Lời mở "người đọc đang bận nghĩ chuyện khác"** — rút từ sách của Roy Garn về từ huyệt cảm xúc. Cố ý để dạng lời mở chứ không thành một luật riêng: nó không bảo phải làm gì, nó đổi giả định mà cả mười luật kia đứng lên.
- **A2 (vế "trả lời điều người đọc đang cãi"), C1 (câu chủ động, dấu phẩy), C3 (câu hỏi đóng)** — rút từ sách về thôi miên bằng ngôn từ. Câu chủ động và dấu phẩy **soi được bằng máy**; "trả lời được bằng có/không" thì kiểm được ngay, khác với chữ "câu hỏi chung chung" khó kiểm.
- **C5** — phép thử của Vitale, nêu ở hai cấp: tiêu đề (*"tiêu đề này có áp vào quảng cáo của đối thủ được không?"*) và toàn bài (*"đối thủ có sao chép bản thảo này dùng cho sản phẩm của họ được không?"*). Thứ đối thủ không chép được chính là bằng chứng đã sống.
- **B2** là điều kiện để cho phép giật tít ở C4; **C3 có ngoại lệ** vì khuôn *"Hầu hết mọi người nghĩ X, nhưng với tôi Y"* là một khuôn sắc bén khi có lập trường thật phía sau.

### ⚡ B2 và B3 có thể đẩy bài về phía văn AI

Cả hai luật đều bảo: cắt mọi thứ không phục vụ thông điệp. Làm đúng tuyệt đối thì ra một bài **không còn chi tiết thừa nào** — mà chi tiết thừa lại chính là thứ chứng minh chuyện có thật (không ai bịa ra chi tiết chẳng để làm gì).

Không phải lỗi của B2/B3. Nhưng chúng cần một đối trọng: xem bản nháp **luật C6 "Để lại dấu tay"** ở `luat/dau-hieu-ai-viet.md` (đang dùng thử).

### Ba thứ CỐ Ý không đưa vào lõi nghề

Vì thuộc lớp giọng cá nhân, ép cho mọi người là sai:

- **Cấm "tụi mình", "ảnh"** — gu vùng miền của từng người. Người ngách khác dùng bình thường.
- **Xưng "tôi", gọi "bạn"** — ngôi xưng là giọng, không phải nghề.
- **Các trục tư tưởng riêng** (điều bạn tin về tiền, về học, về cho đi…) — là niềm tin của từng người, không phải kỹ thuật viết. Chỗ của chúng là `wiki/voice-profile.md`.

### Một chỗ dễ hiểu nhầm: B1 và C5 không cấm trích dẫn

Hai luật này cấm **nhận vơ**, không cấm **trích dẫn**:

- **B1** cấm *bịa* số/tên/kết quả. Trích một con số **có nguồn, ghi rõ nguồn** không phải bịa.
- **C5** hỏi *"đổi tên người viết sang người cùng ngành thì bài còn là của mình không"* — nó áp cho **lõi phân biệt** của bài (chuyện đã sống, số đã đo, người đã gặp, giá đã trả), **không** áp cho bằng chứng phụ trợ có dẫn nguồn.

Trích dẫn người có thẩm quyền là một loại bằng chứng **hợp lệ**, không phải khoản phải trừ. Ranh giới là ***kiểm chứng được hay không***, không phải *có phải chuyện của mình không*.

**Cách nhớ:** mượn **có ghi nguồn** = bằng chứng · mượn **rồi kể như của mình** = vi phạm.

---

## Tầng 2 — 7 khung viết

Mỗi khung có một hướng dẫn nghề riêng, không phải nhãn suông. Lý lẽ: cho AI tự do thì nhận về bảy biến thể của cùng một mạch; ép theo khung mới ra mạch thật sự khác.

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

| Khung | Cách làm cho đúng |
|---|---|
| **Chuyển hoá 5 bước** | Sức nặng nằm ở đoạn *"tôi từng sai"*, không ở đoạn kết quả. Kể cái sai đủ cụ thể để người đọc thấy mình trong đó, rồi mới được quyền kể cái đúng. Đoạn *"cho đến khi"* phải là một thời điểm có thật, không phải một quá trình mơ hồ. |
| **Bằng chứng dẫn đường** | Mở bằng kết quả thì phải là kết quả **đo được, có thật**. Phần *"điều kiện để lặp lại"* là phần hay bị bỏ và là phần khiến bài khác một bài khoe: nói thẳng ai làm được, ai chưa nên làm, cần có sẵn gì. |
| **Lật ngược niềm tin** | Chỉ lật khi có chuyện thật đỡ phía sau — lật cho sốc là hỏng. Phải nêu điều số đông tin bằng **phiên bản mạnh nhất** của nó (không dựng bù nhìn dễ đánh), rồi mới chỉ chỗ nó hỏng. |
| **Một sai lầm đắt giá** | Đoạn *"vì sao lúc đó tin là đúng"* là đoạn quyết định. Thiếu nó, bài thành tự trách; có nó, người đọc nhận ra chính mình đang tin điều đó. Cái giá phải nói bằng con số hoặc bằng thứ mất đi cụ thể, không nói bằng tính từ. Và phần *sai lầm + cái giá* phải **nặng hơn** phần *điều đã đổi* — đếm đoạn cũng được. Kể giải pháp dài hơn kể sai lầm là bài trượt thành quảng cáo cho giải pháp, dù không có một câu bán nào. Đây là luật đối xứng của khung *Trước/sau của người khác* (phần mình làm phải nhỏ hơn phần họ thay đổi). |
| **Bóc một câu hỏi** | Trả lời **thẳng trong 2 câu đầu**, không vòng vo lấy đà — người đọc có câu trả lời rồi mới chịu đọc phần giải thích. Câu hỏi phải là câu khách thật sự hỏi, bằng đúng chữ họ dùng. |
| **Trước / sau của người khác** | Phần *"mình đã làm gì"* phải **nhỏ hơn** phần *"họ đã thay đổi thế nào"* — kể ngược lại là bài khoe công. Tình trạng ban đầu càng cụ thể thì khoảng cách càng thật. |
| **Kể thẳng một chuyện** | ⚠️ **ĐÂY LÀ KHUNG DỄ HỎNG NHẤT.** Sức nặng nằm ở chi tiết và ở chỗ **DỪNG LẠI** — dừng đúng lúc thì người đọc tự rút ra, dừng sai thì thành bài kể lể. Chỉ dùng khi chuyện đủ mạnh để tự đứng một mình. Tuyệt đối không thêm câu *"qua đó tôi nhận ra..."* ở cuối; nếu thấy cần thêm câu đó thì chuyện chưa đủ mạnh, hãy đổi khung khác. |

Khung 1 là công thức 5 bước (hook → sai → bước ngoặt → bài học → mời), nay là một lựa chọn có tên thay vì nằm mờ trong hồ sơ giọng.

Cột "Thông điệp" tồn tại vì đây chính là chỗ quyết định nói ra hay để ẩn — và đó là **quyết định theo từng bài**, nên nó thuộc tầng khung chứ không thuộc tầng luật. Luật áp cho mọi bài thì không được chọn hộ.

**"Để AI tự chọn" vẫn giữ**, nhưng bị ép chọn đúng 1 trong 7 và phải nói ra chọn khung nào.

Tên khung là bản v1, đổi được sau khi dùng thật.

### ⚡ Luật kể chuyện — CHI TIẾT PHẢI CHẠM ĐƯỢC GIÁC QUAN

> Nếu đã kể chuyện thì kể chi tiết bằng hình ảnh, âm thanh, cảm xúc và cảm giác trên cơ thể (tượng hình, tượng thanh), theo đúng chặng kể chuyện mà khung đã có.

**Một lỗ hổng hay gặp.** Các hướng dẫn khung ở trên có nhắc "chi tiết" (khung *Kể thẳng một chuyện*: *"sức nặng nằm ở chi tiết"*; **B1**: *"kể chi tiết thật"*) nhưng **không chỗ nào nói chi tiết LOẠI GÌ**. Nên "chi tiết" dễ bị thi hành thành *chi tiết thông tin* — ngày tháng, con số, tên riêng. Đúng luật B1, mà vẫn ra một câu chuyện **không ai nhìn thấy được**.

⚡ **B1 lo chi tiết ĐÚNG. Luật này lo chi tiết THẤY ĐƯỢC.** Hai việc khác nhau, và một câu chuyện cần cả hai.

#### Bốn neo, cắm vào đúng chặng mà khung đã có

Không đẻ thêm chặng nào. Khung nào có chặng kể chuyện thì cắm neo vào đúng chặng đó.

| Neo | Là gì | Ví dụ |
|---|---|---|
| **Hình** *(tượng hình)* | Thứ mắt nhìn thấy, kể bằng **động tác** chứ không bằng tính từ | *"tôi ngồi nhìn màn hình, refresh liên tục"* · *"viết từng câu chữ, sắp từng khung hình"* |
| **Tiếng** *(tượng thanh)* | Âm thanh thật trong cảnh đó | *"tim tôi đập **thình thịch**"* |
| **Cảm xúc** | Gọi tên thẳng, không né | *"cảm giác vừa sững sờ, vừa nhẹ nhõm"* |
| **Cảm giác cơ thể** | Chỗ cảm xúc đó **nằm trên người** | *"như có ai nhấc hẳn tảng đá ra khỏi ngực mình"* · *"Tôi thở phào"* |

⚡ **Ba câu liền nhau làm đủ cả bốn neo** là mẫu chuẩn của luật này, đặt ở đoạn cao trào — không phải bốn neo rải đều cả bài.

🔴 **Đây là thứ bạn muốn thêm vào giọng, không phải thói quen đã đo được.** Đừng ghi nó vào hồ sơ giọng như một vân tay có sẵn nếu bài cũ của bạn hầu như không có.

#### ⛔ Ranh giới — chỗ luật này tự hỏng

Chi tiết giác quan viết quá tay là **văn AI**, không phải văn hay. Bốn chốt chặn:

1. **Neo phải có thật.** Không nhớ hôm đó nghe thấy gì thì **để trống**. Luật cấm bịa áp nguyên: bịa ra một cơn mưa cho có hình ảnh là vi phạm **B1**, và B1 thắng.
2. **Cấm giọng brochure.** *"nắng vàng trải dài"*, *"không gian ấm cúng"*, *"bầu không khí sôi động"* — đó là **W4 (ngôn từ quảng cáo du lịch)** ở `luat/dau-hieu-ai-viet.md`, một **dấu hiệu AI**, không phải tượng hình.
3. **Ẩn dụ phải sờ được — C2 vẫn áp.** *"tảng đá trên ngực"* đạt. *"một khoảng lặng trong tâm hồn"* trượt.
4. **Chỉ cắm ở cảnh cao trào.** Rải giác quan lên mọi đoạn là làm **phẳng** bài — mà `luat/dau-hieu-ai-viet.md` Tầng 4 gọi đúng cái phẳng đó là dấu hiệu AI: *"bài AI đều một mức 'hay'"*.


📌 **Chỉnh một chỗ ở bản nháp C6** *(ở `luat/dau-hieu-ai-viet.md`)*. C6 viết *"cảm xúc thì BỘC LỘ, đừng mô tả — đừng viết 'tôi đã rất sốc'"*. Nhưng nhiều đoạn cao trào hay **gọi thẳng tên cảm xúc** (*"sững sờ"*, *"nhẹ nhõm"*) rồi **mới** neo vào thân thể. Khuôn đúng là **gọi tên + neo thân thể**, không phải "cấm gọi tên". Khi dùng C6 phải hiểu vế đó theo đây.

---

## Tầng 4 — Đặc trưng hình mẫu

Mỗi định dạng của hình mẫu nên kèm 2-3 câu dạy **cách làm** được mạch đó, không chỉ tên và cấu trúc.

- Cấm mô tả lại cấu trúc bằng chữ khác. Phải nói ra thứ người đọc nhìn bài không tự thấy — chỗ nào là điểm lật, cái gì nói sớm và cái gì giữ tới cuối, đoạn nào cố tình ngắn.
- Nếu bản phân tích cũ chưa có phần cách làm thì vẫn dùng bình thường; chỉ phân tích lại khi cần.

Phân biệt với tầng 2: khung trả lời *"bài này đi theo mạch nào"* (thuộc **nghề**, học được, không đổi theo ngách); định dạng của hình mẫu trả lời *"người này có thói quen viết gì riêng"* (thuộc **cá tính** hình mẫu, phải rút từ bài thật mới có).

### Khung viết và định dạng của hình mẫu là cùng một loại

Cả hai đều là chuỗi chặng của một bài. Đặt cạnh nhau thì thấy ngay:

| | Nội dung |
|---|---|
| Khung "Chuyển hoá 5 bước" | Hook → tôi từng sai thế này → cho đến khi → kết quả và bài học → mời |
| Định dạng của một người làm nội dung | Hook bằng mốc thời gian cụ thể (một năm vỡ nợ) → mô tả chi tiết hoàn cảnh tệ hại → khoảnh khắc giác ngộ → đúc kết thành nguyên lý có tên riêng → framework 3 bước → câu hỏi phản tư → CTA để lại từ khoá |

Ranh giới thật là **tần suất, không phải loại**: mạch lặp lại ở NHIỀU người thì gọi là nghề và đóng sẵn thành khung; mạch của MỘT người thì để nguyên là cá tính của họ. Bằng chứng: 5/7 khung chính là rút ra từ chỗ này — xem bảng đối chiếu ở `luat/hook.md`.

Và mạch của hình mẫu thường **chi tiết hơn** khung (7 chặng có ví dụ thật, so với 5 chặng gọn). Nên câu *"khung thắng hình mẫu"* trong mọi trường hợp là vứt đi phần chi tiết hơn.

**Cách làm:** ô "Khung viết" chứa **cả hai nhóm** — 7 khung ở trên, và các mạch của hình mẫu đang chọn. Người viết tuỳ bài mà chọn bên nào. Khi chủ động chọn mạch hình mẫu thì mạch đó **là** khung, không còn là tham khảo. Kèm một ranh giới cứng: chọn mạch hình mẫu là mượn **cách kể**, không mượn chất liệu — chuyện, số liệu, tên người vẫn phải của người viết (luật B1 và C5).

Thứ tự thắng ở đầu trang **không đổi**: khung vẫn thắng đặc trưng hình mẫu. Chỉ khác ở chỗ giờ khung *có thể chính là* một mạch của hình mẫu, do người viết chọn. Không ai chọn thì AI chọn 1 trong (7 khung + các mạch hình mẫu) và phải nói ra chọn cái nào.

### Hình mẫu dùng thế nào ở từng việc

| Việc | Hình mẫu cho gì | Ghi chú |
|---|---|---|
| Viết bài | Thông điệp cốt lõi + mạch bài | Hình mẫu là *nguyên liệu*, nên chọn trước |
| Soi bài | Chỉ mạch bài, để đối chiếu | Không cần chọn hình mẫu trước — bài đã tồn tại rồi |
| Viết hook | **Hook THẬT**, bóc từ tối đa 12 bài mẫu | Chỗ duy nhất hình mẫu cho dữ liệu thật thay vì bản phân tích cô lại |

⚡ **Luật C5 chạy ở cả hai cấp**: tiêu đề và toàn bài. Với hook, áp cấp tiêu đề: *"hook này đem áp thẳng vào một bài của hình mẫu có dùng được luôn không? Nếu được thì nó chưa phải hook của bài này."*

⚠️ **Hook là chỗ dễ trượt sang nhái nhất**, và lý do cụ thể: một *mạch bài* đủ trừu tượng để "mượn cách kể" vẫn an toàn, còn một *hook* chỉ dài 1-3 câu — khoảng cách từ "bắt chước" tới bản sao gần như bằng không. Luôn đối chiếu hook với bài mẫu trước khi dùng.

---

## Quan hệ với các trang khác

- `luat/vi-du-luat-rieng.md` — chỉ là **ví dụ** một bộ luật riêng, không nằm trong danh sách đọc bắt buộc: đưa nó vào là phát giọng của người khác kèm nghề.
- `wiki/voice-profile.md` — hồ sơ giọng của bạn, gồm cả danh sách kiểm trước khi đăng. Trùng một phần với các luật ở đây; giữ nguyên.
- `luat/hook.md` — **8 kiểu hook**. Giải cho câu ở mục "Vì sao cần lớp này": hook sắc nhưng thân bài nhạt.
- `luat/dau-hieu-ai-viet.md` — các dấu hiệu bài do AI viết, nguyên liệu cho C1 và C3.
- `SKILL.md` — quy trình viết bài. Đọc file đó thay vì chép lại ở đây.

## Links

`luat/vi-du-luat-rieng.md` · `wiki/voice-profile.md` · `luat/hook.md` · `luat/dau-hieu-ai-viet.md`
