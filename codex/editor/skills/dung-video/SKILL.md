---
name: dung-video
description: Dựng video bạn ngồi nói trước ống kính thành video dọc 9:16 kiểu chuyên gia — máy tự nghe lời bạn nói, cắt chỗ ngập ngừng và câu nói lại, chạy phụ đề hai tầng kiểu gõ chữ, chèn thẻ chữ toàn màn hình, thẻ danh sách, ảnh bằng chứng bo góc và cảnh minh hoạ (B-roll) do bạn đưa vào, thêm chuyển cảnh, rồi ra file MP4 hoàn chỉnh kèm các lớp rời và một dự án CapCut dựng sẵn để bạn sửa tay. Dùng khi bạn đưa clip tự quay và nói "dựng video này", "edit video này", "cắt video này", "làm phụ đề chạy cho video này", "làm kiểu chuyên gia ngồi nói", "thêm B-roll vào", "thêm chuyển cảnh", "xuất sang CapCut", "ra bản dọc đăng Reels/TikTok", hoặc gõ $dung-video. Chạy trên Mac chip Apple (M1 trở lên). Không dùng để viết kịch bản hay làm ảnh.
---

# Dựng video — người ngồi nói trước ống kính

Đưa vào một hay vài clip bạn tự quay (nói thẳng vào máy), ra một video dọc 9:16 sẵn đăng Reels/TikTok/Shorts. Cả skill xoay quanh một ý: **mắt người xem không bao giờ phải nhìn một khung hình đứng yên quá vài giây, trong khi lời nói vẫn liền mạch.**

Máy lo phần đo đếm (nghe, cắt khoảng lặng, căn giờ, vẽ chữ, ghép). AI lo phần biên tập (bỏ câu nào, nhấn chữ nào, chèn gì ở đâu) theo luật bên dưới — và **luôn trình bảng dựng cho người dùng duyệt trước khi dựng**.

## Các lớp hiệu ứng

| Lớp | Là gì | Nằm ở đâu trong `bang-dung.json` |
|---|---|---|
| **Cắt nhảy** | Cắt mọi khoảng ngập ngừng, câu nói lại. Đoạn nói dài thì đổi khung (phóng vào/thu ra) để hình không đứng yên | `bo`, `lang_toi_da`, `zoom`, `doi_khung_moi` |
| **Phụ đề hai tầng** | 2–5 chữ một lần, ngay dưới cằm. Dòng nhỏ gõ từng chữ có con trỏ; cụm nhấn to, đậm, nghiêng, hiện mờ rồi rõ | file `phu-de.txt` |
| **Thẻ chữ** | Nền đen hoặc trắng ngà toàn màn hình, đầu mục to, chữ nhỏ hiện từng từ theo lời | `chen` loại `the` |
| **Thẻ danh sách** | Tiêu đề + các dòng gõ ra lần lượt | `chen` loại `danh_sach` |
| **Ảnh bằng chứng** | 1–3 ảnh chụp màn hình bo góc, hơi nghiêng, hiện lần lượt, phụ đề nhảy lên trên | `chen` loại `anh` |
| **Cảnh minh hoạ (B-roll)** | Clip người dùng tự đặt vào thư mục `broll/` của dự án, phụ đề vẫn chạy trên | `chen` loại `broll` |
| **Chuyển cảnh** | Mỗi cảnh chèn vào/ra bằng một kiểu: cắt · mờ · trượt · phóng · lắc (trượt nhanh + nhoè) · nhoè | `chuyen_canh`, `vao`/`ra` trong từng cảnh |
| **Màu** *(tuỳ chọn)* | Áp file chỉnh màu `.cube` (LUT) của chính người dùng, nếu họ có | `lut` |

Công thức chi tiết của phong cách nằm ở [phong-cach/chuyen-gia-ngoi-noi.md](phong-cach/chuyen-gia-ngoi-noi.md) — **đọc file đó trước Bước 4**.

