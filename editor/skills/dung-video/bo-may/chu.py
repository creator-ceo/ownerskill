# -*- coding: utf-8 -*-
"""Ve chu bang ASS (libass trong ffmpeg): phu de 2 tang, the chu, the danh sach, nhan anh.

Luon soan o he toa do 1080x1920 - libass tu co gian khi dung ban nhap 540x960.

Ky thuat "chu an": cau day du luon nam trong dong, phan chua hien dat \\alpha&HFF&.
Nho vay chu hien dan tu trai sang ma cau khong xe dich.
Bong mo = mot lop chu den mo rieng ben duoi (lop 0), chu trang sac net o lop 1.
"""
import cfg

PX, PY = 1080, 1920
FONT_NHO = "Be Vietnam Pro SemiBold"
FONT_TO = "Be Vietnam Pro ExtraBold"
FONT_VUA = "Be Vietnam Pro Medium"
BONG = "&H40&"       # do trong suot cua bong (00 dac, FF trong)


def mau_ass(hex6):
    h = hex6.lstrip("#")
    return "&H{}{}{}&".format(h[4:6], h[2:4], h[0:2]).upper()


def dau_file():
    kieu = [
        # Name, Font, Size, Primary, Secondary, Outline, Back, Bold, Italic, Underline, Strike, ScaleX, ScaleY,
        # Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        "Style: Nho,{},64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,70,70,0,1".format(FONT_NHO),
        "Style: To,{},128,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,1,0,0,100,100,-1,0,1,0,0,2,60,60,0,1".format(FONT_TO),
        "Style: TheTieuDe,{},150,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,-1,0,1,0,0,5,60,60,0,1".format(FONT_TO),
        "Style: ThePhu,{},56,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,60,60,0,1".format(FONT_VUA),
        "Style: DsTieuDe,{},76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,110,90,0,1".format(FONT_TO),
        "Style: DsDong,{},58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,1,0,0,100,100,0,0,1,0,0,7,110,90,0,1".format(FONT_NHO),
        "Style: Nhan,{},52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,20,20,0,1".format(FONT_NHO),
    ]
    return ("[Script Info]\nScriptType: v4.00+\nPlayResX: {}\nPlayResY: {}\nWrapStyle: 0\nScaledBorderAndShadow: yes\n"
            "YCbCr Matrix: TV.709\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
            "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, "
            "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n{}\n\n[Events]\nFormat: Layer, Start, End, "
            "Style, Name, MarginL, MarginR, MarginV, Effect, Text\n").format(PX, PY, "\n".join(kieu))


