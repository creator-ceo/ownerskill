# -*- coding: utf-8 -*-
"""Dong co chu HyperFrames (HeyGen, Apache-2.0): ve lop CHU + THE thanh MOV trong suot bang trinh duyet.

Thay cho ASS (chu.py) khi may co HyperFrames: bong chu mem that, mo-net that, the anh bo goc bang CSS.
Mot lan dung ra MOT file ProRes 4444 co kenh trong suot, dai bang ca video, chua:
  - phu de 2 tang (go tung chu co con tro · cum nhan hien mo dan)
  - the chu, the danh sach, the anh bang chung (the nen dac - che A-roll trong luc hien)
B-roll van do ffmpeg lo (chen.py) - xu ly video trong trinh duyet cham va khong can.

Cai dat (mot lan, ~130 MB, nam ngoai thu muc skill):  python3 dv.py cai-hf
Luat viet canh cua HyperFrames: timeline GSAP duy nhat, dung ban ` { paused: true } `,
khong tween visibility tren .clip, font phai co @font-face tro toi file that.
"""
import os, sys, json, shutil, subprocess, html
sys.dont_write_bytecode = True
import cfg

PX, PY = 1080, 1920
BAN_HF = "0.8.74"


def thu_muc_hf():
    return cfg.thu_muc_cong_cu(".hyperframes")


def lenh_hf():
    p = os.path.join(thu_muc_hf(), "node_modules", ".bin", "hyperframes")
    return p if os.path.exists(p) else None


def gsap_js():
    p = os.path.join(thu_muc_hf(), "node_modules", "gsap", "dist", "gsap.min.js")
    return p if os.path.exists(p) else None


def co_san():
    return bool(lenh_hf() and gsap_js())


def ffprobe():
    """ffprobe that neu may co; khong thi ban thu gon ffprobe_gon.py (xem ly do trong file do)."""
    that = shutil.which("ffprobe")
    for p in ("/opt/homebrew/bin/ffprobe", "/usr/local/bin/ffprobe", os.path.expanduser("~/.local/bin/ffprobe")):
        if not that and os.path.exists(p):
            that = p
    if that:
        return that
    boc = os.path.join(thu_muc_hf(), "bin", "ffprobe")
    goc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffprobe_gon.py")
    noi_dung = '#!/bin/sh\nexec "{}" "{}" "$@"\n'.format(sys.executable, goc)
    if not os.path.exists(boc) or open(boc).read() != noi_dung:
        os.makedirs(os.path.dirname(boc), exist_ok=True)
        open(boc, "w").write(noi_dung)
        os.chmod(boc, 0o755)
    return boc


def cai():
    """Cai HyperFrames + GSAP (tai tu npm, ~130 MB) vao <thu muc du lieu>/.hyperframes - ngoai thu muc skill."""
    if not shutil.which("npm"):
        sys.exit("!! Can Node.js (lenh npm) de cai HyperFrames. Tai tai nodejs.org roi chay lai.")
    d = thu_muc_hf()
    os.makedirs(d, exist_ok=True)
    pj = os.path.join(d, "package.json")
    if not os.path.exists(pj):
        open(pj, "w").write('{"name": "dung-video-hf", "private": true}\n')
    r = subprocess.run(["npm", "install", "hyperframes@" + BAN_HF, "gsap@3", "--no-audit", "--no-fund"],
                       cwd=d, capture_output=True, text=True)
    print(r.stdout[-400:] + r.stderr[-400:])
    # tat thong ke gui ve nha phat trien HyperFrames
    if lenh_hf():
        subprocess.run([lenh_hf(), "telemetry", "disable"], cwd=d, capture_output=True)
    print("HyperFrames:", "san sang" if co_san() else "CHUA CAI DUOC")
    print("!! Dung chay 'hyperframes init': lenh do tu cai them skill vao ~/.agents/skills. dv.py chi goi 'render'.")


def e(s):
    return html.escape(s or "", quote=True)


_font_cache = {}


