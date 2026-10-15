# Bộ máy quảng cáo — luật của thư mục này

Thư mục này là **bộ máy** của skill `$soi-ads`: một bộ script Node kéo số liệu Meta Ads + Google Ads về, chấm từng quảng cáo, đề xuất hành động, và **được phép tự ghi vào tài khoản quảng cáo trong hạn mức cứng**.

Nó chạy code và gọi API thật. Skill `$soi-ads` là phần "đọc số và nói bằng tiếng người"; thư mục này là phần "đo và áp".

## Trước khi viết bất kỳ nội dung quảng cáo nào, đọc từ bộ não của bạn

| Trang | Vì sao cần |
|---|---|
| `wiki/target-customer.md` | Quyết định nhắm ai, nói gì |
| `wiki/voice-profile.md` | Giọng. Bắt buộc đọc trước khi viết chữ đăng ra ngoài |
| `wiki/offer-ladder.md` | Quảng cáo dẫn tới đâu trong bậc thang. Hứa lệch bậc là hỏng cả phễu |
| `wiki/objections-library.md` *(nếu đã dựng)* | Kho phản đối — nguyên liệu trực tiếp cho câu chốt |
| `wiki/business-metrics.md` *(nếu đã dựng)* | Giá bán, tỷ lệ chốt. Đây là chỗ suy ra **CPL mục tiêu** |

⚠️ Trang nào bạn chưa có thì **hỏi**, đừng suy. Nhất là CPL mục tiêu — xem luật 4 dưới đây.

## Bốn luật riêng của thư mục này

1. **Không đưa dữ liệu cá nhân vào repo.** Cấm ghi tên · SĐT · email của bất kỳ ai vào bất kỳ file nào ở đây. Muốn tạo Custom Audience thì tải trực tiếp từ nguồn lên Meta, **không đi vòng qua thư mục này**.

2. **Lớp chặn không được nới trong lúc chạy.** Nới hạn mức = sửa `luat.json` = một quyết định riêng, làm trước, bạn duyệt riêng. **Không bao giờ nới để một hành động đang bị chặn lọt qua.**

3. **Ngưỡng nằm trong `luat.json`, không nằm trong code.** Thêm hạn mức = thêm dòng JSON + thêm ca test trong `kiem.mjs`, không sửa `lib/chan.mjs`.

4. **Con số nào chưa biết thì để `null` và dừng.** Cấm điền một CPL mục tiêu "cho có". `lib/chan.mjs` khoá toàn bộ khi gặp `null` — đó là **tính năng**, không phải phiền toái.

## Khoá API — bạn tự điền, không ai điền hộ

Khoá nằm ở `.khoa/that.env`, file đó **bị `.gitignore` chặn** và không bao giờ được commit. Mẫu rỗng ở `.khoa/mau.env` — chép ra rồi tự điền.

⚠️ Token mở được tài khoản quảng cáo của bạn. Đừng dán nó vào chat, vào tài liệu, hay vào bất kỳ file nào ngoài `.khoa/`.

## Nếu phát sinh insight đáng đưa vào bộ não

Một ngưỡng CPL học được từ thực tế, một góc nhắm hiệu quả bất ngờ, một bài học đắt tiền — mang ngược về bộ não qua `$nap-kho`. **Không sửa thẳng file nào trong `wiki/`**: bộ não chỉ có một đường ghi.
