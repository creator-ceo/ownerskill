#!/usr/bin/env node
// Bộ kiểm. Chạy: node ads/kiem.mjs
// Hai việc: (A) test lớp chặn bằng luật giả, (B) soi luật thật + khoá thật đã sẵn sàng chưa.
import { soi } from './lib/chan.mjs'
import { docLuat, docKhoa, oConTrong, vnd, gioVn } from './lib/cau-hinh.mjs'

let dat = 0, truot = 0
const test = (ten, fn) => {
  try { fn(); dat++; console.log(`  ✅ ${ten}`) }
  catch (e) { truot++; console.log(`  ❌ ${ten}\n       ${e.message}`) }
}
const phaiLa = (a, b, m) => { if (a !== b) throw new Error(`${m || ''} — chờ ${b}, nhận ${a}`) }
const phaiChua = (arr, s) => {
  if (!arr.some(x => String(x).includes(s))) throw new Error(`chờ vi phạm chứa "${s}", nhận [${arr}]`)
}

// ------------------------------ luật giả để test -----------------------------
const LUAT = {
  gioiHanCung: {
    chiTieuNgayToiDaVnd: { meta: 1_000_000, google: 1_000_000 },
    tongChiTieuNgayToiDaVnd: 1_500_000,
    doiNganSachToiDaPhanTram: 20,
    nganSachSanToiThieuVnd: 100_000,
    nganSachSanToiDaVnd: 800_000,
    soHanhDongToiDaMoiLan: 10,
    duocPhep: ['tam_dung_quang_cao', 'bat_lai_quang_cao', 'tam_dung_nhom_quang_cao', 'tang_ngan_sach', 'giam_ngan_sach'],
    camTuyetDoi: ['tao_chien_dich', 'xoa_bat_ky_thu_gi', 'doi_noi_dung_quang_cao', 'doi_trang_dich'],
    khungGioDuocGhi: { tu: 6, den: 22 },
    soNgayDuLieuToiThieu: 3,
    chiTieuToiThieuTruocKhiKetVnd: 300_000
  }
}
const BC_DU = { soNgay: 7, chiTieuVnd: 500_000 }
const BOI = { luat: LUAT, gioHienTai: 10, chiTieuNgayTheoNen: { meta: 400_000, google: 200_000 }, daDoiHomNayVnd: 0 }
const hd = o => ({ nen: 'meta', id: 'a1', ten: 'test', bangChung: BC_DU, ...o })

console.log('\n─── A. Lớp chặn ───')

test('cho qua hành động hợp lệ', () => {
  const r = soi([hd({ kieu: 'tam_dung_quang_cao' })], BOI)
  phaiLa(r.dat.length, 1); phaiLa(r.chan.length, 0)
})

test('chặn kiểu nằm trong danh sách cấm', () => {
  const r = soi([hd({ kieu: 'xoa_bat_ky_thu_gi' })], BOI)
  phaiLa(r.dat.length, 0); phaiChua(r.chan[0].viPham, 'nam_trong_danh_sach_cam')
})

test('chặn kiểu lạ chưa từng khai báo (mặc định là từ chối)', () => {
  const r = soi([hd({ kieu: 'kieu_moi_ai_do_vua_nghi_ra' })], BOI)
  phaiLa(r.dat.length, 0); phaiChua(r.chan[0].viPham, 'kieu_khong_duoc_phep')
})

test('chặn khi chưa đủ SỐ NGÀY dữ liệu', () => {
  const r = soi([hd({ kieu: 'tam_dung_quang_cao', bangChung: { soNgay: 1, chiTieuVnd: 500_000 } })], BOI)
  phaiChua(r.chan[0].viPham, 'chua_du_ngay')
})

test('chặn khi chưa đủ CHI TIÊU để kết luận', () => {
  const r = soi([hd({ kieu: 'tam_dung_quang_cao', bangChung: { soNgay: 7, chiTieuVnd: 50_000 } })], BOI)
  phaiChua(r.chan[0].viPham, 'chua_du_chi_tieu')
})

test('cho tăng ngân sách đúng 20%', () => {
  const r = soi([hd({ kieu: 'tang_ngan_sach', nganSachCu: 200_000, nganSachMoi: 240_000 })], BOI)
  phaiLa(r.dat.length, 1)
})

test('chặn tăng 21%', () => {
  const r = soi([hd({ kieu: 'tang_ngan_sach', nganSachCu: 200_000, nganSachMoi: 242_000 })], BOI)
  phaiChua(r.chan[0].viPham, 'doi_qua_manh')
})

test('chặn ngân sách mới dưới sàn', () => {
  const r = soi([hd({ kieu: 'giam_ngan_sach', nganSachCu: 110_000, nganSachMoi: 95_000 })], BOI)
  phaiChua(r.chan[0].viPham, 'duoi_san')
})

test('chặn "tăng" mà số mới lại nhỏ hơn (nhãn nói một đằng, số làm một nẻo)', () => {
  const r = soi([hd({ kieu: 'tang_ngan_sach', nganSachCu: 200_000, nganSachMoi: 180_000 })], BOI)
  phaiChua(r.chan[0].viPham, 'tang_nhung_so_moi_khong_lon_hon')
})

