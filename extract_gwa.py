"""
일과서버 .Gwa 파일 → 일과시간표.json 변환 스크립트
usage: python extract_gwa.py
"""
import zipfile, struct, json, re
from pathlib import Path
from datetime import datetime

DAYS = ["일", "월", "화", "수", "목", "금", "토"]
WEEKDAY_NAMES = ["월", "화", "수", "목", "금"]
WEEKDAY_IDX   = [1,    2,    3,    4,    5]

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

    def _read_entry(zf, korean_name):
        target = korean_name.encode("euc-kr")
        for info in zf.infolist():
            if info.filename.encode("cp437") == target:
                return zf.read(info)
        return None

    def _parse_class_name(cls):
        """학급명 → "N학년 (M)" 형식. 실패하면 None."""
        m = re.match(r'(\d+)[\s\-학년]*(\d+)', cls.strip())
        return f"{m.group(1)}학년 ({m.group(2)})" if m else None

    with zipfile.ZipFile(gwa_path) as zf:
        # 파일 목록 출력 (학급.kim 등 확인용)
        all_names = []
        for info in zf.infolist():
            try:
                decoded = info.filename.encode("cp437").decode("euc-kr", errors="replace")
            except Exception:
                decoded = info.filename
            all_names.append(decoded)
        print(f"zip 파일 목록: {all_names}")

        # 교사명
        teacher_raw = _read_entry(zf, "교사명.kim")
        if not teacher_raw:
            print("오류: 교사명.kim 없음")
            return
        teacher_names = [t.strip() for t in teacher_raw.decode("euc-kr", errors="replace").split("^") if t.strip()]

        # 학급 목록 (있으면 학급 정보 포함)
        class_raw = _read_entry(zf, "학급.kim")
        classes = []
        if class_raw:
            class_text = class_raw.decode("euc-kr", errors="replace")
            classes = [c.strip() for c in class_text.split("^") if c.strip()]
            print(f"학급 {len(classes)}개: {classes[:8]}")
        else:
            print("학급.kim 없음 — 학급 정보 없이 수업 유무만 저장됩니다")

        # 시간표 이진 데이터
        sch_data = _read_entry(zf, "기본교사시간표.kim")
        if not sch_data:
            print("오류: 기본교사시간표.kim 없음")
            return
        n_ints = len(sch_data) // 4
        ints = list(struct.unpack(f"<{n_ints}I", sch_data[:n_ints * 4]))

    print(f"교사 수: {len(teacher_names)}명")

    def val_to_slot(val):
        if val == 0:
            return ""
        if not classes:
            return "수업"
        # 학급 인덱스 후보: 전체 값, 하위 16비트, 하위 8비트 순으로 시도 (인코딩 방식 불명확)
        for candidate in (val, val & 0xFFFF, val & 0xFF):
            if 1 <= candidate <= len(classes):
                name = _parse_class_name(classes[candidate - 1])
                if name:
                    return name
        return "수업"

    teachers = []
    for ti, name in enumerate(teacher_names):
        sch = {}
        for di, day_name in zip(WEEKDAY_IDX, WEEKDAY_NAMES):
            slots = []
            for pi in range(9):
                val = ints[ti * 63 + di * 9 + pi]
                slots.append(val_to_slot(val))
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

if __name__ == "__main__":
    main()
