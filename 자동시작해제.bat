@echo off
chcp 65001 > nul
title 컴시간 서버 자동시작 해제

set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set DST=%STARTUP%\수업교체찾기_서버.vbs

if exist "%DST%" (
    del "%DST%" > nul 2>&1
    echo 자동 시작이 해제되었습니다.
) else (
    echo 등록된 자동 시작 항목이 없습니다.
)
echo.
pause
