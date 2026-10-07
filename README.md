# 🌱 Farmer Crop Advisory Platform
### AI-Based Smart Decision Support System for Farmers

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React 18](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, full-stack agricultural decision support system designed to empower farmers with data-driven agronomic intelligence. The platform combines machine learning (Random Forest, XGBoost), deep computer vision, and multi-model Large Language Models (AgriLLM-Neural, Google Gemini, Groq Llama 3, OpenAI) to provide personalized recommendations on crop selection, balanced soil nutrition, irrigation schedules, plant disease diagnosis, and mandi market trends.

---

## 🌐 Live Web Experience

> [!TIP]
> **Experience the Live Application Immediately:**  
> 👉 **[Live Cloudflare Edge Web App](https://individuals-pressing-vacuum-tested.trycloudflare.com)**  
> *(No passwords required. Optimized for Android, iOS, tablets, and desktop browsers).*

### 🔑 Demo Accounts for Evaluators & Farmers
| Role | Email | Password | Available Features |
| :--- | :--- | :--- | :--- |
| **🌾 Farmer** | `farmer@demo.org` | `Farmer@123` | Crop Advisory, NPK Soil Planner, Weather Telemetry, Yield Estimator, Fertilizer Advisory, Disease Scanner, AgriAI LLM Chat |
| **🛡️ Admin** | `admin@farmeradvisory.org` | `Admin@123` | Model Accuracy Telemetry, System Health, Farmer Logs, APMC Admin Controls |

---

## 📦 How Public Users Can Experience & Run This Application

Choose any of the options below:

### Option 1: 1-Click ZIP Download (Fastest for Windows / Mac / Linux)
1. Download the complete, pre-packaged project archive directly from this repository:  
   👉 **[Download farmer-crop-advisory.zip](https://github.com/Rakesh18-arch/farmer-crop-advisory/raw/main/downloads/farmer-crop-advisory.zip)** *(or from [Releases](https://github.com/Rakesh18-arch/farmer-crop-advisory/releases))*
2. Unzip the folder anywhere on your computer.
3. On Windows, double-click **`run_project.bat`** (or run `python backend/app.py`).
4. Open `http://localhost:5000` in any web browser!

---

### Option 2: Clone via Git (Developers)
```bash
# Clone the repository
git clone https://github.com/Rakesh18-arch/farmer-crop-advisory.git
cd farmer-crop-advisory

# Windows Quick Start:
run_project.bat

# Manual Python Setup:
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python database/seed.py
python app.py
```
Open **`http://localhost:5000`** — the Flask backend automatically serves the compiled React single-page frontend.

---

### Option 3: Docker & Docker Compose (Zero Configuration)
```bash
git clone https://github.com/Rakesh18-arch/farmer-crop-advisory.git
cd farmer-crop-advisory
docker-compose up -d --build
```
Access the application at `http://localhost:3000` (Frontend) and `http://localhost:5000` (API).

---

### Option 4: 1-Click Cloud Deployment (Render / Hugging Face Spaces)
- **Hugging Face Spaces (100% Free 24/7):**
  Create a new Space with the Docker SDK and upload this repo. It will run 24/7 at `https://<your-username>-farmer-crop-advisory.hf.space`.
- **Render.com:**
  Connect this GitHub repository on Render. The included [`render.yaml`](./render.yaml) automatically builds and provisions the web service.

---

## 🧠 Multi-Model LLM Agricultural Advisory Engine

The platform integrates a hybrid LLM agronomic intelligence architecture:

```text
                               ┌────────────────────────────────────────┐
                               │   Farmer Inquiry / Sowing Context       │
                               └──────────────────┬─────────────────────┘
                                                  ▼
                       ┌──────────────────────────────────────────────────┐
                       │               AgriAI LLM Router                  │
                       └──┬───────────────┬────────────────┬───────────┬──┘
                          │               │                │           │
                          ▼               ▼                ▼           ▼
                   ┌────────────┐  ┌─────────────┐  ┌────────────┐  ┌─────────────┐
                   │  AgriLLM   │  │   Google    │  │    Groq    │  │   OpenAI    │
                   │  -Neural   │  │ Gemini 1.5  │  │ LLaMA 3.3  │  │ GPT-4o Mini │
                   │  (Built-in)│  │    Flash    │  │    70B     │  │             │
                   └────────────┘  └─────────────┘  └────────────┘  └─────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────────────────┐
        │  360° Agronomic Justification & Fertilizer Prescriptions │
        │  • Soil NPK Synergy     • Sowing & Irrigation Stages    │
        │  • IPM Pest Protocols   • Harvest Financial ROI (MSP)   │
        └─────────────────────────────────────────────────────────┘
```

1. **`AgriLLM-Neural` (Built-in Knowledge Engine):** Runs 100% offline without external keys. Produces detailed 360-degree agronomic reasoning for any soil parameter combination.
2. **External Cloud Models:** Easily activated by adding `GEMINI_API_KEY`, `GROQ_API_KEY`, or `OPENAI_API_KEY` to `backend/.env`.

---

## 📁 Repository Structure

```text
farmer-crop-advisory/
├── backend/
│   ├── app.py                      # Unified Application Factory & Static SPA Server
│   ├── config.py                   # Central Config (SQLite/PostgreSQL, JWT, Demo Mode)
│   ├── requirements.txt            # Python Dependencies
│   ├── database/
│   │   ├── db.py                   # SQLAlchemy ORM Setup
│   │   ├── seed.py                 # Master Seed Data (Crops, Diseases, Mandis, Users)
│   │   └── farmer_advisory.db      # SQLite Database with Initialized Master Records
│   ├── models/                     # Domain ORM Models (User, Crop, Farm, Disease, etc.)
│   ├── routes/                     # Modular REST Blueprints (/api/crop, /api/auth, etc.)
│   ├── services/                   # Business Logic, Weather Telemetry & LLM Engine
│   │   └── llm_service.py          # Multi-Provider LLM Service (Gemini, Groq, OpenAI, Neural)
│   ├── ml/                         # Pre-Trained ML Classifiers (Crop, Disease, Yield)
│   └── tests/                      # 30 Automated Unit & Integration Tests (Pytest)
├── frontend/
│   ├── src/                        # React Source Code (Pages, Components, Contexts)
│   └── dist/                       # Production-compiled Single-Page Application Assets
├── downloads/
│   └── farmer-crop-advisory.zip    # Standalone Offline 1-Click ZIP Archive (~930 KB)
├── Dockerfile                      # Production Container for Cloud & Hugging Face
├── docker-compose.yml              # Multi-container Orchestration (Postgres + Flask + Nginx)
├── render.yaml                     # Render.com Infrastructure-as-Code Blueprint
├── run_project.bat                 # Windows 1-Click Desktop Launcher
├── run_in_background.bat           # 24/7 Detached Windows Background Runner
└── push_to_github.bat              # Automated GitHub Synchronization Helper
```

---

## 🧪 Automated Testing & Quality Assurance

Run the test suite:
```bash
cd backend
pytest tests/ -v
```
All 30 unit and integration tests validate authentication, JWT token expiry, crop recommendations, fertilizer calculations, and REST contract compliance.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE). Contributions, forks, and stars are welcome!
