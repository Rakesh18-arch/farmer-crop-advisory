from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models.advisory import FertilizerRecommendation
from models.farm import FarmerProfile
from services.fertilizer_service import FertilizerService
from utils.validators import validate_soil_inputs

fertilizer_bp = Blueprint("fertilizer", __name__, url_prefix="/api/fertilizer")

@fertilizer_bp.route("/recommend", methods=["POST"])
def get_fertilizer_advisory():
    """Calculates fertilizer and organic recommendations based on soil deficits."""
    farmer_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            farmer_id = int(identity)
    except Exception:
        farmer_id = None

    data = request.get_json() or {}

    crop_name = data.get("crop_name", "").strip()
    if not crop_name:
        # Fall back to farmer current crop if available
        if farmer_id:
            profile = FarmerProfile.query.filter_by(user_id=farmer_id).first()
            if profile and profile.current_crop:
                crop_name = profile.current_crop

    if not crop_name:
        return jsonify({"success": False, "message": "Crop name is required for fertilizer advisory."}), 400

    # Soil nutrients
    if farmer_id:
        profile = FarmerProfile.query.filter_by(user_id=farmer_id).first()
        n = data.get("n", profile.n_value if profile else 80.0)
        p = data.get("p", profile.p_value if profile else 40.0)
        k = data.get("k", profile.k_value if profile else 40.0)
        ph = data.get("ph", profile.soil_ph if profile else 6.5)
        soil_type = data.get("soil_type", profile.soil_type if profile else "Loamy")
    else:
        n = data.get("n", 80.0)
        p = data.get("p", 40.0)
        k = data.get("k", 40.0)
        ph = data.get("ph", 6.5)
        soil_type = data.get("soil_type", "Loamy")

    # Validate inputs
    s_ok, s_err = validate_soil_inputs(n, p, k, ph)
    if not s_ok:
        return jsonify({"success": False, "message": s_err}), 400

    result = FertilizerService.calculate_fertilizer_advisory(
        crop_name=crop_name,
        n=float(n),
        p=float(p),
        k=float(k),
        ph=float(ph),
        soil_type=soil_type,
        farmer_id=farmer_id
    )

    return jsonify(result), 200

@fertilizer_bp.route("/history", methods=["GET"])
@jwt_required()
def get_fertilizer_history():
    """Retrieve history of fertilizer recommendations for authenticated farmer."""
    farmer_id = int(get_jwt_identity())
    records = FertilizerRecommendation.query.filter_by(farmer_id=farmer_id).order_by(FertilizerRecommendation.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(records),
        "history": [r.to_dict() for r in records]
    }), 200
