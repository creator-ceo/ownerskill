# -*- coding: utf-8 -*-
"""Cau hinh chung cho dung-video: duong dan, ffmpeg, doc bang dung.

Du lieu (video, am thanh, ban dung) KHONG nam trong thu muc skill hay trong repo git nao:
file video nang, lot vao repo la rat kho go. Mac dinh: ~/CreatorVideo/dung/<ten>/.
Doi goc bang bien moi truong CREATOR_VIDEO_HOME (vd: export CREATOR_VIDEO_HOME=/Volumes/O-Ngoai/CreatorVideo).
Cau hinh duy nhat: ~/.creator-video/ho-so.json (tuy chon) - truong "ten_kenh" duoc them vao goi y cho may nghe.
"""
import os, sys, json, re, shutil, subprocess
sys.dont_write_bytecode = True   # khong de __pycache__ trong thu muc skill

BO_MAY = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(BO_MAY)
FONTS = os.path.join(SKILL, "fonts")                          # Be Vietnam Pro (OFL) - kem san
HO_SO = os.path.expanduser("~/.creator-video/ho-so.json")

W, H, FPS = 1080, 1920, 30

# Mau nen the chu: "den" (den) hoac "trang" (trang nga). Phu de luon chu trang; tren nen trang thi chu toi.
MAU = {"trang": "faf9f6", "den": "000000", "chu_trang": "ffffff", "chu_toi": "111111"}


def nen_cua(c):
    """'nen' cua mot canh chen -> 'trang' | 'den' (gia tri la thi coi nhu den)."""
    return "trang" if str(c.get("nen", "den")).lower() == "trang" else "den"


def goc():
    """Thu muc goc cua moi du lieu: $CREATOR_VIDEO_HOME, mac dinh ~/CreatorVideo."""
    return os.path.abspath(os.path.expanduser(os.environ.get("CREATOR_VIDEO_HOME") or "~/CreatorVideo"))


def ho_so():
    """Doc ~/.creator-video/ho-so.json neu co. Loi hay khong co file -> {}."""
    try:
        with open(HO_SO, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def trong_repo_git(p):
    p = os.path.abspath(p)
    while True:
        if os.path.exists(os.path.join(p, ".git")):
            return p
        cha = os.path.dirname(p)
        if cha == p:
            return None
        p = cha


def goc_lam_viec():
    """Noi chua cac du an dung video: <goc>/dung/."""
    g = os.path.join(goc(), "dung")
    repo = trong_repo_git(g)
    if repo:
        sys.exit("!! Thu muc du lieu {} nam trong repo git {}.\n"
                 "   Dat CREATOR_VIDEO_HOME ra ngoai repo, vd: export CREATOR_VIDEO_HOME=~/CreatorVideo".format(g, repo))
    return g


def thu_muc_cong_cu(ten):
    """Cong cu tai ve (HyperFrames, model nghe) nam o <goc>/<ten>, dung chung cho moi du an."""
    return os.path.join(goc(), ten)


def du_an(ten, tao=False):
    d = os.path.join(goc_lam_viec(), ten)
    if tao:
        os.makedirs(d, exist_ok=True)
    elif not os.path.isdir(d):
        sys.exit("Chua co du an '{}'. Tao bang: python3 dv.py moi {} <file video>".format(ten, ten))
    return d


def ffmpeg():
    for p in (shutil.which("ffmpeg"), os.path.expanduser("~/.local/bin/ffmpeg"),
              "/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if p and os.path.exists(p):
            return p
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit("Khong tim thay ffmpeg. Cai bang: brew install ffmpeg  (hoac: pip3 install imageio-ffmpeg)")


def moi_truong():
    """ffmpeg ban tinh (imageio) khong co fontconfig config -> tao file toi thieu cho libass."""
    env = dict(os.environ)
    conf = os.path.join(goc_lam_viec(), ".fonts.conf")
    if not os.path.exists(conf):
        os.makedirs(os.path.dirname(conf), exist_ok=True)
        open(conf, "w").write('<?xml version="1.0"?><fontconfig><dir>{}</dir><dir>/System/Library/Fonts</dir>'
                              '<cachedir>{}</cachedir></fontconfig>'.format(FONTS, os.path.join(goc_lam_viec(), ".fc-cache")))
    env["FONTCONFIG_FILE"] = conf
    return env


def chay(lenh, im=False):
    """Chay ffmpeg; loi thi in 25 dong cuoi va dung."""
    if not im:
        print("  $ " + " ".join(os.path.basename(x) if i == 0 else x for i, x in enumerate(lenh))[:300])
    r = subprocess.run(lenh, capture_output=True, text=True, env=moi_truong())
    if r.returncode != 0:
        print("\n".join(r.stderr.strip().splitlines()[-25:]))
        sys.exit("!! Lenh loi (ma {})".format(r.returncode))
    return r


def thong_so(path):
    """Do dai, kich thuoc, co tieng khong - doc tu ffmpeg -i (khong can ffprobe)."""
    r = subprocess.run([ffmpeg(), "-hide_banner", "-i", path], capture_output=True, text=True)
    t = r.stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", t)
    dai = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0
    v = re.search(r"Video: .*?(\d{2,5})x(\d{2,5})", t)
    xoay = re.search(r"rotate\s*:\s*(-?\d+)|rotation of (-?[\d.]+)", t)
    w, h = (int(v.group(1)), int(v.group(2))) if v else (0, 0)
    if xoay and abs(int(float(xoay.group(1) or xoay.group(2)))) in (90, 270):
        w, h = h, w
    return {"dai": dai, "w": w, "h": h, "tieng": "Audio:" in t}


def doc_json(p, mac_dinh=None):
    if not os.path.exists(p):
        return mac_dinh
    return json.load(open(p, encoding="utf-8"))


def ghi_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def khoang(s):
    """'12-20' | [12,20] | 12 -> (12, 20)"""
    if isinstance(s, (list, tuple)):
        return int(s[0]), int(s[-1])
    if isinstance(s, int):
        return s, s
    a, _, b = str(s).partition("-")
    return int(a), int(b or a)


def duong_dan(d, p):
    """Duong dan trong bang dung: tuyet doi, ~/..., hoac tuong doi voi thu muc du an."""
    p = os.path.expanduser(p)
    return p if os.path.isabs(p) else os.path.join(d, p)


def duong_lut(d, gia_tri):
    """'lut' trong bang dung -> duong dan file .cube cua chinh nguoi dung, hoac None (giu mau goc)."""
    if not gia_tri:
        return None
    p = duong_dan(d, gia_tri)
    if not p.lower().endswith(".cube"):
        sys.exit("!! 'lut' phai tro toi file .cube: " + p)
    if not os.path.exists(p):
        sys.exit("!! Khong thay file LUT: " + p)
    return p


def lut_cua_file(d, bd, f):
    """LUT cho file goc thu f: 'lut' la mot duong dan (ap chung) hoac danh sach theo thu tu 'nguon'."""
    l = bd.get("lut")
    if isinstance(l, list):
        l = l[f] if f < len(l) else None
    return duong_lut(d, l)


def tg(s):
    """giay -> 01:02.3"""
    return "{:02d}:{:04.1f}".format(int(s // 60), s % 60)
