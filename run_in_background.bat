@echo off
title Starting Farmer Crop Advisory Platform (24/7 Background Mode)
cd /d "%~dp0"

echo ============================================================
echo   Farmer Crop Advisory Platform - 24/7 Background Runner
echo ============================================================
echo.
echo Launching server and Cloudflare Edge Tunnel in the background...
echo (This will continue running even if you close this window or IDE!)
echo.

wscript.exe "%~dp0start_background_247.vbs"

echo Waiting 8 seconds for Cloudflare tunnel to register...
timeout /t 8 /nobreak >nul

if exist "%~dp0LIVE_PUBLIC_URL.txt" (
    type "%~dp0LIVE_PUBLIC_URL.txt"
) else (
    echo Background service is running! Check LIVE_PUBLIC_URL.txt in a few moments for the public link.
)

echo.
echo ============================================================
echo You can now safely CLOSE this window or close Antigravity IDE.
echo The platform will keep running 24/7 in the background!
echo ============================================================
pause
