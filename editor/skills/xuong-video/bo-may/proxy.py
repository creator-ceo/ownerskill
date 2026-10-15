#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tao ban xem nhanh (proxy 720p) + do chuyen dong tung giay.
   Dung giua chung roi chay lai van tiep tuc duoc - clip da xong thi bo qua.
     python3 proxy.py                         xem truoc: bao nhieu clip, uoc tinh bao lau
     python3 proxy.py --run                   chay that, moi clip chua co proxy
     python3 proxy.py --thu-muc "X"           chi xem truoc mot thu muc (vd buoi quay moi)
     python3 proxy.py --run --thu-muc "X"     chi lam mot thu muc
   "X" la duong dan TINH TU thu muc footage, vd "2025-06 Da Lat".
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg
import subprocess, collections, time, re
import tempfile
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser(description="Tao ban xem nhanh 720p cho video trong kho")
ap.add_argument("--run", action="store_true", help="chay that (mac dinh chi xem truoc)")
ap.add_argument("--thu-muc", help="chi lam clip trong thu muc nay (tinh tu thu muc footage)")
ap.add_argument("--jobs", type=int, default=3, help="so clip lam cung luc (mac dinh 3)")
a = ap.parse_args()

OUT = os.path.join(cfg.C["work_root"], "proxy")
TMP = os.path.join(tempfile.gettempdir(), "pxwork")
N = cfg.N
THU_MUC = N(a.thu_muc).strip("/") if a.thu_muc else None

con = cfg.mo_kho(60)
cols = {r[1] for r in con.execute("PRAGMA table_info(media)")}
if "proxy_path" not in cols:
    con.execute("ALTER TABLE media ADD COLUMN proxy_path TEXT")
    con.execute("ALTER TABLE media ADD COLUMN proxy_status TEXT")
con.execute("""CREATE TABLE IF NOT EXISTS motion (
    path TEXT, sec INTEGER, mafd REAL, PRIMARY KEY(path, sec))""")
con.commit()

todo = []
for path, folder, dur, codec, name, st in con.execute(
        "SELECT path, folder, duration, codec, name, proxy_status FROM media WHERE kind='video'"):
    if THU_MUC and not cfg.trong_thu_muc(folder, THU_MUC): continue
    if st == "ok": continue
    todo.append((path, folder, dur or 0, (codec or ""), name))
todo.sort(key=lambda x: (N(x[1]), x[4]))

tot_dur = sum(t[2] for t in todo)
print("=" * 58)
print("  {:<16} {:>4,} clip   {:>6.0f} phut video".format(
    "Chi thu muc" if THU_MUC else "Ca kho", len(todo), tot_dur / 60))
print("  Uoc tinh ~{:.0f}-{:.0f} phut xu ly (tuy may manh hay yeu)".format(tot_dur / 60 / 9, tot_dur / 60 / 3))
print("=" * 58)
if not todo:
    print("Khong con clip nao can lam proxy.")
    sys.exit()
if not a.run:
    print("(moi xem truoc. Them --run de chay that - viec nay chiem may kha lau)")
    sys.exit()
cfg.chot_thu_muc_lam()

os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
FRAME = re.compile(r"^frame:\d+\s+pts:\S+\s+pts_time:([\d.]+)")
MAFD  = re.compile(r"^lavfi\.scd\.mafd=([\d.]+)")

def condense(txt_path):
    """Gom mafd tung khung hinh thanh trung binh tung giay."""
    acc = collections.defaultdict(list); t = None
    try:
        with open(txt_path, errors="replace") as fh:
            for line in fh:
                m = FRAME.match(line)
                if m: t = float(m.group(1)); continue
                m = MAFD.match(line)
                if m and t is not None: acc[int(t)].append(float(m.group(1)))
    except OSError:
        return []
    return [(s, sum(v) / len(v)) for s, v in sorted(acc.items())]

done = [0]; t0 = time.time()

def work(job):
    path, folder, dur, codec, name = job
    rel  = os.path.splitext(N(path))[0] + ".mp4"
    dest = os.path.join(OUT, *rel.split("/"))
    srcf = cfg.src(path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    mfile = os.path.join(TMP, str(abs(hash(path))) + ".txt")
    hw = cfg.hwaccel() if "HEVC" in codec.upper() else []
    cmd = (["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin"] + hw +
           ["-i", srcf,
            "-vf", "scale=1280:-2,scdet=threshold=10,metadata=print:file=" + mfile,
            "-c:v", cfg.encoder(), "-b:v", "3M", "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart", "-y", dest])
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=1800)
        ok = p.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 10000
    except Exception:
        ok = False
    rows = condense(mfile) if ok else []
    try: os.remove(mfile)
    except OSError: pass
    return path, rel if ok else None, "ok" if ok else "loi", rows

with ThreadPoolExecutor(max_workers=a.jobs) as ex:
    for path, dest, status, rows in ex.map(work, todo):
        con.execute("UPDATE media SET proxy_path=?, proxy_status=? WHERE path=?", (dest, status, path))
        if rows:
            con.executemany("INSERT OR REPLACE INTO motion VALUES (?,?,?)",
                            [(path, s, v) for s, v in rows])
        con.commit()
        done[0] += 1
        el = time.time() - t0
        eta = el / done[0] * (len(todo) - done[0])
        print("\r  {:,}/{:,}  ({:.0f}%)  con ~{:.0f} phut   ".format(
            done[0], len(todo), 100.0 * done[0] / len(todo), eta / 60), end="", flush=True)
print("\n\nXong. Proxy nam o:", OUT)
bad = con.execute("SELECT COUNT(*) FROM media WHERE proxy_status='loi'").fetchone()[0]
if bad: print("Co {} file bi loi - chay lai lenh nay se thu lai.".format(bad))
con.close()
