import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models.disease import Disease, DiseasePrediction
from services.disease_service import DiseaseService
from services.pest_service import PestService

disease_bp = Blueprint("disease", __name__, url_prefix="/api/disease")

@disease_bp.route("/predict", methods=["POST"])
def upload_and_predict():
    """Uploads a leaf image and runs AI plant disease diagnosis."""
    farmer_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            farmer_id = int(identity)
    except Exception:
        farmer_id = None

    if "image" not in request.files:
        return jsonify({"success": False, "message": "No 'image' file part in request form-data."}), 400

    file = request.files["image"]
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")

    result, status_code = DiseaseService.process_and_diagnose_image(
        file_storage=file,
        upload_folder=upload_folder,
        farmer_id=farmer_id
    )

    return jsonify(result), status_code

@disease_bp.route("/history", methods=["GET"])
@jwt_required()
def get_prediction_history():
    """Retrieve disease scan history for authenticated farmer."""
    farmer_id = int(get_jwt_identity())
    records = DiseasePrediction.query.filter_by(farmer_id=farmer_id).order_by(DiseasePrediction.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(records),
        "history": [r.to_dict() for r in records]
    }), 200

@disease_bp.route("/knowledgebase", methods=["GET"])
def get_disease_knowledgebase():
    """List all documented crop diseases with symptoms and treatment protocols."""
    crop_filter = request.args.get("crop")
    query = Disease.query
    if crop_filter:
        query = query.filter(Disease.crop_name.ilike(f"%{crop_filter}%"))
    diseases = query.all()
    return jsonify({
        "success": True,
        "count": len(diseases),
        "diseases": [d.to_dict() for d in diseases]
    }), 200

@disease_bp.route("/image/<filename>", methods=["GET"])
def get_uploaded_image(filename):
    """Safely serves uploaded crop leaf images."""
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    return send_from_directory(upload_folder, filename)

@disease_bp.route("/pest-advisory", methods=["POST"])
def get_pest_advisory():
    """Diagnoses pest problems by crop, growth stage, and observed symptoms."""
    data = request.get_json() or {}
    crop = data.get("crop", "").strip()
    growth_stage = data.get("growth_stage", "")
    symptom = data.get("symptom", "")

    if not crop:
        return jsonify({"success": False, "message": "Crop name is required for pest advisory."}), 400

    result = PestService.diagnose_pest(crop, growth_stage, symptom)
    return jsonify(result), 200

@disease_bp.route("/pests", methods=["GET"])
def get_pest_catalog():
    """Returns catalog of known agricultural pests and symptoms."""
    catalog = PestService.get_catalog()
    return jsonify({
        "success": True,
        "count": len(catalog),
        "pests": catalog
    }), 200
