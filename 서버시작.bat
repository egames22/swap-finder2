@echo off
chcp 65001 > nul
title 수업교체 찾기 — 컴시간 프록시 서버

rem py (파이썬 런처) 먼저 시도
py --version > nul 2>&1
if %errorlevel%==0 (
    echo 서버를 시작합니다...
    py "%~dp0comcigan_proxy.py"
    pause
    exit /b
)

rem python 시도
python --version > nul 2>&1
if %errorlevel%==0 (
    echo 서버를 시작합니다...
    python "%~dp0comcigan_proxy.py"
    pause
    exit /b
)

echo =====================================================
echo    Python을 찾을 수 없습니다.
echo =====================================================
echo.
echo    해결 방법:
echo    1. https://www.python.org/downloads 접속
echo    2. 최신 버전 설치 파일 다운로드
echo    3. 설치 시 첫 화면에서
echo       "Add Python to PATH" 반드시 체크!
echo    4. 설치 완료 후 컴퓨터 재시작
echo    5. 이 파일 다시 실행
echo.
start https://www.python.org/downloads/
pause
exit /b 1
