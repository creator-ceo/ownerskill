#!/usr/bin/env node
// Chấm số liệu đã kéo về → đề xuất hành động. CHỈ ĐỌC — không ghi vào tài khoản.
//   node ads/soi.mjs          soi ảnh chụp mới nhất
//   node ads/soi.mjs --gia    soi ảnh chụp giả, dùng ngưỡng mẫu
import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync } from 'node:fs'
import { join } from 'node:path'
import { GOC, docLuat, ngayVn, vnd, oConTrong } from './lib/cau-hinh.mjs'
import { cham, raHanhDong, gom, cpl } from './lib/so.mjs'

const gia = process.argv.includes('--gia')
const thuMuc = join(GOC, 'du-lieu')
if (!existsSync(thuMuc)) { console.log('Chưa có dữ liệu. Chạy: node ads/keo.mjs' + (gia ? ' --gia' : '')); process.exit(1) }

const ten = readdirSync(thuMuc).filter(f => f.endsWith('.json') && f.includes('-gia') === gia).sort().pop()
if (!ten) { console.log(`Chưa có ảnh chụp ${gia ? 'giả' : 'thật'}. Chạy: node ads/keo.mjs${gia ? ' --gia' : ''}`); process.exit(1) }
const anh = JSON.parse(readFileSync(join(thuMuc, ten), 'utf8'))

const luat = docLuat()
// Ngưỡng MẪU chỉ dùng cho chế độ giả. Số thật phải do chủ tài khoản chốt — code không được
// tự đặt giá trị nào vào luat.json (Hard Don't #5: cấm bịa số).
const NGUONG_MAU = { cplMucTieuVnd: 50_000, cplXauGapMay: 2.0, cplTotGapMay: 0.6, ctrThapNguong: 0.008, tanSuatCaoNguong: 2.5, soLeadToiThieuDeTinCpl: 5 }
const GIOI_HAN_MAU = { soNgayDuLieuToiThieu: 3, chiTieuToiThieuTruocKhiKetVnd: 300_000, doiNganSachToiDaPhanTram: 20, nganSachSanToiThieuVnd: 100_000, nganSachSanToiDaVnd: 800_000 }

let nguong = luat.nguongDanhGia, gioiHan = luat.gioiHanCung
if (gia) {
  nguong = { ...nguong, ...NGUONG_MAU }; gioiHan = { ...gioiHan, ...GIOI_HAN_MAU }
  console.log('⚠️  CHẾ ĐỘ GIẢ — dữ liệu bịa + ngưỡng MẪU. Đừng đọc kết luận dưới đây như số thật.\n')
} else {
  const trong = [...oConTrong({ nguongDanhGia: nguong }), ...oConTrong({ gioiHanCung: gioiHan })]
  if (trong.length) {
    console.log('⛔ Chưa soi được — luat.json còn ô chưa điền:')
    for (const o of trong) console.log(`   · ${o}`)
    console.log('\nĐây là chặn cố ý: không có CPL mục tiêu thì mọi kết luận "tốt/xấu" đều là bịa.')
    process.exit(1)
  }
}

const dong = gom(anh.dong)
const NHAN = { giet: '🔴 TẮT', giam: '🟠 GIẢM', giu: '⚪️ GIỮ', nuoi: '🟢 NUÔI', chua_du_bang_chung: '⏳ CHỜ' }
const ket = [], hanhDong = []

for (const h of dong) {
  const d = cham(h, nguong, gioiHan, anh.soNgay)
  ket.push({ h, d })
  hanhDong.push(...raHanhDong(h, d, gioiHan, anh.soNgay))
}

const thuTu = { giet: 0, giam: 1, nuoi: 2, giu: 3, chua_du_bang_chung: 4 }
ket.sort((a, b) => thuTu[a.d.ket] - thuTu[b.d.ket] || b.h.chiTieu - a.h.chiTieu)

console.log(`📊 ${anh.tuNgay} → ${anh.denNgay} · ${dong.length} quảng cáo · CPL mục tiêu ${vnd(nguong.cplMucTieuVnd)}\n`)
for (const { h, d } of ket) {
  // Sắp theo KẾT LUẬN chứ không theo nền — việc cần làm gấp phải nằm trên cùng,
  // nên nhãn nền đi kèm từng dòng thay vì làm tiêu đề nhóm.
  console.log(`${NHAN[d.ket]}  [${h.nen}] ${h.quangCao}`)
  console.log(`        ${h.chienDich} › ${h.nhom}`)
  console.log(`        ${d.vi}`)
  for (const c of d.co) console.log(`        ⚠️  ${c}`)
}

// Tổng kết theo tiền, không theo số dòng — 1 quảng cáo đốt 2tr quan trọng hơn 5 cái đốt 100k.
const tienTheoKet = {}
for (const { h, d } of ket) tienTheoKet[d.ket] = (tienTheoKet[d.ket] || 0) + h.chiTieu
console.log('\n── Tiền đang nằm ở đâu ──')
for (const k of Object.keys(thuTu)) if (tienTheoKet[k]) console.log(`   ${NHAN[k]}  ${vnd(tienTheoKet[k])}`)

const tong = dong.reduce((a, d) => a + d.chiTieu, 0)
const lead = dong.reduce((a, d) => a + d.lead, 0)
console.log(`   tổng ${vnd(tong)} · ${lead} lead · CPL chung ${lead ? vnd(tong / lead) : '—'}`)

mkdirSync(join(GOC, 'de-xuat'), { recursive: true })
// Ngân sách ngày đang cam kết theo nền — lấy MỖI nhóm một lần, vì nhiều quảng cáo
// dùng chung một ngân sách. Cộng theo từng dòng quảng cáo là thổi con số lên nhiều lần,
// mà đây đúng là con số lớp chặn dùng để so trần. Sai chỗ này thì trần thành vô nghĩa.
const daTinh = new Set()
const chiTieuNgayTheoNen = {}
for (const h of dong) {
  const k = `${h.nen}:${h.nhomId}`
  if (daTinh.has(k) || !(h.nganSachHienTai > 0)) continue
  daTinh.add(k)
  chiTieuNgayTheoNen[h.nen] = (chiTieuNgayTheoNen[h.nen] || 0) + h.nganSachHienTai
}

const duong = join(GOC, 'de-xuat', `${ngayVn()}${gia ? '-gia' : ''}.json`)
writeFileSync(duong, JSON.stringify({ soiLuc: new Date().toISOString(), tuAnh: ten, gia, soNgay: anh.soNgay, chiTieuNgayTheoNen, hanhDong }, null, 2), 'utf8')

console.log(`\n💡 ${hanhDong.length} hành động đề xuất → ${duong.replace(GOC + '/', 'bo-may/')}`)
for (const a of hanhDong) {
  const ns = a.nganSachMoi ? ` ${vnd(a.nganSachCu)} → ${vnd(a.nganSachMoi)}` : ''
  console.log(`   · ${a.nen}/${a.kieu}${ns} — ${a.ten}`)
}
console.log(`\nBước tiếp (CHƯA ghi gì, chỉ thử): node ads/ap.mjs${gia ? ' --gia' : ''}`)
