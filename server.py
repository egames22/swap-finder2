"""
수업교체 찾기 서버
- comci.net API 프록시 (CORS 우회)
- index.html 정적 서빙
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request, base64, json, os, mimetypes
from datetime import date, timedelta

PORT = 5000
SCHOOL_CODE = '87163'
SC = '73629_'

# comci.net 자료446 인덱스(1부터) → 교사 실명 매핑
# 인덱스 순서는 comci.net에서 반환하는 자료446 배열 순서와 동일
TEACHER_NAMES = [
    '',       # 0: 미사용
    '김미나',  # 1
    '김현수',  # 2
    '구본경',  # 3
    '허기석',  # 4
    '유성원',  # 5
    '이승종',  # 6
    '김철민',  # 7
    '정복순',  # 8
    '오민섭',  # 9
    '신송화',  # 10
    '서원익',  # 11
    '정은경',  # 12
    '김민호',  # 13
    '장동욱',  # 14
    '김자운',  # 15
    '고정연',  # 16
    '신동관',  # 17
    '유현주',  # 18
    '정유리',  # 19
    '장진영',  # 20
    '박미수',  # 21
    '채정희',  # 22
    '유선숙',  # 23
    '신동숙',  # 24
    '장천우',  # 25
    '송수민',  # 26
    '박경숙',  # 27
    '안예진',  # 28
    '정일화',  # 29
    '황인아',  # 30
    '박지수',  # 31
    '김예인',  # 32
    '김도경',  # 33
    '곽명희',  # 34
    '김혜민',  # 35
    '박미애',  # 36
]


def fetch_comci(r):
    plain = f'{SC}{SCHOOL_CODE}_0_{r}'
    b64 = base64.b64encode(plain.encode()).decode()
    url = f'http://comci.net:4082/36179_T?{b64}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read()
    text = raw.decode('utf-8')
    last = text.rfind('}')
    return json.loads(text[:last + 1])


def is_busy(val):
    if val == 0 or val == '' or val is None:
        return False
    if isinstance(val, str):
        return val.lstrip('>') != '0' and val.lstrip('>') != ''
    return val != 0


def build_dates(data):
    NT = data['교사수']
    start = date.fromisoformat(data['시작일'])
    t542 = data['자료542']

    result = {}
    for weekday in range(1, 6):
        dt = start + timedelta(days=weekday - 1)
        date_str = dt.isoformat()
        teachers_periods = []
        for ti in range(1, NT + 1):
            row = [0] * 8
            try:
                day_arr = t542[ti][weekday]
                for p in range(1, 9):
                    if p < len(day_arr) and is_busy(day_arr[p]):
                        row[p - 1] = 1
            except (IndexError, TypeError, KeyError):
                pass
            teachers_periods.append(row)
        result[date_str] = teachers_periods
    return result


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        path = self.path.split('?')[0]

        if path == '/api/schedule':
            self._handle_schedule()
        else:
            self._serve_static(path)

    def _handle_schedule(self):
        try:
            all_dates = {}
            generated = ''
            for r in [1, 2]:
                data = fetch_comci(r)
                if not generated:
                    generated = data.get('자료244', '')
                all_dates.update(build_dates(data))

            result = {
                'generated': generated,
                'teachers': TEACHER_NAMES[1:],
                'dates': all_dates,
            }
            body = json.dumps(result, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            msg = str(e).encode('utf-8')
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(msg)

    def _serve_static(self, path):
        if path == '/':
            path = '/index.html'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path.lstrip('/'))
        if os.path.isfile(file_path):
            mime = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            with open(file_path, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    server = HTTPServer(('', PORT), Handler)
    print(f'수업교체 찾기 서버: http://localhost:{PORT}')
    print('종료하려면 Ctrl+C')
    server.serve_forever()
