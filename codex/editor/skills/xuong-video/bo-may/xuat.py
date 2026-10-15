#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Xuat cac doan da chon thanh thu muc danh so, keo tha thang vao CapCut.

    python3 xuat.py --tuyen "y3-met-moi"            xuat mot tuyen da luu
    python3 xuat.py "ngoi thien" --luc binh-minh --top 8
    python3 xuat.py --tuyen X --goc                 dung file goc chat luong day du (o footage phai dang cam)
    python3 xuat.py --tuyen X --lut "~/LUT/slog3.cube"   ap LUT - CHI khi nguoi dung yeu cau
    python3 xuat.py --tuyen X --tam                 nang mau tam de xem truoc

Mac dinh GIU NGUYEN MAU. Ap LUT nham vao clip da co mau la hong khong cuu duoc.
"""
import sqlite3, os, sys, argparse, subprocess, shutil, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True   # khong de lai thu muc __pycache__ canh code
import cfg, tim

# Nang mau tam cho footage log - KHONG thay duoc LUT that, chi de xem truoc
TAM = "eq=contrast=1.32:saturation=1.45:gamma=0.94,unsharp=5:5:0.4"

def hang_may(name):
    """Doan hang may quay tu ten file de chon dung LUT khi nguoi dung dua ca hai loai."""
    n = name.upper()
    if n.startswith("DJI"): return "dji"
    if n.startswith(("C0", "DSC", "A7", "ZV")): return "sony"
    return "khac"

def nap_phang(con):
    """Diem do phang tung clip - CHI DE BAO cho nguoi dung biet clip nao co the can LUT.
       Khong tu dong lam gi ca: ap LUT nham vao clip da co mau la hong han."""
    try:
        return {p: (ph, None) for p, ph in con.execute("SELECT path, phang FROM mau_do")}
    except sqlite3.OperationalError:     # kho chua chay do_mau.py
        return {}

def tim_lut(thu_muc):
    """Tu tim file .cube trong thu muc luts/ cua thu muc lam viec."""
    ra = {}
    for f in glob.glob(os.path.join(thu_muc, "*.cube")) + glob.glob(os.path.join(thu_muc, "*.CUBE")):
        t = os.path.basename(f).lower()
        if "dlog" in t or "dji" in t or "d-log" in t: ra.setdefault("dji", f)
        elif "slog" in t or "sony" in t or "s-log" in t: ra.setdefault("sony", f)
        else: ra.setdefault("chung", f)
    return ra

def an_toan(s):
    """Ten file khong dau, khong ky tu la - de Windows va CapCut khong bao loi."""
    s = tim.bo_dau(s)
    return "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in s).strip("-")[:40]

def main():
    ap = argparse.ArgumentParser(description="Xuat doan da chon thanh thu muc danh so cho CapCut")
    ap.add_argument("chu", nargs="?", help="tu khoa (neu khong dung --tuyen)")
    ap.add_argument("--tuyen", help="ten tuyen da luu bang tim.py --luu")
    ap.add_argument("--luc", choices=[x[2] for x in tim.LUC])
    ap.add_argument("--dong", choices=[x[2] for x in tim.DONG])
    ap.add_argument("--sang", choices=[x[2] for x in tim.SANG])
    ap.add_argument("--tu"); ap.add_argument("--den")
    ap.add_argument("--dai-nhat", type=int)
    ap.add_argument("--bo", action="append", help="bo clip co cum chu nay trong nhan")
    ap.add_argument("--bo-noi", action="store_true", help="bo moi canh ngoi noi truoc may")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--moi-clip", type=int, default=2)
    ap.add_argument("--lut", help="mot file .cube dung cho tat ca (chi khi nguoi dung yeu cau)")
    ap.add_argument("--lut-sony"); ap.add_argument("--lut-dji")
    ap.add_argument("--tam", action="store_true", help="nang mau tam khi chua co LUT")
    ap.add_argument("--goc", action="store_true", help="dung file goc thay vi ban proxy 720p")
    ap.add_argument("--ten", help="ten thu muc xuat")
    a = ap.parse_args()

    con = cfg.mo_kho()
    if a.goc and not cfg.C.get("o_goc"):
        sys.exit("--goc can biet thu muc footage. " + cfg.HUONG_DAN_KHAI)
    ds = tim.nap()
    chi_muc = {(d["path"], d["start"]): d for d in ds}

    if a.tuyen:
        try:
            rows = list(con.execute(
                "SELECT path,start,dur FROM tuyen WHERE ten=? ORDER BY thu_tu", (a.tuyen,)))
        except sqlite3.OperationalError:
            rows = []
        if not rows: sys.exit("Khong thay tuyen '{}'. Xem: python3 tim.py --cac-tuyen".format(a.tuyen))
        lay = [chi_muc.get((p, s)) or dict(path=p, start=s, dur=d, name=os.path.basename(p),
               folder=os.path.dirname(p), score=0, luc="", luc_ten="", dong="", dong_ten="", sang_ten="", ngay="", gio="")
               for p, s, d in rows]
        ten_ra = a.ten or a.tuyen
    else:
        lay = tim.gioi_han_moi_clip(tim.loc(ds, a), a.moi_clip)[:a.top]
        ten_ra = a.ten or a.chu or "ket-qua"
    if not lay: sys.exit("Khong co doan nao de xuat.")

    # --- chon LUT (chi dung khi nguoi dung go --lut*) ---
    tu_tim = tim_lut(os.path.join(cfg.C["work_root"], "luts"))
    lut = {"sony": a.lut_sony or a.lut or tu_tim.get("sony") or tu_tim.get("chung"),
           "dji":  a.lut_dji  or a.lut or tu_tim.get("dji")  or tu_tim.get("chung"),
           "khac": a.lut}                # may khac: chi ap khi nguoi dung dua mot LUT chung
    lut = {k: os.path.expanduser(v) for k, v in lut.items() if v}
    lut = {k: v for k, v in lut.items() if os.path.exists(v)}

    bang_phang = nap_phang(con)
    diem = {d["path"]: bang_phang.get(d["path"], (None, None))[0] for d in lay}
    n_phang = sum(1 for v in diem.values() if v is not None and v >= 35)

    ra = os.path.join(cfg.C["work_root"], "xuat", an_toan(ten_ra) or "ket-qua")
    if os.path.isdir(ra): shutil.rmtree(ra)
    os.makedirs(ra)

    print("=" * 66)
    print("Xuat {} doan  ({} giay)  ->  {}".format(
        len(lay), sum(d["dur"] for d in lay), ra))
    print("Nguon  :", "file goc" if a.goc else "ban proxy 720p")
    if a.lut or a.lut_sony or a.lut_dji:
        print("Mau    : ap LUT theo yeu cau -", ", ".join("{}={}".format(k, os.path.basename(v)) for k, v in lut.items()) or "KHONG THAY FILE LUT")
    elif a.tam: print("Mau    : nang mau tam (--tam)")
    else: print("Mau    : GIU NGUYEN - ban tu them LUT trong CapCut")
    if n_phang:
        print("         ({}/{} doan do duoc la kha phang, xem ghi-chu.txt)".format(n_phang, len(lay)))
    print("=" * 66)

    ghi, thanh_cong = [], 0
    for i, d in enumerate(lay, 1):
        rel = cfg.N(d["path"])   # path CHINH LA khoa tuong doi - ghep lai tu folder+name thi mat thu muc
        if a.goc:
            nguon = cfg.src(rel)
            if not os.path.exists(nguon):
                nguon = cfg.prox(os.path.splitext(rel)[0] + ".mp4")
        else:
            nguon = cfg.prox(os.path.splitext(rel)[0] + ".mp4")
        if not os.path.exists(nguon):
            print("  [{:02d}] BO QUA - khong thay file: {}".format(i, d["name"][:40])); continue

        nhan = "_".join(x for x in (an_toan(d.get("luc") or ""), an_toan(d.get("dong") or ""),
                                    an_toan(os.path.splitext(d["name"])[0])) if x)
        dich = os.path.join(ra, "{:02d}_{}.mp4".format(i, nhan))

        # Mac dinh giu nguyen mau. Chi xu ly khi nguoi dung go --lut hoac --tam.
        vf = []
        if a.lut or a.lut_sony or a.lut_dji:
            L = lut.get(hang_may(d["name"]))
            if L: vf.append("lut3d=" + L.replace("\\", "/").replace(":", "\\:"))
        elif a.tam:
            vf.append(TAM)
        vf = ",".join(vf) if vf else None

        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin"] + cfg.hwaccel() + \
              ["-ss", str(d["start"]), "-t", str(d["dur"]), "-i", nguon]
        if vf: cmd += ["-vf", vf]
        cmd += ["-r", "30", "-vsync", "cfr", "-video_track_timescale", "30000",
                "-c:v", cfg.encoder(), "-b:v", "12M" if a.goc else "6M",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-y", dich]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode != 0 or not os.path.exists(dich):
            print("  [{:02d}] LOI: {}".format(i, d["name"][:40])); continue
        thanh_cong += 1
        print("  [{:02d}] {:<42} {:>3}s".format(i, os.path.basename(dich)[:42], d["dur"]))
        ph = diem.get(d["path"])
        ghi_mau = ("     mau   : KHA PHANG (diem {:.0f}) - co the can LUT\n".format(ph)
                   if ph is not None and ph >= 35 else
                   "     mau   : trong on (diem {:.0f})\n".format(ph) if ph is not None else "")
        ghi.append(
            "{:02d}. {}\n     nguon : {}\n     doan  : giay {} -> {}  ({} giay)\n"
            "     quay  : {} {}  |  {}  |  {}\n".format(
                i, os.path.basename(dich), rel, d["start"], d["start"] + d["dur"], d["dur"],
                d.get("ngay",""), d.get("gio",""), d.get("luc_ten",""), d.get("dong_ten",""))
            + ghi_mau
            + "     diem  : {:.2f}\n".format(d.get("score", 0)))

    with open(os.path.join(ra, "ghi-chu.txt"), "w", encoding="utf-8") as fh:
        fh.write("NGUON GOC CUA TUNG DOAN\n" + "=" * 60 + "\n\n" + "\n".join(ghi))
    with open(os.path.join(ra, "DOC-TRUOC.txt"), "w", encoding="utf-8") as fh:
        fh.write("""CÁCH DÙNG TRONG CAPCUT
