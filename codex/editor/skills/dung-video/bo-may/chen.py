# -*- coding: utf-8 -*-
"""Buoc CHEN: dung tung canh chen (the chu, danh sach, anh bang chung, B-roll) thanh clip doc rieng.

Moi canh chen la mot file mp4 khong tieng, dai dung khoang no che len A-roll.
Cung chinh cac file nay duoc chep sang lop/ de editor keo vao CapCut.
B-roll lay tu thu muc broll/ cua du an (nguoi dung tu dat clip vao), hoac mot duong dan tuyet doi.
"""
import os, sys
sys.dont_write_bytecode = True
import cfg, chu


def _mau_ff(hex6):
    return "0x" + hex6.lstrip("#")


def _ma_hoa(nhap):
    return ["-c:v", "libx264", "-preset", "ultrafast" if nhap else "veryfast", "-crf", "26" if nhap else "16",
            "-pix_fmt", "yuv420p", "-r", str(cfg.FPS), "-an"]


def the(d, c, D, dich, w, h, nhap):
    nen = cfg.nen_cua(c)
    if c["loai"] == "the":
        ass = chu.the_chu(D, nen, c.get("tieu_de", ""), c.get("phu", ""))
    else:
        ass = chu.the_danh_sach(D, nen, c.get("tieu_de", ""), c.get("dong", []), c.get("_moc_dong"))
    p_ass = dich[:-4] + ".ass"
    open(p_ass, "w", encoding="utf-8").write(ass)
    cfg.chay([cfg.ffmpeg(), "-y", "-f", "lavfi", "-i", "color=c={}:s={}x{}:r={}:d={:.3f}".format(
        _mau_ff(cfg.MAU[nen]), w, h, cfg.FPS, D),
        "-vf", "ass='{}':fontsdir='{}'".format(p_ass, cfg.FONTS)] + _ma_hoa(nhap) + ["-t", "{:.3f}".format(D), dich], im=True)


