#!/usr/bin/env bash
# =========================================================================
# Farmer Crop Advisory Platform - Unix/Linux/macOS Local Launcher
# =========================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "========================================================================="
echo "  Farmer Crop Advisory Platform - Local Concurrency Runner"
echo "========================================================================="

# 1. Check Python virtual environment
echo "[1/4] Checking Python Virtual Environment..."
if [ ! -f "backend/.venv/bin/python" ]; then
    echo "[INFO] Creating virtual environment at backend/.venv..."
    python3 -m venv backend/.venv
    backend/.venv/bin/pip install --upgrade pip
    backend/.venv/bin/pip install -r backend/requirements.txt
fi

# 2. Seed database if missing
echo "[2/4] Verifying SQLite Database and Seeds..."
if [ ! -f "backend/database/farmer_advisory.db" ]; then
    echo "Running database seeding..."
    backend/.venv/bin/python backend/database/seed.py
fi

# 3. Check Frontend node_modules
if [ ! -d "frontend/node_modules" ]; then
    echo "[INFO] Installing frontend node_modules..."
    (cd frontend && npm install)
fi

# 4. Trap exit signals to kill background servers on Ctrl+C
cleanup() {
    echo ""
    echo "[SHUTDOWN] Stopping backend and frontend servers..."
    kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 5. Start Flask backend
echo "[3/4] Starting Flask API on http://localhost:5000..."
(cd backend && .venv/bin/python app.py) &
BACKEND_PID=$!

# 6. Start React frontend
echo "[4/4] Starting React Vite Frontend on http://localhost:3000..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!

echo ""
echo "========================================================================="
echo "  SUCCESS! Both services are now running:"
echo "    - Frontend: http://localhost:3000"
echo "    - Backend:  http://localhost:5000"
echo "  Press Ctrl+C to terminate both servers cleanly."
echo "========================================================================="

wait
