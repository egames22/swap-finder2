@echo off
chcp 65001 > nul
title 수업교체 자동배포 자동시작 해제

set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set DST=%STARTUP%\수업교체찾기_서버.vbs

if exist "%DST%" (
    del "%DST%" > nul 2>&1
    echo  [1] 로그인 자동실행 해제 완료
) else (
    echo  [1] 로그인 자동실행 항목 없음
)

schtasks /delete /tn "수업교체찾기_일과추출" /f > nul 2>&1
schtasks /delete /tn "수업교체찾기_08시" /f > nul 2>&1
schtasks /delete /tn "수업교체찾기_12시" /f > nul 2>&1
schtasks /delete /tn "수업교체찾기_14시" /f > nul 2>&1
schtasks /delete /tn "수업교체찾기_17시" /f > nul 2>&1
echo  [2] 매일 자동실행 해제 완료

echo.
pause
