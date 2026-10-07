# Faculty Demonstration & End-to-End Evaluation Walkthrough

This document outlines the exact, step-by-step demonstration sequence to showcase the **Farmer Crop Advisory Platform** to college project examiners and review panels.

---

## 1. Quick Demonstration Credentials

| Role | Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Farmer** | `farmer@demo.org` | `Farmer@123` | Full Farmer Portal Access |
| **Admin** | `admin@farmeradvisory.org` | `Admin@123` | Platform Moderation & CSV Reports |

*(Tip: Both login pages feature 1-click **Quick Demo Credentials** autofill buttons for instant login).*

---

## 2. Recommended Demonstration Flow (10 - 15 Minutes)

### Step 1: System Health & Architecture Overview (1 Min)
- Navigate to `http://localhost:5000/api/health` in your browser.
- **Show Examiner:**
  ```json
  {
    "demo_mode": true,
    "environment": "development",
    "service": "Farmer Crop Advisory Platform API",
    "status": "healthy",
    "version": "1.0.0"
  }
  ```
- **Explanation:** Explain the decoupled architecture: Flask REST API backend with SQLite/PostgreSQL-ready schema and React 18 frontend with Vite.

---

### Step 2: Farmer Login & Multilingual Switching (1 Min)
1. Open `http://localhost:3000/login`.
2. Click **"🧑‍🌾 Farmer Demo"** and sign in.
3. In the top navigation bar, click the language dropdown and select **తెలుగు (Telugu)**.
   - Show how navigation labels, titles, and buttons instantly translate to Telugu.
4. Switch to **हिन्दी (Hindi)**, then switch back to **English**.
5. **Key Point:** Highlight that localizing agricultural technology makes AI accessible to non-English-speaking rural farmers.

---

### Step 3: Interactive Farm Dashboard (1 Min)
1. Point out the top 4 real-time telemetry cards:
   - **Active Farm Land:** 2.5 Acres (Loamy Soil)
   - **Live Temperature:** 28°C with 65% Humidity
   - **Soil Reaction:** 6.8 pH (Optimal)
   - **Live Mandi Ticker:** Cotton rate at Kurnool APMC
2. Point out the dynamic **Weather Advisory Banner** calculating whether the current morning hours are favorable for pesticide spraying.

---

### Step 4: AI Crop Recommendation Engine (2 Mins)
1. Navigate to **Crop Advisory** (`/crop-recommendation`).
2. Click **"Fill From My Farm Profile"** to load telemetry.
3. Test Case A (Monsoon Cereal):
   - **N:** 90 | **P:** 42 | **K:** 43 | **pH:** 6.8 | **Temp:** 28°C | **Rainfall:** 180 mm | **Season:** Kharif
   - Click **"Generate AI Recommendation"**.
   - **Result:** **Rice (Paddy)** with **95% Confidence**.
   - Review the agronomic rationale and the alternative crops (Maize, Pulses).
4. Click **"View Sowing Calendar"** or **"Estimate Harvest Yield"** directly from the results card to demonstrate unified platform integration.

---

### Step 5: Digital Soil Health Card (1 Min)
1. Navigate to **Soil Analysis** (`/soil-analysis`).
2. Showcase the digital progress gauges for **Nitrogen, Phosphorus, Potassium, pH, and Moisture**.
3. Point out the dynamic status labels:
   - Deficient / Optimal / Surplus classifications based on ICAR thresholds.
4. Show the actionable organic amendments:
   - Lime/Gypsum dosage for pH correction.
   - Biofertilizer inoculation tips (*Azospirillum* / *Rhizobium*).

---

### Step 6: Live Meteorological Tracking & Spraying Window (1 Min)
1. Navigate to **Weather & Forecast** (`/weather`).
2. In the search box, search for a district (e.g., `Guntur`, `Warangal`, or `Pune`).
3. Show the **5-Day Agricultural Weather Outlook** with rain probability percentages.
4. Point out the **Field Spraying Window Alert**:
   - Demonstrates that if rainfall > 5mm is predicted, the system warns farmers to postpone foliar chemical sprays.

---

### Step 7: Smart Irrigation Schedule (1.5 Mins)
1. Navigate to **Irrigation Advisory** (`/irrigation`).
2. Select:
   - **Crop:** Rice | **Growth Stage:** Flowering | **Soil:** Loamy | **Area:** 2.5 Acres