def co_vua(chu, file_font, co_max, rong_max, co_min, gian=0.0):
    """Co chu lon nhat (<= co_max) de `chu` nam tron MOT dong trong rong_max px - do bang chinh file font.
    gian = letter-spacing (px, am la khit lai). Chu nghieng gia lap rong hon ~4%."""
    from PIL import ImageFont
    co = co_max
    while co > co_min:
        k = (file_font, co)
        if k not in _font_cache:
            _font_cache[k] = ImageFont.truetype(os.path.join(cfg.FONTS, file_font), co)
        rong = _font_cache[k].getlength(chu) * 1.04 + gian * max(0, len(chu) - 1)
        if rong <= rong_max:
            break
        co -= 4
    return co


def mau_css(hex6):
    return "#" + hex6.lstrip("#")


class Canh:
    """Gom HTML + cac lenh GSAP cho mot composition."""

    def __init__(self):
        self.html, self.js, self.n = [], [], 0

    def id(self, tien_to):
        self.n += 1
        return "{}{}".format(tien_to, self.n)

    def go_chu(self, chu, t0, t_xong, t_an_contro, lop="", contro=True):
        """Tra HTML dong chu tach tung ky tu; them lenh hien dan tung ky tu (+ con tro di theo)."""
        did = self.id("g")
        ky = list(chu)
        n = max(1, len(ky))
        buoc = max(0.012, (t_xong - t0) / n)
        phan = ['<span class="dong {}" id="{}">'.format(lop, did)]
        if contro:
            phan.append('<span class="ct ct0" id="{}c0"></span>'.format(did))
        for k, c in enumerate(ky):
            cc = "&nbsp;" if c == " " else e(c)
            cur = '<span class="ct" id="{}c{}"></span>'.format(did, k + 1) if contro else ""
            phan.append('<span class="ch{}" id="{}k{}">{}{}</span>'.format(" sp" if c == " " else "", did, k, cc, cur))
        phan.append("</span>")
        if contro:
            self.js.append('tl.set("#{d}c0",{{opacity:1}},{t:.3f});'.format(d=did, t=t0))
        for k in range(len(ky)):
            t = t0 + k * buoc
            self.js.append('tl.set("#{d}k{k}",{{opacity:1}},{t:.3f});'.format(d=did, k=k, t=t))
            if contro:
                self.js.append('tl.set("#{d}c{a}",{{opacity:0}},{t:.3f});tl.set("#{d}c{b}",{{opacity:1}},{t:.3f});'.format(
                    d=did, a=k, b=k + 1, t=t))
        if contro:
            self.js.append('tl.set("#{d}c{k}",{{opacity:0}},{t:.3f});'.format(d=did, k=len(ky), t=t_an_contro))
        return "".join(phan)

    def hien_mo(self, el_id, t, dai=0.24, mo=14, phong=1.06, y=0):
        self.js.append('tl.fromTo("#{i}",{{opacity:0,filter:"blur({m}px)",scale:{p},y:{y}}},'
                       '{{opacity:1,filter:"blur(0px)",scale:1,y:0,duration:{d},ease:"power2.out"}},{t:.3f});'.format(
                           i=el_id, m=mo, p=phong, y=y, d=dai, t=t))


