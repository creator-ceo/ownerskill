# 🗺️ Mindmap — `mindmap`

> ⚠️ **File này là chỗ DUY NHẤT chứa luật mindmap.** Sửa luật thì sửa ở đây.

Đây là loại việc **khác hẳn** mọi việc còn lại trong xưởng: nó **chạy lệnh ngoài** và **giao file HTML**, không giao chữ để bạn copy đi đăng. Chốt 2026-08-03 sau khi Đoàn so bộ thử.

### Chạy gì

1. **Lấy nguyên liệu.** Ba đường, khai `batMot` nên **phải có ít nhất một**, và có thể có nhiều hơn một cùng lúc:

   | Trong brief | Làm gì |
   |---|---|
   | `trangNguon: <đường dẫn>` | **Đọc trọn** `wiki/<trangNguon>.md`. Không tóm tắt từ trí nhớ, kể cả khi thấy mình vừa đọc trang đó trong phiên này |
   | `## Bài từ Notion` | Mở trang Notion đó, lấy nội dung |
   | `## Bài hiện có` | Dùng thẳng chữ đã dán |

   Server đã kiểm `trangNguon` trỏ vào file có thật trước khi ghi brief — nên **đừng tự sửa đường dẫn** nếu thấy nó lạ; nó đã qua cửa rồi.

   ⚡ **`mucChon: <tiêu đề ##>` (tuỳ chọn) — RÀNG BUỘC CỨNG, đọc trước khi rút gọn.**
   Thêm 2026-08-23 sau khi bạn báo trang gộp nhiều framework (vd `frameworks-core.md`
   gộp 5 cái) mà không có cách nào chọn đúng 1 mục — trước đó chỉ gõ tay vào `mucTieu`
   rồi skill tự đoán, không chắc trúng. Có dòng này thì **CHỈ lấy đúng mục đó** của
   `trangNguon`: từ dòng `## <mucChon>` (khớp nguyên văn) tới heading `##` kế tiếp,
   **bỏ hẳn phần còn lại của trang** — không đọc thêm ngữ cảnh từ mục khác trừ khi
   trang tự dẫn chiếu chéo. Không tìm thấy heading khớp nguyên văn thì **dừng và báo**,
   đừng đoán mục gần giống. `mucChon` thắng nếu nó và `mucTieu` chỉ tới hai hướng khác
   nhau — `mucTieu` lúc đó chỉ còn vai trò chọn *góc nhìn* trong đúng mục đã khoanh.
   Brief không có dòng này → hành vi cũ: đọc cả `trangNguon`, tự rút theo `mucTieu`.

   ⚠️ **Nguồn ngoài wiki đi kèm một ràng buộc.** Nội dung từ Notion hay bài dán **chưa qua `/nap-kho`**, tức chưa có ai soi trùng, chưa đối chiếu giá trị cốt lõi. Dựng mindmap từ nó thì được, nhưng **nói rõ trong `ket-qua.md`** rằng bản đồ này dựng từ nguyên liệu chưa nạp vào bộ não — và nếu nội dung đáng giữ thì **đề xuất nạp qua `/nap-kho`**, đừng tự ghi vào `wiki/`.
2. **Viết `mindmap-nguon.md`** — markdown thuần, phân cấp bằng `#` / `##` / `###` rồi tới gạch đầu dòng. Frontmatter YAML khai màu và độ mở:

```markdown
---
title: <tên gọn>
markmap:
  colorFreezeLevel: 2
  color: ["#dd1717", "#141414", "#b8860b", "#7a1f35", "#2d5016", "#1c3a5e"]
  maxWidth: 320
  initialExpandLevel: <đúng số cấp ô `doSau`; "het" → -1>
  spacingVertical: 10
  spacingHorizontal: 90
---
```

3. **Chốt tên file đầu ra `<ten-file>.html`** — KHÔNG dùng cứng `mindmap.html`. Đoàn chốt
   2026-08-23: *"cái file ở trong kho ko dc đặt tên, nó chỉ là mindmap, như vậy ko tiện
   lắm"* — kéo nhiều file ra khỏi `runs/` (gửi Zalo, để chung một thư mục) thì toàn bộ
   trùng tên `mindmap.html`, không phân biệt được cái nào là cái nào.

   Suy `<ten-file>` từ chính `title` đã viết ở bước 2 — không nghĩ ra tên thứ hai:
   viết thường, bỏ dấu tiếng Việt, thay khoảng trắng/ký tự lạ bằng `-`, cắt còn khoảng
   30–40 ký tự, bỏ gạch nối thừa ở hai đầu. Ví dụ `title: NLP Meta Model & SCORE` →
   `nlp-meta-model-score.html`; `title: 7C Content Formula` → `7c-content-formula.html`.

