@echo off
chcp 65001 > nul
title 수업교체 찾기 — 컴시간 프록시 서버

set PYTHON_EXE=

rem 1단계: 알려진 경로 직접 확인
if exist "%LOCALAPPDATA%\Python\bin\python.exe" set PYTHON_EXE="%LOCALAPPDATA%\Python\bin\python.exe"

rem 2단계: 표준 설치 경로 탐색
if not defined PYTHON_EXE (
    for /d %%d in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
        if exist "%%d\python.exe" set PYTHON_EXE="%%d\python.exe"
    )
)

rem 3단계: C드라이브 루트 탐색
if not defined PYTHON_EXE (
    for /d %%d in ("C:\Python3*") do (
        if exist "%%d\python.exe" set PYTHON_EXE="%%d\python.exe"
    )
)

rem 4단계: PATH 탐색 — WindowsApps(가짜) 제외
if not defined PYTHON_EXE (
    for /f "delims=" %%p in ('where python 2^>nul ^| findstr /v /i "WindowsApps"') do (
        if not defined PYTHON_EXE set PYTHON_EXE="%%p"
    )
)

if not defined PYTHON_EXE (
    echo =====================================================
    echo    Python을 찾을 수 없습니다.
    echo =====================================================
    echo.
    echo    해결 방법:
    echo    1. https://www.python.org/downloads 접속
    echo    2. 최신 버전 설치 파일 다운로드
    echo    3. 설치 첫 화면에서
    echo       "Add Python to PATH" 반드시 체크!
    echo    4. 설치 완료 후 컴퓨터 재시작
    echo    5. 이 파일 다시 실행
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python: %PYTHON_EXE%
echo 서버를 시작합니다...
%PYTHON_EXE% "%~dp0comcigan_proxy.py"
pause
