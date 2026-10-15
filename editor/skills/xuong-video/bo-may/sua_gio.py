#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sua ngay quay khi dong ho may quay bi reset (het pin -> ve nam 2000, hoac nhay toi tuong lai).
   Chi sua trong catalog.db, KHONG dung toi file goc. Gio goc duoc giu de quay lui.

   Cach sua, theo thu tu:
     1. Ten thu muc co ngay  (vd "2025-08-25 Da Lat", "25082025", "20250825")  -> lay ngay do, 12:00
     2. Khong co -> lay ngay o giua cua cac file khac cung thu muc co ngay hop le, 12:00
     3. Van khong co -> bo qua, in ra de nguoi dung tu xem

     python3 sua_gio.py            xem truoc, khong sua
     python3 sua_gio.py --apply    sua that
     python3 sua_gio.py --revert   tra lai nhu cu
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg
import datetime, re, collections

ap = argparse.ArgumentParser(description="Sua ngay quay sai do dong ho may quay bi reset (chi sua trong kho)")
g = ap.add_mutually_exclusive_group()
g.add_argument("--apply", action="store_true", help="sua that")
g.add_argument("--revert", action="store_true", help="tra lai gio goc cho cac file da sua")
a = ap.parse_args()

NAM_DAU = "2015"                                     # truoc moc nay la dong ho may bi reset
NAM_TOI = str(datetime.date.today().year + 2)        # qua moc nay la dong ho may sai

con = cfg.mo_kho(60)
cfg.dam_bao_goc(con)      # dong moi quet vao cung duoc giu gio goc

if a.revert:
    n = con.execute("UPDATE media SET shot_at = shot_at_raw, shot_src = shot_src_raw "
                    "WHERE shot_src IN ('thu-muc', 'thu-muc-giua')").rowcount
    con.commit(); print("Da tra lai gio goc cho {:,} file.".format(n)); sys.exit()

# Ngay trong ten thu muc: nam-thang-ngay (2025-08-25, 20250825) hoac ngay-thang-nam (25-08-2025, 25082025)
NGAY_YMD = re.compile(r"(?<!\d)(20\d{2})[-_. ]?(\d{2})[-_. ]?(\d{2})(?!\d)")
NGAY_DMY = re.compile(r"(?<!\d)(\d{2})[-_. ]?(\d{2})[-_. ]?(20\d{2})(?!\d)")

def ngay_trong_ten(folder):
    for pat, thu_tu in ((NGAY_YMD, (0, 1, 2)), (NGAY_DMY, (2, 1, 0))):
        for m in pat.finditer(folder or ""):
            g = [int(x) for x in m.groups()]
            y, mo, d = g[thu_tu[0]], g[thu_tu[1]], g[thu_tu[2]]
            try:
                return datetime.datetime(y, mo, d, 12, 0, 0)
            except ValueError:
                continue
    return None

bad = con.execute("SELECT path, folder, name FROM media "
                  "WHERE shot_at_raw < ? OR shot_at_raw > ?", (NAM_DAU, NAM_TOI)).fetchall()

folder_median = {}
_by = collections.defaultdict(list)
for fol, sa in con.execute("SELECT folder, shot_at_raw FROM media "
                           "WHERE shot_at_raw >= ? AND shot_at_raw <= ?", (NAM_DAU, NAM_TOI)):
    _by[fol].append(sa)
for fol, lst in _by.items():
    lst.sort()
    folder_median[fol] = lst[len(lst)//2][:10] + " 12:00:00"

theo_ten, theo_giua, chua = [], [], []
for path, folder, name in bad:
    dt = ngay_trong_ten(folder)
    if dt:
        theo_ten.append((dt.isoformat(sep=" "), path)); continue
    med = folder_median.get(folder)
    if med:
        theo_giua.append((med, path)); continue
    chua.append((folder, name))

print("=" * 62)
print("Dong ho may bi reset: {:,} file".format(len(bad)))
print("  sua theo ngay trong ten thu muc : {:>6,}".format(len(theo_ten)))
print("  sua theo cac file cung thu muc  : {:>6,}".format(len(theo_giua)))
print("  khong tu sua duoc               : {:>6,}".format(len(chua)))
print("=" * 62)
for lbl, lst in (("ten thu muc", theo_ten), ("cung thu muc", theo_giua)):
    if lst:
        moi, p = lst[0]
        cu = con.execute("SELECT shot_at_raw, name, folder FROM media WHERE path=?", (p,)).fetchone()
        print("vd ({}): {}   {} -> {}   [{}]".format(lbl, cu[1][:24], cu[0][:16], moi[:16], cu[2]))
for f, n in chua[:5]:
    print("  chua sua: {} / {}".format(f, n))

if not a.apply:
    print("\n(moi xem truoc - chua sua gi. Them --apply de sua that)")
else:
    con.executemany("UPDATE media SET shot_at=?, shot_src='thu-muc' WHERE path=?", theo_ten)
    con.executemany("UPDATE media SET shot_at=?, shot_src='thu-muc-giua' WHERE path=?", theo_giua)
    con.commit()
    print("\nDa sua {:,} file. Chay 'python3 sua_gio.py --revert' de quay lui.".format(
        len(theo_ten) + len(theo_giua)))
con.close()
