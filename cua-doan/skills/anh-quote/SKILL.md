---
name: anh-quote
description: Dùng khi bạn muốn làm ẢNH có chữ để đăng — ảnh quote, ảnh câu nói, ảnh chữ, ảnh bìa bài, ảnh carousel. Đặc biệt khi bạn đưa một ẢNH MẪU (dán link, thả file, chụp màn hình ảnh của người khác) và muốn ra một tấm tương tự nhưng chữ tiếng Việt, màu và font theo nhận diện của mình. Kể cả khi chỉ nói "làm ảnh quote câu này", "dựng ảnh giống ảnh này", "làm cho tôi tấm ảnh chữ", "biến câu này thành ảnh", "làm ảnh đăng Facebook cho bài này", "cắt bài này ra mấy tấm ảnh", hay thả một ảnh vào kèm câu "làm giống cái này".
---

# Ảnh quote — Tô Hải Đoàn

## Skill này chứa gì và KHÔNG chứa gì

Chứa **quy trình dựng ảnh** và **bộ máy render**. Không chứa luật giọng văn, không chứa danh sách từ cấm, không chứa màu/font brand.

Lý do y hệt skill `viet-content`: những thứ đó nằm trong `wiki/` và bạn cập nhật liên tục. Chép vào đây là có hai bản, và bản trong skill sẽ âm thầm lạc hậu.

**Nên: luôn mở file thật ra đọc, đừng viết từ trí nhớ** — kể cả khi thấy mình "đã biết rồi".

| Cần biết | Đọc file |
|---|---|
| Màu brand, font brand, quy trình poster | `wiki/systems-and-stack.md` — mục *Brand & Poster Design Guidelines* |
| Chữ trên ảnh viết thế nào cho đúng giọng | `wiki/voice-profile.md` |
| Câu mở đầu / cách đặt hook | `viet-content/luat/hook.md` |
| Cách xưng hô, khi nào hỏi khi nào tự làm | `wiki/ai-operating-preferences.md` |

Mọi đường dẫn dưới đây tính từ gốc `SecondBrain/`.

## Chỗ để đồ

```
anh-quote/
  mau/     ảnh mẫu bạn đưa vào — BẤT BIẾN, không bao giờ sửa/xoá (như raw/)
  nen/     ảnh nền: ảnh thật của bạn, hoặc nền do AI vẽ
  kieu/    mỗi file .html là MỘT KIỂU đã học được — đây chính là thư viện phong cách
  ra/      kết quả từng lượt: .png + .html + .json
```

Bộ máy nằm trong thư mục skill này: `khung.html` (khung gốc để copy ra kiểu mới), `dung.mjs` (render), `fonts/`.

Bốn font đã nhúng sẵn, tất cả đều **có đủ dấu tiếng Việt** (đã render thử bộ dấu khó nhất `ữ ự ệ ặ ộ ỗ ẫ ỡ ủ ỷ ẳ Ự Ệ Ộ Đ`) và đều giấy phép OFL, kèm file giấy phép:

| Font | Dùng cho |
|---|---|
| Be Vietnam Pro (6 độ đậm) | mặc định — mọi kiểu chữ sans |
| Playpen Sans | chữ viết tay, nét tròn đều |
| Patrick Hand | chữ viết tay, nét mảnh như bút bi |
| Lora + Lora Italic | serif: tiêu đề và chú thích nghiêng |

Nhúng thẳng vào skill nên đổi máy vẫn ra ảnh y hệt — khác với font UTM trên máy bạn, chỉ máy đó mới có.

---

## Bước 1 — Đọc ảnh mẫu thành CÔNG THỨC

Bạn đưa ảnh vào (link hoặc file). Việc đầu tiên: **copy ảnh vào `anh-quote/mau/`** rồi mở ra xem bằng công cụ đọc ảnh. Đừng đoán từ tên file.

