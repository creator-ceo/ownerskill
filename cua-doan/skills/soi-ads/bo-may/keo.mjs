#!/usr/bin/env node
// Kéo số liệu về ads/du-lieu/<ngày>.json. CHỈ ĐỌC — file này không ghi gì vào tài khoản.
//   node ads/keo.mjs            kéo 7 ngày gần nhất
//   node ads/keo.mjs --ngay 14  kéo 14 ngày
//   node ads/keo.mjs --gia      dữ liệu GIẢ, để thử đường ống khi chưa có khoá
import { writeFileSync, mkdirSync } from 'node:fs'
import { join } from 'node:path'
import { GOC, docLuat, ngayVn, vnd } from './lib/cau-hinh.mjs'

const co = process.argv.slice(2)
const soNgay = Number(co[co.indexOf('--ngay') + 1]) || 7
const gia = co.includes('--gia')

const lui = n => ngayVn(new Date(Date.now() - n * 86400_000))
const denNgay = lui(1)          // hôm qua — hôm nay chưa chốt số, lấy vào là méo trung bình
const tuNgay = lui(soNgay)

function duLieuGia () {
  // Số cố định, không random — để chạy lại ra đúng một kết quả, so sánh được.
  const mau = [
    ['meta', 'Webinar T8 — Lạnh', 'Nhóm A · 25-45 SG-HN', 'Hook "3 năm 0 đồng"', 1_680_000, 92_000, 1_150, 41, 1.4, 300_000],
    ['meta', 'Webinar T8 — Lạnh', 'Nhóm A · 25-45 SG-HN', 'Hook "Bỏ nghề"', 1_240_000, 61_000, 430, 6, 3.1, 300_000],
    ['meta', 'Webinar T8 — Lạnh', 'Nhóm B · Lookalike 1%', 'Hook "Không cần viral"', 890_000, 40_000, 520, 19, 1.1, 250_000],
    ['meta', 'Webinar T8 — Retarget 66k', 'Nhóm C · Tệp cũ', 'Nhắc lại webinar', 420_000, 18_000, 610, 24, 2.7, 200_000],
    ['meta', 'Webinar T8 — Lạnh', 'Nhóm D · Sở thích', 'Video 60s', 760_000, 55_000, 210, 0, 1.2, 250_000],
    ['google', 'Search — creator ceo', 'Nhóm thương hiệu', 'RSA thương hiệu', 540_000, 9_800, 380, 22, 0, 200_000],
    ['google', 'Search — creator ceo', 'Nhóm chung', 'RSA "xây kênh"', 1_320_000, 26_000, 340, 4, 0, 400_000]
  ]
  return mau.map(([nen, cd, nhom, qc, chiTieu, hienThi, nhap, lead, tanSuat, ns], i) => ({
    nen, chienDichId: `cd${i}`, chienDich: cd, nhomId: `nh${i}`, nhom,
    quangCaoId: `qc${i}`, quangCao: qc, chiTieu, hienThi, nhap, lead, tanSuat,
    nganSachHienTai: ns,
    tenTaiNguyenQuangCao: nen === 'google' ? `customers/0/adGroupAds/${i}` : null,
    tenTaiNguyenNganSach: nen === 'google' ? `customers/0/campaignBudgets/${i}` : null
  }))
}

/** Ghép số liệu (insights) với trạng thái/ngân sách — hai lời gọi API khác nhau. */
function ghep (soLieu, trangThai, layNganSach) {
  const tt = new Map(trangThai.map(t => [t.quangCaoId, t]))
  return soLieu.map(s => {
    const t = tt.get(s.quangCaoId) || {}
    return { ...s, trangThai: t.trangThai, nganSachHienTai: layNganSach(t),
      tenTaiNguyenQuangCao: t.tenTaiNguyenQuangCao, tenTaiNguyenNganSach: t.tenTaiNguyenNganSach }
  })
}

const loi = []
let dong = []
let tienTe = 'VND'

if (gia) {
  dong = duLieuGia()
  console.log('⚠️  CHẾ ĐỘ GIẢ — số liệu bịa để thử đường ống. Không phải số thật của sếp.')
} else {
  const luat = docLuat()
  if (luat.taiKhoan.meta.adAccountId) {
    try {
      const m = await import('./lib/meta.mjs')
      const tk = await m.thongTinTaiKhoan(); tienTe = tk.tienTe
      const [sl, tt] = await Promise.all([m.soLieu(tuNgay, denNgay), m.trangThai()])
      dong.push(...ghep(sl, tt, t => {
        const n = t.nganSachNhomDonViNho ?? t.nganSachChienDichDonViNho
        return n == null ? null : n / m.heSo(tienTe)
      }))
      console.log(`✅ Meta: ${sl.length} quảng cáo · tài khoản "${tk.ten}" (${tk.tienTe})`)
    } catch (e) { loi.push(`Meta — ${e.message}`) }
  } else loi.push('Meta — chưa điền taiKhoan.meta.adAccountId trong luat.json')

  if (luat.taiKhoan.google.customerId) {
    try {
      const g = await import('./lib/google.mjs')
      const tk = await g.thongTinTaiKhoan()
      const [sl, tt] = await Promise.all([g.soLieu(tuNgay, denNgay), g.trangThai()])
      dong.push(...ghep(sl, tt, t => t.nganSachChienDich || null))
      console.log(`✅ Google: ${sl.length} quảng cáo · tài khoản "${tk.ten}" (${tk.tienTe})`)
    } catch (e) { loi.push(`Google — ${e.message}`) }
  } else loi.push('Google — chưa điền taiKhoan.google.customerId trong luat.json')
}

for (const l of loi) console.log(`⛔ ${l}`)
if (!dong.length) {
  console.log('\nKhông kéo được dòng nào. Chạy `node ads/kiem.mjs` để xem thiếu gì, hoặc `node ads/keo.mjs --gia` để thử đường ống.')
  process.exit(1)
}

mkdirSync(join(GOC, 'du-lieu'), { recursive: true })
const ra = { keoLuc: new Date().toISOString(), tuNgay, denNgay, soNgay, tienTe, gia, loi, dong }
const duong = join(GOC, 'du-lieu', `${ngayVn()}${gia ? '-gia' : ''}.json`)
writeFileSync(duong, JSON.stringify(ra, null, 2), 'utf8')

const tong = dong.reduce((a, d) => a + d.chiTieu, 0)
const lead = dong.reduce((a, d) => a + d.lead, 0)
console.log(`\n📦 ${dong.length} quảng cáo · ${tuNgay} → ${denNgay} (${soNgay} ngày)`)
console.log(`   chi tiêu ${vnd(tong)} · ${lead} lead · CPL trung bình ${lead ? vnd(tong / lead) : '—'}`)
console.log(`   đã lưu: ${duong.replace(GOC + '/', 'bo-may/')}`)
console.log(`\nBước tiếp: node ads/soi.mjs${gia ? ' --gia' : ''}`)
