# -*- coding: utf-8 -*-
"""Buoc NGHE: tieng -> chu co moc thoi gian tung tu, do khoang lang, soan nhap phu de.

Ra trong thu muc du an:
  loi.json      moi tu: {i, f (file thu may), w, s, e, p}
  loi.txt       ban doc duoc, danh so tu - de soan bang dung
  lang.json     khoang im that (do bang ffmpeg silencedetect), theo tung file
  phu-de.txt    ban NHAP phu de (chi tao neu chua co) - AI sua lai truoc khi dung
"""
import os, re, sys, json
sys.dont_write_bytecode = True
import cfg

MODEL = "mlx-community/whisper-large-v3-turbo"
DAU_CAU = re.compile(r"[.!?…]$")


def tach_tieng(src, dich):
    cfg.chay([cfg.ffmpeg(), "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", dich], im=True)


def do_lang(src, nguong_db, toi_thieu=0.18):
    r = cfg.chay([cfg.ffmpeg(), "-hide_banner", "-i", src, "-vn", "-af",
                  "highpass=f=90,silencedetect=noise={}dB:d={}".format(nguong_db, toi_thieu), "-f", "null", "-"], im=True)
    ds, bd = [], None
    for dong in r.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", dong)
        if m:
            bd = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+)", dong)
        if m and bd is not None:
            ds.append([round(bd, 3), round(float(m.group(1)), 3)])
            bd = None
    if bd is not None:
        ds.append([round(bd, 3), 1e9])
    return ds


def nghe_file(wav, goi_y):
    try:
        import mlx_whisper
    except ImportError:
        raise SystemExit("Chưa cài bộ nghe. Chạy: pip3 install mlx-whisper pillow numpy (chỉ chạy được trên Mac chip Apple). Kiểm lại bằng: python3 dv.py kiem")
    kq = mlx_whisper.transcribe(wav, path_or_hf_repo=MODEL, language="vi", word_timestamps=True,
                                condition_on_previous_text=False, initial_prompt=goi_y or None,
                                hallucination_silence_threshold=2.0)
    tu = []
    for seg in kq.get("segments", []):
        for w in seg.get("words", []):
            chu = w["word"].strip()
            if chu:
                tu.append({"w": chu, "s": round(w["start"], 3), "e": round(w["end"], 3),
                           "p": round(w.get("probability", 1), 2)})
    return tu