3. Click **"Calculate Watering Schedule"**.
4. **Result:**
   - **Water Volume:** ~18,500 Liters/Acre.
   - **Pump Run Time:** 2.5 hours with a 5 HP agricultural pump.
   - **Rain-Pause Automation:** Notice the automated rule: *If rainfall exceeds 15 mm within 24 hours, postpone irrigation by 48 hours*.

---

### Step 8: Stoichiometric Fertilizer Deficit Calculator (1.5 Mins)
1. Navigate to **Fertilizer Calculator** (`/fertilizer`).
2. Enter:
   - **Crop:** Rice | **Target Yield:** 2.5 Tons/Acre | **Area:** 2.0 Acres
3. Click **"Calculate Fertilizer Dosage"**.
4. **Result:**
   - **Chemical Bags:** Exact counts for Urea (45kg bags), DAP (50kg bags), and MOP (50kg bags).
   - **Organic Alternative:** 1.5 tons/acre Vermicompost + 50 kg Neem Cake.
   - **Split Application Rule:** Basal dose (sowing) vs Top-dressing splits at 30 and 60 days.

---

### Step 9: Plant Leaf Disease Diagnostic AI (1.5 Mins)
1. Navigate to **Crop Disease AI** (`/disease-detection`).
2. Upload any plant leaf image or drag-and-drop a sample file.
3. Click **"Diagnose Leaf Disease"**.
4. **Result:**
   - Detects the condition with confidence rating.
   - Outlines symptoms.
   - Delivers a two-pronged prescription:
     - **Curative Chemical Spray:** e.g., Copper Oxychloride 50% WP @ 3 g/L.
     - **Organic & Biological Control:** e.g., Neem Oil (10,000 ppm) @ 3 ml/L.

---

### Step 10: Harvest Yield Prediction Engine (1 Min)
1. Navigate to **Harvest Yield AI** (`/yield-prediction`).
2. Select Crop: **Rice**, Area: **3.0 Acres**, Rainfall: **150 mm**, Temperature: **28°C**, Season: **Kharif**.
3. Click **"Predict Harvest Output"**.
4. **Show Examiner the Trained Model Metrics:**
   - Productivity: **~1.85 Tons/Acre**.
   - Total Expected Harvest: **~5.55 Tons**.
   - **Model Used:** Linear Regression ($R^2 = 0.9776$, RMSE = 3.187 tons/ha).

---

### Step 11: Multilingual Agricultural AI Chatbot (1.5 Mins)
1. Navigate to **Agri AI Assistant** (`/chatbot`).
2. Click the quick suggestion: *"What crop should I grow in Kharif?"*
3. Next, type a question in Telugu or Hindi:
   - Telugu: *"టమోటా ఆకు ముడత నివారణ ఎలా?"*
   - Hindi: *"कपास का मंडी भाव क्या है?"*
4. Show how the chatbot answers directly with tailored agro-scientific advice.

---

### Step 12: Superadmin Portal & CSV Report Streaming (1.5 Mins)
1. Log out from the farmer account.
2. Sign in with **"🛡️ Admin Demo"** (`admin@farmeradvisory.org` / `Admin@123`).
3. Navigate to **Admin Portal** (`/admin`).
4. **Show Examiner Platform-Wide Analytics:**
   - Total Registered Farmers, Recommendations Run, Disease Scans, Catalog Counts.
   - Most Recommended Crops breakdown.
5. In the **Registered Farmers Directory**, click **"Deactivate"** on a farmer account to demonstrate moderation, then click **"Activate"**.
6. In the **CSV Data Export Center**, click **"Export Farmers CSV"** and **"Export Recommendations CSV"**.
   - Show the browser streaming and saving the `.csv` files instantly. Open them in Excel or Notepad to show complete tabular records.

---

### Step 13: Pytest Automated Test Suite Verification (1 Min)
1. Open terminal in `farmer-crop-advisory/`.
2. Run:
   ```powershell
   & "backend\.venv\Scripts\python.exe" -m pytest backend/tests -v
   ```
3. **Show Examiner the 100% Pass Rate:**
   ```text
   ======================== 30 passed, 1 warning in 4.64s ========================
   ```
   All 30 unit and integration tests passing cleanly across RBAC, ML classifiers, regression models, rule engines, and API endpoints.
