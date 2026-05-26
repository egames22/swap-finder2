"""
일과서버 .Gwa → 일과시간표.json 변환
- dayhour_t.kim 기준 날짜별 교사 수업 유무 추출
- 출력: 오늘 기준 -30일 ~ +60일 평일 데이터
"""
import zipfile, struct, json
from pathlib import Path
from datetime import date, timedelta, datetime

# 학기별 day 0 기준일 (해당 학기 3월 1일 또는 9월 1일)
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

    stem = gwa_path.stem                        # "2026_1_nsgch"
    sem_key = "_".join(stem.split("_")[:2])    # "2026_1"
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

    with zipfile.ZipFile(gwa_path) as zf:
        # 교사명
        t_raw = _read_entry(zf, "교사명.kim")
        if not t_raw:
            print("오류: 교사명.kim 없음")
            return
        teachers = [t.strip() for t in t_raw.decode("euc-kr", errors="replace").split("^") if t.strip()]

        # 날짜별 시간표 (dayhour_t.kim)
        dh_raw = _read_entry(zf, "dayhour_t.kim")
        if not dh_raw:
            print("오류: dayhour_t.kim 없음")
            return

        N_T = len(teachers)
        N_P = 9
        n_ints = len(dh_raw) // 4
        dh_vals = struct.unpack(f"<{n_ints}I", dh_raw[:n_ints * 4])
        N_DAYS = n_ints // (N_T * N_P)

    print(f"교사 {N_T}명 · {N_DAYS}일 데이터")

    today = date.today()
    window_start = today - timedelta(days=30)
    window_end   = today + timedelta(days=60)
    # 학기 시작일보다 앞으로 가지 않음
    window_start = max(window_start, base_date)

    dates_out = {}
    cur = window_start
    while cur <= window_end:
        if cur.weekday() < 5:          # 평일(월~금)만
            day_idx = (cur - base_date).days
            if 0 <= day_idx < N_DAYS:
                # 각 교사별 9개 교시 수업 유무 (1=수업, 0=빈 시간)
                schedule = []
                base = day_idx * N_T * N_P
                for ti in range(N_T):
                    periods = [1 if dh_vals[base + ti * N_P + pi] != 0 else 0 for pi in range(N_P)]
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
