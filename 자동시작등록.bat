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

:: 2) 매일 오전 7시 자동 실행 (작업 스케줄러)
schtasks /create /tn "수업교체찾기_일과추출" /tr "\"%BAT%\"" /sc daily /st 07:00 /f > nul 2>&1

if %errorlevel% equ 0 (
    echo  [2] 매일 오전 7시 자동실행 등록 완료
) else (
    echo  [2] 매일 자동실행 등록 실패 — 관리자 권한으로 다시 실행하세요.
)

echo.
echo  설정 완료! 지금 바로 배포하려면 자동배포.bat 을 실행하세요.
echo.
pause