Chữ dùng font **Be Vietnam Pro** (kèm sẵn trong `fonts/`, giấy phép OFL). Phụ đề chỉ màu trắng; riêng phụ đề nằm trên thẻ ảnh nền trắng ngà thì tự đổi sang chữ tối.

## Cần gì trên máy

| | |
|---|---|
| Máy | Mac chip Apple (M1 trở lên). Bộ nghe chạy ngay trên máy, tiếng nói **không gửi đi đâu** |
| Bắt buộc | Python 3.9+, ffmpeg (công cụ xử lý video; cài bằng `brew install ffmpeg` là đủ phần vẽ chữ), và `pip3 install mlx-whisper pillow numpy` |
| Lần nghe đầu tiên | Máy tự tải mô hình nghe whisper-large-v3-turbo (khoảng 1,6 GB) từ Hugging Face, chỉ một lần |
| Tuỳ chọn — chữ đẹp hơn | **HyperFrames** (công cụ vẽ chữ bằng trình duyệt, ~130 MB, cần Node.js): `python3 dv.py cai-hf`. Không cài thì máy vẽ chữ bằng ffmpeg — nhanh hơn, kém mượt hơn |
| Tuỳ chọn — nghe lần hai | **PhoWhisper** (bộ nghe luyện riêng cho tiếng Việt): `python3 dv.py cai-pho`. Tải 6,2 GB, chuyển xong còn 2,9 GB; cần thêm `pip3 install torch huggingface_hub` |
| Xuất sang CapCut | CapCut cho Mac, bản 9.x |

## Chỗ để đồ

| Ở đâu | Là gì |
|---|---|
| `bo-may/` cạnh file này | Code (Python). `dv.py` là cửa vào duy nhất |
| `fonts/`, `phong-cach/` cạnh file này | Font kèm sẵn, công thức phong cách |
| `~/CreatorVideo/dung/<tên>/` | **Dữ liệu một video**: `bang-dung.json`, `loi.txt`, `phu-de.txt`, `anh/`, `broll/`, bản nháp, bản cuối, `lop/` |
| `~/CreatorVideo/.hyperframes/`, `~/CreatorVideo/.models/` | Công cụ tuỳ chọn đã cài (dùng chung mọi dự án) |
| `~/Movies/CreatorVideo/<tên>/` | Media gom cho dự án CapCut |
| `~/.creator-video/ho-so.json` | *(tuỳ chọn)* `{"ten_kenh": "Tên kênh của bạn"}` — được thêm vào gợi ý cho bộ nghe để nghe đúng tên riêng |

Muốn để dữ liệu chỗ khác (ví dụ ổ ngoài) thì đặt biến môi trường `CREATOR_VIDEO_HOME`, ví dụ `export CREATOR_VIDEO_HOME=/Volumes/O-Ngoai/CreatorVideo`. Máy **tự dừng** nếu thư mục dữ liệu nằm trong một repo git — video nặng lọt vào repo là rất khó gỡ.

---

## Quy trình

Mọi lệnh chạy trong thư mục `bo-may/` cạnh file này.

### Bước 0 — Kiểm máy

```bash
python3 dv.py kiem
```
Phải ra `San sang.` Thiếu gì thì dòng đó ghi `THIEU` kèm lệnh cài. Hai công cụ tuỳ chọn (HyperFrames, PhoWhisper) ở bảng trên — hỏi người dùng trước khi cài vì chúng tải nhiều dung lượng.

⛔ **Không chạy `hyperframes init`.** Lệnh đó tự cài thêm skill vào `~/.agents/skills/` dùng chung cho mọi phiên, dễ tranh việc của skill này. `dv.py` chỉ gọi `render`.

### Bước 1 — Tạo dự án

```bash
python3 dv.py moi <tên-video> "<đường dẫn clip>"
python3 dv.py moi <tên-video> "<clip 1>" "<clip 2>"     # quay nhiều lần / máy tự chia file
```
Nhiều file thì liệt kê đúng thứ tự — số thứ tự từ chạy nối qua các file. Tên dự án nên theo khuôn `<ngày>-<vài chữ>`, ví dụ `2026-10-14-ban-hang-online`.

