# -*- coding: utf-8 -*-
"""Xuat thang thanh DU AN CAPCUT (Mac, CapCut 9.x) - mo CapCut la thay timeline dung san, sua tay tiep.

    python3 dv.py capcut <ten> [--khong-chep]

Khac bo lop roi (lop/): track chinh la TUNG DOAN quay tro ve file goc, nen keo dai / rut ngan tung
vet cat duoc. Timeline:
  track chinh   : cac doan A-roll (cat doc 9:16 + zoom doi khung bang thong so phong to cua clip)
  video chong 1 : B-roll (ban cat san co 2 giay du hai dau de keo them)
  video chong 2 : the chu / danh sach / anh bang chung - moi cai mot clip rieng
  video chong 3 : lop phu de dep (MOV trong suot, giu hieu ung go chu)
  chu           : phu de bang chu CapCut, SUA DUOC tung dong - de AN san; muon sua thi bat len, an lop 3

Khuon du an (capcut_mau.json) rut tu mot du an trong do CapCut 9.2 tao, da xoa moi ma may va noi dung.
Dinh dang KHONG co tai lieu chinh thuc - CapCut cap nhat co the doi. Doc "Bay" trong SKILL.md truoc khi sua.
Mau (LUT) KHONG mang sang CapCut: muon chinh mau thi them trong CapCut.

CapCut tren Mac chay trong hop cat: ~/Library/Containers/com.lemon.lvoverseas/Data/Movies tro ve ~/Movies,
nen file dat trong ~/Movies thi CapCut tu doc duoc. Media du an chep vao ~/Movies/CreatorVideo/<ten>/.
"""
import os, sys, json, uuid, copy, shutil, subprocess, time, datetime
sys.dont_write_bytecode = True
import cfg, cat, hf, chen, chu

DRAFTS = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
MEDIA = os.path.expanduser("~/Movies/CreatorVideo")
MAU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "capcut_mau.json")
US = 1_000_000
W, H = cfg.W, cfg.H


def uid():
    return str(uuid.uuid4()).upper()


def us(t):
    return int(round(t * US))


def khung_capcut(sw, sh, zoom, x, y):
    """Vung cat 9:16 (giong cat.khung_crop) -> (scale, transform_x, transform_y) cua clip CapCut.
    CapCut dat clip vua khit canvas (fit) o scale 1; transform tinh bang nua be canvas, truc y huong len."""
    cw, ch, cx, cy = cat.khung_crop(sw, sh, zoom, x, y)
    fit = min(W / float(sw), H / float(sh))
    k = W / float(cw)                       # 1 pixel nguon = k pixel canvas khi da cat day khung
    tam_x, tam_y = cx + cw / 2.0, cy + ch / 2.0
    tx = (sw / 2.0 - tam_x) * k / (W / 2.0)
    ty = -(sh / 2.0 - tam_y) * k / (H / 2.0)
    return k / fit, tx, ty


