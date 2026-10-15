# -*- coding: utf-8 -*-
"""Buoc CAT: tu loi.json + lang.json + bang-dung.json -> danh sach doan giu, roi dung A-roll doc 9:16.

Luat cat:
  - Bo moi tu nam trong "bo" (nói lại, vấp, câu hỏng) - do AI chon khi doc loi.txt.
  - Khoang ngung giua hai tu > lang_toi_da thi cat bot, CHI KHI khoang do im that
    (khop lang.json). Whisper doi khi dat moc sai - khong im that ma cat la cat vao chu.
  - Moi doan giu dai hon doi_khung_moi giay thi doi khung (zoom vao/ra) o ranh gioi tu gan nhat,
    khong mat giay nao - mat nguoi xem khong phai nhin mot khung dung yen qua 4-5 giay.
"""
import os, sys
sys.dont_write_bytecode = True
import cfg

DEM_TRUOC = 0.07   # giu truoc tu dau cua doan (phu am dau tieng Viet)
DEM_SAU = 0.12     # giu sau tu cuoi cua doan
DOAN_NGAN_NHAT = 0.30
KHE_KHONG_LOI = 0.8   # khoang khong co chu nao dai hon muc nay: cat luon du co tieng dong (lat sach, "o", "a")


def tu_bi_bo(bd):
    bo = set()
    for k in bd.get("bo", []):
        a, b = cfg.khoang(k)
        bo.update(range(a, b + 1))
    return bo


def gop_lang(lang_f, khe=0.06):
    """Gop hai khoang im cach nhau mot tieng tach rat ngan (silencedetect hay xe doi mot khoang im)."""
    out = []
    for s, e in sorted(lang_f):
        if out and s - out[-1][1] <= khe:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def im_that(lang_f, a, b, toi_thieu):
    """Tra khoang im lon nhat nam trong [a, b], hoac None."""
    tot = None
    for s, e in lang_f:
        lo, hi = max(s, a), min(e, b)
        if hi - lo >= toi_thieu and (tot is None or hi - lo > tot[1] - tot[0]):
            tot = (lo, hi)
    return tot


