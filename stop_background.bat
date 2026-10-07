@echo off
title Stop Farmer Crop Advisory Background Services
cd /d "%~dp0"

echo Stopping Cloudflare tunnel and Python services...
taskkill /F /IM cloudflared.exe 2>NUL
taskkill /F /IM python.exe 2>NUL

echo Services stopped.
pause
