# 🎬 Kịch bản video — `kich-ban-ngan` và `kich-ban-dai`

> ⚠️ **File này là chỗ DUY NHẤT chứa luật kịch bản video.** Cần sửa luật kịch bản thì sửa ở đây, đừng chép sang chỗ khác — luật bị chép hai bản là luật sẽ trôi lệch.

### Luật chung — áp cho CẢ ngắn lẫn dài

1. **Kịch bản là lời NÓI, không phải bài viết đọc lên.** Đọc to bản nháp lên; chỗ nào hụt hơi là chỗ phải cắt. Vì thế `wiki/voice-profile.md` là bắt buộc ở hai việc này — và trong đó hãy tách rõ **giọng nói chuyện / dạy học** với **giọng viết bài**. Hai giọng khác nhau, đừng dùng thay nhau.
2. **Xuất ra bảng 3 cột**, theo khuôn: `Thời gian | Lời thoại | Hình ảnh/Cue`. Không xuất văn xuôi rồi bảo bạn tự chia.
3. **Cột "Hình ảnh/Cue" chỉ được ghi thứ quay được bằng nguồn lực thật** — xem mục *Nguồn lực sản xuất* ngay dưới. Đây là chỗ dễ bịa nhất.
4. **Hook vẫn theo `luat/hook.md`.** Hook là câu **đầu tiên nói ra**, không phải tiêu đề dán lên video.
5. Bước 0 (cấm bịa), Bước 1 (chốt tầng), Bước 3 (chọn chuyện có thật), Bước 5 (tự soi) **áp đủ như bài viết**. Kịch bản không phải ngoại lệ của bất kỳ luật nào.
6. **Bắt buộc ghi ra mạch đã dùng** ở dòng đầu mục `## Kịch bản`, dạng:
   `> Mạch: ngắn — hook · đồng cảm · căng thẳng · CTA` hoặc `> Mạch: dài 3P — 5 chương`.
   Cùng lý do với `> Khung:` ở Bước 3b: không ghi thì sau này không ai trả lời được *"mạch nào đang thắng"*, nhìn câu chữ đoán ngược chỉ là đoán.

### Khác nhau — đúng bảng này, không hơn

| | `kich-ban-ngan` | `kich-ban-dai` |
|---|---|---|
| Khung hình | dọc **9:16** | ngang **16:9** |
| Thời lượng | 30–90 giây | 8–15 phút (webinar dài hơn) |
| Mạch | **7 phân cảnh cảm xúc** | **3P** |
| Hook | 1–3 giây đầu | 15 giây đầu = Promise + Plan + **một Proof trực quan** (B-roll kết quả cuối) |
| CTA | một cái, cuối, thường `comment "[TỪ KHOÁ]"` | **rải có chiến lược, KHÔNG dồn cuối** |
| Trang đọc riêng | `wiki/teachings/` của bạn *(nếu đã dựng)* | `wiki/learnings/` của bạn *(nếu đã dựng)* |

**Mạch ngắn — 7 phân cảnh:** hook · đồng cảm · căng thẳng · tò mò · dứt khoát · hào hứng · CTA comment. Nguồn: `wiki/teachings/` của bạn *(nếu đã dựng)* (Khải bóc tách từ ~1.000 video viral đã quét).
⚠️ **Không bắt buộc đủ 7** — chỉ dùng phân cảnh nào hợp, giữ đúng **thứ tự nhịp**. Ép đủ 7 vào video 45 giây thì mỗi phân cảnh còn 6 giây, không cái nào kịp chạm.

**Mạch dài — 3P:** **Promise** (người xem nhận được gì, nói ngay đầu) · **Proof** (số liệu, chuyện cá nhân, testimonial, case — để không thành clickbait) · **Plan** (bản đồ nội dung kiểu "5 bước", để người xem không lạc). Nguồn: `wiki/learnings/` của bạn *(nếu đã dựng)* §2.
Video dài phải **chia chương và đặt tên chương**, vì nó còn là nguyên liệu cắt lại — *"một video dài cắt 10 mảnh"* (cùng file, §3). Chương không rõ thì không cắt được.

