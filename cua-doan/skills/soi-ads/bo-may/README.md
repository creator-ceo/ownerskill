# Agent quảng cáo — cách cài và cách chạy

Bốn lệnh, chạy theo thứ tự. Ba lệnh đầu **chỉ đọc**, không lệnh nào tiêu tiền.

```bash
node ads/kiem.mjs     # soi lớp chặn + xem còn thiếu cấu hình gì
node ads/keo.mjs      # kéo số liệu 7 ngày về ads/du-lieu/
node ads/soi.mjs      # chấm điểm → ads/de-xuat/
node ads/ap.mjs       # THỬ KHAN: soi đề xuất qua lớp chặn, không ghi
```

Ghi thật cần hai cờ: `node ads/ap.mjs --that --toi-dong-y`

Thử toàn bộ đường ống bằng dữ liệu giả, không cần khoá gì cả:

```bash
node ads/keo.mjs --gia && node ads/soi.mjs --gia && node ads/ap.mjs --gia
```

---

## Cài đặt — hai cổng chờ thật, đọc trước khi bắt đầu

### Meta: khoảng 20 phút, không phải chờ ai duyệt

Quản tài khoản quảng cáo của **chính mình** thì **không cần App Review**. Dùng System User:

1. `business.facebook.com` → Cài đặt doanh nghiệp → **Người dùng hệ thống** → Thêm
2. Gán tài sản: tài khoản quảng cáo cần quản, quyền **Quản lý chiến dịch**
3. Tạo token với quyền `ads_read` + `ads_management`, chọn **không hết hạn**
4. Dán vào `.khoa/that.env` ở dòng `META_TOKEN=`
5. Điền `taiKhoan.meta.adAccountId` trong `luat.json` (dạng `act_1234567890`)

### Google: tính bằng TUẦN, không có đường vòng

Developer token mới cấp nằm ở mức **Test Account** — chỉ chạy được với tài khoản test, **không chạm được tài khoản thật**. Muốn chạm tài khoản thật phải nộp đơn xin **Basic Access** ở API Center và chờ Google duyệt.

Không có cách nào rút ngắn. Code trong `lib/google.mjs` đã đúng và chạy được ngay khi token lên Basic; trước đó nó trả lỗi `DEVELOPER_TOKEN_NOT_APPROVED` và `keo.mjs` sẽ in lỗi đó ra chứ không im lặng bỏ qua.

1. `ads.google.com` → Công cụ → **API Center** → lấy developer token, **nộp đơn xin Basic Access ngay hôm nay** (chờ song song với việc làm phần Meta)
2. `console.cloud.google.com` → APIs & Services → bật **Google Ads API** → Credentials → tạo OAuth client **Desktop app**
3. Dán `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` vào `.khoa/that.env`
4. Chạy `node ads/xin-khoa-google.mjs` → làm theo hướng dẫn → dán `GOOGLE_REFRESH_TOKEN` vào
5. Điền `taiKhoan.google.customerId` trong `luat.json` (10 chữ số, bỏ dấu gạch)

> 💡 Meta chạy được trước. Đừng chờ Google mới bắt đầu — `keo.mjs` chạy một nền cũng ra kết quả, nền còn lại chỉ báo lỗi ở dòng riêng.

---

## Cấu trúc

| | |
|---|---|
| `luat.json` | **Mọi** ngưỡng và hạn mức. Sửa hành vi agent = sửa file này, không sửa code. |
| `lib/chan.mjs` | Lớp chặn. Hàm thuần, không mạng không file. 16 ca test trong `kiem.mjs`. |
| `lib/so.mjs` | Chấm điểm. Thuần số học — cùng bảng số phải ra cùng kết luận, mọi lần. |
| `lib/meta.mjs` · `lib/google.mjs` | Gọi API. Ba hàm cuối mỗi file là ba chỗ duy nhất chạm được vào tiền. |
| `nhat-ky.jsonl` | Append-only. Mỗi hành động ghi một dòng — kể cả ca hỏng và ca bị chặn. |
| `.khoa/` | Khoá. Đã bị `.gitignore` chặn. Repo có cron tự commit, lọt một lần là vĩnh viễn. |
| `du-lieu/` · `de-xuat/` | Ảnh chụp số liệu và đề xuất theo ngày. Không vào git. |

## Ba thứ agent này CỐ Ý không làm

Ghi ra để một phiên AI khác không "tốt bụng" đề xuất mọc lại — theo nguyên tắc 4 ở `../wiki/agent-harness-design.md`.

1. **Không tự tạo chiến dịch / nhóm / quảng cáo mới.** Chỉ tắt, bật, và dịch ngân sách trên thứ đã có. Tạo mới là việc của người — nó cần một phán đoán chiến lược mà `lib/so.mjs` không có đầu vào để làm.
2. **Không tự đổi nội dung quảng cáo hay trang đích.** Viết chữ đăng ra ngoài đi qua skill `/viet-content`, có Đoàn duyệt. Không nối thẳng vào đây.
3. **Không tự chạy `ap.mjs` theo lịch.** `keo` và `soi` hẹn giờ được. `ap` chỉ chạy khi Đoàn gõ lệnh. Bỏ luật này là bỏ người gác cuối cùng.