def phu_de(c, cum, y_goc, tren=False, toi=False):
    """cum: {t0, t1, t_noi, nho, to}. y_goc = mep duoi dong to (toa do 1080x1920)."""
    nho, to = cum["nho"].strip(), cum["to"].strip()
    t0, t1 = cum["t0"], cum["t1"]
    if t1 - t0 < 0.05:
        return
    lop = "cap" + (" toi" if toi else "")
    trong = []
    if nho and to:
        ti_le = len(nho) / float(len(nho) + len(to))
        t_to = min(t1 - 0.25, max(t0 + 0.18, t0 + ti_le * (cum["t_noi"] - t0)))
        go_xong = min(t_to - 0.02, t0 + max(0.18, len(nho) * 0.022))
        trong.append(c.go_chu(nho, t0, go_xong, t_to, "nho"))
        tid = c.id("to")
        trong.append('<span class="to" id="{}" style="font-size:{}px">{}</span>'.format(
            tid, co_vua(to, "BeVietnamPro-ExtraBold.ttf", 128, 930, 64, -2), e(to)))
        c.hien_mo(tid, t_to)
    elif nho:
        go_xong = min(t0 + max(0.2, len(nho) * 0.032), t0 + 0.7 * (t1 - t0))
        trong.append(c.go_chu(nho, t0, go_xong, go_xong + 0.25, "nho"))
    elif to:
        tid = c.id("to")
        trong.append('<span class="to" id="{}" style="font-size:{}px">{}</span>'.format(
            tid, co_vua(to, "BeVietnamPro-ExtraBold.ttf", 128, 930, 64, -2), e(to)))
        c.hien_mo(tid, t0)
    vi_tri = "top:{}px".format(int(y_goc - 190)) if tren else "bottom:{}px".format(PY - y_goc - 30)
    c.html.append('<div class="clip {}" data-start="{:.3f}" data-duration="{:.3f}"><div class="khoi" style="{}">{}</div></div>'.format(
        lop, t0, t1 - t0, vi_tri, "".join(trong)))


# ---- chuyen canh vao/ra cua the ----
# Khung the nam tren lop trong suot -> trong luc chuyen canh, A-roll ben duoi lo ra = chuyen canh that.
# Cac kieu: cat (khong hieu ung) · mo · truot · phong · lac (truot nhanh + nhoe chuyen dong) · nhoe
KIEU_CC = ("cat", "mo", "truot", "phong", "lac", "nhoe")


def chuyen_canh(c, kid, t0, D, vao, ra, dai=0.3):
    dai = min(dai, D / 3.0)
    d_lac = min(0.22, dai)
    tu = {"mo": ("{opacity:0}", "{opacity:1"),
          "truot": ("{xPercent:100}", "{xPercent:0"),
          "phong": ("{opacity:0,scale:1.15}", "{opacity:1,scale:1"),
          "lac": ('{xPercent:100,filter:"blur(28px)"}', '{xPercent:0,filter:"blur(0px)"'),
          "nhoe": ('{opacity:0,filter:"blur(34px)"}', '{opacity:1,filter:"blur(0px)"')}
    di = {"mo": ("{opacity:1}", "{opacity:0"),
          "truot": ("{xPercent:0}", "{xPercent:-100"),
          "phong": ("{opacity:1,scale:1}", "{opacity:0,scale:1.08"),
          "lac": ('{xPercent:0,filter:"blur(0px)"}', '{xPercent:-100,filter:"blur(28px)"'),
          "nhoe": ('{opacity:1,filter:"blur(0px)"}', '{opacity:0,filter:"blur(34px)"')}
    if vao in tu:
        dd = d_lac if vao == "lac" else dai
        c.js.append('tl.fromTo("#{k}",{a},{b},duration:{d:.3f},ease:"{e}"}},{t:.3f});'.format(
            k=kid, a=tu[vao][0], b=tu[vao][1], d=dd, e="power4.out" if vao == "lac" else "power2.out", t=t0))
    if ra in di:
        dd = d_lac if ra == "lac" else dai
        c.js.append('tl.fromTo("#{k}",{a},{b},duration:{d:.3f},ease:"{e}"}},{t:.3f});'.format(
            k=kid, a=di[ra][0], b=di[ra][1], d=dd, e="power4.in" if ra == "lac" else "power2.in", t=t0 + D - dd))


