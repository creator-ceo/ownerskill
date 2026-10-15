#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Do do net va do sang tung giay tren ban proxy. Chay lai duoc, khong lam lai clip da xong.
     python3 analyze.py                    moi clip da co proxy ma chua do
     python3 analyze.py --thu-muc "X"      chi clip trong thu muc X (tinh tu thu muc footage)
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg
import subprocess, collections, re, time
import tempfile
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser(description="Do do net, do sang tung giay tren proxy")
ap.add_argument("--thu-muc", help="chi do clip trong thu muc nay (tinh tu thu muc footage)")
ap.add_argument("--jobs", type=int, default=2, help="so clip do cung luc (mac dinh 2)")
a = ap.parse_args()

TMP = os.path.join(tempfile.gettempdir(), "qwork"); os.makedirs(TMP, exist_ok=True)
N = cfg.N
THU_MUC = N(a.thu_muc).strip("/") if a.thu_muc else None

con = cfg.mo_kho(120)
con.execute("""CREATE TABLE IF NOT EXISTS quality (
  path TEXT, sec INTEGER, blur REAL, yavg REAL, ylow REAL, yhigh REAL,
  PRIMARY KEY(path, sec))""")
con.commit()
if "proxy_status" not in {r[1] for r in con.execute("PRAGMA table_info(media)")}:
    sys.exit("Chua co clip nao co proxy. Chay proxy.py --run truoc.")
done = {p for (p,) in con.execute("SELECT DISTINCT path FROM quality")}

todo = []
for path, prox, folder, dur in con.execute(
        "SELECT path, proxy_path, folder, duration FROM media "
        "WHERE kind='video' AND proxy_status='ok'"):
    if THU_MUC and not cfg.trong_thu_muc(folder, THU_MUC): continue
    prox = cfg.prox(prox) if prox else None
    if path in done or not prox or not os.path.exists(prox): continue
    todo.append((path, prox, dur or 0))
print("Can do: {:,} clip  ({:.0f} phut)".format(len(todo), sum(t[2] for t in todo)/60))
if not todo: sys.exit()

PT = re.compile(r"^frame:\d+\s+pts:\S+\s+pts_time:([\d.]+)")
KV = re.compile(r"^lavfi\.(?:signalstats\.)?(blur|YAVG|YLOW|YHIGH)=([-\d.]+)")

def analyze(job):
    path, prox, dur = job
    f = os.path.join(TMP, str(abs(hash(path))) + ".txt")
    cmd = ["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-i",prox,
           "-vf","fps=2,blurdetect,signalstats,metadata=print:file="+f,"-f","null","-"]
    try:
        subprocess.run(cmd, capture_output=True, timeout=1200)
    except Exception:
        return path, []
    acc = collections.defaultdict(lambda: collections.defaultdict(list)); t = None
    try:
        with open(f, errors="replace") as fh:
            for line in fh:
                m = PT.match(line)
                if m: t = int(float(m.group(1))); continue
                m = KV.match(line)
                if m and t is not None: acc[t][m.group(1)].append(float(m.group(2)))
    except OSError:
        return path, []
    try: os.remove(f)
    except OSError: pass
    out = []
    for s, d in sorted(acc.items()):
        def av(k):
            v = d.get(k)
            return sum(v)/len(v) if v else None
        out.append((path, s, av("blur"), av("YAVG"), av("YLOW"), av("YHIGH")))
    return path, out

n = 0; t0 = time.time()
with ThreadPoolExecutor(max_workers=a.jobs) as ex:
    for path, rows in ex.map(analyze, todo):
        if rows:
            con.executemany("INSERT OR REPLACE INTO quality VALUES (?,?,?,?,?,?)", rows)
            con.commit()
        n += 1
        el = time.time()-t0
        print("\r  {:,}/{:,}  con ~{:.0f} phut".format(n, len(todo), el/n*(len(todo)-n)/60),
              end="", flush=True)
print("\nXong.")
con.close()
