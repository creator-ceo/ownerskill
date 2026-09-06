---
name: soi-ads
description: Chạy và tối ưu quảng cáo Meta (Facebook) + Google Ads cho bạn — kéo số liệu về, chấm từng quảng cáo, đề xuất tắt/giảm/nuôi, và áp vào tài khoản trong hạn mức cứng sau khi bạn duyệt. Dùng khi bạn gõ /soi-ads, hoặc nói bất cứ điều gì kiểu "quảng cáo hôm nay thế nào", "soi giúp ads", "CPL đang bao nhiêu", "tắt mấy cái ads kém đi", "tăng ngân sách cho cái đang ngon", "ads Facebook đang lỗ", "check Google Ads", "sao lead ít thế", "nên đổi hook nào cho quảng cáo". Cũng dùng khi bạn hỏi vì sao một quảng cáo bị tắt, hoặc muốn xem lịch sử agent đã tự làm gì.
---

# Soi và tối ưu quảng cáo

## Ranh giới của skill này — đọc trước

Skill này **được phép tiêu tiền của bạn**. Không skill nào khác trong hệ có quyền đó. Nên nó có một luật mà các skill khác không có:

> ### Không bao giờ chạy `bo-may/ap.mjs --that --toi-dong-y` nếu bạn chưa nói "được" **trong chính cuộc hội thoại này**.
>
> Không suy ra từ việc bạn từng duyệt hôm qua. Không suy ra từ câu *"cứ tối ưu giúp anh"*. Phải là một câu đồng ý, sau khi đã nhìn thấy danh sách hành động cụ thể.

Luật đầy đủ của bộ máy ở `bo-may/CLAUDE.md` — đọc khi định sửa gì trong `bo-may/`.

---

## ⚠️ Lần đầu dùng — CHÉP BỘ MÁY RA NGOÀI trước khi làm gì khác

Skill này được cài dưới dạng plugin, nên `bo-may/` nằm trong thư mục cache của Claude Code. **Bản cập nhật plugin sau sẽ ghi đè thư mục đó** — cuốn theo `luat.json` bạn đã điền, khoá API trong `.khoa/`, và cả `nhat-ky.jsonl` ghi lịch sử agent đã làm gì.

Nên việc đầu tiên là chép bộ máy ra thư mục làm việc của bạn:

```bash
cp -R "$CLAUDE_PLUGIN_ROOT/skills/soi-ads/bo-may" ./ads
```

Từ đó về sau **mọi lệnh chạy trong `./ads`**, không chạy trong thư mục plugin. Ở các bước dưới, chỗ nào ghi `bo-may/` thì đọc là `ads/`.

Rồi thêm hai dòng này vào `.gitignore` của bạn — khoá API không bao giờ được commit:

```
ads/.khoa/*
!ads/.khoa/mau.env
```

📌 Đã chép rồi thì bỏ qua mục này. Kiểm bằng cách xem thư mục `ads/` đã có chưa.

---

## Quy trình — 5 bước

### Bước 0. Soi máy trước khi soi số

```bash
node bo-may/kiem.mjs
```

Nếu báo còn ô chưa điền trong `bo-may/luat.json`: **dừng lại, hỏi bạn**, đừng tự điền số nào. Nhất là `cplMucTieuVnd` — không có CPL mục tiêu thì mọi chữ "tốt/xấu" ở các bước sau đều là bịa, đúng thứ Hard Don't #5 cấm.

Cách suy CPL mục tiêu cùng bạn (hỏi, đừng tự tính rồi ghi):
`giá bán × tỷ lệ chốt từ lead × phần trăm chịu chi cho marketing`. Số liệu nền ở `wiki/business-metrics.md` nếu bạn đã dựng trang đó. **Tỷ lệ chốt từ lead thì hầu như không bộ não nào có sẵn** — phải hỏi.

### Bước 1. Kéo và chấm

