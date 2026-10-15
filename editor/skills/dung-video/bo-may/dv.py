#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dung-video - dung video nguoi ngoi noi truoc ong kinh (ban doc 9:16).

    python3 dv.py kiem                              kiem may: ffmpeg, may nghe, font, cong cu tuy chon
    python3 dv.py moi <ten> <file...>               tao du an tu mot hay nhieu clip quay
    python3 dv.py nghe <ten>                        tieng -> chu co moc tung tu, soan nhap phu de
    python3 dv.py khung <ten> [--giay N]            anh kiem khung cat doc + vi tri phu de
    python3 dv.py dung <ten> --nhap [--tu S --den E] ban xem nhanh 540x960 (co the chi dung mot khuc)
    python3 dv.py dung <ten>                        ban cuoi 1080x1920 + bo lop roi cho CapCut
    python3 dv.py soi <ten> [--nhap]                tu soi tung cho cat: anh 4 khung + song am, do tieng bup / lem tieng
    python3 dv.py capcut <ten> [--khong-chep]       xuat thang thanh du an CapCut (mo CapCut la thay timeline dung san)
    python3 dv.py cai-hf                            (tuy chon) cai HyperFrames - ve chu dep hon, ~130 MB
    python3 dv.py cai-pho                           (tuy chon) cai PhoWhisper - nghe lan hai de doi chieu, 2,9 GB