Máy tạo sẵn hai thư mục trong dự án: `anh/` (ảnh bằng chứng — ảnh chụp màn hình doanh thu, tin nhắn khách, bình luận…) và `broll/` (cảnh minh hoạ). **Nhờ người dùng tự thả file vào đó**; skill không tự đi lấy ảnh hay cảnh ở nơi khác.

### Bước 2 — Kiểm khung cắt dọc

```bash
python3 dv.py khung <tên> --giay 20
```
**Mở `khung-0.jpg` ra nhìn.** Khung vàng = khung thường, đỏ = khung phóng to, vạch trắng = chỗ phụ đề.
Sửa trong `bang-dung.json` cho tới khi: mặt nằm giữa khung đỏ, không mất đỉnh đầu, vạch trắng nằm **ngay dưới cằm**. `khung.x` = tâm ngang (0–1), `khung.y` = tâm dọc, `phu_de_y` = vị trí phụ đề (mặc định 0.70). Mỗi file một góc máy thì `khung` là danh sách, mỗi file một mục.

### Bước 3 — Nghe

```bash
python3 dv.py nghe <tên>
```
Clip 4 phút mất khoảng nửa phút đến một phút, tuỳ máy. Ra:
- `loi.txt` — lời nói đánh số từng từ: `[0082-0090] f0 00:34.1 | Cái chương thứ 9 ...`. Từ có dấu `?` là máy nghe không chắc.
- `phu-de.txt` — bản **nháp** phụ đề máy tự chia. Bước 4 phải rà lại; bản nháp hay tách đôi từ ghép (*"quyết | định"*).
- `loi-doi-chieu.txt` — *(khi đã cài PhoWhisper)* những chỗ hai bộ nghe **khác nhau về nội dung**, đánh số từ theo `loi.txt`. Đã lọc chỗ chỉ khác tiếng đệm/chữ lặp.

Hai bộ nghe mỗi bên giỏi một kiểu: PhoWhisper nghe từ tiếng Việt tốt hơn, nhưng viết số bằng chữ (*"ba mươi phút"*), đôi khi làm mất nửa câu hoặc **bịa thêm câu ở cuối file**. Nên bộ nghe chính vẫn là bản trong `loi.txt`; PhoWhisper chỉ chỉ ra chỗ cần soát.

Tên riêng hay bị nghe sai (tên người, tên thương hiệu, tên sản phẩm) thì thêm vào `goi_y_tu` trong `bang-dung.json`, xoá `phu-de.txt`, rồi nghe lại.

### Bước 4 — Soạn bảng dựng (AI làm, theo luật dưới)

Đọc trọn `loi.txt`, rồi sửa hai file:

**`bang-dung.json` → `bo`**: danh sách khoảng số từ phải bỏ, dạng `"72-73"`.
**`bang-dung.json` → `chen`**: danh sách cảnh chèn, mỗi cảnh neo vào **khoảng số từ** (`"tu": "82-90"`) chứ không neo giây — cắt lại bao nhiêu lần thì cảnh chèn vẫn bám đúng câu nói.

```json
{"loai": "the",       "tu": "82-90",   "nen": "den",   "tieu_de": "Bước 1", "phu": "Viết ra điều khách sợ nhất"}
{"loai": "danh_sach", "tu": "126-142", "nen": "trang", "tieu_de": "Bạn cần đúng 2 thứ:", "dong": ["1. Một lời hứa rõ", "2. Một bằng chứng thật"], "moc_dong": [126, 139]}
{"loai": "anh",       "tu": "207-221", "nen": "den",   "file": ["anh/doanh-thu.png", "anh/tin-nhan.png"], "nhan": ["tháng 8", "khách nhắn"]}
{"loai": "broll",     "tu": "58-65",   "file": "broll/pha-ca-phe.mp4", "tu_giay": 3}
```

`file` viết tương đối thì tính từ thư mục dự án. B-roll có thể thêm `"x"`, `"y"` (tâm khung cắt dọc, 0–1) và `"zoom"`.

