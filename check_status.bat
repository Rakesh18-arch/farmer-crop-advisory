@echo off
title Farmer Crop Advisory Platform - Service Status
cd /d "%~dp0"

echo ============================================================
echo   Farmer Crop Advisory Platform - Status Check
echo ============================================================
echo.

tasklist /FI "IMAGENAME eq cloudflared.exe" 2>NUL | find /I /N "cloudflared.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [STATUS] Cloudflare Edge Tunnel: RUNNING
) else (
    echo [STATUS] Cloudflare Edge Tunnel: STOPPED
)

tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [STATUS] Python Flask / Unified Server: RUNNING
) else (
    echo [STATUS] Python Flask / Unified Server: STOPPED
)

echo.
if exist "%~dp0LIVE_PUBLIC_URL.txt" (
    echo ----------------- CURRENT LIVE PUBLIC URL -----------------
    type "%~dp0LIVE_PUBLIC_URL.txt"
    echo -----------------------------------------------------------
) else (
    echo No active URL file found. Run 'run_in_background.bat' to start.
)

echo.
pause