class DuAn:
    def __init__(self):
        self.mau = json.load(open(MAU, encoding="utf-8"))
        self.d = copy.deepcopy(self.mau["draft_info"])
        self.d["id"] = uid()
        self.d["canvas_config"] = {"ratio": "9:16", "width": W, "height": H, "background": None}
        self.d["fps"] = float(cfg.FPS)
        self.d["tracks"] = []
        self.nhap_vao = []           # vat lieu da "nhap" - cho draft_meta_info

    def _phu(self):
        ids = []
        for k, x in self.mau["refs_video"].items():
            m = copy.deepcopy(x)
            m["id"] = uid()
            self.d["materials"].setdefault(k, []).append(m)
            ids.append(m["id"])
        return ids

    def vat_lieu(self, path, loai="video"):
        ts = cfg.thong_so(path)
        m = copy.deepcopy(self.mau["video_material"])
        lid = str(uuid.uuid4())
        m.update({"id": uid(), "path": path, "material_name": os.path.basename(path), "width": ts["w"],
                  "height": ts["h"], "duration": us(ts["dai"]), "has_audio": ts["tieng"], "type": loai,
                  "local_material_id": lid, "unique_id": uuid.uuid4().hex, "has_sound_separated": False})
        self.d["materials"]["videos"].append(m)
        if lid not in [x["id"] for x in self.nhap_vao]:
            self.nhap_vao.append({"id": lid, "path": path, "w": ts["w"], "h": ts["h"], "dai": ts["dai"], "loai": loai})
        m["_ts"] = ts
        return m

    def track(self, loai, flag=0):
        t = {"attribute": 0, "flag": flag, "id": uid(), "is_default_name": True, "name": "", "type": loai, "segments": []}
        self.d["tracks"].append(t)
        return t

    def doan_video(self, tr, m, src_us, dai_us, dst_us, scale=1.0, tx=0.0, ty=0.0, lop=0, am=1.0):
        s = copy.deepcopy(self.mau["segment_video"])
        s.update({"id": uid(), "material_id": m["id"], "extra_material_refs": self._phu(),
                  "source_timerange": {"start": src_us, "duration": dai_us},
                  "target_timerange": {"start": dst_us, "duration": dai_us},
                  "render_index": lop, "track_render_index": lop, "track_attribute": 0,
                  "volume": am, "last_nonzero_volume": 1.0, "visible": True, "speed": 1.0,
                  "common_keyframes": [], "keyframe_refs": [], "uniform_scale": {"on": True, "value": 1.0}})
        s["clip"] = {"alpha": 1.0, "flip": {"horizontal": False, "vertical": False}, "rotation": 0.0,
                     "scale": {"x": scale, "y": scale}, "transform": {"x": tx, "y": ty}}
        tr["segments"].append(s)
        return s

    def doan_chu(self, tr, chu_, dst_us, dai_us, y, lop, hien=False):
        m = copy.deepcopy(self.mau["text_material"])
        m["id"] = uid()
        m["content"] = json.dumps({"styles": [{"fill": {"content": {"solid": {"color": [1, 1, 1]}, "render_type": "solid"}},
                                               "range": [0, len(chu_)], "size": 9, "bold": True}], "text": chu_},
                                  ensure_ascii=False)
        m.update({"font_size": 9.0, "alignment": 1, "background_alpha": 0.0, "background_style": 0,
                  "has_shadow": True, "shadow_alpha": 0.6, "shadow_color": "#000000", "border_width": 0.0})
        self.d["materials"]["texts"].append(m)
        s = copy.deepcopy(self.mau["segment_text"])
        s.update({"id": uid(), "material_id": m["id"], "extra_material_refs": [],
                  "target_timerange": {"start": dst_us, "duration": dai_us}, "source_timerange": None,
                  "render_index": 14000 + lop, "track_render_index": lop, "visible": hien,
                  "common_keyframes": [], "keyframe_refs": []})
        s["clip"] = {"alpha": 1.0, "flip": {"horizontal": False, "vertical": False}, "rotation": 0.0,
                     "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": y}}
        tr["segments"].append(s)

    def ghi(self, ten, tong, thu=None):
        """Ghi thu muc du an vao kho CapCut + dang ky vao danh sach. Khong bao gio ghi de du an co san.
        thu = thu muc nhap: ghi ra do, KHONG dang ky vao CapCut (de kiem bo xuat)."""
        global DRAFTS
        if thu:
            DRAFTS = thu
            os.makedirs(thu, exist_ok=True)
        elif pgrep_capcut():
            sys.exit("!! CapCut dang mo. Dong CapCut truoc (CapCut ghi lai danh sach du an luc thoat, se xoa mat du an moi).")
        ten_tm, k = ten, 2
        while os.path.exists(os.path.join(DRAFTS, ten_tm)):
            ten_tm = "{}-{}".format(ten, k); k += 1
        fd = os.path.join(DRAFTS, ten_tm)
        tid = self.d["id"]
        bay_gio = int(time.time() * US)
        self.d["duration"] = us(tong)
        for m in self.d["materials"]["videos"]:
            m.pop("_ts", None)
        os.makedirs(os.path.join(fd, "Timelines", tid))
        noi = json.dumps(self.d, ensure_ascii=False)
        open(os.path.join(fd, "draft_info.json"), "w", encoding="utf-8").write(noi)
        open(os.path.join(fd, "Timelines", tid, "draft_info.json"), "w", encoding="utf-8").write(noi)
        pj = copy.deepcopy(self.mau["project"])
        pj.update({"id": uid(), "main_timeline_id": tid, "create_time": bay_gio, "update_time": bay_gio})
        pj["timelines"] = [{"create_time": bay_gio, "id": tid, "is_marked_delete": False, "name": "Dòng thời gian 01",
                            "update_time": bay_gio}]
        json.dump(pj, open(os.path.join(fd, "Timelines", "project.json"), "w", encoding="utf-8"), ensure_ascii=False)
        json.dump({"dockItems": [{"dockIndex": 0, "ratio": 1, "timelineIds": [tid], "timelineNames": ["Dòng thời gian 01"]}],
                   "layoutOrientation": 1}, open(os.path.join(fd, "timeline_layout.json"), "w", encoding="utf-8"), ensure_ascii=False)
        s = int(time.time())
        open(os.path.join(fd, "draft_settings"), "w").write(
            "[General]\ncloud_last_modify_platform=mac\ndraft_create_time={}\ndraft_last_edit_time={}\nreal_edit_keys=0\nreal_edit_seconds=0\n".format(s, s))
        open(os.path.join(fd, "draft_agency_config.json"), "w").write(
            '{"is_auto_agency_enabled":false,"is_auto_agency_popup":false,"is_single_agency_mode":false,"marterials":null,"use_converter":false,"video_resolution":720}')
        open(os.path.join(fd, "draft_biz_config.json"), "w").write("")
        open(os.path.join(fd, "key_value.json"), "w").write("{}")
        meta = copy.deepcopy(self.mau["draft_meta_info"])
        did = uid()
        vao = [{"ai_group_type": "", "create_time": s, "duration": us(x["dai"]), "enter_from": 0,
                "extra_info": os.path.basename(x["path"]), "file_Path": x["path"], "height": x["h"], "id": x["id"],
                "import_time": s, "import_time_ms": bay_gio, "item_source": 1, "material_color_tag": "", "md5": "",
                "metetype": "video", "roughcut_time_range": {"duration": us(x["dai"]), "start": 0},
                "sub_time_range": {"duration": -1, "start": -1}, "type": 0, "width": x["w"]} for x in self.nhap_vao]
        meta.update({"draft_fold_path": fd, "draft_id": did, "draft_name": ten_tm, "draft_root_path": DRAFTS,
                     "tm_draft_create": bay_gio, "tm_draft_modified": bay_gio, "tm_duration": us(tong),
                     "draft_materials": [{"type": 0, "value": vao}, {"type": 1, "value": []}, {"type": 2, "value": []},
                                         {"type": 3, "value": []}, {"type": 6, "value": []}]})
        json.dump(meta, open(os.path.join(fd, "draft_meta_info.json"), "w", encoding="utf-8"), ensure_ascii=False)
        if not thu:
            dang_ky(fd, ten_tm, did, bay_gio, us(tong))
        return fd, ten_tm


