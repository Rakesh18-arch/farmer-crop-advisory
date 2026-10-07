from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from services.scheme_service import SchemeService

schemes_bp = Blueprint("schemes", __name__, url_prefix="/api/schemes")

@schemes_bp.route("", methods=["GET"])
def get_all_schemes():
    """Retrieve filtered government agricultural welfare schemes."""
    state = request.args.get("state")
    category = request.args.get("category")
    crop = request.args.get("crop")
    scheme_type = request.args.get("type")

    schemes = SchemeService.get_schemes(state=state, category=category, crop=crop, scheme_type=scheme_type)
    return jsonify({
        "success": True,
        "count": len(schemes),
        "schemes": schemes
    }), 200

@schemes_bp.route("/<int:scheme_id>", methods=["GET"])
def get_scheme_detail(scheme_id):
    """Retrieve full details of a specific government scheme."""
    scheme = SchemeService.get_scheme_by_id(scheme_id)
    if not scheme:
        return jsonify({"success": False, "message": "Government scheme not found."}), 404
    return jsonify({
        "success": True,
        "scheme": scheme
    }), 200

@schemes_bp.route("", methods=["POST"])
@jwt_required()
def create_scheme():
    """Admin-only: register a new government welfare scheme."""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role != "admin":
        return jsonify({"success": False, "message": "Administrative privileges required."}), 403

    data = request.get_json() or {}
    if not data.get("scheme_name") or not data.get("description"):
        return jsonify({"success": False, "message": "Scheme name and description are required."}), 400

    created, err = SchemeService.create_or_update_scheme(data)
    if err:
        return jsonify({"success": False, "message": err}), 400

    return jsonify({
        "success": True,
        "message": "Scheme registered successfully.",
        "scheme": created
    }), 201
