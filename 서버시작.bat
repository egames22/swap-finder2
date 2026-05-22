@echo off
chcp 65001 > nul
title 수업교체 찾기 — 컴시간 프록시 서버

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo =====================================================
    echo    Python이 설치되어 있지 않습니다.
    echo =====================================================
    echo.
    echo    Python 설치 방법:
    echo    1. https://www.python.org 에 접속
    echo    2. [Downloads] - [Windows] 클릭
    echo    3. 최신 버전 설치 파일 다운로드
    echo    4. 설치 시 "Add Python to PATH" 반드시 체크
    echo    5. 설치 완료 후 이 파일 다시 실행
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 서버를 시작합니다...
python "%~dp0comcigan_proxy.py"
pause
