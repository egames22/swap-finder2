@echo off
chcp 65001 > nul
title 수업교체 찾기 서버
cd /d "%~dp0"
echo.
echo  수업교체 찾기 서버 시작 중...
echo  브라우저에서 열기: http://localhost:5000
echo  종료: 이 창을 닫으세요
echo.
python server.py
pause
