---
name: xuong-video
description: Lập kho cho chính footage bạn đã quay rồi tìm lại khi cần — quét thư mục footage, làm bản xem nhanh nhẹ, máy tự chấm đoạn nào nét và không rung, tìm cảnh cũ theo chữ, giờ quay, độ sáng, kiểu máy quay, rồi xuất thư mục đánh số kéo thẳng vào CapCut. Dùng khi bạn vừa đổ thẻ nhớ, khi cần cảnh minh hoạ (B-roll) cho video mới và muốn biết kho có sẵn chưa, hoặc khi nói "nhập footage mới", "có cảnh bình minh nào không", "tìm cảnh đọc sách", "lấy cảnh cũ dùng lại", "tra kho video", "xuất cho CapCut", hoặc gõ /xuong-video. Không viết kịch bản, không cắt dựng video, không tự chỉnh màu.
---

# Xưởng video — kho footage của bạn, tìm được và dùng lại được

> Skill này **không làm video**. Nó giữ footage bạn đã quay sao cho tìm lại được, và đưa đúng đoạn cần dùng vào CapCut.

Đi kèm là một bộ máy **trống**: chưa có cảnh nào, chưa có nhãn nào. Kho được lập từ chính footage của bạn.

## Ba việc skill làm

| Việc | Khi nào | Ra cái gì |
|---|---|---|
| **Nhập kho** | Sau mỗi lần đổ thẻ nhớ | Danh mục mọi clip, bản xem nhanh, các đoạn máy chấm là dùng được |
| **Tra kho** | Khi kịch bản cần cảnh minh hoạ — B-roll, tức cảnh chèn vào lúc bạn đang nói, ví dụ tay rót cà phê, phố buổi sáng | Danh sách đoạn khớp + một video xem thử ghép sẵn |
| **Xuất CapCut** | Khi đã chọn xong | Một thư mục, các đoạn đánh số 01, 02, 03… kéo thẳng vào CapCut |

Mỗi buổi quay nhập kho xong là thành cảnh minh hoạ cho video sau. Quay càng nhiều, phần phải đi quay mới càng ít.

## Nguyên tắc: chỉ ĐỌC footage gốc

Skill không đổi tên, không di chuyển, không xoá file nào trong thư mục footage. Mọi thứ nó tạo ra (danh mục, bản xem nhanh, đoạn xuất) nằm trong một **thư mục làm việc** riêng. Sửa ngày giờ quay cũng chỉ sửa trong danh mục, có lệnh trả lại như cũ.

## Cần có trên máy

- **Python 3** — kiểm: `python3 --version` (Windows: `python --version`).
- **FFmpeg** — phần mềm miễn phí xử lý video. Kiểm: `ffmpeg -version`. Chưa có thì cài: Mac `brew install ffmpeg` (cần Homebrew — trình cài phần mềm cho Mac, hướng dẫn ở brew.sh), Windows `winget install Gyan.FFmpeg`.

Mọi lệnh dưới đây chạy trong thư mục `bo-may/` nằm cạnh file này. Trên Windows gõ `python` thay cho `python3`.

---

## Lần đầu dùng

**Bước 1 — Khai thư mục footage.** Là thư mục chứa video bạn quay, ví dụ `~/Movies/Footage` hay cả ổ cứng ngoài `/Volumes/O-Video`. Nên để mỗi buổi quay một thư mục con bên trong.

```bash
python3 cfg.py --khai "/đường/dẫn/tới/thư mục footage"
```

Lệnh này ghi file cấu hình `~/.creator-video/kho.json`:

| Trường | Là gì |
|---|---|
| `o_goc` | Thư mục footage. Skill chỉ đọc ở đây |
| `work_root` | Thư mục làm việc. Mặc định `~/CreatorVideo/kho`. Muốn đặt chỗ khác thì thêm `--lam "/đường/dẫn"` |

Bản xem nhanh tốn khoảng **1,4 GB cho mỗi giờ video** — đặt thư mục làm việc ở ổ còn trống.

