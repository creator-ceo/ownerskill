// Chấm điểm quảng cáo. THUẦN SỐ HỌC — không AI, không mạng, không đọc file.
// Vì sao không để model chấm: cùng một bảng số phải ra cùng một kết luận, mọi lần.
// Model không đảm bảo được điều đó, mà đây lại là thứ quyết định tắt/bật tiền.

export const cpl = h => (h.lead > 0 ? h.chiTieu / h.lead : null)
export const ctr = h => (h.hienThi > 0 ? h.nhap / h.hienThi : 0)

/**
 * @returns {{ ket:string, vi:string, co:string[], diem:number }}
 *   ket: chua_du_bang_chung | giet | giam | giu | nuoi
 */
export function cham (h, nguong, gioiHan, soNgay) {
  const co = []
  const c = cpl(h)
  const t = ctr(h)
  const duNgay = soNgay >= gioiHan.soNgayDuLieuToiThieu
  const duTien = h.chiTieu >= gioiHan.chiTieuToiThieuTruocKhiKetVnd

  if (!duNgay || !duTien) {
    return {
      ket: 'chua_du_bang_chung',
      vi: `mới ${soNgay} ngày · tiêu ${Math.round(h.chiTieu).toLocaleString('vi-VN')}đ — chưa đủ để kết luận gì`,
      co: [], diem: 0
    }
  }

  // Tiêu hết ngưỡng mà không ra lead nào: đây là ca rõ ràng nhất, xử trước.
  if (h.lead === 0) {
    return { ket: 'giet', vi: `tiêu ${Math.round(h.chiTieu).toLocaleString('vi-VN')}đ, 0 lead`, co: ['tiêu hết ngưỡng mà không ra lead nào — đây là ca rõ nhất, không cần chờ thêm'], diem: -3 }
  }

  const tiLe = c / nguong.cplMucTieuVnd
  if (t < nguong.ctrThapNguong) co.push(`ctr thấp (${(t * 100).toFixed(2)}% < ${(nguong.ctrThapNguong * 100).toFixed(2)}%)`)
  if (h.tanSuat >= nguong.tanSuatCaoNguong) co.push(`tần suất ${h.tanSuat.toFixed(1)} — người xem bắt đầu chán, đổi nội dung chứ đừng đổi ngân sách`)

  // Ít lead thì con số CPL chưa đáng tin, dù nó đẹp hay xấu. Không cho leo thang.
  const tinDuoc = h.lead >= nguong.soLeadToiThieuDeTinCpl
  if (!tinDuoc) co.push(`mới ${h.lead} lead — CPL chưa đủ mẫu để tin`)

  let ket, diem
  if (tiLe >= nguong.cplXauGapMay) { ket = 'giet'; diem = -2 }
  else if (tiLe > 1.2) { ket = 'giam'; diem = -1 }
  else if (tinDuoc && tiLe <= nguong.cplTotGapMay) { ket = 'nuoi'; diem = 2 }
  else { ket = 'giu'; diem = 0 }

  return {
    ket,
    vi: `CPL ${Math.round(c).toLocaleString('vi-VN')}đ = ${tiLe.toFixed(2)}× mục tiêu · ${h.lead} lead · CTR ${(t * 100).toFixed(2)}%`,
    co, diem
  }
}

/**
 * Từ kết luận → hành động cụ thể, đã tự kẹp vào trần % của luật.
 * Kẹp ở đây để đề xuất KHẢ THI; lib/chan.mjs vẫn soi lại lần nữa ở ap.mjs.
 * Hai lớp cùng một luật là cố ý — lớp này để tiện, lớp kia để an toàn.
 */
export function raHanhDong (h, danhGia, gioiHan, soNgay) {
  const chung = {
    nen: h.nen, ten: h.quangCao, chienDich: h.chienDich,
    bangChung: { soNgay, chiTieuVnd: h.chiTieu },
    vi: danhGia.vi
  }
  const b = gioiHan.doiNganSachToiDaPhanTram / 100

  switch (danhGia.ket) {
    case 'giet':
      return [{ ...chung, kieu: 'tam_dung_quang_cao', id: h.quangCaoId, tenTaiNguyen: h.tenTaiNguyenQuangCao }]

    case 'nuoi': {
      if (!(h.nganSachHienTai > 0)) return []   // không biết ngân sách cũ thì không đề xuất số mới
      const moi = Math.min(Math.round(h.nganSachHienTai * (1 + b)), gioiHan.nganSachSanToiDaVnd)
      if (moi <= h.nganSachHienTai) return []
      return [{ ...chung, kieu: 'tang_ngan_sach', id: h.nhomId, capDo: 'nhom',
        tenTaiNguyen: h.tenTaiNguyenNganSach, nganSachCu: h.nganSachHienTai, nganSachMoi: moi }]
    }

    case 'giam': {
      if (!(h.nganSachHienTai > 0)) return []
      const moi = Math.max(Math.round(h.nganSachHienTai * (1 - b)), gioiHan.nganSachSanToiThieuVnd)
      if (moi >= h.nganSachHienTai) return []
      return [{ ...chung, kieu: 'giam_ngan_sach', id: h.nhomId, capDo: 'nhom',
        tenTaiNguyen: h.tenTaiNguyenNganSach, nganSachCu: h.nganSachHienTai, nganSachMoi: moi }]
    }

    default:
      return []
  }
}

/** Gộp nhiều dòng cùng một quảng cáo (nhiều ngày) thành một dòng tổng. */
export function gom (dong) {
  const m = new Map()
  for (const d of dong) {
    const k = `${d.nen}:${d.quangCaoId}`
    const c = m.get(k)
    if (!c) { m.set(k, { ...d }); continue }
    c.chiTieu += d.chiTieu; c.hienThi += d.hienThi; c.nhap += d.nhap; c.lead += d.lead
    c.tanSuat = Math.max(c.tanSuat || 0, d.tanSuat || 0)
  }
  return [...m.values()]
}