def t_ass(s):
    s = max(0.0, s)
    cs = int(round(s * 100))
    return "{}:{:02d}:{:02d}.{:02d}".format(cs // 360000, cs // 6000 % 60, cs // 100 % 60, cs % 100)


def esc(s):
    return s.replace("\\", "/").replace("{", "(").replace("}", ")").replace("\n", " ")


def dong(layer, t0, t1, kieu, chu):
    if t1 - t0 < 0.01:
        return ""
    return "Dialogue: {},{},{},{},,0,0,0,,{}\n".format(layer, t_ass(t0), t_ass(t1), kieu, chu)


def con_tro(co):
    """Khoi con tro trang, cao bang chu."""
    w, h = int(co * 0.42), int(co * 0.98)
    return "{\\p1}m 0 0 l %d 0 %d %d 0 %d{\\p0}" % (w, w, h, h)


class Ve:
    """Gom cac dong ASS; moi 'trang thai' chu ve 2 lop: bong + chu."""

    def __init__(self, mau="ffffff", bong=True):
        self.out = []
        self.mau = mau_ass(mau)
        self.bong = bong

    def trang_thai(self, t0, t1, kieu, x, y, phan, them=""):
        """phan: list (chu, trang_thai) voi trang_thai in hien|an|vao|contro|contro_an
        'vao' = mo dan + net dan trong 0.22s dau cua dong."""
        for lop in ((0, 1) if self.bong else (1,)):
            if lop == 0:
                dau = "{\\pos(%d,%d)\\c&H000000&\\blur9\\bord0\\shad0%s}" % (x, y + 5, them)
                hien = "{\\alpha%s}" % BONG
                vao = "{\\alpha&HFF&\\t(0,220,\\alpha%s)}" % BONG
            else:
                dau = "{\\pos(%d,%d)\\c%s\\bord0\\shad0%s}" % (x, y, self.mau, them)
                hien = "{\\alpha&H00&\\blur0.4}"
                vao = "{\\alpha&HFF&\\blur12\\t(0,220,\\alpha&H00&\\blur0.4)}"
            an = "{\\alpha&HFF&}"
            s = dau
            for chu, tt in phan:
                if not chu:
                    continue
                if tt == "hien":
                    s += hien + esc(chu)
                elif tt == "an":
                    s += an + esc(chu)
                elif tt == "vao":
                    s += vao + esc(chu)
                elif tt == "contro":
                    s += hien + chu
                elif tt == "contro_an":
                    s += an + chu
            self.out.append(dong(lop, t0, t1, kieu, s))

    def go(self, t0, t_xong, t1, kieu, x, y, chu, co, contro=True, truoc=None, sau=None):
        """Go tung ky tu tu t0 den t_xong, giu nguyen den t1."""
        truoc, sau = truoc or [], sau or []
        n = len(chu)
        if n == 0:
            return
        buoc = max(0.012, (t_xong - t0) / n)
        ct = con_tro(co) if contro else ""
        k_truoc = 0
        # gom ky tu theo buoc khung hinh de khong de ra qua nhieu dong ASS
        moi_lan = max(1, int(round((1 / cfg.FPS) / buoc)))
        k = 0
        while k < n:
            a = t0 + k * buoc
            k2 = min(n, k + moi_lan)
            b = t0 + k2 * buoc if k2 < n else t_xong
            self.trang_thai(a, b, kieu, x, y, truoc + [(chu[:k], "hien"), (ct, "contro"), (chu[k:], "an")] + sau)
            k = k2
        self.trang_thai(t_xong, t1, kieu, x, y, truoc + [(chu, "hien"), (ct, "contro_an")] + sau)

    def text(self):
        return "".join(self.out)


def phu_de(ve, cum, y_goc, tren_nen_sang=False):
    """cum: {t0, t1, nho, to}. y_goc = mep duoi dong to."""
    nho, to = cum["nho"].strip(), cum["to"].strip()
    t0, t1 = cum["t0"], cum["t1"]
    if tren_nen_sang:
        ve.mau = mau_ass(cfg.MAU["chu_toi"])
    if nho and to:
        ti_le = len(nho) / float(len(nho) + len(to))
        t_to = min(t1 - 0.25, max(t0 + 0.18, cum.get("t_to") or (t0 + ti_le * (cum["t_noi"] - t0))))
        go_xong = min(t_to - 0.02, t0 + max(0.18, len(nho) * 0.022))
        ve.go(t0, go_xong, t_to, "Nho", 540, y_goc - 134, nho, 64, contro=True)
        ve.trang_thai(t_to, t1, "Nho", 540, y_goc - 134, [(nho, "hien")])
        ve.trang_thai(t_to, t1, "To", 540, y_goc, [(to, "vao")])
    elif nho:
        go_xong = min(t0 + max(0.2, len(nho) * 0.032), t0 + 0.7 * (t1 - t0))
        ve.go(t0, go_xong, t1, "Nho", 540, y_goc - 40, nho, 64, contro=True)
    elif to:
        ve.trang_thai(t0, t1, "To", 540, y_goc, [(to, "vao")])
    ve.mau = mau_ass(cfg.MAU["chu_trang"])


def the_chu(D, nen, tieu_de, phu):
    """The toan man hinh: dau muc to hien mo dan, chu nho ben duoi hien tung tu."""
    mau = cfg.MAU["chu_toi"] if nen == "trang" else cfg.MAU["chu_trang"]
    ve = Ve(mau, bong=False)
    y = int(PY * 0.46)
    ve.trang_thai(0, D, "TheTieuDe", 540, y, [(tieu_de, "vao")])
    tu = phu.split()
    if tu:
        bat_dau, het = 0.35, max(0.5, D - 0.45)
        buoc = (het - bat_dau) / len(tu)
        for k in range(len(tu)):
            a = bat_dau + k * buoc
            b = bat_dau + (k + 1) * buoc if k < len(tu) - 1 else D
            phan = [(" ".join(tu[:k]) + (" " if k else ""), "hien"), (tu[k], "vao"),
                    ((" " + " ".join(tu[k + 1:])) if k < len(tu) - 1 else "", "an")]
            ve.trang_thai(a, b, "ThePhu", 540, y + 100, phan)
    return dau_file() + ve.text()


def the_danh_sach(D, nen, tieu_de, cac_dong, moc=None):
    """Tieu de go ra truoc, tung dong go lan luot. moc: giay bat dau tung dong (tuy chon)."""
    mau = cfg.MAU["chu_toi"] if nen == "trang" else cfg.MAU["chu_trang"]
    ve = Ve(mau, bong=False)
    x = 110
    y = int(PY * 0.34) if tieu_de else int(PY * 0.44)
    if tieu_de:
        ve.go(0.05, min(0.6, 0.3 * D), D, "DsTieuDe", x, y, tieu_de, 76, contro=False)
        y += 150
    n = len(cac_dong)
    if n:
        bd, het = (0.7 if tieu_de else 0.15), max(1.0, D - 0.6)
        for k, c in enumerate(cac_dong):
            a = moc[k] if moc and k < len(moc) and moc[k] is not None else bd + k * (het - bd) / n
            ve.go(a, min(D - 0.1, a + max(0.25, len(c) * 0.03)), D, "DsDong", x, y + k * 100, c, 58, contro=False)
    return dau_file() + ve.text()


def nhan_anh(D, nen, nhan):
    """nhan: list (chu, x, y, t_hien)."""
    mau = cfg.MAU["chu_toi"] if nen == "trang" else cfg.MAU["chu_trang"]
    ve = Ve(mau, bong=False)
    for chu, x, y, t in nhan:
        if chu:
            ve.trang_thai(t, D, "Nhan", x, y, [(chu, "vao")])
    return dau_file() + ve.text()


def srt(cum):
    def ts(s):
        ms = int(round(s * 1000))
        return "{:02d}:{:02d}:{:02d},{:03d}".format(ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)
    out = []
    for k, c in enumerate(cum, 1):
        chu = (c["nho"] + ("\n" + c["to"] if c["to"] else "")).strip()
        out.append("{}\n{} --> {}\n{}\n".format(k, ts(c["t0"]), ts(c["t1"]), chu))
    return "\n".join(out)