def the_chu(c, t0, D, nen, tieu_de, phu):
    tid = c.id("td")
    tu = (phu or "").split()
    ds = []
    bat_dau, het = 0.35, max(0.5, D - 0.45)
    buoc = (het - bat_dau) / max(1, len(tu))
    for k, w in enumerate(tu):
        wid = c.id("w")
        ds.append('<span class="tu" id="{}">{}</span>'.format(wid, e(w)))
        c.hien_mo(wid, t0 + bat_dau + k * buoc, dai=0.22, mo=6, phong=1.0, y=10)
    c.html.append('<div class="clip the" data-start="{t:.3f}" data-duration="{d:.3f}"><div class="the-khung nen-{n}" id="{k}">'
                  '<div class="giua"><div class="tieu-de" id="{i}" style="font-size:{co}px">{td}</div><div class="phu">{p}</div></div></div></div>'.format(
                      n=nen, t=t0, d=D, i=tid, td=e(tieu_de), p=" ".join(ds), k=c.khung_the,
                      co=co_vua(tieu_de, "BeVietnamPro-ExtraBold.ttf", 150, 950, 80, -3)))
    c.hien_mo(tid, t0 + 0.02, dai=0.32)


def the_danh_sach(c, t0, D, nen, tieu_de, dong, moc=None):
    trong = []
    if tieu_de:
        trong.append('<div class="ds-td">{}</div>'.format(c.go_chu(tieu_de, t0 + 0.05, t0 + min(0.6, 0.3 * D), 0, contro=False)))
    n = len(dong)
    bd, het = (0.7 if tieu_de else 0.15), max(1.0, D - 0.6)
    for k, s in enumerate(dong):
        a = moc[k] if moc and k < len(moc) and moc[k] is not None else bd + k * (het - bd) / max(1, n)
        trong.append('<div class="ds-dong">{}</div>'.format(
            c.go_chu(s, t0 + a, t0 + min(D - 0.1, a + max(0.25, len(s) * 0.03)), 0, contro=False)))
    c.html.append('<div class="clip the" data-start="{t:.3f}" data-duration="{d:.3f}"><div class="the-khung nen-{n}" id="{k}"><div class="ds{g}">{x}</div></div></div>'.format(
        n=nen, t=t0, d=D, g="" if tieu_de else " ds-giua", x="".join(trong), k=c.khung_the))


def the_anh(c, t0, D, nen, files, nhan, nghieng=True):
    """1-3 anh bo goc bang CSS; anh ngang xep chong doc, anh doc xep canh nhau."""
    from PIL import Image
    n = min(3, len(files))
    kt = [Image.open(f).size for f in files[:n]]
    ngang = sum(1 for w, h in kt if w > h) * 2 >= n
    goc = [0] if n == 1 else ([-3, 3] if n == 2 else [-4, 2, -2])
    buoc = min(0.6, max(0.25, (D - 0.8) / max(1, n)))
    o = []
    for k in range(n):
        if ngang and n > 1:
            w_max, h_max = 860, {2: 560, 3: 400}[n]
            cx, cy = 540, (PY * ([0.43, 0.77] if n == 2 else [0.37, 0.61, 0.85])[k])
        else:
            w_max, h_max = {1: 860, 2: 470, 3: 320}[n], {1: 1250, 2: 1000, 3: 820}[n]
            cx, cy = PX * ([0.5] if n == 1 else ([0.27, 0.73] if n == 2 else [0.18, 0.5, 0.82]))[k], PY * 0.55
        w, h = kt[k]
        tl_ = min(w_max / w, h_max / h)
        ww, hh = int(w * tl_), int(h * tl_)
        aid = c.id("a")
        g = goc[k] if nghieng else 0
        chu_nhan = nhan[k] if k < len(nhan) else ""
        o.append('<div class="anh" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                 '<img src="img/{f}" alt="">{lb}</div>'.format(
                     i=aid, x=int(cx - ww / 2), y=int(cy - hh / 2), w=ww, h=hh, f=os.path.basename(files[k]),
                     lb='<div class="nhan-anh">{}</div>'.format(e(chu_nhan)) if chu_nhan else ""))
        c.js.append('tl.fromTo("#{i}",{{opacity:0,y:40,scale:0.95,rotation:{g}}},{{opacity:1,y:0,scale:1,rotation:{g},'
                    'duration:0.32,ease:"power3.out"}},{t:.3f});'.format(i=aid, g=g, t=t0 + 0.1 + k * buoc))
    c.html.append('<div class="clip the" data-start="{t:.3f}" data-duration="{d:.3f}"><div class="the-khung nen-{n}" id="{k}">{x}</div></div>'.format(
        n=nen, t=t0, d=D, x="".join(o), k=c.khung_the))


