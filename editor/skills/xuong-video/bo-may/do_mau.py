#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Do do phang (nhat mau) cua tung clip de xep hang: nghi quay log <-> da co mau san.
   Khong ket luan gi - chi xep thu tu de NGUOI xem va tu chi ra ranh gioi.
     python3 do_mau.py          do tat ca clip da co proxy ma chua do, roi in bang
     python3 do_mau.py --bang   chi in bang xep hang
"""
import os, sys, re, subprocess, collections, time, argparse
import tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser(description="Do do phang mau tung clip (goi y, khong ket luan)")
ap.add_argument("--bang", action="store_true", help="chi in bang xep hang, khong do them")
a = ap.parse_args()

con = cfg.mo_kho(120)
con.execute("""CREATE TABLE IF NOT EXISTS mau_do (
  path TEXT PRIMARY KEY, ymin REAL, ymax REAL, sat REAL, phang REAL)""")
con.commit()

KV = re.compile(r"lavfi\.signalstats\.(YMIN|YMAX|SATAVG)=([-\d.]+)")
TMP = os.path.join(tempfile.gettempdir(), "domau"); os.makedirs(TMP, exist_ok=True)

def do(job):
    path, prox = job
    tf = os.path.join(TMP, str(abs(hash(path))) + ".txt")
    try:
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-i",prox,
            "-vf","fps=1/3,signalstats,metadata=print:file="+tf,"-f","null","-"],
            capture_output=True, timeout=600)
    except Exception:
        return None
    acc = collections.defaultdict(list)
    try:
        for line in open(tf, errors="replace"):
            m = KV.search(line)
            if m: acc[m.group(1)].append(float(m.group(2)))
        os.remove(tf)
    except OSError: pass
    if not acc.get("YMIN"): return None
    # dung PHAN VI 10% thay vi cuc tri - mot khung hinh la khong lam hong ca clip
    def q(v, p):
        v = sorted(v); return v[min(int(len(v)*p), len(v)-1)]
    ymin = q(acc["YMIN"], 0.10)      # muc den dien hinh
    ymax = q(acc["YMAX"], 0.90)      # muc trang dien hinh
    sat  = sum(acc["SATAVG"])/len(acc["SATAVG"]) if acc.get("SATAVG") else 0.0
    # do phang: den bi nang len bao nhieu + trang bi chan lai bao nhieu
    phang = ymin + max(0.0, 235.0 - ymax)
    return (path, ymin, ymax, sat, phang)

if not a.bang:
    if "proxy_status" not in {r[1] for r in con.execute("PRAGMA table_info(media)")}:
        sys.exit("Chua co clip nao co proxy. Chay proxy.py --run truoc.")
    xong = {p for (p,) in con.execute("SELECT path FROM mau_do")}
    jobs = []
    for path, prox in con.execute(
            "SELECT path, proxy_path FROM media WHERE proxy_status='ok' AND proxy_path IS NOT NULL"):
        if path in xong: continue
        full = cfg.prox(prox)
        if os.path.exists(full): jobs.append((path, full))
    print("Can do: {:,} clip".format(len(jobs)))
    if jobs:
        n, t0 = 0, time.time()
        with ThreadPoolExecutor(max_workers=5) as ex:
            for r in ex.map(do, jobs):
                n += 1
                if r: con.execute("INSERT OR REPLACE INTO mau_do VALUES (?,?,?,?,?)", r)
                if n % 20 == 0:
                    con.commit()
                    el = time.time()-t0
                    print("\r  {:,}/{:,}  con ~{:.0f} phut".format(n,len(jobs),el/n*(len(jobs)-n)/60),
                          end="", flush=True)
        con.commit(); print("\r  {:,}/{:,}  xong.            ".format(n, len(jobs)))

rows = list(con.execute("""SELECT m.path, d.ymin, d.ymax, d.sat, d.phang, m.folder, m.name
    FROM mau_do d JOIN media m ON m.path=d.path ORDER BY d.phang DESC"""))
print("\nDa do {:,} clip. Xep tu PHANG NHAT (nghi la log) den TUONG PHAN NHAT.\n".format(len(rows)))
print("{:<4} {:<30} {:>6} {:>6} {:>6} {:>7}  {}".format("#","Clip","YMIN","YMAX","Bao hoa","Do phang","Thu muc"))
print("-"*104)
for i, (p, mn, mx, sa, ph, f, n) in enumerate(rows, 1):
    if i <= 12 or i > len(rows)-12:
        print("{:<4} {:<30} {:>6.0f} {:>6.0f} {:>6.1f} {:>7.0f}  {}".format(
            i, n[:30], mn, mx, sa, ph, cfg.N(f)[:32]))
    elif i == 13:
        print("     ... {} clip o giua ...".format(len(rows)-24))
con.close()