======================

1. Mở CapCut, tạo dự án mới
2. Kéo CẢ THƯ MỤC này thả vào khung Media
3. Các đoạn đã đánh số 01, 02, 03... nên sẽ vào đúng thứ tự
4. Chọn tất cả, kéo xuống dòng thời gian (timeline)

Tên file cho biết: số thứ tự _ lúc quay trong ngày _ kiểu chuyển động _ clip gốc
Muốn biết đoạn này cắt từ giây nào của clip gốc, mở file ghi-chu.txt

VỀ MÀU
------
Các đoạn này XUẤT NGUYÊN BẢN, không đụng gì vào màu. Bạn tự thêm bộ màu
(LUT) trong CapCut cho chắc.

Nếu đã chạy bước đo màu, trong ghi-chu.txt mỗi đoạn có một dòng "mau":
  - "KHA PHANG"  -> nhiều khả năng quay chế độ màu nhạt (log), nên thêm LUT
  - "trong on"   -> nhiều khả năng đã có màu sẵn, không cần đụng vào
Đây chỉ là PHỎNG ĐOÁN đo bằng máy. Cảnh trong nhà hay trời mù vốn ít
tương phản nên cũng bị chấm là phẳng dù không hề quay log. Mắt bạn
quyết, đừng tin con số này.

LƯU Ý: các đoạn này được máy chấm điểm kỹ thuật (nét, ổn định, đủ sáng).
Máy không biết ý bạn muốn kể. Chọn bỏ cái nào, cắt ở đâu, xếp thứ tự
nào vẫn là việc của bạn.
""")
    print("\nXong {}/{} doan.".format(thanh_cong, len(lay)))
    if thanh_cong == 0:
        print("!! KHONG XUAT DUOC DOAN NAO - dung keo thu muc nay vao CapCut.")
        print("   Thuong la chua co proxy (chay proxy.py --run), hoac dung --goc khi o footage chua cam.")
        sys.exit(1)
    if thanh_cong < len(lay):
        print("!! Thieu {} doan - xem cac dong BO QUA / LOI o tren.".format(len(lay) - thanh_cong))
    print("Keo ca thu muc nay tha vao CapCut:\n  {}".format(ra))
    con.close()

if __name__ == "__main__":
    main()
