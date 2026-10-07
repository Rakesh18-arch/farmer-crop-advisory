import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Ensure paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
DATASET_PATH = os.path.join(PROJECT_ROOT, "datasets", "crop_recommendation_data.csv")
MODEL_SAVE_PATH = os.path.join(CURRENT_DIR, "crop_model.pkl")
PREPROCESSOR_SAVE_PATH = os.path.join(CURRENT_DIR, "preprocessor.pkl")

def generate_benchmark_dataset(file_path: str):
    """Generates realistic agronomic training samples for 12 key crops."""
    print("[DATASET] Generating calibrated agricultural telemetry dataset...")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Agronomic profiles: (N_mean, N_std, P_mean, P_std, K_mean, K_std, temp_mean, temp_std, hum_mean, hum_std, ph_mean, ph_std, rain_mean, rain_std)
    profiles = {
        "Rice": (80, 10, 48, 8, 40, 5, 23.5, 2.5, 82, 5, 6.4, 0.4, 230, 25),
        "Maize": (78, 12, 48, 9, 20, 4, 22.0, 3.0, 65, 8, 6.3, 0.5, 85, 15),
        "Cotton": (118, 12, 46, 8, 20, 5, 24.0, 2.0, 79, 6, 6.9, 0.5, 80, 12),
        "Groundnut": (22, 6, 52, 9, 38, 6, 26.5, 3.0, 68, 7, 6.5, 0.4, 75, 15),
        "Sugarcane": (195, 20, 72, 10, 95, 12, 28.0, 3.0, 75, 8, 7.0, 0.5, 200, 30),
        "Wheat": (115, 14, 58, 8, 35, 5, 16.5, 2.5, 58, 6, 6.8, 0.4, 95, 18),
        "Millet": (48, 8, 28, 6, 20, 4, 29.0, 3.5, 45, 8, 6.6, 0.5, 52, 12),
        "Pulses": (25, 6, 58, 8, 68, 8, 20.0, 2.5, 52, 7, 7.1, 0.4, 65, 14),
        "Tomato": (98, 12, 74, 9, 78, 9, 22.5, 2.0, 68, 6, 6.5, 0.3, 90, 15),
        "Chilli": (105, 12, 55, 7, 56, 7, 26.0, 2.5, 62, 7, 6.7, 0.4, 72, 12),
        "Soybean": (28, 6, 68, 8, 42, 6, 24.5, 2.5, 70, 6, 6.8, 0.4, 98, 16),
        "Banana": (180, 15, 65, 8, 195, 15, 27.5, 2.0, 80, 5, 6.7, 0.4, 165, 20)
    }

    records = []
    np.random.seed(42)
    samples_per_crop = 200

    for crop, (nm, ns, pm, ps, km, ks, tm, ts, hm, hs, phm, phs, rm, rs) in profiles.items():
        for _ in range(samples_per_crop):
            n = max(5, np.random.normal(nm, ns))
            p = max(5, np.random.normal(pm, ps))
            k = max(5, np.random.normal(km, ks))
            temp = np.random.normal(tm, ts)
            hum = np.clip(np.random.normal(hm, hs), 10, 100)
            ph = np.clip(np.random.normal(phm, phs), 3.5, 9.5)
            rain = max(10, np.random.normal(rm, rs))
            records.append({
                "N": round(n, 2),
                "P": round(p, 2),
                "K": round(k, 2),
                "temperature": round(temp, 2),
                "humidity": round(hum, 2),
                "ph": round(ph, 2),
                "rainfall": round(rain, 2),
                "crop": crop
            })

    df = pd.DataFrame(records)
    df.to_csv(file_path, index=False)
    print(f"[DATASET] Saved {len(df)} samples across 12 crops to: {file_path}")
    return df

def train_and_evaluate():
    """Trains and compares Random Forest, Decision Tree, KNN, Logistic Regression."""
    if not os.path.exists(DATASET_PATH):
        df = generate_benchmark_dataset(DATASET_PATH)
    else:
        df = pd.read_csv(DATASET_PATH)

    print(f"[TRAIN] Loaded dataset with {len(df)} samples.")
    feature_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    X = df[feature_cols]
    y = df["crop"]

    # Encode crop labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # 80-20 Train-Test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.20, random_state=42, stratify=y_encoded
    )

    # Standardize numerical features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Candidate models for rigorous comparison
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }

    results = {}
    print("\n" + "=" * 50)
    print("      MODEL PERFORMANCE COMPARISON (TEST SET)")
    print("=" * 50)

    best_name = None
    best_accuracy = -1.0
    best_model = None

    for name, clf in models.items():
        clf.fit(X_train_scaled, y_train)
        preds = clf.predict(X_test_scaled)
        acc = accuracy_score(y_test, preds)
        results[name] = acc
        print(f"  --> {name:<22} Accuracy: {acc * 100:.2f}%")

        if acc > best_accuracy:
            best_accuracy = acc
            best_name = name
            best_model = clf

    print("=" * 50)
    print(f"[SELECTED] Best Performing Model: {best_name} ({best_accuracy * 100:.2f}%)")

    # Save trained best model and preprocessors
    joblib.dump(best_model, MODEL_SAVE_PATH)
    joblib.dump({
        "scaler": scaler,
        "label_encoder": label_encoder,
        "feature_names": feature_cols,
        "model_name": best_name,
        "accuracy": round(best_accuracy, 4),
        "classes": list(label_encoder.classes_)
    }, PREPROCESSOR_SAVE_PATH)

    print(f"[SUCCESS] Model artifact saved to: {MODEL_SAVE_PATH}")
    print(f"[SUCCESS] Preprocessor artifact saved to: {PREPROCESSOR_SAVE_PATH}")

    # Detailed Classification Report
    y_pred_best = best_model.predict(X_test_scaled)
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred_best, target_names=label_encoder.classes_))

    return best_name, best_accuracy

if __name__ == "__main__":
    train_and_evaluate()
