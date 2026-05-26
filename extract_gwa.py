"""
일과서버 .Gwa 파일 → 일과시간표.json 변환 스크립트
usage: python extract_gwa.py
"""
import zipfile, struct, json, glob
from pathlib import Path
from datetime import datetime

DAYS = ["일", "월", "화", "수", "목", "금", "토"]
WEEKDAY_NAMES = ["월", "화", "수", "목", "금"]
WEEKDAY_IDX   = [1,    2,    3,    4,    5]

def main():
    script_dir = Path(__file__).parent
    # 서버 PC 설치 경로 우선, 없으면 스크립트 옆 폴더
    server_path = Path(r"C:\Program Files (x86)\일과서버\dat")
    dat_dir = server_path if server_path.exists() else script_dir / "일과서버" / "dat"

    gwa_files = sorted(dat_dir.glob("*.Gwa"))
    if not gwa_files:
        print(f"오류: {dat_dir} 에서 .Gwa 파일을 찾을 수 없습니다.")
        return

    gwa_path = gwa_files[-1]
    print(f"파일: {gwa_path.name}")

    def _read_entry(zf, korean_name):
        """cp437-encoded EUC-KR 파일명으로 저장된 항목을 읽기"""
        target = korean_name.encode("euc-kr")
        for info in zf.infolist():
            if info.filename.encode("cp437") == target:
                return zf.read(info)
        raise KeyError(f"{korean_name} 항목을 찾을 수 없음")

    with zipfile.ZipFile(gwa_path) as zf:
        # 교사명 읽기
        teacher_raw = _read_entry(zf, "교사명.kim").decode("euc-kr", errors="replace")
        teacher_names = [t.strip() for t in teacher_raw.split("^") if t.strip()]

        # 시간표 읽기 (little-endian int32 배열)
        sch_data = _read_entry(zf, "기본교사시간표.kim")
        n_ints = len(sch_data) // 4
        ints = list(struct.unpack(f"<{n_ints}I", sch_data[:n_ints * 4]))

    print(f"교사 수: {len(teacher_names)}명")

    teachers = []
    for ti, name in enumerate(teacher_names):
        sch = {}
        for di, day_name in zip(WEEKDAY_IDX, WEEKDAY_NAMES):
            slots = []
            for pi in range(9):
                val = ints[ti * 63 + di * 9 + pi]
                slots.append("수업" if val != 0 else "")
            sch[day_name] = slots
        teachers.append({"name": name, "dname": name, "schedule": sch})

    output = {
        "school": "논산여자상업고등학교",
        "source": gwa_path.name,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "teachers": teachers
    }

    out_path = script_dir / "일과시간표.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"완료: {len(teachers)}명 → {out_path.name}")
    print("이제 관리자 패널에서 '일과시간표.json 불러오기'를 사용하세요.")

if __name__ == "__main__":
    main()
