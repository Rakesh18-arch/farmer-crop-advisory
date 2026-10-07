@echo off
title Push Farmer Crop Advisory Platform to GitHub
cd /d "%~dp0"

echo ============================================================
echo   Pushing Farmer Crop Advisory Platform to GitHub
echo ============================================================
echo.

set GIT_EXE=C:\Users\Rakesh\.gemini\antigravity-ide\scratch\mingit\cmd\git.exe
set GH_EXE=C:\Users\Rakesh\.gemini\antigravity-ide\scratch\gh\bin\gh.exe

"%GIT_EXE%" status

echo.
echo Pushing branch 'main' to https://github.com/Rakesh18-arch/farmer-crop-advisory.git ...
echo.

"%GIT_EXE%" push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================
    echo [NOTE] Repository needs to be created on GitHub:
    echo 1. Open: https://github.com/new
    echo 2. Repository name: farmer-crop-advisory
    echo 3. Set to "Public" and click "Create repository"
    echo 4. Double-click this script again to push immediately!
    echo ============================================================
) else (
    echo.
    echo [SUCCESS] Code successfully pushed to GitHub!
    echo Visit: https://github.com/Rakesh18-arch/farmer-crop-advisory
)

echo.
pause