```bash
node bo-may/keo.mjs && node bo-may/soi.mjs
```

Nếu một nền báo lỗi còn nền kia chạy được thì **cứ đi tiếp với nền chạy được**, nhưng nói rõ nền nào đang mù. Đặc biệt: lỗi `DEVELOPER_TOKEN_NOT_APPROVED` của Google là cổng chờ đã biết trước, không phải hỏng — xem `bo-may/README.md`.

### Bước 2. Đọc bảng số, rồi thêm thứ code không đọc được

`bo-may/soi.mjs` đã chấm xong phần **định lượng** (CPL, CTR, tần suất, đủ bằng chứng chưa). Đừng chấm lại — cùng một bảng số phải ra cùng một kết luận, đó là lý do phần đó nằm trong code chứ không nằm ở đây.

Việc của bạn là ba câu hỏi mà số không tự trả lời:

| Câu hỏi | Cách trả lời |
|---|---|
| **Vì sao cái này chết?** | Phân biệt ba loại chết khác nhau — chúng cần ba cách chữa khác nhau. |
| **Cụm nào đang lặp lại một kiểu sai?** | Ba quảng cáo cùng chết ở một nhóm đối tượng = vấn đề nhắm, không phải vấn đề nội dung. Ba quảng cáo cùng hook chết ở ba nhóm khác nhau = vấn đề hook. |
| **Thử gì tiếp?** | Rút hook mới từ `viet-content/luat/hook.md` *(8 kiểu hook)* và phản đối từ `wiki/objections-library.md` *(nếu đã dựng)*. **Không tự nghĩ hook mới** khi kho còn hook chưa dùng. |

**Ba loại chết, đừng gộp làm một:**

| Dấu hiệu | Chẩn đoán | Chữa |
|---|---|---|
| CTR thấp, tần suất thấp | **Người ta không buồn nhìn** — hook hỏng | Đổi hook, giữ nguyên nhắm |
| CTR ổn, tần suất cao | **Người ta nhìn chán rồi** — nội dung mòn | Đổi hình/video, đừng đổi ngân sách. Tăng tiền cho cái đang mòn là đổ tiền vào chỗ thủng. |
| CTR ổn, tần suất ổn, nhưng ít lead | **Đứt ở trang đích**, không phải ở quảng cáo | Đừng tắt quảng cáo. Đi soi trang đăng ký. |

⚠️ Cột phải của dòng thứ ba là chỗ agent hay sai nhất: số của quảng cáo trông xấu nên nó tắt quảng cáo, trong khi lỗi nằm ở trang sau cú nhấp.

### Bước 3. Thử khan, rồi trình cho bạn

```bash
node bo-may/ap.mjs
```

Trình cho bạn theo đúng thứ tự này:

1. **Tiền đang nằm ở đâu** — bao nhiêu đang chảy vào nhóm 🔴, bao nhiêu vào 🟢. Con số này quan trọng hơn số lượng quảng cáo.
2. **Danh sách hành động qua chặn**, mỗi dòng một câu lý do bằng tiếng người.
3. **Danh sách bị chặn và vì sao** — đừng giấu. Một hành động bị chặn vì `chua_du_bang_chung` là thông tin thật: nghĩa là *chưa biết*, không phải *đã ổn*.
4. **Việc phải làm tay** — thứ agent không có quyền: đổi hook, đổi hình, sửa trang đích, tạo nhóm mới.

Rồi hỏi một câu thẳng: *"Em áp mấy cái này chứ ạ?"*

### Bước 4. Áp — chỉ khi bạn đã gật

```bash
node bo-may/ap.mjs --that --toi-dong-y
```

Nếu bạn chỉ duyệt một phần: **đừng chạy rồi chọn lọc sau** — sửa file trong `bo-may/de-xuat/`, bỏ các dòng không được duyệt, rồi mới chạy. Lớp chặn không biết bạn duyệt cái nào.