def tinh_doan(tu, lang, bd, dai_file):
    """-> doan [{f, s, e, zoom}], thong ke."""
    bo = tu_bi_bo(bd)
    giu = [t for t in tu if t["i"] not in bo]
    if not giu:
        sys.exit("!! Khong con tu nao sau khi bo.")
    lang_max = float(bd.get("lang_toi_da", 0.25))
    tk = {"khoang_cat": 0, "khoang_bo_qua": 0, "giay_lang_cat": 0.0, "doan_bo": 0, "tu_bo": len(bo), "khe_on": 0}
    lang = [gop_lang(x) for x in lang]

    doan = []
    s0 = max(0.0, giu[0]["s"] - 0.15)
    for a, b in zip(giu, giu[1:]):
        f = a["f"]
        if b["f"] != f or b["i"] != a["i"] + 1:
            # nhay qua doan bi bo, hoac sang file khac
            doan.append({"f": f, "s": s0, "e": a["e"] + DEM_SAU})
            s0 = max(0.0, b["s"] - DEM_TRUOC)
            tk["doan_bo"] += 1
            continue
        khe = b["s"] - a["e"]
        if khe <= lang_max:
            continue
        nua = max(lang_max / 2, DEM_SAU)
        if khe >= KHE_KHONG_LOI:
            # khong co chu nao suot khe dai: tieng dong / tieng dem -> cat ca khe
            cat_tu, cat_den = a["e"] + nua, b["s"] - max(lang_max / 2, DEM_TRUOC)
            im_ = im_that(lang[f], a["e"], b["s"], 0.15)
            if not im_ or im_[1] - im_[0] < khe - 2 * nua - 0.1:
                tk["khe_on"] += 1
        else:
            # khe ngan: chi cat phan im that - moc cua may nghe co the lech vao chu
            im = im_that(lang[f], a["e"], b["s"], min(0.15, lang_max))
            if not im:
                tk["khoang_bo_qua"] += 1
                continue
            cat_tu, cat_den = max(im[0], a["e"] + nua), min(im[1], b["s"] - max(lang_max / 2, DEM_TRUOC))
        if cat_den - cat_tu < 0.12:
            tk["khoang_bo_qua"] += 1
            continue
        doan.append({"f": f, "s": s0, "e": cat_tu})
        s0 = cat_den
        tk["khoang_cat"] += 1
        tk["giay_lang_cat"] += cat_den - cat_tu
    doan.append({"f": giu[-1]["f"], "s": s0, "e": min(giu[-1]["e"] + 0.35, dai_file[giu[-1]["f"]])})

    # luong tu ve khung hinh de hinh-tieng khong lech dan qua hang chuc lan cat
    for d in doan:
        d["s"] = round(d["s"] * cfg.FPS) / cfg.FPS
        d["e"] = round(d["e"] * cfg.FPS) / cfg.FPS
    # gop doan qua ngan vao doan truoc (cung file)
    gon = []
    for d in doan:
        if gon and d["e"] - d["s"] < DOAN_NGAN_NHAT and gon[-1]["f"] == d["f"] and d["s"] >= gon[-1]["e"]:
            gon[-1]["e"] = d["e"]
        elif d["e"] - d["s"] > 1e-3:
            gon.append(d)
    doan = gon

    # doi khung trong doan dai: tach tai ranh gioi tu, khong bo giay nao
    moi = float(bd.get("doi_khung_moi", 4.5))
    zooms = bd.get("zoom", [1.0, 1.12])
    kq = []
    for d in doan:
        ranh = [t["s"] - 0.02 for t in giu if t["f"] == d["f"] and d["s"] + 1.5 < t["s"] < d["e"] - 1.5]
        diem, moc = [], d["s"]
        while d["e"] - moc > moi + 1.0 and moi > 0:
            muc_tieu = moc + moi
            gan = [r for r in ranh if r > moc + 1.5]
            if not gan:
                break
            r = min(gan, key=lambda x: abs(x - muc_tieu))
            r = round(r * cfg.FPS) / cfg.FPS
            if d["e"] - r < 1.5:
                break
            diem.append(r); moc = r
        moc = d["s"]
        for r in diem + [d["e"]]:
            kq.append({"f": d["f"], "s": moc, "e": r, "noi_lien": moc != d["s"]})
            moc = r
    for k, d in enumerate(kq):
        d["zoom"] = zooms[k % len(zooms)]
    tk["doi_khung"] = sum(1 for d in kq if d["noi_lien"])
    tk["cat"] = sum(1 for d in kq[1:] if not d["noi_lien"])
    return kq, tk


def anh_xa(doan):
    """-> ham doi (file, giay goc) sang giay tren ban dung."""
    moc, off = [], 0.0
    for d in doan:
        moc.append((d["f"], d["s"], d["e"], off))
        off += d["e"] - d["s"]

    def doi(f, t):
        tot = None
        for ff, s, e, o in moc:
            if ff != f:
                continue
            if s <= t <= e:
                return o + (t - s)
            # tu bi cat: kep ve diem gan nhat
            kc = min(abs(t - s), abs(t - e))
            v = o if abs(t - s) <= abs(t - e) else o + (e - s)
            if tot is None or kc < tot[0]:
                tot = (kc, v)
        return tot[1] if tot else 0.0
    return doi, off


def khung_crop(sw, sh, zoom, x, y):
    """Vung cat 9:16 tren khung goc (ngang hay doc deu duoc)."""
    if sw / sh > 9 / 16:
        ch = sh / zoom; cw = ch * 9 / 16
    else:
        cw = sw / zoom; ch = cw * 16 / 9
    cw, ch = int(cw) // 2 * 2, int(ch) // 2 * 2
    cx = min(max(0, x * sw - cw / 2), sw - cw)
    cy = min(max(0, y * sh - ch / 2), sh - ch)
    return cw, ch, int(cx), int(cy)


def dau_van_tay(bd, doan, w, h, nhap):
    import json, hashlib
    k = {"doan": doan, "khung": bd.get("khung"), "lut": bd.get("lut"), "nguon": bd["nguon"],
         "wh": [w, h], "nhap": nhap}
    return hashlib.sha1(json.dumps(k, sort_keys=True).encode()).hexdigest()


