@echo off
chcp 65001 > nul
title 컴시간 서버 자동시작 등록

echo =====================================================
echo   컴시간 서버 자동시작 등록
echo =====================================================
echo.
echo 컴퓨터에 로그인할 때마다 서버가 자동으로 시작됩니다.
echo (창 없이 백그라운드에서 조용히 실행)
echo.

set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set DST=%STARTUP%\수업교체찾기_서버.vbs

copy "%~dp0서버백그라운드.vbs" "%DST%" > nul 2>&1

if exist "%DST%" (
    echo  완료! 다음 로그인부터 서버가 자동으로 시작됩니다.
    echo.
    echo  지금 바로 서버를 시작하려면 서버시작.bat 을 실행하세요.
) else (
    echo  복사에 실패했습니다. 관리자에게 문의하세요.
)
echo.
pause