def _lam_anh(src, dich, w_max, h_max, goc, ban_kinh=26):
    """Bo goc + bong do + nghieng - lam mot lan bang Pillow, ra PNG trong suot."""
    from PIL import Image, ImageDraw, ImageFilter
    im = Image.open(src).convert("RGBA")
    tl = min(w_max / im.width, h_max / im.height)
    im = im.resize((max(1, int(im.width * tl)), max(1, int(im.height * tl))), Image.LANCZOS)
    mat = Image.new("L", im.size, 0)
    ImageDraw.Draw(mat).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=ban_kinh, fill=255)
    im.putalpha(mat)
    le = 40
    nen = Image.new("RGBA", (im.width + 2 * le, im.height + 2 * le), (0, 0, 0, 0))
    bong = Image.new("RGBA", im.size, (0, 0, 0, 150))
    bong.putalpha(mat.point(lambda v: v * 150 // 255))
    nen.paste(bong, (le, le + 12), bong)
    nen = nen.filter(ImageFilter.GaussianBlur(16))
    nen.paste(im, (le, le), im)
    if goc:
        nen = nen.rotate(goc, resample=Image.BICUBIC, expand=True)
    nen.save(dich)
    return nen.size


def anh(d, c, D, dich, w, h, nhap):
    """1-3 anh chup man hinh bo goc, hien lan luot, nhan nho phia tren moi anh."""
    nen = cfg.nen_cua(c)
    files = c["file"] if isinstance(c["file"], list) else [c["file"]]
    files = [cfg.duong_dan(d, f) for f in files]
    for f in files:
        if not os.path.exists(f):
            sys.exit("!! Khong thay anh: " + f)
    n = len(files)
    nhan = c.get("nhan", [])
    if isinstance(nhan, str):
        nhan = [nhan]
    nghieng = c.get("nghieng", True)
    goc_ds = [0] if n == 1 else ([-3, 3] if n == 2 else [-4, 2, -2])
    tl = w / 1080.0
    from PIL import Image
    ngang = sum(1 for f in files[:3] if Image.open(f).width > Image.open(f).height) * 2 >= min(n, 3)
    if ngang and n > 1:
        # anh ngang (anh chup, man hinh may tinh): xep chong doc, moi tam gan het be ngang
        # chua cho phu de o tren dau (y ~ 0.17) -> anh bat dau tu ~0.26
        o_w, o_h = 860 * tl, {2: 560, 3: 400}[min(n, 3)] * tl
        tam = [0.5] * n
        tam_ys = [0.43, 0.77] if n == 2 else [0.37, 0.61, 0.85]
    else:
        # anh doc (chup man hinh dien thoai): xep canh nhau
        o_w = {1: 860, 2: 470, 3: 320}[min(n, 3)] * tl
        o_h = {1: 1250, 2: 1000, 3: 820}[min(n, 3)] * tl
        tam = [0.5] if n == 1 else ([0.27, 0.73] if n == 2 else [0.18, 0.5, 0.82])
        tam_ys = [0.55] * n
    lenh = [cfg.ffmpeg(), "-y", "-f", "lavfi", "-i", "color=c={}:s={}x{}:r={}:d={:.3f}".format(
        _mau_ff(cfg.MAU[nen]), w, h, cfg.FPS, D)]
    loc, truoc = [], "[0:v]"
    buoc = min(0.6, max(0.25, (D - 0.8) / max(1, n)))
    nhan_ass = []
    for k, f in enumerate(files[:3]):
        png = dich[:-4] + "_{}.png".format(k)
        pw, ph = _lam_anh(f, png, o_w, o_h, goc_ds[k] if nghieng else 0, ban_kinh=int(26 * tl))
        lenh += ["-loop", "1", "-t", "{:.3f}".format(D), "-i", png]
        t = 0.1 + k * buoc
        tam_y = tam_ys[k]
        x, y = int(tam[k] * w - pw / 2), int(tam_y * h - ph / 2)
        loc.append("[{i}:v]format=rgba,fade=t=in:st={t:.2f}:d=0.25:alpha=1[a{k}]".format(i=k + 1, t=t, k=k))
        loc.append("{}[a{}]overlay={}:{}:format=auto[o{}]".format(truoc, k, x, y, k))
        truoc = "[o{}]".format(k)
        # nhan dat ngay tren mep anh, toa do 1080x1920
        chu_nhan = nhan[k] if k < len(nhan) else ""
        nhan_ass.append((chu_nhan, int(tam[k] * 1080), int((tam_y * h - ph / 2) / tl) + 10, t))
    p_ass = dich[:-4] + ".ass"
    open(p_ass, "w", encoding="utf-8").write(chu.nhan_anh(D, nen, nhan_ass))
    loc.append("{}ass='{}':fontsdir='{}'[v]".format(truoc, p_ass, cfg.FONTS))
    lenh += ["-filter_complex", ";".join(loc), "-map", "[v]"] + _ma_hoa(nhap) + ["-t", "{:.3f}".format(D), dich]
    cfg.chay(lenh, im=True)


def nguon_broll(d, c):
    """Canh B-roll -> duong dan file that. 'file' tuong doi thi tinh tu thu muc du an (vd 'broll/canh-1.mp4')."""
    if not c.get("file"):
        sys.exit("!! Canh B-roll thieu 'file'. Dat clip vao {}/broll/ roi ghi \"file\": \"broll/<ten clip>\"".format(d))
    src = cfg.duong_dan(d, c["file"])
    if not os.path.exists(src):
        sys.exit("!! Khong thay B-roll: {}\n   Dat clip vao {}/broll/ roi ghi \"file\": \"broll/<ten clip>\"".format(src, d))
    return src


def broll(d, c, D, dich, w, h, nhap, canh_bao):
    src = nguon_broll(d, c)
    ts = cfg.thong_so(src)
    tu = float(c.get("tu_giay", 0))
    if ts["dai"] and ts["dai"] - tu < D:
        canh_bao.append("B-roll {} chi con {:.1f}s tu giay {:.1f}, can {:.1f}s - dong bang khung cuoi".format(
            os.path.basename(src), ts["dai"] - tu, tu, D))
    import cat
    cw, ch, cx, cy = cat.khung_crop(ts["w"], ts["h"], float(c.get("zoom", 1.0)), float(c.get("x", 0.5)), float(c.get("y", 0.5)))
    lut = cfg.duong_lut(d, c.get("lut"))
    if lut:
        print("Mau B-roll  : {} - LUT {}".format(os.path.basename(src), os.path.basename(lut)))
    # chuyen canh "phong": nuong san phong to vao file (dau: 1.15 -> 1, cuoi: 1 -> 1.08), phan mo dan lam o buoc ghep
    vao, ra, dcc = c.get("_vao"), c.get("_ra"), min(float(c.get("_dai_cc", 0.3)), D / 3.0)
    if "phong" in (vao, ra):
        z = "1" + ("+0.15*max(0,1-it/{d:.3f})".format(d=dcc) if vao == "phong" else "") + \
            ("+0.08*max(0,(it-{b:.3f})/{d:.3f})".format(b=D - dcc, d=dcc) if ra == "phong" else "")
        khung = "crop={}:{}:{}:{},scale={}:{}:flags=lanczos,zoompan=z='{}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={}x{}:fps={}".format(
            cw, ch, cx, cy, 2 * w, 2 * h, z, w, h, cfg.FPS)
    else:
        khung = "crop={}:{}:{}:{},scale={}:{}:flags=lanczos,fps={}".format(cw, ch, cx, cy, w, h, cfg.FPS)
    vf = "{},setsar=1{},tpad=stop_mode=clone:stop_duration={:.2f}".format(
        khung, ",lut3d=file='{}'".format(lut) if lut else "", D)
    cfg.chay([cfg.ffmpeg(), "-y", "-ss", "{:.3f}".format(tu), "-i", src, "-vf", vf] + _ma_hoa(nhap) +
             ["-t", "{:.3f}".format(D), dich], im=True)


def dung_mot(d, c, D, dich, w, h, nhap, canh_bao):
    loai = c["loai"]
    if loai in ("the", "danh_sach"):
        the(d, c, D, dich, w, h, nhap)
    elif loai == "anh":
        anh(d, c, D, dich, w, h, nhap)
    elif loai == "broll":
        broll(d, c, D, dich, w, h, nhap, canh_bao)
    else:
        sys.exit("!! Loai chen la: " + loai)