Lệnh tự từ chối nếu thư mục làm việc nằm **bên trong** thư mục footage (lần quét sau sẽ quét nhầm bản xem nhanh như footage thật), hoặc nằm trong một thư mục dự án có git (công cụ quản lý mã nguồn — dữ liệu hàng chục GB lọt vào đó sẽ bị đẩy lên cùng code).

**Bước 2 — Kiểm máy.**

```bash
python3 cfg.py
```

| Dòng báo | Làm gì |
|---|---|
| `Thu muc footage: (chua khai)` | Làm lại bước 1 |
| `Thu muc footage: ... (KHONG THAY)` | Ổ chưa cắm, hoặc đổi tên, đổi chữ cái ổ. Tra kho và xuất từ bản xem nhanh vẫn chạy được; nhập kho và xuất bản gốc thì không |
| `FFmpeg: KHONG CO` | Cài FFmpeg |
| `!! THU MUC LAM VIEC NAM ...` | **Dừng.** Khai lại với `--lam` chỗ khác |

**Bước 3 — Nhập kho lần đầu** theo mục *Nhập kho* ngay dưới. Kho nhỏ thì quét cả thư mục footage một lần; kho lớn thì làm bản xem nhanh từng thư mục một.

---

## Nhập kho — sau mỗi lần đổ thẻ nhớ

Chép footage vào **một thư mục riêng cho buổi quay**, nằm bên trong thư mục footage (ví dụ `2025-08-25 Đà Lạt`). Đặt ngày vào tên thư mục thì máy còn cứu được ngày quay khi đồng hồ máy quay bị sai. Rồi chạy đúng thứ tự:

```bash
python3 catalog.py scan "/đường/dẫn/thư mục footage/2025-08-25 Đà Lạt"
python3 sua_gio.py                                       # xem trước; hợp lý thì chạy lại với --apply
python3 proxy.py --thu-muc "2025-08-25 Đà Lạt"           # xem trước: bao nhiêu clip, ước bao lâu
python3 proxy.py --run --thu-muc "2025-08-25 Đà Lạt"
python3 analyze.py --thu-muc "2025-08-25 Đà Lạt"
python3 chon_canh.py
```

`--thu-muc` nhận đường dẫn **tính từ thư mục footage**, không có phần đầu.

| Bước | Làm gì | Ghi chú |
|---|---|---|
| `catalog.py scan` | Lập danh mục, đọc ngày giờ quay, độ dài, khung hình | Quét lại bao nhiêu lần cũng được — file đã có thì bỏ qua. Thư mục nằm ngoài thư mục footage thì tự từ chối |
| `sua_gio.py` | Sửa ngày quay khi đồng hồ máy quay bị reset (hết pin → về năm 2000) | Lấy ngày từ tên thư mục; không có thì lấy theo các clip khác cùng thư mục. Báo `0 file` là tốt. Có `--revert` để trả lại |
| `proxy.py` | Làm bản xem nhanh 720p — để tra và xuất nhanh mà không phải đọc file gốc nặng | **Chậm nhất chuỗi**, chiếm máy lâu. Báo người dùng con số ước tính và **chờ họ đồng ý** rồi mới thêm `--run`. Dừng giữa chừng, chạy lại sẽ làm tiếp |
| `analyze.py` | Đo độ nét, độ sáng từng giây | |
| `chon_canh.py` | Chấm điểm, cắt thành đoạn 3–8 giây dùng được | **Luôn chấm lại cả kho**, không chấm riêng buổi mới: ngưỡng tính so với toàn kho. Kho mới chỉ vài clip thì có thể ra rất ít đoạn — bình thường. Thêm `--reel 40` để dựng video xem thử 40 đoạn đẹp nhất |

Xem tổng quan kho: `python3 catalog.py report`. Chia kho thành các buổi quay theo thời gian: `python3 catalog.py events`.

---

## Gắn nhãn nội dung — để kho biết trong cảnh có gì (không bắt buộc)