Xong thì báo lại: bao nhiêu xong, bao nhiêu hỏng, bao nhiêu bị chặn. Ca **hỏng** phải nói rõ — tài khoản lúc đó đang ở trạng thái nửa vời, và đó là thứ bạn cần biết ngay.

---

## Khi bạn hỏi "agent đã tự làm gì rồi"

```bash
tail -30 bo-may/nhat-ky.jsonl
```

Mỗi dòng một hành động, có `ket` là `da_ghi` · `hong` · `bi_chan`. Đọc rồi kể lại bằng tiếng người, đừng dán JSON thô ra.

---

## Khi bạn nhờ viết nội dung quảng cáo

**Không viết ở đây.** Chuyển sang skill `viet-content` — nó có đủ luật giọng, checklist chống giọng AI, và bước bạn duyệt. Skill này lo phần số; skill kia lo phần chữ.

Nhưng khi trình đề xuất thì **được phép nói rõ cần viết gì**: *"Hook 'Bỏ nghề' chết vì CTR 0.70% — nên thử hook số 4 trong kho, chạy `/viet-content` để dựng."*

---

## Bốn cái bẫy đã biết

1. **Tắt quá sớm.** Đây là sai lầm số một của mọi agent tối ưu ads. `bo-may/luat.json` đã chặn bằng `soNgayDuLieuToiThieu` + `chiTieuToiThieuTruocKhiKetVnd`, nhưng bạn cũng đừng *khuyên* bạn tắt tay thứ mà lớp chặn vừa từ chối tắt. Chặn rồi lại lách qua đường mồm là vô hiệu hoá chính lớp chặn.

2. **Đọc CPL đẹp trên 2 lead.** Hai lead may mắn cho ra CPL 15.000đ trông như vàng. `bo-may/soi.mjs` gắn cảnh báo *"chưa đủ mẫu để tin"* — đừng bỏ qua dòng đó khi tóm tắt.

3. **Nới hạn mức để một đề xuất lọt qua.** Nếu thấy mình đang định sửa `bo-may/luat.json` giữa lúc đang chạy quy trình: **dừng**. Nới hạn mức là quyết định riêng, làm trước, bạn duyệt riêng. Xem luật 2 ở `bo-may/CLAUDE.md`.

4. **Tăng ngân sách cho quảng cáo đang mòn.** Tần suất cao + CPL còn đẹp = nó *sắp* hỏng, không phải *đang* ngon. Đổ thêm tiền chỉ làm nó mòn nhanh hơn.

---

## Khi quảng cáo dạy ra một điều đáng nhớ

Một ngưỡng CPL học được, một góc nhắm bất ngờ, một hook chết vì lý do không ai đoán trước — đó là thứ đáng vào bộ não. Gợi ý chạy `/nap-kho`.

🚫 **Đừng sửa thẳng `wiki/`** — bộ não chỉ có một đường ghi.

⚠️ Nếu `wiki/` của bạn có một dòng luật đi ngược với việc đang chạy quảng cáo (ví dụ *"chưa chạy ads trả phí trước khi content organic chứng minh được"*), **nói ra chỗ chỏi nhau đó**, đừng lờ đi và cũng đừng tự sửa. Bạn quyết, rồi ghi lại quyết định qua `/nap-kho`.

---

## Skill này của ai

Viết bởi **Tô Hải Đoàn** — người làm nội dung và xây thương hiệu cá nhân tại Việt Nam. Đây không phải skill dựng cho vui: nó là quy trình tôi dùng cho công việc của chính mình mỗi ngày, đóng gói lại để bạn chạy được trên dữ liệu của bạn.

Giấy phép MIT, bạn dùng và sửa thoải mái.

**Kẹt ở đâu, hoặc muốn được hướng dẫn dùng cho đúng việc của bạn** thì nhắn tôi: [facebook.com/tohaidoan](https://www.facebook.com/tohaidoan/)