def dung_a_roll(d, bd, doan, dich, w, h, nhap=False):
    """Cat + dung A-roll. Danh sach cat, khung, LUT khong doi so voi lan truoc thi dung lai file cu
    (sua chu / the / B-roll khong phai cat lai - va khong can cam o ngoai chua file goc)."""
    van_tay = dau_van_tay(bd, doan, w, h, nhap)
    p_vt = dich + ".van-tay"
    if os.path.exists(dich) and os.path.exists(p_vt) and open(p_vt).read().strip() == van_tay:
        print("Dung lai A-roll da cat (danh sach cat khong doi): " + os.path.basename(dich))
        return
    nguon = bd["nguon"]
    thieu = [p for p in nguon if not os.path.exists(p)]
    if thieu:
        sys.exit("!! Khong thay file nguon (o ngoai chua cam?):\n   " + "\n   ".join(thieu))
    khung = bd.get("khung", {})
    ts = [cfg.thong_so(p) for p in nguon]
    for p, t in zip(nguon, ts):
        if not t["w"]:
            sys.exit("!! Khong doc duoc kich thuoc khung hinh: " + p)
    lenh = [cfg.ffmpeg(), "-y"]
    for p in nguon:
        lenh += ["-i", p]
    loc = []
    dem = {}
    for d_ in doan:
        dem[d_["f"]] = dem.get(d_["f"], 0) + 1
    nhan = {}
    for f, n in dem.items():
        vs = "".join("[v{}_{}]".format(f, k) for k in range(n))
        as_ = "".join("[a{}_{}]".format(f, k) for k in range(n))
        loc.append("[{}:v]split={}{}".format(f, n, vs) if n > 1 else "[{}:v]null{}".format(f, vs))
        loc.append("[{}:a]asplit={}{}".format(f, n, as_) if n > 1 else "[{}:a]anull{}".format(f, as_))
        nhan[f] = 0
    # mau: chi ap khi bang dung co "lut" (file .cube cua chinh nguoi dung); khong co thi giu mau goc
    lut_f = {}
    for f, p in enumerate(nguon):
        lut_f[f] = cfg.lut_cua_file(d, bd, f)
        if lut_f[f]:
            print("Mau A-roll  : {} - LUT {}".format(os.path.basename(p), os.path.basename(lut_f[f])))
    cap = []
    for k, d_ in enumerate(doan):
        f = d_["f"]; j = nhan[f]; nhan[f] += 1
        kf = khung[f] if isinstance(khung, list) else khung
        cw, ch, cx, cy = khung_crop(ts[f]["w"], ts[f]["h"], d_["zoom"], kf.get("x", 0.5), kf.get("y", 0.45))
        dai = d_["e"] - d_["s"]
        loc.append("[v{f}_{j}]trim=start={s:.4f}:end={e:.4f},setpts=PTS-STARTPTS,crop={cw}:{ch}:{cx}:{cy},"
                   "scale={w}:{h}:flags=lanczos,setsar=1,fps={fps}{lut}[vc{k}]".format(
                       f=f, j=j, s=d_["s"], e=d_["e"], cw=cw, ch=ch, cx=cx, cy=cy, w=w, h=h, fps=cfg.FPS, k=k,
                       lut=",lut3d=file='{}'".format(lut_f[f]) if lut_f[f] else ""))
        mo = 0.006 if d_["noi_lien"] else 0.012
        loc.append("[a{f}_{j}]atrim=start={s:.4f}:end={e:.4f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,"
                   "afade=t=in:d={mo},afade=t=out:st={st:.4f}:d={mo}[ac{k}]".format(
                       f=f, j=j, s=d_["s"], e=d_["e"], k=k, mo=mo, st=max(0, dai - mo)))
        cap.append("[vc{k}][ac{k}]".format(k=k))
    # fps sau concat: nguon 29.97 cat theo luoi 1/30 -> thieu vai khung, ra ~29.7 fps (CapCut xu ly kem)
    loc.append("{}concat=n={}:v=1:a=1[vc][an]".format("".join(cap), len(doan)))
    loc.append("[vc]fps={}[vn]".format(cfg.FPS))
    loc.append("[an]highpass=f=70,aresample=48000[ao]")     # can am luong lam o buoc ghep (2 luot, co nhac)
    lenh += ["-filter_complex", ";".join(loc), "-map", "[vn]", "-map", "[ao]", "-fps_mode", "cfr", "-r", str(cfg.FPS),
             "-c:v", "libx264", "-preset", "ultrafast" if nhap else "veryfast", "-crf", "26" if nhap else "14",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", dich]
    print("Dung A-roll: {} doan tu {} file...".format(len(doan), len(nguon)))
    if os.path.exists(p_vt):
        os.remove(p_vt)
    cfg.chay(lenh, im=True)
    open(p_vt, "w").write(van_tay)
