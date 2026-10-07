# 🌱 Farmer Crop Advisory Platform
### AI-Based Smart Decision Support System for Farmers

A full-stack, enterprise-grade agricultural decision support platform built with **Flask**, **React.js**, **SQLAlchemy**, and **Scikit-learn/TensorFlow**. Designed to empower farmers with personalized, data-driven insights on crop selection, balanced fertilizer nutrition, weather-smart irrigation, plant disease diagnosis, and mandi market intelligence.

---

## 📌 Architecture Overview

```text
farmer-crop-advisory/
├── backend/
│   ├── app.py                      # Application Factory & Blueprint Registry
│   ├── config.py                   # Central Configuration (SQLite/PostgreSQL, JWT, Demo Mode)
│   ├── requirements.txt            # Python Dependencies
│   ├── .env.example                # Environment Variable Template
│   ├── database/
│   │   ├── db.py                   # SQLAlchemy Instance & init_db
│   │   └── seed.py                 # Comprehensive Master Seeder (Admin, Farmer, Crops, Diseases, Mandis)
│   ├── models/                     # Relational ORM Domain Models
│   │   ├── user.py                 # User, Authentication, Password Reset
│   │   ├── farm.py                 # FarmerProfile, Farm Plots, SoilRecord
│   │   ├── crop.py                 # Crop Agronomics, CropHistory, CropRecommendation
│   │   ├── disease.py              # Disease Master & Image Prediction Logs
│   │   ├── market.py               # Mandi Markets & Commodity Rates
│   │   ├── advisory.py             # Fertilizer, Irrigation & Government Schemes
│   │   ├── notification.py         # In-App Notifications
│   │   └── chat.py                 # AI Chatbot History
│   ├── routes/                     # Modular REST API Endpoints
│   │   ├── auth_routes.py          # /api/auth (JWT Login, Register, Profile, Reset)
│   │   ├── farmer_routes.py        # /api/farmer (Profile, Soil Analysis, Telemetry)
│   │   ├── crop_routes.py          # /api/crop (Crop Selection & ML Recommendation)
│   │   ├── fertilizer_routes.py    # /api/fertilizer (NPK Deficiencies & Organic Alternatives)
│   │   ├── irrigation_routes.py    # /api/irrigation (Smart Water Scheduling)
│   │   ├── disease_routes.py       # /api/disease (Leaf Diagnosis & Image Processing)
│   │   ├── weather_routes.py       # /api/weather (Forecast & Dynamic Farming Alerts)
│   │   ├── market_routes.py        # /api/market (Mandi Prices & Trends)
│   │   ├── schemes_routes.py       # /api/schemes (Government Welfare Schemes)
│   │   ├── chatbot_routes.py       # /api/chatbot (Agricultural NLP Advisor)
│   │   └── admin_routes.py         # /api/admin (System Statistics & Management)
│   ├── services/                   # Business Logic & External Integrations
│   ├── ml/                         # AI Models & Training Pipelines
│   └── utils/                      # Validators & Helper Utilities
└── frontend/                       # React.js Modern Dashboard
    ├── src/
    │   ├── components/             # Reusable UI Elements (Navbar, Sidebar, Cards)
    │   ├── pages/                  # Route Pages (Dashboard, Disease, Advisory)
    │   ├── services/               # Axios API Clients
    │   ├── context/                # Auth & Multi-language Contexts
    │   └── locales/                # Internationalization (en, te, hi)
```

---

## 🚀 Quick Start Guide

### 1. Backend Setup
```bash
cd backend
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Seed database with master agronomic data & test accounts
python database/seed.py

# Launch Flask development server
python app.py
```
Backend API will be accessible at: `http://localhost:5000` (Health check: `http://localhost:5000/api/health`)

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```
Frontend Web Dashboard will be available at: `http://localhost:3000`

---

## ⚡ 1-Click Fast Launch (Local Development)

### On Windows:
Double-click `run_local.bat` or run in terminal:
```cmd
.\run_local.bat
```

### On Linux / macOS:
```bash
chmod +x run_local.sh
./run_local.sh
```
This automatically boots the Flask API on `http://localhost:5000` and the React frontend on `http://localhost:3000`.

---

## 🧪 Automated Pytest Test Suite

Execute the 30 unit & integration test cases:
```bash
cd backend
.venv\Scripts\python.exe -m pytest tests -v
```
Output:
```text
======================== 30 passed, 1 warning in 4.64s ========================
```

---

## 🔑 Demo Credentials

| Role | Email | Password | Access Level |
|---|---|---|---|
| **System Admin** | `admin@farmeradvisory.org` | `Admin@123` | Platform Moderation & CSV Reports |
| **Demo Farmer** | `farmer@demo.org` | `Farmer@123` | Full Farmer Portal Access |

---

## 📚 Project Documentation & Viva Guides

- 📘 [DEMO_WALKTHROUGH.md](file:///C:/Users/Rakesh/.gemini/antigravity-ide/scratch/farmer-crop-advisory/DEMO_WALKTHROUGH.md): Exact 10-minute faculty presentation sequence and test cases.
- 🎓 [FACULTY_VIVA_GUIDE.md](file:///C:/Users/Rakesh/.gemini/antigravity-ide/scratch/farmer-crop-advisory/FACULTY_VIVA_GUIDE.md): Technical defense answers (ML math, ICAR formulas, RBAC security).
- 🚀 [DEPLOYMENT_GUIDE.md](file:///C:/Users/Rakesh/.gemini/antigravity-ide/scratch/farmer-crop-advisory/DEPLOYMENT_GUIDE.md): Production deployment guides for Docker, Render, AWS EC2, and Google Cloud Run.
- 🐳 [docker-compose.yml](file:///C:/Users/Rakesh/.gemini/antigravity-ide/scratch/farmer-crop-advisory/docker-compose.yml): Production container orchestration.
- ☁️ [render.yaml](file:///C:/Users/Rakesh/.gemini/antigravity-ide/scratch/farmer-crop-advisory/render.yaml): Render Blueprint for free cloud hosting.