Chưa gắn nhãn thì kho chỉ tìm được theo **tên thư mục, tên file**, giờ quay, độ sáng, kiểu máy quay. Gắn nhãn rồi thì tìm được *"đọc sách bên cửa sổ"*, *"rót cà phê"*.

Kho mới **không có nhãn nào**. Hai cách gắn:

**Cách 1 — Nhờ AI xem ảnh rồi gắn.**

```bash
python3 nap_nhan.py --anh --so 12                                   # 12 clip chưa có nhãn
python3 nap_nhan.py --anh --so 12 --thu-muc "2025-08-25 Đà Lạt"     # chỉ một buổi quay
```

Mỗi clip ra một ảnh ghép 6 khung hình trải đều từ đầu tới cuối, kèm file `can-gan-nhan.json` để điền, nằm trong `gan-nhan/lo-<ngày giờ>/` của thư mục làm việc. AI mở từng ảnh `NN.jpg`, điền vào mục có `"anh": "NN.jpg"`, rồi nạp:

```bash
python3 nap_nhan.py "<đường dẫn>/can-gan-nhan.json"
```

**Cách 2 — Tự viết.** Cùng định dạng, mỗi clip một mục:

```json
[
  {
    "path": "2025-08-25 Đà Lạt/C0012.MP4",
    "trong_ngoai": "ngoài trời",
    "boi_canh": "đồi thông, sương sớm",
    "chu_the": "một người mặc áo khoác nâu",
    "hanh_dong": "đi bộ trên đường mòn",
    "loai_shot": "toàn cảnh, máy đứng yên",
    "gio_quay": "sáng sớm",
    "dung_cho": "mở đầu video về nhịp sống chậm",
    "tu_khoa": "thông, sương, đi bộ",
    "ghi_chu": ""
  }
]
```

| Ô | Điền gì |
|---|---|
| `path` | Đường dẫn clip tính từ thư mục footage. Không có thì dùng `"file": "C0012.MP4"`, nhưng chỉ được khi tên đó **không trùng** clip nào khác — máy quay hay đặt trùng tên ở các buổi khác nhau |
| `hanh_dong` | Đang làm gì. Cảnh **ngồi nói trước máy** thì ghi đúng cụm *"nói trước máy"* để lệnh lọc `--bo-noi` bắt được |
| `dung_cho` | Cảnh này hợp minh hoạ cho ý gì |
| các ô còn lại | Không biết thì để trống — ô trống không ghi đè gì |

Nạp xong máy báo: vào bao nhiêu, ghi bao nhiêu, bỏ cái nào và vì sao. Trước lần nạp đầu tiên trong ngày, danh mục được tự sao lưu. Xem đã gắn được bao nhiêu: `python3 nap_nhan.py --xem`.

**Giới hạn khi tìm:** nhãn gắn theo **cả clip**, không theo từng giây. Clip ghi *"lật trang sách"* không có nghĩa giây nào cũng lật trang. Clip đã có nhãn mà chưa có đoạn chấm điểm vẫn được trả về nguyên clip (cột Điểm ghi `chua`), xếp sau các đoạn đã chấm.

---

## Tra kho — tìm cảnh có sẵn cho video mới

Khi kịch bản đã có danh sách cảnh cần quay (shotlist), tra từng cảnh minh hoạ xem kho có sẵn chưa.

| Cách lọc | Gõ | Giá trị |
|---|---|---|
| Chữ trong nhãn + tên thư mục + tên file | `"doc sach"` | Không cần gõ dấu. Khớp theo đầu từ: `an` không khớp `ban` |
| Bỏ clip có cụm chữ | `--bo "khach san"` | Lặp lại được |
| Bỏ mọi cảnh ngồi nói trước máy | `--bo-noi` | **Luôn bật khi tìm cảnh minh hoạ** |
| Lúc nào trong ngày | `--luc` | `binh-minh` `sang` `trua` `chieu` `hoang-hon` `toi` |
| Máy quay chuyển động thế nào | `--dong` | `tinh` (đứng yên) `lia-cham` `vua` `manh` |
| Độ sáng | `--sang` | `toi` `vua` `sang` |
| Khoảng ngày | `--tu` `--den` | `2025-08-01` |

