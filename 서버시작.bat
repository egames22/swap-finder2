@echo off
chcp 65001 > nul
title 수업교체 찾기 — 컴시간 프록시 서버

set PYTHON_EXE=

rem 1단계: py 런처
where /q py 2>nul
if %errorlevel%==0 set PYTHON_EXE=py

rem 2단계: python 명령
if not defined PYTHON_EXE (
    where /q python 2>nul
    if %errorlevel%==0 set PYTHON_EXE=python
)

rem 3단계: 사용자 설치 경로 탐색 (일반적인 설치 위치)
if not defined PYTHON_EXE (
    for /d %%d in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
        if exist "%%d\python.exe" set PYTHON_EXE="%%d\python.exe"
    )
)

rem 4단계: C드라이브 루트 탐색
if not defined PYTHON_EXE (
    for /d %%d in ("C:\Python3*") do (
        if exist "%%d\python.exe" set PYTHON_EXE="%%d\python.exe"
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
