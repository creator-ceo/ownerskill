#!/usr/bin/env node
// Lấy GOOGLE_REFRESH_TOKEN một lần duy nhất. Chạy: node ads/xin-khoa-google.mjs
// Cần có sẵn GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET trong ads/.khoa/that.env
// (tạo OAuth client loại "Desktop app" ở console.cloud.google.com → Credentials).
import { createServer } from 'node:http'
import { docKhoa } from './lib/cau-hinh.mjs'

const k = docKhoa()
const thieu = ['GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET'].filter(x => !k[x])
if (thieu.length) { console.log(`⛔ Thiếu ${thieu.join(', ')} trong ads/.khoa/that.env`); process.exit(1) }

const CONG = 8765
const CHUYEN_VE = `http://127.0.0.1:${CONG}`
const url = new URL('https://accounts.google.com/o/oauth2/v2/auth')
url.search = new URLSearchParams({
  client_id: k.GOOGLE_CLIENT_ID,
  redirect_uri: CHUYEN_VE,
  response_type: 'code',
  scope: 'https://www.googleapis.com/auth/adwords',
  access_type: 'offline',
  prompt: 'consent'   // bắt buộc, thiếu là Google KHÔNG trả refresh_token ở lần cấp thứ hai
}).toString()

console.log('\n1. Thêm đúng dòng này vào "Authorized redirect URIs" của OAuth client:')
console.log(`   ${CHUYEN_VE}`)
console.log('\n2. Mở link sau trong trình duyệt, đăng nhập tài khoản QUẢN TRỊ Google Ads:\n')
console.log(url.toString())
console.log(`\n3. Đang chờ ở ${CHUYEN_VE} ... (Ctrl+C để huỷ)\n`)

const may = createServer(async (req, res) => {
  const q = new URL(req.url, CHUYEN_VE).searchParams
  const ma = q.get('code')
  const loi = q.get('error')
  const tra = s => { res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); res.end(`<meta charset=utf-8><body style="font:16px/1.6 system-ui;padding:3rem">${s}</body>`) }

  if (loi) { tra(`❌ Google trả lỗi: ${loi}`); console.log(`⛔ ${loi}`); may.close(); process.exit(1) }
  if (!ma) { tra('Đang chờ...'); return }

  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code: ma, client_id: k.GOOGLE_CLIENT_ID, client_secret: k.GOOGLE_CLIENT_SECRET,
      redirect_uri: CHUYEN_VE, grant_type: 'authorization_code'
    })
  })
  const j = await r.json()
  if (!j.refresh_token) {
    tra('❌ Google không trả refresh_token. Vào myaccount.google.com/permissions gỡ quyền của app này rồi chạy lại.')
    console.log('⛔ Không có refresh_token:', JSON.stringify(j))
    may.close(); process.exit(1)
  }
  tra('✅ Xong. Quay lại cửa sổ dòng lệnh — token đã in ở đó.')
  console.log('✅ Chép đúng dòng dưới đây vào ads/.khoa/that.env:\n')
  console.log(`GOOGLE_REFRESH_TOKEN=${j.refresh_token}\n`)
  console.log('⚠️  Token này mở được tài khoản quảng cáo. Đừng dán nó vào chat, vào Notion, hay vào bất kỳ file nào ngoài .khoa/')
  may.close(); process.exit(0)
})
may.listen(CONG, '127.0.0.1')
