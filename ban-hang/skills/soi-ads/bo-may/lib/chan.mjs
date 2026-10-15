// ============================================================================
// LỚP CHẶN — thứ duy nhất đứng giữa agent và tiền thật.
//
// Ba luật tự đặt cho file này, đừng ai gỡ:
//   1. HÀM THUẦN. Không gọi mạng, không đọc file, không gọi AI. Vào gì ra nấy,
//      nên test được — mà một lớp an toàn không test được thì không phải lớp an toàn.
//   2. MẶC ĐỊNH LÀ TỪ CHỐI. Không khớp luật nào → chặn. Không phải cho qua.
//   3. THIẾU DỮ LIỆU = CHẶN. Một ô `null` trong gioiHanCung khoá cả bộ. Cố ý:
//      agent chưa biết trần tiền thì không được phép tiêu đồng nào.
// ============================================================================
import { oConTrong, vnd } from './cau-hinh.mjs'

export const KIEU_DOI_NGAN_SACH = new Set(['tang_ngan_sach', 'giam_ngan_sach'])

/**
 * @param {Array} hanhDongs  [{ kieu, nen:'meta'|'google', id, ten,
 *                              nganSachCu?, nganSachMoi?, bangChung:{soNgay, chiTieuVnd} }]
 * @param {object} boiCanh   { luat, gioHienTai, chiTieuNgayTheoNen:{meta,google}, daDoiHomNayVnd }
 * @returns {{ dat:Array, chan:Array, khoaToanBo:string|null }}
 */
