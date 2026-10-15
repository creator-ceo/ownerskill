#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cham diem tung giay va cat thanh cac doan dung duoc. Xep hang theo: net + on dinh + do sang.
   Luon cham lai CA KHO (nguong tinh tuong doi tren toan kho), khong cham rieng buoi moi.
     python3 chon_canh.py              cham diem, in cac doan hay nhat
     python3 chon_canh.py --reel 40    dung them video xem thu tu 40 doan hay nhat
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg
import math, subprocess, collections, bisect

ap = argparse.ArgumentParser(description="Cham diem va cat doan dung duoc tren ca kho")
ap.add_argument("--reel", type=int, metavar="K", help="dung video xem thu tu K doan hay nhat")
a = ap.parse_args()

OUT  = os.path.join(cfg.C["work_root"], "tuyen-chon")
MIN_LEN, MAX_LEN = 3, 8          # doan dai it nhat 3 giay, cat toi da 8 giay
EDGE = 1                          # bo 1 giay dau/cuoi moi clip
N = cfg.N

con = cfg.mo_kho(120)
if not cfg.co_bang(con, "quality"):
    sys.exit("Chua do chat luong clip nao. Chay proxy.py --run roi analyze.py truoc.")
con.execute("""CREATE TABLE IF NOT EXISTS segments (
  path TEXT, start INTEGER, dur INTEGER, score REAL,
  sharp REAL, steady REAL, expo REAL, folder TEXT, name TEXT,
  PRIMARY KEY(path, start))""")

# ---- gom du lieu ----
q = collections.defaultdict(dict)
for p, s, blur, ya, yl, yh in con.execute("SELECT path,sec,blur,yavg,ylow,yhigh FROM quality"):
    q[p][s] = [blur, ya, yl, yh, None]
if cfg.co_bang(con, "motion"):
    for p, s, mafd in con.execute("SELECT path,sec,mafd FROM motion"):
        if p in q and s in q[p]: q[p][s][4] = mafd

blurs = sorted(v[0] for d in q.values() for v in d.values() if v[0] is not None)
def rank(sorted_arr, x):
    return bisect.bisect_left(sorted_arr, x) / max(len(sorted_arr), 1)

# do rung = do lech chuan cua chuyen dong trong cua so 5 giay
shakes = []
per_clip = {}
for p, d in q.items():
    secs = sorted(d)
    mv = {s: d[s][4] for s in secs if d[s][4] is not None}
    sh = {}
    for s in secs:
        w = [mv[t] for t in range(s-2, s+3) if t in mv]
        if len(w) >= 3:
            m = sum(w)/len(w)
            sh[s] = math.sqrt(sum((x-m)**2 for x in w)/len(w))
    per_clip[p] = sh; shakes += list(sh.values())
shakes.sort()

def expo_score(ya, yl, yh):
    if ya is None: return 0.5
    s = 1.0
    if ya < 45:  s -= (45-ya)/45          # toi qua
    if ya > 200: s -= (ya-200)/55         # sang qua
    if yh is not None and yh > 245: s -= 0.4   # chay sang
    if yl is not None and yl < 4:   s -= 0.2   # ben toi
    return max(0.0, min(1.0, s))

meta = {p: (N(f), n, d) for p, f, n, d in con.execute(
    "SELECT path,folder,name,duration FROM media WHERE kind='video'")}

# ---- cham diem tung giay ----
scored = {}
for p, d in q.items():
    sh = per_clip.get(p, {}); dur = (meta.get(p) or (None,None,0))[2] or 0
    out = {}
    for s, v in d.items():
        if s < EDGE or (dur and s > dur - EDGE - 1): continue
        if v[0] is None or s not in sh: continue
        sharp  = 1.0 - rank(blurs, v[0])
        steady = 1.0 - rank(shakes, sh[s])
        expo   = expo_score(v[1], v[2], v[3])
        out[s] = (0.40*sharp + 0.40*steady + 0.20*expo, sharp, steady, expo)
    scored[p] = out

allv = sorted(x[0] for d in scored.values() for x in d.values())
THR = allv[int(len(allv)*0.55)] if allv else 0.5     # lay nhom 45% tot nhat

