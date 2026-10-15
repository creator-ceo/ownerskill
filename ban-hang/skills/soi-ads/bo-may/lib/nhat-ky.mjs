// Nhật ký append-only. Mỗi hành động GHI vào tài khoản quảng cáo đẻ đúng một dòng.
// Cùng luật với log.md của bộ não: chỉ nối thêm, không bao giờ viết đè.
import { appendFileSync, existsSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import { GOC } from './cau-hinh.mjs'

const DUONG = join(GOC, 'nhat-ky.jsonl')

export function ghi (muc) {
  appendFileSync(DUONG, JSON.stringify({ luc: new Date().toISOString(), ...muc }) + '\n', 'utf8')
}

export function doc () {
  if (!existsSync(DUONG)) return []
  return readFileSync(DUONG, 'utf8').split('\n').filter(Boolean).map(d => {
    try { return JSON.parse(d) } catch { return null }
  }).filter(Boolean)
}

/** Tổng số tiền/ngày agent đã tự ý dịch chuyển hôm nay — đầu vào của lớp chặn. */
export function daDoiHomNay (ngay) {
  let tong = 0
  for (const m of doc()) {
    if (m.ket !== 'da_ghi' || m.ngay !== ngay) continue
    if (typeof m.chenhNganSachVnd === 'number') tong += Math.abs(m.chenhNganSachVnd)
  }
  return tong
}
