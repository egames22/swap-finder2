@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo 일과서버 시간표 추출 중...
python extract_gwa.py
if %errorlevel% neq 0 (
    echo 오류: 시간표 추출 실패
    pause
    exit /b 1
)

echo.
echo GitHub에 배포 중...
git add 일과시간표.json
git commit -m "chore: 일과시간표 자동 업데이트"
git push

echo.
echo 배포 완료!