# ---- nghe lan hai bang PhoWhisper (VinAI, BSD-3) roi doi chieu ----
# Moi bo nghe gioi mot kieu: Pho nghe tu tieng Viet tot hon, nhung viet so bang chu ("ba muoi phut"), doi khi
# lam mat nua cau hoac bia them cau o cuoi file. Khong ben nao thang han -> turbo lam chinh (moc thoi gian,
# con so), Pho chi de CHI RA CHO LECH cho AI soat khi viet phu de.
MODEL_PHO = os.path.join(cfg.thu_muc_cong_cu(".models"), "phowhisper-large-mlx")
DEM = {"à", "ờ", "ừ", "á", "ạ", "ơ", "cái", "mình", "thì", "là", "và", "mà", "đó", "đấy", "ở", "này", "nhé", "nhá", "thế", "rồi", "cũng"}
SO = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def so_thanh_chu(n):
    """30 -> 'ba mươi' (du dung de so khop, khong can dung chinh ta tung ca)."""
    if n < 10:
        return SO[n]
    if n < 20:
        return "mười" + ("" if n == 10 else " " + ("lăm" if n % 10 == 5 else SO[n % 10]))
    if n < 100:
        dv = n % 10
        return SO[n // 10] + " mươi" + ("" if dv == 0 else " " + {1: "mốt", 5: "lăm"}.get(dv, SO[dv]))
    if n < 1000:
        du = n % 100
        return SO[n // 100] + " trăm" + ("" if du == 0 else (" lẻ " + SO[du] if du < 10 else " " + so_thanh_chu(du)))
    return str(n)


def chuan(w):
    w = re.sub(r"[^\w\s-]", "", w.lower()).strip()
    if re.fullmatch(r"\d+", w):
        return so_thanh_chu(int(w)).split()
    if re.fullmatch(r"\d+-\d+", w):
        a, b = w.split("-")
        return so_thanh_chu(int(a)).split() + so_thanh_chu(int(b)).split()
    return [w] if w else []


def doi_chieu(tu, tu_pho):
    """-> danh sach cho lech: (i_dau, i_cuoi, chu turbo, chu pho). i = so tu trong loi.json."""
    import difflib
    a, ai = [], []
    for t in tu:
        for x in chuan(t["w"]):
            a.append(x); ai.append(t["i"])
    b = [x for t in tu_pho for x in chuan(t["w"])]
    lech = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        chu_a, chu_b = " ".join(a[i1:i2]), " ".join(b[j1:j2])
        # mot ben nghe them toan tieng dem / chu lap ("cai cai cai", "minh minh") -> khong phai lech noi dung
        mot_ben = a[i1:i2] if not chu_b else (b[j1:j2] if not chu_a else None)
        if mot_ben is not None and all(x in DEM for x in mot_ben):
            continue
        i_dau = ai[i1] if i1 < len(ai) else ai[-1]
        i_cuoi = ai[i2 - 1] if i2 > i1 else i_dau
        lech.append((i_dau, i_cuoi, chu_a, chu_b))
    return lech


def cai_pho():
    """Tai PhoWhisper-large (6,2 GB, huggingface.co/vinai) + script chuyen doi chinh thuc cua Apple
    (github.com/ml-explore/mlx-examples, whisper/convert.py) -> ban MLX 2,9 GB o <thu muc du lieu>/.models/.
    Can torch va huggingface_hub. Mat khoang 5 phut tai + 2 phut chuyen (tuy mang)."""
    import subprocess, urllib.request
    if os.path.exists(os.path.join(MODEL_PHO, "config.json")):
        print("PhoWhisper MLX da co:", MODEL_PHO); return
    try:
        import torch, huggingface_hub  # noqa
    except Exception:
        sys.exit("!! Can them hai goi de chuyen doi: pip3 install torch huggingface_hub")
    goc = os.path.dirname(MODEL_PHO)
    os.makedirs(goc, exist_ok=True)
    conv = os.path.join(goc, "mlx_convert.py")
    if not os.path.exists(conv):
        urllib.request.urlretrieve("https://raw.githubusercontent.com/ml-explore/mlx-examples/main/whisper/convert.py", conv)
    from huggingface_hub import snapshot_download
    print("Tai vinai/PhoWhisper-large (6,2GB)...")
    snap = snapshot_download("vinai/PhoWhisper-large", allow_patterns=["*.json", "*.txt", "pytorch_model.bin"])
    print("Chuyen sang MLX...")
    r = subprocess.run([sys.executable, conv, "--torch-name-or-path", snap, "--mlx-path", MODEL_PHO, "--dtype", "float16"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:]); sys.exit("!! Chuyen doi loi")
    # convert.py moi luu model.safetensors, mlx_whisper tren may doc weights.safetensors
    w = os.path.join(MODEL_PHO, "weights.safetensors")
    if not os.path.exists(w):
        os.symlink("model.safetensors", w)
    print("Xong:", MODEL_PHO, "- ban goc 6,2GB trong ~/.cache/huggingface co the xoa neu can cho")


def dong_doc(tu, khoang_ngat=0.45):
    """Gom tu thanh dong theo cho ngung / dau cau - de doc va soan bang dung."""
    dong, cur = [], []
    for k, t in enumerate(tu):
        if cur and (t["f"] != cur[-1]["f"] or t["s"] - cur[-1]["e"] > khoang_ngat or len(cur) >= 18):
            dong.append(cur); cur = []
        cur.append(t)
        if DAU_CAU.search(t["w"]):
            dong.append(cur); cur = []
    if cur:
        dong.append(cur)
    return dong


def nhap_phu_de(tu, toi_da_tu=5, toi_da_ky_tu=24):
    """Cat nhap: 2-5 tu mot lan hien, ngat o cho ngung va dau cau. AI se sua chu sai + chon tu nhan."""
    def diem_ngat(a, b):
        """Ngat truoc b tot co nao: khoang ngung dai, b viet hoa (whisper hoa dau cau), a co dau cau."""
        d = b["s"] - a["e"]
        if re.search(r"[.,!?…:;]$", a["w"]):
            d += 0.5
        if b["w"][:1].isupper():
            d += 0.3
        if re.match(r"^\d", a["w"]):          # "30 | phut" - dung tach so khoi don vi
            d -= 0.5
        return d

    # 1) tach thanh cau o cho ngung dai / dau cau
    cau, cur = [], []
    for t in tu:
        if cur and (t["f"] != cur[-1]["f"] or t["s"] - cur[-1]["e"] > 0.45):
            cau.append(cur); cur = []
        cur.append(t)
        if re.search(r"[.!?…]$", t["w"]):
            cau.append(cur); cur = []
    if cur:
        cau.append(cur)

    # 2) moi cau chia toi uu (quy hoach dong): nham 3-4 tu mot lan hien, ngat o cho tot nhat
    def gia(ds, i, j):
        n, dai = j - i, len(" ".join(x["w"] for x in ds[i:j]))
        if n > toi_da_tu + 1 or (dai > toi_da_ky_tu and n > 1):
            return 1e9
        c = 0.25 * (n - 3.5) ** 2 + (1.2 if n == 1 else 0)
        if j < len(ds):
            c -= 2.0 * diem_ngat(ds[j - 1], ds[j])
        return c

    cum = []
    for ds in cau:
        n = len(ds)
        tot, tr = [0.0] + [1e18] * n, [0] * (n + 1)
        for j in range(1, n + 1):
            for i in range(max(0, j - toi_da_tu - 1), j):
                v = tot[i] + gia(ds, i, j)
                if v < tot[j]:
                    tot[j], tr[j] = v, i
        cat_, j = [], n
        while j > 0:
            cat_.append(ds[tr[j]:j]); j = tr[j]
        cum += cat_[::-1]
    dong = ["# Moi dong = mot lan hien chu.  <tu dau>-<tu cuoi> | dong nho // DONG TO",
            "# So la so thu tu tu trong loi.txt. Chu hien thi sua thoai mai, moc thoi gian van theo so.",
            "# Chi dong nho  -> go tung chu co con tro.  Co '// ...' -> dong to dam nghieng hien mo dan.",
            "# Chi '// ...'   -> mot dong to.   Xoa dong = khong hien chu doan do.", ""]
    for c in cum:
        chu = " ".join(re.sub(r"[.,!?…:;]+$", "", x["w"]) for x in c).lower()
        dong.append("{}-{} | {}".format(c[0]["i"], c[-1]["i"], chu))
    return "\n".join(dong) + "\n"


def main(ten):
    d = cfg.du_an(ten)
    bd = cfg.doc_json(os.path.join(d, "bang-dung.json"))
    nguon = bd["nguon"]
    tat_ca = []
    lang = []
    for f, src in enumerate(nguon):
        if not os.path.exists(src):
            sys.exit("!! Khong thay file nguon: " + src)
        wav = os.path.join(d, "tieng-{}.wav".format(f))
        print("[{}/{}] Tach tieng + nghe: {}".format(f + 1, len(nguon), os.path.basename(src)))
        tach_tieng(src, wav)
        tu = nghe_file(wav, bd.get("goi_y_tu", ""))
        for t in tu:
            t["f"] = f
        tat_ca += tu
        lang.append(do_lang(wav, bd.get("nguong_lang_db", -35)))
        print("      {} tu, {} khoang im".format(len(tu), len(lang[-1])))
    for i, t in enumerate(tat_ca):
        t["i"] = i
        t.update({k: t.pop(k) for k in ("f", "w", "s", "e", "p")})   # sap thu tu khoa cho de doc
    cfg.ghi_json(os.path.join(d, "loi.json"), tat_ca)
    cfg.ghi_json(os.path.join(d, "lang.json"), lang)

    nghi_ngo = sum(1 for t in tat_ca if t["p"] < 0.5)
    with open(os.path.join(d, "loi.txt"), "w", encoding="utf-8") as fo:
        fo.write("# [tu dau-tu cuoi] file  thoi diem | loi noi.   Tu co dau ? = may nghe khong chac (p<0.5)\n")
        for dg in dong_doc(tat_ca):
            chu = " ".join(t["w"] + ("?" if t["p"] < 0.5 else "") for t in dg)
            fo.write("[{:04d}-{:04d}] f{} {} | {}\n".format(dg[0]["i"], dg[-1]["i"], dg[0]["f"], cfg.tg(dg[0]["s"]), chu))
    # nghe lan hai (neu may co PhoWhisper va bang dung khong tat)
    p_dc = os.path.join(d, "loi-doi-chieu.txt")
    if bd.get("nghe_kep", True) and os.path.exists(os.path.join(MODEL_PHO, "config.json")):
        import mlx_whisper
        dong = ["# Cho hai bo nghe KHAC NHAU. turbo = ban dang dung (loi.txt). pho = PhoWhisper (VinAI, luyen rieng tieng Viet).",
                "# Khong ben nao luon dung: Pho gioi tu tieng Viet, turbo gioi con so va it mat cau. Soat khi viet phu de.", ""]
        tong_lech = 0
        for f, src in enumerate(nguon):
            print("Nghe lan hai bang PhoWhisper: file {} ...".format(f + 1))
            wav = os.path.join(d, "tieng-{}.wav".format(f))
            kq = mlx_whisper.transcribe(wav, path_or_hf_repo=MODEL_PHO, language="vi", word_timestamps=True,
                                        condition_on_previous_text=False, hallucination_silence_threshold=2.0)
            tu_pho = [{"w": w["word"].strip()} for sg in kq.get("segments", []) for w in sg.get("words", []) if w["word"].strip()]
            lech = doi_chieu([t for t in tat_ca if t["f"] == f], tu_pho)
            tong_lech += len(lech)
            for i1, i2, x, y in lech:
                dong.append("[{:04d}-{:04d}] {} | turbo: {:<28} | pho: {}".format(
                    i1, i2, cfg.tg(tat_ca[i1]["s"]), x or "(khong co)", y or "(khong co)"))
        open(p_dc, "w", encoding="utf-8").write("\n".join(dong) + "\n")
        print("Doi chieu: {} cho hai bo nghe khac nhau -> loi-doi-chieu.txt".format(tong_lech))
    elif os.path.exists(p_dc):
        os.remove(p_dc)
    pd = os.path.join(d, "phu-de.txt")
    if not os.path.exists(pd):
        open(pd, "w", encoding="utf-8").write(nhap_phu_de(tat_ca))
        print("Da soan nhap phu-de.txt")
    else:
        print("phu-de.txt da co - KHONG ghi de. Xoa di neu muon soan nhap lai.")
    print("Xong: {} tu ({} tu may nghe khong chac) -> loi.txt".format(len(tat_ca), nghi_ngo))


if __name__ == "__main__":
    main(sys.argv[1])
