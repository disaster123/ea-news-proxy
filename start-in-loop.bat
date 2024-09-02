@echo off
:: Change to the directory where the .bat file is located
cd /d %~dp0

:START
echo Starting news-proxy.exe...
news-proxy.exe

:: If the executable stops, wait for 5 seconds before restarting
echo news-proxy.exe has stopped. Restarting in 5 seconds...
timeout /t 5 > nul
goto START
