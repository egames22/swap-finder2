@echo off
chcp 65001 > nul
title 컴시간 서버 자동시작 등록

echo =====================================================
echo   컴시간 서버 자동시작 등록
echo =====================================================
echo.
echo 컴퓨터를 켤 때마다 서버가 자동으로 시작되도록 설정합니다.
echo (창 없이 백그라운드에서 조용히 실행됩니다)
echo.

set VBS_PATH=%~dp0서버백그라운드.vbs

schtasks /create /tn "수업교체찾기_컴시간서버" /tr "wscript.exe \"%VBS_PATH%\"" /sc onlogon /ru "%USERNAME%" /f > nul 2>&1

if %errorlevel%==0 (
    echo  완료! 앞으로 컴퓨터를 켤 때마다 서버가 자동으로 시작됩니다.
    echo.
    echo  지금 바로 서버를 시작하려면 서버시작.bat 을 실행하세요.
) else (
    echo  실패했습니다.
    echo  이 파일을 마우스 우클릭 - [관리자 권한으로 실행] 해보세요.
)
echo.
pause