**`phu-de.txt`**: mỗi dòng một lần hiện chữ — `<từ đầu>-<từ cuối> | dòng nhỏ // CỤM NHẤN`. Chỉ có dòng nhỏ thì gõ từng chữ; chỉ có `// ...` thì hiện một dòng to; xoá dòng thì đoạn đó không có chữ.

#### Luật biên tập

**Cắt (`bo`)**
1. Bỏ không cần hỏi: "alo", đếm ngược, câu nói lại (giữ **lần nói sau cùng trọn vẹn**), câu vấp bỏ dở, lời tự nhắc ("mình sẽ… mình sẽ").
2. **Bỏ một ý có nội dung thật thì phải hỏi người dùng.** AI không tự quyết video dài hay ngắn.
3. Ba giây đầu phải vào thẳng ý. Mở đầu mà rào đón thì **đề xuất** câu mở đầu mạnh hơn có sẵn trong lời, không tự đảo thứ tự.
4. Khoảng lặng máy tự cắt, đừng liệt kê vào `bo`. Luật máy: khe ngắn chỉ cắt khi im thật; khe **≥ 0,8 giây không có chữ nào** thì cắt luôn dù có tiếng động (lật giấy, "ờ", "à").

**Phụ đề**
5. 2–5 chữ một lần, dòng nhỏ tối đa khoảng 26 ký tự. Sửa chữ máy nghe sai theo ngữ cảnh — **từ có dấu `?` trong `loi.txt` và mọi dòng trong `loi-doi-chieu.txt` phải soát kỹ**: chọn bản hợp ngữ cảnh; cả hai đều gượng thì đưa vào mục "cần nghe lại" của bảng trình, đừng đoán rồi im. Dòng chỉ PhoWhisper có ở **cuối file** thường là câu nó bịa.
6. Được lược từ đệm (*thì, là, cái, mà*) nếu không đổi nghĩa. Không viết thêm ý người nói không nói.
7. Cụm nhấn (`// ...`): con số, kết quả, từ khoá của ý, chữ mang cảm xúc. Cứ 1–3 dòng một cụm; **không quá 40% số dòng** có cụm nhấn — nhấn khắp nơi là không nhấn gì.
8. Đoạn nằm dưới thẻ chữ / danh sách thì không cần phụ đề (máy tự bỏ và báo số).

**Cảnh chèn**
9. `the`: đầu mục của bài (bước 1, bước 2…), tên phần, một con số lớn. **2–5 giây.** Xen kẽ nền `den` và `trang`.
10. `danh_sach`: khi người nói liệt kê 2–4 ý. Mỗi dòng ≤ 35 ký tự. `moc_dong` neo mỗi dòng vào số từ bắt đầu ý đó để chữ gõ ra đúng lúc nói.
11. `anh`: khi nhắc tới bằng chứng (doanh thu, tin nhắn khách, bình luận, kết quả). **Chỉ dùng ảnh người dùng đã thả vào `anh/`** — thiếu thì ghi vào mục "xin ảnh" của bảng trình, không lấy ảnh khác thế vào. Ảnh ngang tự xếp chồng dọc, ảnh dọc (chụp màn hình điện thoại) xếp cạnh nhau.
12. `broll`: khi câu nói tả cảnh hay hành động. **Chỉ dùng clip người dùng đã thả vào `broll/`** — mở từng clip ra xem (trích một khung bằng ffmpeg) trước khi chọn, ghi `tu_giay` là giây bắt đầu lấy trong clip. Không có cảnh hợp thì ghi "cần quay thêm" vào bảng trình, đừng chèn đại.
13. **Mặt người nói là tài sản chính**: tổng thời lượng cảnh chèn ≤ 40% video, mỗi cảnh ≤ 5 giây (trừ danh sách dài).
14. **Chuyển cảnh nhanh và gọn.** Mặc định: thẻ chữ *phóng* vào, *mờ* ra · danh sách *trượt* vào, *mờ* ra · ảnh *trượt* vào và ra · B-roll *mờ* vào và ra. Mỗi lần 0,3 giây (*lắc* 0,22 giây). Một video dùng tối đa 2–3 kiểu; *lắc* và *nhoè* để dành cho chỗ nhấn mạnh.

