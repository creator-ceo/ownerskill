// Meta Marketing API (Graph). Chỉ dùng fetch, không npm.
// Quyền cần: ads_read (đọc) + ads_management (ghi), lấy qua System User của Business Manager.
import { docLuat, docKhoa } from './cau-hinh.mjs'

const G = 'https://graph.facebook.com'

// Meta trả tiền theo "đơn vị nhỏ nhất". VND không có phần thập phân nên hệ số là 1;
// USD/EUR là 100. Sai hệ số này = đặt ngân sách lệch 100 lần, nên KHÔNG đoán bừa:
// đồng nào không có trong bảng thì nổ lỗi.
const HE_SO = { VND: 1, JPY: 1, KRW: 1, USD: 100, EUR: 100, GBP: 100, AUD: 100, SGD: 100 }
export function heSo (tienTe) {
  const h = HE_SO[tienTe]
  if (!h) throw new Error(`Chưa biết hệ số đơn vị nhỏ nhất của ${tienTe}. Thêm vào HE_SO ở lib/meta.mjs, đừng đoán.`)
  return h
}

function khoa () {
  const k = docKhoa().META_TOKEN
  if (!k) throw new Error('Thiếu META_TOKEN trong ads/.khoa/that.env — xem ads/.khoa/mau.env')
  return k
}
function taiKhoan () {
  const id = docLuat().taiKhoan.meta.adAccountId
  if (!id) throw new Error('Chưa điền taiKhoan.meta.adAccountId trong ads/luat.json')
  return String(id).startsWith('act_') ? id : `act_${id}`
}
const ver = () => docLuat().phienBanApi.meta

async function goi (duong, { method = 'GET', body } = {}) {
  const url = new URL(`${G}/${ver()}/${duong}`)
  const opt = { method, headers: {} }
  if (method === 'GET') url.searchParams.set('access_token', khoa())
  else {
    const f = new URLSearchParams({ ...body, access_token: khoa() })
    opt.body = f; opt.headers['content-type'] = 'application/x-www-form-urlencoded'
  }
  const r = await fetch(url, opt)
  const j = await r.json().catch(() => ({}))
  if (!r.ok || j.error) {
    const e = j.error || {}
    throw new Error(`Meta ${r.status}: ${e.message || 'lỗi không rõ'}${e.error_user_msg ? ` — ${e.error_user_msg}` : ''} (code ${e.code}${e.error_subcode ? '/' + e.error_subcode : ''})`)
  }
  return j
}

/** Tự lật trang. Meta phân trang mọi thứ; không lật là thầm mất dữ liệu. */
async function goiHet (duong, tham = {}) {
  const q = new URLSearchParams({ ...tham, limit: '200' })
  let d = `${duong}?${q}`, ra = [], vong = 0
  while (d && vong++ < 50) {
    const j = await goi(d)
    ra.push(...(j.data || []))
    const sau = j.paging?.cursors?.after
    d = j.paging?.next && sau ? `${duong}?${new URLSearchParams({ ...tham, limit: '200', after: sau })}` : null
  }
  return ra
}

export async function thongTinTaiKhoan () {
  const j = await goi(`${taiKhoan()}?fields=name,currency,account_status,amount_spent,timezone_name`)
  return { ten: j.name, tienTe: j.currency, heSo: heSo(j.currency), trangThai: j.account_status, muiGio: j.timezone_name }
}

const SO_LEAD = new Set(['lead', 'offsite_conversion.fb_pixel_lead', 'onsite_conversion.lead_grouped', 'onsite_web_lead'])

/** Số liệu cấp QUẢNG CÁO trong khoảng ngày. Trả về khuôn chung của hệ (xem chuan-hoa.mjs). */
export async function soLieu (tuNgay, denNgay) {
  const rows = await goiHet(`${taiKhoan()}/insights`, {
    level: 'ad',
    time_range: JSON.stringify({ since: tuNgay, until: denNgay }),
    fields: ['campaign_id', 'campaign_name', 'adset_id', 'adset_name', 'ad_id', 'ad_name',
      'spend', 'impressions', 'clicks', 'ctr', 'frequency', 'reach', 'actions'].join(',')
  })
  return rows.map(r => {
    let lead = 0
    for (const a of r.actions || []) if (SO_LEAD.has(a.action_type)) lead = Math.max(lead, Number(a.value) || 0)
    return {
      nen: 'meta',
      chienDichId: r.campaign_id, chienDich: r.campaign_name,
      nhomId: r.adset_id, nhom: r.adset_name,
      quangCaoId: r.ad_id, quangCao: r.ad_name,
      chiTieu: Number(r.spend) || 0,
      hienThi: Number(r.impressions) || 0,
      nhap: Number(r.clicks) || 0,
      lead,
      tanSuat: Number(r.frequency) || 0
    }
  })
}

/** Trạng thái + ngân sách hiện tại. Cần để biết "ngân sách cũ" trước khi đề xuất đổi. */
export async function trangThai () {
  const ads = await goiHet(`${taiKhoan()}/ads`, {
    fields: 'id,name,status,effective_status,adset{id,name,status,daily_budget,lifetime_budget},campaign{id,name,status,daily_budget}'
  })
  return ads.map(a => ({
    nen: 'meta', quangCaoId: a.id, quangCao: a.name, trangThai: a.status, trangThaiThuc: a.effective_status,
    nhomId: a.adset?.id, nhom: a.adset?.name, nhomTrangThai: a.adset?.status,
    nganSachNhomDonViNho: a.adset?.daily_budget ? Number(a.adset.daily_budget) : null,
    nganSachTronDoi: a.adset?.lifetime_budget ? Number(a.adset.lifetime_budget) : null,
    chienDichId: a.campaign?.id, chienDich: a.campaign?.name,
    nganSachChienDichDonViNho: a.campaign?.daily_budget ? Number(a.campaign.daily_budget) : null
  }))
}

// ------------------------------- PHẦN GHI ------------------------------------
// Ba hàm dưới đây là ba chỗ duy nhất trong toàn dự án chạm được vào tiền của Đoàn.
// Không hàm nào tự kiểm tra luật — việc đó là của lib/chan.mjs, gọi ở ap.mjs.
// Cố ý tách: một chỗ chặn, một chỗ làm. Trộn vào nhau là mất chỗ để test.

export async function doiTrangThaiQuangCao (adId, trangThai) {
  if (!['ACTIVE', 'PAUSED'].includes(trangThai)) throw new Error(`Trạng thái lạ: ${trangThai}`)
  return goi(adId, { method: 'POST', body: { status: trangThai } })
}

export async function doiTrangThaiNhom (adsetId, trangThai) {
  if (!['ACTIVE', 'PAUSED'].includes(trangThai)) throw new Error(`Trạng thái lạ: ${trangThai}`)
  return goi(adsetId, { method: 'POST', body: { status: trangThai } })
}

/** @param {number} vnd ngân sách ngày theo ĐƠN VỊ TIỀN THẬT (đồng), hàm tự nhân hệ số. */
export async function doiNganSachNgay (id, vnd, tienTe) {
  const n = Math.round(vnd * heSo(tienTe))
  if (!(n > 0)) throw new Error('Ngân sách phải > 0')
  return goi(id, { method: 'POST', body: { daily_budget: String(n) } })
}
