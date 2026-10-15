#!/usr/bin/env python3
"""Server tĩnh chỉ để XEM THỬ trang giải thích trước khi publish.

Vì sao phải có file này thay vì `python3 -m http.server`:
trang.html cố tình KHÔNG có <head>/<meta charset> (Artifact tự bọc khi publish),
mà http.server trả `text/html` không kèm charset → trình duyệt đoán Latin-1
→ tiếng Việt vỡ thành "VÃ¬ sao nÃ³i". Trang không sai, chỗ xem sai.
"""
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler


class UTF8Handler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        kieu = super().guess_type(path)
        if kieu.startswith("text/") and "charset=" not in kieu:
            kieu += "; charset=utf-8"
        return kieu


cong = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
goc = sys.argv[2] if len(sys.argv) > 2 else "giai-thich"
HTTPServer(("127.0.0.1", cong), partial(UTF8Handler, directory=goc)).serve_forever()
