#!/usr/bin/env node
// Dựng ảnh quote: kiểu (HTML) + nội dung (JSON) -> PNG, bằng Chrome có sẵn trên máy.
//
//   node dung.mjs --kieu <file.html> --noi-dung <file.json> --ra <file.png> [--kho 1080x1350] [--scale 2]
//
// Không cần npm install, không gọi mạng. Font nhúng từ ./fonts nên máy nào chạy cũng ra ảnh y hệt.
//
// Vì sao điều khiển Chrome qua giao thức DevTools chứ không dùng cờ --screenshot cho gọn:
// đã thử cờ đó, Chrome chụp xong ảnh rồi TREO không thoát (đo được: bị giết ở giây 25,
// mã thoát 142, ảnh vẫn ra). Ngoài ra cờ --screenshot chụp theo đồng hồ, không biết chữ
// đã co xong hay chưa — câu dài sẽ ra ảnh chữ tràn khung mà không ai báo. Đi qua DevTools
// thì chụp đúng lúc trang báo "đã xong", và bắt được cả lỗi JS trong template.

import { readFileSync, writeFileSync, mkdirSync, existsSync, rmSync, statSync } from 'node:fs'
import { spawn } from 'node:child_process'
import { dirname, resolve, basename } from 'node:path'
import { fileURLToPath } from 'node:url'
import { tmpdir } from 'node:os'

const THU_MUC_SKILL = dirname(fileURLToPath(import.meta.url))

const CHROME_CO_THE_O = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
]

function timChrome() {
  const co = CHROME_CO_THE_O.find((p) => existsSync(p))
  if (!co) {
    throw new Error(
      'Không tìm thấy Chrome/Chromium/Edge/Brave trên máy. Skill này chụp ảnh bằng trình duyệt có sẵn — ' +
        'cần ít nhất một trong: ' + CHROME_CO_THE_O.join(' · ')
    )
  }
  return co
}

function docThamSo(argv) {
  const ts = {}
  for (let i = 0; i < argv.length; i += 2) {
    if (!argv[i].startsWith('--')) throw new Error(`Tham số sai ở "${argv[i]}" — phải theo cặp --ten giatri`)
    ts[argv[i].slice(2)] = argv[i + 1]
  }
  return ts
}

const ts = docThamSo(process.argv.slice(2))
if (!ts.kieu || !ts.ra) {
  console.error(`Thiếu tham số.

  node dung.mjs --kieu <file.html> --ra <file.png> [--noi-dung <file.json>] [--kho 1080x1350] [--scale 2]

  --kieu      file HTML của kiểu ảnh (trong anh-quote/kieu/)
  --noi-dung  file JSON chứa câu chữ; bỏ qua thì dùng nội dung mặc định ghi sẵn trong file kiểu
  --ra        đường dẫn file PNG xuất ra
  --kho       khổ ảnh, mặc định 1080x1350 (4:5)
  --scale     bội số điểm ảnh, mặc định 2 (ảnh ra 2160x2700, nét trên màn retina)`)
  process.exit(1)
}

const [rong, cao] = (ts.kho || '1080x1350').split('x').map(Number)
if (!rong || !cao) throw new Error(`--kho sai định dạng: "${ts.kho}" — phải dạng 1080x1350`)
const scale = Number(ts.scale || 2)

const duongDanKieu = resolve(ts.kieu)
const duongDanRa = resolve(ts.ra)
let html = readFileSync(duongDanKieu, 'utf8')