**Chữ trên thẻ là thứ người xem đọc.** Viết bằng chính lời người xem hay nói, câu ngắn, không viết tắt, không mã, không thuật ngữ nội bộ. Người lạ đọc lần đầu phải hiểu ngay.

### Bước 5 — Trình bảng dựng cho người dùng duyệt, CHỜ DUYỆT

Không dựng trước khi người dùng gật. Trình một bảng ngắn:

| Mục | Nội dung |
|---|---|
| Đoạn bỏ | từng khoảng, trích vài chữ đầu + lý do |
| Cảnh chèn | loại · câu nói đi kèm · chữ trên thẻ / tên ảnh / tên clip B-roll |
| Xin ảnh / xin cảnh | chỗ cần ảnh bằng chứng hay cảnh minh hoạ mà `anh/`, `broll/` chưa có |
| Cần nghe lại | chữ máy nghe không chắc mà AI đã sửa theo ngữ cảnh |
| Câu mở đầu | giữ nguyên hay đề xuất câu khác (luật 3) |

### Bước 6 — Dựng nháp, TỰ NHÌN trước khi đưa người dùng

```bash
python3 dv.py dung <tên> --nhap                     # cả video, 540x960, khoảng 1 phút cho video 1 phút
python3 dv.py dung <tên> --nhap --tu 20 --den 45    # chỉ dựng một khúc (giây trên bản dựng) để sửa nhanh
```

**Đọc khối báo cáo cuối.** Máy tự khai mọi thứ nó bỏ:
- `Cat`: bao nhiêu từ bỏ theo bảng dựng, bao nhiêu khoảng lặng cắt, bao nhiêu khe có tiếng động vẫn cắt, bao nhiêu khe **không** cắt vì không im thật.
- `Phu de`: số dòng trong file → số dòng hiện, bỏ vì chữ đã cắt, bỏ vì nằm dưới thẻ chữ.
- `Nhip hinh`: bao nhiêu giây đổi hình một lần so với mục tiêu, và **quãng hình đứng yên dài nhất**. Quá 6 giây thì thêm cảnh chèn hoặc giảm `doi_khung_moi`.
- Dòng `!!` là cảnh báo (B-roll ngắn hơn chỗ cần nên phải đứng hình khung cuối…).

Rồi **trích khung hình ra nhìn** — phụ đề, từng thẻ chữ, từng cảnh chèn:
```bash
ffmpeg -ss <giây> -i ~/CreatorVideo/dung/<tên>/ban-nhap.mp4 -frames:v 1 -vf scale=360:-2 -q:v 4 <thư mục tạm>/k.jpg
```

Rồi **soi từng chỗ cắt**:
```bash
python3 dv.py soi <tên> --nhap
```
Mỗi chỗ cắt thành một dải ảnh: 4 khung quanh vết cắt + sóng âm có vạch đỏ + chữ trước/sau, 6 chỗ một tấm trong thư mục `soi/` của dự án. Máy đo thêm hai thứ, **chỉ ở vết cắt thật**: `bup` — tiếng tách ngay vết cắt to vọt so với hai bên; `lem tieng` — sát vết cắt vẫn đang nói to, nghi cắt vào giữa chữ. Đó là **gợi ý**: nhìn sóng âm trong ảnh rồi mới sửa (thường là nới `bo` ra một từ). Tối đa 3 vòng sửa–dựng–soi rồi đưa người dùng.

Thấy lỗi thì sửa rồi dựng lại — **không đưa người dùng bản mình chưa nhìn**. Xong thì gửi đường dẫn `ban-nhap.mp4` cho người dùng.

📌 **Sửa chữ, thẻ, B-roll thì không cắt lại đoạn quay chính**: máy nhớ danh sách cắt; không đổi `bo`, `khung`, `lut` thì dùng lại file đã cắt — nhanh hơn, và không cần cắm lại ổ chứa file gốc.

