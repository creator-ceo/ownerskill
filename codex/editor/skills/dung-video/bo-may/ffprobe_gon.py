#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ffprobe thu gon - chay bang ffmpeg san co, de HyperFrames qua duoc buoc kiem tra may.

Vi sao co file nay: nhieu may chi co ffmpeg (vd goi pip imageio-ffmpeg), khong co ffprobe; ban ffprobe
tinh ma ffmpeg.org gioi thieu (evermeet.cx) chi co cho chip Intel. HyperFrames doi ffprobe ngay tu buoc
kiem tra, du lop chu cua dung-video khong chua video/am thanh nao.

Ho tro: `-version`, va kieu hoi JSON (`-print_format json`/`-of json` + `-show_streams`/`-show_format`).
Kieu goi khac -> bao loi to (ma 2), KHONG tra so bia. Moi lan goi ghi vao <thu muc du lieu>/.ffprobe-gon.log.
Co ffprobe that (vd cai ffmpeg bang Homebrew) thi dv.py tu dung ban that, bo qua file nay.
"""
import sys, os, re, json, subprocess, datetime

LOG = os.path.join(os.path.expanduser(os.environ.get("CREATOR_VIDEO_HOME") or "~/CreatorVideo"), ".ffprobe-gon.log")


def ffmpeg():
    # dv.py truyen dung ffmpeg no dang dung qua bien moi truong nay khi goi HyperFrames
    for p in (os.environ.get("HYPERFRAMES_FFMPEG_PATH"), os.path.expanduser("~/.local/bin/ffmpeg"),
              "/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if p and os.path.exists(p):
            return p
    import shutil
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def ghi(s):
    try:
        with open(LOG, "a") as f:
            f.write("{} {}\n".format(datetime.datetime.now().isoformat(timespec="seconds"), s))
    except OSError:
        pass


def doc(path):
    r = subprocess.run([ffmpeg(), "-hide_banner", "-i", path], capture_output=True, text=True)
    t = r.stderr
    if "No such file" in t or "Invalid data" in t:
        return None
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", t)
    dai = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else None
    fmt = re.search(r"Input #0, ([^,]+(?:,[^,]+)*?), from", t)
    streams = []
    for i, dong in enumerate(re.findall(r"Stream #0:\d+.*?: (Video|Audio): (.*)", t)):
        loai, chi = dong
        s = {"index": i, "codec_type": loai.lower(), "codec_name": chi.split()[0].strip(",")}
        if loai == "Video":
            kt = re.search(r"(\d{2,5})x(\d{2,5})", chi)
            if kt:
                s["width"], s["height"] = int(kt.group(1)), int(kt.group(2))
            fps = re.search(r"([\d.]+) fps", chi)
            if fps:
                s["r_frame_rate"] = s["avg_frame_rate"] = "{}/1".format(fps.group(1)) if "." not in fps.group(1) else \
                    "{}/1000".format(int(round(float(fps.group(1)) * 1000)))
            pf = re.search(r", (yuv\w+|rgba|rgb24|gray\w*|pal8|ya8)\b", chi)
            if pf:
                s["pix_fmt"] = pf.group(1)
        else:
            sr = re.search(r"(\d+) Hz", chi)
            if sr:
                s["sample_rate"] = sr.group(1)
            s["channels"] = 1 if "mono" in chi else 2
        if dai is not None:
            s["duration"] = "{:.6f}".format(dai)
        streams.append(s)
    return {"streams": streams,
            "format": {"filename": path, "format_name": fmt.group(1) if fmt else "", "nb_streams": len(streams),
                       **({"duration": "{:.6f}".format(dai)} if dai is not None else {})}}


def main(a):
    ghi(" ".join(a))
    if "-version" in a or "--version" in a:
        v = subprocess.run([ffmpeg(), "-version"], capture_output=True, text=True).stdout.splitlines()
        print((v[0] if v else "ffmpeg version ?").replace("ffmpeg version", "ffprobe version") + " (ffprobe_gon.py)")
        return 0
    json_ra = ("json" in a) and ("-print_format" in a or "-of" in a or "-output_format" in a)
    if not json_ra or not ({"-show_streams", "-show_format"} & set(a)):
        sys.stderr.write("ffprobe_gon: kieu goi chua ho tro: {}\n".format(" ".join(a)))
        ghi("  -> CHUA HO TRO")
        return 2
    file = next((x for x in reversed(a) if not x.startswith("-") and os.path.exists(x)), None)
    if not file:
        sys.stderr.write("ffprobe_gon: khong thay file trong lenh\n")
        return 1
    d = doc(file)
    if d is None:
        sys.stderr.write("{}: Invalid data found when processing input\n".format(file))
        return 1
    ra = {}
    if "-show_streams" in a:
        ra["streams"] = d["streams"]
    if "-show_format" in a:
        ra["format"] = d["format"]
    print(json.dumps(ra, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