// ── 1. Đổ nội dung mới vào khối JSON của file kiểu ──────────────────────────
if (ts['noi-dung']) {
  const duongDanNoiDung = resolve(ts['noi-dung'])
  const noiDung = JSON.parse(readFileSync(duongDanNoiDung, 'utf8'))
  const khoiJson = /<script type="application\/json" id="noi-dung">[\s\S]*?<\/script>/
  if (!khoiJson.test(html)) {
    throw new Error(
      `File kiểu "${basename(duongDanKieu)}" không có khối <script type="application/json" id="noi-dung">. ` +
        'Mọi file kiểu bắt buộc phải có khối này — xem khung.html.'
    )
  }
  html = html.replace(
    khoiJson,
    `<script type="application/json" id="noi-dung">\n${JSON.stringify(noiDung, null, 2)}\n</script>`
  )

  // Ảnh nền của sếp: đổi sang đường dẫn tuyệt đối để Chrome đọc được dù HTML nằm ở đâu.
  // Tìm ở nhiều gốc vì file nội dung có thể nằm ở thư mục lượt chạy, ở /tmp, hay bất kỳ
  // đâu — bắt sếp đếm cho đúng số dấu ../ là kiểu lỗi vặt làm nản người dùng.
  if (noiDung.anhNen) {
    const cacGoc = [
      dirname(duongDanNoiDung),        // cạnh file nội dung
      resolve(dirname(duongDanKieu), '..'), // gốc anh-quote/
      process.cwd(),
    ]
    const duongDanAnh = cacGoc.map((g) => resolve(g, noiDung.anhNen)).find(existsSync)
    if (!duongDanAnh) {
      throw new Error(
        `Không thấy ảnh nền "${noiDung.anhNen}". Đã tìm ở:\n` +
          cacGoc.map((g) => `  · ${resolve(g, noiDung.anhNen)}`).join('\n')
      )
    }
    html = html.replace(/__ANH_NEN__/g, `file://${encodeURI(duongDanAnh)}`)
  }
}

// Kiểu tự khai "tôi cần ảnh nền" bằng thẻ meta. Không suy từ việc file có chuỗi
// __ANH_NEN__ hay không — chuỗi đó nằm trong JS của MỌI kiểu nên suy kiểu ấy luôn sai.
const canAnhNen = /<meta name="can-anh-nen" content="co"\s*\/?>/.test(html)
if (canAnhNen && html.includes('__ANH_NEN__')) {
  throw new Error(
    `Kiểu "${basename(duongDanKieu)}" bắt buộc phải có ảnh nền, nhưng file nội dung không có trường "anhNen". ` +
      'Thêm "anhNen": "../nen/ten-file.jpg" vào JSON, hoặc chọn kiểu không dùng ảnh nền.'
  )
}

// ── 2. Trỏ font về thư mục fonts của skill (tuyệt đối) ──────────────────────
html = html.replace(/__THU_MUC_FONT__/g, `file://${encodeURI(THU_MUC_SKILL)}/fonts`)

// ── 3. Ghi file HTML đã dựng cạnh ảnh — để còn mở ra xem/sửa tay khi cần ────
mkdirSync(dirname(duongDanRa), { recursive: true })
const duongDanHtml = duongDanRa.replace(/\.png$/i, '.html')
writeFileSync(duongDanHtml, html)

// ── 4. Chụp qua giao thức DevTools ──────────────────────────────────────────
const hoSoTam = `${tmpdir()}/anh-quote-chrome-${process.pid}`
const chrome = spawn(
  timChrome(),
  [
    '--headless',
    '--disable-gpu',
    '--hide-scrollbars',
    '--no-first-run',
    '--no-default-browser-check',
    '--remote-debugging-port=0', // để Chrome tự chọn cổng trống, không đụng cổng đang dùng
    `--user-data-dir=${hoSoTam}`, // hồ sơ riêng, không đụng vào Chrome sếp đang mở
    'about:blank',
  ],
  { stdio: ['ignore', 'ignore', 'pipe'] }
)

const donDep = () => {
  try { chrome.kill() } catch {}
  rmSync(hoSoTam, { recursive: true, force: true })
}
process.on('exit', donDep)

// Chrome in dòng "DevTools listening on ws://..." ra stderr — đó là cách duy nhất
// biết cổng nó vừa tự chọn.
const diaChiWs = await new Promise((ok, loi) => {
  let dem = ''
  const hetGio = setTimeout(() => loi(new Error('Chrome không mở được cổng DevTools sau 20 giây.')), 20000)
  chrome.stderr.on('data', (b) => {
    dem += b.toString()
    const m = dem.match(/DevTools listening on (ws:\/\/\S+)/)
    if (m) { clearTimeout(hetGio); ok(m[1]) }
  })
  chrome.on('exit', (ma) => { clearTimeout(hetGio); loi(new Error(`Chrome thoát sớm (mã ${ma}):\n${dem}`)) })
})

