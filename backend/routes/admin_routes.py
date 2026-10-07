import csv
import io
from datetime import datetime
from functools import wraps
from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from models.user import User
from models.farm import FarmerProfile, Farm
from models.crop import Crop, CropRecommendation
from models.disease import Disease, DiseasePrediction
from models.market import Market, MarketPrice
from models.advisory import (
    FertilizerRecommendation,
    IrrigationRecommendation,
    GovernmentScheme
)

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

def admin_required():
    """Custom decorator to verify admin privileges."""
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            user_id = int(get_jwt_identity())
            user = db.session.get(User, user_id)
            if not user or user.role != "admin":
                return jsonify({
                    "success": False,
                    "message": "Access denied. Administrator privileges required."
                }), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@admin_bp.route("/stats", methods=["GET"])
@admin_required()
def get_system_stats():
    """
    Returns platform-wide administrative statistics:
    farmer counts, advisory counts, disease scans, popular crops, system diagnostics.
    """
    total_farmers = User.query.filter_by(role="farmer").count()
    total_admins = User.query.filter_by(role="admin").count()
    total_recommendations = CropRecommendation.query.count()
    total_disease_scans = DiseasePrediction.query.count()
    total_fert_advisories = FertilizerRecommendation.query.count()
    total_irrig_advisories = IrrigationRecommendation.query.count()
    total_crops_catalog = Crop.query.count()
    total_diseases_catalog = Disease.query.count()
    total_schemes = GovernmentScheme.query.count()

    # Popular crops recommended
    popular_crops_raw = (
        db.session.query(
            CropRecommendation.recommended_crop,
            db.func.count(CropRecommendation.id).label("count")
        )
        .group_by(CropRecommendation.recommended_crop)
        .order_by(db.desc("count"))
        .limit(6)
        .all()
    )
    popular_crops = [{"crop": item[0], "count": item[1]} for item in popular_crops_raw]

    # Recent activity
    recent_recs = CropRecommendation.query.order_by(CropRecommendation.created_at.desc()).limit(5).all()
    recent_scans = DiseasePrediction.query.order_by(DiseasePrediction.created_at.desc()).limit(5).all()

    return jsonify({
        "success": True,
        "metrics": {
            "total_farmers": total_farmers,
            "total_admins": total_admins,
            "total_recommendations": total_recommendations,
            "total_disease_scans": total_disease_scans,
            "total_fert_advisories": total_fert_advisories,
            "total_irrig_advisories": total_irrig_advisories,
            "total_crops_catalog": total_crops_catalog,
            "total_diseases_catalog": total_diseases_catalog,
            "total_schemes": total_schemes
        },
        "popular_crops": popular_crops,
        "recent_recommendations": [r.to_dict() for r in recent_recs],
        "recent_scans": [s.to_dict() for s in recent_scans],
        "system_status": {
            "database": "online",
            "ml_crop_model": "loaded",
            "ml_yield_model": "loaded",
            "timestamp": datetime.utcnow().isoformat()
        }
    }), 200

@admin_bp.route("/farmers", methods=["GET"])
@admin_required()
def get_farmers_list():
    """
    List registered farmers with pagination and search filtering.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 15, type=int)
    q = request.args.get("q", "").strip()

    query = User.query.filter_by(role="farmer")

    if q:
        query = query.filter(
            db.or_(
                User.full_name.ilike(f"%{q}%"),
                User.email.ilike(f"%{q}%"),
                User.phone_number.ilike(f"%{q}%"),
                User.state.ilike(f"%{q}%"),
                User.district.ilike(f"%{q}%")
            )
        )

    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    farmers_data = []
    for user in pagination.items:
        user_dict = user.to_dict()
        profile = FarmerProfile.query.filter_by(user_id=user.id).first()
        if profile:
            user_dict["farm_size"] = profile.farm_size
            user_dict["soil_type"] = profile.soil_type
            user_dict["current_crop"] = profile.current_crop
            user_dict["water_source"] = profile.water_source
        else:
            user_dict["farm_size"] = None
            user_dict["soil_type"] = None
            user_dict["current_crop"] = None
            user_dict["water_source"] = None
        farmers_data.append(user_dict)

    return jsonify({
        "success": True,
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "farmers": farmers_data
    }), 200

@admin_bp.route("/farmers/<int:user_id>/toggle-status", methods=["PUT"])
@admin_required()
def toggle_farmer_status(user_id):
    """Enable or disable farmer account."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    if user.role == "admin":
        return jsonify({"success": False, "message": "Cannot deactivate administrative accounts."}), 400

    user.is_active = not user.is_active
    db.session.commit()
    status_str = "activated" if user.is_active else "deactivated"
    return jsonify({
        "success": True,
        "message": f"Farmer account successfully {status_str}.",
        "is_active": user.is_active
    }), 200

