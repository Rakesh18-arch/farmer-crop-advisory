@echo off
TITLE Farmer Crop Advisory Platform - Local Development Runner
echo =========================================================================
echo   Farmer Crop Advisory Platform - 1-Click Local Runner
echo =========================================================================
echo.

:: 1. Check Python installation & Virtual Environment
echo [1/4] Checking Python Virtual Environment...
IF NOT EXIST "backend\.venv\Scripts\python.exe" (
    echo [SETUP] Virtual environment not found. Bootstrapping backend\.venv...
    python -m venv backend\.venv
    backend\.venv\Scripts\python.exe -m pip install --upgrade pip
    backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
) ELSE (
    echo [OK] Backend virtual environment verified.
)

:: 2. Ensure Database is seeded
echo [2/4] Verifying SQLite Database and Agronomic Seeds...
IF NOT EXIST "backend\database\farmer_advisory.db" (
    echo [SETUP] Database not found. Running master seed script...
    backend\.venv\Scripts\python.exe backend\database\seed.py
) ELSE (
    echo [OK] Agronomic database verified.
)

:: 3. Check Frontend node_modules
IF NOT EXIST "frontend\node_modules" (
    echo [SETUP] Frontend node_modules not found. Running npm install...
    cd frontend && call npm install && cd ..
)

:: 4. Launch Flask Backend in a new terminal window
echo [3/4] Launching Flask Backend on http://localhost:5000...
start "Agri-Advisory Backend (Port 5000)" cmd /k "cd backend && .venv\Scripts\python.exe app.py"

:: 5. Launch Vite Frontend in a new terminal window
echo [4/4] Launching Vite React Frontend on http://localhost:3000...
start "Agri-Advisory Frontend (Port 3000)" cmd /k "cd frontend && npm run dev"


echo.
echo =========================================================================
echo   SUCCESS! Both services are now running concurrently:
echo     - Frontend Web App:  http://localhost:3000
echo     - Backend REST API:  http://localhost:5000
echo     - Health Check:      http://localhost:5000/api/health
echo.
echo   Demo Credentials:
echo     - Farmer: farmer@demo.org / Farmer@123
echo     - Admin:  admin@farmeradvisory.org / Admin@123
echo =========================================================================
pause
