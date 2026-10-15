# -*- coding: utf-8 -*-
"""Buoc SOI: tu soi tung cho cat tren ban da dung - hoc tu browser-use/video-use (MIT).

Moi cho cat ra mot dai anh: 4 khung hinh quanh vet cat (-0.4 · -0.1 · +0.1 · +0.4 giay) + song am
+-0.8 giay co vach do + chu truoc/sau. Ghep 6 cho cat mot tam, nen duoi 195KB de doc duoc.
Kem hai phep do bang so (khong can nhin):
  - "bup": o 20ms ngay vet cat to hon han hai ben (tieng tach khi noi hai khuc am)
  - "lem tieng": ngay truoc/sau vet cat van dang co tieng noi to -> co the cat vao giua chu
Doc bang: python3 dv.py soi <ten> [--nhap]
"""
import os, sys, json, subprocess
sys.dont_write_bytecode = True
import cfg

W_KHUNG = 150      # be ngang moi khung hinh trong dai anh
MOI_TAM = 6        # so cho cat moi tam anh


def _am_thanh(video):
    import numpy as np
    r = subprocess.run([cfg.ffmpeg(), "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                       capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.int16).astype("float32") / 32768.0


def _db(x):
    import numpy as np
    return 20 * np.log10(max(1e-6, float(np.sqrt(np.mean(x * x))) if len(x) else 1e-6))


def do_so(am, t, sr=16000):
    """-> (bup_db, tieng_truoc_db, tieng_sau_db, nen_db) quanh vet cat t."""
    import numpy as np
    i = int(t * sr)
    o = int(0.02 * sr)
    giua = am[max(0, i - o // 2): i + o // 2]
    hai_ben = np.concatenate([am[max(0, i - 4 * o): max(0, i - 2 * o)], am[i + 2 * o: i + 4 * o]])
    bup = _db(giua) - _db(hai_ben)
    truoc = _db(am[max(0, i - int(0.03 * sr)): i])
    sau = _db(am[i: i + int(0.03 * sr)])
    ca = am[max(0, i - sr): i + sr]
    return bup, truoc, sau, _db(ca)


def dai_anh(video, moc, dich_png, font):
    from PIL import Image, ImageDraw
    t = moc["t"]
    anh = []
    for dt in (-0.4, -0.1, 0.1, 0.4):
        p = dich_png + "_{}.jpg".format(dt)
        subprocess.run([cfg.ffmpeg(), "-v", "error", "-y", "-ss", "{:.3f}".format(max(0, t + dt)), "-i", video,
                        "-frames:v", "1", "-vf", "scale={}:-2".format(W_KHUNG), "-q:v", "6", p])
        anh.append(Image.open(p).convert("RGB") if os.path.exists(p) else Image.new("RGB", (W_KHUNG, 266)))
    h_k = anh[0].height
    song = dich_png + "_song.png"
    subprocess.run([cfg.ffmpeg(), "-v", "error", "-y", "-ss", "{:.3f}".format(max(0, t - 0.8)), "-t", "1.6", "-i", video,
                    "-filter_complex", "aformat=channel_layouts=mono,showwavespic=s={}x70:colors=0x33cc66".format(4 * W_KHUNG),
                    "-frames:v", "1", song])
    rong = 4 * W_KHUNG
    img = Image.new("RGB", (rong, h_k + 70 + 46), (18, 18, 18))
    for k, a in enumerate(anh):
        img.paste(a, (k * W_KHUNG, 0))
    d = ImageDraw.Draw(img)
    d.line([(2 * W_KHUNG, 0), (2 * W_KHUNG, h_k)], fill=(255, 60, 60), width=2)
    if os.path.exists(song):
        img.paste(Image.open(song).convert("RGB"), (0, h_k))
    x_cat = int(rong * 0.8 / 1.6)
    d.line([(x_cat, h_k), (x_cat, h_k + 70)], fill=(255, 60, 60), width=2)
    nhan = "{} {} {}".format(cfg.tg(t), moc["loai"], ("!! " + moc["co"]) if moc.get("co") else "")
    d.text((6, h_k + 72), nhan, fill=(255, 210, 80) if moc.get("co") else (220, 220, 220), font=font)
    chu = "{}  |  {}".format(moc.get("truoc", "")[-30:], moc.get("sau", "")[:30])
    d.text((6, h_k + 94), chu, fill=(200, 200, 200), font=font)
    for p in [dich_png + "_{}.jpg".format(x) for x in (-0.4, -0.1, 0.1, 0.4)] + [song]:
        if os.path.exists(p):
            os.remove(p)
    return img


def ghep_tam(dai, dich):
    """Ghep cac dai anh thanh luoi 2 cot, nen tu dong cho duoi 190KB."""
    from PIL import Image
    if not dai:
        return None
    w, h = dai[0].size
    cot = 2
    hang = (len(dai) + cot - 1) // cot
    tam = Image.new("RGB", (cot * w + 6, hang * h + 6 * (hang - 1)), (0, 0, 0))
    for k, a in enumerate(dai):
        tam.paste(a, ((k % cot) * (w + 6), (k // cot) * (h + 6)))
    for q in (80, 70, 60, 50, 40, 30):
        tam.save(dich, quality=q)
        if os.path.getsize(dich) < 190_000:
            break
    return dich


def soi(d, video, moc_file):
    from PIL import ImageFont
    if not os.path.exists(video) or not os.path.exists(moc_file):
        sys.exit("!! Chua co ban dung hoac file moc cat: {}\nDung lai bang dv.py dung truoc.".format(video))
    moc = json.load(open(moc_file, encoding="utf-8"))
    am = _am_thanh(video)
    font = ImageFont.truetype(os.path.join(cfg.FONTS, "BeVietnamPro-Medium.ttf"), 15)
    ra = os.path.join(d, "soi")
    os.makedirs(ra, exist_ok=True)
    for f in os.listdir(ra):
        os.remove(os.path.join(ra, f))
    co_loi = []
    for m in moc:
        bup, truoc, sau, nen = do_so(am, m["t"])
        loi = []
        # chi vet CAT moi noi hai khuc am; doi khung / chen hinh thi tieng van chay lien -> khong the bup
        if m["loai"] == "cat" and bup > 9 and max(truoc, sau) > -45:
            loi.append("bup {:+.0f}dB".format(bup))
        # dang noi to sat vet cat (ca hai phia deu gan muc tieng noi cua doan) -> nghi cat vao chu
        if m["loai"] == "cat" and min(truoc, sau) > nen - 4 and min(truoc, sau) > -32:
            loi.append("lem tieng")
        m["co"] = ", ".join(loi)
        if loi:
            co_loi.append(m)
    # uu tien ve cho co loi, roi toi cac cho cat that; chen/doi khung chi ve khi co loi
    ve = [m for m in moc if m["co"]] + [m for m in moc if not m["co"] and m["loai"] == "cat"]
    tam = []
    for k in range(0, len(ve), MOI_TAM):
        dai = [dai_anh(video, m, os.path.join(ra, "_t{}".format(i)), font) for i, m in enumerate(ve[k:k + MOI_TAM], k)]
        p = ghep_tam(dai, os.path.join(ra, "soi-{:02d}.jpg".format(k // MOI_TAM + 1)))
        if p:
            tam.append(p)
    dem = {}
    for m in moc:
        dem[m["loai"]] = dem.get(m["loai"], 0) + 1
    print("Soi {} moc ({}) -> ve {} dai anh vao {} tam".format(
        len(moc), ", ".join("{} {}".format(v, k) for k, v in dem.items()), len(ve), len(tam)))
    print("Nghi co loi: {} cho".format(len(co_loi)))
    for m in co_loi:
        print("  {}  {:<9} {:<18}  ...{} | {}...".format(cfg.tg(m["t"]), m["loai"], m["co"], m.get("truoc", "")[-24:], m.get("sau", "")[:24]))
    for p in tam:
        print("  " + p)
    print("=> Mo tung tam anh ra nhin. So do la GOI Y: 'lem tieng' co the la noi lien mach tu nhien; nhin song am roi moi sua.")