Chưa biết kho có gì: `python3 tim.py --bo-loc`.

Cho từng cảnh cần tìm:

1. **Đổi mô tả cảnh thành bộ lọc.** *"Cảnh đọc sách, không phải cảnh ngồi nói"* → `"doc sach" --bo-noi`. *"Ngồi thiền lúc trời chưa sáng, máy đứng yên"* → `"ngoi thien" --luc binh-minh --dong tinh`. Đọc dòng nhãn dưới mỗi kết quả trước khi chọn.
2. **Tra, lưu thành tuyển chọn, dựng video xem thử:**
   ```bash
   python3 tim.py "ngoi thien" --luc binh-minh --dong tinh --top 8 --luu "2025-09-13-day-som-c03" --xem
   ```
   Đặt tên tuyển chọn theo khuôn `<ngày>-<tên video>-c<số cảnh>` để nhìn tên là biết của video nào, cảnh nào.
3. **Gửi người dùng video xem thử** (`tuyen-chon/tim-*.mp4` trong thư mục làm việc). Chưa xem thì chưa kết luận.
4. **Báo lại theo bảng:**

   | Cảnh # | Có sẵn? | Tuyển chọn đã lưu | Số đoạn | Ghi chú |
   |---|---|---|---|---|
   | 3 | một phần | 2025-09-13-day-som-c03 | 8 | Chưa xem. Toàn cảnh rộng, không có cận tay |
   | 5 | không | — | 0 | Kho không có đoạn nào lúc hoàng hôn |

   - Chỉ ghi `có` sau khi **người dùng đã xem và đồng ý**. Máy tìm ra đoạn khớp bộ lọc thì ghi `một phần`.
   - Tra ra 0 đoạn thì ghi `không` — **đó là câu trả lời đúng**. Đừng nới dần bộ lọc cho tới khi ra cái gì đó: vơ đại đoạn gần giống thì người dùng không bao giờ biết lần nào là thật.

Xem các tuyển chọn đã lưu: `python3 tim.py --cac-tuyen`.

---

## Xuất sang CapCut

```bash
python3 xuat.py --tuyen "2025-09-13-day-som-c03"
python3 xuat.py --tuyen "2025-09-13-day-som-c03" --goc     # bản gốc nét nhất — ổ footage phải đang cắm
```

Ra thư mục `xuat/<tên tuyển chọn>/` trong thư mục làm việc: các đoạn đánh số `01_`, `02_`… (CapCut nhập đúng thứ tự), kèm `ghi-chu.txt` (đoạn cắt từ giây nào của clip gốc nào) và `DOC-TRUOC.txt` (cách kéo vào CapCut).

| Mặc định | Vì sao |
|---|---|
| **Giữ nguyên màu** | Xem luật số 1 bên dưới. Người dùng tự thêm bộ màu (LUT) trong CapCut |
| Lấy từ bản xem nhanh 720p | Dựng thử là đủ. Bản đăng thật thì thêm `--goc` |
| **Giữ nguyên khung hình** | Chưa tự cắt dọc 9:16. Footage quay ngang mà video đăng dọc thì báo trước: người dùng phải tự cắt trong CapCut |

`xuat.py` in `Xong N/M doan`. **N nhỏ hơn M thì đọc các dòng `BO QUA`** trước khi báo xong — thường là thiếu bản xem nhanh.

Chỉ khi người dùng **yêu cầu** mới áp LUT lúc xuất: `--lut "<file .cube>"` cho tất cả, hoặc `--lut-sony` / `--lut-dji` riêng từng hãng (đoán hãng theo tên file). `--tam` nâng màu tạm để xem trước, không thay được LUT thật.

### Đo màu — đoán clip nào quay log (không bắt buộc)

Quay log là chế độ quay cho hình nhạt màu, xám xám để chỉnh màu sau. Clip log cần thêm LUT, clip có màu sẵn thì không.