4. **Sinh file**, từ thư mục run — **hai lệnh, cả hai đều bắt buộc**:

```bash
npx --yes markmap-cli mindmap-nguon.md -o <ten-file>.html --offline --no-open
node ../../va-mindmap.mjs <ten-file>.html
```

5. **Mở `<ten-file>.html` kiểm bằng mắt** trước khi bàn giao. Đếm số nhánh cấp 1 khớp số mục lớn đã định chưa.

### Bốn chốt chặn — đều là lỗi đã mắc thật, đừng gỡ

0. 🚫 **Không bao giờ bỏ lệnh `va-mindmap.mjs`.** markmap gọi `fit()` lúc khởi tạo, **trước khi font đo được kích thước chữ** — nó tính khung bằng 0 rồi để cả cây ở toạ độ **âm**, nằm ngoài khung nhìn. Mở file ra là **trắng trang**, phải tự bấm nút thu-gọn trong toolbar mới thấy. Đo thật 2026-08-07: 9 node, node đầu ở `x=-62 y=-20`. Bạn báo đúng chỗ này: *"trong thư viện mindmap ko hiển thị dc nhỉ"*. Bản vá đợi `document.fonts.ready` rồi mới `fit()`, và fit lại khi đổi kích thước cửa sổ. Chạy lại nhiều lần vô hại — có dấu thì nó bỏ qua.

1. 🚫 **Không bao giờ bỏ cờ `--offline`.** Thiếu nó thì file gọi d3 + markmap-view từ CDN. Member mở lúc không có mạng là **trắng trang** — mà họ sẽ không báo lại, họ chỉ nghĩ tài liệu hỏng.
2. 🚫 **Không thay markmap bằng mermaid `mindmap`.** Mermaid chỉ vẽ được **cây**; nó không vẽ được mũi tên quay ngược (vòng lặp) hay hộp lồng nhau (hai tầng). Và nó không cho chỉnh font/khoảng cách/bo góc — chỉ đổi được `fill`/`stroke` — nên kết quả luôn trông như sơ đồ kỹ thuật. Cần vẽ *vòng lặp* hay *hai tầng* thì làm **thêm** một file mermaid `.md` bên cạnh, không thay thế.
3. 🚫 **Không đặt chữ tiếng Việt vào SVG `<text>`.** Dấu chồng bị vỡ — "NGƯỢC" hiện ra thành "NGƯ Ợ C". Chữ đè lên hình phải là `<div>` HTML định vị tuyệt đối bên trên SVG.

### Luật nội dung

- **Rút gọn tàn nhẫn.** Mindmap là *bản đồ*, không phải bản tóm tắt. Mỗi node tối đa một dòng ngắn. Trang 4.000 từ ra khoảng 8 nhánh lớn là vừa — ra 20 nhánh là chưa rút.
- **Giữ nguyên chữ của bạn ở các node chốt.** Câu cửa miệng (*"Não loạn thì Notion cũng loạn"*) đưa vào nguyên văn, đừng diễn đạt lại cho "gọn hơn".
- **Ô `keoTheo` là ràng buộc cứng** — nhánh bạn ghi ở đó không được lược, kể cả khi thấy nó nhỏ.
- **Áp Hard Don't #2**: lược sạch tên người thật, số doanh thu, thông tin VIP. Bản đồ này gửi ra ngoài.

### Giao gì

Trong `ket-qua.md`, mục `## Mindmap` ghi: đường dẫn `<ten-file>.html`, danh sách nhánh cấp 1, và **những gì đã cố ý lược bỏ kèm lý do**. Nói rõ file mở offline được và gửi Zalo/Messenger được.

Giữ luôn `mindmap-nguon.md` trong thư mục run — lần sau sửa nội dung thì sửa file đó rồi chạy lại **hai lệnh** ở bước 4, không phải dựng lại từ đầu. **Sinh lại là mất bản vá**, nên đừng chỉ chạy lệnh đầu. `mindmap-nguon.md` giữ nguyên tên (nguồn nội bộ, không gửi ra ngoài) — chỉ file `.html` giao ra mới cần tên ngắn gọn.

Không cần dặn bạn tự mở file: thư viện tự mọc nút **🗺️ Mở `<ten-file>.html`** cho mọi run có file xem được (`scan.mjs` → `fileXem`) — nút tự đọc đúng tên file thật, không hardcode.
