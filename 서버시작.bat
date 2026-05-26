@echo off
chcp 65001 > nul
title 수업교체 찾기 -- 컴시간 프록시 서버

set PYTHON_EXE=

if exist "%LOCALAPPDATA%\Python\bin\python.exe"                       set PYTHON_EXE=%LOCALAPPDATA%\Python\bin\python.exe
if not defined PYTHON_EXE if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" set PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python314\python.exe
if not defined PYTHON_EXE if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe
if not defined PYTHON_EXE if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
if not defined PYTHON_EXE if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
if not defined PYTHON_EXE if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe
if not defined PYTHON_EXE if exist "C:\Python314\python.exe"          set PYTHON_EXE=C:\Python314\python.exe
if not defined PYTHON_EXE if exist "C:\Python313\python.exe"          set PYTHON_EXE=C:\Python313\python.exe
if not defined PYTHON_EXE if exist "C:\Python312\python.exe"          set PYTHON_EXE=C:\Python312\python.exe
if not defined PYTHON_EXE if exist "C:\Python311\python.exe"          set PYTHON_EXE=C:\Python311\python.exe

if not defined PYTHON_EXE (
    echo =====================================================
    echo    Python을 찾을 수 없습니다.
    echo =====================================================
    echo.
    echo    python.org 에서 설치 후 다시 실행하세요.
    echo.
    pause
    exit /b 1
)

echo Python: %PYTHON_EXE%
echo 서버를 시작합니다...
"%PYTHON_EXE%" "%~dp0comcigan_proxy.py"
pause
