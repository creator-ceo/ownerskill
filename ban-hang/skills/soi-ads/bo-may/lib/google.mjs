// Google Ads API (REST). Chỉ dùng fetch, không npm.
//
// ⚠️ CỔNG CHỜ THẬT, không có đường vòng: developer token mới cấp nằm ở mức
// "Test Account" — chỉ chạy được với tài khoản test, KHÔNG chạm được tài khoản
// thật. Phải nộp đơn xin Basic Access ở API Center, Google duyệt tính bằng TUẦN.
// Code dưới đây đúng và chạy được ngay khi token lên Basic; trước đó nó sẽ trả
// lỗi DEVELOPER_TOKEN_NOT_APPROVED và `keo.mjs` sẽ nói rõ ra chứ không im lặng.
import { docLuat, docKhoa } from './cau-hinh.mjs'

const API = 'https://googleads.googleapis.com'
const MICRO = 1_000_000   // Google tính mọi khoản tiền theo phần triệu

function khoa () {
  const k = docKhoa()
  const thieu = ['GOOGLE_DEVELOPER_TOKEN', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'GOOGLE_REFRESH_TOKEN'].filter(x => !k[x])
  if (thieu.length) throw new Error(`Thiếu ${thieu.join(', ')} trong ads/.khoa/that.env — xem ads/.khoa/mau.env`)
  return k
}
function taiKhoan () {
  const t = docLuat().taiKhoan.google
  if (!t.customerId) throw new Error('Chưa điền taiKhoan.google.customerId trong ads/luat.json')
  return { cid: String(t.customerId).replace(/\D/g, ''), mcc: t.loginCustomerId ? String(t.loginCustomerId).replace(/\D/g, '') : null }
}
const ver = () => docLuat().phienBanApi.google

// Access token sống 1 giờ — giữ trong bộ nhớ tiến trình, không ghi ra đĩa.
let veTam = null
async function ve () {
  if (veTam && veTam.het > Date.now() + 60_000) return veTam.token
  const k = khoa()
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: k.GOOGLE_CLIENT_ID, client_secret: k.GOOGLE_CLIENT_SECRET,
      refresh_token: k.GOOGLE_REFRESH_TOKEN, grant_type: 'refresh_token'
    })
  })
  const j = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(`OAuth Google ${r.status}: ${j.error || ''} ${j.error_description || ''}`.trim())
  veTam = { token: j.access_token, het: Date.now() + (j.expires_in || 3600) * 1000 }
  return veTam.token
}

async function goi (duong, body) {
  const k = khoa(), { mcc } = taiKhoan()
  const h = {
    authorization: `Bearer ${await ve()}`,
    'developer-token': k.GOOGLE_DEVELOPER_TOKEN,
    'content-type': 'application/json'
  }
  if (mcc) h['login-customer-id'] = mcc
  const r = await fetch(`${API}/${ver()}/${duong}`, { method: 'POST', headers: h, body: JSON.stringify(body) })
  const chu = await r.text()
  let j; try { j = JSON.parse(chu) } catch { j = chu }
  if (!r.ok) {
    const loi = j?.error?.details?.[0]?.errors?.[0]
    const ma = loi ? JSON.stringify(loi.errorCode) : ''
    throw new Error(`Google Ads ${r.status}: ${loi?.message || j?.error?.message || chu.slice(0, 300)} ${ma}`.trim())
  }
  return j
}

/** searchStream trả về MẢNG các khối, mỗi khối có `results` — phải gộp lại, quên là mất dữ liệu. */
async function truyVan (gaql) {
  const { cid } = taiKhoan()
  const j = await goi(`customers/${cid}/googleAds:searchStream`, { query: gaql })
  return (Array.isArray(j) ? j : [j]).flatMap(k => k.results || [])
}

export async function thongTinTaiKhoan () {
  const r = await truyVan('SELECT customer.id, customer.descriptive_name, customer.currency_code, customer.time_zone FROM customer LIMIT 1')
  const c = r[0]?.customer
  if (!c) throw new Error('Không đọc được thông tin tài khoản Google Ads')
  return { ten: c.descriptiveName, tienTe: c.currencyCode, muiGio: c.timeZone }
}

export async function soLieu (tuNgay, denNgay) {
  const rows = await truyVan(`
    SELECT campaign.id, campaign.name, ad_group.id, ad_group.name,
           ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status,
           metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions
    FROM ad_group_ad
    WHERE segments.date BETWEEN '${tuNgay}' AND '${denNgay}'
      AND ad_group_ad.status != 'REMOVED'`)
  const gom = new Map()
  for (const r of rows) {
    const id = r.adGroupAd?.ad?.id
    if (!id) continue
    const c = gom.get(id) || {
      nen: 'google',
      chienDichId: r.campaign?.id, chienDich: r.campaign?.name,
      nhomId: r.adGroup?.id, nhom: r.adGroup?.name,
      quangCaoId: id, quangCao: r.adGroupAd?.ad?.name || `Ad ${id}`,
      chiTieu: 0, hienThi: 0, nhap: 0, lead: 0, tanSuat: 0
    }
    c.chiTieu += Number(r.metrics?.costMicros || 0) / MICRO
    c.hienThi += Number(r.metrics?.impressions || 0)
    c.nhap += Number(r.metrics?.clicks || 0)
    c.lead += Number(r.metrics?.conversions || 0)
    gom.set(id, c)
  }
  return [...gom.values()]
}

export async function trangThai () {
  const rows = await truyVan(`
    SELECT campaign.id, campaign.name, campaign.status,
           campaign_budget.resource_name, campaign_budget.amount_micros,
           ad_group.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.status,
           ad_group_ad.resource_name
    FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED'`)
  return rows.map(r => ({
    nen: 'google',
    quangCaoId: r.adGroupAd?.ad?.id, quangCao: r.adGroupAd?.ad?.name || `Ad ${r.adGroupAd?.ad?.id}`,
    tenTaiNguyenQuangCao: r.adGroupAd?.resourceName,
    trangThai: r.adGroupAd?.status,
    nhomId: r.adGroup?.id, nhom: r.adGroup?.name,
    chienDichId: r.campaign?.id, chienDich: r.campaign?.name, chienDichTrangThai: r.campaign?.status,
    tenTaiNguyenNganSach: r.campaignBudget?.resourceName,
    nganSachChienDich: Number(r.campaignBudget?.amountMicros || 0) / MICRO
  }))
}

// ------------------------------- PHẦN GHI ------------------------------------
export async function doiTrangThaiQuangCao (tenTaiNguyen, trangThai) {
  if (!['ENABLED', 'PAUSED'].includes(trangThai)) throw new Error(`Trạng thái lạ: ${trangThai}`)
  const { cid } = taiKhoan()
  return goi(`customers/${cid}/adGroupAds:mutate`, {
    operations: [{ update: { resourceName: tenTaiNguyen, status: trangThai }, updateMask: 'status' }]
  })
}

/** @param {number} tien ngân sách ngày theo tiền thật, hàm tự đổi sang micro. */
export async function doiNganSachNgay (tenTaiNguyenNganSach, tien) {
  if (!(tien > 0)) throw new Error('Ngân sách phải > 0')
  const { cid } = taiKhoan()
  return goi(`customers/${cid}/campaignBudgets:mutate`, {
    operations: [{ update: { resourceName: tenTaiNguyenNganSach, amountMicros: String(Math.round(tien * MICRO)) }, updateMask: 'amount_micros' }]
  })
}