CSS = """
@font-face{font-family:"BVP";src:url("fonts/BeVietnamPro-Medium.ttf");font-weight:500}
@font-face{font-family:"BVP";src:url("fonts/BeVietnamPro-SemiBold.ttf");font-weight:600}
@font-face{font-family:"BVP";src:url("fonts/BeVietnamPro-ExtraBold.ttf");font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:transparent}
#root{position:relative;width:100%;height:100%;font-family:"BVP",sans-serif}
.clip{position:absolute;inset:0}
.khoi{position:absolute;left:70px;right:70px;text-align:center;color:#fff}
.cap .dong,.cap .to{display:block;text-shadow:0 5px 22px rgba(0,0,0,.55),0 2px 4px rgba(0,0,0,.35)}
.cap.toi .khoi{color:#111}
.cap.toi .dong,.cap.toi .to{text-shadow:none}
.nho{font-weight:600;font-size:64px;line-height:1.18;letter-spacing:-.5px}
.to{font-weight:800;font-style:italic;font-size:128px;line-height:1.05;letter-spacing:-2px;margin-top:6px;opacity:0}
.ch{opacity:0;position:relative}
.ct{position:absolute;left:100%;top:.1em;width:.42em;height:.95em;background:currentColor;opacity:0;margin-left:2px}
.ct0{position:relative;display:inline-block;left:0;top:.12em;vertical-align:top}
.the .ct{display:none}
.the-khung{position:absolute;inset:0;overflow:hidden}
.nen-trang{background:#faf9f6;color:#111}
.nen-den{background:#000;color:#fff}
.giua{position:absolute;left:60px;right:60px;top:46%;transform:translateY(-50%);text-align:center}
.tieu-de{display:block;font-weight:800;font-size:150px;line-height:1;letter-spacing:-3px;opacity:0}
.phu{margin-top:10px;font-weight:500;font-size:56px}
.tu{display:inline-block;opacity:0;margin:0 10px}
.ds{position:absolute;left:110px;right:90px;top:34%}
.ds-giua{top:44%}
.ds-td{font-weight:800;font-size:76px;line-height:1.2;margin-bottom:40px}
.ds-dong{font-weight:600;font-style:italic;font-size:58px;line-height:1.25;margin-bottom:26px}
.anh{position:absolute;opacity:0}
.anh img{display:block;width:100%;height:100%;object-fit:cover;border-radius:26px;box-shadow:0 18px 44px rgba(0,0,0,.45)}
.nen-trang .anh img{box-shadow:0 14px 34px rgba(0,0,0,.18)}
.nhan-anh{position:absolute;left:0;right:0;bottom:100%;margin-bottom:22px;text-align:center;font-weight:600;font-size:52px}
"""