### Bước 7 — Sửa theo lời người dùng

Người dùng nói bằng lời ("bỏ câu này", "thẻ này ngắn thôi", "chỗ này chèn cảnh pha cà phê"), AI sửa `bang-dung.json` / `phu-de.txt`, dựng nháp lại đúng khúc đó bằng `--tu`/`--den`.

### Bước 8 — Bản cuối

```bash
python3 dv.py dung <tên>
```
Ra `ban-dung.mp4` (1080x1920, âm lượng chuẩn mạng xã hội −14 LUFS) và thư mục `lop/` gồm các lớp rời để sửa tay trong CapCut/Premiere:

| File | Đặt vào đâu |
|---|---|
| `01-a-roll-da-cat.mp4` | đoạn quay chính (người nói) đã cắt, đã cân âm lượng — track chính, 0:00 |
| `02-chu-va-the-trong-suot.mov` | *(khi vẽ bằng HyperFrames)* file video nền trong suốt chứa **cả phụ đề lẫn thẻ chữ / danh sách / ảnh bằng chứng** — track trên cùng, 0:00 |
| `02-phu-de-trong-suot.mov` | *(khi vẽ bằng ffmpeg)* chỉ phụ đề, nền trong suốt — track trên cùng, 0:00; thẻ chữ nằm trong `03-chen/` |
| `02-phu-de.srt` | thay file .mov nếu muốn sửa chữ trong CapCut (mất hiệu ứng) |
| `03-chen/NN_<phút>m<giây>s_<loại>.mp4` | track phụ, đặt đúng mốc ghi trong tên file — xem `moc-thoi-gian.txt` |

Trong `lop/` có sẵn `DOC-TRUOC.txt` hướng dẫn bằng tiếng Việt để chuyển cho người dựng.

### Bước 9 — Xuất thẳng thành dự án CapCut (khi người dùng muốn tự chỉnh tiếp)

```bash
python3 dv.py capcut <tên>            # ĐÓNG CapCut trước khi chạy
```

Máy tạo một dự án tên `dv-<tên>` ngay trong danh sách dự án của CapCut (Mac, CapCut 9.x). Mở CapCut là thấy timeline dựng sẵn:

| Track | Chứa gì | Sửa được gì |
|---|---|---|
| chính | từng đoạn quay đã cắt, **trỏ về file gốc** (cắt dọc 9:16 + phóng to đổi khung bằng thông số của clip) | kéo dài / rút ngắn **từng vết cắt**, đổi khung |
| video chồng 1 | B-roll, mỗi đoạn dư 2 giây hai đầu | kéo thêm, thay, xoá |
| video chồng 2 | thẻ chữ, danh sách, ảnh bằng chứng — mỗi cái một clip | dời, xoá, đổi độ dài |
| video chồng 3 | lớp phụ đề đẹp (nền trong suốt) | bật/tắt |
| chữ | phụ đề bằng chữ CapCut, **để ẩn sẵn** | muốn sửa chữ: bật track này, tắt video chồng 3 |

- **Chuyển cảnh:** thẻ chữ mang sẵn hiệu ứng vào/ra (khi vẽ bằng HyperFrames). B-roll chưa mang chuyển cảnh sang CapCut — thêm tay bằng thư viện Chuyển cảnh của CapCut.
- **Màu:** file LUT (nếu có) không mang sang dự án CapCut — muốn chỉnh màu thì thêm trong CapCut.
- **Media gom vào `~/Movies/CreatorVideo/<tên>/`**, vì CapCut trên Mac chỉ tự đọc được file trong `~/Movies`. Đoạn quay gốc được chép nguyên file sang đó. `--khong-chep` = trỏ thẳng về file gốc, nhưng có thể CapCut không được phép đọc.
- `--thu <thư mục>` = ghi dự án ra thư mục nháp, **không** đăng ký vào CapCut — để kiểm bộ xuất.
- **Không bao giờ ghi đè dự án có sẵn**: trùng tên thì thêm `-2`, `-3`. Trước khi ghi danh sách dự án (`root_meta_info.json`), máy sao lưu thành `root_meta_info.json.truoc-dung-video-<giờ>`.
- CapCut đang mở thì lệnh **từ chối chạy** — CapCut ghi lại danh sách dự án lúc thoát, sẽ xoá mất dự án mới.