# ---- gom thanh doan lien tuc ----
con.execute("DELETE FROM segments"); rows = []
for p, d in scored.items():
    fol, nm, _ = meta.get(p, ("", "", 0))
    secs = sorted(s for s, v in d.items() if v[0] >= THR)
    run = []
    for s in secs + [None]:
        if run and s is not None and s == run[-1] + 1:
            run.append(s); continue
        if len(run) >= MIN_LEN:
            for i in range(0, len(run), MAX_LEN):
                ch = run[i:i+MAX_LEN]
                if len(ch) < MIN_LEN: break
                vs = [d[t] for t in ch]
                rows.append((p, ch[0], len(ch),
                             sum(v[0] for v in vs)/len(vs),
                             sum(v[1] for v in vs)/len(vs),
                             sum(v[2] for v in vs)/len(vs),
                             sum(v[3] for v in vs)/len(vs), fol, nm))
        run = [s] if s is not None else []
con.executemany("INSERT OR REPLACE INTO segments VALUES (?,?,?,?,?,?,?,?,?)", rows)
con.commit()

tot = sum(r[2] for r in rows)
print("=" * 70)
print("Tim duoc {:,} doan dung duoc, tong {:.0f} phut (tu {:.0f} phut goc)".format(
    len(rows), tot/60, sum(len(d) for d in scored.values())/60))
print("=" * 70)
print("\n{:<30} {:>6} {:>5} {:>6} {:>6} {:>6}  {}".format(
    "Clip","Giay","Dai","Diem","Net","On dinh","Thu muc"))
for r in sorted(rows, key=lambda x: -x[3])[:20]:
    print("{:<30} {:>5}s {:>4}s {:>6.2f} {:>6.2f} {:>6.2f}  {}".format(
        r[8][:30], r[1], r[2], r[3], r[4], r[5], r[7][:26]))

print("\n-- Theo thu muc --")
g = collections.defaultdict(lambda: [0, 0])
for r in rows: x = g[r[7]]; x[0] += 1; x[1] += r[2]
for f in sorted(g, key=lambda x: -g[x][1]):
    print("  {:<44} {:>4} doan  {:>5.0f} phut".format(f[:44], g[f][0], g[f][1]/60))

# ---- dung video xem thu ----
if a.reel:
    k = a.reel
    os.makedirs(OUT, exist_ok=True)
    # moi clip gop toi da 2 doan, va cach nhau it nhat 20 giay -> tranh trung lap
    cap, last, top = collections.Counter(), {}, []
    for r in sorted(rows, key=lambda x: -x[3]):
        if len(top) >= k: break
        if cap[r[0]] >= 2: continue
        if r[0] in last and abs(r[1]-last[r[0]]) < 20: continue
        cap[r[0]] += 1; last[r[0]] = r[1]; top.append(r)
    top.sort(key=lambda x: (x[7], x[8], x[1]))   # xep theo thu muc cho de xem
    px = {p: cfg.prox(pp) for p, pp in con.execute("SELECT path,proxy_path FROM media WHERE proxy_status='ok'") if pp}
    FONT = cfg.font() or ""
    parts, lst = [], os.path.join(OUT, "list.txt")
    print("\nDang dung video xem thu tu {} doan...".format(len(top)))
    for i, r in enumerate(top):
        src = px.get(r[0])
        if not src or not os.path.exists(src): continue
        o = os.path.join(OUT, "seg{:03d}.mp4".format(i))
        lab = "{}  {}s  diem {:.2f}".format(r[8][:24], r[1], r[3]).replace(":", "\\:").replace("'", "")
        vf = "scale=1280:-2"
        if FONT and os.path.exists(FONT):
            vf += (",drawtext=fontfile='{}':text='{}':x=20:y=h-50:fontsize=22:"
                   "fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=8").format(FONT, lab)
        cmd = ["ffmpeg","-hide_banner","-loglevel","error","-nostdin",
               "-ss",str(r[1]),"-t",str(r[2]),"-i",src,"-vf",vf,
               "-r","30","-vsync","cfr","-video_track_timescale","30000",
               "-c:v",cfg.encoder(),"-b:v","4M","-an","-y",o]
        if subprocess.run(cmd, capture_output=True).returncode == 0:
            parts.append(o)
    with open(lst,"w") as fh:
        for pth in parts: fh.write("file '{}'\n".format(pth))
    reel = os.path.join(OUT, "xem-thu.mp4")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-f","concat","-safe","0",
                    "-i",lst,"-c","copy","-y",reel], capture_output=True)
    for pth in parts:
        try: os.remove(pth)
        except OSError: pass
    try: os.remove(lst)
    except OSError: pass
    print("Xong:", reel, "({:.0f} giay)".format(sum(r[2] for r in top)))
con.close()
