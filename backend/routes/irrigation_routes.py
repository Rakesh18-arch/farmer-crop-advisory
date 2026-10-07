from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models.advisory import IrrigationRecommendation
from models.farm import FarmerProfile
from services.irrigation_service import IrrigationService

irrigation_bp = Blueprint("irrigation", __name__, url_prefix="/api/irrigation")

@irrigation_bp.route("/recommend", methods=["POST"])
def get_irrigation_advisory():
    """Generates weather-aware smart irrigation schedule and water requirements."""
    farmer_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            farmer_id = int(identity)
    except Exception:
        farmer_id = None

    data = request.get_json() or {}

    # Defaults from profile if available
    profile = None
    if farmer_id:
        profile = FarmerProfile.query.filter_by(user_id=farmer_id).first()

    crop_name = data.get("crop_name") or (profile.current_crop if profile else "Rice")
    soil_type = data.get("soil_type") or (profile.soil_type if profile else "Loamy")
    soil_moisture = float(data.get("soil_moisture", profile.soil_moisture if profile else 45.0))
    temperature = float(data.get("temperature", 28.0))
    humidity = float(data.get("humidity", 65.0))
    rainfall_forecast = float(data.get("rainfall_forecast", 0.0))
    current_weather = data.get("current_weather", "Clear")
    growth_stage = data.get("growth_stage", "Vegetative")

    result = IrrigationService.calculate_irrigation_advisory(
        crop_name=crop_name,
        soil_type=soil_type,
        soil_moisture=soil_moisture,
        temperature=temperature,
        humidity=humidity,
        rainfall_forecast=rainfall_forecast,
        current_weather=current_weather,
        growth_stage=growth_stage,
        farmer_id=farmer_id
    )

    return jsonify(result), 200

@irrigation_bp.route("/history", methods=["GET"])
@jwt_required()
def get_irrigation_history():
    """Retrieve history of irrigation recommendations for authenticated farmer."""
    farmer_id = int(get_jwt_identity())
    records = IrrigationRecommendation.query.filter_by(farmer_id=farmer_id).order_by(IrrigationRecommendation.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(records),
        "history": [r.to_dict() for r in records]
    }), 200
