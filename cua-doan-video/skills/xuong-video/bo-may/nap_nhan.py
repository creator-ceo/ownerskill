#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nhan noi dung cho tung clip (trong canh co gi), de tim.py tra theo noi dung chu khong chi theo ten.
   Kho moi KHONG co nhan nao - ban tu gan, hoac nho AI xem anh roi gan.

    python3 nap_nhan.py --anh                    dung anh 6 khung cho 12 clip chua co nhan + file mau de dien
    python3 nap_nhan.py --anh --so 30 --thu-muc "X"
    python3 nap_nhan.py <file.json>              nap nhan da dien vao kho
    python3 nap_nhan.py --xem                    bao nhieu clip da co nhan, thu muc nao con thieu

File nhan la mot danh sach JSON, moi clip mot muc. Khoa la `path` (duong dan tinh tu thu muc
footage, giong cot path trong kho). Khong co path thi dung `file` (ten file) - nhung chi khi ten
do la DUY NHAT trong kho: may quay hay dat trung ten (C0001.MP4...) o nhieu buoi.
O nao de trong thi khong ghi. Truoc lan nap dau tien trong ngay, catalog.db duoc sao luu.
"""
import json, os, sys, shutil, datetime, collections, argparse, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg

O = ("loai_shot", "gio_quay", "trong_ngoai", "boi_canh", "chu_the", "hanh_dong",
     "dung_cho", "tu_khoa", "ghi_chu", "nguon")
O_NOI_DUNG = ("trong_ngoai", "boi_canh", "chu_the", "hanh_dong", "dung_cho", "tu_khoa")


def tao_bang(con):
    con.execute("""CREATE TABLE IF NOT EXISTS nhan (
      path TEXT PRIMARY KEY,
      loai_shot   TEXT,   -- kieu khung: can / trung / toan canh; may tinh / lia / di chuyen
      gio_quay    TEXT,   -- sang som / sang / trua / chieu / hoang hon / toi
      trong_ngoai TEXT,   -- trong nha / ngoai troi
      boi_canh    TEXT,   -- o dau: quan ca phe, bai bien, ban lam viec...
      chu_the     TEXT,   -- ai / cai gi trong khung
      hanh_dong   TEXT,   -- dang lam gi
      dung_cho    TEXT,   -- hop minh hoa cho y nao trong video
      tu_khoa     TEXT,
      ghi_chu     TEXT,
      nguon       TEXT    -- 'ai-xem-anh' | 'tu-gan'
    )""")


def sao_luu():
    p = cfg.db()
    dich = p + ".truoc-nap-nhan-" + datetime.date.today().isoformat()
    if not os.path.exists(dich):
        shutil.copy2(p, dich)
        print("Da sao luu kho:", dich)


def da_co_nhan(con):
    tao_bang(con)
    dk = " OR ".join("COALESCE({},'') != ''".format(c) for c in O_NOI_DUNG)
    return {cfg.N(p) for (p,) in con.execute("SELECT path FROM nhan WHERE " + dk)}


def xem(con):
    co = da_co_nhan(con)
    tong, dem = collections.Counter(), collections.Counter()
    for (p,) in con.execute("SELECT path FROM media WHERE kind='video'"):
        p = cfg.N(p)
        nhom = p.split("/")[0] if "/" in p else "(ngay trong thu muc footage)"
        tong[nhom] += 1
        dem[nhom] += p in co
    if not tong:
        print("Kho chua co video nao."); return
    print("{:<36} {:>7} / {:<5}".format("Thu muc", "co nhan", "tong"))
    for k, n in sorted(tong.items()):
        print("{:<36} {:>7} / {:<5}{}".format(k[:36], dem[k], n, "" if dem[k] == n else "   <- thieu {}".format(n - dem[k])))
    print("\nTong: {} / {} video co nhan noi dung".format(sum(dem.values()), sum(tong.values())))


def nap(con, file_json):
    try:
        data = json.load(open(file_json, encoding="utf-8"))
    except Exception as e:
        sys.exit("Khong doc duoc {}: {}".format(file_json, e))
    if isinstance(data, dict):
        data = data.get("clip") or data.get("clips") or []
    tao_bang(con)
    duong = {cfg.N(p): p for (p,) in con.execute("SELECT path FROM media WHERE kind='video'")}
    ten = collections.defaultdict(list)
    for p, n in con.execute("SELECT path, name FROM media WHERE kind='video'"):
        ten[cfg.N(n)].append(p)
    ok, trong, thieu, trung = 0, 0, [], []
    for d in data:
        cot = [c for c in O if c != "nguon" and str(d.get(c) or "").strip()]
        if not cot:
            trong += 1; continue
        p = duong.get(cfg.N(d.get("path") or ""))
        if not p:
            ps = ten.get(cfg.N(d.get("file") or d.get("name") or ""), [])
            if len(ps) > 1:
                trung.append(d.get("file") or d.get("name")); continue
            if not ps:
                thieu.append(d.get("path") or d.get("file") or d.get("name")); continue
            p = ps[0]
        con.execute("INSERT INTO nhan (path) VALUES (?) ON CONFLICT(path) DO NOTHING", (p,))
        con.execute("UPDATE nhan SET {}, nguon=? WHERE path=?".format(", ".join(c + "=?" for c in cot)),
                    [str(d[c]).strip() for c in cot] + [d.get("nguon") or "ai-xem-anh", p])
        ok += 1
    con.commit()
    # tu khai phan bi bo: vao bao nhieu, ghi bao nhieu, bo cai nao
    print("Vao {} muc -> ghi {} clip | de trong {} | khong thay trong kho {} | ten trung {}".format(
        len(data), ok, trong, len(thieu), len(trung)))
    for x in thieu[:20]:
        print("  KHONG THAY:", x)
    for x in trung[:20]:
        print("  TEN TRUNG (ghi them path de chi dung clip):", x)


def dung_anh(con, so, thu_muc):
    """Moi clip mot anh ghep 6 khung (3x2) trai deu tu dau toi cuoi, de AI hoac nguoi xem roi gan nhan.
       Doc ban proxy neu co, khong thi doc file goc - chi doc, khong sua."""
    co = da_co_nhan(con)
    cols = {r[1] for r in con.execute("PRAGMA table_info(media)")}
    px_col = "proxy_path" if "proxy_path" in cols else "NULL"
    rows = []
    for path, folder, name, dur, px in con.execute(
            "SELECT path, folder, name, duration, {} FROM media WHERE kind='video' "
            "ORDER BY folder, name".format(px_col)):
        if cfg.N(path) in co: continue
        if thu_muc and not cfg.trong_thu_muc(folder, thu_muc): continue
        rows.append((path, folder, name, dur, px))
    if not rows:
        print("Khong con clip nao chua co nhan" + (" trong '{}'.".format(thu_muc) if thu_muc else "."))
        return
    rows = rows[:so]
    lo = datetime.datetime.now().strftime("lo-%Y%m%d-%H%M%S")
    ra = os.path.join(cfg.C["work_root"], "gan-nhan", lo)
    os.makedirs(ra, exist_ok=True)
    mau = []
    for i, (path, folder, name, dur, px) in enumerate(rows, 1):
        nguon = cfg.prox(px) if px else None
        if not nguon or not os.path.exists(nguon):
            nguon = cfg.src(path) if cfg.C.get("o_goc") else None
        if not nguon or not os.path.exists(nguon):
            print("  bo qua (khong thay proxy lan file goc):", name); continue
        dur = float(dur or 30)
        o = os.path.join(ra, "{:02d}.jpg".format(i))
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
               "-ss", "{:.2f}".format(dur * 0.05), "-t", "{:.2f}".format(dur * 0.9), "-i", nguon,
               "-vf", "fps=6/{:.3f},scale=420:-2,tile=3x2".format(max(dur * 0.9, 0.5)),
               "-frames:v", "1", "-q:v", "4", "-y", o]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode != 0 or not os.path.exists(o):
            print("  LOI dung anh:", name); continue
        muc = {"anh": os.path.basename(o), "path": cfg.N(path)}
        muc.update({c: "" for c in O if c != "nguon"})
        mau.append(muc)
        print("  {:02d}.jpg  {}".format(i, cfg.N(path)))
    f = os.path.join(ra, "can-gan-nhan.json")
    with open(f, "w", encoding="utf-8") as fh:
        json.dump(mau, fh, ensure_ascii=False, indent=2)
    print("\nDa dung {} anh o: {}".format(len(mau), ra))
    print("File de dien   : {}".format(f))
    print("Xem tung anh (anh NN.jpg ung voi muc co \"anh\": \"NN.jpg\"), dien cac o, roi chay:")
    print('    python3 nap_nhan.py "{}"'.format(f))


def main():
    ap = argparse.ArgumentParser(description="Gan nhan noi dung cho clip trong kho")
    ap.add_argument("file", nargs="?", help="file JSON nhan da dien de nap vao kho")
    ap.add_argument("--xem", action="store_true", help="bao nhieu clip da co nhan")
    ap.add_argument("--anh", action="store_true", help="dung anh 6 khung cho clip chua co nhan")
    ap.add_argument("--so", type=int, default=12, help="so clip moi lo khi --anh (mac dinh 12)")
    ap.add_argument("--thu-muc", help="chi clip trong thu muc nay khi --anh")
    a = ap.parse_args()

    con = cfg.mo_kho(60)
    if a.xem:
        xem(con)
    elif a.anh:
        dung_anh(con, a.so, a.thu_muc)
    elif a.file:
        if not os.path.exists(a.file):
            sys.exit("Khong thay file nhan: " + a.file)
        sao_luu()
        nap(con, a.file)
        print("Tong clip co nhan noi dung trong kho: {}".format(len(da_co_nhan(con))))
    else:
        ap.print_help()
    con.close()


if __name__ == "__main__":
    main()
