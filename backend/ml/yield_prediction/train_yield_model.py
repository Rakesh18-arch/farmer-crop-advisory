import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
DATASET_PATH = os.path.join(PROJECT_ROOT, "datasets", "crop_yield_data.csv")
MODEL_SAVE_PATH = os.path.join(CURRENT_DIR, "yield_model.pkl")
PREPROCESSOR_SAVE_PATH = os.path.join(CURRENT_DIR, "yield_preprocessor.pkl")

def generate_yield_dataset(file_path: str):
    """Generates realistic agronomic yield records based on ICAR productivity benchmarks."""
    print("[YIELD DATASET] Generating synthetic yield benchmarks...")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    np.random.seed(42)

    # Base yield in tons/hectare (mean, std)
    crop_yield_bases = {
        "Rice": (3.8, 0.6), "Wheat": (3.5, 0.5), "Maize": (4.2, 0.7),
        "Cotton": (2.2, 0.4), "Groundnut": (2.0, 0.3), "Sugarcane": (72.0, 8.0),
        "Millet": (1.8, 0.3), "Pulses": (1.4, 0.25), "Tomato": (24.0, 3.5),
        "Chilli": (2.8, 0.4), "Soybean": (2.1, 0.3), "Banana": (42.0, 5.0)
    }

    seasons = ["Kharif", "Rabi", "Zaid"]
    records = []

    for crop, (base_y, std_y) in crop_yield_bases.items():
        for _ in range(150):
            area = round(float(np.random.uniform(1.0, 15.0)), 1)  # hectares
            rainfall = round(float(np.random.uniform(50.0, 300.0)), 1)
            temp = round(float(np.random.uniform(18.0, 36.0)), 1)
            n = round(float(np.random.uniform(40.0, 180.0)), 1)
            p = round(float(np.random.uniform(20.0, 80.0)), 1)
            k = round(float(np.random.uniform(20.0, 90.0)), 1)
            ph = round(float(np.random.uniform(5.5, 8.2)), 2)
            fert_usage = round(float(np.random.uniform(50.0, 250.0)), 1)  # kg/ha
            season = np.random.choice(seasons)

            # Realistic yield calculation with agronomic response curve
            fert_boost = (fert_usage / 150.0) * 0.15
            rain_factor = 1.0 - abs(rainfall - 150.0) / 400.0
            noise = np.random.normal(0, std_y * 0.5)

            actual_yield_per_ha = max(0.5, (base_y * rain_factor * (1.0 + fert_boost)) + noise)
            total_yield_tons = round(actual_yield_per_ha * area, 2)

            records.append({
                "crop": crop,
                "season": season,
                "area_ha": area,
                "rainfall": rainfall,
                "temperature": temp,
                "n": n,
                "p": p,
                "k": k,
                "ph": ph,
                "fertilizer_kg_ha": fert_usage,
                "yield_tons_per_ha": round(actual_yield_per_ha, 2),
                "total_yield_tons": total_yield_tons
            })

    df = pd.DataFrame(records)
    df.to_csv(file_path, index=False)
    print(f"[YIELD DATASET] Generated {len(df)} samples: {file_path}")
    return df

def train_yield_models():
    """Trains and compares Linear Regression, Random Forest Regressor, and Gradient Boosting Regressor."""
    if not os.path.exists(DATASET_PATH):
        df = generate_yield_dataset(DATASET_PATH)
    else:
        df = pd.read_csv(DATASET_PATH)

    features = ["crop", "season", "area_ha", "rainfall", "temperature", "n", "p", "k", "ph", "fertilizer_kg_ha"]
    target = "yield_tons_per_ha"

    X = df[features]
    y = df[target]

    categorical_cols = ["crop", "season"]
    numerical_cols = ["area_ha", "rainfall", "temperature", "n", "p", "k", "ph", "fertilizer_kg_ha"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_cols)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    candidate_models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    }

    print("\n" + "=" * 55)
    print("      YIELD REGRESSION MODEL BENCHMARKS (TEST SET)")
    print("=" * 55)

    best_name = None
    best_r2 = -float("inf")
    best_model = None

    for name, model in candidate_models.items():
        model.fit(X_train_proc, y_train)
        preds = model.predict(X_test_proc)
        r2 = r2_score(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        print(f"  --> {name:<28} R2: {r2:.4f} | RMSE: {rmse:.3f} tons/ha")

        if r2 > best_r2:
            best_r2 = r2
            best_name = name
            best_model = model

    print("=" * 55)
    print(f"[SELECTED] Best Model: {best_name} (R² = {best_r2:.4f})")

    # Serialize artifacts
    joblib.dump(best_model, MODEL_SAVE_PATH)
    joblib.dump({
        "preprocessor": preprocessor,
        "model_name": best_name,
        "r2_score": round(best_r2, 4),
        "features": features
    }, PREPROCESSOR_SAVE_PATH)

    print(f"[SUCCESS] Saved model to: {MODEL_SAVE_PATH}")
    print(f"[SUCCESS] Saved preprocessor to: {PREPROCESSOR_SAVE_PATH}")

    return best_name, best_r2

if __name__ == "__main__":
    train_yield_models()
