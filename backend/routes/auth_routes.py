import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from database.db import db
from models.user import User
from models.farm import FarmerProfile
from utils.validators import validate_registration_data, validate_login_data

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new farmer or user."""
    data = request.get_json() or {}
    is_valid, error_msg = validate_registration_data(data)
    if not is_valid:
        return jsonify({"success": False, "message": error_msg}), 400

    email = data.get("email").strip().lower()
    phone = data.get("phone_number").strip()

    # Check for existing email or phone
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email is already registered."}), 409
    if User.query.filter_by(phone_number=phone).first():
        return jsonify({"success": False, "message": "Phone number is already registered."}), 409

    role = "admin" if data.get("role") == "admin" else "farmer"
    
    new_user = User(
        full_name=data.get("full_name").strip(),
        phone_number=phone,
        email=email,
        preferred_language=data.get("preferred_language", "en"),
        state=data.get("state").strip(),
        district=data.get("district").strip(),
        village=data.get("village", "").strip(),
        role=role
    )
    new_user.set_password(data.get("password"))

    db.session.add(new_user)
    db.session.flush()

    # Automatically initialize default farmer profile for farmers
    if role == "farmer":
        profile = FarmerProfile(
            user_id=new_user.id,
            farm_size=float(data.get("farm_size", 2.0)),
            soil_type=data.get("soil_type", "Loamy"),
            water_source=data.get("water_source", "Borewell"),
            irrigation_type=data.get("irrigation_type", "Drip Irrigation"),
            current_crop=data.get("current_crop", "Rice")
        )
        db.session.add(profile)

    db.session.commit()

    # Create JWT Access Token
    access_token = create_access_token(identity=str(new_user.id))

    return jsonify({
        "success": True,
        "message": "Registration successful! Welcome to Farmer Crop Advisory.",
        "access_token": access_token,
        "user": new_user.to_dict()
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user with email and password."""
    data = request.get_json() or {}
    is_valid, error_msg = validate_login_data(data)
    if not is_valid:
        return jsonify({"success": False, "message": error_msg}), 400

    email = data.get("email").strip().lower()
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    if not user.is_active:
        return jsonify({"success": False, "message": "Your account has been deactivated."}), 403

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Retrieve logged-in user details."""
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    return jsonify({
        "success": True,
        "user": user.to_dict()
    }), 200

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    """Generate a password reset token (student prototype workflow)."""
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()

    if not email:
        return jsonify({"success": False, "message": "Email is required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        # Avoid leaking user existence in production; for student prototype give helpful response
        return jsonify({
            "success": True,
            "message": "If this email is registered, password reset instructions have been dispatched."
        }), 200

    # Generate token valid for 1 hour
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Password reset token generated successfully.",
        "reset_token": token,  # Provided directly for local prototype testing
        "note": "In production, this token is sent exclusively via SMS/Email."
    }), 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """Reset password using generated token."""
    data = request.get_json() or {}
    token = data.get("token", "").strip()
    new_password = data.get("new_password", "").strip()

    if not token or not new_password:
        return jsonify({"success": False, "message": "Both reset token and new password are required."}), 400

    if len(new_password) < 6:
        return jsonify({"success": False, "message": "New password must be at least 6 characters long."}), 400

    user = User.query.filter_by(reset_token=token).first()
    if not user:
        return jsonify({"success": False, "message": "Invalid or unrecognized reset token."}), 400

    if user.reset_token_expiry and user.reset_token_expiry < datetime.utcnow():
        return jsonify({"success": False, "message": "Reset token has expired. Please request a new one."}), 400

    user.set_password(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Password has been successfully reset! You can now log in."
    }), 200
