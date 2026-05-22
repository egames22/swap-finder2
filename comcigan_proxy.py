#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
수업교체 찾기 — 컴시간 로컬 프록시 서버
Python 표준 라이브러리만 사용 (별도 설치 불필요)
"""

import json, re, socket, sys, urllib.parse, urllib.request
from base64 import b64encode
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 3001
COMCI = "http://222.106.100.23:4082"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
_ctx = {}

def fetch(url, enc="utf-8"):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read().decode(enc, errors="replace")

def init():
    global _ctx
    html = fetch(f"{COMCI}/st", enc="euc-kr")
    scripts = re.findall(r"<script[^>]*>([\s\S]*?)</script>", html, re.IGNORECASE)
    script = next((s for s in scripts if "일일자료" in s), "")
    if not script:
        raise RuntimeError("컴시간 응답 파싱 실패 — 서버 구조가 변경되었을 수 있습니다")

    def ri(pat):
        m = re.search(pat, script)
        return int("".join(c for c in m.group(0) if c.isdigit())) if m else None

    route_m = re.search(r"\./\d+\?\d+l", script)
    prefix_m = re.search(r"'(\d+_)'", script)
    if not route_m or not prefix_m:
        raise RuntimeError("라우트/프리픽스 정보를 찾을 수 없습니다")

    route = route_m.group(0)
    baseurl = f"{COMCI}{route[1:8]}"
    _ctx.update({
        "prefix":    prefix_m.group(1),
        "daynum":    ri(r"일일자료=Q자료\(자료\.자료(\d+)"),
        "thnum":     ri(r"성명=자료\.자료(\d+)"),
        "sbnum":     ri(r"자료\.자료(\d+)\[sb\]"),
        "baseurl":   baseurl,
        "searchurl": f"{baseurl}{route[8:]}",
    })

def search_school(q):
    enc = urllib.parse.quote(q.encode("euc-kr"))
    data = json.loads(fetch(_ctx["searchurl"] + enc).replace("\0", ""))
    return [{"region": s[1], "name": s[2], "code": s[3]}
            for s in data.get("학교검색", [])]

def get_teacher_schedule(sccode):
    b64 = b64encode(f"{_ctx['prefix']}{sccode}_0_1".encode()).decode()
    raw = json.loads(fetch(f"{_ctx['baseurl']}?{b64}").replace("\0", ""))

    sbnum = _ctx["sbnum"]
    thnum = _ctx["thnum"]
    daynum = _ctx["daynum"]
    subjects = raw.get(f"자료{sbnum}", [])
    teachers = raw.get(f"자료{thnum}", [])
    days_raw = raw.get(f"자료{daynum}", [])

    def px(n):
        s = str(n)
        return int(s[:2]) if len(s) == 5 else int(s[:1])

    def trim(lst):
        lst = list(lst)
        while lst and not lst[-1]:
            lst.pop()
        return lst

    schedule = {}
    for gi, grade in enumerate(days_raw[1:]):
        for ci, cls in enumerate(grade):
            for di, day in enumerate(cls[1:6]):
                for pi, x in enumerate(trim(day[1:])):
                    if not x:
                        continue
                    si = px(x)
                    ti = int(str(x)[-2:])
                    tname = teachers[ti] if ti < len(teachers) else ""
                    if not tname:
                        continue
                    subj = subjects[si] if si < len(subjects) else ""
                    schedule.setdefault(tname, {}).setdefault(str(di), {})[str(pi + 1)] = {
                        "subject": subj,
                        "grade": gi + 1,
                        "cls": ci + 1,
                    }
    return schedule

def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        p = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(p.query)
        try:
            if p.path == "/ping":
                self._ok({"ok": True})
            elif p.path == "/search":
                self._ok(search_school(q.get("q", [""])[0]))
            elif p.path == "/teacher-schedule":
                code = int(q.get("code", ["0"])[0])
                self._ok(get_teacher_schedule(code))
            else:
                self.send_response(404)
                self._cors()
                self.end_headers()
        except Exception as e:
            self._ok({"error": str(e)}, 500)

    def _ok(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass

if __name__ == "__main__":
    print("=" * 54)
    print("    수업교체 찾기 — 컴시간 프록시 서버")
    print("=" * 54)
    print("컴시간 서버 연결 중...", end=" ", flush=True)
    try:
        init()
        ip = local_ip()
        print("성공!\n")
        print(f"  이 PC에서 접속:   http://localhost:{PORT}")
        print(f"  다른 PC에서 접속: http://{ip}:{PORT}")
        print("\n  이 창을 열어두세요. 닫으면 서버가 종료됩니다.")
        print("  종료: Ctrl+C\n")
        HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료했습니다.")
    except Exception as e:
        print(f"실패\n\n오류: {e}")
        input("\nEnter를 눌러 종료하세요...")
        sys.exit(1)
