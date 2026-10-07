from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models.crop import Crop, CropRecommendation
from models.farm import FarmerProfile
from services.recommendation_service import RecommendationService

crop_bp = Blueprint("crop", __name__, url_prefix="/api/crop")

@crop_bp.route("/list", methods=["GET"])
def get_all_crops():
    """Retrieve master crop list."""
    category = request.args.get("category")
    query = Crop.query
    if category:
        query = query.filter_by(category=category)
    crops = query.order_by(Crop.name.asc()).all()
    return jsonify({
        "success": True,
        "count": len(crops),
        "crops": [c.to_dict() for c in crops]
    }), 200

@crop_bp.route("/<int:crop_id>", methods=["GET"])
def get_crop_details(crop_id):
    """Retrieve full details of a single crop."""
    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({"success": False, "message": "Crop not found."}), 404
    return jsonify({
        "success": True,
        "crop": crop.to_dict()
    }), 200

@crop_bp.route("/seasonal", methods=["GET"])
def get_crops_by_season():
    """Filter crops by growing season (Kharif, Rabi, Zaid, Perennial)."""
    season = request.args.get("season", "Kharif").capitalize()
    crops = Crop.query.filter(Crop.season.ilike(f"%{season}%")).all()
    return jsonify({
        "success": True,
        "season": season,
        "count": len(crops),
        "crops": [c.to_dict() for c in crops]
    }), 200

@crop_bp.route("/recommend", methods=["POST"])
def recommend_crop():
    """
    ML-Driven Crop Recommendation API.
    Can accept explicit values or fall back to authenticated farmer profile values.
    """
    # Check if user is authenticated (optional for guest experimentation)
    farmer_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            farmer_id = int(identity)
    except Exception:
        farmer_id = None

    data = request.get_json() or {}

    # If farmer is logged in and fields are omitted, use profile values
    if farmer_id:
        profile = FarmerProfile.query.filter_by(user_id=farmer_id).first()
        if profile:
            n = data.get("n", profile.n_value)
            p = data.get("p", profile.p_value)
            k = data.get("k", profile.k_value)
            ph = data.get("ph", profile.soil_ph)
            soil_type = data.get("soil_type", profile.soil_type)
        else:
            n = data.get("n", 80.0)
            p = data.get("p", 45.0)
            k = data.get("k", 40.0)
            ph = data.get("ph", 6.5)
            soil_type = data.get("soil_type", "Loamy")
    else:
        n = data.get("n", 80.0)
        p = data.get("p", 45.0)
        k = data.get("k", 40.0)
        ph = data.get("ph", 6.5)
        soil_type = data.get("soil_type", "Loamy")

    temperature = data.get("temperature", 25.0)
    humidity = data.get("humidity", 70.0)
    rainfall = data.get("rainfall", 120.0)
    season = data.get("season", "Kharif")

    response_data, status_code = RecommendationService.get_crop_recommendation(
        n=n, p=p, k=k,
        temperature=temperature,
        humidity=humidity,
        ph=ph,
        rainfall=rainfall,
        soil_type=soil_type,
        season=season,
        farmer_id=farmer_id
    )

    return jsonify(response_data), status_code

@crop_bp.route("/recommendations/history", methods=["GET"])
@jwt_required()
def get_recommendation_history():
    """List recommendation history for authenticated farmer."""
    farmer_id = int(get_jwt_identity())
    records = CropRecommendation.query.filter_by(farmer_id=farmer_id).order_by(CropRecommendation.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(records),
        "history": [r.to_dict() for r in records]
    }), 200

@crop_bp.route("/calendar", methods=["GET"])
def get_calendar():
    """Retrieve stage-by-stage crop calendar and agronomic tasks."""
    from services.calendar_service import CalendarService
    crop_name = request.args.get("crop", "Rice")
    result = CalendarService.get_crop_calendar(crop_name)
    return jsonify(result), 200

@crop_bp.route("/predict-yield", methods=["POST"])
def get_yield_estimate():
    """AI Harvest Yield Estimation API."""
    from services.yield_service import YieldService
    data = request.get_json() or {}
    crop = data.get("crop", "Rice")
    area = float(data.get("area_acres", 2.0))
    rain = float(data.get("rainfall", 120.0))
    temp = float(data.get("temperature", 28.0))
    n = float(data.get("n", 80.0))
    p = float(data.get("p", 40.0))
    k = float(data.get("k", 40.0))
    ph = float(data.get("ph", 6.5))
    season = data.get("season", "Kharif")
    fert = float(data.get("fertilizer_kg", 100.0))

    result = YieldService.calculate_estimated_yield(
        crop=crop, area_acres=area, rainfall=rain,
        temperature=temp, n=n, p=p, k=k, ph=ph,
        season=season, fertilizer_usage_kg=fert
    )
    return jsonify(result), 200

@crop_bp.route("/explain-recommendation", methods=["POST"])
def explain_recommendation():
    """Generates deep LLM-powered agronomic justification for recommended crop."""
    from services.llm_service import LLMService
    data = request.get_json() or {}
    crop = data.get("crop", "Rice")
    soil = {
        "nitrogen": data.get("n", 80),
        "phosphorus": data.get("p", 40),
        "potassium": data.get("k", 40),
        "ph": data.get("ph", 6.5),
        "soil_type": data.get("soil_type", "Alluvial"),
        "season": data.get("season", "Kharif")
    }
    weather = {
        "temperature": data.get("temperature", 28.0),
        "humidity": data.get("humidity", 70.0),
        "rainfall": data.get("rainfall", 200.0)
    }
    confidence = float(data.get("confidence", 0.95))

    report = LLMService.explain_crop_recommendation(crop, soil, weather, confidence)
    return jsonify({
        "success": True,
        **report
    }), 200