def pgrep_capcut():
    r = subprocess.run(["pgrep", "-x", "CapCut"], capture_output=True, text=True)
    return bool(r.stdout.strip())


def dang_ky(fd, ten, did, bay_gio, tong_us):
    """Them du an vao root_meta_info.json (danh sach CapCut hien o man hinh dau). Sao luu truoc."""
    p = os.path.join(DRAFTS, "root_meta_info.json")
    if not os.path.exists(p):
        print("!! Khong thay root_meta_info.json - CapCut se tu quet thu muc (co the phai mo lai app)")
        return
    sl = p + ".truoc-dung-video-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(p, sl)
    r = json.load(open(p, encoding="utf-8"))
    ds = r.setdefault("all_draft_store", [])
    mau = copy.deepcopy(ds[0]) if ds else {}
    mau.update({"draft_cover": os.path.join(fd, "draft_cover.jpg"), "draft_fold_path": fd, "draft_id": did,
                "draft_json_file": os.path.join(fd, "draft_info.json"), "draft_name": ten, "draft_root_path": DRAFTS,
                "tm_draft_create": bay_gio, "tm_draft_modified": bay_gio, "tm_draft_removed": 0, "tm_duration": tong_us,
                "draft_is_invisible": False, "draft_timeline_materials_size": 0})
    ds.insert(0, mau)
    r["draft_ids"] = int(r.get("draft_ids", len(ds) - 1)) + 1
    json.dump(r, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    print("Dang ky vao danh sach CapCut (sao luu: {})".format(os.path.basename(sl)))


def chep_nguon(p, md):
    """File goc -> ~/Movies/CreatorVideo/<ten>/ (CapCut doc duoc)."""
    if not os.path.exists(p):
        sys.exit("!! Khong thay file nguon (o ngoai chua cam?): " + p)
    dich = os.path.join(md, "nguon-" + os.path.basename(p))
    if not (os.path.exists(dich) and os.path.getsize(dich) == os.path.getsize(p)):
        print("  chep {} ({:.0f} MB)...".format(os.path.basename(p), os.path.getsize(p) / 1e6))
        shutil.copy2(p, dich)
    return dich


def xuat(a, dv):
    """a: tham so dong lenh; dv: module dv (de dung chung tinh_chen / tinh_phu_de)."""
    d = cfg.du_an(a.ten)
    bd = cfg.doc_json(os.path.join(d, "bang-dung.json"))
    tu = cfg.doc_json(os.path.join(d, "loi.json"))
    lang = cfg.doc_json(os.path.join(d, "lang.json"))
    if tu is None:
        sys.exit("Chua nghe. Chay: python3 dv.py nghe " + a.ten)
    canh_bao = []
    md = os.path.join(MEDIA, a.ten)
    os.makedirs(md, exist_ok=True)

    # --- ke hoach: y het lenh dung ---
    ts_nguon = [cfg.thong_so(p)["dai"] if os.path.exists(p) else max([t["e"] for t in tu if t["f"] == f] or [0]) + 1.0
                for f, p in enumerate(bd["nguon"])]
    doan, tk = cat.tinh_doan(tu, lang, bd, ts_nguon)
    doi, tong = cat.anh_xa(doan)
    chen_ds = dv.tinh_chen(bd, tu, doi, tong, canh_bao)
    _, cum_ok, _, _ = dv.tinh_phu_de(d, bd, tu, doi, tong, chen_ds)
    y_goc = int(chu.PY * float(bd.get("phu_de_y", 0.70)))
    dong_co = bd.get("dong_co") or ("hyperframes" if hf.co_san() else "ass")

    du = DuAn()
    # --- track chinh: tung doan A-roll tro ve file goc ---
    print("Chuan bi media vao {}".format(md))
    nguon = []
    for p in bd["nguon"]:
        dich = p if (a.khong_chep and os.path.exists(p)) else chep_nguon(p, md)
        nguon.append(dich)
    khung = bd.get("khung", {})
    if bd.get("lut") or any(c.get("lut") for c in bd.get("chen", [])):
        canh_bao.append("Bang dung co LUT nhung du an CapCut KHONG mang LUT sang - them LUT trong CapCut neu can")
    tr = du.track("video", 0)
    dst = 0
    mat_nguon = {}
    for x in doan:
        f = x["f"]
        m = du.vat_lieu(nguon[f])
        ts = m["_ts"]
        kf = khung[f] if isinstance(khung, list) else khung
        sc, tx, ty = khung_capcut(ts["w"], ts["h"], x["zoom"], kf.get("x", 0.5), kf.get("y", 0.45))
        dai = us(x["e"]) - us(x["s"])
        du.doan_video(tr, m, us(x["s"]), dai, dst, sc, tx, ty, lop=0, am=1.0)
        dst += dai
    tong_us = dst

    # --- video chong 1: B-roll ---
    brolls = [x for x in chen_ds if x["loai"] == "broll"]
    if brolls:
        trb = du.track("video", 2)
        for x in brolls:
            c = x["c"]
            D = x["t1"] - x["t0"]
            src = chen.nguon_broll(d, c)
            tu_g = float(c.get("tu_giay", 0))
            dem = min(2.0, tu_g)                                   # 2 giay du dau de keo them trong CapCut
            dich = os.path.join(md, "broll-{:02d}-{}".format(x["k"], os.path.splitext(os.path.basename(src))[0]) + ".mp4")
            cfg.chay([cfg.ffmpeg(), "-y", "-ss", "{:.3f}".format(tu_g - dem), "-i", src, "-t", "{:.3f}".format(D + dem + 2.0),
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-an", dich], im=True)
            m = du.vat_lieu(dich)
            ts = m["_ts"]
            sc, tx, ty = khung_capcut(ts["w"], ts["h"], float(c.get("zoom", 1.0)), float(c.get("x", 0.5)), float(c.get("y", 0.5)))
            du.doan_video(trb, m, us(dem), min(us(D), m["duration"] - us(dem)), us(x["t0"]), sc, tx, ty, lop=1, am=0.0)

    # --- video chong 2: the chu / danh sach / anh - moi cai mot clip ---
    the_ds = [x for x in chen_ds if x["loai"] in ("the", "danh_sach", "anh")]
    if the_ds:
        trt = du.track("video", 2)
        for x in the_ds:
            D = x["t1"] - x["t0"]
            print("  ve the #{} {} ({:.1f}s, vao {} / ra {})".format(x["k"], x["loai"], D, x["vao"], x["ra"]))
            if dong_co == "hyperframes":
                # MOV trong suot: chuyen canh vao/ra nam san trong clip, A-roll ben duoi lo ra dung luc
                dich = os.path.join(md, "the-{:02d}-{}.mov".format(x["k"], x["loai"]))
                hf.dung_lop(d, [], [dict(x, t0=0.0, t1=D)], D, y_goc, dich, nhap=False)
            else:
                dich = os.path.join(md, "the-{:02d}-{}.mp4".format(x["k"], x["loai"]))
                chen.dung_mot(d, x["c"], D, dich, W, H, False, canh_bao)
                canh_bao.append("The #{}: ve bang ASS nen KHONG co chuyen canh trong CapCut - them tay".format(x["k"]))
            m = du.vat_lieu(dich)
            du.doan_video(trt, m, 0, min(us(D), m["duration"]), us(x["t0"]), 1.0, 0.0, 0.0, lop=2, am=0.0)

    # --- video chong 3: lop phu de dep (MOV trong suot) ---
    lop = os.path.join(md, "phu-de-trong-suot.mov")
    print("  ve lop phu de ({} dong)".format(len(cum_ok)))
    if dong_co == "hyperframes":
        hf.dung_lop(d, cum_ok, [], tong, y_goc, lop, nhap=False)
    else:
        ve = chu.Ve(cfg.MAU["chu_trang"])
        for c in cum_ok:
            if c["tren"] and c["tren"]["loai"] == "anh":
                chu.phu_de(ve, c, int(chu.PY * 0.17), tren_nen_sang=(c["tren"]["nen"] == "trang"))
            else:
                chu.phu_de(ve, c, y_goc)
        p_ass = os.path.join(md, "_phu-de.ass")
        open(p_ass, "w", encoding="utf-8").write(chu.dau_file() + ve.text())
        cfg.chay([cfg.ffmpeg(), "-y", "-f", "lavfi", "-i", "color=c=black@0.0:s={}x{}:r={}:d={:.3f},format=rgba".format(W, H, cfg.FPS, tong),
                  "-vf", "ass='{}':fontsdir='{}':alpha=1".format(p_ass, cfg.FONTS), "-c:v", "prores_ks", "-profile:v", "4444",
                  "-pix_fmt", "yuva444p10le", "-t", "{:.3f}".format(tong), lop], im=True)
    trl = du.track("video", 2)
    m = du.vat_lieu(lop)
    du.doan_video(trl, m, 0, min(tong_us, m["duration"]), 0, 1.0, 0.0, 0.0, lop=3, am=0.0)

    # --- chu CapCut sua duoc, an san ---
    trc = du.track("text", 0)
    y_chu = (H / 2.0 - (y_goc - 70)) / (H / 2.0)
    for c in cum_ok:
        chu_ = (c["nho"] + ("\n" + c["to"] if c["to"] else "")).strip() or c["to"]
        du.doan_chu(trc, chu_, us(c["t0"]), max(1, us(c["t1"]) - us(c["t0"])), y_chu, lop=4, hien=False)

    fd, ten_tm = du.ghi("dv-" + a.ten, tong, thu=getattr(a, "thu", None))
    print("\n=== Du an CapCut: {} ===".format(ten_tm))
    print("Thu muc du an : " + fd)
    print("Media         : " + md)
    print("Track chinh   : {} doan quay (tro ve file goc, keo dai/rut ngan tung vet cat duoc)".format(len(doan)))
    print("Video chong   : {} B-roll · {} the (co chuyen canh vao/ra) · 1 lop phu de trong suot".format(len(brolls), len(the_ds)))
    print("Mau           : giu nguyen nhu luc quay (LUT neu co trong bang dung KHONG mang sang CapCut)")
    if brolls:
        print("Chuyen canh B-roll: CHUA mang sang CapCut (ban dung MP4 thi co) - them tay bang thu vien Chuyen canh cua CapCut")
    print("Chu CapCut    : {} dong - dang AN; muon sua chu thi bat track chu, an lop phu de trong suot".format(len(cum_ok)))
    print("Do dai        : {}".format(cfg.tg(tong_us / US)))
    for x in canh_bao:
        print("!! " + x)
    if getattr(a, "thu", None):
        print("=> CHE DO THU: du an KHONG dang ky vao CapCut, chi de kiem file.")
    else:
        print("=> Mo CapCut, tim du an '{}' o man hinh dau.".format(ten_tm))
