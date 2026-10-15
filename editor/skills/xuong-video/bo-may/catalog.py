#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
catalog.py - Lap danh muc anh/video trong thu muc footage (chi DOC, khong sua file).

Cach dung:
    python3 catalog.py scan   "<thu muc buoi quay>"     # quet va lap chi muc
    python3 catalog.py report                            # xem tong quan kho
    python3 catalog.py events                            # tu chia thanh cac "buoi quay"
"""
import os, sys, re, sqlite3, subprocess, argparse, datetime
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg

DB_DEFAULT = cfg.db()

VIDEO_EXT = {".mp4",".mov",".m4v",".avi",".mkv",".mts",".m2ts",".mpg",".mpeg",".wmv",".flv",".3gp",".webm",".insv",".lrv"}
PHOTO_EXT = {".jpg",".jpeg",".heic",".heif",".png",".dng",".raw",".cr2",".cr3",".nef",".arw",".raf",".orf",".rw2",".tif",".tiff",".gif",".webp",".bmp"}
AUDIO_EXT = {".wav",".mp3",".m4a",".aac",".aiff",".flac"}
ALL_EXT = VIDEO_EXT | PHOTO_EXT | AUDIO_EXT

SKIP_DIRS = {".Spotlight-V100",".fseventsd",".Trashes",".TemporaryItems","$RECYCLE.BIN",
             "System Volume Information",".DocumentRevisions-V100",".DS_Store"}

# mdls tra ket qua theo thu tu ALPHABET cua ten field
MD_FIELDS = sorted([
    "kMDItemContentCreationDate",
    "kMDItemContentTypeTree",
    "kMDItemDurationSeconds",
    "kMDItemPixelWidth",
    "kMDItemPixelHeight",
    "kMDItemLatitude",
    "kMDItemLongitude",
    "kMDItemAcquisitionModel",
    "kMDItemAcquisitionMake",
    "kMDItemCodecs",
    "kMDItemTotalBitRate",
    "kMDItemAudioChannelCount",
])

SCHEMA = """
CREATE TABLE IF NOT EXISTS media (
  path TEXT PRIMARY KEY,
  name TEXT, ext TEXT, kind TEXT,
  size INTEGER, mtime REAL,
  shot_at TEXT,          -- thoi diem quay/chup (ISO)
  shot_src TEXT,         -- nguon lay thoi diem: ten-dji | exif | ffmpeg | filename | mtime
  duration REAL,
  width INTEGER, height INTEGER,
  lat REAL, lon REAL,
  camera TEXT, codec TEXT, bitrate REAL,
  has_audio INTEGER,
  folder TEXT,
  event_id INTEGER,
  scanned_at TEXT
);
CREATE INDEX IF NOT EXISTS i_shot ON media(shot_at);
CREATE INDEX IF NOT EXISTS i_kind ON media(kind);
CREATE INDEX IF NOT EXISTS i_ev   ON media(event_id);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY,
  start TEXT, end TEXT, n_items INTEGER, n_video INTEGER,
  total_dur REAL, total_size INTEGER,
  lat REAL, lon REAL, top_folder TEXT, label TEXT
);
"""

def db_open(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    con = sqlite3.connect(path, timeout=60)
    con.executescript(SCHEMA)
    return con

# ---------- doc metadata ----------
def read_mdls(path):
    """Doc metadata qua Spotlight (chi co tren macOS). Tra dict rong neu khong co."""
    if sys.platform != "darwin":
        return {}
    cmd = ["mdls", "-raw", "-nullMarker", ""]
    for f in MD_FIELDS:
        cmd += ["-name", f]
    cmd.append(path)
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=20).stdout.decode("utf-8", "replace")
    except Exception:
        return {}
    vals = out.split("\0")
    d = {}
    for k, v in zip(MD_FIELDS, vals):
        v = v.strip()
        if v and v != "(null)":
            d[k] = v
    return d

FF_DUR  = re.compile(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)")
FF_DIM  = re.compile(r"Video:.*?,\s*(\d{2,5})x(\d{2,5})")
FF_VCOD = re.compile(r"Video:\s*([a-zA-Z0-9_]+)")
FF_DATE = re.compile(r"creation_time\s*:\s*([0-9T:\-\.Z]+)")
FF_LOC  = re.compile(r"location\s*:\s*([+\-][\d.]+)([+\-][\d.]+)")

def read_ffmpeg(path):
    """Doc metadata bang ffmpeg (khong can Spotlight)."""
    try:
        p = subprocess.run(["ffmpeg","-hide_banner","-i",path],
                           capture_output=True, timeout=60)
        t = p.stderr.decode("utf-8","replace")
    except Exception:
        return {}
    d = {}
    m = FF_DUR.search(t)
    if m: d["duration"] = int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
    m = FF_DIM.search(t)
    if m: d["width"], d["height"] = int(m.group(1)), int(m.group(2))
    m = FF_VCOD.search(t)
    if m: d["codec"] = m.group(1)
    m = FF_DATE.search(t)
    if m:
        raw = m.group(1)
        try:
            dt = datetime.datetime.fromisoformat(raw.replace("Z", "").split(".")[0])
            if raw.endswith("Z"):      # creation_time trong file la UTC
                dt = cfg.gio_dia_phuong(dt.replace(tzinfo=datetime.timezone.utc))
            d["shot_at"] = dt.isoformat(sep=" ")
        except ValueError:
            pass
    m = FF_LOC.search(t)
    if m:
        d["lat"], d["lon"] = float(m.group(1)), float(m.group(2))
    d["has_audio"] = 1 if "Audio:" in t else 0
    return d

# Ngay gio nam trong TEN FILE: IMG_20230415_183012, VID_20230415, 2023-04-15 18.30.12, PXL_...
# May DJI ghi gio quay THAT (gio dia phuong) vao ten file - nguon dang tin nhat
DJI_TEN = re.compile(r"DJI_(20\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})")
FN_PATTERNS = [
    re.compile(r"(20\d{2})[-_.]?(\d{2})[-_.]?(\d{2})[-_ .T]?(\d{2})[-_.:]?(\d{2})[-_.:]?(\d{2})"),
    re.compile(r"(20\d{2})[-_.]?(\d{2})[-_.]?(\d{2})"),
]
def from_filename(name):
    for pat in FN_PATTERNS:
        m = pat.search(name)
        if not m: continue
        g = [int(x) for x in m.groups()]
        try:
            if len(g) == 6: dt = datetime.datetime(g[0],g[1],g[2],g[3],g[4],g[5])
            else:           dt = datetime.datetime(g[0],g[1],g[2])
            if 2000 <= dt.year <= 2100:
                return dt.isoformat(sep=" ")
        except ValueError:
            pass
    return None

def parse_md_date(s):
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S"):
        try:
            # mdls in gio UTC (+0000). Cat mui gio di ma khong doi la lech dung bang mui gio.
            return cfg.gio_dia_phuong(datetime.datetime.strptime(s, fmt)).isoformat(sep=" ")
        except ValueError:
            pass
    return None

def kind_of(ext):
    if ext in VIDEO_EXT: return "video"
    if ext in PHOTO_EXT: return "photo"
    if ext in AUDIO_EXT: return "audio"
    return "other"

def probe(path, st, root):
    ext = os.path.splitext(path)[1].lower()
    k = kind_of(ext)
    # Khoa = duong dan tuong doi so voi THU MUC FOOTAGE (khong phai thu muc dang quet),
    # de quet rieng mot buoi quay moi van khop voi kho cu.
    r = {"path":cfg.rel(path), "name":cfg.N(os.path.basename(path)), "ext":ext, "kind":k,
         "size":st.st_size, "mtime":st.st_mtime,
         "folder":cfg.rel(os.path.dirname(path)) or ".",
         "shot_at":None,"shot_src":None,"duration":None,"width":None,"height":None,
         "lat":None,"lon":None,"camera":None,"codec":None,"bitrate":None,"has_audio":None}

    m = DJI_TEN.search(r["name"])
    if m:
        try:
            dt = datetime.datetime(*[int(x) for x in m.groups()])
            if 2015 <= dt.year <= datetime.date.today().year + 2:   # mat pin -> nam 2000, khong tin
                r["shot_at"], r["shot_src"] = dt.isoformat(sep=" "), "ten-dji"
        except ValueError:
            pass

    md = read_mdls(path)
    if md:
        d = md.get("kMDItemContentCreationDate")
        if d:
            iso = parse_md_date(d)
            # Spotlight chua doc duoc metadata thi tra NGAY TAO FILE (= ngay chep vao o)
            # ma van gan nhan nhu ngay chup. Trung ngay tao file thi khong tin.
            sinh = getattr(st, "st_birthtime", None)
            if iso and sinh and abs((datetime.datetime.fromisoformat(iso) -
                                     datetime.datetime.fromtimestamp(sinh)).total_seconds()) < 5:
                iso = None
            if iso and r["shot_at"] is None: r["shot_at"], r["shot_src"] = iso, "exif"
        for src, dst, cast in (("kMDItemDurationSeconds","duration",float),
                               ("kMDItemPixelWidth","width",int),
                               ("kMDItemPixelHeight","height",int),
                               ("kMDItemLatitude","lat",float),
                               ("kMDItemLongitude","lon",float),
                               ("kMDItemTotalBitRate","bitrate",float),
                               ("kMDItemAudioChannelCount","has_audio",int)):
            if src in md:
                try: r[dst] = cast(float(md[src])) if cast is int else cast(md[src])
                except ValueError: pass
        mk, mo = md.get("kMDItemAcquisitionMake"), md.get("kMDItemAcquisitionModel")
        r["camera"] = " ".join(x for x in (mk,mo) if x) or None
        r["codec"]  = md.get("kMDItemCodecs")

    # Video thieu thong tin -> hoi ffmpeg
    if k == "video" and (r["duration"] is None or r["width"] is None or r["shot_at"] is None):
        ff = read_ffmpeg(path)
        for key in ("duration","width","height","codec","lat","lon","has_audio"):
            if r.get(key) is None and ff.get(key) is not None:
                r[key] = ff[key]
        if r["shot_at"] is None and ff.get("shot_at"):
            r["shot_at"], r["shot_src"] = ff["shot_at"], "ffmpeg"

    if r["shot_at"] is None:
        fn = from_filename(r["name"])
        if fn: r["shot_at"], r["shot_src"] = fn, "filename"
    if r["shot_at"] is None:
        r["shot_at"] = datetime.datetime.fromtimestamp(st.st_mtime).isoformat(sep=" ")
        r["shot_src"] = "mtime"
    return r

COLS = ["path","name","ext","kind","size","mtime","shot_at","shot_src","duration",
        "width","height","lat","lon","camera","codec","bitrate","has_audio",
        "folder","event_id","scanned_at"]

def cmd_scan(args):
    goc = cfg.can_o_goc()
    root = os.path.abspath(os.path.expanduser(args.root))
    if not os.path.isdir(root):
        # cho phep go duong dan tinh tu thu muc footage
        thu = cfg.src(args.root)
        if os.path.isdir(thu): root = os.path.abspath(thu)
        else: sys.exit("Khong thay thu muc: " + root)
    if cfg.ngoai_o_goc(root):
        sys.exit("Thu muc {} nam NGOAI thu muc footage {}.\n"
                 "Kho luu duong dan tuong doi so voi thu muc footage - quet ngoai thi buoc proxy\n"
                 "va xuat se khong tim thay file. Chep buoi quay vao trong thu muc footage,\n"
                 "hoac khai lai: python3 cfg.py --khai \"<thu muc footage>\"".format(root, goc))
    cfg.chot_thu_muc_lam()
    con = db_open(args.db)
    done = {p: (s, m) for p, s, m in con.execute("SELECT path,size,mtime FROM media")}
    print("Da co san trong danh muc: {:,} file".format(len(done)))
    print("Dang duyet cay thu muc...")

    todo = []
    skipped = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith("._")]
        for fn in filenames:
            if fn.startswith("._") or fn == ".DS_Store": continue
            if os.path.splitext(fn)[1].lower() not in ALL_EXT: continue
            fp = os.path.join(dirpath, fn)
            try: st = os.stat(fp)
            except OSError: continue
            prev = done.get(cfg.rel(fp))   # kho luu tuong doi - so bang tuyet doi la nhan doi ca kho
            if prev and prev[0] == st.st_size and abs(prev[1] - st.st_mtime) < 1:
                skipped += 1; continue
            todo.append((fp, st))
    print("Can xu ly: {:,} file  (bo qua {:,} da lam roi)".format(len(todo), skipped))
    if not todo:
        con.close(); return

    now = datetime.datetime.now().isoformat(timespec="seconds")
    sql = "INSERT OR REPLACE INTO media ({}) VALUES ({})".format(
        ",".join(COLS), ",".join("?"*len(COLS)))
    buf, n = [], 0
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for r in ex.map(lambda a: probe(a[0], a[1], root), todo):
            r["event_id"] = None; r["scanned_at"] = now
            buf.append([r[c] for c in COLS]); n += 1
            if len(buf) >= 300:
                con.executemany(sql, buf); con.commit(); buf = []
                pct = 100.0*n/len(todo)
                print("\r  {:,}/{:,}  ({:.1f}%)".format(n, len(todo), pct), end="", flush=True)
    if buf: con.executemany(sql, buf); con.commit()
    print("\r  {:,}/{:,}  (100%)   Xong.".format(n, len(todo)))

    src = dict(con.execute("SELECT shot_src, COUNT(*) FROM media GROUP BY shot_src"))
    print("\nNguon thoi gian:", ", ".join("{}={:,}".format(k,v) for k,v in src.items()))
    if src.get("mtime",0) > 0.5*sum(src.values()):
        print("\n  !! Phan lon file khong doc duoc ngay quay that (dang lay ngay sua file).")
        if sys.platform == "darwin":
            print("     Co the o dia chua duoc Spotlight lap chi muc. Mo System Settings >")
            print("     Spotlight > Search Privacy, bo o dia ra khoi danh sach loai tru,")
            print("     doi lap chi muc xong roi chay lai lenh scan.")
    con.close()

def human_size(b):
    for u in ("B","KB","MB","GB","TB"):
        if b < 1024: return "{:.1f} {}".format(b,u)
        b /= 1024
    return "{:.1f} PB".format(b)

def human_dur(s):
    if not s: return "0"
    s = int(s); h, m = s//3600, (s%3600)//60
    return "{}h{:02d}m".format(h,m) if h else "{}m{:02d}s".format(m, s%60)

def cmd_report(args):
    con = db_open(args.db); c = con.cursor()
    tot = c.execute("SELECT COUNT(*), SUM(size) FROM media").fetchone()
    if not tot[0]: sys.exit("Danh muc rong. Chay lenh scan truoc.")
    print("="*64)
    print("TONG QUAN KHO:  {:,} file   {}".format(tot[0], human_size(tot[1] or 0)))
    print("="*64)
    print("\n-- Theo loai --")
    for k, n, sz, dur in c.execute(
        "SELECT kind, COUNT(*), SUM(size), SUM(duration) FROM media GROUP BY kind ORDER BY SUM(size) DESC"):
        print("  {:<7} {:>8,} file  {:>10}  {}".format(k, n, human_size(sz or 0),
              human_dur(dur) if dur else ""))
    print("\n-- Theo nam --")
    for y, n, sz, dur in c.execute(
        "SELECT substr(shot_at,1,4), COUNT(*), SUM(size), SUM(duration) FROM media "
        "GROUP BY 1 ORDER BY 1"):
        print("  {}  {:>8,} file  {:>10}  video {}".format(y, n, human_size(sz or 0), human_dur(dur)))
    print("\n-- Thiet bi quay/chup --")
    for cam, n in c.execute(
        "SELECT COALESCE(camera,'(khong ro)'), COUNT(*) FROM media GROUP BY 1 ORDER BY 2 DESC LIMIT 12"):
        print("  {:<34} {:>8,}".format(cam[:34], n))
    print("\n-- 15 thu muc lon nhat --")
    for f, n, sz in c.execute(
        "SELECT folder, COUNT(*), SUM(size) FROM media GROUP BY folder ORDER BY SUM(size) DESC LIMIT 15"):
        print("  {:>10}  {:>7,} file  {}".format(human_size(sz or 0), n, f[:60]))
    g = c.execute("SELECT COUNT(*) FROM media WHERE lat IS NOT NULL").fetchone()[0]
    print("\n-- Toa do GPS: {:,}/{:,} file ({:.0f}%) --".format(g, tot[0], 100.0*g/tot[0]))
    con.close()

def cmd_events(args):
    """Tu dong chia kho thanh cac 'buoi quay': cach nhau > N gio thi la buoi moi."""
    con = db_open(args.db); c = con.cursor()
    rows = c.execute("SELECT path, shot_at, kind, duration, size, lat, lon, folder "
                     "FROM media WHERE shot_at IS NOT NULL ORDER BY shot_at").fetchall()
    if not rows: sys.exit("Danh muc rong. Chay lenh scan truoc.")
    gap = datetime.timedelta(hours=args.gap)
    con.execute("DELETE FROM events"); con.execute("UPDATE media SET event_id=NULL")

    def T(s):
        try: return datetime.datetime.fromisoformat(s)
        except ValueError: return None

    groups, cur, prev = [], [], None
    for r in rows:
        t = T(r[1])
        if t is None: continue
        if prev is not None and t - prev > gap:
            groups.append(cur); cur = []
        cur.append((t, r)); prev = t
    if cur: groups.append(cur)

    print("Chia duoc {:,} buoi quay (nguong cach nhau {} gio)\n".format(len(groups), args.gap))
    ev_rows, upd = [], []
    for i, g in enumerate(groups, 1):
        ts = [x[0] for x in g]; rs = [x[1] for x in g]
        nv  = sum(1 for r in rs if r[2] == "video")
        dur = sum(r[3] or 0 for r in rs if r[2] == "video")
        sz  = sum(r[4] or 0 for r in rs)
        lats = [r[5] for r in rs if r[5] is not None]
        lons = [r[6] for r in rs if r[6] is not None]
        folders = {}
        for r in rs: folders[r[7]] = folders.get(r[7], 0) + 1
        top = max(folders, key=folders.get)
        ev_rows.append((i, ts[0].isoformat(sep=" "), ts[-1].isoformat(sep=" "),
                        len(rs), nv, dur, sz,
                        sum(lats)/len(lats) if lats else None,
                        sum(lons)/len(lons) if lons else None, top, None))
        upd += [(i, r[0]) for r in rs]
    con.executemany("INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)", ev_rows)
    con.executemany("UPDATE media SET event_id=? WHERE path=?", upd)
    con.commit()

    print("{:<5} {:<11} {:<4} {:>7} {:>6} {:>9} {:>9}  {}".format(
        "#","Ngay","Ngay","File","Video","Thoi luong","Dung luong","Thu muc chinh"))
    print("-"*104)
    big = con.execute("SELECT * FROM events ORDER BY total_size DESC LIMIT ?", (args.top,)).fetchall()
    for e in big:
        d0, d1 = e[1][:10], e[2][:10]
        days = (datetime.date.fromisoformat(d1) - datetime.date.fromisoformat(d0)).days + 1
        print("{:<5} {:<11} {:<4} {:>7,} {:>6,} {:>9} {:>9}  {}".format(
            e[0], d0, "{}d".format(days), e[3], e[4], human_dur(e[5]), human_size(e[6] or 0), (e[9] or "")[:36]))
    print("\n(dang hien {} buoi lon nhat / tong {}) ".format(len(big), len(groups)))
    con.close()

def main():
    ap = argparse.ArgumentParser(description="Lap danh muc kho anh/video (chi doc file goc)")
    ap.add_argument("--db", default=DB_DEFAULT)
    sub = ap.add_subparsers(dest="cmd")
    sub.required = True
    p = sub.add_parser("scan", help="quet mot thu muc nam trong thu muc footage")
    p.add_argument("root"); p.add_argument("--jobs", type=int, default=8); p.set_defaults(f=cmd_scan)
    p = sub.add_parser("report", help="tong quan kho"); p.set_defaults(f=cmd_report)
    p = sub.add_parser("events", help="tu chia kho thanh cac buoi quay")
    p.add_argument("--gap", type=float, default=8.0); p.add_argument("--top", type=int, default=40); p.set_defaults(f=cmd_events)
    a = ap.parse_args(); a.f(a)

if __name__ == "__main__":
    main()