test('chặn khi vượt trần chi tiêu ngày của nền', () => {
  const boi = { ...BOI, chiTieuNgayTheoNen: { meta: 990_000, google: 0 } }
  const r = soi([hd({ kieu: 'tang_ngan_sach', nganSachCu: 200_000, nganSachMoi: 220_000 })], boi)
  phaiChua(r.chan[0].viPham, 'vuot_tran_nen_meta')
})

test('cộng dồn TRONG một lượt: 3 lệnh tăng nhỏ vẫn phải đụng trần', () => {
  const boi = { ...BOI, chiTieuNgayTheoNen: { meta: 950_000, google: 0 } }
  const r = soi([
    hd({ id: 'a', kieu: 'tang_ngan_sach', nganSachCu: 100_000, nganSachMoi: 120_000 }),
    hd({ id: 'b', kieu: 'tang_ngan_sach', nganSachCu: 100_000, nganSachMoi: 120_000 }),
    hd({ id: 'c', kieu: 'tang_ngan_sach', nganSachCu: 100_000, nganSachMoi: 120_000 })
  ], boi)
  if (r.dat.length === 3) throw new Error('cả 3 đều lọt — trần không cộng dồn trong lượt')
})

test('nhớ phần đã dịch chuyển từ đầu ngày (chặn lách bằng cách chạy nhiều lượt)', () => {
  const boi = { ...BOI, daDoiHomNayVnd: 299_000 } // trần luỹ kế = 1.5tr * 20% = 300k
  const r = soi([hd({ kieu: 'tang_ngan_sach', nganSachCu: 200_000, nganSachMoi: 220_000 })], boi)
  phaiChua(r.chan[0].viPham, 'luy_ke')
})

test('khoá toàn bộ khi ngoài khung giờ', () => {
  const r = soi([hd({ kieu: 'tam_dung_quang_cao' })], { ...BOI, gioHienTai: 3 })
  phaiLa(r.dat.length, 0)
  if (!r.khoaToanBo) throw new Error('phải khoá toàn bộ')
})

test('khoá toàn bộ khi quá số hành động một lượt', () => {
  const r = soi(Array.from({ length: 11 }, (_, i) => hd({ id: 'x' + i, kieu: 'tam_dung_quang_cao' })), BOI)
  phaiLa(r.dat.length, 0)
  if (!r.khoaToanBo) throw new Error('phải khoá toàn bộ')
})

test('khoá toàn bộ khi luật còn ô null (thiếu dữ liệu = chặn)', () => {
  const luat = { gioiHanCung: { ...LUAT.gioiHanCung, tongChiTieuNgayToiDaVnd: null } }
  const r = soi([hd({ kieu: 'tam_dung_quang_cao' })], { ...BOI, luat })
  phaiLa(r.dat.length, 0)
  if (!r.khoaToanBo) throw new Error('luật thiếu mà vẫn cho chạy — đây là lỗi nguy hiểm nhất')
})

test('một hành động hỏng không kéo cả lượt chết, và không lọt', () => {
  const r = soi([hd({ id: 'ok', kieu: 'tam_dung_quang_cao' }), hd({ id: 'xau', kieu: 'xoa_bat_ky_thu_gi' })], BOI)
  phaiLa(r.dat.length, 1); phaiLa(r.chan.length, 1)
})

// ------------------------------- B. luật thật --------------------------------
console.log('\n─── B. Cấu hình thật ───')
const luatThat = docLuat()
const khoa = docKhoa()
const trong = oConTrong(luatThat)

if (trong.length) {
  console.log(`  ⚠️  luat.json còn ${trong.length} ô CHƯA ĐIỀN — agent đang bị khoá, không ghi được gì:`)
  for (const o of trong) console.log(`       · ${o}`)
} else {
  console.log('  ✅ luat.json đã điền đủ')
  const g = luatThat.gioiHanCung
  console.log(`     trần ngày: meta ${vnd(g.chiTieuNgayToiDaVnd.meta)} · google ${vnd(g.chiTieuNgayToiDaVnd.google)} · tổng ${vnd(g.tongChiTieuNgayToiDaVnd)}`)
}

const canMeta = ['META_TOKEN']
const canGoogle = ['GOOGLE_DEVELOPER_TOKEN', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'GOOGLE_REFRESH_TOKEN']
const thieuM = canMeta.filter(k => !khoa[k])
const thieuG = canGoogle.filter(k => !khoa[k])
console.log(thieuM.length ? `  ⚠️  Meta: thiếu ${thieuM.join(', ')}` : '  ✅ Meta: có khoá')
console.log(thieuG.length ? `  ⚠️  Google: thiếu ${thieuG.join(', ')}` : '  ✅ Google: có khoá')
console.log(`  ℹ️  bây giờ là ${gioVn()}h giờ VN — khung được ghi là ${luatThat.gioiHanCung.khungGioDuocGhi.tu}h–${luatThat.gioiHanCung.khungGioDuocGhi.den}h`)

console.log(`\n─── Kết: ${dat} đạt · ${truot} trượt ───\n`)
process.exit(truot ? 1 : 0)
