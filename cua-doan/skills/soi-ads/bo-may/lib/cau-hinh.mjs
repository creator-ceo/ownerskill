// Nạp luật + khoá. Không phụ thuộc npm — cùng lối với owner-os/*.mjs.
import { readFileSync, existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

export const GOC = dirname(dirname(fileURLToPath(import.meta.url)))

export function docLuat () {
  const p = join(GOC, 'luat.json')
  if (!existsSync(p)) throw new Error('Không thấy ads/luat.json')
  return JSON.parse(readFileSync(p, 'utf8'))
}

/** Đọc .khoa/that.env. Trả object rỗng nếu chưa có — để `kiem.mjs` báo đẹp thay vì nổ. */
export function docKhoa () {
  const p = join(GOC, '.khoa', 'that.env')
  if (!existsSync(p)) return {}
  const ra = {}
  for (const dong of readFileSync(p, 'utf8').split('\n')) {
    const s = dong.trim()
    if (!s || s.startsWith('#')) continue
    const i = s.indexOf('=')
    if (i < 1) continue
    const v = s.slice(i + 1).trim().replace(/^["']|["']$/g, '')
    if (v) ra[s.slice(0, i).trim()] = v
  }
  return ra
}

/**
 * Gom mọi ô còn `null` trong luat.json thành danh sách phẳng.
 * Dùng để CHẶN chạy khi chưa điền, thay vì để code tự đoán một con số.
 * Đây là luật chống bịa số ở wiki/ai-operating-preferences.md (Hard Don't #5)
 * viết thành code: thiếu dữ liệu thì dừng lại hỏi, không tự điền.
 */
export function oConTrong (o, duong = '') {
  const ra = []
  for (const [k, v] of Object.entries(o)) {
    if (k.startsWith('ghiChu') || k === 'meta_ban') continue
    const d = duong ? `${duong}.${k}` : k
    if (v === null) ra.push(d)
    else if (v && typeof v === 'object' && !Array.isArray(v)) ra.push(...oConTrong(v, d))
  }
  return ra
}

export const vnd = n =>
  n == null ? '—' : new Intl.NumberFormat('vi-VN').format(Math.round(n)) + 'đ'

/** Ngày YYYY-MM-DD theo giờ Việt Nam, không phụ thuộc múi giờ máy. */
export const ngayVn = (d = new Date()) =>
  new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Ho_Chi_Minh' }).format(d)

/** Giờ 0–23 theo giờ Việt Nam. Lớp chặn khungGioDuocGhi dùng hàm này. */
export const gioVn = (d = new Date()) =>
  Number(new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Ho_Chi_Minh', hour: '2-digit', hour12: false }).format(d))
