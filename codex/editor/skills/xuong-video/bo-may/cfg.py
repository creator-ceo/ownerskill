#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cau hinh dung chung cho ca bo may - tu nhan biet macOS hay Windows.

    python3 cfg.py                                   kiem tra may nay
    python3 cfg.py --khai "<thu muc footage>"        khai thu muc footage (lan dau dung)
    python3 cfg.py --khai "<thu muc footage>" --lam "<thu muc lam viec>"

File cau hinh: ~/.creator-video/kho.json  (rieng tung may)
    {
      "o_goc":     "<thu muc chua footage goc - skill chi DOC, khong sua>",
      "work_root": "<thu muc lam viec: catalog.db, proxy/, xuat/ - mac dinh ~/CreatorVideo/kho>",
      "mui_gio":   7      (khong bat buoc - chi khai khi quay o mui gio khac mui gio cua may)
    }
Chay thu tren kho gia: dat bien moi truong KHO_VIDEO_CONFIG tro toi mot file cau hinh khac.

Vi sao cau hinh nam o thu muc nha chu khong nam canh code: moi may mot o dia
khac nhau (Mac la /Volumes/..., Windows la D:\\) - de chung mot file thi hai may
ghi de len nhau.
"""
import os, json, sys, subprocess, argparse, unicodedata as ud

HERE = os.path.dirname(os.path.abspath(__file__))
WIN  = sys.platform.startswith("win")

FILE_CAU_HINH = os.path.join(os.path.expanduser("~"), ".creator-video", "kho.json")

_DEFAULT = {
    "o_goc": None,                        # bat buoc khai - khong doan thay nguoi dung
    "work_root": "~/CreatorVideo/kho",
    "mui_gio": None,
}

def _tim_file():
    for p in (os.environ.get("KHO_VIDEO_CONFIG"), FILE_CAU_HINH):
        if p and os.path.isfile(p):
            return p
    return None

def load():
    d = dict(_DEFAULT)
    f = _tim_file()
    if f:
        try:
            d.update(json.load(open(f, encoding="utf-8")))
        except Exception as e:
            print("!! Khong doc duoc {}: {}".format(f, e), file=sys.stderr)
    d["work_root"] = os.path.abspath(os.path.expanduser(d["work_root"]))
    if d.get("o_goc"):
        d["o_goc"] = os.path.abspath(os.path.expanduser(d["o_goc"]))
    d["_nguon"] = f
    return d

C = load()

HUONG_DAN_KHAI = ('Chua khai thu muc footage. Chay:\n'
                  '    python3 cfg.py --khai "<duong dan toi thu muc chua footage>"')

def can_o_goc():
    """Dung lai voi huong dan neu chua khai thu muc footage."""
    if not C.get("o_goc"):
        sys.exit(HUONG_DAN_KHAI)
    return C["o_goc"]

def N(s):
    """Chuan hoa dau tieng Viet ve dang lien (NFC) - macOS luu dang tach dau."""
    return ud.normalize("NFC", s or "")

def _nam_trong(con, cha):
    """True neu duong dan `con` nam trong (hoac trung) thu muc `cha`."""
    a = N(os.path.abspath(con)).replace("\\", "/").rstrip("/")
    b = N(os.path.abspath(cha)).replace("\\", "/").rstrip("/")
    if WIN: a, b = a.lower(), b.lower()
    return a == b or a.startswith(b + "/")

def trong_thu_muc(folder, thu_muc):
    """Thu muc trong kho (cot folder) co nam trong `thu_muc` khong. "Buoi 1" khong khop "Buoi 10"."""
    f, t = N(folder).replace("\\", "/"), N(thu_muc).replace("\\", "/").strip("/")
    if WIN: f, t = f.lower(), t.lower()
    return f == t or f.startswith(t + "/")

def rel(p, goc=None):
    """Khoa chung cho moi may: duong dan tuong doi so voi thu muc footage, NFC, dau '/'.
       File nam ngoai thu muc footage thi tra nguyen duong dan tuyet doi - de loi hien ra."""
    goc = N(os.path.abspath(goc or can_o_goc())).replace("\\", "/").rstrip("/")
    p = N(os.path.abspath(p)).replace("\\", "/")
    a, b = (p.lower(), goc.lower()) if WIN else (p, goc)
    if a == b: return ""
    if a.startswith(b + "/"): return p[len(goc) + 1:]
    return p

def ngoai_o_goc(p):
    k = rel(p)
    return k.startswith("/") or (len(k) > 1 and k[1] == ":")

def trong_git(p=None):
    """Goc repo git neu thu muc nam trong mot repo. Proxy va catalog.db rat nang -
       lot vao repo la bi day len cung code."""
    cur = os.path.abspath(p or C["work_root"])
    while True:
        if os.path.isdir(os.path.join(cur, ".git")): return cur
        nxt = os.path.dirname(cur)
        if nxt == cur: return None
        cur = nxt

def chot_thu_muc_lam():
    """Dung neu thu muc lam viec dat sai cho. Goi truoc moi buoc ghi du lieu nang."""
    g = trong_git()
    if g:
        sys.exit("!! Thu muc lam viec {} nam trong repo git {}.\n"
                 "   Proxy va catalog.db rat nang se bi dua len cung code. Doi work_root\n"
                 "   sang thu muc ngoai repo:  python3 cfg.py --khai \"<footage>\" --lam \"<thu muc khac>\""
                 .format(C["work_root"], g))
    if C.get("o_goc") and _nam_trong(C["work_root"], C["o_goc"]):
        sys.exit("!! Thu muc lam viec {} nam BEN TRONG thu muc footage {}.\n"
                 "   Lan quet sau se quet nham ca proxy nhu footage that. Doi work_root ra ngoai."
                 .format(C["work_root"], C["o_goc"]))
    os.makedirs(C["work_root"], exist_ok=True)

def dam_bao_goc(con):
    """Cot shot_at_raw / shot_src_raw giu gio GOC truoc moi lan sua, de --revert tra lai duoc."""
    cols = {r[1] for r in con.execute("PRAGMA table_info(media)")}
    if "shot_at_raw" not in cols:
        con.execute("ALTER TABLE media ADD COLUMN shot_at_raw TEXT")
    if "shot_src_raw" not in cols:
        con.execute("ALTER TABLE media ADD COLUMN shot_src_raw TEXT")
    con.execute("UPDATE media SET shot_at_raw = shot_at WHERE shot_at_raw IS NULL")
    con.execute("UPDATE media SET shot_src_raw = shot_src WHERE shot_src_raw IS NULL")
    con.commit()

def gio_dia_phuong(dt):
    """Doi moc gio CO mui gio (vd UTC) sang gio noi quay, bo thong tin mui gio.
       Mac dinh theo mui gio may nay. Quay o nuoc ngoai: khai "mui_gio": <so gio>."""
    import datetime as _d
    if dt.tzinfo is None: return dt
    mg = C.get("mui_gio")
    tz = _d.timezone(_d.timedelta(hours=float(mg))) if mg is not None else None
    return dt.astimezone(tz).replace(tzinfo=None)

def _resolve(base, rel_path):
    """Tim file that tren dia. macOS luu dau tieng Viet dang tach (NFD),
       Windows so khop ten file theo dung tung byte -> phai thu ca hai dang."""
    parts = N(rel_path).split("/")
    for norm in ("NFC", "NFD"):
        p = os.path.join(base, *[ud.normalize(norm, x) for x in parts])
        if os.path.exists(p): return p
    cur = base
    for part in parts:
        direct = os.path.join(cur, part)
        if os.path.exists(direct):
            cur = direct; continue
        want = ud.normalize("NFC", part); hit = None
        try:
            for e in os.listdir(cur):
                if ud.normalize("NFC", e) == want: hit = e; break
        except OSError:
            break
        if hit is None: break
        cur = os.path.join(cur, hit)
    else:
        return cur
    return os.path.join(base, *parts)

def src(rel_path):
    """Duong dan day du toi file goc trong thu muc footage."""
    return _resolve(can_o_goc(), rel_path)

def prox(rel_path):
    """Duong dan day du toi ban proxy."""
    return _resolve(os.path.join(C["work_root"], "proxy"), rel_path)

def db():
    return os.path.join(C["work_root"], "catalog.db")

def mo_kho(timeout=120):
    """Mo catalog.db da co. Chua co thi dung lai va chi cach tao."""
    import sqlite3
    if not os.path.exists(db()):
        sys.exit("Chua co kho o {}.\nNhap footage truoc:  python3 catalog.py scan \"<thu muc buoi quay>\"".format(db()))
    return sqlite3.connect(db(), timeout=timeout)

def co_bang(con, ten):
    return con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (ten,)).fetchone() is not None

_enc = _hw = None
def encoder():
    """Chon bo ma hoa nhanh nhat may nay co."""
    global _enc
    if _enc: return _enc
    try:
        out = subprocess.run(["ffmpeg","-hide_banner","-encoders"],
                             capture_output=True, timeout=30).stdout.decode("utf-8","replace")
    except Exception:
        out = ""
    for e in ("h264_videotoolbox","h264_nvenc","h264_qsv","h264_amf"):
        if e in out: _enc = e; break
    else:
        _enc = "libx264"
    return _enc

def hwaccel():
    """Cach giai ma phan cung, tra ve list de ghep vao lenh ffmpeg."""
    global _hw
    if _hw is not None: return _hw
    try:
        out = subprocess.run(["ffmpeg","-hide_banner","-hwaccels"],
                             capture_output=True, timeout=30).stdout.decode("utf-8","replace")
    except Exception:
        out = ""
    for h in ("videotoolbox","cuda","d3d11va","qsv"):
        if h in out: _hw = ["-hwaccel", h]; break
    else:
        _hw = []
    return _hw

def font():
    """Font de ghi chu len video."""
    for f in ("/System/Library/Fonts/Supplemental/Arial.ttf",
              "C:/Windows/Fonts/arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(f): return f
    return None

def co_ffmpeg():
    try:
        return subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=30).returncode == 0
    except Exception:
        return False

def khai(o_goc, lam=None):
    """Ghi file cau hinh. Kiem tra truoc, sai thi khong ghi gi."""
    o_goc = os.path.abspath(os.path.expanduser(o_goc))
    lam = os.path.abspath(os.path.expanduser(lam or _DEFAULT["work_root"]))
    if not os.path.isdir(o_goc):
        sys.exit("Khong thay thu muc footage: {}".format(o_goc))
    if _nam_trong(lam, o_goc):
        sys.exit("Thu muc lam viec {} nam BEN TRONG thu muc footage - chon cho khac.".format(lam))
    g = trong_git(lam)
    if g:
        sys.exit("Thu muc lam viec {} nam trong repo git {} - chon cho khac.".format(lam, g))
    dich = os.environ.get("KHO_VIDEO_CONFIG") or FILE_CAU_HINH
    cu = {}
    if os.path.isfile(dich):
        try: cu = json.load(open(dich, encoding="utf-8"))
        except Exception: cu = {}
    cu.update({"o_goc": o_goc, "work_root": lam})
    os.makedirs(os.path.dirname(dich), exist_ok=True)
    with open(dich, "w", encoding="utf-8") as fh:
        json.dump(cu, fh, ensure_ascii=False, indent=2)
    os.makedirs(lam, exist_ok=True)
    print("Da ghi cau hinh:", dich)
    print("  Thu muc footage (chi doc):", o_goc)
    print("  Thu muc lam viec         :", lam)

def kiem():
    print("He dieu hanh :", "Windows" if WIN else sys.platform)
    print("File cau hinh:", C["_nguon"] or "(chua co)")
    if C.get("o_goc"):
        print("Thu muc footage:", C["o_goc"], "(co)" if os.path.isdir(C["o_goc"]) else "(KHONG THAY)")
    else:
        print("Thu muc footage: (chua khai)")
    print("Thu muc lam  :", C["work_root"])
    print("Kho          :", db(), "(co)" if os.path.exists(db()) else "(chua co)")
    print("FFmpeg       :", "co" if co_ffmpeg() else "KHONG CO - cai FFmpeg truoc")
    print("Bo ma hoa    :", encoder())
    print("Giai ma cung :", " ".join(hwaccel()) or "(khong co)")
    print("Font         :", font() or "(khong co)")
    if not C.get("o_goc"):
        print("\n" + HUONG_DAN_KHAI)
    g = trong_git()
    if g:
        print("\n!! THU MUC LAM VIEC NAM TRONG REPO GIT:", g)
        print("   Proxy va catalog.db rat nang - se bi dua len cung code.")
        print("   Doi work_root sang thu muc ngoai repo.")
    if C.get("o_goc") and _nam_trong(C["work_root"], C["o_goc"]):
        print("\n!! THU MUC LAM VIEC NAM BEN TRONG THU MUC FOOTAGE - doi work_root ra ngoai.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Kiem tra may / khai thu muc footage")
    ap.add_argument("--khai", metavar="THU_MUC_FOOTAGE", help="khai thu muc chua footage goc (skill chi doc)")
    ap.add_argument("--lam", metavar="THU_MUC_LAM_VIEC", help="noi de catalog.db, proxy/, xuat/ (mac dinh ~/CreatorVideo/kho)")
    a = ap.parse_args()
    if a.khai:
        khai(a.khai, a.lam)
    else:
        kiem()