Báo cáo cho người dùng theo thứ tự: đã làm gì (dựng bản nào, đã tự xem bao nhiêu khung) → thấy gì (độ dài, nhịp đổi hình, số cảnh chèn, cảnh báo) → rồi mới kết luận.

---

## Tuỳ chọn trong `bang-dung.json`

| Khoá | Mặc định | Ý nghĩa |
|---|---|---|
| `zoom` | `[1.0, 1.12]` | các mức khung luân phiên sau mỗi lần cắt / đổi khung. `[1.0]` = tắt |
| `doi_khung_moi` | `4.5` | đoạn nói liền dài hơn bấy nhiêu giây thì đổi khung một lần. `0` = tắt |
| `lang_toi_da` | `0.25` | giữ lại tối đa bấy nhiêu giây lặng ở chỗ nối |
| `nguong_lang_db` | `-35` | mức coi là im. Phòng ồn thì nâng lên −30 rồi **nghe lại** |
| `goi_y_tu` | tên kênh (nếu có) + vài tên mạng xã hội | tên riêng gợi ý cho bộ nghe, cách nhau bằng dấu phẩy |
| `nhac` | `null` | `{"file": "nhac/nen.mp3", "am_luong": 0.15}` — nhạc nền, tự nhỏ đi khi có tiếng nói. Dùng nhạc người dùng có quyền dùng |
| `lut` | `null` | file chỉnh màu `.cube` của người dùng: một đường dẫn (áp cho mọi file quay) hoặc danh sách theo đúng thứ tự `nguon` (`null` ở file nào thì file đó giữ màu gốc) |
| `lut` (trong một cảnh B-roll) | không có | file `.cube` riêng cho cảnh đó |
| `nen` (trong thẻ) | `"den"` | `"den"` hoặc `"trang"` (trắng ngà) |
| `chuyen_canh` | xem luật 14 | đổi chung, ví dụ `{"the": ["lac","mo"], "broll": "cat", "giay": 0.3}` |
| `vao` / `ra` (trong một cảnh chèn) | theo `chuyen_canh` | `cat` · `mo` · `truot` · `phong` · `lac` · `nhoe` |
| `keo_dai` (trong một cảnh chèn) | `0.12` | kéo cảnh chèn dài thêm sau từ cuối (giây) |
| `dong_co` | tự chọn | `"hyperframes"` (có cài thì mặc định) hoặc `"ass"` (vẽ bằng ffmpeg — nhanh, kém mượt, không cần cài thêm) |
| `nghe_kep` | `true` | nghe lần hai bằng PhoWhisper để đối chiếu (khi đã cài) |
| `phong_cach` | `"chuyen-gia-ngoi-noi"` | file công thức trong `phong-cach/` |
| `nhip_muc_tieu` | `3.1` | số giây mỗi lần đổi hình để so trong báo cáo |

## Bẫy đã gặp — đọc trước khi sửa bộ máy

