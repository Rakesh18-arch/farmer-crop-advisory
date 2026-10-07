from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from models.user import User
from models.farm import FarmerProfile, SoilRecord
from models.crop import CropHistory, CropRecommendation
from models.advisory import IrrigationRecommendation, FertilizerRecommendation
from models.notification import Notification
from utils.validators import validate_soil_inputs

farmer_bp = Blueprint("farmer", __name__, url_prefix="/api/farmer")

@farmer_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Retrieve farmer profile along with user profile data."""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    profile = FarmerProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        # Create empty profile if not yet initialized
        profile = FarmerProfile(user_id=user_id)
        db.session.add(profile)
        db.session.commit()

    return jsonify({
        "success": True,
        "user": user.to_dict(),
        "profile": profile.to_dict()
    }), 200

@farmer_bp.route("/profile", methods=["PUT", "POST"])
@jwt_required()
def update_profile():
    """Update agricultural profile details."""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    profile = FarmerProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = FarmerProfile(user_id=user_id)
        db.session.add(profile)

    data = request.get_json() or {}

    # Update basic user fields if provided
    if "full_name" in data:
        user.full_name = data["full_name"].strip()
    if "state" in data:
        user.state = data["state"].strip()
    if "district" in data:
        user.district = data["district"].strip()
    if "village" in data:
        user.village = data["village"].strip()
    if "preferred_language" in data:
        user.preferred_language = data["preferred_language"].strip()

    # Update farm parameters
    if "farm_size" in data:
        try:
            profile.farm_size = float(data["farm_size"])
        except ValueError:
            pass

    if "farm_location" in data:
        profile.farm_location = data["farm_location"]
    if "soil_type" in data:
        profile.soil_type = data["soil_type"]
    if "water_source" in data:
        profile.water_source = data["water_source"]
    if "irrigation_type" in data:
        profile.irrigation_type = data["irrigation_type"]
    if "current_crop" in data:
        profile.current_crop = data["current_crop"]
    if "previous_crops" in data:
        profile.previous_crops = data["previous_crops"]

    # Soil values update & validation
    n = data.get("n_value", profile.n_value)
    p = data.get("p_value", profile.p_value)
    k = data.get("k_value", profile.k_value)
    ph = data.get("soil_ph", profile.soil_ph)
    moisture = data.get("soil_moisture", profile.soil_moisture)

    is_valid, err_msg = validate_soil_inputs(n, p, k, ph, moisture)
    if not is_valid:
        return jsonify({"success": False, "message": err_msg}), 400

    profile.n_value = float(n)
    profile.p_value = float(p)
    profile.k_value = float(k)
    profile.soil_ph = float(ph)
    profile.soil_moisture = float(moisture)

    # Automatically save a periodic SoilRecord for historical soil tracking
    new_soil_record = SoilRecord(
        farmer_profile_id=profile.id,
        n=profile.n_value,
        p=profile.p_value,
        k=profile.k_value,
        ph=profile.soil_ph,
        moisture=profile.soil_moisture,
        notes="Profile soil parameters updated by farmer"
    )
    db.session.add(new_soil_record)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Farmer profile updated successfully.",
        "user": user.to_dict(),
        "profile": profile.to_dict()
    }), 200

@farmer_bp.route("/soil-analysis", methods=["GET"])
@jwt_required()
def get_soil_analysis():
    """Classifies soil metrics into LOW, NORMAL, HIGH and provides agronomic feedback."""
    user_id = int(get_jwt_identity())
    profile = FarmerProfile.query.filter_by(user_id=user_id).first()
    
    n = profile.n_value if profile else 80.0
    p = profile.p_value if profile else 40.0
    k = profile.k_value if profile else 40.0
    ph = profile.soil_ph if profile else 6.5
    moisture = profile.soil_moisture if profile else 45.0

    # Soil classification criteria based on ICAR / Agricultural guidelines
    def classify_nutrient(val, low_limit, high_limit):
        if val < low_limit:
            return "LOW", "Sub-optimal level. Supplementation advised."
        elif val > high_limit:
            return "HIGH", "Abundant level. Avoid excessive chemical dosage."
        else:
            return "NORMAL", "Ideal nutrient level for productive cultivation."

    n_status, n_desc = classify_nutrient(n, 50.0, 140.0)
    p_status, p_desc = classify_nutrient(p, 25.0, 60.0)
    k_status, k_desc = classify_nutrient(k, 30.0, 75.0)

    # pH classification
    if ph < 6.0:
        ph_status = "ACIDIC"
        ph_desc = "Acidic soil. Agricultural lime application recommended."
    elif ph > 7.8:
        ph_status = "ALKALINE"
        ph_desc = "Alkaline soil. Gypsum application or organic matter recommended."
    else:
        ph_status = "NEUTRAL (OPTIMAL)"
        ph_desc = "Optimal soil pH (6.0 - 7.8) for maximum macro & micro nutrient availability."

    # Moisture classification
    if moisture < 30.0:
        moisture_status = "DEFICIENT (DRY)"
        moisture_desc = "Soil moisture is critically low. Timely irrigation needed."
    elif moisture > 70.0:
        moisture_status = "SATURATED (WET)"
        moisture_desc = "Soil is water-logged. Ensure drainage to prevent root rot."
    else:
        moisture_status = "ADEQUATE"
        moisture_desc = "Adequate soil moisture for active crop transpiration."

    return jsonify({
        "success": True,
        "soil_analysis": {
            "nitrogen": {"value": n, "status": n_status, "explanation": n_desc, "unit": "kg/ha"},
            "phosphorus": {"value": p, "status": p_status, "explanation": p_desc, "unit": "kg/ha"},
            "potassium": {"value": k, "status": k_status, "explanation": k_desc, "unit": "kg/ha"},
            "ph": {"value": ph, "status": ph_status, "explanation": ph_desc, "unit": "pH scale"},
            "moisture": {"value": moisture, "status": moisture_status, "explanation": moisture_desc, "unit": "%"}
        },
        "soil_type": profile.soil_type if profile else "Loamy",
        "overall_health_score": round(
            (1.0 if n_status == "NORMAL" else 0.6) * 25 +
            (1.0 if p_status == "NORMAL" else 0.6) * 25 +
            (1.0 if k_status == "NORMAL" else 0.6) * 25 +
            (1.0 if "OPTIMAL" in ph_status else 0.6) * 25, 1
        )
    }), 200

@farmer_bp.route("/crop-history", methods=["GET"])
@jwt_required()
def get_crop_history():
    """List crop history for the logged-in farmer."""
    user_id = int(get_jwt_identity())
    histories = CropHistory.query.filter_by(farmer_id=user_id).order_by(CropHistory.year.desc()).all()
    return jsonify({
        "success": True,
        "count": len(histories),
        "history": [h.to_dict() for h in histories]
    }), 200

@farmer_bp.route("/crop-history", methods=["POST"])
@jwt_required()
def add_crop_history():
    """Add a new crop harvest record."""
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    crop_name = data.get("crop_name", "").strip()
    season = data.get("season", "Kharif").strip()
    year = data.get("year")

    if not crop_name or not year:
        return jsonify({"success": False, "message": "Crop name and year are required."}), 400

    try:
        year_int = int(year)
    except ValueError:
        return jsonify({"success": False, "message": "Year must be a valid integer."}), 400

    record = CropHistory(
        farmer_id=user_id,
        crop_name=crop_name,
        season=season,
        year=year_int,
        yield_achieved=float(data.get("yield_achieved", 0.0)) if data.get("yield_achieved") else None,
        area_cultivated=float(data.get("area_cultivated", 0.0)) if data.get("area_cultivated") else None,
        notes=data.get("notes", "")
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Crop history record saved successfully.",
        "record": record.to_dict()
    }), 201

@farmer_bp.route("/dashboard-summary", methods=["GET"])
@jwt_required()
def get_dashboard_summary():
    """Aggregates all key indicators for high-performance dashboard load."""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    profile = FarmerProfile.query.filter_by(user_id=user_id).first()

    # Latest crop recommendation
    latest_rec = CropRecommendation.query.filter_by(farmer_id=user_id).order_by(CropRecommendation.created_at.desc()).first()
    
    # Latest irrigation advisory
    latest_irrig = IrrigationRecommendation.query.filter_by(farmer_id=user_id).order_by(IrrigationRecommendation.created_at.desc()).first()
    
    # Unread notifications
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.created_at.desc()).limit(5).all()

    return jsonify({
        "success": True,
        "farmer_name": user.full_name if user else "Farmer",
        "location": f"{user.district}, {user.state}" if user else "Location",
        "current_crop": profile.current_crop if profile else "Not selected",
        "farm_size": profile.farm_size if profile else 0.0,
        "soil_type": profile.soil_type if profile else "Loamy",
        "soil_moisture": profile.soil_moisture if profile else 45.0,
        "latest_crop_recommendation": latest_rec.to_dict() if latest_rec else None,
        "latest_irrigation_advisory": latest_irrig.to_dict() if latest_irrig else None,
        "unread_notifications": [n.to_dict() for n in notifications],
        "notification_count": len(notifications)
    }), 200