### Nguồn lực sản xuất — chỗ dễ bịa nhất trong cả xưởng

Đọc theo đúng thứ tự, dừng ở chỗ đầu tiên có dữ liệu:

1. **`wiki/video-production-setup.md`** — ⚡ **BẮT BUỘC ĐỌC nếu bạn đã dựng trang này.** Nó ghi nguồn lực quay thật của bạn: máy quay · mic · ổn định hình · đèn · bối cảnh · nhân vật · B-roll · hậu kỳ. **Chưa có trang này thì HỎI, đừng suy ra thiết bị** — rồi đề nghị nạp câu trả lời vào bộ não qua `/nap-kho`.
2. **Ô "Nguồn lực quay lần này"** (`nguonLuc`) trong `brief.md` — chỉ dùng để **ghi đè** cho lượt này (hôm nay có người cầm máy, hôm nay quay chỗ khác…). Trống là bình thường, nghĩa là dùng bản mặc định ở trang trên.
3. Thứ nào **cả hai đều không có** → ghi `[cần bổ sung: ...]`.

**Bốn ràng buộc từ trang đó chi phối mạnh nhất — thuộc trước khi viết shot nào:**

| | |
|---|---|
| **Quay một mình** | Mọi shot phải tự đặt máy rồi vào khung. Không có shot cần người thứ hai điều khiển máy. |
| **Gimbal RS4 Mini coi như KHÔNG CÓ** | Có trong nhà nhưng *"rất ít dùng vì 1 mình"*. Shot động mượt: chỉ Pocket 3. Shot đi theo nhân vật: không có. |
| **Mặc định MỘT góc máy** | Có ba máy không nghĩa là quay ba góc. Không ghi "cắt sang góc 2" trừ khi brief nói rõ có dùng Pocket 3. |
| **Hậu kỳ đơn giản** | Cắt ghép + phụ đề chữ chạy + hiệu ứng đơn giản. Không đề xuất motion graphic, animation, đồ hoạ 3D. |

Cộng một dòng bắt buộc mở đầu shotlist: **"dọn hậu cảnh trước khi quay"** — phòng không ở trạng thái quay được ngay.

🚫 **Tuyệt đối không suy ra thiết bị.** Không được viết "quay bằng iPhone" vì *"chắc ai cũng có iPhone"*. `video-production-brief-worksheet.md` nói thẳng cái giá: gợi ý dolly shot khi không có gimbal, gợi ý 2 máy phỏng vấn khi chỉ có 1 người quay — ra một bản lý thuyết **không quay được**, mà đọc thì vẫn rất xuôi tai.

Ba mục trong trang đó **cố ý còn trống** (kho B-roll nằm ở đâu · thời gian quay mỗi buổi · trang phục/nhận diện). Gặp thì ghi `[cần bổ sung: ...]` và nêu ở *"Đề xuất cho bộ não"* — **đừng đoán, và đừng coi trang đã nạp là đã đầy đủ.**

### Shotlist — chỉ chạy khi brief bật

**Chạy khi** `brief.md` có `shotlist: co`. Không có dòng đó → **bỏ hẳn**, đừng làm cho đủ.

Xuất bảng **7 cột** theo khuôn:

`Shot # | Cảnh quay | Góc máy | Thiết bị | Âm thanh | Diễn xuất/Ghi chú | Thời lượng dự kiến`

Ghi vào mục riêng `## Shotlist`, đặt **ngay sau** `## Kịch bản`.

⚠️ Giữ đúng tên mục `## Kịch bản`. `## Shotlist` là mục phụ — **không được thay thế nó**.

Ba luật của shotlist:

1. **Mỗi shot phải nằm trong nguồn lực đã khai.** Không có gimbal thì không có shot chuyển động mượt. Không có người cầm máy thì không có shot đi theo nhân vật.
2. **Cột Thiết bị ghi tên thật**, không ghi chữ chung chung "máy quay". Không biết tên thật → `[cần bổ sung: tên máy]`.
3. **Tổng thời lượng các shot phải khớp thời lượng mục tiêu.** Lệch thì nói thẳng ra trong `ket-qua.md`, đừng để bạn tự cộng lại mới phát hiện.
