---
name: cai-thu-thu
description: Bước 1 khi dựng đội nhân sự A.I — cài vai Thủ thư, người giữ kho tài liệu của bạn. Tạo thư mục bộ não, dạy cách nạp thông tin bằng /nap-kho, rồi kiểm xem đã lưu thật vào file chưa. Dùng khi bạn mới bắt đầu, hỏi "cài vai đầu tiên", "dựng kho tài liệu cho tôi", "bắt đầu từ đâu", hoặc gõ /cai-thu-thu.
---

# Cài vai Thủ thư — bước 1 trong 5

Thủ thư là vai đầu tiên vì mọi vai sau đều **đọc từ kho** do vai này giữ và **ghi vào kho** qua vai này. Chưa có kho thì các vai sau không có gì để đọc.

**Kho chỉ là một thư mục file thường.** Không có tài khoản, không có phần mềm riêng. Bạn mở ra đọc được bằng mắt.

## Việc 1 — Dựng khung kho *(làm một lần)*

Dùng **chính thư mục đang mở** làm kho (nên là một thư mục riêng, chỉ để làm việc này; đang mở thư mục lẫn lộn thì nhờ bạn mở lại ở một thư mục mới). Đừng hỏi bạn đặt ở đâu. Trong đó tạo:

```
raw/                  ← tài liệu gốc bạn đưa vào, không bao giờ sửa
wiki/                 ← các trang đã được đúc lại
wiki/doi-ngu.md       ← sổ đội: vai nào đã cài, cài ngày nào
index.md              ← danh sách mọi trang kèm một dòng tóm tắt
log.md                ← nhật ký, chỉ ghi thêm xuống dưới
```

Đây là lần **duy nhất** bạn dựng file trong `wiki/` mà không qua `/nap-kho`. Các thư mục khác (`ke-hoach/`, `content/`, `doi-thu/`…) do các vai sau tự tạo cạnh kho để chứa sản phẩm, chúng không phải một phần của kho. Từ đây về sau mọi trang đều ghi qua `/nap-kho`.

Nội dung `wiki/doi-ngu.md` ban đầu:

```
# Sổ đội

| Bước | Vai | Đã cài ngày | Ghi chú |
|---|---|---|---|
| 1 | Thủ thư | | |
| 2 | Nghiên cứu | | |
| 3 | Tổng giám đốc | | |
| 4 | Content | | |
| 5 | Editor | | |
```

**Không dựng sẵn các trang trống** như giọng văn, khách hàng hay mục tiêu. Mỗi vai sẽ dựng đúng trang nó cần, vào đúng lúc nó cần, bằng thông tin thật. Trang trống chỉ làm hệ thống tưởng đã có dữ liệu.

## Việc 2 — Nói với bạn ba điều

1. Kho là thư mục file, bạn sở hữu hoàn toàn.
2. Thông tin muốn lưu thì nói với Thủ thư (`/nap-kho`). Thủ thư đọc, soi xem có trùng cái cũ không, rồi mới ghi. Không sửa tay trực tiếp vào `wiki/`, vì sau vài tuần sẽ có hai trang nói ngược nhau mà không ai biết.
3. Các vai sau sẽ hỏi bạn đúng thứ chúng cần. Bạn không phải trả lời hết một lần.

## Việc 3 — Nạp hai trang đầu tiên, bằng `/nap-kho`

**Trang 1: hồ sơ gốc** (`wiki/about-me.md`). Bảo bạn kể hai ba câu: bạn là ai, làm gì, cho ai, hiện bán gì (nếu có). Gọi `/nap-kho` để ghi.

**Trang 2: cách làm việc với A.I** (`wiki/ai-operating-preferences.md`). Hỏi ba câu, mỗi câu một lượt:
1. *"Bạn muốn mình xưng hô thế nào?"*
2. *"Việc nào mình được cứ làm, việc nào bắt buộc phải hỏi bạn trước?"*
3. *"Có điều gì mình tuyệt đối không được làm hoặc nói thay bạn?"*

Gọi `/nap-kho` để ghi. Trang này quan trọng vì mọi vai sau đọc nó đầu tiên.

Rồi mở file vừa ghi, đọc to một dòng cho bạn nghe.

## Việc 4 — Kiểm xem lưu thật chưa

Mời bạn mở **một đoạn chat mới** trong thư mục này, rồi chạy `/kiem-chung`. Ở bước này chỉ hỏi bốn câu đầu (đọc được file, bạn là ai, điều tuyệt đối không được làm, một chi tiết chỉ bạn biết). Trả lời đúng nghĩa là kho lưu thật chứ không chỉ nằm trong trí nhớ đoạn chat.

## Xong khi nào

Đủ cả ba: có đủ khung thư mục · có hai trang `about-me.md` và `ai-operating-preferences.md` ghi bằng `/nap-kho` · `/kiem-chung` đạt bốn câu.

Ghi ngày cài vào dòng "Thủ thư" trong `wiki/doi-ngu.md` (qua `/nap-kho`). Rồi nói: *"Bước 2 là cài vai Nghiên cứu. Gõ `/cai-nghien-cuu`."*

## Skill này của ai

Tô Hải Đoàn, giấy phép MIT.
