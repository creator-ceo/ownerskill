#!/usr/bin/env bash
# Soi an toàn một thư mục skill trước khi tin nó.
#
#   ./scripts/soi-an-toan.sh [đường-dẫn]     (mặc định: cả repo)
#
# Skill là VĂN BẢN RA LỆNH CHO AI, chạy trong phiên có quyền đọc file và chạy lệnh.
# Cài skill lạ = để người khác viết chỉ thị cho con AI đang ngồi trong máy bạn.
# Script này soi 6 nhóm rủi ro. Nó KHÔNG thay được việc đọc, nhưng khoanh vùng chỗ phải đọc.
#
# Mã thoát: 0 = sạch · 1 = có chỗ phải xem tận mắt
set -uo pipefail

GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DICH="${1:-$GOC}"
[ -d "$DICH" ] || { echo "❌ không có thư mục: $DICH"; exit 1; }

co_van_de=0
muc() { printf '\n\033[1m%s\033[0m\n' "$1"; }
sach() { printf '   ✅ %s\n' "$1"; }
ngo()  { printf '   ⚠️  %s\n' "$1"; co_van_de=1; }

echo "🔎 Soi an toàn: $DICH"

# ── 1. File chạy được ──────────────────────────────────────────
muc "1. File chạy được (skill lành chỉ cần .md)"
n=$(find "$DICH" -type f \( -name "*.sh" -o -name "*.py" -o -name "*.mjs" -o -name "*.js" \
    -o -name "*.rb" -o -name "*.pl" -o -name "*.php" \) 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -eq 0 ]; then sach "không có file chạy được"
else ngo "$n file chạy được — ĐỌC TỪNG CÁI:"
     find "$DICH" -type f \( -name "*.sh" -o -name "*.py" -o -name "*.mjs" -o -name "*.js" \) | sed 's|^|      |'
fi

# ── 2. Hook / MCP / LSP — thứ TỰ CHẠY, nguy nhất ───────────────
muc "2. Hook · MCP · LSP (tự chạy, không cần bạn gõ gì)"
h=$(find "$DICH" \( -name "hooks.json" -o -name ".mcp.json" -o -name "*.lsp.json" \) 2>/dev/null)
if [ -z "$h" ]; then sach "không có hook, không có MCP server"
else ngo "CÓ cấu hình tự chạy — đọc kỹ trước khi cài:"; echo "$h" | sed 's|^|      |'; fi

# ── 3. Lệnh phá hoại / leo quyền ───────────────────────────────
muc "3. Lệnh phá hoại · leo quyền · tải-rồi-chạy"
r=$(grep -rnoE "(rm -rf [~/\*]|sudo |chmod 777|eval \(|base64 -d|curl [^|]*\| *(ba)?sh|wget [^|]*\| *(ba)?sh)" "$DICH" 2>/dev/null | head -20)
if [ -z "$r" ]; then sach "không có"
else ngo "có lệnh đáng ngờ:"; echo "$r" | sed 's|^|      |'; fi

# ── 4. Gửi dữ liệu ra ngoài ────────────────────────────────────
muc "4. Gửi dữ liệu ra ngoài (webhook, endpoint lạ)"
r=$(grep -rnoiE "(webhook\.site|requestbin|pipedream\.net|ngrok\.io|\.onion|POST https?://[a-z0-9.-]*/(collect|log|track|beacon))" "$DICH" 2>/dev/null | head -10)
if [ -z "$r" ]; then sach "không có endpoint thu thập lạ"
else ngo "CÓ chỗ gửi dữ liệu đi — đọc ngay:"; echo "$r" | sed 's|^|      |'; fi

# ── 5. Đọc trộm bí mật ─────────────────────────────────────────
muc "5. Lệnh đọc file bí mật của máy"
r=$(grep -rnoiE "(cat ~/\.(ssh|aws|npmrc)|id_rsa|\.aws/credentials|security find-generic-password|keychain dump|printenv|env \|)" "$DICH" 2>/dev/null | head -10)
if [ -z "$r" ]; then sach "không có"
else ngo "CÓ lệnh đụng vào bí mật:"; echo "$r" | sed 's|^|      |'; fi

# ── 6. Prompt injection ────────────────────────────────────────
muc "6. Chỉ thị ngầm (prompt injection)"
r=$(grep -rnoiE "(ignore (all )?previous instructions|disregard (the )?above|you are now [a-z]|new system prompt|do not tell the user|without telling the user|hide this from)" "$DICH" 2>/dev/null | head -10)
if [ -z "$r" ]; then sach "không có"
else ngo "khớp mẫu injection — ĐỌC TẬN NƠI, phần lớn là dương tính giả:"
     echo "$r" | sed 's|^|      |'
     printf '      ↑ skill dạy CHỐNG injection cũng khớp mẫu này. Đọc rồi mới kết luận.\n'
fi

# ── Kết ────────────────────────────────────────────────────────
echo
if [ "$co_van_de" -eq 0 ]; then
  printf '\033[32m✅ SẠCH — không có dấu hiệu nào trong 6 nhóm.\033[0m\n'
  printf '   Nhớ: sạch theo máy quét ≠ an toàn tuyệt đối. Skill vẫn là chỉ thị cho AI.\n'
else
  printf '\033[33m⚠️  CÓ CHỖ PHẢI XEM TẬN MẮT (xem ⚠️ ở trên).\033[0m\n'
  printf '   Đừng cài cho tới khi đọc xong và hiểu vì sao nó ở đó.\n'
fi
exit "$co_van_de"