Nhìn ảnh và trả lời đủ 8 câu — viết ra thành bảng cho bạn thấy, đừng giữ trong đầu:

| # | Đọc ra cái gì | Ví dụ câu trả lời |
|---|---|---|
| 1 | **Nền** là gì | màu trơn · chuyển màu · giấy có kết cấu · ảnh chụp thật · hoạ tiết vẽ |
| 2 | **Chữ nằm đâu** | giữa khung · dồn xuống đáy · lệch trái, chiếm 2/3 trên |
| 3 | **Chữ to cỡ nào** so với khung | chiếm ~60% chiều cao · chỉ một dòng nhỏ giữa khung trống |
| 4 | **Kiểu chữ** | sans đậm đặc · serif thanh · viết tay · chữ hoa toàn bộ |
| 5 | **Bảng màu** | mấy màu, màu nào làm nền, màu nào làm điểm nhấn |
| 6 | **Có gì ngoài câu quote** | nhãn nhỏ phía trên · tên người nói · logo · handle · số trang |
| 7 | **Điểm nhấn thị giác** | gạch màu · khối màu · dấu ngoặc kép to · đường kẻ · khung viền |
| 8 | **Khoảng thở** | lề rộng hay chật, chữ có bị dồn sát mép không |

⚠️ **Đọc CẤU TRÚC, không sao chép nhận diện.** Đoàn đã chốt: mượn bố cục, thay bằng màu/font của mình. Ảnh ra phải nhìn là biết của bạn, không phải bản photocopy của người ta. Nếu ảnh mẫu dùng màu tím và font serif Ý, mà brand bạn là đỏ/vàng/giấy grid — thì lấy *bố cục* của họ, dùng *màu* của bạn.

## Bước 2 — Phân loại nền, biết cái gì tự làm được cái gì phải xin

Đây là bước hay bị bỏ qua nhất, và bỏ qua là hỏng cả tấm ảnh.

| Nền trong ảnh mẫu | Làm sao | Có phải xin bạn không |
|---|---|---|
| Màu trơn, chuyển màu, giấy kẻ ô, khối hình, đường kẻ, vệt sáng | Dựng thẳng bằng CSS trong file kiểu | Không |
| **Ảnh chụp thật**: người, lớp học, sân khấu, bàn làm việc, sản phẩm | **Phải có ảnh của bạn** | **Có — bắt buộc hỏi** |
| Tranh vẽ / hoạ tiết phức tạp / ảnh nghệ thuật | Viết prompt để bạn cho AI vẽ, rồi thả vào `nen/` | **Có — đưa prompt cho bạn** |

**Tuyệt đối không** thay một tấm ảnh chân dung bằng một khối màu rồi coi như xong. Thà dừng lại hỏi. Kiểu `anh-that-phu-toi.html` đã cài sẵn chốt chặn: thiếu ảnh nền là `dung.mjs` báo lỗi ngay, không lặng lẽ đẻ ra một tấm nền đen.

## Bước 3 — LIỆT KÊ CÁI THIẾU RỒI HỎI (đây là bước bạn yêu cầu rõ nhất)

Trước khi dựng, đưa bạn một danh sách gọn những gì còn thiếu. Hỏi một lượt, đừng hỏi nhỏ giọt từng câu.

Thường thiếu mấy thứ này:

- **Câu chữ**: Bạn muốn ảnh nói câu gì? Nếu bạn chỉ đưa ảnh mẫu mà chưa có câu → hỏi. Nếu bạn đưa một bài dài và bảo "cắt ra ảnh" → tự chọn câu, nhưng trình lại 3 câu ứng viên để bạn chọn.
- **Ảnh nền** (nếu Bước 2 xếp vào nhóm cần ảnh thật): nói rõ cần ảnh *kiểu gì* — "cần một ảnh chân dung anh nhìn nghiêng, nền tối, chừa khoảng trống bên trái để đặt chữ" — chứ đừng chỉ nói "cần ảnh".
- **Tên/handle dưới chân ảnh**: có ghi không, ghi gì.
- **Nhãn nhỏ phía trên**: ảnh mẫu có, mình có làm theo không.
- **Bộ mấy tấm**: một tấm hay một loạt (carousel).

