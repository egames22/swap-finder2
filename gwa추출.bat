@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 일과서버 시간표 추출 중...
python extract_gwa.py
echo.
pause
