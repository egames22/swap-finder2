// 수업교체 찾기 — Cloudflare Worker
// comci.net CORS 프록시

const SCHOOL_CODE = '87163';
const SC = '73629_';

// comci.net 자료446 순서와 동일한 교사 실명 목록 (37·38번은 자율/창체 가상 항목)
const TEACHER_NAMES = [
  '김미나', '김현수', '구본경', '허기석', '유성원',
  '이승종', '김철민', '정복순', '오민섭', '신송화',
  '서원익', '정은경', '김민호', '장동욱', '김자운',
  '고정연', '신동관', '유현주', '정유리', '장진영',
  '박미수', '채정희', '유선숙', '신동숙', '장천우',
  '송수민', '박경숙', '안예진', '정일화', '황인아',
  '박지수', '김진숙', '정진희', '김도경', '김혜민',
  '박미애', '자율', '창체',
];

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
};

function isBusy(val) {
  if (val === 0 || val === null || val === undefined || val === '') return false;
  if (typeof val === 'string') {
    const v = val.startsWith('>') ? val.slice(1) : val;
    return v !== '' && v !== '0';
  }
  return val !== 0;
}

async function fetchComci(r) {
  const plain = `${SC}${SCHOOL_CODE}_0_${r}`;
  const b64 = btoa(plain);
  const resp = await fetch(`http://comci.net:4082/36179_T?${b64}`, {
    headers: { 'User-Agent': 'Mozilla/5.0' },
  });
  const text = await resp.text();
  const last = text.lastIndexOf('}');
  return JSON.parse(text.slice(0, last + 1));
}

function buildDates(data) {
  const start = new Date(data['시작일']);
  const t542 = data['자료542'];
  const NT = data['교사수'];
  const out = {};

  for (let weekday = 1; weekday <= 5; weekday++) {
    const dt = new Date(start);
    dt.setDate(dt.getDate() + weekday - 1);
    const dateStr = dt.toISOString().slice(0, 10);

    const rows = [];
    for (let ti = 1; ti <= NT; ti++) {
      const row = new Array(8).fill(0);
      try {
        const dayArr = t542[ti][weekday];
        for (let p = 1; p < dayArr.length && p <= 8; p++) {
          const v = dayArr[p];
          if (!isBusy(v)) continue;
          const rawStr = String(typeof v === 'string' && v.startsWith('>') ? v.slice(1) : v);
          const num = parseInt(rawStr);
          if (!isNaN(num) && num > 0) {
            const cc = num % 1000;
            const g = Math.floor(cc / 100);
            const b = cc % 100;
            row[p - 1] = (g > 0 && b > 0) ? { g: String(g), b: String(b) } : 1;
          } else {
            row[p - 1] = 1;
          }
        }
      } catch (_) {}
      rows.push(row);
    }
    out[dateStr] = rows;
  }
  return out;
}

export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS });
    }

    const { pathname } = new URL(request.url);

    if (pathname !== '/api/schedule') {
      return new Response('Not Found', { status: 404 });
    }

    try {
      let generated = '';
      let allDates = {};

      for (const r of [1, 2]) {
        const data = await fetchComci(r);
        if (!generated) generated = data['자료244'] || '';
        Object.assign(allDates, buildDates(data));
      }

      return new Response(
        JSON.stringify({ generated, teachers: TEACHER_NAMES, dates: allDates }),
        {
          headers: {
            ...CORS,
            'Content-Type': 'application/json; charset=utf-8',
            'Cache-Control': 'max-age=300',
          },
        }
      );
    } catch (e) {
      return new Response(e.message, {
        status: 500,
        headers: CORS,
      });
    }
  },
};
