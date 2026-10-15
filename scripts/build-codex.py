#!/usr/bin/env python3
"""Sinh bản Codex từ bản Claude Code.

Chạy:  python3 scripts/build-codex.py
Đọc 8 gói vai ở gốc repo, ghi ra codex/<gói>/ và .agents/plugins/marketplace.json.
Bản Codex khác bản gốc ở: lệnh gọi skill dùng $ thay vì /, lệnh cài dùng codex,
bỏ chỗ nhắc riêng Claude Code. KHÔNG sửa tay thư mục codex/, sửa ở gói gốc rồi chạy lại.
"""
import json, os, re, shutil, glob, sys
GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(GOC)
ROLES = ["thu-thu","nghien-cuu","tong-giam-doc","content","editor","ban-hang","cham-soc","phat-trien-san-pham"]
SKILLS = sorted({os.path.basename(d) for r in ROLES for d in glob.glob(f"{r}/skills/*")})
# tên dài trước để regex không cắt cụt (viet-content trước viet)
SK_RE = "|".join(re.escape(s) for s in sorted(SKILLS, key=len, reverse=True))

def chuyen(t):
    # 1. lệnh cài gói
    t = t.replace("`claude plugin install <tên gói>@ownerskill`", "gói cần cài (trong Codex gõ `/plugins`, chọn kho ownerskill)")
    t = re.sub(r"`claude plugin install ([a-z-]+)@ownerskill`", r"gói `\1` (trong Codex gõ `/plugins`, chọn kho ownerskill, cài gói đó)", t)
    t = re.sub(r"claude plugin install ([a-z-]+)@ownerskill", r"cài gói \1 (trong Codex gõ /plugins)", t)
    t = t.replace("claude plugin marketplace add creator-ceo/ownerskill", "codex plugin marketplace add creator-ceo/ownerskill")
    # 2. lệnh gọi skill: /ten -> $ten (chỉ tên skill của bộ, không đụng đường dẫn)
    t = re.sub(r"(?<![\w/.\-$])/(" + SK_RE + r")(?![\w\-])", r"$\1", t)
    # 3. chỗ riêng Claude Code
    t = t.replace('cp -R "$CLAUDE_PLUGIN_ROOT/skills/soi-ads/bo-may" ./ads', 'cp -R "<thư mục chứa SKILL.md của soi-ads>/bo-may" ./ads')
    t = t.replace("nằm trong thư mục cache của Claude Code", "nằm trong thư mục cài đặt của Codex")
    t = t.replace("công cụ tạo nhiệm vụ theo lịch của Claude Code", "tính năng chạy theo lịch của Codex (automations) nếu bản bạn dùng có")
    t = t.replace("`~/.claude/scheduled-tasks/`", "phần cài đặt chạy theo lịch của Codex")
    t = t.replace("~/.claude/skills/", "~/.agents/skills/").replace("~/.claude/skills", "~/.agents/skills")
    t = t.replace("node .claude/skills/anh-quote/dung.mjs", "node <thư mục skill anh-quote>/dung.mjs")
    t = t.replace("bo-may/CLAUDE.md", "bo-may/AGENTS.md")
    t = t.replace("Cấu hình đã có sẵn trong `.claude/launch.json`, chạy `xem.py` nằm cùng thư mục skill này.", "Chạy `python3 xem.py` nằm cùng thư mục skill này.")
    t = t.replace("WebSearch/WebFetch", "công cụ tìm kiếm và đọc trang web").replace("WebSearch", "công cụ tìm kiếm web").replace("WebFetch", "công cụ đọc trang web")
    t = t.replace("Claude Code", "Codex").replace("CLAUDE.md", "AGENTS.md")
    t = re.sub(r"\bClaude\b", "Codex", t)
    return t

for r in ROLES:
    dst = f"codex/{r}"
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(f"{r}/skills", f"{dst}/skills", ignore=shutil.ignore_patterns("__pycache__", "node_modules", ".DS_Store"))
    for f in glob.glob(f"{dst}/**/*", recursive=True):
        if os.path.isfile(f) and f.endswith((".md", ".json", ".mjs", ".py", ".html", ".txt")):
            try: s = open(f, encoding="utf-8").read()
            except UnicodeDecodeError: continue
            # chỉ chuyển văn bản tài liệu; mã chạy (.mjs .py) chỉ đổi chú thích nhắc Claude
            t = chuyen(s) if f.endswith(".md") else s.replace("~/.claude/skills", "~/.agents/skills")
            if t != s: open(f, "w", encoding="utf-8").write(t)
    # CLAUDE.md của soi-ads/bo-may -> AGENTS.md để Codex đọc
    for c in glob.glob(f"{dst}/**/CLAUDE.md", recursive=True):
        os.replace(c, os.path.join(os.path.dirname(c), "AGENTS.md"))
    meta = json.load(open(f"{r}/.claude-plugin/plugin.json", encoding="utf-8"))
    plug = {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "name": r,
            "version": meta["version"], "description": chuyen(meta["description"]),
            "author": meta["author"], "license": "MIT",
            "repository": "https://github.com/creator-ceo/ownerskill", "keywords": meta.get("keywords", [])}
    json.dump(plug, open(f"{dst}/plugin.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(f"{dst}/plugin.json", "a").write("\n")

# gói tong-hop dùng nguyên bản gốc (tiếng Anh, không nhắc lệnh riêng): thêm plugin.json ở gốc gói
mh = json.load(open(".claude-plugin/marketplace.json", encoding="utf-8"))
th = [p for p in mh["plugins"] if p["name"] == "tong-hop"][0]
json.dump({"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "name": "tong-hop", "version": "1.0.0",
           "description": th["description"], "license": "MIT", "repository": "https://github.com/creator-ceo/ownerskill"},
          open("tong-hop/plugin.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open("tong-hop/plugin.json", "a").write("\n")

os.makedirs(".agents/plugins", exist_ok=True)
plugins = []
for r in ROLES:
    mo_ta = json.load(open(f"codex/{r}/plugin.json", encoding="utf-8"))["description"]
    plugins.append({"name": r, "source": {"source": "local", "path": f"./codex/{r}"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Productivity"})
plugins.append({"name": "tong-hop", "source": {"source": "local", "path": "./tong-hop"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Productivity"})
json.dump({"name": "ownerskill", "interface": {"displayName": "Ownerskill"}, "plugins": plugins},
          open(".agents/plugins/marketplace.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(".agents/plugins/marketplace.json", "a").write("\n")
print("Đã sinh", len(ROLES), "gói Codex vào codex/ và .agents/plugins/marketplace.json")
