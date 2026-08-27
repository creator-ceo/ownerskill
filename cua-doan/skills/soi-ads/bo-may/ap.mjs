#!/usr/bin/env node
// Áp đề xuất vào tài khoản quảng cáo. ĐÂY LÀ FILE DUY NHẤT TIÊU ĐƯỢC TIỀN.
//
//   node ads/ap.mjs                          THỬ KHAN — soi qua lớp chặn, không ghi gì
//   node ads/ap.mjs --that --toi-dong-y      ghi thật
//
// Vì sao phải hai cờ chứ không một: `--that` một mình quá dễ gõ nhầm, quá dễ lọt
// vào một script tự động nào đó. Cờ thứ hai không thêm an toàn kỹ thuật nào —
// nó thêm một khoảnh khắc để người gõ kịp nghĩ. Đó là mục đích duy nhất của nó.
import { readFileSync, readdirSync, existsSync } from 'node:fs'
import { join } from 'node:path'
import { GOC, docLuat, gioVn, ngayVn, vnd, oConTrong } from './lib/cau-hinh.mjs'
import { soi as soiChan, inKetQua } from './lib/chan.mjs'
import { ghi as ghiNhatKy, daDoiHomNay } from './lib/nhat-ky.mjs'

const co = process.argv.slice(2)
const gia = co.includes('--gia')
const that = co.includes('--that') && co.includes('--toi-dong-y')
const doiGhi = co.includes('--that') && !co.includes('--toi-dong-y')

if (gia && co.includes('--that')) {
  console.log('⛔ `--gia` và `--that` chỏi nhau: dữ liệu giả trỏ tới ID không có thật.')
  process.exit(1)
}
if (doiGhi) {
  console.log('⛔ Có `--that` nhưng thiếu `--toi-dong-y`. Hai cờ, cố ý.\n   node ads/ap.mjs --that --toi-dong-y')
  process.exit(1)
}

const thuMuc = join(GOC, 'de-xuat')
if (!existsSync(thuMuc)) { console.log('Chưa có đề xuất. Chạy: node ads/soi.mjs' + (gia ? ' --gia' : '')); process.exit(1) }
const ten = readdirSync(thuMuc).filter(f => f.endsWith('.json') && f.includes('-gia') === gia).sort().pop()
if (!ten) { console.log(`Chưa có đề xuất ${gia ? 'giả' : 'thật'}. Chạy: node ads/soi.mjs${gia ? ' --gia' : ''}`); process.exit(1) }

const dx = JSON.parse(readFileSync(join(thuMuc, ten), 'utf8'))
const luat = docLuat()

// Ở chế độ giả, mượn bộ giới hạn mẫu để soi được lớp chặn khi luat.json còn trống.
const GIOI_HAN_MAU = {
  chiTieuNgayToiDaVnd: { meta: 2_000_000, google: 1_000_000 },
  tongChiTieuNgayToiDaVnd: 2_500_000,
  nganSachSanToiThieuVnd: 100_000, nganSachSanToiDaVnd: 800_000,
  chiTieuToiThieuTruocKhiKetVnd: 300_000
}
const luatDung = gia ? { ...luat, gioiHanCung: { ...luat.gioiHanCung, ...GIOI_HAN_MAU } } : luat

if (!gia) {
  const trong = oConTrong({ gioiHanCung: luatDung.gioiHanCung })
  if (trong.length) {
    console.log('⛔ luat.json còn ô chưa điền — agent bị khoá, không ghi được gì:')
    for (const o of trong) console.log(`   · ${o}`)
    process.exit(1)
  }
}

const ketQua = soiChan(dx.hanhDong, {
  luat: luatDung,
  gioHienTai: gioVn(),
  chiTieuNgayTheoNen: dx.chiTieuNgayTheoNen || {},
  daDoiHomNayVnd: daDoiHomNay(ngayVn())
})

console.log(`📄 ${ten} · ${dx.hanhDong.length} đề xuất${gia ? '  ⚠️ CHẾ ĐỘ GIẢ + giới hạn mẫu' : ''}\n`)
console.log(inKetQua(ketQua))

if (!that) {
  console.log(`\n🧪 THỬ KHAN — chưa ghi gì vào tài khoản.`)
  if (ketQua.dat.length && !gia) console.log(`   Muốn ghi thật: node ads/ap.mjs --that --toi-dong-y`)
  if (gia) console.log(`   Chế độ giả không ghi thật được (ID không có thật). Đây là bài thử lớp chặn.`)
  process.exit(0)
}

if (!ketQua.dat.length) { console.log('\nKhông có hành động nào qua chặn. Dừng.'); process.exit(0) }

const meta = await import('./lib/meta.mjs')
const google = await import('./lib/google.mjs')
const tienTe = 'VND'
let xong = 0, hong = 0

console.log('\n── GHI THẬT ──')
for (const h of ketQua.dat) {
  const muc = {
    ngay: ngayVn(), nen: h.nen, kieu: h.kieu, id: h.id, ten: h.ten, vi: h.vi,
    nganSachCu: h.nganSachCu ?? null, nganSachMoi: h.nganSachMoi ?? null,
    chenhNganSachVnd: h.nganSachMoi != null ? h.nganSachMoi - h.nganSachCu : null
  }
  try {
    if (h.nen === 'meta') {
      if (h.kieu === 'tam_dung_quang_cao') await meta.doiTrangThaiQuangCao(h.id, 'PAUSED')
      else if (h.kieu === 'bat_lai_quang_cao') await meta.doiTrangThaiQuangCao(h.id, 'ACTIVE')
      else if (h.kieu === 'tam_dung_nhom_quang_cao') await meta.doiTrangThaiNhom(h.id, 'PAUSED')
      else await meta.doiNganSachNgay(h.id, h.nganSachMoi, tienTe)
    } else {
      if (h.kieu === 'tam_dung_quang_cao') await google.doiTrangThaiQuangCao(h.tenTaiNguyen, 'PAUSED')
      else if (h.kieu === 'bat_lai_quang_cao') await google.doiTrangThaiQuangCao(h.tenTaiNguyen, 'ENABLED')
      else await google.doiNganSachNgay(h.tenTaiNguyen, h.nganSachMoi)
    }
    ghiNhatKy({ ...muc, ket: 'da_ghi' })
    xong++
    console.log(`   ✅ ${h.kieu} · ${h.ten}${h.nganSachMoi ? ` → ${vnd(h.nganSachMoi)}` : ''}`)
  } catch (e) {
    // Ghi log cả ca HỎNG. Không có dòng này thì một lỗi giữa chừng biến mất không dấu vết,
    // và lần sau không ai biết tài khoản đang ở trạng thái nào.
    ghiNhatKy({ ...muc, ket: 'hong', loi: e.message })
    hong++
    console.log(`   ❌ ${h.kieu} · ${h.ten} — ${e.message}`)
  }
}

for (const h of ketQua.chan) ghiNhatKy({ ngay: ngayVn(), nen: h.nen, kieu: h.kieu, id: h.id, ten: h.ten, ket: 'bi_chan', viPham: h.viPham })

console.log(`\n${xong} xong · ${hong} hỏng · ${ketQua.chan.length} bị chặn — nhật ký: ads/nhat-ky.jsonl`)
if (hong) process.exit(1)