```bash
python3 do_mau.py        # đo, in bảng từ phẳng nhất tới tương phản nhất
python3 bang_anh.py      # dựng trang ảnh nhỏ xếp theo độ phẳng, để mắt người phân định
```

Đo xong, `ghi-chu.txt` lúc xuất có thêm dòng `mau: KHA PHANG` cho đoạn nghi quay log. **Gợi ý, không phải kết luận.**

---

## Luật — đã sai rồi mới có

**1. Không tự áp LUT.** Đo tự động hay sai: cùng một máy, quay thường có thể ra log mà quay tua nhanh (timelapse) lại ra màu sẵn — chế độ đổi theo từng file, không theo thư mục hay theo máy. Cảnh trong nhà, trời mù vốn ít tương phản nên đo ra "phẳng" dù không quay log. Áp LUT nhầm vào clip đã có màu là hỏng không cứu được; bỏ sót clip log thì chỉnh tay được. Nên mặc định giữ nguyên màu.

**2. Ngày giờ quay — tin nguồn nào trước:**

| Nguồn | Tin được không |
|---|---|
| Tên file máy DJI (`DJI_YYYYMMDDHHMMSS…`) | ✅ Nhất — máy ghi giờ địa phương. **Trừ năm 2000**: máy hết pin thì chính tên file cũng sai |
| Giờ ghi bên trong file video | ✅ Nhưng là giờ quốc tế (UTC), phải đổi sang giờ nơi quay. Skill tự đổi theo múi giờ đang cài trên máy tính. Quay ở múi giờ khác thì thêm `"mui_gio": <số giờ>` vào file cấu hình |
| Spotlight (tính năng tìm kiếm của Mac) | ⚠️ Khi chưa đọc được thông tin trong file, nó trả **ngày chép file vào ổ** mà trông y như ngày quay. Máy đã tự loại trường hợp này |
| Ngày sửa file | ❌ Chép file là đổi. Chỉ dùng khi không còn nguồn nào |

Kiểm ngày giờ đúng sai **không cần mở video**: so giờ quay với độ sáng đo được. Trưa phải sáng nhất, hoàng hôn tối dần. Đường cong không theo mặt trời là giờ sai.

**3. Kho lưu đường dẫn tính từ thư mục footage.** Đổi ổ, đổi chữ cái ổ, chuyển sang máy khác thì chỉ cần khai lại thư mục footage, kho vẫn dùng được. Khi sửa code, luôn lấy đường dẫn qua `cfg.src()` / `cfg.prox()` — hai hàm này xử lý được cả hai kiểu lưu dấu tiếng Việt khác nhau giữa Mac và Windows. Đừng tự ghép đường dẫn.

**4. Điểm chấm là thứ tự, không phải phán xét.** Máy đo nét, không rung, đủ sáng. Nó không biết cảnh có ý nghĩa hay không.

---

## Dùng trên máy khác

Mỗi máy một file cấu hình riêng (`~/.creator-video/kho.json`), vì ổ footage trên mỗi máy có đường dẫn khác nhau. Muốn dùng kho cũ trên máy mới: cài Python và FFmpeg, chép nguyên thư mục làm việc sang, rồi khai:

```bash
python3 cfg.py --khai "<thư mục footage trên máy này>" --lam "<thư mục làm việc vừa chép>"
```

Máy không có Spotlight (Windows) thì ngày giờ video đọc qua FFmpeg; ảnh chỉ còn tên file và ngày sửa file — nhập ảnh thì nên nhập trên Mac.

## Skill này KHÔNG làm

- Không viết kịch bản hay danh sách cảnh cần quay.
- Không cắt dựng video.
- Không đổi tên, di chuyển, xoá file gốc.
- Không chạy `proxy.py --run` khi người dùng chưa đồng ý — chạy hàng giờ và chiếm máy.
- Không tự cắt dọc 9:16, không tự áp LUT.

---

Tác giả: Tô Hải Đoàn, giấy phép MIT