const ws = new WebSocket(diaChiWs)
await new Promise((ok, loi) => { ws.onopen = ok; ws.onerror = () => loi(new Error('Không nối được vào Chrome.')) })

let soThuTu = 0
const dangCho = new Map()
const suKien = new Map()
ws.onmessage = (e) => {
  const tin = JSON.parse(e.data)
  if (tin.id && dangCho.has(tin.id)) {
    const { ok, loi } = dangCho.get(tin.id)
    dangCho.delete(tin.id)
    tin.error ? loi(new Error(`${tin.error.message}`)) : ok(tin.result)
  } else if (tin.method && suKien.has(tin.method)) {
    suKien.get(tin.method)(tin.params)
    suKien.delete(tin.method)
  }
}
const goi = (method, params = {}) =>
  new Promise((ok, loi) => {
    const id = ++soThuTu
    dangCho.set(id, { ok, loi })
    ws.send(JSON.stringify({ id, method, params }))
  })
const doiSuKien = (method, giay = 20) =>
  new Promise((ok, loi) => {
    const hetGio = setTimeout(() => loi(new Error(`Chờ ${method} quá ${giay} giây.`)), giay * 1000)
    suKien.set(method, (p) => { clearTimeout(hetGio); ok(p) })
  })

// Mở một tab mới rồi bám vào nó
const { targetId } = await goi('Target.createTarget', { url: 'about:blank' })
const { sessionId } = await goi('Target.attachToTarget', { targetId, flatten: true })
const goiTab = (method, params = {}) =>
  new Promise((ok, loi) => {
    const id = ++soThuTu
    dangCho.set(id, { ok, loi })
    ws.send(JSON.stringify({ id, method, params, sessionId }))
  })

await goiTab('Page.enable')
await goiTab('Runtime.enable')

// Khổ ảnh đặt bằng viewport ảo, không phụ thuộc cửa sổ thật -> ảnh luôn đúng kích thước
await goiTab('Emulation.setDeviceMetricsOverride', {
  width: rong, height: cao, deviceScaleFactor: 1, mobile: false,
})

const loiJs = []
ws.addEventListener('message', (e) => {
  const tin = JSON.parse(e.data)
  if (tin.method === 'Runtime.exceptionThrown') {
    loiJs.push(tin.params.exceptionDetails?.exception?.description || tin.params.exceptionDetails?.text)
  }
})

const daTai = doiSuKien('Page.loadEventFired')
await goiTab('Page.navigate', { url: `file://${encodeURI(duongDanHtml)}` })
await daTai

// Điểm mấu chốt: chờ đúng lời hứa "đã co chữ xong" của template, không chờ theo đồng hồ.
const ketQua = await goiTab('Runtime.evaluate', {
  expression: '(window.saMSanSang || Promise.resolve()).then(() => "xong")',
  awaitPromise: true,
  returnByValue: true,
})
if (ketQua.exceptionDetails) {
  throw new Error(`Template lỗi khi dựng chữ: ${ketQua.exceptionDetails.exception?.description}`)
}

const { data } = await goiTab('Page.captureScreenshot', {
  format: 'png',
  captureBeyondViewport: false,
  clip: { x: 0, y: 0, width: rong, height: cao, scale },
})
writeFileSync(duongDanRa, Buffer.from(data, 'base64'))

ws.close()
donDep()

if (loiJs.length) {
  console.warn(`⚠ Template có lỗi JS (ảnh vẫn ra nhưng có thể sai):\n  ${loiJs.join('\n  ')}`)
}
if (!existsSync(duongDanRa)) throw new Error('Chụp xong nhưng không thấy file ảnh.')
const kb = Math.round(statSync(duongDanRa).size / 1024)
console.log(`✓ ${duongDanRa}`)
console.log(`  ${rong * scale}×${cao * scale} px (khổ ${rong}×${cao} @${scale}x) · ${kb} KB`)
console.log(`  bản HTML để sửa tay: ${duongDanHtml}`)
process.exit(0)
