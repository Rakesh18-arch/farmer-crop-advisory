from database.db import db
from models.crop import Crop, CropRecommendation
from ml.crop_recommendation.predict_crop import predict_suitable_crop
from utils.validators import validate_soil_inputs, validate_environmental_inputs

class RecommendationService:
    @staticmethod
    def get_crop_recommendation(n, p, k, temperature, humidity, ph, rainfall,
                                 soil_type="Loamy", season="Kharif", farmer_id=None):
        """
        Orchestrates ML prediction, enriches with agronomic database records,
        and persists recommendation telemetry if farmer is authenticated.
        """
        # Validate soil inputs
        s_ok, s_err = validate_soil_inputs(n, p, k, ph)
        if not s_ok:
            return {"success": False, "message": s_err}, 400

        # Validate environmental inputs
        e_ok, e_err = validate_environmental_inputs(temperature, humidity, rainfall)
        if not e_ok:
            return {"success": False, "message": e_err}, 400

        # Run inference
        prediction = predict_suitable_crop(
            float(n), float(p), float(k), 
            float(temperature), float(humidity), 
            float(ph), float(rainfall),
            soil_type, season
        )

        recommended_name = prediction["recommended_crop"]
        crop_info = Crop.query.filter(Crop.name.ilike(f"%{recommended_name}%")).first()

        # Save recommendation to DB
        new_record = CropRecommendation(
            farmer_id=farmer_id,
            recommended_crop=recommended_name,
            confidence_score=prediction["confidence_score"],
            alternative_crop_1=prediction.get("alternative_crop_1"),
            alternative_crop_2=prediction.get("alternative_crop_2"),
            explanation=prediction["explanation"],
            input_n=float(n),
            input_p=float(p),
            input_k=float(k),
            input_ph=float(ph),
            input_temp=float(temperature),
            input_humidity=float(humidity),
            input_rainfall=float(rainfall),
            soil_type=soil_type,
            season=season
        )
        db.session.add(new_record)
        db.session.commit()

        return {
            "success": True,
            "recommendation_id": new_record.id,
            "recommended_crop": recommended_name,
            "confidence_score": prediction["confidence_score"],
            "alternative_crop_1": prediction.get("alternative_crop_1"),
            "alternative_crop_2": prediction.get("alternative_crop_2"),
            "explanation": prediction["explanation"],
            "model_used": prediction.get("model_used", "AI Model"),
            "crop_details": crop_info.to_dict() if crop_info else None,
            "input_summary": {
                "n": float(n),
                "p": float(p),
                "k": float(k),
                "ph": float(ph),
                "temperature": float(temperature),
                "humidity": float(humidity),
                "rainfall": float(rainfall),
                "soil_type": soil_type,
                "season": season
            }
        }, 200
