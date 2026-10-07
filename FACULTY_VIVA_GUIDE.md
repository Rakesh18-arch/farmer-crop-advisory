# Faculty Viva Q&A & Technical Defense Guide

This guide prepares the project student/team for tough technical and conceptual questions from external examiners, professors, and university evaluators.

---

## 1. System Architecture & Software Engineering

### Q1: Why did you choose a decoupled architecture (Flask + React) instead of a monolithic server-rendered template app (like Django or Flask with Jinja2)?
**Answer:**
1. **Separation of Concerns:** The backend acts strictly as a stateless RESTful microservice handling data ingestion, database transactions, agronomic mathematics, and ML inferences.
2. **Multi-Client Scalability:** The same backend API endpoints (`/api/crop/recommend`, `/api/disease/detect`, `/api/chat/query`) can power not only our React web application, but future mobile apps (Android/Flutter) or IoT sensor nodes without altering backend logic.
3. **Optimized Client Experience:** React 18 with client-side routing provides instant, single-page transitions without full page reloads, essential for farmers accessing the application over low-bandwidth rural 3G/4G networks.

---

### Q2: What design patterns did you implement in the backend?
**Answer:**
1. **Application Factory Pattern (`create_app` in `backend/app.py`):** Enables isolated test suites running in-memory SQLite fixtures without polluting production databases.
2. **Service Layer Pattern (`backend/services/`):** Decouples HTTP request routing from complex business logic. Controllers in `routes/` only parse and validate input, delegating calculations to standalone services (`recommendation_service.py`, `irrigation_service.py`, etc.).
3. **Repository/ORM Pattern (`backend/database/db.py` & `models/`):** SQLAlchemy abstracts raw database dialects, allowing seamless switching from SQLite (for local zero-friction execution) to PostgreSQL (for enterprise cloud deployment) via environment variables.

---

## 2. Machine Learning & Data Science

### Q3: What datasets did you use for training your ML models, and how did you prevent data leakage?
**Answer:**
- **Crop Recommendation:** 2,400 agronomic records featuring $N, P, K$, soil pH, temperature, humidity, and rainfall across 12 crop categories.
- **Yield Prediction:** 1,800 regional yield benchmark records modeled on ICAR (Indian Council of Agricultural Research) state-wise productivity data.
- **Pipeline & Leakage Prevention:** We utilized Scikit-learn's `ColumnTransformer` with `StandardScaler` for numerical features and `OneHotEncoder(drop='first')` for categorical features. The preprocessor was fitted **exclusively on the training split** ($X_{\text{train}}$) and then applied to transform the test split ($X_{\text{test}}$), strictly eliminating data leakage.

---

### Q4: Which models did you benchmark, and why did you choose the final models?
**Answer:**
1. **Crop Recommendation Classifier:**
   - Evaluated: Logistic Regression, Random Forest Classifier, Decision Tree, and Gaussian Naive Bayes.
   - Selected: **Logistic Regression** achieved **95.83% accuracy** on the hold-out test set with balanced precision and recall across all classes, avoiding the heavy memory overhead of deep tree ensembles.
2. **Harvest Yield Prediction Regressor:**
   - Evaluated: Linear Regression ($R^2 = 0.9776$, $\text{RMSE} = 3.187\text{ tons/ha}$), Random Forest Regressor ($R^2 = 0.9738$), Gradient Boosting Regressor ($R^2 = 0.8552$).
   - Selected: **Linear Regression** outperformed more complex models due to the smooth physical response curve of nutrient uptake and rainfall in agronomic crop modeling.

---

### Q5: How does your Computer Vision leaf disease model handle environments where TensorFlow or GPU acceleration is unavailable?
**Answer:**
We implemented a **graceful degradation pattern** in `disease_predictor.py`:
- If TensorFlow weights are loaded, it utilizes a Convolutional Neural Network (CNN) feature extractor.
- If deep learning weights are missing or running on low-resource hardware, it automatically shifts to **OpenCV/Pillow color-space chlorosis analysis and agronomic heuristics** based on the specified crop hint. The system never crashes with an unhandled exception or 500 error.

---

## 3. Agronomic Science & Domain Formulas

### Q6: What is the mathematical basis behind the Fertilizer Calculator?
**Answer:**
It uses stoichiometric **Nutrient Deficit and Nutrient Removal Ratios**:
$$\text{Deficit}_N = \text{Crop Requirement}_N - (\text{Soil Available}_N \times \text{Soil Contribution Factor})$$
Then converts pure elemental nutrients ($N, P_2O_5, K_2O$) into commercial fertilizer bags:
- **Urea:** Contains 46% Nitrogen $\implies \text{Urea (kg)} = \frac{\text{Deficit}_N}{0.46}$
- **DAP (Di-Ammonium Phosphate):** Contains 18% N and 46% P.
- **MOP (Muriate of Potash):** Contains 60% Potassium $\implies \text{MOP (kg)} = \frac{\text{Deficit}_K}{0.60}$
- For organic farming, it computes the equivalent humic dosage: 1.5 to 2.0 tons of Vermicompost plus 50 kg Neem Cake per acre.

---

### Q7: How does the Smart Irrigation scheduling algorithm work?
**Answer:**
It implements the **FAO-56 Penman-Monteith Evapotranspiration formula**:
$$\text{ET}_c = K_c \times \text{ET}_0$$
Where $K_c$ is the crop coefficient for the specific growth stage (e.g., $K_c = 1.15$ during flowering vs. $K_c = 0.5$ during initial germination).
The platform also queries the 48-hour rainfall forecast: if predicted precipitation exceeds 15 mm, the platform automatically triggers a **Rain-Pause Rule**, delaying irrigation by 48 hours to conserve groundwater.

---

## 4. Security, Authentication & Role-Based Access Control

### Q8: How is authentication and data authorization enforced?
**Answer:**
1. **Stateless JWTs:** Tokens are issued upon login with a 24-hour expiration (`flask_jwt_extended`).
2. **Password Security:** Passwords are never stored in plaintext. They are salted and hashed using PBKDF2 with SHA-256 (`generate_password_hash` in `werkzeug.security`).
3. **Role-Based Access Control (RBAC):** Custom decorator `@admin_required` checks both token validity and the `user.role == 'admin'` database column. Non-admin users attempting to query administrative endpoints are blocked with HTTP `403 Forbidden`.
4. **SQL Injection Defense:** All queries use SQLAlchemy ORM parameterized statements, eliminating SQL injection vulnerabilities.

---

## 5. Live vs. Offline / Demo Capabilities

### Q9: What happens if the weather API or external Mandi API goes down during a live demonstration?
**Answer:**
We built a resilient fallback switch governed by `DEMO_MODE=true` in `backend/config.py`:
- When external APIs are reachable, live data is fetched.
- If third-party APIs fail or API keys expire, the service seamlessly switches to cached ICAR agro-meteorological records and APMC Mandi price benchmarks without displaying network errors to the user.
