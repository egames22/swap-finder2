@echo off
chcp 65001 > nul
title 수업교체 자동배포 자동시작 등록

echo =====================================================
echo   수업교체 자동배포 자동시작 등록
echo =====================================================
echo.

set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set DST=%STARTUP%\수업교체찾기_서버.vbs
set BAT=%~dp0자동배포.bat

:: 1) 로그인 시 1회 실행 (VBS → 시작프로그램)
(
  echo Dim WshShell
  echo Set WshShell = CreateObject^("WScript.Shell"^)
  echo WshShell.Run """"%BAT%"""", 0, False
) > "%DST%"

if exist "%DST%" (
    echo  [1] 로그인 자동실행 등록 완료
) else (
    echo  [1] 로그인 자동실행 등록 실패 — 관리자 권한으로 다시 실행하세요.
    pause
    exit /b 1
)

:: 2) 매일 4회 자동 실행 (작업 스케줄러)
set OK=1
schtasks /create /tn "수업교체찾기_08시" /tr "\"%BAT%\"" /sc daily /st 08:00 /f > nul 2>&1
if %errorlevel% neq 0 set OK=0
schtasks /create /tn "수업교체찾기_12시" /tr "\"%BAT%\"" /sc daily /st 12:00 /f > nul 2>&1
if %errorlevel% neq 0 set OK=0
schtasks /create /tn "수업교체찾기_14시" /tr "\"%BAT%\"" /sc daily /st 14:00 /f > nul 2>&1
if %errorlevel% neq 0 set OK=0
schtasks /create /tn "수업교체찾기_17시" /tr "\"%BAT%\"" /sc daily /st 17:00 /f > nul 2>&1
if %errorlevel% neq 0 set OK=0

if %OK% equ 1 (
    echo  [2] 매일 08:00 / 12:00 / 14:00 / 17:00 자동실행 등록 완료
) else (
    echo  [2] 일부 등록 실패 — 관리자 권한으로 다시 실행하세요.
)

echo.
echo  설정 완료! 지금 바로 배포하려면 자동배포.bat 을 실행하세요.
echo.
pause