Du lieu nam o ~/CreatorVideo/dung/<ten>/ (doi goc bang bien CREATOR_VIDEO_HOME).
"""
import os, sys, re, json, shutil, argparse, platform
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg, cat, chu, chen, hf

LOAI_CHE_PHU_DE = ("the", "danh_sach")     # the chu tu mang chu, khong hien phu de
GOI_Y_CHUNG = "Facebook, TikTok, YouTube, Zalo, CapCut"


def cmd_kiem(a):
    ok = True
    if sys.platform != "darwin" or platform.machine() != "arm64":
        ok = False
        print("may         : {} {} - may nghe (mlx-whisper) CHI chay tren Mac chip Apple (M1 tro len)".format(
            sys.platform, platform.machine()))
    print("ffmpeg      :", cfg.ffmpeg())
    r = cfg.chay([cfg.ffmpeg(), "-hide_banner", "-filters"], im=True).stdout
    for f in ("ass", "overlay", "loudnorm"):
        co = (" " + f + " ") in r
        ok &= co
        print("  bộ lọc {:<9}: {}".format(f, "có" if co else "THIẾU (cần bản ffmpeg có libass: brew install ffmpeg)"))
    co_lut = " lut3d " in r
    print("  bộ lọc {:<9}: {}".format("lut3d", "có" if co_lut else "không có, chỉ cần khi dùng file màu .cube"))
    try:
        import mlx_whisper  # noqa
        print("mlx-whisper : co")
    except Exception:
        ok = False; print("mlx-whisper : THIẾU  (pip3 install mlx-whisper)")
    for ten, goi in (("PIL", "pillow"), ("numpy", "numpy")):
        try:
            __import__(ten)
            print("{:<12}: co".format(goi))
        except Exception:
            ok = False; print("{:<12}: THIẾU  (pip3 install {})".format(goi, goi))
    for f in ("BeVietnamPro-SemiBold.ttf", "BeVietnamPro-ExtraBold.ttf", "BeVietnamPro-Medium.ttf"):
        co = os.path.exists(os.path.join(cfg.FONTS, f))
        ok &= co
        print("font {:<27}: {}".format(f, "có" if co else "THIẾU (" + cfg.FONTS + ")"))
    print("HyperFrames : {}".format("co (ve chu dep)" if hf.co_san() else "chua cai -> ve chu bang ASS. Cai (tuy chon, ~130 MB): python3 dv.py cai-hf"))
    if hf.co_san():
        print("  ffprobe   : {}".format(hf.ffprobe()))
    import nghe
    print("PhoWhisper  : {}".format("co (nghe lan hai de doi chieu)" if os.path.exists(os.path.join(nghe.MODEL_PHO, "config.json"))
                                    else "chua cai -> chi nghe mot lan. Cai (tuy chon, 2,9 GB): python3 dv.py cai-pho"))
    print("thu muc lam : {}".format(cfg.goc_lam_viec()))
    print("\n=> " + ("Sẵn sàng." if ok else "Còn thiếu, xem các dòng THIẾU."))


def cmd_moi(a):
    d = cfg.du_an(a.ten, tao=True)
    p = os.path.join(d, "bang-dung.json")
    if os.path.exists(p):
        sys.exit("Du an '{}' da co bang-dung.json - khong ghi de.".format(a.ten))
    nguon = []
    for f in a.file:
        src = os.path.abspath(os.path.expanduser(f))
        if not os.path.exists(src):
            sys.exit("!! Khong thay file: " + f)
        nguon.append(src)
    for x in ("anh", "broll"):
        os.makedirs(os.path.join(d, x), exist_ok=True)
    ten_kenh = str(cfg.ho_so().get("ten_kenh") or "").strip()
    cfg.ghi_json(p, {
        "nguon": nguon,
        "khung": {"x": 0.5, "y": 0.45},
        "zoom": [1.0, 1.12],
        "doi_khung_moi": 4.5,
        "lang_toi_da": 0.25,
        "nguong_lang_db": -35,
        "phu_de_y": 0.70,
        "phong_cach": "chuyen-gia-ngoi-noi",
        "nhip_muc_tieu": 3.1,
        "nghe_kep": True,
        "goi_y_tu": ", ".join(x for x in (ten_kenh, GOI_Y_CHUNG) if x),
        "bo": [],
        "chen": [],
        "nhac": None,
        "lut": None,
    })
    for f in nguon:
        ts = cfg.thong_so(f)
        print("  {}  {:.0f}s  {}x{}{}".format(os.path.basename(f), ts["dai"], ts["w"], ts["h"], "" if ts["tieng"] else "  !! KHONG CO TIENG"))
    print("Da tao {}\nTiep: python3 dv.py nghe {}".format(d, a.ten))
    print("Anh bang chung tha vao {}/anh/ · clip B-roll tha vao {}/broll/".format(d, d))


def cmd_khung(a):
    d = cfg.du_an(a.ten)
    bd = cfg.doc_json(os.path.join(d, "bang-dung.json"))
    ra = []
    for f, src in enumerate(bd["nguon"]):
        ts = cfg.thong_so(src)
        kf = bd["khung"][f] if isinstance(bd["khung"], list) else bd["khung"]
        hop = []
        for z, mau in zip(bd.get("zoom", [1.0]), ("yellow", "red", "cyan")):
            cw, ch, cx, cy = cat.khung_crop(ts["w"], ts["h"], z, kf.get("x", .5), kf.get("y", .45))
            hop.append("drawbox=x={}:y={}:w={}:h={}:color={}:t={}".format(cx, cy, cw, ch, mau, max(4, ts["h"] // 200)))
            if z == bd.get("zoom", [1.0])[0]:
                yp = cy + int(ch * bd.get("phu_de_y", .7))
                hop.append("drawbox=x={}:y={}:w={}:h={}:color=white@0.8:t=fill".format(cx, yp - ch // 60, cw, ch // 30))
        dich = os.path.join(d, "khung-{}.jpg".format(f))
        cfg.chay([cfg.ffmpeg(), "-y", "-ss", str(a.giay), "-i", src, "-frames:v", "1",
                  "-vf", ",".join(hop) + ",scale=900:-2", "-q:v", "5", dich], im=True)
        ra.append(dich)
    print("Vang = khung goc, do = khung zoom, vach trang = cho phu de.\n" + "\n".join(ra))


def doc_phu_de(p, tu):
    cum, sai = [], []
    for so, dg in enumerate(open(p, encoding="utf-8"), 1):
        dg = dg.strip()
        if not dg or dg.startswith("#"):
            continue
        m = re.match(r"^(\d+)\s*-\s*(\d+)\s*\|\s*(.*)$", dg)
        if not m:
            sai.append(so); continue
        a, b = int(m.group(1)), int(m.group(2))
        if a >= len(tu) or b >= len(tu) or b < a:
            sai.append(so); continue
        nho, _, to = m.group(3).partition("//")
        cum.append({"a": a, "b": b, "nho": nho.strip(), "to": to.strip()})
    if sai:
        print("!! phu-de.txt: bo qua {} dong sai khuon (dong {})".format(len(sai), ", ".join(map(str, sai[:10]))))
    return cum


# Chuyen canh mac dinh theo loai canh chen. Doi chung: "chuyen_canh" trong bang dung;
# doi rieng mot canh: "vao" / "ra" trong canh do. Kieu: cat · mo · truot · phong · lac · nhoe
CC_MAC_DINH = {"the": ("phong", "mo"), "danh_sach": ("truot", "mo"), "anh": ("truot", "truot"), "broll": ("mo", "mo")}


def giai_chuyen_canh(bd, c):
    chung = bd.get("chuyen_canh") or {}
    mac = chung.get(c["loai"]) or CC_MAC_DINH.get(c["loai"], ("cat", "cat"))
    if isinstance(mac, str):
        mac = (mac, mac)
    return c.get("vao") or mac[0], c.get("ra") or mac[1], float(chung.get("giay", 0.3))


def tinh_chen(bd, tu, doi, tong, canh_bao):
    """Moc tung canh chen tren ban dung (chua dung gi). Dung chung cho `dung` va `capcut`."""
    ds = []
    for k, c in enumerate(bd.get("chen", [])):
        ia, ib = cfg.khoang(c["tu"])
        t0 = doi(tu[ia]["f"], tu[ia]["s"]) - 0.06
        t1 = doi(tu[ib]["f"], tu[ib]["e"]) + float(c.get("keo_dai", 0.12))
        t0, t1 = max(0.0, t0), min(tong, t1)
        if t1 - t0 < 0.4:
            if 0 <= t0 < tong:
                canh_bao.append("chen #{} ({}) chi dai {:.2f}s - bo qua".format(k, c["loai"]))
            continue
        if c["loai"] == "danh_sach" and c.get("moc_dong"):
            c["_moc_dong"] = [None if m is None else max(0.1, doi(tu[m]["f"], tu[m]["s"]) - t0) for m in c["moc_dong"]]
        vao, ra, dai_cc = giai_chuyen_canh(bd, c)
        ds.append({"k": k, "loai": c["loai"], "t0": t0, "t1": t1, "file": None, "nen": cfg.nen_cua(c), "c": c,
                   "vao": vao, "ra": ra, "dai_cc": dai_cc})
    return sorted(ds, key=lambda x: x["t0"])


def tinh_phu_de(d, bd, tu, doi, tong, chen_ds):
    """Moc tung lan hien phu de. -> (cum_ds, cum_ok, bo_vi_cat, bo_vi_the)"""
    cum_ds = doc_phu_de(os.path.join(d, "phu-de.txt"), tu)
    bo = cat.tu_bi_bo(bd)
    cum_ok, bo_vi_cat, bo_vi_the = [], 0, 0
    for c in cum_ds:
        con = [i for i in range(c["a"], c["b"] + 1) if i not in bo]
        if not con:
            bo_vi_cat += 1; continue
        c["t0"] = doi(tu[con[0]]["f"], tu[con[0]]["s"]) - 0.04
        c["t_noi"] = doi(tu[con[-1]]["f"], tu[con[-1]]["e"])
        if c["t_noi"] < 0 or c["t0"] > tong:
            continue
        tren = [x for x in chen_ds if x["t0"] - 0.05 <= c["t0"] < x["t1"]]
        if tren and tren[0]["loai"] in LOAI_CHE_PHU_DE:
            bo_vi_the += 1; continue
        c["tren"] = tren[0] if tren else None
        cum_ok.append(c)
    for k, c in enumerate(cum_ok):
        ke = cum_ok[k + 1]["t0"] if k + 1 < len(cum_ok) else tong
        c["t1"] = ke - 0.02 if ke - c["t_noi"] < 0.7 else c["t_noi"] + 0.35
        # khong de phu de tran sang the chu ke tiep
        for x in chen_ds:
            if x["loai"] in LOAI_CHE_PHU_DE and c["t0"] < x["t0"] < c["t1"]:
                c["t1"] = x["t0"]
    return cum_ds, cum_ok, bo_vi_cat, bo_vi_the


def loc_chuyen_canh(j, x, w, truoc):
    """Bo loc ffmpeg dat canh chen j len nen, co chuyen canh vao/ra. Thoi gian tinh tren ban dung.
    mo = alpha mo dan · truot = truot tu phai vao, truot sang trai ra · lac = truot nhanh + nhoe ngang
    phong = mo dan (phan phong to da nuong san trong file B-roll) · nhoe = nhoe + mo dan."""
    t0, t1 = x["t0"], x["t1"]
    D = t1 - t0
    vao, ra = x.get("vao", "cat"), x.get("ra", "cat")
    d = min(x.get("dai_cc", 0.3), D / 3.0)
    dl = min(0.22, d)
    chuoi = ["setpts=PTS-STARTPTS+{:.4f}/TB".format(t0), "format=yuva420p"]
    if vao in ("mo", "phong", "nhoe"):
        chuoi.append("fade=t=in:st={:.4f}:d={:.3f}:alpha=1".format(t0, d))
    if ra in ("mo", "phong", "nhoe"):
        chuoi.append("fade=t=out:st={:.4f}:d={:.3f}:alpha=1".format(t1 - d, d))
    if vao in ("lac", "nhoe"):
        chuoi.append("gblur=sigma={}:sigmaV={}:enable='between(t,{:.4f},{:.4f})'".format(
            28 if vao == "lac" else 18, 0.01 if vao == "lac" else 18, t0, t0 + (dl if vao == "lac" else d)))
    if ra in ("lac", "nhoe"):
        dd = dl if ra == "lac" else d
        chuoi.append("gblur=sigma={}:sigmaV={}:enable='between(t,{:.4f},{:.4f})'".format(
            28 if ra == "lac" else 18, 0.01 if ra == "lac" else 18, t1 - dd, t1))
    # vi tri x: truot / lac vao tu phai, ra ve trai; ease-out bac 3
    xs = []
    if vao in ("truot", "lac"):
        dd = dl if vao == "lac" else d
        xs.append("if(lt(t,{a:.4f}),{w}*pow(1-(t-{t0:.4f})/{dd:.4f},3)".format(a=t0 + dd, w=w, t0=t0, dd=dd))
    if ra in ("truot", "lac"):
        dd = dl if ra == "lac" else d
        xs.append("if(gt(t,{b:.4f}),-{w}*pow((t-{b:.4f})/{dd:.4f},3)".format(b=t1 - dd, w=w, dd=dd))
    bx = "0"
    for e in reversed(xs):
        bx = e + "," + bx + ")"
    return ["[{j}:v]{c}[c{j}]".format(j=j, c=",".join(chuoi)),
            "{}[c{j}]overlay=x='{x}':y=0:format=auto:eof_action=pass:enable='between(t,{a:.4f},{b:.4f})'[b{j}]".format(
                truoc, j=j, x=bx, a=t0, b=t1 - 0.001)]


def cmd_dung(a):
    d = cfg.du_an(a.ten)
    bd = cfg.doc_json(os.path.join(d, "bang-dung.json"))
    tu = cfg.doc_json(os.path.join(d, "loi.json"))
    lang = cfg.doc_json(os.path.join(d, "lang.json"))
    if tu is None:
        sys.exit("Chua nghe. Chay: python3 dv.py nghe " + a.ten)
    nhap = a.nhap
    tl = 0.5 if nhap else 1.0
    w, h = int(cfg.W * tl), int(cfg.H * tl)
    # do dai tung file goc: doc tu loi.json neu o chua cam (chi can de kep diem cuoi)
    ts_nguon = []
    for f, p in enumerate(bd["nguon"]):
        dai = cfg.thong_so(p)["dai"] if os.path.exists(p) else 0
        ts_nguon.append(dai or max([t["e"] for t in tu if t["f"] == f] or [0]) + 1.0)
    canh_bao = []
    # dong co ve chu: HyperFrames (dep hon, can cai) hoac ASS (libass trong ffmpeg, du phong)
    dong_co = bd.get("dong_co") or ("hyperframes" if hf.co_san() else "ass")
    if dong_co == "hyperframes" and not hf.co_san():
        sys.exit("!! bang-dung.json dat dong_co=hyperframes nhung chua cai. Chay: python3 dv.py cai-hf")
    VE_BANG_HF = ("the", "danh_sach", "anh") if dong_co == "hyperframes" else ()

    # --- 1. danh sach doan giu ---
    doan, tk = cat.tinh_doan(tu, lang, bd, ts_nguon)
    doi, tong = cat.anh_xa(doan)

    # chi dung mot khuc (xem nhanh mot doan): loc lai doan theo giay tren ban dung
    tu_s, den_s = (a.tu or 0.0), (a.den or tong)
    if a.tu is not None or a.den is not None:
        moi, off = [], 0.0
        for x in doan:
            dx = x["e"] - x["s"]
            lo, hi = max(off, tu_s), min(off + dx, den_s)
            if hi - lo > 0.05:
                moi.append(dict(x, s=x["s"] + (lo - off), e=x["s"] + (hi - off)))
            off += dx
        doan = moi
        doi_goc = doi
        doi = lambda f, t: doi_goc(f, t) - tu_s
        tong = den_s - tu_s

    thu = os.path.join(d, "tam")
    os.makedirs(thu, exist_ok=True)
    a_roll = os.path.join(thu, "a-roll-cat{}.mp4".format("-nhap" if nhap else ""))
    cat.dung_a_roll(d, bd, doan, a_roll, w, h, nhap)

    # --- 2. canh chen ---
    chen_ds = tinh_chen(bd, tu, doi, tong, canh_bao)
    for x in chen_ds:
        c, k = x["c"], x["k"]
        print("Chen #{:02d} {:<9} {} -> {}  ({:.1f}s)".format(k, c["loai"], cfg.tg(x["t0"]), cfg.tg(x["t1"]), x["t1"] - x["t0"]))
        c["_vao"], c["_ra"], c["_dai_cc"] = x["vao"], x["ra"], x["dai_cc"]
        if c["loai"] not in VE_BANG_HF:      # the chu ve bang HyperFrames o buoc 3, B-roll luon do ffmpeg
            x["file"] = os.path.join(thu, "chen-{:02d}-{}{}.mp4".format(k, c["loai"], "-nhap" if nhap else ""))
            chen.dung_mot(d, c, x["t1"] - x["t0"], x["file"], w, h, nhap, canh_bao)

    # --- 3. phu de ---
    bo = cat.tu_bi_bo(bd)
    cum_ds, cum_ok, bo_vi_cat, bo_vi_the = tinh_phu_de(d, bd, tu, doi, tong, chen_ds)
    y_goc = int(chu.PY * float(bd.get("phu_de_y", 0.70)))
    p_ass = lop_mov = None
    if dong_co == "hyperframes":
        lop_mov = os.path.join(thu, "lop-chu{}.mov".format("-nhap" if nhap else ""))
        hf.dung_lop(d, cum_ok, [x for x in chen_ds if x["loai"] in VE_BANG_HF], tong, y_goc, lop_mov, nhap)
    else:
        ve = chu.Ve(cfg.MAU["chu_trang"])
        for c in cum_ok:
            if c["tren"] and c["tren"]["loai"] == "anh":
                chu.phu_de(ve, c, int(chu.PY * 0.17), tren_nen_sang=(c["tren"]["nen"] == "trang"))
            else:
                chu.phu_de(ve, c, y_goc)
        p_ass = os.path.join(thu, "phu-de.ass")
        open(p_ass, "w", encoding="utf-8").write(chu.dau_file() + ve.text())

    # --- 4. ghep ---
    ten_ra = "ban-nhap.mp4" if nhap else "ban-dung.mp4"
    if a.tu is not None or a.den is not None:
        ten_ra = ten_ra.replace(".mp4", "-{:.0f}-{:.0f}s.mp4".format(tu_s, den_s))
    ra = os.path.join(d, ten_ra)
    lenh = [cfg.ffmpeg(), "-y", "-i", a_roll]
    co_file = [x for x in chen_ds if x["file"]]
    for x in co_file:
        lenh += ["-i", x["file"]]
    loc, truoc = [], "[0:v]"
    for j, x in enumerate(co_file, 1):
        loc += loc_chuyen_canh(j, x, w, truoc)
        truoc = "[b{}]".format(j)
    n_vao = len(co_file) + 1
    if lop_mov:
        lenh += ["-i", lop_mov]
        loc.append("[{}:v]scale={}:{},format=yuva444p[lc]".format(n_vao, w, h))
        loc.append("{}[lc]overlay=0:0:format=auto:eof_action=pass[v]".format(truoc))
        n_vao += 1
    else:
        loc.append("{}ass='{}':fontsdir='{}'[v]".format(truoc, p_ass, cfg.FONTS))
    # can am luong 2 luot: do truoc, roi ap tuyen tinh -> ra dung -14 LUFS (1 luot lech ~1.5 LU)
    r = cfg.chay([cfg.ffmpeg(), "-hide_banner", "-nostats", "-i", a_roll, "-vn", "-af",
                  "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], im=True)
    do = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    can = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:"
           "measured_thresh={input_thresh}:offset={target_offset}:linear=true,aresample=48000").format(**do)
    am = "[am]"
    nhac = bd.get("nhac")
    if nhac and nhac.get("file"):
        lenh += ["-stream_loop", "-1", "-i", cfg.duong_dan(d, nhac["file"])]
        n_i = n_vao
        loc.append("[{}:a]volume={},aformat=sample_rates=48000:channel_layouts=stereo[nh]".format(n_i, nhac.get("am_luong", 0.15)))
        loc.append("[0:a]asplit=2[g1][g2]")
        loc.append("[nh][g1]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[nd]")
        loc.append("[g2][nd]amix=inputs=2:duration=first:normalize=0,{}[am]".format(can))
    else:
        loc.append("[0:a]{}[am]".format(can))
    lenh += ["-filter_complex", ";".join(loc), "-map", "[v]", "-map", am, "-fps_mode", "cfr", "-r", str(cfg.FPS),
             "-c:v", "libx264", "-preset", "ultrafast" if nhap else "medium", "-crf", "27" if nhap else "18",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k" if nhap else "192k", "-movflags", "+faststart",
             "-t", "{:.3f}".format(tong), ra]
    print("Ghep: A-roll + {} canh chen + {} lan hien phu de (ve chu bang {})...".format(len(chen_ds), len(cum_ok), dong_co))
    cfg.chay(lenh, im=True)
    cfg.ghi_json(ra + ".moc.json", moc_cat(doan, tu, bo, chen_ds))

    # --- 5. bo lop roi cho CapCut / Premiere (chi ban cuoi) ---
    if not nhap and not a.khong_lop:
        xuat_lop(d, a_roll, chen_ds, cum_ok, p_ass, tong, w, h, can, lop_mov, co_lut=bool(bd.get("lut")))

    # --- 6. bao cao: tu khai phan bi bo ---
    goc = sum(ts_nguon)
    doi_hinh = tk["cat"] + tk["doi_khung"] + 2 * len(chen_ds)
    dai_nhat = do_quang_dung_yen(doan, chen_ds)
    print("\n=== {} ===".format(ra))
    print("Do dai      : goc {} -> ban dung {}  (bo {:.0f}%)".format(cfg.tg(goc), cfg.tg(tong), 100 * (1 - tong / goc) if goc else 0))
    print("Cat         : {} tu bo theo bang dung ({} cho nhay), {} khoang lang cat ({:.1f}s)".format(
        tk["tu_bo"], tk["doan_bo"], tk["khoang_cat"], tk["giay_lang_cat"]))
    print("              trong do {} khe dai co tieng dong/tieng dem khong thanh chu (lat sach, 'o', 'a') - van cat".format(tk["khe_on"]))
    print("              {} khoang ngung ngan KHONG cat vi khong im that (moc may nghe co the lech)".format(tk["khoang_bo_qua"]))
    print("Phu de      : {} dong trong phu-de.txt -> hien {} | bo {} vi chu da cat | bo {} vi nam duoi the chu".format(
        len(cum_ds), len(cum_ok), bo_vi_cat, bo_vi_the))
    print("Nhip hinh   : {} lan doi hinh (cat {} + doi khung {} + chen {}) -> {:.1f}s/lan  (muc tieu: {}s/lan)".format(
        doi_hinh, tk["cat"], tk["doi_khung"], len(chen_ds), tong / max(1, doi_hinh), bd.get("nhip_muc_tieu", 3.1)))
    print("              quang hinh dung yen dai nhat: {:.1f}s luc {}".format(dai_nhat[0], cfg.tg(dai_nhat[1])))
    for c in canh_bao:
        print("!! " + c)


def moc_cat(doan, tu, bo, chen_ds):
    """Moi vet cat / doi khung / chen tren ban dung, kem chu ngay truoc va sau - cho buoc soi."""
    giu = [t for t in tu if t["i"] not in bo]
    ra, off = [], 0.0
    for k, x in enumerate(doan):
        if k:
            p = doan[k - 1]
            truoc = [t["w"] for t in giu if t["f"] == p["f"] and t["e"] <= p["e"] + 0.05][-5:]
            sau = [t["w"] for t in giu if t["f"] == x["f"] and t["s"] >= x["s"] - 0.05][:5]
            ra.append({"t": round(off, 3), "loai": "doi_khung" if x["noi_lien"] else "cat",
                       "truoc": " ".join(truoc), "sau": " ".join(sau)})
        off += x["e"] - x["s"]
    for c in chen_ds:
        ra.append({"t": round(c["t0"], 3), "loai": "vao_" + c["loai"]})
        ra.append({"t": round(c["t1"], 3), "loai": "ra_" + c["loai"]})
    return sorted(ra, key=lambda m: m["t"])


def cmd_soi(a):
    import soi
    d = cfg.du_an(a.ten)
    video = a.file or os.path.join(d, "ban-nhap.mp4" if a.nhap else "ban-dung.mp4")
    soi.soi(d, video, video + ".moc.json")


def do_quang_dung_yen(doan, chen_ds):
    moc = [0.0]
    off = 0.0
    for x in doan:
        off += x["e"] - x["s"]
        moc.append(off)
    for x in chen_ds:
        moc += [x["t0"], x["t1"]]
    moc = sorted(moc)
    tot = (0.0, 0.0)
    for a, b in zip(moc, moc[1:]):
        if b - a > tot[0]:
            tot = (b - a, a)
    return tot


def xuat_lop(d, a_roll, chen_ds, cum_ok, p_ass, tong, w, h, can, lop_mov=None, co_lut=False):
    lop = os.path.join(d, "lop")
    if os.path.isdir(lop):
        shutil.rmtree(lop)
    os.makedirs(os.path.join(lop, "03-chen"))
    # hinh giu nguyen, chi can lai tieng cho bang ban dung
    cfg.chay([cfg.ffmpeg(), "-y", "-i", a_roll, "-c:v", "copy", "-af", can, "-c:a", "aac", "-b:a", "256k",
              os.path.join(lop, "01-a-roll-da-cat.mp4")], im=True)
    if lop_mov:
        # HyperFrames da ve san lop chu + the thanh ProRes 4444 trong suot
        shutil.copy(lop_mov, os.path.join(lop, "02-chu-va-the-trong-suot.mov"))
    else:
        print("Xuat lop phu de trong suot (ProRes 4444)...")
        cfg.chay([cfg.ffmpeg(), "-y", "-f", "lavfi", "-i", "color=c=black@0.0:s={}x{}:r={}:d={:.3f},format=rgba".format(w, h, cfg.FPS, tong),
                  "-vf", "ass='{}':fontsdir='{}':alpha=1".format(p_ass, cfg.FONTS),
                  "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-alpha_bits", "8",
                  "-t", "{:.3f}".format(tong), os.path.join(lop, "02-phu-de-trong-suot.mov")], im=True)
    open(os.path.join(lop, "02-phu-de.srt"), "w", encoding="utf-8").write(chu.srt(cum_ok))
    ghi = ["Đặt từng file vào timeline đúng mốc (phút:giây trên bản dựng):", ""]
    for n, x in enumerate([x for x in chen_ds if x["file"]], 1):
        ten = "{:02d}_{}_{}.mp4".format(n, cfg.tg(x["t0"]).replace(":", "m").replace(".", "s"), x["loai"])
        shutil.copy(x["file"], os.path.join(lop, "03-chen", ten))
        ghi.append("  {}  {} -> {}  ({:.1f}s)".format(ten, cfg.tg(x["t0"]), cfg.tg(x["t1"]), x["t1"] - x["t0"]))
    open(os.path.join(lop, "03-chen", "moc-thoi-gian.txt"), "w", encoding="utf-8").write("\n".join(ghi) + "\n")
    open(os.path.join(lop, "DOC-TRUOC.txt"), "w", encoding="utf-8").write(
        "Các lớp rời để sửa tay trong CapCut / Premiere\n"
        "==============================================\n"
        "1. 01-a-roll-da-cat.mp4  -> đoạn quay chính, đặt ở 0:00. Đã cắt khoảng lặng, cắt câu hỏng, đã cân âm lượng.\n"
        "2. 03-chen/*.mp4         -> đặt lên trên đoạn quay chính, mỗi file đúng mốc ghi trong tên file\n"
        "                            (01_00m12s3_the.mp4 = đặt ở giây 12,3). Xem moc-thoi-gian.txt.\n"
        + ("3. 02-chu-va-the-trong-suot.mov -> lớp trên cùng, đặt ở 0:00. Chứa cả phụ đề LẪN thẻ chữ /\n"
           "   danh sách / ảnh bằng chứng (thẻ nền đặc sẽ che đoạn quay đúng lúc). Giữ nguyên hiệu ứng.\n"
           if lop_mov else
           "3. 02-phu-de-trong-suot.mov -> lớp trên cùng, đặt ở 0:00. Giữ nguyên kiểu chữ gõ + mờ dần.\n") +
        "   Muốn sửa chữ thì bỏ file .mov, nhập 02-phu-de.srt (CapCut: Văn bản > Nhập phụ đề) - sẽ mất hiệu ứng.\n"
        + ("Màu: đã áp file LUT ghi trong bang-dung.json.\n" if co_lut else
           "Màu: giữ nguyên như lúc quay (chưa áp LUT nào).\n"))
    print("Lop roi: " + lop)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="lenh")
    s.add_parser("kiem")
    s.add_parser("cai-hf")
    s.add_parser("cai-pho")
    x = s.add_parser("moi"); x.add_argument("ten"); x.add_argument("file", nargs="+")
    x = s.add_parser("nghe"); x.add_argument("ten")
    x = s.add_parser("khung"); x.add_argument("ten"); x.add_argument("--giay", type=float, default=5)
    x = s.add_parser("dung"); x.add_argument("ten"); x.add_argument("--nhap", action="store_true")
    x.add_argument("--tu", type=float); x.add_argument("--den", type=float)
    x.add_argument("--khong-lop", action="store_true", dest="khong_lop")
    x = s.add_parser("soi"); x.add_argument("ten"); x.add_argument("--nhap", action="store_true"); x.add_argument("--file")
    x = s.add_parser("capcut"); x.add_argument("ten"); x.add_argument("--khong-chep", action="store_true", dest="khong_chep")
    x.add_argument("--thu", help="ghi du an ra thu muc nay, KHONG dang ky vao CapCut (kiem bo xuat)")
    a = p.parse_args()
    if a.lenh == "kiem":
        cmd_kiem(a)
    elif a.lenh == "cai-hf":
        hf.cai()
    elif a.lenh == "cai-pho":
        import nghe
        nghe.cai_pho()
    elif a.lenh == "moi":
        cmd_moi(a)
    elif a.lenh == "nghe":
        import nghe
        nghe.main(a.ten)
    elif a.lenh == "khung":
        cmd_khung(a)
    elif a.lenh == "dung":
        cmd_dung(a)
    elif a.lenh == "soi":
        cmd_soi(a)
    elif a.lenh == "capcut":
        import capcut
        capcut.xuat(a, sys.modules[__name__])
    else:
        p.print_help()


if __name__ == "__main__":
    main()
