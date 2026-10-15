#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dung bang anh thu nho, xep theo do phang mau, de NGUOI nhin va tu chi ra clip nao quay log.
   Can chay do_mau.py truoc.
     python3 bang_anh.py                  tat ca clip da do
     python3 bang_anh.py --moi-trang 40   so anh moi trang
"""
import os, sys, subprocess, shutil, argparse
import tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser(description="Bang anh thu nho xep theo do phang mau")
ap.add_argument("--moi-trang", type=int, default=40)
ap.add_argument("--cot", type=int, default=5)
a = ap.parse_args()

con = cfg.mo_kho(120)
if not cfg.co_bang(con, "mau_do"):
    sys.exit("Chua co du lieu. Chay: python3 do_mau.py")
rows = list(con.execute("""SELECT m.path, m.proxy_path, m.folder, m.name, m.duration,
       d.ymin, d.ymax, d.phang
       FROM mau_do d JOIN media m ON m.path=d.path ORDER BY d.phang DESC"""))
if not rows: sys.exit("Chua co du lieu. Chay: python3 do_mau.py")

RA = os.path.join(cfg.C["work_root"], "bang-mau")
if os.path.isdir(RA): shutil.rmtree(RA)
os.makedirs(RA)
TMP = os.path.join(tempfile.gettempdir(), "bang"); shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
FONT = cfg.font()
print("Dung anh thu nho cho {:,} clip...".format(len(rows)))

def thumb(job):
    i, (path, prox, fol, name, dur, mn, mx, ph) = job
    full = cfg.prox(prox) if prox else None
    if not full or not os.path.exists(full): return None
    o = os.path.join(TMP, "t{:04d}.png".format(i))
    giua = max(1, int((dur or 10) / 2))
    nhan = "{}. {}  phang={:.0f}".format(i + 1, os.path.splitext(name)[0][:22], ph)
    nhan = nhan.replace(":", "").replace("'", "").replace("\\", "")
    vf = "scale=360:-2"
    if FONT:
        vf += (",drawtext=fontfile='{}':text='{}':x=6:y=h-26:fontsize=17:fontcolor=white"
               ":box=1:boxcolor=black@0.65:boxborderw=5").format(FONT, nhan)
    r = subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin",
        "-ss",str(giua),"-i",full,"-vf",vf,"-frames:v","1","-y",o], capture_output=True)
    return o if r.returncode == 0 and os.path.exists(o) else None

with ThreadPoolExecutor(max_workers=6) as ex:
    anh = [x for x in ex.map(thumb, list(enumerate(rows))) if x]
print("Duoc {:,} anh. Ghep thanh trang...".format(len(anh)))

cot, moi = a.cot, a.moi_trang
hang = (moi + cot - 1) // cot
trang = 0
for b in range(0, len(anh), moi):
    lo = anh[b:b + moi]
    d = os.path.join(TMP, "seq"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for k, f in enumerate(lo): shutil.copyfile(f, os.path.join(d, "i{:03d}.png".format(k)))
    trang += 1
    out = os.path.join(RA, "trang{:02d}.jpg".format(trang))
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin",
        "-i", os.path.join(d, "i%03d.png"),
        "-vf","tile={}x{}:padding=6:margin=6:color=0x202020".format(cot, hang),
        "-frames:v","1","-q:v","4","-y",out], capture_output=True)
    if os.path.exists(out):
        print("  {}  ({} clip, hang {}-{})".format(
            os.path.basename(out), len(lo), b + 1, b + len(lo)))
print("\nXong. Anh o:", RA)
print("Trang dau = PHANG NHAT (nhieu kha nang la log)")
print("Trang cuoi = TUONG PHAN NHAT (nhieu kha nang da co mau)")
con.close()