1. **Tiếng động không phải im lặng.** Tiếng lật giấy làm máy đo tưởng có tiếng nói, không dám cắt — một thẻ chữ kéo dài gần 7 giây. Vì vậy có luật khe ≥ 0,8 giây không có chữ thì cắt. Luật này cũng dọn luôn "ờ, à" vì bộ nghe thường không chép chúng ra chữ.
2. **Máy đo im lặng hay xé đôi một khoảng im** bởi một tiếng tách rất ngắn. Không gộp thì chỉ cắt được nửa. `gop_lang()` gộp các khoảng cách nhau ≤ 0,06 giây.
3. **Cắt dọc từ file nhỏ là mờ.** Cắt 9:16 từ khung ngang chỉ còn khoảng 32% bề ngang — từ 4K ra 1215px (nét), từ 720p ra 405px (vỡ). Luôn dùng file gốc độ phân giải cao.
4. **Ảnh ngang xếp hai cột thì bé tí.** Máy tự nhận ảnh ngang hay dọc để xếp chồng hay xếp cạnh.
5. **Bản nháp phụ đề tách đôi từ ghép.** Bộ nghe trả về từng âm tiết; máy không biết "quyết định" là một từ. Bước 4 luôn phải rà.
6. **Chỉ chạy trên Mac chip Apple.** mlx-whisper chỉ chạy trên chip Apple. Muốn chạy Windows phải thay bộ nghe (ví dụ faster-whisper) — chưa làm.
7. **`hyperframes init` tự cài skill ra máy dùng chung.** Có skill trong đó tự nhận là cửa vào cho mọi yêu cầu làm video — dễ giành việc của skill này. `dv.py` không gọi `init`; nó dùng bản cài riêng trong `~/CreatorVideo/.hyperframes/`.
8. **HyperFrames đòi `ffprobe`**, nhiều máy chỉ có `ffmpeg` (ví dụ cài qua gói pip `imageio-ffmpeg`). `ffprobe_gon.py` làm thay bằng `ffmpeg`: hỗ trợ `-version` và kiểu hỏi JSON, gặp kiểu gọi lạ thì báo lỗi to, mọi lần gọi ghi vào `~/CreatorVideo/.ffprobe-gon.log`. Có `ffprobe` thật thì máy tự dùng bản thật.
9. **Cụm nhấn dài bị xuống 2 dòng.** Máy đo độ rộng bằng chính file font rồi thu cỡ chữ cho vừa một dòng; tiêu đề thẻ chữ cũng vậy.
10. **Rút ổ chứa file gốc giữa chừng** → máy kiểm file nguồn trước và báo bằng lời, không dựng dở.
11. **Khuôn dự án CapCut không có tài liệu chính thức.** `capcut_mau.json` rút từ một dự án trống do CapCut 9.2 tạo. CapCut cập nhật có thể đổi khuôn — dự án xuất ra không mở được thì rút khuôn lại từ một dự án mới tạo bằng bản CapCut hiện tại.
12. **File trong Desktop/Documents đồng bộ iCloud có thể chỉ nằm trên mây** (`ls -lO` hiện `dataless`). Đọc vào là máy âm thầm tải về cả file video nặng. Kiểm trước khi đọc.
13. **Chuyển cảnh khi vẽ bằng ffmpeg** (B-roll, thẻ khi `dong_co` là `ass`): *phóng* được làm sẵn vào file B-roll; *nhoè*/*lắc* dùng độ nhoè không đổi trong khoảng chuyển cảnh (ffmpeg không cho độ nhoè đổi theo thời gian). Thẻ vẽ bằng HyperFrames thì chuyển cảnh mượt thật.

## Skill này KHÔNG làm

- **Không viết kịch bản hay danh sách cảnh cần quay.**
- **Không đăng video lên đâu cả.** Đăng là việc có người bấm.
- **Không tự lấy ảnh, cảnh, nhạc ở nơi khác** — chỉ dùng file người dùng đưa vào.
- **Không xoá, không sửa file quay gốc.**

## Ghi nguồn

Dùng các công cụ mã nguồn mở, cài từ nguồn công khai — skill không chép mã hay mô hình của họ vào đây: [HyperFrames](https://github.com/heygen-com/hyperframes) (Apache-2.0 — vẽ chữ) · [mlx-whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper) (MIT — bộ nghe, kèm script chuyển đổi mô hình) · [PhoWhisper](https://github.com/VinAIResearch/PhoWhisper) (VinAI, BSD-3 — bộ nghe thứ hai) · [Be Vietnam Pro](https://github.com/bettergui/BeVietnamPro) (OFL — font, kèm trong `fonts/`) · ý tưởng soi chỗ cắt bằng dải khung + sóng âm từ [browser-use/video-use](https://github.com/browser-use/video-use) (MIT).

Tác giả: Tô Hải Đoàn, giấy phép MIT