Sau khi hỏi xong và có câu trả lời thì mới dựng. Theo `wiki/ai-operating-preferences.md`, giai đoạn này **luôn hỏi trước khi làm**, cho tới khi bạn duyệt quy trình là ổn.

## Bước 4 — Viết chữ tiếng Việt

Đọc `wiki/voice-profile.md` trước khi đặt bút. Chữ trên ảnh cũng là content — luật giọng văn áp y như bài viết.

Riêng chữ trên ảnh có thêm mấy ràng buộc vật lý:

- **Ngắn.** Kiểu nền tối chữ lớn sống được tới ~25 chữ. Dài hơn thì chữ tự co lại và mất hết sức nặng — lúc đó chọn kiểu giấy grid, hoặc cắt câu.
- **Một ý một tấm.** Hai ý thì làm hai tấm.
- **Bọc `*dấu sao*` quanh cụm cần tô màu nhấn** — thường là vế lật, vế chốt. Đừng tô quá một cụm mỗi tấm, tô hết thì không còn gì là nhấn.
- **Không bịa.** Luật chống bịa số/chuyện trong `ai-operating-preferences.md` áp cho ảnh y như cho bài viết — mà ảnh còn nguy hơn vì nó bị chụp lại và lan đi.

## Bước 5 — Chọn kiểu rồi dựng

Xem `anh-quote/kieu/` có kiểu nào khớp công thức Bước 1 chưa. Có thì dùng lại (đó là lý do có thư viện). Chưa có thì **copy `khung.html` ra một file kiểu mới** rồi sửa.

Năm kiểu đang có. Ba kiểu đầu học thẳng từ mẫu bạn đưa 2026-08-08 — **đó là ba kiểu chính bạn muốn làm**:

| File | Nền | Hợp với |
|---|---|---|
| ⭐ `giay-viet-tay.html` | giấy kem có hạt + đốm | **chữ trên nền màu** — cấu trúc lặp mấy dòng cùng khuôn |
| ⭐ `anh-ca-nhan-chu-den.html` | **ảnh của bạn**, chữ đen đặt vào mảng sáng, không phủ | **chữ trên ảnh cá nhân** — ảnh phải có mảng trống sáng |
| ⭐ `so-do-vang-chanh.html` | xám nhạt + pill vàng chanh | **biểu đồ** — quy trình, phễu, mô hình mấy bước |
| `giay-grid-brand.html` | giấy kẻ ô + mảng vàng nghiêng góc trên | quote tuyên ngôn, bài học, câu chốt |
| `nen-toi-chu-lon.html` | gần đen + vệt sáng vàng | câu ngắn, đánh thẳng, quan điểm trái chiều |
| `anh-that-phu-toi.html` | ảnh của bạn + phủ tối dâng từ đáy | ảnh rối, không có mảng trống — chữ trắng nổi trên lớp phủ |

⚠️ Hai kiểu ảnh **khác nhau về chất**, đừng lẫn: `anh-ca-nhan-chu-den` để chữ trông như *vốn có* trên mặt bàn/mảng tường (đẹp hơn, nhưng kén ảnh); `anh-that-phu-toi` phủ tối cả khung (chạy được với mọi ảnh, nhưng nhìn ra ngay là chữ dán lên). Ảnh nào cũng dùng được thì chọn kiểu đầu.

Viết file nội dung JSON:

```json
{
  "nhan": "SỰ THẬT",
  "chinh": "Đừng cố nghĩ hộ khách hàng. *Để họ tự nói ra điều họ sợ.*",
  "ghiChu": "— Tô Hải Đoàn",
  "chan": "@tohaidoan",
  "canChu": "trai",
  "coChuToiDa": 108,
  "anhNen": "nen/ten-file.jpg"
}
```

