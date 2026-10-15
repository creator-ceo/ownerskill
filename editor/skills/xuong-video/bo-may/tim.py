#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tra kho tu lieu - tim doan video dung duoc cho mot y trong kich ban.

Tim theo chu = khop voi NHAN NOI DUNG cua clip (neu da gan bang nap_nhan.py: boi canh,
ai trong khung, dang lam gi, dung cho y nao, tu khoa) cong ten thu muc + ten file.
Khop theo dau tu: "an" khong khop "ban".

Vi du:
    python3 tim.py "doc sach"                 tim theo chu (khong can go dau)
    python3 tim.py "sach" --bo-noi            bo moi canh ngoi noi truoc may (tim B-roll)
    python3 tim.py "laptop" --bo "khach san"  bo clip co cum chu nay trong nhan
    python3 tim.py --luc hoang-hon --dong tinh
    python3 tim.py "thien" --top 20 --xem     dung video xem thu
    python3 tim.py --tu 2025-06-21 --den 2025-06-22
    python3 tim.py "bien" --luu "y3-met-moi"  luu lai thanh mot tuyen chon
    python3 tim.py --cac-tuyen                xem cac tuyen da luu
    python3 tim.py --bo-loc                   xem cac gia tri loc co san
"""
import sqlite3, os, sys, argparse, subprocess, collections, re
import unicodedata as ud
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg

# ---- thoi diem trong ngay, suy tu gio quay ----
LUC = [(4,7,"binh-minh","bình minh"), (7,11,"sang","buổi sáng"),
       (11,14,"trua","buổi trưa"),    (14,17,"chieu","buổi chiều"),
       (17,19,"hoang-hon","hoàng hôn"), (19,28,"toi","tối")]
def luc_cua(h):
    for lo, hi, ma, ten in LUC:
        if lo <= h < hi: return ma, ten
    return "toi", "tối"

# ---- kieu chuyen dong, suy tu do lech khung hinh trung binh ----
DONG = [(0,0.30,"tinh","máy tĩnh"), (0.30,1.0,"lia-cham","lia chậm"),
        (1.0,2.5,"vua","chuyển động vừa"), (2.5,9e9,"manh","chuyển động mạnh")]
SANG = [(0,70,"toi","tối"), (70,130,"vua","vừa"), (130,999,"sang","sáng")]
def xep(bang, v):
    if v is None: return "?", "?"
    for lo, hi, ma, ten in bang:
        if lo <= v < hi: return ma, ten
    return "?", "?"

def bo_dau(s):
    """Bo dau tieng Viet de tim kiem khong can go dau."""
    s = ud.normalize("NFD", cfg.N(s).lower())
    s = "".join(ch for ch in s if not ud.combining(ch))
    return s.replace("đ", "d")

def chuan_tim(s):
    """Chuoi de so khop: bo dau, bo dau cau -> khop theo dau tu."""
    return " " + re.sub(r"[^0-9a-z_]+", " ", bo_dau(s)).strip() + " "

O_NHAN = ("trong_ngoai", "boi_canh", "chu_the", "hanh_dong", "dung_cho", "tu_khoa")

# Canh ngoi noi truoc may hay duoc ghi nhan theo nhieu cach. Tim B-roll ma khong bo
# nhung canh nay la vo nham mat nguoi dang noi. Khi gan nhan canh noi, nen dung
# mot trong cac cum duoi day (vd "nói trước máy") de --bo-noi bat duoc.
CANH_NOI = ("talking head", "noi voi may", "noi voi khan gia", "noi truoc may", "tu quay noi",
            "ke chuyen voi khan gia")

def _hang(con, sql):
    """Doc bang; bang chua co (chua chay buoc truoc) thi tra rong thay vi bao loi."""
    try:
        return list(con.execute(sql))
    except sqlite3.OperationalError:
        return []

def nap_nhan(con):
    if not cfg.co_bang(con, "nhan"):
        return {}
    ra = {}
    for r in con.execute("SELECT path, loai_shot, gio_quay, {} FROM nhan".format(", ".join(O_NHAN))):
        d = dict(zip(("loai_shot", "gio_quay") + O_NHAN, r[1:]))
        if any(d[k] for k in O_NHAN):
            ra[r[0]] = d
    return ra

def nap():
    """Doc toan bo doan + chi so, tinh san thuoc tinh cho tung doan.
    Clip DA GAN NHAN ma chua co doan cham diem (chua do chat luong, hoac khong doan nao
    qua nguong) van duoc tra ve nguyen clip: da co nguoi xem va gan nhan thi khong bo qua."""
    con = cfg.mo_kho()
    nhan = nap_nhan(con)
    mv = collections.defaultdict(dict)
    for p, s, v in _hang(con, "SELECT path,sec,mafd FROM motion"): mv[p][s] = v
    ya = collections.defaultdict(dict)
    for p, s, v in _hang(con, "SELECT path,sec,yavg FROM quality"): ya[p][s] = v
    khi = {p: t for p, t in con.execute("SELECT path,shot_at FROM media")}
    out = []
    hang = _hang(con, "SELECT path,start,dur,score,sharp,steady,expo,folder,name FROM segments")
    co_doan = {r[0] for r in hang}
    for path, fol, nm, dai in con.execute("SELECT path,folder,name,duration FROM media WHERE kind='video'"):
        if path in nhan and path not in co_doan:
            st = int((dai or 0) * 0.04)
            hang.append((path, st, max(1, min(8, int((dai or 1) - st))), None, None, None, None, fol, nm))
    for path, st, dur, sc, sharp, steady, expo, fol, nm in hang:
        rng = range(st, st + dur)
        m = [mv[path][s] for s in rng if s in mv[path]]
        y = [ya[path][s] for s in rng if s in ya[path]]
        t = khi.get(path) or ""
        gio = int(t[11:13]) if len(t) >= 13 and t[11:13].isdigit() else 12
        lma, lten = luc_cua(gio)
        dma, dten = xep(DONG, sum(m)/len(m) if m else None)
        sma, sten = xep(SANG, sum(y)/len(y) if y else None)
        n = nhan.get(path) or {}
        out.append(dict(path=path, start=st, dur=dur, score=sc if sc is not None else 0.0,
                        da_cham=sc is not None, folder=cfg.N(fol),
                        name=nm, ngay=t[:10], gio=t[11:16],
                        luc=lma, luc_ten=lten, dong=dma, dong_ten=dten,
                        sang=sma, sang_ten=sten, nhan=n,
                        tim=chuan_tim(" ".join([cfg.N(fol), nm] + [n.get(k) or "" for k in O_NHAN]))))
    con.close()
    return out

def loc(ds, a):
    r = ds
    if a.chu:
        tu = chuan_tim(a.chu).split()
        r = [d for d in r if all(" " + t in d["tim"] for t in tu)]
    bo_ds = list(getattr(a, "bo", None) or [])
    if getattr(a, "bo_noi", False):
        bo_ds += CANH_NOI
    truoc = len(r)
    for bo in bo_ds:
        cum = chuan_tim(bo)
        r = [d for d in r if cum not in d["tim"]]
    a._bo_dem = truoc - len(r)
    for khoa in ("luc", "dong", "sang"):
        v = getattr(a, khoa)
        if v: r = [d for d in r if d[khoa] == v]
    if a.tu:  r = [d for d in r if d["ngay"] >= a.tu]
    if a.den: r = [d for d in r if d["ngay"] <= a.den]
    if a.dai_nhat: r = [d for d in r if d["dur"] <= a.dai_nhat]
    # khop NGUYEN CUM xep truoc (bo dau thi "doc" = doc/dọc/đọc, khop le tung tu hay nham),
    # roi doan da cham diem, roi clip chua cham (lay nguyen clip)
    cum = chuan_tim(a.chu) if a.chu and len(a.chu.split()) > 1 else None
    for d in r:
        d["khop_cum"] = bool(cum and cum in d["tim"])
    a._khop_cum = sum(1 for d in r if d["khop_cum"]) if cum else None
    return sorted(r, key=lambda d: (not d["khop_cum"], not d["da_cham"], -d["score"]))

def gioi_han_moi_clip(ds, n):
    """Moi clip gop toi da n doan -> tranh nhan duoc nhieu lat cat giong nhau."""
    dem, out = collections.Counter(), []
    for d in ds:
        if dem[d["path"]] >= n: continue
        dem[d["path"]] += 1; out.append(d)
    return out

def main():
    ap = argparse.ArgumentParser(description="Tra kho tu lieu video")
    ap.add_argument("chu", nargs="?", help="tu khoa (khong can go dau)")
    ap.add_argument("--luc",  choices=[x[2] for x in LUC], help="thoi diem trong ngay")
    ap.add_argument("--dong", choices=[x[2] for x in DONG], help="kieu chuyen dong cua may quay")
    ap.add_argument("--sang", choices=[x[2] for x in SANG], help="do sang")
    ap.add_argument("--tu", help="tu ngay YYYY-MM-DD"); ap.add_argument("--den", help="den ngay YYYY-MM-DD")
    ap.add_argument("--dai-nhat", type=int, help="chi lay doan ngan hon N giay")
    ap.add_argument("--bo", action="append", help="bo clip co cum chu nay trong nhan; lap lai duoc")
    ap.add_argument("--bo-noi", action="store_true", help="bo moi canh ngoi noi truoc may - dung khi tim B-roll")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--moi-clip", type=int, default=2, help="toi da bao nhieu doan tu cung mot clip")
    ap.add_argument("--xem", action="store_true", help="dung video xem thu")
    ap.add_argument("--luu", help="luu ket qua thanh mot tuyen chon co ten")
    ap.add_argument("--cac-tuyen", action="store_true", help="xem cac tuyen da luu")
    ap.add_argument("--bo-loc", action="store_true", help="xem kho co nhung gia tri loc nao")
    a = ap.parse_args()

    con = cfg.mo_kho()
    con.execute("""CREATE TABLE IF NOT EXISTS tuyen (
        ten TEXT, thu_tu INTEGER, path TEXT, start INTEGER, dur INTEGER,
        PRIMARY KEY(ten, thu_tu))""")
    con.commit()

    if a.cac_tuyen:
        rows = list(con.execute(
            "SELECT ten, COUNT(*), SUM(dur) FROM tuyen GROUP BY ten ORDER BY ten"))
        if not rows: print("Chua luu tuyen nao.")
        for t, n, d in rows: print("  {:<28} {:>3} doan  {:>4} giay".format(t, n, d))
        return

    ds = nap()
    if a.bo_loc:
        print("Kho co {:,} doan dung duoc.".format(len(ds)))
        cn = {d["path"] for d in ds if d["nhan"]}
        cc = {d["path"] for d in ds if d["nhan"] and not d["da_cham"]}
        print("  {} clip co nhan noi dung (tra theo noi dung duoc); {} trong so do chua cham diem -> tra ve nguyen clip".format(len(cn), len(cc)))
        print("  {} doan chua co nhan -> chi khop theo ten thu muc / ten file\n".format(sum(1 for d in ds if not d["nhan"])))
        if not ds:
            print("Kho chua co doan nao. Chay du luong nhap kho: proxy.py --run, analyze.py, chon_canh.py.")
            return
        for khoa, nhan in (("luc","Thoi diem"), ("dong","Chuyen dong"), ("sang","Do sang")):
            c = collections.Counter(d[khoa] for d in ds)
            print("--{}  {}:".format(khoa, nhan))
            for k, n in c.most_common():
                ten = next((d[khoa+"_ten"] for d in ds if d[khoa] == k), k)
                print("    {:<12} {:>5,} doan   ({})".format(k, n, ten))
            print()
        print("Thu muc co trong kho:")
        for f, n in collections.Counter(d["folder"] for d in ds).most_common():
            print("    {:<46} {:>4} doan".format(f[:46], n))
        return

    kq = gioi_han_moi_clip(loc(ds, a), a.moi_clip)
    if not kq:
        print("Khong tim thay doan nao khop. Thu bo bot bo loc, hoac chay --bo-loc de xem co gi.")
        return

    lay = kq[:a.top]
    print("Tim thay {:,} doan, hien {} doan dau  ({} giay)".format(
        len(kq), len(lay), sum(d["dur"] for d in lay)))
    print("  trong {} doan tim thay: {} da cham diem · {} clip chua cham (lay nguyen clip) · {} chua co nhan (chi khop ten thu muc)".format(
        len(kq), sum(1 for d in kq if d["da_cham"]), sum(1 for d in kq if not d["da_cham"]), sum(1 for d in kq if not d["nhan"])))
    if getattr(a, "_khop_cum", None) is not None:
        print("  {} doan khop nguyen cum '{}' (xep truoc), con lai chi khop le tung tu".format(
            sum(1 for d in kq if d["khop_cum"]), a.chu))
    if getattr(a, "_bo_dem", 0):
        print("  da bo {} doan theo --bo/--bo-noi".format(a._bo_dem))
    print("-" * 96)
    print("{:<3} {:<26} {:>5} {:>4} {:>6}  {:<11} {:<16}  {}".format(
        "#","Clip","Giay","Dai","Diem","Luc","Chuyen dong","Thu muc"))
    for i, d in enumerate(lay, 1):
        print("{:<3} {:<26} {:>4}s {:>3}s {:>6}  {:<11} {:<16}  {}".format(
            i, d["name"][:26], d["start"], d["dur"], "{:.2f}".format(d["score"]) if d["da_cham"] else "chua",
            d["luc_ten"], d["dong_ten"], d["folder"][:24]))
        n = d["nhan"]
        if n:
            print("      {}".format(" · ".join(x for x in (n.get("hanh_dong"), n.get("boi_canh")) if x)[:120]))
            if n.get("dung_cho"):
                print("      dung cho: {}".format(n["dung_cho"][:110]))
        else:
            print("      (chua co nhan noi dung)")

    if a.luu:
        con.execute("DELETE FROM tuyen WHERE ten=?", (a.luu,))
        con.executemany("INSERT INTO tuyen VALUES (?,?,?,?,?)",
                        [(a.luu, i, d["path"], d["start"], d["dur"]) for i, d in enumerate(lay)])
        con.commit()
        print("\nDa luu tuyen '{}' gom {} doan.".format(a.luu, len(lay)))

    if a.xem:
        out = os.path.join(cfg.C["work_root"], "tuyen-chon")
        os.makedirs(out, exist_ok=True)
        ten = (a.luu or a.chu or "ket-qua").replace(" ", "-")
        dich = os.path.join(out, "tim-{}.mp4".format(bo_dau(ten)))
        FONT = cfg.font(); parts = []
        print("\nDang dung video xem thu...")
        for i, d in enumerate(lay):
            srcf = cfg.prox(os.path.splitext(d["path"])[0] + ".mp4")
            if not os.path.exists(srcf): continue
            o = os.path.join(out, "_t{:03d}.mp4".format(i))
            vf = "scale=1280:-2"
            if FONT:
                nhan = "{}. {}  {}s  {}".format(i+1, d["name"][:20], d["start"], d["dong_ten"])
                nhan = nhan.replace(":", "").replace("'", "")
                vf += (",drawtext=fontfile='{}':text='{}':x=20:y=h-50:fontsize=22:"
                       "fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=8").format(FONT, nhan)
            cmd = ["ffmpeg","-hide_banner","-loglevel","error","-nostdin",
                   "-ss",str(d["start"]),"-t",str(d["dur"]),"-i",srcf,"-vf",vf,
                   "-r","30","-vsync","cfr","-video_track_timescale","30000",
                   "-c:v",cfg.encoder(),"-b:v","4M","-an","-y",o]
            if subprocess.run(cmd, capture_output=True).returncode == 0: parts.append(o)
        if parts:
            lst = os.path.join(out, "_list.txt")
            with open(lst,"w") as fh:
                for p in parts: fh.write("file '{}'\n".format(p))
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-f","concat",
                            "-safe","0","-i",lst,"-c","copy","-y",dich], capture_output=True)
            for p in parts + [lst]:
                try: os.remove(p)
                except OSError: pass
            print("Xong:", dich)
        else:
            print("Khong dung duoc - khong tim thay file proxy.")
    con.close()

if __name__ == "__main__":
    main()