def dung_lop(d, cum_ok, the_ds, tong, y_goc, dich, nhap=False):
    """Viet composition vao tam/hf/ roi render MOV trong suot. the_ds: [{loai,t0,t1,c}]"""
    if not co_san():
        sys.exit("!! Chua cai HyperFrames. Chay: python3 dv.py cai-hf  (hoac dat \"dong_co\": \"ass\")")
    pd = os.path.join(d, "tam", "hf")
    if os.path.isdir(pd):
        shutil.rmtree(pd)
    for x in ("fonts", "img"):
        os.makedirs(os.path.join(pd, x))
    for f in ("BeVietnamPro-Medium.ttf", "BeVietnamPro-SemiBold.ttf", "BeVietnamPro-ExtraBold.ttf"):
        shutil.copy(os.path.join(cfg.FONTS, f), os.path.join(pd, "fonts", f))
    shutil.copy(gsap_js(), os.path.join(pd, "gsap.min.js"))

    c = Canh()
    for x in the_ds:
        cc, D = x["c"], x["t1"] - x["t0"]
        nen = cfg.nen_cua(cc)
        c.khung_the = c.id("k")
        chuyen_canh(c, c.khung_the, x["t0"], D, x.get("vao", "cat"), x.get("ra", "cat"), x.get("dai_cc", 0.3))
        if x["loai"] == "the":
            the_chu(c, x["t0"], D, nen, cc.get("tieu_de", ""), cc.get("phu", ""))
        elif x["loai"] == "danh_sach":
            the_danh_sach(c, x["t0"], D, nen, cc.get("tieu_de", ""), cc.get("dong", []), cc.get("_moc_dong"))
        elif x["loai"] == "anh":
            files = cc["file"] if isinstance(cc["file"], list) else [cc["file"]]
            files = [cfg.duong_dan(d, f) for f in files]
            for f in files:
                if not os.path.exists(f):
                    sys.exit("!! Khong thay anh: " + f)
                _anh_nho(f, os.path.join(pd, "img", os.path.basename(f)))
            nhan = cc.get("nhan", [])
            the_anh(c, x["t0"], D, nen, files, [nhan] if isinstance(nhan, str) else nhan, cc.get("nghieng", True))
    for cum in cum_ok:
        tren = cum.get("tren")
        if tren and tren["loai"] == "anh":
            phu_de(c, cum, int(PY * 0.17), tren=True, toi=(tren["nen"] == "trang"))
        else:
            phu_de(c, cum, y_goc)

    trang = ('<!doctype html>\n<html lang="vi"><head><meta charset="UTF-8">'
             '<meta name="viewport" content="width=1080, height=1920">'
             '<script src="gsap.min.js"></script><style>{css}</style></head><body>\n'
             '<div id="root" data-composition-id="lopchu" data-start="0" data-duration="{T:.3f}" data-width="1080" data-height="1920">\n'
             '{h}\n</div>\n<script>\nconst tl = gsap.timeline({{ paused: true }});\n{j}\n'
             'window.__timelines["lopchu"] = tl;\ntl.seek(0);\n</script>\n</body></html>\n').format(
        css=CSS, T=tong, h="\n".join(c.html), j="\n".join(c.js))
    open(os.path.join(pd, "index.html"), "w", encoding="utf-8").write(trang)
    open(os.path.join(pd, "meta.json"), "w").write('{"id": "lopchu", "name": "lopchu"}\n')

    env = dict(os.environ)
    env["HYPERFRAMES_NO_TELEMETRY"] = "1"
    env["HYPERFRAMES_FFPROBE_PATH"] = ffprobe()
    env["HYPERFRAMES_FFMPEG_PATH"] = cfg.ffmpeg()
    lenh = [lenh_hf(), "render", pd, "--format", "mov", "-o", dich, "--fps", str(cfg.FPS),
            "-q", "draft" if nhap else "looks", "--quiet"]
    print("Ve lop chu bang HyperFrames: {} dong phu de, {} the ({:.0f}s)...".format(len(cum_ok), len(the_ds), tong))
    r = subprocess.run(lenh, cwd=thu_muc_hf(), capture_output=True, text=True, env=env)
    if r.returncode != 0 or not os.path.exists(dich):
        print("\n".join((r.stdout + "\n" + r.stderr).strip().splitlines()[-30:]))
        sys.exit("!! HyperFrames render loi. Composition o: " + pd)
    return pd


def _anh_nho(src, dich, canh_dai=1600):
    """Anh to qua thi thu nho truoc - trinh duyet khong phai giai ma anh 4000px moi khung."""
    from PIL import Image
    im = Image.open(src)
    if max(im.size) > canh_dai:
        im.thumbnail((canh_dai, canh_dai))
        im.convert("RGB").save(dich, quality=92)
    else:
        shutil.copy(src, dich)