- Phần nào không dùng thì để `""` — nó tự ẩn, không để lại khoảng trống.
- `anhNen` viết **tương đối với thư mục `anh-quote/`** (vd `nen/abc.jpg`).
- `coChuToiDa` là trần trên; chữ tự co xuống cho vừa khung, không bao giờ tràn.
- Riêng `anh-ca-nhan-chu-den` có thêm `viTri` (`duoi-trai` · `duoi-giua` · `tren-trai` · `giua`) và `tamNen` (`khong` · `mo` · `trang`). Mặc định `khong` — chỉ bật tấm nền khi ảnh không có mảng trống nào, vì bật lên là mất đúng cái duyên của kiểu này.

**Kiểu sơ đồ dùng JSON khác hẳn** — nội dung của nó là một chuỗi bước, không phải một câu:

```json
{
  "nhan": "Phần 2",
  "tieuDe": "Dùng kể chuyện làm cỗ máy tăng trưởng",
  "phuDe": "Dòng một.\nDòng hai.",
  "cacBuoc": [
    { "ten": "chú ý", "chuThich": "Sự chú ý khiến người ta dừng lướt", "phia": "tren" },
    { "ten": "tin cậy", "chuThich": "Tin cậy khiến họ chịu nghe", "phia": "duoi" }
  ]
}
```

`phia` xen kẽ `tren`/`duoi` cho cân. Đẹp nhất ở 3–5 bước; quá 5 thì tách hai tấm.

Rồi render:

```bash
node .claude/skills/anh-quote/dung.mjs --kieu anh-quote/kieu/giay-grid-brand.html --noi-dung anh-quote/ra/<lượt>/noi-dung.json --ra anh-quote/ra/<lượt>/anh.png
```

Khổ mặc định 1080×1350 (4:5), xuất @2x. Khổ khác thì thêm `--kho 1080x1080` hoặc `--kho 1080x1920`.

## Bước 6 — TỰ NHÌN ẢNH TRƯỚC KHI ĐƯA ĐOÀN

**Bắt buộc mở file PNG ra xem bằng công cụ đọc ảnh.** Render chạy xong không có nghĩa là ảnh đẹp — đã có lần lệnh báo thành công, ảnh ra đủ dung lượng, mà mảng vàng và lưới giấy trong thiết kế **không hề xuất hiện** (xem *Bẫy đã gặp thật* §2).

Nhìn và kiểm:

- Chữ có bị tràn, bị cắt, bị dính mép không
- Cụm nhấn có đúng cụm mình muốn không
- Chi tiết trang trí mình viết trong CSS có **thật sự hiện ra** không
- Trên nền ảnh thật: chữ có đủ tương phản để đọc không

Nghi ngờ chỗ nào thì đo bằng pixel, đừng đoán:

```bash
python3 -c "from PIL import Image; im=Image.open('anh-quote/ra/x/anh.png').convert('RGB'); print(im.size, im.getpixel((40, 900)))"
```

Theo luật bằng chứng trong `ai-operating-preferences.md`: **cấm nói "xong" khi chưa trình bằng chứng** — với skill này bằng chứng là chính tấm ảnh đã mở ra xem.

## Bước 7 — Lưu lại phong cách + ghi log

Bạn duyệt rồi thì:

