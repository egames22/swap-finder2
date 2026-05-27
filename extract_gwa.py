"""
일과서버 .Gwa → 일과시간표.json 변환
- 기본교사시간표.kim (요일별 반복 시간표) + dayhour_t.kim (날짜별 변경)
- 날짜별 변경 있으면 변경 우선, 없으면 기본 시간표 사용
- 출력: 오늘 기준 -30일 ~ +60일 평일 데이터
"""
import zipfile, struct, json
from pathlib import Path
from datetime import date, timedelta, datetime

SEMESTER_START = {
    "2024_1": date(2024, 3, 1),
    "2025_1": date(2025, 3, 1),
    "2026_1": date(2026, 3, 1),
    "2024_2": date(2024, 9, 1),
    "2025_2": date(2025, 9, 1),
    "2026_2": date(2026, 9, 1),
}

def main():
    script_dir = Path(__file__).parent
    server_path = Path(r"C:\Program Files (x86)\일과서버\dat")
    dat_dir = server_path if server_path.exists() else script_dir / "일과서버" / "dat"

    gwa_files = sorted(dat_dir.glob("*.Gwa"))
    if not gwa_files:
        print(f"오류: {dat_dir} 에서 .Gwa 파일을 찾을 수 없습니다.")
        return

    gwa_path = gwa_files[-1]
    print(f"파일: {gwa_path.name}")

    stem = gwa_path.stem
    sem_key = "_".join(stem.split("_")[:2])
    base_date = SEMESTER_START.get(sem_key)
    if not base_date:
        print(f"오류: 알 수 없는 학기 코드 '{sem_key}'")
        return
    print(f"기준일(day 0): {base_date}")

    def _read_entry(zf, korean_name):
        target = korean_name.encode("euc-kr")
        for info in zf.infolist():
            if info.filename.encode("cp437") == target:
                return zf.read(info)
        return None

    def _read_ints(raw):
        n = len(raw) // 4
        return struct.unpack(f"<{n}I", raw[:n * 4])

    with zipfile.ZipFile(gwa_path) as zf:
        # 교사명
        t_raw = _read_entry(zf, "교사명.kim")
        if not t_raw:
            print("오류: 교사명.kim 없음")
            return
        teachers = [t.strip() for t in t_raw.decode("euc-kr", errors="replace").split("^") if t.strip()]
        NT = len(teachers)
        NP = 9

        # 기본교사시간표.kim — 요일별 반복 기준 시간표
        # 구조: teacher × 7day × 9period  (day 0=일, 1=월, ..., 5=금, 6=토)
        base_raw = _read_entry(zf, "기본교사시간표.kim")
        if not base_raw:
            print("오류: 기본교사시간표.kim 없음")
            return
        base_vals = _read_ints(base_raw)

        # dayhour_t.kim — 날짜별 변경 시간표 (변경 있는 날만 기록, 없으면 기본 사용)
        dh_raw = _read_entry(zf, "dayhour_t.kim")
        if not dh_raw:
            print("오류: dayhour_t.kim 없음")
            return
        n_ints = len(dh_raw) // 4
        dh_vals = _read_ints(dh_raw)
        N_DAYS = n_ints // (NT * NP)

    print(f"교사 {NT}명 · {N_DAYS}일 데이터")

    today = date.today()
    window_start = max(today - timedelta(days=30), base_date)
    window_end   = today + timedelta(days=60)

    dates_out = {}
    cur = window_start
    while cur <= window_end:
        if cur.weekday() < 5:
            day_idx = (cur - base_date).days
            if 0 <= day_idx < N_DAYS:
                schedule = []
                # python weekday() 0=월 → file_day 1=월
                file_day = cur.weekday() + 1
                for ti in range(NT):
                    dh_off = day_idx * NT * NP + ti * NP
                    dh_row = dh_vals[dh_off:dh_off + NP]
                    if any(v != 0 for v in dh_row):
                        # 이 날 변경 있음 → 변경 시간표 사용
                        periods = [1 if v != 0 else 0 for v in dh_row]
                    else:
                        # 변경 없음 → 기본 시간표(요일별) 사용
                        # 구조: [teacher][period_1indexed][day] — position 0 unused
                        periods = [0] * NP
                        for p in range(1, NP):  # p=1..8 = 교시1-8
                            slot = ti * 7 * NP + p * 7 + file_day
                            periods[p - 1] = 1 if base_vals[slot] != 0 else 0
                    schedule.append(periods)
                dates_out[cur.isoformat()] = schedule
        cur += timedelta(days=1)

    output = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "teachers": teachers,
        "dates": dates_out,
    }

    out_path = script_dir / "일과시간표.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, separators=(",", ":"))

    print(f"완료: {len(teachers)}명 · {len(dates_out)}일 → {out_path.name}")

if __name__ == "__main__":
    main()