export function soi (hanhDongs, boiCanh) {
  const { luat, gioHienTai, chiTieuNgayTheoNen = {}, daDoiHomNayVnd = 0 } = boiCanh
  const g = luat.gioiHanCung

  // ---- Khoá toàn bộ: luật chưa điền xong thì không xét từng hành động nữa ----
  const trong = oConTrong({ gioiHanCung: g })
  if (trong.length) {
    return { dat: [], chan: hanhDongs.map(h => ({ ...h, viPham: ['luat_chua_dien'] })),
      khoaToanBo: `luat.json còn ${trong.length} ô chưa điền: ${trong.join(', ')}` }
  }
  if (!Array.isArray(hanhDongs)) return { dat: [], chan: [], khoaToanBo: 'hanhDongs không phải mảng' }

  if (gioHienTai < g.khungGioDuocGhi.tu || gioHienTai >= g.khungGioDuocGhi.den) {
    return { dat: [], chan: hanhDongs.map(h => ({ ...h, viPham: ['ngoai_khung_gio'] })),
      khoaToanBo: `Bây giờ là ${gioHienTai}h. Chỉ được ghi trong khung ${g.khungGioDuocGhi.tu}h–${g.khungGioDuocGhi.den}h giờ VN.` }
  }
  if (hanhDongs.length > g.soHanhDongToiDaMoiLan) {
    return { dat: [], chan: hanhDongs.map(h => ({ ...h, viPham: ['qua_nhieu_hanh_dong'] })),
      khoaToanBo: `${hanhDongs.length} hành động, trần là ${g.soHanhDongToiDaMoiLan}. Chia nhỏ ra chạy nhiều lượt, và đọc lại lượt trước trước khi chạy lượt sau.` }
  }

  const dat = [], chan = []
  // Cộng dồn TRONG lượt này, nối tiếp phần đã dịch chuyển từ đầu ngày.
  // Không có biến này thì 10 hành động mỗi cái lọt trần riêng vẫn vượt trần chung.
  let dichLuyKe = daDoiHomNayVnd
  const chiTieuDuKien = { ...chiTieuNgayTheoNen }

  for (const h of hanhDongs) {
    const viPham = []

    if (!h || typeof h !== 'object') { chan.push({ h, viPham: ['hanh_dong_khong_hop_le'] }); continue }
    if (g.camTuyetDoi.includes(h.kieu)) viPham.push('nam_trong_danh_sach_cam')
    if (!g.duocPhep.includes(h.kieu)) viPham.push('kieu_khong_duoc_phep')
    if (!['meta', 'google'].includes(h.nen)) viPham.push('nen_khong_hop_le')
    if (!h.id) viPham.push('thieu_id')

    // ---- Bằng chứng: chặn cái sai phổ biến nhất — giết quảng cáo khi chưa đủ dữ liệu ----
    const bc = h.bangChung || {}
    if (!(bc.soNgay >= g.soNgayDuLieuToiThieu)) {
      viPham.push(`chua_du_ngay(${bc.soNgay ?? '?'}<${g.soNgayDuLieuToiThieu})`)
    }
    if (!(bc.chiTieuVnd >= g.chiTieuToiThieuTruocKhiKetVnd)) {
      viPham.push(`chua_du_chi_tieu(${vnd(bc.chiTieuVnd)}<${vnd(g.chiTieuToiThieuTruocKhiKetVnd)})`)
    }

    // ---- Riêng cho việc đổi ngân sách ----
    if (KIEU_DOI_NGAN_SACH.has(h.kieu)) {
      const cu = h.nganSachCu, moi = h.nganSachMoi
      if (!(cu > 0) || !(moi > 0)) viPham.push('ngan_sach_khong_hop_le')
      else {
        const phanTram = Math.abs(moi - cu) / cu * 100
        if (phanTram > g.doiNganSachToiDaPhanTram + 1e-9) {
          viPham.push(`doi_qua_manh(${phanTram.toFixed(1)}%>${g.doiNganSachToiDaPhanTram}%)`)
        }
        if (h.kieu === 'tang_ngan_sach' && moi <= cu) viPham.push('tang_nhung_so_moi_khong_lon_hon')
        if (h.kieu === 'giam_ngan_sach' && moi >= cu) viPham.push('giam_nhung_so_moi_khong_nho_hon')
        if (moi < g.nganSachSanToiThieuVnd) viPham.push(`duoi_san(${vnd(moi)}<${vnd(g.nganSachSanToiThieuVnd)})`)
        if (moi > g.nganSachSanToiDaVnd) viPham.push(`tren_tran_san(${vnd(moi)}>${vnd(g.nganSachSanToiDaVnd)})`)

        const chenh = moi - cu
        const nenMoi = (chiTieuDuKien[h.nen] ?? 0) + chenh
        if (nenMoi > g.chiTieuNgayToiDaVnd[h.nen]) {
          viPham.push(`vuot_tran_nen_${h.nen}(${vnd(nenMoi)}>${vnd(g.chiTieuNgayToiDaVnd[h.nen])})`)
        }
        const tongMoi = Object.values({ ...chiTieuDuKien, [h.nen]: nenMoi }).reduce((a, b) => a + (b || 0), 0)
        if (tongMoi > g.tongChiTieuNgayToiDaVnd) {
          viPham.push(`vuot_tran_tong(${vnd(tongMoi)}>${vnd(g.tongChiTieuNgayToiDaVnd)})`)
        }
        // Trần dịch chuyển luỹ kế: chặn kiểu lách "mỗi lượt +20%" chạy 5 lượt trong ngày.
        if (dichLuyKe + Math.abs(chenh) > g.tongChiTieuNgayToiDaVnd * (g.doiNganSachToiDaPhanTram / 100)) {
          viPham.push('vuot_tran_dich_chuyen_luy_ke_trong_ngay')
        }

        if (!viPham.length) { chiTieuDuKien[h.nen] = nenMoi; dichLuyKe += Math.abs(chenh) }
      }
    }

    if (viPham.length) chan.push({ ...h, viPham })
    else dat.push(h)
  }

  return { dat, chan, khoaToanBo: null }
}

export function inKetQua ({ dat, chan, khoaToanBo }) {
  const d = []
  if (khoaToanBo) d.push(`⛔ KHOÁ TOÀN BỘ: ${khoaToanBo}`)
  d.push(`✅ qua chặn: ${dat.length}   ⛔ bị chặn: ${chan.length}`)
  for (const h of dat) d.push(`   ✅ ${h.nen}/${h.kieu} · ${h.ten || h.id}`)
  for (const h of chan) d.push(`   ⛔ ${h.nen || '?'}/${h.kieu || '?'} · ${h.ten || h.id || '?'} — ${h.viPham.join(', ')}`)
  return d.join('\n')
}