@admin_bp.route("/recommendations", methods=["GET"])
@admin_required()
def get_all_recommendations():
    """Retrieve all crop recommendations platform-wide with pagination."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    pagination = CropRecommendation.query.order_by(CropRecommendation.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "success": True,
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "recommendations": [r.to_dict() for r in pagination.items]
    }), 200

@admin_bp.route("/reports/<string:report_type>", methods=["GET"])
@admin_required()
def export_csv_report(report_type):
    """
    Generates and streams downloadable CSV reports:
    'farmers', 'recommendations', 'diseases', 'market_prices', 'schemes'
    """
    output = io.StringIO()
    writer = csv.writer(output)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{report_type}_{timestamp}.csv"

    if report_type == "farmers":
        writer.writerow(["User ID", "Full Name", "Email", "Phone", "State", "District", "Village", "Language", "Active", "Created At"])
        users = User.query.filter_by(role="farmer").order_by(User.id.asc()).all()
        for u in users:
            writer.writerow([u.id, u.full_name, u.email, u.phone_number, u.state, u.district, u.village, u.preferred_language, u.is_active, u.created_at])

    elif report_type == "recommendations":
        writer.writerow(["ID", "Farmer ID", "Recommended Crop", "Confidence", "Alternative 1", "Alternative 2", "N", "P", "K", "pH", "Temp", "Humidity", "Rainfall", "Season", "Date"])
        recs = CropRecommendation.query.order_by(CropRecommendation.id.desc()).all()
        for r in recs:
            writer.writerow([r.id, r.farmer_id, r.recommended_crop, r.confidence_score, r.alternative_crop_1, r.alternative_crop_2, r.input_n, r.input_p, r.input_k, r.input_ph, r.input_temp, r.input_humidity, r.input_rainfall, r.season, r.created_at])

    elif report_type == "diseases":
        writer.writerow(["ID", "Farmer ID", "Image Name", "Crop", "Detected Disease", "Confidence", "Date"])
        scans = DiseasePrediction.query.order_by(DiseasePrediction.id.desc()).all()
        for s in scans:
            writer.writerow([s.id, s.farmer_id, s.image_filename, s.detected_crop, s.detected_disease, s.confidence, s.created_at])

    elif report_type == "market_prices":
        writer.writerow(["ID", "Market", "State", "Commodity", "Variety", "Min Price", "Max Price", "Modal Price", "Recorded Date"])
        prices = MarketPrice.query.join(Market).order_by(MarketPrice.id.desc()).all()
        for p in prices:
            m_name = p.market.market_name if p.market else "N/A"
            m_state = p.market.state if p.market else "N/A"
            writer.writerow([p.id, m_name, m_state, p.commodity, p.variety, p.min_price, p.max_price, p.modal_price, p.price_date])

    elif report_type == "schemes":
        writer.writerow(["ID", "Scheme Name", "Category", "Target State", "Beneficiary Type", "Financial Benefit", "Portal URL"])
        schemes = GovernmentScheme.query.all()
        for sc in schemes:
            writer.writerow([sc.id, sc.scheme_name, sc.category, sc.target_state, sc.beneficiary_type, sc.financial_benefit, sc.official_portal_url])

    else:
        return jsonify({
            "success": False,
            "message": f"Unsupported report type '{report_type}'. Available: farmers, recommendations, diseases, market_prices, schemes."
        }), 400

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "text/csv; charset=utf-8"
        }
    )
