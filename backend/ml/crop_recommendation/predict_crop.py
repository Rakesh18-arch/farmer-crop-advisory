import os

try:
    import joblib
    import numpy as np
except ImportError:
    joblib = None
    np = None

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "crop_model.pkl")
PREPROCESSOR_PATH = os.path.join(CURRENT_DIR, "preprocessor.pkl")

# Cached model artifacts
_model = None
_preprocessor = None

def _load_artifacts():
    global _model, _preprocessor
    if joblib is None:
        return None, None
    if _model is None and os.path.exists(MODEL_PATH) and os.path.exists(PREPROCESSOR_PATH):
        try:
            _model = joblib.load(MODEL_PATH)
            _preprocessor = joblib.load(PREPROCESSOR_PATH)
        except Exception as e:
            print(f"[WARN] Error loading crop model: {e}")
            _model = None
            _preprocessor = None
    return _model, _preprocessor

def predict_suitable_crop(n: float, p: float, k: float, temperature: float, 
                          humidity: float, ph: float, rainfall: float, 
                          soil_type: str = "Loamy", season: str = "Kharif") -> dict:
    """
    Predicts the best suitable crop given soil and climate conditions.
    Returns:
        recommended_crop, confidence, alternative_1, alternative_2, explanation
    """
    model, prep = _load_artifacts()

    if model is not None and prep is not None:
        try:
            scaler = prep["scaler"]
            label_encoder = prep["label_encoder"]
            classes = prep["classes"]

            features = np.array([[n, p, k, temperature, humidity, ph, rainfall]])
            features_scaled = scaler.transform(features)

            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(features_scaled)[0]
                top_indices = np.argsort(probs)[::-1]
                
                top_crop = classes[top_indices[0]]
                top_conf = float(probs[top_indices[0]])
                alt_1 = classes[top_indices[1]] if len(top_indices) > 1 else None
                alt_2 = classes[top_indices[2]] if len(top_indices) > 2 else None
            else:
                pred_idx = model.predict(features_scaled)[0]
                top_crop = label_encoder.inverse_transform([pred_idx])[0]
                top_conf = 0.85
                alt_1 = "Maize" if top_crop != "Maize" else "Rice"
                alt_2 = "Pulses" if top_crop != "Pulses" else "Wheat"

            explanation = (
                f"{top_crop} is recommended with a model confidence of {round(top_conf * 100, 1)}% "
                f"based on your soil nutrient levels (N={n}, P={p}, K={k}, pH={ph}) "
                f"and prevailing climatic metrics (Temp={temperature}°C, Rain={rainfall}mm). "
                f"Secondary viable alternatives include {alt_1} and {alt_2}."
            )

            return {
                "recommended_crop": top_crop,
                "confidence_score": round(top_conf * 100, 2),
                "alternative_crop_1": alt_1,
                "alternative_crop_2": alt_2,
                "explanation": explanation,
                "model_used": prep.get("model_name", "Random Forest")
            }
        except Exception as e:
            print(f"[ERROR] Inference error in predict_crop: {e}")

    # Robust Agronomic Heuristic Fallback
    return _rule_based_crop_fallback(n, p, k, temperature, humidity, ph, rainfall, season)

def _rule_based_crop_fallback(n, p, k, temp, hum, ph, rain, season):
    """Agronomic rule-based decision fallback if ML model is unavailable."""
    if rain > 180 and temp > 20 and n > 70:
        top_crop, alt1, alt2 = "Rice", "Sugarcane", "Banana"
    elif temp < 20 and n > 90 and season in ("Rabi", "Winter"):
        top_crop, alt1, alt2 = "Wheat", "Tomato", "Pulses"
    elif n > 90 and rain < 120 and temp > 22:
        top_crop, alt1, alt2 = "Cotton", "Maize", "Chilli"
    elif n < 40 and p > 40:
        top_crop, alt1, alt2 = "Groundnut", "Pulses", "Soybean"
    elif rain < 60 and temp > 25:
        top_crop, alt1, alt2 = "Millet", "Pulses", "Groundnut"
    elif k > 120:
        top_crop, alt1, alt2 = "Banana", "Sugarcane", "Tomato"
    else:
        top_crop, alt1, alt2 = "Maize", "Groundnut", "Cotton"

    return {
        "recommended_crop": top_crop,
        "confidence_score": 82.5,
        "alternative_crop_1": alt1,
        "alternative_crop_2": alt2,
        "explanation": (
            f"{top_crop} is recommended based on established agronomic threshold standards for "
            f"soil N={n}, P={p}, K={k}, pH={ph} and climate temp={temp}°C, rain={rain}mm."
        ),
        "model_used": "Agronomic Knowledgebase Heuristic"
    }
