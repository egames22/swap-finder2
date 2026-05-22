@echo off
chcp 65001 > nul
title 컴시간 서버 자동시작 해제

schtasks /delete /tn "수업교체찾기_컴시간서버" /f > nul 2>&1

if %errorlevel%==0 (
    echo 자동 시작이 해제되었습니다.
) else (
    echo 등록된 자동 시작 항목이 없거나 이미 해제되었습니다.
)
echo.
pause