1. **Kiểu mới thì giữ lại** trong `anh-quote/kieu/`, đặt tên gợi hình (`bao-chi-den-trang.html`, chứ không phải `kieu-3.html`). Đầu file ghi comment: học từ ảnh mẫu nào, hợp với loại quote gì, **không** hợp với gì.
2. **Append `log.md`** một dòng — không rewrite (luật sắt #4).
3. **KHÔNG tự ghi vào `wiki/`.** Đoàn chốt 2026-07-30: chỉ còn một đường ghi vào `wiki/` là skill `/nap-kho`. Nếu trong lúc làm ảnh phát hiện một insight đáng vào bộ não (một cách nói hay, một phản ứng của khán giả), thì **đề xuất** bạn chạy `/nap-kho`, đừng tự tay sửa `wiki/`.

---

## Bẫy đã gặp thật — đọc trước khi sửa bộ máy

**1. Cờ `--screenshot` của Chrome làm treo tiến trình.** Chụp xong ảnh nhưng không thoát; đo được: bị giết ở giây 25, mã thoát 142, ảnh vẫn ra. Vì vậy `dung.mjs` điều khiển Chrome qua giao thức DevTools. Đừng "đơn giản hoá" ngược lại.

**2. Trong file kiểu, khối CSS riêng của kiểu phải nằm CUỐI khối `<style>`.** Ban đầu nó nằm trên, và bộ máy chung bên dưới ghi đè ngược lại — lưới giấy biến mất, mảng vàng biến mất, `justify-content: flex-end` của kiểu ảnh thật bị vô hiệu hoàn toàn. Nhìn ảnh thì chỉ thấy "nền hơi trơn", không thấy báo lỗi gì.

**3. Lớp trang trí phải đặt ở `.phu`, không đặt ở `.khung::before`.** `::before` là con đầu tiên, `.nen` là thẻ đứng sau và cũng `position:absolute` — nên `.nen` đè chết trang trí.

**4. Màu quá nhạt = tàng hình ở khổ lớn.** Vạch lưới `alpha .07` đo được 0 vạch trên ảnh 2160px. Phải lên `.12` mới hiện. Đừng tin con số nghe có vẻ "tinh tế" — chụp rồi đếm pixel.

**5. Trong flex, phần chữ bị nén làm hàm co chữ tính sai.** Ở `so-do-vang-chanh`, tiêu đề nằm trong flex column nên bị co lại; hàm co chữ tưởng chữ tràn nên hạ cỡ xuống — tiêu đề ra **nhỏ hơn cả phụ đề**, ngược hẳn ý đồ. Sửa bằng `flex: 0 0 auto` cho phần đầu. Kèm theo: **đo tiêu đề bằng SỐ DÒNG**, đừng so `scrollHeight` với `clientHeight` — với div tự do hai giá trị đó luôn bằng nhau nên phép so vô nghĩa.

**6. Font viết tay trên máy bạn không dùng được cho kiểu giấy.** Đã render thử cả 5 font UTM có chữ "hand/script/brush" trong tên: toàn chữ ký hoa mỹ hoặc brush lem, không phải nét viết tay đều. Kiểu `giay-viet-tay` dùng **Playpen Sans** (đã nhúng). Patrick Hand cũng nhúng sẵn, mảnh hơn, giống bút bi — đổi bằng một dòng `--font-chinh`.

**7. Poppins không dùng cho tiếng Việt.** Brand Guide ghi Poppins là font chính, nhưng chính guide cũng ghi nó vẽ sai dấu nặng/dấu hỏi khi viết hoa. Ảnh quote toàn tiếng Việt → dùng **Be Vietnam Pro** (đã nhúng sẵn trong `fonts/`, không phụ thuộc font cài trên máy). Font UTM trên máy bạn chỉ dùng làm font nhấn, và phải nhớ nó chỉ có trên máy bạn.

**8. Đường dẫn `anhNen` viết tương đối với `anh-quote/`.** `dung.mjs` có tìm ở vài gốc khác nhau và báo rõ đã tìm ở đâu, nhưng viết đúng ngay từ đầu vẫn nhanh hơn.

## Links
`wiki/systems-and-stack.md` · `wiki/voice-profile.md` · `wiki/ai-operating-preferences.md` · `viet-content/luat/hook.md` · skill `viet-content` (viết chữ) · skill `nap-kho` (đường duy nhất ghi vào `wiki/`)
